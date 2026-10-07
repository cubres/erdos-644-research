#!/usr/bin/env python3
"""
Exact check of the SIX-PLUS-ONE Fano construction behind the central-trace lemma.

Lemma (finite form).  Parts V_1..V_r of sizes n_i.  Let s,v be integer trace vectors with
sum_i s_i = sum_i v_i = k, and for every part i
      v_i <= 2 s_i   and   3*ceil((2s_i-v_i)/4) + 4*ceil(v_i/4) <= n_i.            (*)
Then there are seven k-sets G_1..G_7 (G_1..G_6 of trace s, G_7 of trace v) with no
transversal of size <= 2.  [ (*) holds whenever 6 s_i + v_i <= 4 n_i - 21. ]
Consequently, in a type-closed family (all k-sets whose trace lies in an admissible set S)
with property (7,2): if s in S has n_i/2 <= s_i and 6 s_i <= 4 n_i - 21 for all i, then the
box u_i = 4 n_i - 6 s_i - 21 contains no admissible trace, and the complement of such a box
is a transversal:  tau <= N - sum_i u_i = 6k - 3N + 21 r.

Construction (per part i): Fano plane on points 0..6, lines L; l0 = the line of G_7.
Class V_p has ceil((2s_i-v_i)/4) points of part i if p in l0, ceil(v_i/4) if p not in l0.
G_l (l != l0) takes s_i points of part i from the four classes off l; G_7 takes v_i points
of part i from the four classes off l0.  A point of V_p lies only in edges G_l with p not
on l, so for two points in V_p, V_q the line through p,q gives an edge missing both.

This script builds the sets explicitly for many random integer instances and verifies by
BRUTE FORCE over all vertex pairs (x=y allowed) that no pair meets all seven edges, that
traces are exact, and that the classes fit into the parts.  It also checks the
continuous per-part Fano covering value Phi(s,...,s,v) = max(v,(6s+v)/4) against an
exhaustive rational search over the LP's vertices (exact Fractions).
Run: python3 -B central_trace_check.py
"""
import itertools, random
from fractions import Fraction

# Fano plane: points 0..6, lines = {i,i+1,i+3} mod 7
LINES = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]
assert all(len(a & b) == 1 for a, b in itertools.combinations(LINES, 2))

