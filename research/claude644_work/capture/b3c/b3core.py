"""b3core: STANDARD-LIBRARY core shared by the certifier and the checker (Erdos 644, balanced 3-class regime).

Model (rank 1, three parts).  Variables z: x0,x1,x2 (capacities) = 0..2, g0,g1,g2 (class thresholds) = 3..5,
tau = 6, and revealed types t_k = (t_k0,t_k1,t_k2) at 7+3k.  A region is (ineqs, eqs): ineq (d, r) means
sum_k d[k] z_k <= r, eq (d, r) means equality.  All numbers are Fractions.

Templates: every bad tuple used is a SUPPORT template (maximal cells of a bad support on the 7 rows, row->type
assignment).  Per part i it is feasible iff w . (row loads in part i) <= x_i for every vertex w of
P_D = {w >= 0 : w(C) <= 1 for all cells C}  (LP duality; masses on cells).  Vertices are enumerated EXACTLY here.
"""
from fractions import Fraction as F
import itertools, json
X = lambda i: i
G = lambda i: 3 + i
TAU = 6
def T(k, i): return 7 + 3*k + i
Q34 = F(3, 4)
FULL = 127
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
FANO_CELLS = tuple(sorted(sum(1 << l for l, L in enumerate(LINES) if p not in L) for p in range(7)))
PATS = [p for p in itertools.product([0, 1], repeat=3) if any(p)]
# ---------------------------------------------------------------- region builders
def base_region(balanced=True, sorted_x=False, box=None, excess=False):
    """excess=True adds the EXCESS BOUND tau <= 3/4 + e_i = 3/4 + x_i - g_i (i=0,1,2) [notes_typeclosed, FULL_PROOF]"""
    C = []; E = []
    for i in range(3):
        C.append(({X(i): F(-1)}, F(0)))
        C.append(({X(i): F(1)}, F(3, 2)))
        C.append(({X(i): F(2, 3), G(i): F(-1)}, F(0)))
        C.append(({G(i): F(1), X(i): F(-1)}, F(0)))
        C.append(({G(i): F(1)}, F(1)))
    C.append(({TAU: F(-1)}, -Q34))
    C.append(({TAU: F(1), X(0): F(-1), X(1): F(-1), X(2): F(-1), G(0): F(1), G(1): F(1), G(2): F(1)}, F(0)))
    if balanced is True:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            C.append(({X(i): F(1), X(j): F(1), G(i): F(-1), G(j): F(-1)}, Q34))
    elif isinstance(balanced, str) and balanced.startswith('unb'):
        # UNBALANCED piece: e_i + e_j >= 3/4 for the pair named 'unbij' (the union of the balanced region and the
        # three unbalanced pieces is the whole 3-super-class regime)
        i, j = int(balanced[3]), int(balanced[4])
        C.append(({X(i): F(-1), X(j): F(-1), G(i): F(1), G(j): F(1)}, -Q34))
    if box is not None:
        lo, hi = box
        for i in range(3):
            C.append(({X(i): F(-1)}, -F(lo[i]))); C.append(({X(i): F(1)}, F(hi[i])))
    if excess:
        for i in range(3):
            C.append(({TAU: F(1), X(i): F(-1), G(i): F(1)}, Q34))
    if sorted_x:
        C.append(({X(0): F(1), X(1): F(-1)}, F(0))); C.append(({X(1): F(1), X(2): F(-1)}, F(0)))
    return C, E
def type_region(k):
    C = []; E = [({T(k, 0): F(1), T(k, 1): F(1), T(k, 2): F(1)}, F(1))]
    for i in range(3):
        C.append(({T(k, i): F(-1)}, F(0)))
        C.append(({T(k, i): F(1), X(i): F(-1)}, F(0)))
    return C, E
def pattern_region(k, pat):
    C = []
    for i in range(3):
        if pat[i]: C.append(({T(k, i): F(-1), G(i): F(1)}, F(0)))          # t_i >= g_i
        else: C.append(({T(k, i): F(1), X(i): F(-2, 3)}, F(0)))           # t_i <= 2x_i/3
    return C
def request_region(k, w):
    C = []
    for l in range(3):
        d = {T(k, l): F(1), X(l): F(-1)}
        for kk, vv in w[l].items(): d[kk] = d.get(kk, 0) + vv
        C.append(({a: b for a, b in d.items() if b != 0}, F(0)))
    return C
def neg(d): return {k: -v for k, v in d.items()}
# ---------------------------------------------------------------- supports and exact vertices
def is_bad_support(cells):
    return all((a | b) != FULL for a in cells for b in cells) and all(0 < c < FULL for c in cells)
