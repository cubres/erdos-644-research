"""generalp: lazy-template MILP adversary for h super-heavy classes over p = h parts (no light parts).
Variables: x_i, sigma_i (class infima, 2x_i/3 <= sigma_i <= min(1,x_i)), tau > 3/4, class minimisers t^X
(t^X_X = sigma_X; cross traces in [0,2x_m/3] u [sigma_m, x_m]; sum = 1), class-level directional infima mu[X][Y].
Hypotheses (proved consequences of a minimal counterexample to Th):
  (F)  sum_i e_i >= tau                                    [free vector sigma - eps]
  (X)  excess: mode 'single': tau <= 3/4 + e_i for all i   [needs Th for h-1 classes];
               mode 'pair'  : tau <= 3/4 + e_i + e_j       [needs Th for h-2 classes; L+ when h = 4]
               mode 'none'
  (B)  every class-level blocking map costs >= tau (levels > 0).
Strategy (static): Fano arc colourings with minimiser rows + V(minimiser, minimiser) pairs.  The MILP looks for
an adversary (all templates fail by >= eta2).  INFEASIBLE => the static strategy provably works (float MILP;
exact certificate to be extracted separately).
usage: python3 adv4.py h excessmode [eta] [xmin]
"""
import itertools, sys, os, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H
LINES, PENCIL = H.LINES, H.PENCIL
M = 20.0
h = int(sys.argv[1]); mode = sys.argv[2]
eta = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-3
xmin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
eta2 = 1e-4
ETAS = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-3      # strict super-heaviness margin
CRIT = (sys.argv[6] == 'crit') if len(sys.argv) > 6 else False  # class-criticality vectors v^D

class Model:
    def __init__(s): s.nv = 0; s.lb = []; s.ub = []; s.integ = []; s.rows = []; s.lo = []; s.hi = []; s.names = []
    def var(s, lb=0.0, ub=10.0, integer=False, name=''):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.names.append(name); s.nv += 1
        return s.nv - 1
    def add(s, coefs, lo=-np.inf, hi=np.inf): s.rows.append(dict(coefs)); s.lo.append(lo); s.hi.append(hi)
    def solve(s, time_limit=600):
        A = lil_matrix((len(s.rows), s.nv))
        for k, r in enumerate(s.rows):
            for j, c in r.items(): A[k, j] += c
        return milp(c=np.zeros(s.nv), constraints=LinearConstraint(A.tocsr(), s.lo, s.hi), integrality=np.array(s.integ),
                    bounds=Bounds(s.lb, s.ub), options={'time_limit': time_limit, 'disp': False})

def arc_colourings(h):
    """maps lines -> classes (0..h-1) with every class an arc (no 3 concurrent lines), up to Fano automorphism
    (classes NOT renamed: classes are distinguishable)."""
    out = []; seen = set()
    for col in itertools.product(range(h), repeat=7):
        if col in seen: continue
        ok = all(len(set(col[l] for l in PENCIL[q])) > 1 for q in range(7))
        orbit = set()
        for lp in H.LPERMS:
            nc = [None]*7
            for i in range(7): nc[lp[i]] = col[i]
            orbit.add(tuple(nc))
        seen |= orbit
        if ok: out.append(col)
    return out
COLS = arc_colourings(h)
print("arc colourings (up to Fano aut):", len(COLS), flush=True)

m = Model()
x = [m.var(xmin, 1.5, name=f'x{i}') for i in range(h)]
sg = [m.var(0.0, 1.0, name=f's{i}') for i in range(h)]
tau = m.var(0.75 + eta, 3.0, name='tau')
for i in range(h):
    m.add({sg[i]: 1, x[i]: -2/3}, lo=0); m.add({sg[i]: 1, x[i]: -1}, hi=0)
# (F)
d = {tau: 1}
for i in range(h): d[x[i]] = -1; d[sg[i]] = 1
m.add(d, hi=0)
# (X)
if mode == 'single':
    for i in range(h): m.add({tau: 1, x[i]: -1, sg[i]: 1}, hi=0.75)
elif mode == 'pair':
    for i, j in itertools.combinations(range(h), 2): m.add({tau: 1, x[i]: -1, sg[i]: 1, x[j]: -1, sg[j]: 1}, hi=0.75)
# mu
mu = [[(sg[X] if X == Y else m.var(0.0, 1.0, name=f'mu{X}{Y}')) for Y in range(h)] for X in range(h)]
for X in range(h):
    for Y in range(h):
        if X != Y: m.add({mu[X][Y]: 1, x[Y]: -1}, hi=0)
# (B) class-level blocking maps
nmaps = 0
for pi in itertools.product(range(h), repeat=h):
    used = sorted(set(pi)); pre = {Y: [X for X in range(h) if pi[X] == Y] for Y in used}
    L = []
    for sel in itertools.product(*[pre[Y] for Y in used]):
        f = {tau: -1}
        for Y, X in zip(used, sel):
            f[x[Y]] = f.get(x[Y], 0) + 1; f[mu[X][Y]] = f.get(mu[X][Y], 0) - 1
        L.append((f, 0))
    for X in range(h):
        if pi[X] != X: L.append(({mu[X][pi[X]]: -1}, -1e-7))
    bs = [m.var(0, 1, integer=True) for _ in L]; m.add({b: 1 for b in bs}, lo=1)
    for b, (f, r) in zip(bs, L):
        g = dict(f); g[b] = g.get(b, 0) - M; m.add(g, lo=r - M)
    nmaps += 1
