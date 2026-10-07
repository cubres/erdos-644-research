"""Erdős #644, budget analysis of the FKW 1999 upper-bound scheme.

Normalise by r (so k = r/8 when s = 0).  FKW build 7 edges from a good triple (A1,A2,A3) with
pairwise intersections a12 >= a13 >= a23 by repeatedly taking an edge that avoids a prescribed set
of size <= T := beta*r  (they use beta = 7/8).  This script recomputes every prescribed-set size as a
function of (a12, a13, a23, beta) and reports, for a given beta, which (a12,a13,a23) the scheme covers.

Lemma 1, Case 1 (a13 <= (k + a12)/2):   |A12∪B0| = T, |A12∪B1∪B2'| = T, |A12∪B2∪B1'| = T,
                                         |B4| = 3r - 3T + a12          (needs a12 <= 4T - 3r)
                                         feasibility: |A3-A1-A2| = r - a13 - a23 >= T - a12,
                                                      b_i = T - a12 - |B_{3-i}| >= 0 and <= r - a_i3 - a12
Lemma 1, Case 2 (a13 >  (k + a12)/2):   |B5| = 2k + a13 + max(|B3|, a13 - k) with
                                         |B3| = max(a12 - a13 + k, a23); needs |B5| <= T.
Theorem cases choose the good triple so that Lemma 1's hypotheses (2)-(4) hold; their own avoided
sets have size exactly T by construction (Cases 1,4) or <= T (Cases 2,3).
"""
import itertools, sys
from fractions import Fraction as Fr

def lemma1_ok(a12, a13, a23, beta, r=Fr(1)):
    """Return (case, ok, worst_avoided_set/r) for the FKW Lemma 1 scheme with budget T = beta*r."""
    k = r / 8; T = beta * r
    a12, a13, a23 = sorted([a12, a13, a23], reverse=True)
    if a13 <= (k + a12) / 2:
        B0 = T - a12
        if r - a13 - a23 < B0: return ('1', False, None)   # cannot place B0 inside A3 - A1 - A2
        B1 = (k + a12) / 2; B2 = (k + a12) / 2          # A3 - B0 split (sizes floor/ceil; use halves)
        if B1 + B2 != r - B0: B1 = B2 = (r - B0) / 2
        b1 = T - a12 - B2; b2 = T - a12 - B1
        if b1 < 0 or b2 < 0: return ('1', False, None)
        if b1 > r - a13 - a12 or b2 > r - a23 - a12: return ('1', False, None)
        B4 = 2 * r - 2 * a12 - b1 - b2
        return ('1', B4 <= T, B4 / r)
    else:
        B3 = max(a12 - a13 + k, a23)
        B5 = 2 * k + a13 + max(B3, a13 - k)
        return ('2', B5 <= T, B5 / r)

def scan(beta, D=16):
    grid = [Fr(i, D) for i in range(0, D // 2 + 1)]   # intersections up to r/2
    covered, total, worst = 0, 0, []
    for a12 in grid:
        for a13 in grid:
            for a23 in grid:
                if not (a12 >= a13 >= a23): continue
                # FKW hypotheses (2)-(4) at s=0:  a12 <= r/2, a13 <= 3r/8, a13 + a23 <= 5r/8
                if a12 > Fr(1, 2) or a13 > Fr(3, 8) or a13 + a23 > Fr(5, 8): continue
                total += 1
                case, ok, size = lemma1_ok(a12, a13, a23, beta)
                if ok: covered += 1
                else: worst.append((float(a12), float(a13), float(a23), case, None if size is None else float(size)))
    return covered, total, worst

if __name__ == '__main__':
    for beta in [Fr(7, 8), Fr(13, 16), Fr(25, 32), Fr(3, 4)]:
        covered, total, worst = scan(beta)
        print(f"beta={float(beta):.4f}: Lemma 1 scheme covers {covered}/{total} grid triples (a12>=a13>=a23 in FKW's region)")
        if worst:
            amax = max(w[0] for w in worst if w[3] == '1' and w[4] is not None) if any(w[3]=='1' and w[4] is not None for w in worst) else None
            print(f"   uncovered examples: {worst[:4]}")
            print(f"   Case-1 bound a12 <= 4*beta-3 = {float(4*beta-3):.4f}")
    print()
    print("Closed form (Lemma 1, Case 1): |B4|/r = 3 - 3*beta + a12/r, so the scheme needs a12/r <= 4*beta - 3.")
    print("At the Fano value a12 = r/2 this forces beta >= 7/8; at beta = 3/4 the scheme tolerates only a12 = 0.")
