"""ADAPTIVE PROOF SEARCH for Th(3) in the 3-super-class regime (balanced optional).
State: a list of types (type 0,1,2 = class minimisers of A,B,C), linear constraints (rows).  Facts used:
  * base: 0<=x_X<=3/2, 2x_X/3<=s_X<=min(x_X,1), minimiser t^X_X = s_X, types in [0,x], sum 1, tau>3/4,
    tau<=s-excess bounds (sum e >= tau), optional balanced e_i+e_j<=3/4, optional excess bound tau<=3/4+e_i;
  * class gap for every type and part: t_X <= 2x_X/3 or t_X >= s_X; every type strictly super-heavy somewhere
    (t_X >= 2x_X/3 + ETA_S for some X) -- pencil lemma otherwise;
  * tau*(C) >= tau: for a blocking map pi of the current types either some selection has
    sum_i (x_i - t^{sel(i)}_i) >= tau, or all selections are < tau and a NEW type w escapes pi
    (w_i <= t^r_i - ETA_W for all r with pi(r)=i);
  * templates T(a;b,b;c) (Lemma 7.63 on the Fano incidence) and V(s,t) must FAIL (strictly, by ETA_F).
DFS: at each node solve the LP (max strictness slack); infeasible -> exact certificate leaf; else find at the
LP point a feasible template (branch on its violated constraint) or a map with cost<tau (branch as above) or
a class-gap violation; if none: OPEN (a genuine counterexample to the menu at that point, up to the
unbranched facts).  Limits: max types, max nodes."""
import sys, itertools, json, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert')
ETA_S = F(1, 1000); ETA_W = F(1, 10**6)
args = dict(a.split('=') for a in sys.argv[1:])
BAL = int(args.get('bal', 1)); EXC = int(args.get('exc', 1)); MAXT = int(args.get('maxt', 7)); MAXN = int(args.get('maxn', 20000))
XMIN = F(args.get('xmin', '0')); ETA_F = F(args.get('etaf', '0'))   # template failure strictness (0 = plain strict)
TAUMIN = F(args.get('taumin', '3/4'))
P = 'ABC'
def R(d, rhs, strict=False): return ({k: F(v) for k, v in d.items() if F(v) != 0}, F(rhs), bool(strict))
def xv(i): return 'x' + P[i]
def sv(i): return 's' + P[i]
def tv(k, i): return sv(i) if k == i and k < 3 else f't{k}{P[i]}'
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PEN = [l for l in LINES if 6 in l]
def base_rows():
    rows = []
    for i in range(3):
        rows += [R({xv(i): -1}, -XMIN), R({xv(i): 1}, F(3, 2)), R({xv(i): F(2, 3), sv(i): -1}, 0),
                 R({sv(i): 1, xv(i): -1}, 0), R({sv(i): 1}, 1)]
    rows.append(R({'tau': -1}, -TAUMIN, TAUMIN == F(3, 4)))
    d = {'tau': 1}
    for i in range(3): d[xv(i)] = -1; d[sv(i)] = 1
    rows.append(R(d, 0))                              # tau <= sum e
    if BAL:
        for i, j in itertools.combinations(range(3), 2):
            rows.append(R({xv(i): 1, sv(i): -1, xv(j): 1, sv(j): -1}, F(3, 4)))
    if EXC:
        for i in range(3): rows.append(R({'tau': 1, xv(i): -1, sv(i): 1}, F(3, 4)))
    return rows
def type_rows(k):
    rows = []; s = {}
    for i in range(3):
        v = tv(k, i); s[v] = 1
        if not (k == i and k < 3): rows += [R({v: -1}, 0), R({v: 1, xv(i): -1}, 0)]
    rows += [R(s, 1), R({kk: -1 for kk in s}, -1)]
    return rows
def type_disj(k):
    """class-gap disjunctions and 'super-heavy somewhere' for type k"""
    D = []
    for i in range(3):
        if k == i and k < 3: continue
        v = tv(k, i)
        D.append((f'cls {k}{P[i]}', [[R({v: 1, xv(i): F(-2, 3)}, 0)], [R({v: -1, sv(i): 1}, 0)]]))
    if k >= 3:
        D.append((f'sh {k}', [[R({tv(k, i): -1, xv(i): F(2, 3)}, -ETA_S)] for i in range(3)]))
    return D
def T_alts(a, b, c):
    typ = {}
    for l in LINES: typ[l] = a if 6 not in l else None
    typ[PEN[0]] = b; typ[PEN[1]] = b; typ[PEN[2]] = c
    alts = set()
    for i in range(3):
        for q in range(7):
            d = {xv(i): F(2)}
            for l in LINES:
                if q in l: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) - 1
            alts.add(tuple(sorted(d.items())))
        d = {xv(i): F(4)}
        for l in LINES: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) - 1
        alts.add(tuple(sorted(d.items())))
    return [[R(dict(d), -ETA_F, True)] for d in sorted(alts)]