# minimisers
T = []; Z = []
for X in range(h):
    t = [m.var(0.0, 1.0, name=f't{X}{i}') for i in range(h)]
    m.add({v: 1 for v in t}, lo=1, hi=1)
    z = [m.var(0, 1, integer=True) for i in range(h)]
    for i in range(h):
        m.add({t[i]: 1, x[i]: -1}, hi=0)
        m.add({t[i]: 1, sg[i]: -1, z[i]: -M}, lo=-M)       # z=1 => t_i >= sigma_i
        m.add({t[i]: 1, x[i]: -2/3, z[i]: -M}, hi=0)       # z=0 => t_i <= 2x_i/3
    m.add({z[X]: 1}, lo=1); m.add({t[X]: 1, sg[X]: -1}, hi=0)   # minimiser: t_X = sigma_X
    w = [m.var(0, 1, integer=True) for i in range(h)]              # strictly super-heavy somewhere
    for i in range(h):
        m.add({w[i]: 1, z[i]: -1}, hi=0)
        m.add({t[i]: 1, x[i]: -2/3, w[i]: -M}, lo=ETAS - M)      # w=1 => t_i >= 2x_i/3 + ETAS
    m.add({v: 1 for v in w}, lo=1)
    for Y in range(h):
        if Y != X: m.add({t[Y]: 1, mu[X][Y]: -1}, lo=0)     # t in S_X => t_Y >= mu[X][Y]
    T.append(t); Z.append(z)
if CRIT:
    for D in range(h):
        v = [m.var(0.0, 1.5, name=f'v{D}{i}') for i in range(h)]
        for i in range(h): m.add({v[i]: 1, x[i]: -1}, hi=0)
        f = {vi: -1 for vi in v}
        for i in range(h): f[x[i]] = f.get(x[i], 0) + 1
        m.add(f, hi=0.75 + 1e-6)                                  # cost(v^D) <= 3/4 (+)
        for X in range(h):
            if X == D: continue
            # role X (minimiser of S_X) is blocked by v^D unless it lies in S_D (z^X_D = 1)
            bs = [m.var(0, 1, integer=True) for i in range(h)]
            m.add(dict([(b, 1) for b in bs] + [(Z[X][D], 1)]), lo=1)
            for i, b in enumerate(bs):
                m.add({v[i]: 1, T[X][i]: -1, b: M}, hi=M - 1e-6)   # b=1 => v_i <= t_i - 1e-6
print("maps", nmaps, "vars", m.nv, "rows", len(m.rows), "ETAS", ETAS, "CRIT", CRIT, flush=True)

def forms(key):
    L = []
    if key[0] == 'F':
        col = key[1]
        for i in range(h):
            rows = [T[col[l]][i] for l in range(7)]
            for q in range(7):
                f = {}
                for l in PENCIL[q]: f[rows[l]] = f.get(rows[l], 0) + 1
                f[x[i]] = f.get(x[i], 0) - 2; L.append((f, 0))
            f = {}
            for l in range(7): f[rows[l]] = f.get(rows[l], 0) + 1
            f[x[i]] = f.get(x[i], 0) - 4; L.append((f, 0))
    elif key[0] == 'V':
        a, b = key[1:]
        for i in range(h):
            L += [({T[a][i]: 1, T[b][i]: 1, x[i]: -1}, 0), ({T[a][i]: 1.25, T[b][i]: 0.5, x[i]: -1}, 0)]
    return L
def fail_any(lins):
    bs = [m.var(0, 1, integer=True) for _ in lins]
    m.add({b: 1 for b in bs}, lo=1)
    for b, (form, rhs) in zip(bs, lins):
        f = dict(form); f[b] = f.get(b, 0) - M; m.add(f, lo=rhs + eta2 - M)
KEYS = [('F', col) for col in COLS] + [('V', a, b) for a in range(h) for b in range(h) if a != b]
def feasible_at(Xs, key):
    return all(sum(c*Xs[v] for v, c in f.items()) <= r + eta2/2 for f, r in forms(key))
added = set()
t0 = time.time()
for it in range(400):
    res = m.solve()
    if res.status != 0:
        print("it", it, "status", res.status, res.message, "added", len(added), "time", round(time.time()-t0), flush=True)
        break
    Xs = res.x
    feas = [k for k in KEYS if k not in added and feasible_at(Xs, k)]
    xs = [round(Xs[v], 4) for v in x]; ss = [round(Xs[v], 4) for v in sg]
    print("it", it, "tau", round(Xs[tau], 4), "x", xs, "sigma", ss, "feasible templates", len(feas), "time", round(time.time()-t0), flush=True)
    if not feas:
        print("ADVERSARY FOUND (all templates fail):")
        for X in range(h): print("  t^%d" % X, [round(Xs[v], 4) for v in T[X]])
        print("  mu", [[round(Xs[mu[X][Y]], 4) for Y in range(h)] for X in range(h)])
        break
    for k in feas[:40]:
        fail_any(forms(k)); added.add(k)
