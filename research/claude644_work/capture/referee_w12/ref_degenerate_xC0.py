"""REFEREE (w12): boundary case x_C = 0 (so s_C = 0).  There the identity map, the pair maps P(Y->X) (Z-rep
blocked at Z) and Lemma 0's map are INVALID (u_C = s_C - eps < 0), so the written proof does not cover it.
Question: does the CONCLUSION (some T(X;Y,Y;Z) or V(s,t) feasible) still hold there?  Exhaustive-ish random
search over the 5 free parameters (x_A, x_B, s_A, s_B, c) plus a hill climb on the worst template margin."""
import itertools, random, math
random.seed(12345)
def tau_star(x, types):
    """exact tau* for finitely many types over parts with capacities x (min over blocking assignments)."""
    p = len(x); best = math.inf
    for sigma in itertools.product(range(p), repeat=len(types)):
        u = list(x); ok = True
        for i in range(p):
            ts = [t[i] for t, s in zip(types, sigma) if s == i]
            if ts:
                m = min(ts)
                if m <= 0: ok = False; break
                u[i] = m          # approached from below
        if ok: best = min(best, sum(x) - sum(u))
    return best
def T_margin(x, a, b, c):
    """T(X;Y,Y;Z) with a = X-rep, b = Y-rep, c = Z-rep: min slack over parts (>= 0 iff feasible)"""
    m = math.inf
    for i in range(len(x)):
        m = min(m, 2*x[i]-2*a[i]-b[i], 2*x[i]-2*a[i]-c[i], 2*x[i]-2*b[i]-c[i], 4*x[i]-4*a[i]-2*b[i]-c[i])
    return m
def V_margin(x, s, t):
    m = math.inf
    for i in range(len(x)): m = min(m, x[i]-s[i]-t[i], x[i]-5*s[i]/4-t[i]/2)
    return m
def best_template(x, types):
    best = -math.inf
    for X, Y, Z in itertools.permutations(range(3)):
        best = max(best, T_margin(x, types[X], types[Y], types[Z]))
    for S, T_ in itertools.permutations(range(3), 2):
        best = max(best, V_margin(x, types[S], types[T_]))
    return best
def hyp_ok(x, sA, sB, c, tol=0):
    xA, xB = x[0], x[1]
    if not (2*xA/3 - tol <= sA <= min(1, xA) + tol and 2*xB/3 - tol <= sB <= min(1, xB) + tol): return False
    eA, eB = xA - sA, xB - sB
    if eA + eB > 3/4 + tol: return False
    cross = [(1 - sA, xB, sB), (1 - sB, xA, sA), (c, xA, sA), (1 - c, xB, sB)]
    for t, xi, si in cross:
        if t < -tol or t > xi + tol: return False
        if not (t <= 2*xi/3 + tol or t >= si - tol): return False
    return True
worst = None; cnt = 0; cnt_tau = 0
for it in range(400000):
    xA = random.uniform(0, 1.5); xB = random.uniform(0, 1.5)
    sA = random.uniform(2*xA/3, min(1, xA)); sB = random.uniform(2*xB/3, min(1, xB)); c = random.uniform(0, 1)
    x = (xA, xB, 0.0)
    if not hyp_ok(x, sA, sB, c): continue
    types = [(sA, 1 - sA, 0.0), (1 - sB, sB, 0.0), (c, 1 - c, 0.0)]
    cnt += 1
    ts = tau_star(x, types)
    if ts <= 3/4: continue
    cnt_tau += 1
    m = best_template(x, types)
    if worst is None or m < worst[0]: worst = (m, x, sA, sB, c, ts)
print('samples satisfying hypotheses:', cnt, ' with tau*>3/4:', cnt_tau)
print('worst best-template margin among tau*>3/4 samples:', worst)
# hill climb from the worst sample to minimise the best-template margin subject to tau* > 3/4 and hypotheses
if worst:
    m, x, sA, sB, c, ts = worst; cur = [x[0], x[1], sA, sB, c]; curm = m
    step = 0.05
    for rnd in range(20000):
        cand = [v + random.gauss(0, step) for v in cur]
        xA, xB, sA, sB, c = cand; x = (xA, xB, 0.0)
        if xA < 0 or xB < 0 or not hyp_ok(x, sA, sB, c): continue
        types = [(sA, 1 - sA, 0.0), (1 - sB, sB, 0.0), (c, 1 - c, 0.0)]
        if tau_star(x, types) <= 3/4 + 1e-9: continue
        mm = best_template(x, types)
        if mm < curm: cur, curm = cand, mm
        if rnd % 5000 == 4999: step *= 0.5
    xA, xB, sA, sB, c = cur; x = (xA, xB, 0.0); types = [(sA, 1 - sA, 0.0), (1 - sB, sB, 0.0), (c, 1 - c, 0.0)]
    print('hill-climb minimum of best-template margin:', curm, 'at x =', x, 'types =', types, 'tau* =', tau_star(x, types))
    print('(a NEGATIVE value would be a counterexample to the conclusion at x_C = 0)')
