#!/usr/bin/env python3
"""
Exact check of the capture trade-off for "thinned two-part + two anchors" families
(the shape of note 7.101 and 7.104).  Pure integer arithmetic, standard library only.

Family G(k,Q,S,D):
  disjoint A,B with |A|=|B|=Q, disjoint D1,D2 with |Di|=D=k-Q (anchor padding);
  core  = { E subset A u B : |E|=k, |E cap A| in S }  (S subset [k-Q, Q]);
  anchors A u D1, B u D2.
  For U subset V and m>=0:  H^(m)_U = { G : |G \ U| <= m }.

Claims checked (all U up to symmetry, all m in range):
 (A1) upper bound, for every U and 0<=m<=min(c-1,k-d-1), (d,c) any gap of S:
        tau(H^(m)_U) <= (|U cap A|-(c-1-m))^+ + (|U cap B|-(k-d-1-m))^+ + 2
 (A2) lower bound, U_j=(A minus j pts) u (B minus j pts), 0<=m<=j:
        tau(H^(m)_{U_j}) >= min(t-2(j-m), t+g-1-2j+m),  g = largest gap, t = tau(H)
 (A3) the resulting deficit profile
        Def(delta,m) = t - max{ tau(H^(m)_U) : |U| <= k+t+delta }
      satisfies (g-4-delta-2m)^+ - slack <= Def <= (g-2-delta-2m)^+ where slack accounts
      for the branches of (A1) in which one positive part vanishes (reported, not assumed).

Exactness of the symmetry reduction: H^(m)_U is invariant under all permutations of each
cell A cap U, A \ U, B cap U, B \ U, D1 cap U, D1 \ U, D2 cap U, D2 \ U.  Hence whether a
set T is a transversal depends only on its cell counts, and a core edge avoiding T with at
most m points outside U exists iff suitable cell counts exist.  Part (B) validates this
reduction against a literal brute force over all subsets T on a tiny instance.

Run:  python3 -B gap_capture_check.py
"""
import itertools, sys

def edge_exists(S, k, x, x2, y, y2, m):
    """Is there a core edge with |E cap A| in S using at most x free A-inside points,
    x2 free A-outside points, y free B-inside, y2 free B-outside, and <= m outside points?"""
    for a in S:
        b = k - a
        e2 = a - x if a > x else 0
        e4 = b - y if b > y else 0
        if e2 <= x2 and e2 <= a and e4 <= y2 and e4 <= b and e2 + e4 <= m:
            return True
    return False

def tau_reduced(k, Q, S, D, jA, jB, u1, u2, m):
    """Exact tau(H^(m)_U) for U with |U cap A|=Q-jA, |U cap B|=Q-jB, |U cap Di|=ui."""
    al, be = Q - jA, Q - jB
    anc1 = (jA + (D - u1)) <= m      # anchor A u D1 protrudes jA + |D1 \ U|
    anc2 = (jB + (D - u2)) <= m
    best = None
    for x2 in range(jA + 1):
        for y2 in range(jB + 1):
            # for each x, largest y with no avoiding edge (monotone decreasing in x)
            y = be
            for x in range(al + 1):
                while y >= 0 and edge_exists(S, k, x, x2, y, y2, m):
                    y -= 1
                if y < 0:
                    break
                tA = (al - x) + (jA - x2)
                tB = (be - y) + (jB - y2)
                cost = tA + tB
                if anc1 and tA == 0:
                    cost += 1
                if anc2 and tB == 0:
                    cost += 1
                if best is None or cost < best:
                    best = cost
    return best

def gaps(S):
    Ss = sorted(S)
    return [(Ss[i], Ss[i + 1]) for i in range(len(Ss) - 1) if Ss[i + 1] - Ss[i] >= 2]

