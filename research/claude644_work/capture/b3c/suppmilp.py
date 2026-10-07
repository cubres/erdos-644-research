"""Discovery: all-support bad-tuple MILP at a point (min capacity scale lambda); returns support + assignment.
Plus float vertex lists of P_D (qhull) for maximal supports (cached)."""
import numpy as np, itertools
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from scipy.spatial import HalfspaceIntersection
from fractions import Fraction as F
from supports import maximal_extension, is_bad
CELLS = [S for S in range(1, 127) if bin(S).count('1') <= 5]
CONF = [(k, k2) for k, S in enumerate(CELLS) for k2, T in enumerate(CELLS) if k2 > k and (S | T) == 127]
def support_milp(types, x, time_limit=30, lam_max=1.2):
    m = len(types); p = len(x)
    nz = 7*m; nc = len(CELLS); ny = p*nc; nvar = nz + nc + ny + 1; L = nvar - 1
    zi = lambda j, t: j*m + t; ui = lambda c: nz + c; yi = lambda i, c: nz + nc + i*nc + c
    rows = []; lo = []; hi = []
    def add(c, l, h): rows.append(c); lo.append(l); hi.append(h)
    for j in range(7): add({zi(j, t): 1 for t in range(m)}, 1, 1)
    for i in range(p):
        c = {yi(i, k): 1 for k in range(nc)}; c[L] = -float(x[i]); add(c, -np.inf, 0)
        for k in range(nc): add({yi(i, k): 1, ui(k): -lam_max*float(x[i])}, -np.inf, 0)
        for j in range(7):
            c = {yi(i, k): 1 for k, S in enumerate(CELLS) if S >> j & 1}
            for t in range(m): c[zi(j, t)] = -float(types[t][i])
            add(c, 0, np.inf)
    for k, k2 in CONF: add({ui(k): 1, ui(k2): 1}, -np.inf, 1)
    A = lil_matrix((len(rows), nvar))
    for r, c in enumerate(rows):
        for k, v in c.items(): A[r, k] = v
    integ = np.zeros(nvar); integ[:nz+nc] = 1
    ub = np.full(nvar, np.inf); ub[:nz+nc] = 1; ub[L] = lam_max
    obj = np.zeros(nvar); obj[L] = 1
    res = milp(c=obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integ,
               bounds=Bounds(np.zeros(nvar), ub), options={'time_limit': time_limit})
    if res.x is None: return None
    z = res.x
    asg = tuple(int(max(range(m), key=lambda t: z[zi(j, t)])) for j in range(7))
    used = [CELLS[k] for k in range(nc) if z[ui(k)] > 0.5]
    return res.fun, asg, used
_VC = {}
def vertices_float(maxcells):
    if maxcells in _VC: return _VC[maxcells]
    H = []
    for C in maxcells: H.append([1.0 if C >> j & 1 else 0.0 for j in range(7)] + [-1.0])
    for j in range(7):
        a = [0.0]*7; a[j] = -1.0; H.append(a + [0.0])
    hs = HalfspaceIntersection(np.array(H), np.full(7, 1/20))
    V = np.unique(np.round(hs.intersections, 9), axis=0)
    V = V[np.abs(V).sum(axis=1) > 1e-12]
    VR = tuple(tuple(F(float(v)).limit_denominator(2000) for v in row) for row in V)
    _VC[maxcells] = VR
    return VR
def support_template(types, x, time_limit=30):
    r = support_milp(types, x, time_limit)
    if r is None: return None
    lam, asg, used = r
    if lam > 1 + 1e-9: return None
    mx = maximal_extension(used)
    return lam, mx, asg
def support_milp_multi(scen, time_limit=20, lam_max=1.2):
    """scen: list of (types (m x 3), x (3)) sharing assignment and support.  min lambda."""
    m = len(scen[0][0]); p = 3; S = len(scen)
    nz = 7*m; nc = len(CELLS); ny = S*p*nc; nvar = nz + nc + ny + 1; L = nvar - 1
    zi = lambda j, t: j*m + t; ui = lambda c: nz + c; yi = lambda s, i, c: nz + nc + (s*p + i)*nc + c
    rows = []; lo = []; hi = []
    def add(c, l, h): rows.append(c); lo.append(l); hi.append(h)
    for j in range(7): add({zi(j, t): 1 for t in range(m)}, 1, 1)
    for s, (types, x) in enumerate(scen):
        for i in range(p):
            c = {yi(s, i, k): 1 for k in range(nc)}; c[L] = -float(x[i]); add(c, -np.inf, 0)
            for k in range(nc): add({yi(s, i, k): 1, ui(k): -lam_max*max(float(x[i]), 1e-9)}, -np.inf, 0)
            for j in range(7):
                c = {yi(s, i, k): 1 for k, Sc in enumerate(CELLS) if Sc >> j & 1}
                for t in range(m): c[zi(j, t)] = -float(types[t][i])
                add(c, 0, np.inf)
    for k, k2 in CONF: add({ui(k): 1, ui(k2): 1}, -np.inf, 1)
    A = lil_matrix((len(rows), nvar))
    for r, c in enumerate(rows):
        for k, v in c.items(): A[r, k] = v
    integ = np.zeros(nvar); integ[:nz+nc] = 1
    ub = np.full(nvar, np.inf); ub[:nz+nc] = 1; ub[L] = lam_max
    obj = np.zeros(nvar); obj[L] = 1
    res = milp(c=obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integ,
               bounds=Bounds(np.zeros(nvar), ub), options={'time_limit': time_limit})
    if res.x is None: return None
    z = res.x
    asg = tuple(int(max(range(m), key=lambda t: z[zi(j, t)])) for j in range(7))
    used = [CELLS[k] for k in range(nc) if z[ui(k)] > 0.5]
    return res.fun, asg, used
