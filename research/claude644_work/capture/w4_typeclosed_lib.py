"""Library for the continuous type-closed model (Erdos 644), typeclosed attack w4.

Conventions: rank r (types sum to r), capacities x (list), types = list of tuples.
All exact functions use Fractions / ints.  MILP functions (scipy HiGHS) are discovery only.
"""
from fractions import Fraction as F
import itertools, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- exact tau* for a finite type set ----------------
def tau_star(types, x):
    """Continuous transversal coefficient: N - sup{sum u : u free}, u free iff every type a has
    some i with a_i > u_i.  Enumerates blocking thresholds g_i (u_i -> g_i from below blocks
    types with a_i >= g_i, g_i >0), or u_i = x_i (blocks nothing).  Exact."""
    p = len(x); N = sum(x)
    types = [tuple(t) for t in types]
    if not types:
        return F(0)
    cand = [sorted(set(t[i] for t in types if t[i] > 0)) for i in range(p)]
    best = None
    def rec(i, alive, acc):
        nonlocal best
        # alive: types not yet blocked
        if i == p:
            if not alive:
                if best is None or acc > best: best = acc
            return
        # option: no block at i
        # prune: upper bound acc + sum of remaining x
        ub = acc + sum(x[i:])
        if best is not None and ub <= best: return
        rec(i+1, alive, acc + x[i])
        for g in cand[i]:
            nal = [t for t in alive if t[i] < g]
            rec(i+1, nal, acc + g)
    rec(0, types, F(0) if isinstance(x[0], F) else 0)
    if best is None:
        return None
    return N - best

def tau_star_witness(types, x):
    p=len(x); N=sum(x); types=[tuple(t) for t in types]
    cand=[sorted(set(t[i] for t in types if t[i]>0)) for i in range(p)]
    best=[None,None]
    def rec(i,alive,acc,gs):
        if i==p:
            if not alive and (best[0] is None or acc>best[0]): best[0]=acc; best[1]=list(gs)
            return
        if best[0] is not None and acc+sum(x[i:])<=best[0]: return
        rec(i+1,alive,acc+x[i],gs+[None])
        for g in cand[i]:
            rec(i+1,[t for t in alive if t[i]<g],acc+g,gs+[g])
    rec(0,types,0,[])
    return N-best[0], best[1]

# ---------------- two-type capacity functions (note Thm 7.69) ----------------
def load_cap42():
    raw = json.load(open(os.path.join(HERE, 'w4_tc_cap42_vertices.json')))
    return [[(F(u), F(v)) for u, v in f] for f in raw]

def pair_bad(a, b, x, cap42):
    """True iff some certified two-type function M has M(a_i,b_i) <= x_i for all i."""
    for f in cap42:
        ok = True
        for i in range(len(x)):
            if max(u*a[i] + v*b[i] for u, v in f) > x[i]:
                ok = False; break
        if ok: return True
    return False

def single_bad(a, x):
    return all(7*a[i] <= 4*x[i] for i in range(len(x)))

# ---------------- Fano ----------------
FANO_LINES = [frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]

# ---------------- general bad-tuple MILP (all bad supports at once) ----------------
CELLS = [S for S in range(1, 127) if bin(S).count('1') <= 5]

