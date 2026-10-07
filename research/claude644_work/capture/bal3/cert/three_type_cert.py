"""EXACT certificate for the THREE-TYPE THEOREM (3 parts A,B,C; types alpha,beta,gamma with alpha the
minimiser of the class S_A of types super-heavy at A, etc.).
Hypotheses encoded (all linear):
  0 <= x_X (<= 3/2);  2x_X/3 <= s_X <= x_X, s_X <= 1;  alpha=(s_A,aB,aC), beta=(bA,s_B,bC), gamma=(cA,cB,s_C),
  entries >= 0, <= x, sums = 1;  tau > 3/4 (strict);
  class gap: each cross trace t_Y <= 2x_Y/3 OR t_Y >= s_Y;
  tau*({alpha,beta,gamma}) >= tau: for each of the 27 blocking maps pi (type r blocked at part pi(r)):
     OR_{selections} sum_{used i}(x_i - t^{sel(i)}_i) >= tau   OR   some t^r_{pi(r)} <= 0 (map invalid).
Conclusion: one of the six T(X;Y,Y;Z) colourings or six V(s,t) supports is feasible.
Method: DFS over disjunctions; each leaf is an infeasible linear system with strict rows, certified by an
exact rational Motzkin certificate (Fractions), multipliers found by HiGHS then solved exactly on the support.
usage: three_type_cert.py [xmin as fraction string, default 0] [bal 0/1]"""
import sys, itertools, json, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
XMIN = F(sys.argv[1]) if len(sys.argv) > 1 else F(0)
BAL = int(sys.argv[2]) if len(sys.argv) > 2 else 0
V = ['xA', 'xB', 'xC', 'sA', 'sB', 'sC', 'aB', 'aC', 'bA', 'bC', 'cA', 'cB', 'tau']
IX = {v: i for i, v in enumerate(V)}
P = 'ABC'
def tv(r, i):   # variable name of type r's trace at part i (r,i in 0..2)
    if r == i: return 's' + P[i]
    return 'abc'[r] + P[i]
# a row: (coef dict, rhs, strict)  meaning  coef.z < rhs (strict) or <= rhs
def row(d, rhs, strict=False): return ({k: F(v) for k, v in d.items() if v != 0}, F(rhs), strict)
BASE = []
for i in range(3):
    X = P[i]
    BASE.append(row({'x' + X: -1}, -XMIN))
    BASE.append(row({'x' + X: 1}, F(3, 2)))
    BASE.append(row({'x' + X: F(2, 3), 's' + X: -1}, 0))
    BASE.append(row({'s' + X: 1, 'x' + X: -1}, 0))
    BASE.append(row({'s' + X: 1}, 1))
for r in range(3):
    s = {}
    for i in range(3):
        v = tv(r, i); s[v] = s.get(v, 0) + 1
        if r != i:
            BASE.append(row({v: -1}, 0)); BASE.append(row({v: 1, 'x' + P[i]: -1}, 0))
    BASE.append(row(s, 1)); BASE.append(row({k: -w for k, w in s.items()}, -1))
BASE.append(row({'tau': -1}, F(-3, 4), True))
if BAL:
    for i, j in itertools.combinations(range(3), 2):
        BASE.append(row({'x' + P[i]: 1, 's' + P[i]: -1, 'x' + P[j]: 1, 's' + P[j]: -1}, F(3, 4)))
DISJ = []   # list of (name, [alternatives]); each alternative = list of rows (conjunction)
for r in range(3):
    for i in range(3):
        if r == i: continue
        v = tv(r, i)
        DISJ.append((f'cls {v}', [[row({v: 1, 'x' + P[i]: F(-2, 3)}, 0)], [row({v: -1, 's' + P[i]: 1}, 0)]]))