def check_family(name, k, Q, S, jmax, mmax, deltas):
    D = k - Q
    S = sorted(set(S))
    assert min(S) >= k - Q and max(S) <= Q
    t = tau_reduced(k, Q, S, D, 0, 0, D, D, 0)
    G = gaps(S)
    g = max(c - d for d, c in G)
    print(f"== {name}: k={k} Q={Q} |V|={2*Q+2*D} S={S}")
    print(f"   tau(H)={t}, largest gap g={g}, formula 2Q-k-g+2={2*Q-k-g+2}, "
          f"k+t={k+t}, |A u B|={2*Q}, 3k/4={3*k/4}")
    ok = True
    # (A1) upper bound for every U-type and every gap
    cnt = 0
    for jA in range(jmax + 1):
        for jB in range(jmax + 1):
            for u1 in (0, D):
                for u2 in (0, D):
                    for m in range(mmax + 1):
                        tv = tau_reduced(k, Q, S, D, jA, jB, u1, u2, m)
                        al, be = Q - jA, Q - jB
                        for (d, c) in G:
                            if m <= min(c - 1, k - d - 1):
                                ub = max(0, al - (c - 1 - m)) + max(0, be - (k - d - 1 - m)) + 2
                                cnt += 1
                                if tv > ub:
                                    ok = False
                                    print("   (A1) FAIL", jA, jB, u1, u2, m, (d, c), tv, ub)
    print(f"   (A1) upper bound checked on {cnt} (U-type, m, gap) triples: {'PASS' if ok else 'FAIL'}")
    # (A2) lower bound for symmetric U_j
    ok2 = True
    for j in range(jmax + 1):
        for m in range(j + 1):
            tv = tau_reduced(k, Q, S, D, j, j, 0, 0, m)
            lb = min(t - 2 * (j - m), t + g - 1 - 2 * j + m)
            if tv < lb:
                ok2 = False
                print("   (A2) FAIL", j, m, tv, lb)
    print(f"   (A2) lower bound for U_j (0<=m<=j<={jmax}): {'PASS' if ok2 else 'FAIL'}")
    # (A3) deficit profile
    table = {}
    for jA in range(jmax + 1):
        for jB in range(jmax + 1):
            for u1 in (0, D):
                for u2 in (0, D):
                    size = 2 * Q - jA - jB + u1 + u2
                    for m in range(mmax + 1):
                        tv = tau_reduced(k, Q, S, D, jA, jB, u1, u2, m)
                        table[(size, m)] = max(table.get((size, m), -1), tv)
    print("   deficit profile Def(delta,m) [exact over U-types with jA,jB<=%d] vs (g-2-delta-2m)^+:" % jmax)
    ok3 = True
    for delta in deltas:
        row = []
        for m in range(mmax + 1):
            best = max([v for (sz, mm), v in table.items() if mm == m and sz <= k + t + delta] + [0])
            dfc = t - best
            pred_hi = max(0, g - 2 - delta - 2 * m)
            pred_lo = max(0, g - 4 - delta - 2 * m)
            row.append(f"{dfc}[{pred_lo},{pred_hi}]")
            if dfc > pred_hi:
                ok3 = False
        print(f"   delta={delta:>3}: " + "  ".join(row))
    print(f"   (A3) upper estimate Def <= (g-2-delta-2m)^+ : {'PASS' if ok3 else 'FAIL'}")
    return ok and ok2 and ok3

def brute_tau(edges, nverts, maxsize):
    """literal minimum transversal by increasing size (edges as bitmasks)."""
    if not edges:
        return 0
    for s in range(maxsize + 1):
        for T in itertools.combinations(range(nverts), s):
            mask = 0
            for v in T:
                mask |= 1 << v
            if all(e & mask for e in edges):
                return s
    return None

def validate_reduction_tiny():
    """Compare tau_reduced with a literal brute force on a tiny instance (all U-types)."""
    k, Q = 5, 4
    S = [1, 4]
    D = k - Q
    A = list(range(0, Q)); B = list(range(Q, 2 * Q))
    D1 = list(range(2 * Q, 2 * Q + D)); D2 = list(range(2 * Q + D, 2 * Q + 2 * D))
    n = 2 * Q + 2 * D
    core = []
    for E in itertools.combinations(A + B, k):
        if len(set(E) & set(A)) in S:
            core.append(frozenset(E))
    anchors = [frozenset(A + D1), frozenset(B + D2)]
    allE = core + anchors
    bad = 0; tested = 0
    for jA in range(Q + 1):
        for jB in range(Q + 1):
            for u1 in range(D + 1):
                for u2 in range(D + 1):
                    U = set(A[jA:]) | set(B[jB:]) | set(D1[:u1]) | set(D2[:u2])
                    for m in range(0, 4):
                        fam = [E for E in allE if len(E - U) <= m]
                        masks = [sum(1 << v for v in E) for E in fam]
                        tb = brute_tau(masks, n, n)
                        tr = tau_reduced(k, Q, S, D, jA, jB, u1, u2, m)
                        tested += 1
                        if tb != tr:
                            bad += 1
                            print("   reduction mismatch", jA, jB, u1, u2, m, tb, tr)
    print(f"== (B) symmetry reduction vs literal brute force, k={k},Q={Q},S={S}: "
          f"{tested} (U,m) cases, mismatches={bad}: {'PASS' if bad == 0 else 'FAIL'}")
    return bad == 0

if __name__ == "__main__":
    allok = validate_reduction_tiny()
    # a scaled-down 7.104-like shape: symmetric S, two largest gaps in the middle, N=2Q<7k/4
    allok &= check_family("F1", k=24, Q=20, S=list(range(4, 7)) + [12] + list(range(18, 21)),
                          jmax=6, mmax=5, deltas=[-2, 0, 2, 4])
    allok &= check_family("F2", k=32, Q=27, S=list(range(5, 11)) + [16] + [22] + list(range(22, 28)),
                          jmax=7, mmax=5, deltas=[-2, 0, 2, 4, 6])
    allok &= check_family("F3", k=40, Q=34, S=list(range(6, 13)) + [20] + list(range(28, 35)),
                          jmax=8, mmax=6, deltas=[-2, 0, 2, 4, 6])
    print("ALL PASS" if allok else "SOME CHECK FAILED")
    sys.exit(0 if allok else 1)