def ceil_div(a, b):
    return -((-a) // b)

def build(n, s, v):
    r = len(n)
    l0 = LINES[6]
    # class sizes per (point, part)
    csz = [[(ceil_div(2 * s[i] - v[i], 4) if p in l0 else ceil_div(v[i], 4)) for i in range(r)]
           for p in range(7)]
    for i in range(r):
        if sum(csz[p][i] for p in range(7)) > n[i]:
            return None
    # vertices: (part, index); assign classes consecutively inside each part
    cls = {}   # vertex -> point p
    members = {(p, i): [] for p in range(7) for i in range(r)}
    for i in range(r):
        idx = 0
        for p in range(7):
            for _ in range(csz[p][i]):
                cls[(i, idx)] = p
                members[(p, i)].append((i, idx))
                idx += 1
    edges = []
    for li, l in enumerate(LINES):
        trace = v if li == 6 else s
        E = set()
        for i in range(r):
            pool = [x for p in range(7) if p not in l for x in members[(p, i)]]
            if len(pool) < trace[i]:
                return "SHORT"
            E |= set(pool[:trace[i]])
        edges.append(frozenset(E))
    return cls, edges

def verify(n, s, v):
    res = build(n, s, v)
    if res is None:
        return "nofit"
    if res == "SHORT":
        raise AssertionError("class union too small: construction error")
    cls, edges = res
    r = len(n)
    # exact traces
    for li, E in enumerate(edges):
        tr = [sum(1 for (i, _) in E if i == j) for j in range(r)]
        want = list(v if li == 6 else s)
        assert tr == want, (tr, want)
        assert len(E) == sum(want)
    union = sorted(set().union(*edges))
    # brute force: no pair (x=y allowed) meets all seven edges
    for a in range(len(union)):
        for b in range(a, len(union)):
            x, y = union[a], union[b]
            if all((x in E) or (y in E) for E in edges):
                raise AssertionError("found a 2-transversal: construction is not bad")
    # every vertex outside the union is in no edge, so it cannot help either
    return "bad"

def phi_exact(dem):
    """min sum_p w_p s.t. sum_{p not in l} w_p >= dem_l, w>=0 : exhaustive over basic solutions
    (7 variables, 7 covering constraints + 7 nonnegativity); exact rationals."""
    best = None
    rows = []
    for l in LINES:
        rows.append(([0 if p in l else 1 for p in range(7)], dem[LINES.index(l)]))
    # candidate vertices: choose 7 tight constraints among 14 (7 covering + 7 w_p=0)
    cons = [(r, b) for r, b in rows] + [([1 if q == p else 0 for q in range(7)], 0) for p in range(7)]
    for T in itertools.combinations(range(14), 7):
        M = [list(map(Fraction, cons[t][0])) for t in T]
        rhs = [Fraction(cons[t][1]) for t in T]
        # Gaussian elimination
        A = [M[i] + [rhs[i]] for i in range(7)]
        ok = True
        for c in range(7):
            piv = next((i for i in range(c, 7) if A[i][c] != 0), None)
            if piv is None:
                ok = False; break
            A[c], A[piv] = A[piv], A[c]
            for i in range(7):
                if i != c and A[i][c] != 0:
                    f = A[i][c] / A[c][c]
                    A[i] = [A[i][j] - f * A[c][j] for j in range(8)]
        if not ok:
            continue
        w = [A[i][7] / A[i][i] for i in range(7)]
        if any(x < 0 for x in w):
            continue
        if all(sum(w[p] for p in range(7) if p not in l) >= dem[li] for li, l in enumerate(LINES)):
            val = sum(w)
            if best is None or val < best:
                best = val
    return best

if __name__ == "__main__":
    random.seed(20260923)
    counts = {"bad": 0, "nofit": 0}
    for trial in range(400):
        r = random.randint(1, 4)
        k = random.randint(8, 40)
        # random central-ish trace s and part sizes n with n_i/2 <= s_i <= 2n_i/3 roughly
        cuts = sorted(random.sample(range(1, k), r - 1)) if r > 1 else []
        s = [b - a for a, b in zip([0] + cuts, cuts + [k])]
        if min(s) == 0:
            continue
        n = [random.randint(max(1, (3 * si + 1) // 2), 2 * si) for si in s]   # s_i in [n_i/2, 2n_i/3]
        # v: any trace with v_i <= min(2 s_i, 4 n_i - 6 s_i)
        cap = [max(0, min(2 * s[i], 4 * n[i] - 6 * s[i])) for i in range(r)]
        if sum(cap) < k:
            continue
        v = [0] * r
        rem = k
        order = list(range(r)); random.shuffle(order)
        for i in order:
            take = min(cap[i], rem)
            if i != order[-1]:
                take = random.randint(max(0, rem - sum(cap[j] for j in order[order.index(i) + 1:])), take)
            v[i] = take; rem -= take
        if rem != 0:
            continue
        counts[verify(n, s, v)] += 1
    print("six-plus-one integer constructions verified bad by brute force:", counts["bad"],
          "| instances where rounding did not fit (no claim):", counts["nofit"])
    # continuous per-part formula Phi(s,..,s,v) = max(v,(6s+v)/4), exact rationals
    nchk = 0
    for s0 in range(1, 9):
        for v0 in range(0, 25):
            for pos in range(7):
                dem = [Fraction(s0)] * 7
                dem[pos] = Fraction(v0)
                val = phi_exact(dem)
                assert val == max(Fraction(v0), Fraction(6 * s0 + v0, 4)), (s0, v0, pos, val)
                nchk += 1
    print("Phi(s x6, v) = max(v,(6s+v)/4) verified exactly on", nchk, "demand vectors")
    # the balanced formula Phi = sum/4 when every point p has sum_{l ni p} s_l <= sum/2
    nb = 0
    random.seed(7)
    for _ in range(300):
        dem = [Fraction(random.randint(3, 9)) for _ in range(7)]
        tot = sum(dem)
        balanced = all(sum(dem[li] for li, l in enumerate(LINES) if p in l) <= tot / 2 for p in range(7))
        val = phi_exact(dem)
        if balanced:
            assert val == tot / 4, (dem, val)
            nb += 1
        else:
            assert val > tot / 4
    print("balanced Phi = (sum)/4 verified exactly on", nb, "random balanced demand vectors")
    print("ALL PASS")