def bad_tuple_milp(types, x, time_limit=60, fixed_rows=None, verbose=False):
    """Discovery MILP: exists row->type assignment and cell masses per part with no covering pair.
    Returns (status, assignment, cells) ; status in 'BAD','NONE','UNKNOWN'."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    m = len(types); p = len(x)
    nz = 7*m; nc = len(CELLS); ny = p*nc
    nvar = nz + nc + ny
    zi = lambda j, t: j*m + t
    ui = lambda c: nz + c
    yi = lambda i, c: nz + nc + i*nc + c
    rows = []; lo = []; hi = []
    def add(coefs, l, h):
        rows.append(coefs); lo.append(l); hi.append(h)
    for j in range(7):
        add({zi(j, t): 1 for t in range(m)}, 1, 1)
    # symmetry breaking: type index nondecreasing
    for j in range(6):
        c = {}
        for t in range(m):
            c[zi(j, t)] = c.get(zi(j, t), 0) + t
            c[zi(j+1, t)] = c.get(zi(j+1, t), 0) - t
        add(c, -np.inf, 0)
    xf = [float(v) for v in x]
    for i in range(p):
        add({yi(i, c): 1 for c in range(nc)}, -np.inf, xf[i])
        for c in range(nc):
            add({yi(i, c): 1, ui(c): -xf[i]}, -np.inf, 0)
        for j in range(7):
            c = {yi(i, k): 1 for k, S in enumerate(CELLS) if S >> j & 1}
            for t in range(m):
                c[zi(j, t)] = -float(types[t][i])
            add(c, 0, np.inf)
    idx = {S: k for k, S in enumerate(CELLS)}
    for k, S in enumerate(CELLS):
        for k2, T in enumerate(CELLS):
            if k2 <= k: continue
            if S | T == 127:
                add({ui(k): 1, ui(k2): 1}, -np.inf, 1)
    if fixed_rows is not None:
        for j, t in enumerate(fixed_rows):
            add({zi(j, t): 1}, 1, 1)
    A = lil_matrix((len(rows), nvar))
    for r, c in enumerate(rows):
        for k, v in c.items(): A[r, k] = v
    integrality = np.zeros(nvar); integrality[:nz+nc] = 1
    ub = np.full(nvar, np.inf); ub[:nz+nc] = 1
    res = milp(c=np.zeros(nvar), constraints=LinearConstraint(A.tocsr(), lo, hi),
               integrality=integrality, bounds=Bounds(np.zeros(nvar), ub),
               options={'time_limit': time_limit, 'disp': verbose})
    if res.status == 0:
        z = res.x
        assign = [max(range(m), key=lambda t: z[zi(j, t)]) for j in range(7)]
        cells = {}
        for i in range(p):
            for k, S in enumerate(CELLS):
                if z[yi(i, k)] > 1e-9: cells[(i, S)] = z[yi(i, k)]
        return 'BAD', assign, cells
    if res.status == 2:
        return 'NONE', None, None
    return 'UNKNOWN', None, res.message

# ---------------- exact per-part capacity for a fixed support & row loads ----------------
def support_min_mass(parents, loads):
    """Exact min total parent mass covering row loads (list of 7 Fractions) for given parent cells
    (bitmasks). Uses scipy LP for discovery then verifies primal/dual exactly via rationalisation.
    Returns Fraction value or None if rational reconstruction fails."""
    from scipy.optimize import linprog
    P = list(parents); n = len(P)
    A = np.array([[-(1.0 if (C >> j) & 1 else 0.0) for C in P] for j in range(7)])
    b = np.array([-float(l) for l in loads])
    res = linprog(np.ones(n), A_ub=A, b_ub=b, bounds=(0, None), method='highs')
    if res.status != 0: return None
    for bound in (100, 1000, 100000, 10**7):
        y = [F(v).limit_denominator(bound) if v > 1e-12 else F(0) for v in res.x]
        w = [F(-v).limit_denominator(bound) if abs(v) > 1e-12 else F(0) for v in res.ineqlin.marginals]
        if any(v < 0 for v in y) or any(v < 0 for v in w): continue
        if any(sum(y[k] for k, C in enumerate(P) if C >> j & 1) < loads[j] for j in range(7)): continue
        if any(sum(w[j] for j in range(7) if C >> j & 1) > 1 for C in P): continue
        pv = sum(y); dv = sum(w[j]*loads[j] for j in range(7))
        if pv == dv: return pv
    return None

def bad_tuple_margin(types, x, time_limit=120, lam_max=3.0):
    """Discovery MILP: minimise lambda such that a bad 7-tuple exists with capacities lambda*x.
    lambda <= 1 <=> bad tuple at the true capacities.  Returns (lambda, assignment) or (None,msg)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    m = len(types); p = len(x)
    nz = 7*m; nc = len(CELLS); ny = p*nc
    nvar = nz + nc + ny + 1
    L = nvar - 1
    zi = lambda j, t: j*m + t
    ui = lambda c: nz + c
    yi = lambda i, c: nz + nc + i*nc + c
    rows = []; lo = []; hi = []
    def add(coefs, l, h): rows.append(coefs); lo.append(l); hi.append(h)
    for j in range(7): add({zi(j, t): 1 for t in range(m)}, 1, 1)
    for j in range(6):
        c = {}
        for t in range(m):
            c[zi(j, t)] = c.get(zi(j, t), 0) + t
            c[zi(j+1, t)] = c.get(zi(j+1, t), 0) - t
        add(c, -np.inf, 0)
    xf = [float(v) for v in x]
    for i in range(p):
        c = {yi(i, k): 1 for k in range(nc)}; c[L] = -xf[i]; add(c, -np.inf, 0)
        for k in range(nc): add({yi(i, k): 1, ui(k): -lam_max*xf[i]}, -np.inf, 0)
        for j in range(7):
            c = {yi(i, k): 1 for k, S in enumerate(CELLS) if S >> j & 1}
            for t in range(m): c[zi(j, t)] = -float(types[t][i])
            add(c, 0, np.inf)
    for k, S in enumerate(CELLS):
        for k2, T in enumerate(CELLS):
            if k2 > k and S | T == 127: add({ui(k): 1, ui(k2): 1}, -np.inf, 1)
    A = lil_matrix((len(rows), nvar))
    for r, c in enumerate(rows):
        for k, v in c.items(): A[r, k] = v
    integrality = np.zeros(nvar); integrality[:nz+nc] = 1
    ub = np.full(nvar, np.inf); ub[:nz+nc] = 1; ub[L] = lam_max
    obj = np.zeros(nvar); obj[L] = 1
    res = milp(c=obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integrality,
               bounds=Bounds(np.zeros(nvar), ub), options={'time_limit': time_limit})
    if res.x is None: return None, res.message
    z = res.x
    assign = [max(range(m), key=lambda t: z[zi(j, t)]) for j in range(7)]
    return res.fun, assign, res.status

