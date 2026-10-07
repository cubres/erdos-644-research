"""Fast float versions (numpy) of tau*, class structure, triple-window value, Fano margin, pair margin (42 fns) and
the general support margin for climbs (wave typeclosed3).  Exactness is restored afterwards by badcheck.py.
"""
import itertools, json, sys
import numpy as np

HERE = '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/'
sys.path.insert(0, HERE)
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def tau_star_f(K, x):
    """K: n x p float array, x: p.  Exact threshold enumeration (min cost over blocking t), p = 3 assumed."""
    K = np.asarray(K); x = np.asarray(x)
    n, p = K.shape
    best = np.inf
    c0 = sorted(set(K[:, 0][K[:, 0] > 0])) + [None]
    c1 = sorted(set(K[:, 1][K[:, 1] > 0])) + [None]
    for t0 in c0:
        b0 = (K[:, 0] >= t0 - 1e-15) if t0 is not None else np.zeros(n, bool)
        cost0 = x[0] - t0 if t0 is not None else 0.0
        if cost0 >= best:
            continue
        for t1 in c1:
            b1 = (K[:, 1] >= t1 - 1e-15) if t1 is not None else np.zeros(n, bool)
            cost1 = cost0 + (x[1] - t1 if t1 is not None else 0.0)
            if cost1 >= best:
                continue
            unb = ~(b0 | b1)
            if not unb.any():
                best = min(best, cost1)
                continue
            r = K[unb, 2]
            if (r <= 0).any():
                continue
            t2 = r.min()
            best = min(best, cost1 + x[2] - t2)
    return best


def classes_f(K, x):
    K = np.asarray(K); x = np.asarray(x)
    return [np.where(K[:, i] > 2 * x[i] / 3)[0] for i in range(3)]


def superheavy_margin(K, x):
    """min over types of max_i (c_i - 2x_i/3)/x_i : > 0 iff every type strictly super-heavy somewhere"""
    K = np.asarray(K); x = np.asarray(x)
    return ((K - 2 * x / 3) / x).max(1).min()


def triple_window_value(K, x):
    """min over class triples of |a v b v c| - (N - 3/4); <= 0 iff a triple window exists; inf if a class is empty"""
    K = np.asarray(K); x = np.asarray(x)
    S = classes_f(K, x)
    if any(len(s) == 0 for s in S):
        return np.inf
    N = x.sum()
    A = K[S[0]][:, None, None, :]
    B = K[S[1]][None, :, None, :]
    C = K[S[2]][None, None, :, :]
    J = np.maximum(np.maximum(A, B), C).sum(-1)
    return J.min() - (N - 0.75)


_TT = None


def load_tt_f():
    global _TT
    if _TT is None:
        from fractions import Fraction as Fr
        d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'))
        _TT = [np.array([[float(Fr(u)), float(Fr(v))] for u, v in d[k]['record']['vertices']]) for k in sorted(d, key=int)]
    return _TT


def pair_margin_f(K, x):
    """min over ordered pairs (a != b) and the 42 functions of max over parts/vertices of (u a_i + v b_i - x_i)/x_i"""
    K = np.asarray(K); x = np.asarray(x)
    TT = load_tt_f()
    n = len(K)
    best = np.inf
    for shape in TT:                      # shape: k x 2
        # value[a,b] = max over parts, vertices ( u*K[a,i] + v*K[b,i] - x_i ) / x_i
        u = shape[:, 0][:, None, None, None]
        v = shape[:, 1][:, None, None, None]
        val = (u * K[None, :, None, :] + v * K[None, None, :, :] - x) / x     # k x n x n x p
        m = val.max(axis=(0, 3))
        np.fill_diagonal(m, np.inf)
        best = min(best, m.min())
    return best


_REPS = {}