def _solve(A, b):
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [a - f*bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]
_VCACHE = {}
def support_vertices(cells):
    """all vertices of P_D (exact).  A vertex w with support J (w_j>0 iff j in J) is the unique solution of |J|
    tight cell equations restricted to J; enumerate J and |J|-subsets of distinct restricted cells."""
    key = tuple(sorted(cells))
    if key in _VCACHE: return _VCACHE[key]
    V = set()
    for J in range(1, 128):
        idx = [j for j in range(7) if J >> j & 1]; k = len(idx)
        rc = sorted(set(c & J for c in cells if c & J))
        for S in itertools.combinations(rc, k):
            A = [[F(1) if (c >> j & 1) else F(0) for j in idx] for c in S]
            sol = _solve(A, [F(1)]*k)
            if sol is None or any(v <= 0 for v in sol): continue
            w = [F(0)]*7
            for j, v in zip(idx, sol): w[j] = v
            if all(sum(w[j] for j in range(7) if c >> j & 1) <= 1 for c in cells): V.add(tuple(w))
    V = sorted(V)
    _VCACHE[key] = V
    return V
def support_ineqs(cells, asg):
    out = []; seen = set()
    for w in support_vertices(cells):
        for i in range(3):
            d = {}
            for j in range(7):
                if w[j]: d[T(asg[j], i)] = d.get(T(asg[j], i), 0) + w[j]
            d[X(i)] = d.get(X(i), 0) - 1
            d = {a: b for a, b in d.items() if b != 0}
            key = tuple(sorted(d.items()))
            if key in seen: continue
            seen.add(key); out.append((d, F(0)))
    return out
def witness_support(hexstr):
    v = int(hexstr, 16)
    lose = [S for S in range(128) if not (v >> S) & 1]
    return tuple(sorted(S for S in lose if not any(T != S and (T & S) == S for T in lose)))
def template_support(tp, pairdata=None):
    """tp = ['F', asg] | ['P', [f, j, l]] | ['S', [cells, asg]]  ->  (cells, asg)"""
    kind, data = tp
    if kind == 'F': return FANO_CELLS, tuple(data)
    if kind == 'S': return tuple(data[0]), tuple(data[1])
    f, j, l = data
    hexstr, mask = pairdata['minimal_functions'][f]['witness']
    cells = witness_support(hexstr)
    asg = tuple(l if (mask >> r) & 1 else j for r in range(7))
    return cells, asg
# ---------------------------------------------------------------- certificates
def combo(cert, ineqs, eqs):
    y, ye = cert
    tot = {}; val = F(0)
    for r, c in y.items():
        if c < 0: return None, None
        d, rhs = ineqs[r]
        for k, v in d.items(): tot[k] = tot.get(k, 0) + c*v
        val += c*rhs
    for r, c in ye.items():
        d, rhs = eqs[r]
        for k, v in d.items(): tot[k] = tot.get(k, 0) + c*v
        val += c*rhs
    return {k: v for k, v in tot.items() if v != 0}, val
def check_max(cert, ineqs, eqs, d, h):
    tot, val = combo(cert, ineqs, eqs)
    return tot is not None and tot == {k: v for k, v in d.items() if v != 0} and val <= h
def strict_system(ineqs, eqs, d, h, n):
    """augmented system in variables (z, s=index n): P rows, -d.z + s <= -h, -tau + s <= -3/4 ; goal max s <= 0"""
    A = list(ineqs) + [({**neg(d), n: F(1)}, -h), ({TAU: F(-1), n: F(1)}, -Q34)]
    return A, list(eqs), {n: F(1)}, F(0)
def check_ineq(cert, ineqs, eqs, d, h, n):
    """cert = ['plain', y, ye] or ['strict', y, ye]"""
    kind, y, ye = cert
    if kind == 'plain': return check_max((y, ye), ineqs, eqs, d, h)
    A, E, dd, hh = strict_system(ineqs, eqs, d, h, n)
    return check_max((y, ye), A, E, dd, hh)
def check_empty(cert, ineqs, eqs, n):
    """cert = ['farkas', y, ye] (region empty) or ['tau', y, ye] (max tau <= 3/4 on region)"""
    kind, y, ye = cert
    if kind == 'farkas':
        tot, val = combo((y, ye), ineqs, eqs)
        return tot is not None and tot == {} and val < 0
    return check_max((y, ye), ineqs, eqs, {TAU: F(1)}, Q34)
