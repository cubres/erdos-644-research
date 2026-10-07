"""generalp: RIGID one-type-per-class MILP adversary (three_type_milp.py generalised).
Parts: h super-heavy parts 0..h-1 (each hosting exactly one type t^X, super-heavy there: t^X_X = sigma_X in
[2x_X/3 + ETAS, min(1,x_X)]) and L light parts h..h+L-1 (all traces <= 2x_l/3).  Cross traces at heavy parts obey
the class gap (<= 2x_m/3 or >= sigma_m).  tau*({t^0..t^{h-1}}) >= tau = 3/4 + eta encoded by ALL blocking maps.
Menu: Fano arc colourings (classes distinguishable, up to Fano automorphism) + ordered V pairs; every template must
FAIL by >= eta2 in some part.  INFEASIBLE => every such rigid family with tau* > 3/4 has a Fano or V bad tuple
[numerical; exact certificate via kclass_cert.py].  usage: kclass_milp.py h L eta [xmin] [menu: full|T|noV|fanoonly]
"""
import sys, os, itertools, numpy as np, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
h = int(sys.argv[1]); L = int(sys.argv[2]); eta = float(sys.argv[3])
xmin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
menu = sys.argv[5] if len(sys.argv) > 5 else 'full'
p = h + L; M = 20.0; ETAS = 1e-3; eta2 = 1e-4
class Model:
    def __init__(s): s.nv = 0; s.lb = []; s.ub = []; s.integ = []; s.rows = []; s.lo = []; s.hi = []
    def var(s, lb=0.0, ub=10.0, integer=False):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.nv += 1; return s.nv - 1
    def add(s, coefs, lo=-np.inf, hi=np.inf): s.rows.append(dict(coefs)); s.lo.append(lo); s.hi.append(hi)
    def solve(s, time_limit=3000):
        A = lil_matrix((len(s.rows), s.nv))
        for k, r in enumerate(s.rows):
            for j, c in r.items(): A[k, j] += c
        return milp(c=np.zeros(s.nv), constraints=LinearConstraint(A.tocsr(), s.lo, s.hi), integrality=np.array(s.integ),
                    bounds=Bounds(s.lb, s.ub), options={'time_limit': time_limit, 'disp': False})
def arc_colourings(h):
    out = []; seen = set()
    for col in itertools.product(range(h), repeat=7):
        if col in seen: continue
        ok = all(len(set(col[l] for l in H.PENCIL[q])) > 1 for q in range(7))
        orbit = set()
        for lp in H.LPERMS:
            nc = [None]*7
            for i in range(7): nc[lp[i]] = col[i]
            orbit.add(tuple(nc))
        seen |= orbit
        if ok: out.append(col)
    return out
m = Model()
x = [m.var(xmin, 1.5) for i in range(h)] + [m.var(xmin, 3.0) for l in range(L)]
sg = [m.var(0, 1) for i in range(h)]; tau = m.var(0.75 + eta, 3)
for i in range(h): m.add({sg[i]: 1, x[i]: -2/3}, lo=ETAS); m.add({sg[i]: 1, x[i]: -1}, hi=0)
T = []
for c in range(h):
    t = [m.var(0, 1) for i in range(p)]; m.add({v: 1 for v in t}, lo=1, hi=1)
    for i in range(p): m.add({t[i]: 1, x[i]: -1}, hi=0)
    m.add({t[c]: 1, sg[c]: -1}, lo=0, hi=0)
    for i in range(h):
        if i == c: continue
        z = m.var(0, 1, integer=True)
        m.add({t[i]: 1, sg[i]: -1, z: -M}, lo=-M); m.add({t[i]: 1, x[i]: -2/3, z: -M}, hi=0)
    for l in range(h, p): m.add({t[l]: 1, x[l]: -2/3}, hi=0)
    T.append(t)
def disj(lins):
    bs = [m.var(0, 1, integer=True) for _ in lins]; m.add({b: 1 for b in bs}, lo=1)
    for b, (f, r) in zip(bs, lins):
        g = dict(f); g[b] = g.get(b, 0) - M; m.add(g, lo=r - M)
nmaps = 0
for pi in itertools.product(range(p), repeat=h):
    used = sorted(set(pi)); pre = {i: [r for r in range(h) if pi[r] == i] for i in used}
    Ls = []
    for sel in itertools.product(*[pre[i] for i in used]):
        f = {tau: -1}
        for i, r in zip(used, sel): f[x[i]] = f.get(x[i], 0) + 1; f[T[r][i]] = f.get(T[r][i], 0) - 1
        Ls.append((f, 0))
    for r in range(h):
        if pi[r] != r: Ls.append(({T[r][pi[r]]: -1}, 0))
    disj(Ls); nmaps += 1
COLS = arc_colourings(h)
if menu == 'T':
    COLS = [c for c in COLS if sorted(c.count(k) for k in range(h)) == sorted([4, 2, 1] + [0]*(h-3))]
ntm = 0
if menu != 'noFano':
    for col in COLS:
        Ls = []
        for i in range(p):
            for q in range(7):
                f = {x[i]: -2}
                for l in H.PENCIL[q]: f[T[col[l]][i]] = f.get(T[col[l]][i], 0) + 1
                Ls.append((f, eta2))
            f = {x[i]: -4}
            for l in range(7): f[T[col[l]][i]] = f.get(T[col[l]][i], 0) + 1
            Ls.append((f, eta2))
        disj(Ls); ntm += 1
if menu not in ('noV', 'T', 'fanoonly'):
    for a, b in itertools.permutations(range(h), 2):
        Ls = []
        for i in range(p):
            Ls.append(({T[a][i]: 1, T[b][i]: 1, x[i]: -1}, eta2)); Ls.append(({T[a][i]: 1.25, T[b][i]: 0.5, x[i]: -1}, eta2))
        disj(Ls); ntm += 1
print("h", h, "L", L, "eta", eta, "xmin", xmin, "menu", menu, "maps", nmaps, "templates", ntm, "vars", m.nv, "rows", len(m.rows), flush=True)
t0 = time.time(); res = m.solve()
print("status", res.status, res.message, "time %.1f" % (time.time() - t0), flush=True)
if res.status == 0:
    X = res.x
    print("ADVERSARY: tau", round(X[tau], 5), "x", [round(X[v], 4) for v in x], "sigma", [round(X[v], 4) for v in sg])
    for c in range(h): print("  t^%d" % c, [round(X[v], 4) for v in T[c]])
    xs = [X[v] for v in x]; Ts = [[X[v] for v in T[c]] for c in range(h)]
    print("  check tau*", H.tau_star_fast(xs, Ts), "fano margin", H.fano_margin(xs, Ts)[0])
