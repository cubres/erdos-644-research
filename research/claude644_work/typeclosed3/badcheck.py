"""Exact / float bad-7-tuple checkers for finite type families over p parts (wave typeclosed3).

A bad 7-tuple = rows c^1..c^7 in K + a support D (downset of cells with no two cells covering [7]) + per-part masses.
By LP duality per part (Lemma 7.63 mechanism / Theorem 7.69), for a fixed support D with dual vertex list V_D
(supports715.json) and fixed row types, the tuple is realisable iff  max_{v in V_D} v . z^i <= x_i  for every part i,
where z^i_j = c^{row j}_i.  All 715 non-dictator maximal supports are complete (note Lemma 7.65), so
   K has a bad 7-tuple  <=>  exists D in catalogue, exists rows [7] -> K with M_D(z^i) <= x_i for all i.
Checkers:
  two_type_bad(K, x, tol)      the 42 Theorem 7.69 functions on all ordered pairs (exact with Fractions)
  fano_bad(K, x, tol)          tc3lib.fano_search (all assignments, pruned)
  general_bad(K, x, tol, ...)  DFS over rows for every support with partial-sum pruning (vertices have nonnegative
                               coefficients), symmetry: rows visited in an order adapted to the support; returns the
                               first (support index, assignment) found or None.  Exact when tol = 0 and inputs are
                               Fractions; with floats use tol > 0 for 'no bad tuple within margin'.
  margin_general(K, x)         min over supports/assignments of max_i (M_D(z^i) - x_i)/x_i  (float; > 0 = no tuple)
                               -- expensive; used for candidates only.
"""
import json, itertools, sys
from fractions import Fraction as Fr
import numpy as np

HERE = '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/'
sys.path.insert(0, HERE)
from tc3lib import fano_search, v_search, tau_star, LINES

_TT = None
_SUP = None


def load_tt():
    global _TT
    if _TT is None:
        d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'))
        _TT = [[(Fr(u), Fr(v)) for u, v in d[k]['record']['vertices']] for k in sorted(d, key=int)]
        assert len(_TT) == 42
    return _TT


def load_supports():
    """list of (maximal_cells, vertices as list of tuples of Fractions, float array of vertices)"""
    global _SUP
    if _SUP is None:
        d = json.load(open(HERE + 'supports715.json'))
        _SUP = []
        for q in d['orbits']:
            if q['dictator']:
                continue
            V = [tuple(Fr(s) for s in v) for v in q['vertices']]
            _SUP.append((q['maximal_cells'], V, np.array([[float(s) for s in v] for v in V])))
        assert len(_SUP) == 715
    return _SUP


def two_type_bad(K, x, tol=0):
    """returns (a_index, b_index, function_index) of the first ordered pair with a two-type bad tuple, else None.
    Convention of p644_three_part_two_type_barrier_check.py: pair (s,t) excluded by shape iff
    max over parts, vertices (u*s_i + v*t_i - x_i) > 0."""
    TT = load_tt()
    p = len(x)
    for a in range(len(K)):
        for b in range(len(K)):
            if a == b:
                continue
            for fi, shape in enumerate(TT):
                if all(u * K[a][i] + v * K[b][i] <= x[i] + tol for i in range(p) for u, v in shape):
                    return (a, b, fi)
    return None


def pair_margin(K, x):
    """min over ordered pairs and functions of max over parts/vertices of (u s + v t - x)/x  (float): > 0 = no pair tuple"""
    TT = load_tt()
    p = len(x)
    best = None
    for a in range(len(K)):
        for b in range(len(K)):
            if a == b:
                continue
            for shape in TT:
                m = max((float(u) * float(K[a][i]) + float(v) * float(K[b][i]) - float(x[i])) / float(x[i])
                        for i in range(p) for u, v in shape)
                if best is None or m < best:
                    best = m
    return best


def fano_bad(K, x, tol=0):
    return fano_search(K, x, tol)


def general_bad(K, x, tol=0, supports=None, exact=True, max_supports=None):
    """DFS over the 7 rows for every support.  K: list of type tuples (Fractions or floats), x: capacities.
    exact=True uses Fractions arithmetic on the vertex list (slow but exact); exact=False uses numpy floats + tol.
    Returns (support_index, rows) or None."""
    S = load_supports() if supports is None else supports
    p = len(x)
    n = len(K)
    for si, (cells, V, Vf) in enumerate(S):
        if max_supports is not None and si >= max_supports:
            break
        if exact:
            res = _dfs_exact(K, x, V, tol)
        else:
            res = _dfs_float(K, x, Vf, tol)
        if res is not None:
            return (si, res)
    return None


