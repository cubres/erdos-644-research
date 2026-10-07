"""Toolkit for the continuous type-closed model over p parts (discovery; exact where noted).

Model: capacities x (p parts), types c with 0 <= c <= x, |c| = 1.  A box w (0<=w<=x) is free for K
if no c in K has c <= w.  tau*(K) = N - sup{|w| : w free}.  Sup semantics: blocking thresholds.
A threshold vector t (t_i in (0, x_i] or INF) blocks c iff c_i >= t_i for some i with t_i finite.
cost(t) = sum over finite t_i of (x_i - t_i).  tau*(K) = min cost over blocking t (exact, Fractions ok).

Bad tuples: Fano (Lemma 7.63: rows on points, per part: row <= x, line sums <= 2x, total <= 4x) with
an arbitrary assignment of types to the 7 points; V(a,b) (5 rows a, 2 rows b): max(a+b, 5a/4+b/2) <= x.
"""
import itertools
from fractions import Fraction as Fr

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
INF = None


def tau_star(K, x, want=False):
    p = len(x)
    cands = [sorted(set([c[i] for c in K if c[i] > 0])) + [INF] for i in range(p)]
    best = None
    bestt = None
    # enumerate thresholds for parts 0..p-2, compute the last one
    for tt in itertools.product(*cands[:-1]):
        unb = [c for c in K if not any(tt[i] is not INF and c[i] >= tt[i] for i in range(p - 1))]
        if not unb:
            tl = INF
        else:
            if any(c[-1] <= 0 for c in unb):
                continue
            tl = min(c[-1] for c in unb)
        t = list(tt) + [tl]
        cost = sum(x[i] - t[i] for i in range(p) if t[i] is not INF)
        if best is None or cost < best:
            best, bestt = cost, t
    return (best, bestt) if want else best


def fano_part_ok(z, xi, tol=0):
    if max(z) > xi + tol:
        return False
    if sum(z) > 4 * xi + tol:
        return False
    for l in LINES:
        if z[l[0]] + z[l[1]] + z[l[2]] > 2 * xi + tol:
            return False
    return True


def fano_ok(rows, x, tol=0):
    """rows: list of 7 types (assigned to points 0..6)"""
    return all(fano_part_ok([r[i] for r in rows], x[i], tol) for i in range(len(x)))


def v_ok(a, b, x, tol=0):
    return all(max(a[i] + b[i], Fr(5, 4) * a[i] + b[i] / 2 if isinstance(a[i], Fr) else 1.25 * a[i] + 0.5 * b[i])
               <= x[i] + tol for i in range(len(x)))


def fano_search(K, x, tol=0, limit=None):
    """search assignments of types (indices) to the 7 Fano points; symmetry-reduced by requiring
    the multiset pattern to be tried in a canonical order is skipped: brute force with pruning.
    Returns first feasible assignment (tuple of indices) or None."""
    n = len(K)
    p = len(x)
    # prune: per-part row bounds always hold (types <= x). Use DFS over points 0..6 with partial
    # line-sum and total checks.
    order = [0, 1, 2, 3, 4, 5, 6]
    lines_by_last = {}
    for l in LINES:
        lines_by_last.setdefault(max(l), []).append(l)
    assign = [None] * 7
    tot = [0] * p
    count = [0]

    def rec(k):
        if k == 7:
            return True
        for idx in range(n):
            c = K[idx]
            ok = True
            for i in range(p):
                if tot[i] + c[i] > 4 * x[i] + tol:
                    ok = False
                    break
            if not ok:
                continue
            assign[k] = idx
            for l in lines_by_last.get(k, []):
                for i in range(p):
                    if K[assign[l[0]]][i] + K[assign[l[1]]][i] + K[assign[l[2]]][i] > 2 * x[i] + tol:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                for i in range(p):
                    tot[i] += c[i]
                if rec(k + 1):
                    return True
                for i in range(p):
                    tot[i] -= c[i]
            assign[k] = None
        return False

    return tuple(assign) if rec(0) else None


def v_search(K, x, tol=0):
    for i, a in enumerate(K):
        for j, b in enumerate(K):
            if i != j and v_ok(a, b, x, tol):
                return (i, j)
    return None


def maximal_free_boxes_containing(K, x, lower):
    """threshold vectors t blocking all of K with t_i > lower_i (so w = t - eps >= lower),
    minimal cost first. Returns list of (cost, t, blockers) where blockers[i] = types touching facet i."""
    p = len(x)
    cands = [sorted(set([c[i] for c in K if c[i] > lower[i]])) + [INF] for i in range(p)]
    out = []
    for t in itertools.product(*cands):
        if all(any(t[i] is not INF and c[i] >= t[i] for i in range(p)) for c in K):
            cost = sum(x[i] - t[i] for i in range(p) if t[i] is not INF)
            out.append((cost, t))
    # keep only minimal (maximal boxes): no other t' componentwise >= t (as box) blocking all
    out.sort(key=lambda r: r[0])
    res = []
    for cost, t in out:
        blockers = []
        for i in range(p):
            if t[i] is INF:
                blockers.append([])
            else:
                blockers.append([k for k, c in enumerate(K) if c[i] >= t[i] and
                                 all(t[j] is INF or c[j] < t[j] for j in range(p) if j != i)])
        res.append((cost, t, blockers))
    return res