def V_alts(s, t):
    alts = []
    for i in range(3):
        alts.append([R({xv(i): 1, tv(s, i): -1, tv(t, i): -1}, -ETA_F, True)])
        alts.append([R({xv(i): 1, tv(s, i): F(-5, 4), tv(t, i): F(-1, 2)}, -ETA_F, True)])
    return alts
def lp(rows, VARS):
    IX = {v: j for j, v in enumerate(VARS)}; n = len(VARS); M = len(rows)
    A = np.zeros((M + 1, n + 1)); b = np.zeros(M + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, IX[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[M, n] = 1.0; b[M] = 1.0
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * (n + 1), method='highs')
    if res.status == 2: return -np.inf, None, None
    if res.status != 0: return None, None, None
    return -res.fun, dict(zip(VARS, res.x[:n])), -res.ineqlin.marginals
def exact_cert(rows, VARS):
    t, z, du = lp(rows, VARS)
    if t is None or t > 1e-9: return None
    if du is None:
        n = len(VARS); M = len(rows); IX = {v: j for j, v in enumerate(VARS)}
        Aeq = np.zeros((n + 1, M)); beq = np.zeros(n + 1)
        for k, (coef, rhs, st) in enumerate(rows):
            for v, c in coef.items(): Aeq[IX[v], k] = float(c)
            Aeq[n, k] = float(rhs)
        beq[n] = -1.0
        res = linprog(np.ones(M), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method='highs')
        if res.status != 0: return None
        return solve_exact(rows, VARS, [k for k in range(M) if res.x[k] > 1e-11], res.x, True)
    return solve_exact(rows, VARS, [k for k in range(len(rows)) if du[k] > 1e-11], du, False)
def solve_exact(rows, VARS, supp, du, nonstrict):
    import sympy as sp
    lam = sp.symbols('l0:%d' % len(supp))
    eqs = [sum(sp.Rational(rows[k][0].get(v, 0)) * lam[q] for q, k in enumerate(supp)) for v in VARS]
    if nonstrict: eqs.append(sum(sp.Rational(rows[k][1]) * lam[q] for q, k in enumerate(supp)) + 1)
    else: eqs.append(sum((1 if rows[k][2] else 0) * lam[q] for q, k in enumerate(supp)) - 1)
    sol = sp.linsolve(eqs, lam)
    if not sol: return None
    sol = list(sol)[0]
    free = set().union(*[e.free_symbols for e in sol])
    if free:
        guess = {lam[q]: sp.Rational(F(du[k]).limit_denominator(10**8)) for q, k in enumerate(supp)}
        sol = [e.subs({f: guess[f] for f in free}) for e in sol]
    L = [F(str(v)) for v in sol]
    if any(v < 0 for v in L): return None
    for v in VARS:
        if sum(l * rows[k][0].get(v, 0) for l, k in zip(L, supp)) != 0: return None
    val = sum(l * rows[k][1] for l, k in zip(L, supp)); sw = sum(l for l, k in zip(L, supp) if rows[k][2])
    return [(k, l) for k, l in zip(supp, L)] if (val < 0 or (val == 0 and sw > 0)) else None
def holds(r, z, tol=1e-9):
    val = sum(float(c) * z[k] for k, c in r[0].items())
    return val < float(r[1]) - tol if r[2] else val <= float(r[1]) + tol
def best_map(z, nt):
    """cheapest valid blocking map of the current types at point z: returns (cost, pi)"""
    x = [z[xv(i)] for i in range(3)]; T = [[z[tv(k, i)] for i in range(3)] for k in range(nt)]
    best = [None]
    def rec(k, caps, pi):
        c = sum(x) - sum(caps)
        if best[0] is not None and c >= best[0][0]: return
        if k == nt: best[0] = (c, tuple(pi)); return
        for i in range(3):
            if T[k][i] > 1e-7:
                c2 = list(caps); c2[i] = min(c2[i], T[k][i]); rec(k + 1, c2, pi + [i])
    rec(0, list(x), [])
    return best[0]
def map_selections_alts(pi, nt):
    used = sorted(set(pi)); alts = []
    for sel in itertools.product(*[[r for r in range(nt) if pi[r] == i] for i in used]):
        d = {'tau': 1}
        for i, r in zip(used, sel):
            d[xv(i)] = d.get(xv(i), 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append(d)
    return alts
STATS = {'nodes': 0, 'leaves': 0, 'certfail': 0, 'open': 0, 'maxtypes': 0}
OPEN = []; LEAVES = []
def vars_for(nt):
    V = [xv(i) for i in range(3)] + [sv(i) for i in range(3)] + ['tau']
    for k in range(nt):
        for i in range(3):
            v = tv(k, i)
            if v not in V: V.append(v)
    return V
def leaf(rows, nt, path):
    c = exact_cert(rows, vars_for(nt)); STATS['leaves'] += 1
    if c is None: STATS['certfail'] += 1; print("CERT FAIL", path[-3:], flush=True)
    else: LEAVES.append(path)
def dfs(rows, nt, done, path):
    STATS['nodes'] += 1; STATS['maxtypes'] = max(STATS['maxtypes'], nt)
    if STATS['nodes'] > MAXN: return
    VARS = vars_for(nt)
    t, z, du = lp(rows, VARS)
    if t is None: print("LP trouble", flush=True); STATS['open'] += 1; return
    if t <= 1e-9: leaf(rows, nt, path); return
    # 1) disjunctions (class gap / super-heavy / templates) not satisfied at z
    cand = []
    for k in range(nt):
        for nm, alts in type_disj(k):
            if nm in done: continue
            if not any(all(holds(r, z) for r in a) for a in alts): cand.append((nm, alts))
    if not cand:
        for a, b, c in itertools.product(range(nt), repeat=3):
            nm = f'T {a},{b},{c}'
            if nm in done or a == b: continue
            alts = T_alts(a, b, c)
            if not any(all(holds(r, z) for r in al) for al in alts): cand.append((nm, alts))
        for s_, t_ in itertools.permutations(range(nt), 2):
            nm = f'V {s_},{t_}'
            if nm in done: continue
            alts = V_alts(s_, t_)
            if not any(all(holds(r, z) for r in al) for al in alts): cand.append((nm, alts))
    if cand:
        # pick the disjunction with fewest LP-feasible alternatives (cap evaluation)
        best = None
        for nm, alts in cand[:40]:
            feas = [ai for ai, al in enumerate(alts) if (lambda tt: tt is not None and tt > 1e-9)(lp(rows + al, VARS)[0])]
            if best is None or len(feas) < len(best[2]): best = (nm, alts, feas)
            if len(feas) <= 1: break
        nm, alts, feas = best
        for ai, al in enumerate(alts):
            if ai in feas: dfs(rows + al, nt, done | {nm}, path + [(nm, ai)])
            else: leaf(rows + al, nt, path + [(nm, ai)])
        return
    # 2) blocking maps: tau*(current types) >= tau ?
    cost, pi = best_map(z, nt)
    if cost < z['tau'] - 1e-9:
        nm = f'map {pi}'
        sel = map_selections_alts(pi, nt)
        # branch A_j: selection j has cost >= tau
        for j, d in enumerate(sel):
            r = R({k: -v for k, v in d.items()}, 0)          # tau - cost <= 0   (d = tau - sum(x - t)) -> careful sign
            rr = R(d, 0)
            tt = lp(rows + [rr], VARS)[0]
            if tt is not None and tt > 1e-9: dfs(rows + [rr], nt, done, path + [(nm, j)])
            else: leaf(rows + [rr], nt, path + [(nm, j)])
        # branch B: all selections cost < tau and a new type escapes pi
        if nt >= MAXT:
            STATS['open'] += 1; OPEN.append((path + [(nm, 'new')], z)); print("OPEN (max types)", len(path), round(z['tau'], 4), flush=True); return
        k = nt; newrows = []
        for d in sel: newrows.append(R({kk: -v for kk, v in d.items()}, 0, True))   # cost - tau ... strict: tau - cost > 0
        newrows += type_rows(k)
        for r in range(nt):
            i = pi[r]; newrows.append(R({tv(k, i): 1, tv(r, i): -1}, -ETA_W))
        rows2 = rows + newrows
        tt = lp(rows2, vars_for(nt + 1))[0]
        if tt is not None and tt > 1e-9: dfs(rows2, nt + 1, done, path + [(nm, 'new')])
        else: leaf(rows2, nt + 1, path + [(nm, 'new')])
        return
    STATS['open'] += 1; OPEN.append((path, z))
    print("OPEN (all facts satisfied)", len(path), {k: round(v, 4) for k, v in z.items()}, flush=True)
rows0 = base_rows()
for k in range(3): rows0 += type_rows(k)
t0 = time.time()
dfs(rows0, 3, frozenset(), [])
print("ARGS", args, "STATS", STATS, "time %.1f" % (time.time() - t0), flush=True)