def _dfs_exact(K, x, V, tol):
    p = len(x)
    n = len(K)
    nv = len(V)
    # partial sums per part per vertex
    ps = [[Fr(0)] * nv for _ in range(p)]
    assign = [None] * 7
    # order rows by decreasing total vertex weight (prune earlier)
    weight = [sum(v[j] for v in V) for j in range(7)]
    order = sorted(range(7), key=lambda j: -weight[j])

    def rec(k):
        if k == 7:
            return True
        j = order[k]
        for idx in range(n):
            c = K[idx]
            ok = True
            for i in range(p):
                psi = ps[i]
                ci = c[i]
                xi = x[i] + tol
                for vi in range(nv):
                    if psi[vi] + V[vi][j] * ci > xi:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            for i in range(p):
                psi = ps[i]
                ci = c[i]
                for vi in range(nv):
                    psi[vi] += V[vi][j] * ci
            assign[j] = idx
            if rec(k + 1):
                return True
            for i in range(p):
                psi = ps[i]
                ci = c[i]
                for vi in range(nv):
                    psi[vi] -= V[vi][j] * ci
            assign[j] = None
        return False

    return tuple(assign) if rec(0) else None


def _dfs_float(K, x, Vf, tol):
    p = len(x)
    n = len(K)
    Kf = np.array([[float(v) for v in c] for c in K])          # n x p
    xf = np.array([float(v) for v in x]) + tol
    ps = np.zeros((p, Vf.shape[0]))
    assign = [None] * 7
    weight = Vf.sum(0)
    order = sorted(range(7), key=lambda j: -weight[j])
    col = [Vf[:, j] for j in range(7)]

    def rec(k):
        if k == 7:
            return True
        j = order[k]
        cj = col[j]
        for idx in range(n):
            add = np.outer(Kf[idx], cj)              # p x nv
            new = ps + add
            if (new.max(1) <= xf).all():
                ps[:] = new
                assign[j] = idx
                if rec(k + 1):
                    return True
                ps[:] = new - add
                assign[j] = None
        return False

    return tuple(assign) if rec(0) else None


def margin_general(K, x, supports=None, limit=None):
    """float: min over supports and assignments of max_i (M_D(z^i) - x_i)/x_i.  Full enumeration (n^7 per support)
    with branch-and-bound on the current best; use only for small n (<= 8)."""
    S = load_supports() if supports is None else supports
    p = len(x)
    n = len(K)
    Kf = np.array([[float(v) for v in c] for c in K])
    xf = np.array([float(v) for v in x])
    best = [np.inf, None]
    for si, (cells, V, Vf) in enumerate(S):
        if limit is not None and si >= limit:
            break
        nv = Vf.shape[0]
        ps = np.zeros((p, nv))
        assign = [None] * 7
        weight = Vf.sum(0)
        order = sorted(range(7), key=lambda j: -weight[j])
        col = [Vf[:, j] for j in range(7)]

        def rec(k):
            if k == 7:
                m = ((ps.max(1) - xf) / xf).max()
                if m < best[0]:
                    best[0] = m
                    best[1] = (si, tuple(assign))
                return
            j = order[k]
            cj = col[j]
            for idx in range(n):
                add = np.outer(Kf[idx], cj)
                new = ps + add
                if ((new.max(1) - xf) / xf).max() < best[0]:
                    ps[:] = new
                    assign[j] = idx
                    rec(k + 1)
                    ps[:] = new - add
                    assign[j] = None

        rec(0)
    return best


def verify_tuple(K, x, si, rows):
    """exact re-check of a found tuple against the support's vertex list (all parts)."""
    cells, V, Vf = load_supports()[si]
    p = len(x)
    for i in range(p):
        z = [K[rows[j]][i] for j in range(7)]
        M = max(sum(v[j] * z[j] for j in range(7)) for v in V)
        if M > x[i]:
            return False
    return True


def full_check(K, x, tol=0, verbose=True):
    """returns dict with tau*, two-type, Fano, general results (exact if inputs are Fractions and tol = 0)."""
    out = {}
    out['tau'] = tau_star(K, x)
    out['pair'] = two_type_bad(K, x, tol)
    out['fano'] = fano_bad(K, x, tol)
    out['general'] = general_bad(K, x, tol, exact=(tol == 0 and isinstance(x[0], Fr)))
    if verbose:
        print('tau* = %s (%.5f)  pair=%s fano=%s general=%s' % (out['tau'], float(out['tau']), out['pair'], out['fano'],
                                                                out['general']))
    return out


