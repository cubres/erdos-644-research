"""generalp: EXACT certificate for the rigid one-type-per-class theorem with h super-heavy classes and L 2/3-light
parts (generalises bal3/cert/three_type_cert.py; same leaf certificates: exact rational Motzkin multipliers).
Hypotheses (linear; strict rows marked):
  XMIN <= x_i; heavy x_X <= 3/2, light x_l <= 3;  s_X > 2x_X/3 (strict), s_X <= x_X, s_X <= 1;
  type t^X: t^X_X = s_X, 0 <= t^X_i <= x_i, sum_i t^X_i = 1, light traces t^X_l <= 2x_l/3;
  tau > 3/4 (strict);  class gap: t^X_m <= 2x_m/3 OR t^X_m >= s_m (m heavy, m != X);
  tau*({t^X}) >= tau: every blocking map pi (type r blocked at part pi(r)) has some selection of cost >= tau
  or is invalid (t^r_{pi(r)} <= 0).
Conclusion: some Fano arc colouring (classes distinguishable) or some ordered V pair is feasible in every part.
The DFS refutes the negation: every template fails (strictly) in some part; leaves are infeasible linear systems.
usage: kclass_cert.py h L [xmin fraction] [menu full|noV]  -> leaves json in genp/cert/"""
import sys, os, itertools, json, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H
h = int(sys.argv[1]); L = int(sys.argv[2]); XMIN = F(sys.argv[3]); menu = sys.argv[4]
MODE = sys.argv[5]   # 'frontier D'  -> sys.argv[6] = D ;  'worker k W' -> sys.argv[6] = k, sys.argv[7] = W
ARG1 = int(sys.argv[6]); ARG2 = int(sys.argv[7]) if len(sys.argv) > 7 else 0
TAG = f'kclass_h{h}_L{L}_x{str(XMIN).replace("/", "_")}_{menu}'
p = h + L
V = [f'x{i}' for i in range(p)] + [f's{X}' for X in range(h)] + [f't{X}_{i}' for X in range(h) for i in range(p) if i != X] + ['tau']
IX = {v: i for i, v in enumerate(V)}
def tv(r, i): return f's{i}' if r == i else f't{r}_{i}'
def row(d, rhs, strict=False): return ({k: F(v) for k, v in d.items() if v != 0}, F(rhs), strict)
def neg(d): return {k: -w for k, w in d.items()}
BASE = []
for i in range(p):
    BASE.append(row({f'x{i}': -1}, -XMIN)); BASE.append(row({f'x{i}': 1}, F(3, 2) if i < h else 3))
for X in range(h):
    BASE.append(row({f'x{X}': F(2, 3), f's{X}': -1}, 0, True))
    BASE.append(row({f's{X}': 1, f'x{X}': -1}, 0)); BASE.append(row({f's{X}': 1}, 1))
for r in range(h):
    s = {}
    for i in range(p):
        v = tv(r, i); s[v] = s.get(v, 0) + 1
        if r != i:
            BASE.append(row({v: -1}, 0)); BASE.append(row({v: 1, f'x{i}': -1}, 0))
            if i >= h: BASE.append(row({v: 1, f'x{i}': F(-2, 3)}, 0))
    BASE.append(row(s, 1)); BASE.append(row(neg(s), -1))
BASE.append(row({'tau': -1}, F(-3, 4), True))
DISJ = []
for r in range(h):
    for i in range(h):
        if r == i: continue
        v = tv(r, i)
        DISJ.append((f'gap {v}', [[row({v: 1, f'x{i}': F(-2, 3)}, 0)], [row({v: -1, f's{i}': 1}, 0)]]))