def fano_reps(n):
    """all assignments of n types to the 7 Fano points modulo the Fano automorphism group (168) -- as an array."""
    if n in _REPS:
        return _REPS[n]
    perms = []
    for p in itertools.permutations(range(7)):
        if all(tuple(sorted(p[i] for i in l)) in set(tuple(sorted(l2)) for l2 in LINES) for l in LINES):
            perms.append(p)
    assert len(perms) == 168
    seen = set()
    reps = []
    for a in itertools.product(range(n), repeat=7):
        if a in seen:
            continue
        orbit = {tuple(a[p[i]] for i in range(7)) for p in perms}
        seen |= orbit
        reps.append(a)
    R = np.array(reps, dtype=np.int64)
    _REPS[n] = R
    return R


def fano_margin_f(K, x, eta=1e-4):
    """min over all Fano assignments (mod automorphisms) of max normalised violation of Lemma 7.63 in any part.
    For n >= 8 types: DFS feasibility at capacities x(1+eta) only; returns eta if infeasible, -1 if feasible."""
    K = np.asarray(K); x = np.asarray(x)
    n = len(K)
    if n >= 8:
        from tc3lib import fano_search
        Kl = [tuple(float(v) for v in c) for c in K]
        xl = [float(v) * (1 + eta) for v in x]
        return -1.0 if fano_search(Kl, xl) is not None else eta
    R = fano_reps(n)
    best = np.inf
    for i in range(len(x)):
        pass
    Z = K[R]                                   # nA x 7 x p
    tot = (Z.sum(1) - 4 * x) / x              # nA x p
    worst = tot.max(1)
    for l in LINES:
        s = (Z[:, l[0], :] + Z[:, l[1], :] + Z[:, l[2], :] - 2 * x) / x
        worst = np.maximum(worst, s.max(1))
    return worst.min()


def general_margin_f(K, x, supports, limit=None):
    """min over supports/assignments of max_i (M_D(z^i) - x_i)/x_i (float branch and bound)."""
    from badcheck import margin_general
    return margin_general(K, x, supports, limit)[0]


_ASSIGN = {}


def all_assignments(n):
    if n not in _ASSIGN:
        _ASSIGN[n] = np.array(list(itertools.product(range(n), repeat=7)), dtype=np.int64)
    return _ASSIGN[n]


def pareto_vertices(Vf):
    """keep only vertices not dominated componentwise by another vertex (only these can attain max v.z, z >= 0)"""
    keep = []
    for i in range(len(Vf)):
        dom = False
        for j in range(len(Vf)):
            if i != j and (Vf[j] >= Vf[i]).all() and (Vf[j] > Vf[i]).any():
                dom = True
                break
        if not dom:
            keep.append(i)
    return Vf[keep]


_PV = {}


def general_margin_vec(K, x, supports, return_witness=False, chunk=300000):
    """float: min over the 715 supports and ALL n^7 row assignments of max_i (M_D(z^i) - x_i)/x_i, vectorised
    (per-part BLAS matmul against the Pareto-maximal dual vertices).  supports: badcheck.load_supports()."""
    K = np.asarray(K, dtype=float); x = np.asarray(x, dtype=float)
    n, p = K.shape
    A = all_assignments(n)
    best = np.inf; wit = None
    for si, (cells, V, Vf) in enumerate(supports):
        if si not in _PV:
            _PV[si] = np.ascontiguousarray(pareto_vertices(Vf).T)     # 7 x nv'
        PT = _PV[si]
        for s in range(0, len(A), chunk):
            Ac = A[s:s + chunk]
            m = np.full(len(Ac), -np.inf)
            for i in range(p):
                Zi = K[:, i][Ac]                          # nA x 7
                Mi = (Zi @ PT).max(1)                     # nA
                m = np.maximum(m, (Mi - x[i]) / x[i])
            k = m.argmin()
            if m[k] < best:
                best = m[k]; wit = (si, tuple(int(v) for v in Ac[k]))
    return (best, wit) if return_witness else best