def bad_tuple_milp_req(types, x, T, time_limit=120, max_actual=None, verbose=False):
    """Discovery MILP with REQUESTED rows: each row is an actual type or a requested row with load
    vector V (0<=V<=x) of deletion cost sum_i (x_i - V_i) <= T (valid when tau* > T: some admissible
    type f <= V exists).  All bad supports at once (cells of size <= 5, no covering pair).
    Returns (status, rows) where rows[j] = ('type', t) or ('req', [V_i]); cells dict."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    m = len(types); p = len(x)
    nz = 7*m; nr = 7; nv = 7*p; nc = len(CELLS); ny = p*nc
    zi = lambda j, t: j*m + t
    ri = lambda j: nz + j
    vi = lambda j, i: nz + nr + j*p + i
    ui = lambda c: nz + nr + nv + c
    yi = lambda i, c: nz + nr + nv + nc + i*nc + c
    nvar = nz + nr + nv + nc + ny
    rows = []; lo = []; hi = []
    def add(coefs, l, h): rows.append(coefs); lo.append(l); hi.append(h)
    xf = [float(v) for v in x]
    for j in range(7):
        c = {zi(j, t): 1 for t in range(m)}; c[ri(j)] = 1; add(c, 1, 1)
        for i in range(p): add({vi(j, i): 1, ri(j): -xf[i]}, -np.inf, 0)
        c = {vi(j, i): -1 for i in range(p)}; c[ri(j)] = sum(xf); add(c, -np.inf, float(T))
    # symmetry breaking on rows: requested rows last, types nondecreasing (index m for requested)
    for j in range(6):
        c = {}
        for t in range(m):
            c[zi(j, t)] = c.get(zi(j, t), 0) + t; c[zi(j+1, t)] = c.get(zi(j+1, t), 0) - t
        c[ri(j)] = c.get(ri(j), 0) + m; c[ri(j+1)] = c.get(ri(j+1), 0) - m
        add(c, -np.inf, 0)
    if max_actual is not None:
        pass
    for i in range(p):
        add({yi(i, k): 1 for k in range(nc)}, -np.inf, xf[i])
        for k in range(nc): add({yi(i, k): 1, ui(k): -xf[i]}, -np.inf, 0)
        for j in range(7):
            c = {yi(i, k): 1 for k, S in enumerate(CELLS) if S >> j & 1}
            for t in range(m): c[zi(j, t)] = -float(types[t][i])
            c[vi(j, i)] = -1
            add(c, 0, np.inf)
    for k, S in enumerate(CELLS):
        for k2, T2 in enumerate(CELLS):
            if k2 > k and S | T2 == 127: add({ui(k): 1, ui(k2): 1}, -np.inf, 1)
    A = lil_matrix((len(rows), nvar))
    for r, c in enumerate(rows):
        for k, v in c.items(): A[r, k] = v
    integrality = np.zeros(nvar); integrality[:nz+nr] = 1; integrality[nz+nr+nv:nz+nr+nv+nc] = 1
    ub = np.full(nvar, np.inf); ub[:nz+nr] = 1; ub[nz+nr+nv:nz+nr+nv+nc] = 1
    # objective: prefer many requested rows (fewer actual types)
    obj = np.zeros(nvar)
    for j in range(7): obj[ri(j)] = -1
    res = milp(c=obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integrality,
               bounds=Bounds(np.zeros(nvar), ub), options={'time_limit': time_limit, 'disp': verbose})
    if res.x is None:
        return ('NONE' if res.status == 2 else 'UNKNOWN'), None, None
    z = res.x; out = []
    for j in range(7):
        if z[ri(j)] > 0.5: out.append(('req', [z[vi(j, i)] for i in range(p)]))
        else: out.append(('type', max(range(m), key=lambda t: z[zi(j, t)])))
    cells = {(i, S): z[yi(i, k)] for i in range(p) for k, S in enumerate(CELLS) if z[yi(i, k)] > 1e-9}
    return 'BAD', out, cells