for pi in itertools.product(range(p), repeat=h):
    used = sorted(set(pi)); pre = {i: [r for r in range(h) if pi[r] == i] for i in used}
    alts = []
    for sel in itertools.product(*[pre[i] for i in used]):
        d = {'tau': 1}
        for i, r in zip(used, sel):
            d[f'x{i}'] = d.get(f'x{i}', 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append([row(d, 0)])
    for r in range(h):
        if pi[r] != r: alts.append([row({tv(r, pi[r]): 1}, 0)])
    DISJ.append((f'map {pi}', alts))
def arc_colourings(h):
    out = []; seen = set()
    for col in itertools.product(range(h), repeat=7):
        if col in seen: continue
        ok = all(len(set(col[l] for l in H.PENCIL[q])) > 1 for q in range(7))
        orbit = set()
        for lp_ in H.LPERMS:
            nc = [None]*7
            for i in range(7): nc[lp_[i]] = col[i]
            orbit.add(tuple(nc))
        seen |= orbit
        if ok: out.append(col)
    return out
COLS = arc_colourings(h)
def tmpl_F(col):
    alts = []
    for i in range(p):
        for q in range(7):
            d = {f'x{i}': -2}
            for l in H.PENCIL[q]: d[tv(col[l], i)] = d.get(tv(col[l], i), 0) + 1
            alts.append([row(neg(d), 0, True)])
        d = {f'x{i}': -4}
        for l in range(7): d[tv(col[l], i)] = d.get(tv(col[l], i), 0) + 1
        alts.append([row(neg(d), 0, True)])
    return alts
def tmpl_V(S, T):
    alts = []
    for i in range(p):
        s, t, xx = tv(S, i), tv(T, i), f'x{i}'
        for d in [{s: 1, t: 1, xx: -1}, {s: F(5, 4), t: F(1, 2), xx: -1}]:
            alts.append([row(neg(d), 0, True)])
    return alts
for col in COLS: DISJ.append((f'F {"".join(map(str, col))}', tmpl_F(col)))
if menu != 'noV':
    for S, T in itertools.permutations(range(h), 2): DISJ.append((f'V {S}{T}', tmpl_V(S, T)))
print("vars", len(V), "disjunctions", len(DISJ), "colourings", len(COLS), flush=True)
def eval_row(r, z):
    val = sum(float(c) * z[IX[k]] for k, c in r[0].items())
    return val < float(r[1]) - 1e-9 if r[2] else val <= float(r[1]) + 1e-9
def viol(alt, z):
    return max(sum(float(c) * z[IX[k]] for k, c in r[0].items()) - float(r[1]) for r in alt)
def lp(rows):
    n = len(V); Mr = len(rows)
    A = np.zeros((Mr + 1, n + 1)); b = np.zeros(Mr + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, IX[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[Mr, n] = 1.0; b[Mr] = 1.0
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * (n + 1), method='highs')
    if res.status == 2: return -np.inf, None, None
    return -res.fun, res.x, -res.ineqlin.marginals
def exact_cert(rows):
    t, z, du = lp(rows)
    if t > 1e-9: return None
    if du is None:
        return exact_cert_nonstrict([(c, r, False) for c, r, s in rows])
    supp = [k for k in range(len(rows)) if du[k] > 1e-11]
    return solve_exact(rows, supp, du)
def exact_cert_nonstrict(rows):
    n = len(V); Mr = len(rows)
    Aeq = np.zeros((n + 1, Mr)); beq = np.zeros(n + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): Aeq[IX[v], k] = float(c)
        Aeq[n, k] = float(rhs)
    beq[n] = -1.0
    res = linprog(np.ones(Mr), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * Mr, method='highs')
    if res.status != 0: return None
    supp = [k for k in range(Mr) if res.x[k] > 1e-11]
    return solve_exact(rows, supp, res.x, nonstrict=True)
def solve_exact(rows, supp, du, nonstrict=False):
    import sympy as sp
    lam = sp.symbols('l0:%d' % len(supp))
    eqs = []
    for v in V:
        eqs.append(sum(sp.Rational(rows[k][0].get(v, 0)) * lam[q] for q, k in enumerate(supp)))
    if nonstrict: eqs.append(sum(sp.Rational(rows[k][1]) * lam[q] for q, k in enumerate(supp)) + 1)
    else: eqs.append(sum((1 if rows[k][2] else 0) * lam[q] for q, k in enumerate(supp)) - 1)
    sol = sp.linsolve(eqs, lam)
    if not sol: return None
    sol = list(sol)[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    if free:
        guess = {lam[q]: sp.Rational(F(du[k]).limit_denominator(10**8)) for q, k in enumerate(supp)}
        sol = [e.subs({f: guess[f] for f in free}) for e in sol]
    Lm = [F(str(v)) for v in sol]
    if any(v < 0 for v in Lm): return None
    for v in V:
        if sum(l * rows[k][0].get(v, 0) for l, k in zip(Lm, supp)) != 0: return None
    val = sum(l * rows[k][1] for l, k in zip(Lm, supp)); sw = sum(l for l, k in zip(Lm, supp) if rows[k][2])
    if val < 0 or (val == 0 and sw > 0): return [(k, l) for k, l in zip(supp, Lm)]
    return None
STATS = {'leaves': 0, 'certfail': 0, 'cex': 0, 'nodes': 0}
LEAVES = []; FRONT = []
DD = {nm: alts for nm, alts in DISJ}
def leaf(rows, path):
    c = exact_cert(rows); STATS['leaves'] += 1
    if c is None: STATS['certfail'] += 1; print("CERT FAIL at", path, flush=True)
    else: LEAVES.append((path, c))
def dfs(rows, path):
    STATS['nodes'] += 1
    t, z, du = lp(rows)
    if t <= 1e-9: leaf(rows, path); return
    if MODE == 'frontier' and len(path) >= ARG1: FRONT.append(path); return
    # cheap heuristic: unsatisfied disjunction with fewest nearly-feasible alternatives (violation <= thr)
    best = None
    for name, alts in DISJ:
        if any(all(eval_row(r, z) for r in alt) for alt in alts): continue
        vs = sorted(viol(alt, z) for alt in alts)
        key = (sum(1 for v in vs if v <= 0.05), vs[0])
        if best is None or key < best[0]: best = (key, name, alts)
    if best is None:
        STATS['cex'] += 1; print("COUNTEREXAMPLE (all disjunctions satisfied):", path, [round(v, 5) for v in z], flush=True); return
    _, name, alts = best
    for ai, alt in enumerate(alts):
        tt, _, _ = lp(rows + alt)
        if tt > 1e-9: dfs(rows + alt, path + [(name, ai)])
        else: leaf(rows + alt, path + [(name, ai)])
    if STATS['nodes'] % 200 == 0: print("nodes", STATS['nodes'], "leaves", STATS['leaves'], "depth", len(path), flush=True)
t0 = time.time()
sys.setrecursionlimit(10000)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert'), exist_ok=True)
CDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert')
def rows_of(pth):
    R = list(BASE)
    for nm, ai in pth: R = R + DD[nm][ai]
    return R
if MODE == 'frontier':
    dfs(list(BASE), [])
    json.dump({'frontier': [[list(st) for st in pth] for pth in FRONT]}, open(os.path.join(CDIR, TAG + '_frontier.json'), 'w'))
    print("FRONTIER", len(FRONT), "nodes", STATS, "time %.1f" % (time.time() - t0), flush=True)
    OUT = TAG + f'_front{ARG1}.json'
else:
    FR = json.load(open(os.path.join(CDIR, TAG + '_frontier.json')))['frontier']
    mine = [pth for q, pth in enumerate(FR) if q % ARG2 == ARG1]
    for q, pth in enumerate(mine):
        pth = [(nm, ai) for nm, ai in pth]
        dfs(rows_of(pth), pth)
        print("worker", ARG1, "done", q + 1, "of", len(mine), "stats", STATS, "time %.1f" % (time.time() - t0), flush=True)
    OUT = TAG + f'_w{ARG1}of{ARG2}.json'
print("h", h, "L", L, "XMIN", XMIN, "menu", menu, "MODE", MODE, "stats", STATS, "time %.1f" % (time.time() - t0), flush=True)
json.dump({'h': h, 'L': L, 'xmin': str(XMIN), 'menu': menu, 'stats': STATS, 'vars': V,
           'leaves': [[pth, [[{kk: str(vv) for kk, vv in rows_of(pth)[k][0].items()}, str(rows_of(pth)[k][1]), rows_of(pth)[k][2], str(l)] for k, l in c]] for pth, c in LEAVES]},
          open(os.path.join(CDIR, OUT), 'w'))