for pi in itertools.product(range(3), repeat=3):
    used = sorted(set(pi)); pre = {i: [r for r in range(3) if pi[r] == i] for i in used}
    alts = []
    for sel in itertools.product(*[pre[i] for i in used]):
        d = {'tau': 1}
        for i, r in zip(used, sel):
            d['x' + P[i]] = d.get('x' + P[i], 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append([row(d, 0)])                       # tau - cost <= 0
    for r in range(3):
        if pi[r] != r: alts.append([row({tv(r, pi[r]): 1}, 0)])   # t <= 0 : map invalid
    DISJ.append((f'map {pi}', alts))
def tmpl_T(X, Y, Z):
    alts = []
    for i in range(3):
        A, B, C, x = tv(X, i), tv(Y, i), tv(Z, i), 'x' + P[i]
        for d, rhs in [({A: 2, B: 1, x: -2}, 0), ({A: 2, C: 1, x: -2}, 0), ({B: 2, C: 1, x: -2}, 0), ({A: 4, B: 2, C: 1, x: -4}, 0)]:
            # violation: form > 0  <=>  -form < 0 strict
            dd = {}
            for k, w in d.items(): dd[k] = dd.get(k, 0) - w
            alts.append([row(dd, 0, True)])
    return alts
def tmpl_V(S, T):
    alts = []
    for i in range(3):
        s, t, x = tv(S, i), tv(T, i), 'x' + P[i]
        for d in [{s: 1, t: 1, x: -1}, {s: F(5, 4), t: F(1, 2), x: -1}]:
            dd = {}
            for k, w in d.items(): dd[k] = dd.get(k, 0) - w
            alts.append([row(dd, 0, True)])
    return alts
for X, Y, Z in itertools.permutations(range(3)): DISJ.append((f'T {P[X]}{P[Y]}{P[Z]}', tmpl_T(X, Y, Z)))
for S, T in itertools.permutations(range(3), 2): DISJ.append((f'V {P[S]}{P[T]}', tmpl_V(S, T)))
def eval_row(r, z):
    val = sum(float(c) * z[IX[k]] for k, c in r[0].items())
    return val < float(r[1]) - 1e-9 if r[2] else val <= float(r[1]) + 1e-9
def lp(rows):
    """max t s.t. strict rows: a.z + t <= b ; nonstrict a.z <= b ; t <= 1. returns (t*, z, duals)"""
    n = len(V); M = len(rows)
    A = np.zeros((M + 1, n + 1)); b = np.zeros(M + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, IX[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[M, n] = 1.0; b[M] = 1.0
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * (n + 1), method='highs')
    if res.status == 2: return -np.inf, None, None
    return -res.fun, res.x, -res.ineqlin.marginals
def exact_cert(rows):
    """exact Motzkin certificate: lam>=0 over rows, sum lam*a = 0, sum lam*b < 0 or (=0 and strict weight>0)"""
    t, z, du = lp(rows)
    if t > 1e-9: return None
    if du is None:
        # phase-1 infeasible even without strictness: find Farkas via LP on nonstrict relaxation with t fixed
        rows2 = [(c, r, False) for c, r, s in rows]
        return exact_cert_nonstrict(rows2)
    M = len(rows)
    supp = [k for k in range(M) if du[k] > 1e-11]
    return solve_exact(rows, supp, du)
def exact_cert_nonstrict(rows):
    # Farkas: min 0 s.t. ... use linprog on dual: find lam>=0, lam A = 0, lam b = -1
    n = len(V); M = len(rows)
    Aeq = np.zeros((n + 1, M)); beq = np.zeros(n + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): Aeq[IX[v], k] = float(c)
        Aeq[n, k] = float(rhs)
    beq[n] = -1.0
    res = linprog(np.ones(M), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method='highs')
    if res.status != 0: return None
    supp = [k for k in range(M) if res.x[k] > 1e-11]
    return solve_exact(rows, supp, res.x, nonstrict=True)
def solve_exact(rows, supp, du, nonstrict=False):
    import sympy as sp
    n = len(V)
    lam = sp.symbols('l0:%d' % len(supp))
    eqs = []
    for j, v in enumerate(V):
        eqs.append(sum(sp.Rational(rows[k][0].get(v, 0)) * lam[q] for q, k in enumerate(supp)))
    # normalisation
    if nonstrict:
        eqs.append(sum(sp.Rational(rows[k][1]) * lam[q] for q, k in enumerate(supp)) + 1)
    else:
        eqs.append(sum((1 if rows[k][2] else 0) * lam[q] for q, k in enumerate(supp)) - 1)
    sol = sp.linsolve(eqs, lam)
    if not sol: return None
    sol = list(sol)[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    if free:
        guess = {lam[q]: sp.Rational(F(du[k]).limit_denominator(10**8)) for q, k in enumerate(supp)}
        sol = [e.subs({f: guess[f] for f in free}) for e in sol]
    L = [F(str(v)) for v in sol]
    if any(v < 0 for v in L): return None
    # exact verification
    for v in V:
        if sum(l * rows[k][0].get(v, 0) for l, k in zip(L, supp)) != 0: return None
    val = sum(l * rows[k][1] for l, k in zip(L, supp))
    sw = sum(l for l, k in zip(L, supp) if rows[k][2])
    if val < 0 or (val == 0 and sw > 0):
        return [(k, l) for k, l in zip(supp, L)]
    return None
STATS = {'leaves': 0, 'certfail': 0, 'cex': 0}
LEAVES = []
def dfs(rows, depth, path):
    t, z, du = lp(rows)
    if t <= 1e-9:
        c = exact_cert(rows)
        STATS['leaves'] += 1
        if c is None:
            STATS['certfail'] += 1; print("CERT FAIL at", path, flush=True)
        else:
            LEAVES.append((path, c))
        return
    # choose unsatisfied disjunction with fewest LP-feasible alternatives
    best = None
    for name, alts in DISJ:
        if any(all(eval_row(r, z) for r in alt) for alt in alts): continue
        feas = []
        for ai, alt in enumerate(alts):
            tt, _, _ = lp(rows + alt)
            if tt > 1e-9: feas.append(ai)
        if best is None or len(feas) < len(best[2]): best = (name, alts, feas)
        if len(feas) <= 1: break
    if best is None:
        STATS['cex'] += 1; print("COUNTEREXAMPLE (all disjunctions satisfied):", path, list(z), flush=True); return
    name, alts, feas = best
    for ai, alt in enumerate(alts):
        if ai in feas: dfs(rows + alt, depth + 1, path + [(name, ai)])
        else:
            c = exact_cert(rows + alt); STATS['leaves'] += 1
            if c is None: STATS['certfail'] += 1; print("CERT FAIL (pruned) at", path + [(name, ai)], flush=True)
            else: LEAVES.append((path + [(name, ai)], c))
DD = {nm: alts for nm, alts in DISJ}
def rows_of(p):
    R = list(BASE)
    for nm, ai in p: R = R + DD[nm][ai]
    return R
t0 = time.time()
dfs(list(BASE), 0, [])
print("XMIN", XMIN, "BAL", BAL, "stats", STATS, "time %.1f" % (time.time() - t0), flush=True)
json.dump({'xmin': str(XMIN), 'bal': BAL, 'stats': STATS,
           'leaves': [[[(nm, ai, [[{k: str(v) for k, v in r[0].items()}, str(r[1]), r[2]] for r in DD[nm][ai]]) for nm, ai in p],
                       [[{kk: str(vv) for kk, vv in rows_of(p)[k][0].items()}, str(rows_of(p)[k][1]), rows_of(p)[k][2], str(l)] for k, l in c]]
                      for p, c in LEAVES]},
          open(f'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert/three_type_leaves_x{str(XMIN).replace("/", "_")}_b{BAL}.json', 'w'))
