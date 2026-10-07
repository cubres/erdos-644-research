#!/usr/bin/env python3
"""
Exact check for the SINGLE-GAP family SG(j,g) (no anchors):
  k = 8j, A,B disjoint, |A|=|B|=Q=7j-1 (so |A u B| = 7k/4-2 < 7k/4: (7,2) automatic),
  gap (d,c) with d = 4j - ceil(g/2), c = d+g, S = [k-Q, d] u [c, Q],
  H = { E subset A u B : |E|=k, |E cap A| in S }.
Checks (exact integer arithmetic, symmetry-reduced over the cells A cap U, A \ U, B cap U, B \ U;
the reduction itself is validated against literal brute force in gap_capture_check.py):
  (1) tau(H) = 3k/4 - g;
  (2) every minimum transversal has |T cap A| = Q-c+1 and |T cap B| = Q-k+d+1 (both >= 2),
      hence every pair of vertices lies in a minimum transversal (pair extension);
  (3) the exact deficit profile Def(delta,m) = t - max{tau(H^(m)_U): |U| <= k+t+delta}
      equals (g-2-delta-2m)^+ on the tested range (all U-types with at most jmax points
      removed from each part; smaller U are dominated by monotonicity of H^(m)_U in U).
Run: python3 -B sg_capture_check.py
"""
import math, sys
sys.setrecursionlimit(10000)
from gap_capture_check import edge_exists

def tau_core(k, S, al, jA, be, jB, m, want_argmins=False):
    best = None; arg = set()
    for x2 in range(jA + 1):
        for y2 in range(jB + 1):
            y = be
            for x in range(al + 1):
                while y >= 0 and edge_exists(S, k, x, x2, y, y2, m):
                    y -= 1
                if y < 0:
                    break
                cost = (al - x) + (jA - x2) + (be - y) + (jB - y2)
                if best is None or cost < best:
                    best = cost; arg = set()
                if want_argmins and cost == best:
                    arg.add(((al - x) + (jA - x2), (be - y) + (jB - y2)))
    return best, arg

def all_min_splits(k, S, Q):
    """all (|T cap A|, |T cap B|) of minimum transversals of H (U=V, m=0): exhaustive over counts"""
    best = None; splits = set()
    for tA in range(Q + 1):
        for tB in range(Q + 1):
            if not edge_exists(S, k, Q - tA, 0, Q - tB, 0, 0):
                c = tA + tB
                if best is None or c < best:
                    best = c; splits = {(tA, tB)}
                elif c == best:
                    splits.add((tA, tB))
    return best, splits

def check(j, g, jmax, mmax, deltas):
    k = 8 * j; Q = 7 * j - 1
    d = 4 * j - math.ceil(g / 2); c = d + g
    assert k - Q <= d and c <= Q
    S = list(range(k - Q, d + 1)) + list(range(c, Q + 1))
    t, splits = all_min_splits(k, S, Q)
    ok = (t == 3 * k // 4 - g) and splits == {(Q - c + 1, Q - k + d + 1)} and min(Q - c + 1, Q - k + d + 1) >= 2
    print(f"SG(j={j},g={g}): k={k} Q={Q} |V|={2*Q} (7k/4={7*k/4}) gap=({d},{c}) tau={t} (3k/4-g={3*k//4-g}) "
          f"min-cover splits={sorted(splits)}  {'OK' if ok else 'FAIL'}")
    table = {}
    for jA in range(jmax + 1):
        for jB in range(jmax + 1):
            for m in range(mmax + 1):
                tv, _ = tau_core(k, S, Q - jA, jA, Q - jB, jB, m)
                size = 2 * Q - jA - jB
                table[(size, m)] = max(table.get((size, m), -1), tv)
    ok3 = True
    for delta in deltas:
        row = []
        for m in range(mmax + 1):
            best = max([v for (sz, mm), v in table.items() if mm == m and sz <= k + t + delta] + [0])
            dfc = t - best
            pred = max(0, g - 2 - delta - 2 * m)
            row.append(f"{dfc}({pred})")
            if dfc != pred:
                ok3 = False
        print(f"   delta={delta:>3}: " + "  ".join(row))
    print(f"   Def(delta,m) == (g-2-delta-2m)^+ on the table: {'PASS' if ok3 else 'FAIL'}")
    return ok and ok3

if __name__ == "__main__":
    allok = True
    allok &= check(3, 4, jmax=5, mmax=4, deltas=[-2, 0, 1, 2])
    allok &= check(4, 6, jmax=6, mmax=4, deltas=[-2, 0, 1, 2, 4])
    allok &= check(5, 8, jmax=8, mmax=5, deltas=[-2, 0, 1, 2, 4, 6])
    allok &= check(6, 10, jmax=9, mmax=6, deltas=[-2, 0, 2, 4, 6, 8])
    print("ALL PASS" if allok else "SOME CHECK FAILED")
    sys.exit(0 if allok else 1)