if __name__ == '__main__':
    # validation on known families
    d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_three_part_two_type_barrier.json'))
    K = [tuple(Fr(v, 80) for v in t) for t in d['types']]
    x = [Fr(513, 640)] * 3
    print('7.79 family (expect: no pair, Fano yes, general yes):')
    import time
    t0 = time.time()
    r = full_check(K, x)
    print('  time', round(time.time() - t0, 1), ' verify:', r['general'] and verify_tuple(K, x, *r['general']))
    # H3-cex: expect V (pair) yes, no Fano; general yes (the V support)
    x = [Fr(5, 4), Fr(5, 4), Fr(3, 200)]
    K = [(Fr(3, 20), Fr(17, 20), Fr(0)), (Fr(17, 20), Fr(3, 20), Fr(0)), (Fr(84, 100), Fr(15, 100), Fr(1, 100))]
    print('H3-cex (expect pair yes, Fano no, general yes):')
    t0 = time.time()
    r = full_check(K, x)
    print('  time', round(time.time() - t0, 1), ' verify:', r['general'] and verify_tuple(K, x, *r['general']))
    # W(5/4,3/20) two parts with the third part removed: 2-part family, expect pair yes
    x = [Fr(5, 4), Fr(5, 4)]
    K = [(Fr(3, 20), Fr(17, 20)), (Fr(17, 20), Fr(3, 20))]
    print('W(5/4,3/20) (expect pair yes, Fano no):')
    r = full_check(K, x)


def general_bad_int(K, x, supports=None, verbose=False):
    """EXACT 'no bad tuple' check with integer arithmetic: K, x rational (Fractions).  Scale the family by the lcm of
    all denominators (types and x), scale each support's Pareto-maximal vertex list by its own lcm, and run the
    pruned DFS over rows with Python ints.  Returns (support_index, rows) or None (= exact certificate of absence)."""
    import math
    from fastlib import pareto_vertices
    S = load_supports() if supports is None else supports
    p = len(x)
    n = len(K)
    L = 1
    for c in K:
        for v in c:
            L = L * Fr(v).denominator // math.gcd(L, Fr(v).denominator)
    for v in x:
        L = L * Fr(v).denominator // math.gcd(L, Fr(v).denominator)
    Ki = [[int(Fr(v) * L) for v in c] for c in K]
    xi = [int(Fr(v) * L) for v in x]
    for si, (cells, V, Vf) in enumerate(S):
        # Pareto-maximal vertices (exact, via the float array's mask)
        keep = []
        for i in range(len(V)):
            dom = any(i != j and all(V[j][k] >= V[i][k] for k in range(7)) and any(V[j][k] > V[i][k] for k in range(7)) for j in range(len(V)))
            if not dom:
                keep.append(V[i])
        LD = 1
        for v in keep:
            for q in v:
                LD = LD * q.denominator // math.gcd(LD, q.denominator)
        Vi = [[int(q * LD) for q in v] for v in keep]
        cap = [xi[i] * LD for i in range(p)]
        nv = len(Vi)
        ps = [[0] * nv for _ in range(p)]
        assign = [None] * 7
        weight = [sum(v[j] for v in Vi) for j in range(7)]
        order = sorted(range(7), key=lambda j: -weight[j])
        col = [[Vi[vi][j] for vi in range(nv)] for j in range(7)]

        def rec(k):
            if k == 7:
                return True
            j = order[k]
            cj = col[j]
            for idx in range(n):
                c = Ki[idx]
                ok = True
                for i in range(p):
                    psi = ps[i]; ci = c[i]; capi = cap[i]
                    for vi in range(nv):
                        if psi[vi] + cj[vi] * ci > capi:
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    continue
                for i in range(p):
                    psi = ps[i]; ci = c[i]
                    for vi in range(nv):
                        psi[vi] += cj[vi] * ci
                assign[j] = idx
                if rec(k + 1):
                    return True
                for i in range(p):
                    psi = ps[i]; ci = c[i]
                    for vi in range(nv):
                        psi[vi] -= cj[vi] * ci
                assign[j] = None
            return False

        if rec(0):
            return (si, tuple(assign))
        if verbose and si % 100 == 99:
            print('   support', si + 1, 'done', flush=True)
    return None
