"""8-edge variant at budget T=13 (r=16): FKW Lemma-1 steps for A4..A6, then TWO final edges A7, A8 that
split the over-budget set B4 = (A1∪A2) − A12 − B1' − B2' into pieces each within budget.
Prover wins iff no 8-edge configuration has ALL <=7-subfamilies 2-pierceable."""
import sys, time, itertools
from p644_strategy import *
k, r, T = 2, 16, 13
def script8(a12, a13, a23, beta0, beta1, split):
    Tt = (1, 2, 3); beta2 = r - beta0 - beta1
    if beta1 < a13 or beta2 < a23 or beta0 < 0 or a12 + beta0 > T: return None
    b2 = T - a12 - beta1; b1 = T - a12 - beta2
    if b1 < 0 or b2 < 0 or b1 > r - a13 - a12 or b2 > r - a23 - a12: return None
    c1 = r - a13 - a12 - b1      # |cell1 \ B1'|  (cell1 = A1 − A13 − A12)
    c3 = r - a23 - a12 - b2      # |cell3 \ B2'|
    B4 = a13 + a23 + c1 + c3
    if B4 <= T: return None      # then the 7-edge script already works
    # split: A7 avoids A13 ∪ A23 ∪ (cell1\B1') ∪ (q3 units of cell3\B2') ; A8 avoids A13 ∪ A23 ∪ (cell3\B2') ∪ (q1 units of cell1\B1')
    q3 = T - a13 - a23 - c1; q1 = T - a13 - a23 - c3
    if q3 < 0 or q1 < 0: return None
    steps = {}
    steps[3] = {'avoid': [cellin((1, 2), 1, 2)]}
    steps[4] = {'picks': [('B0', cellin(Tt, 2), beta0)], 'avoid': [contains(1, 3), 'B0']}
    steps[5] = {'picks': [('B1r', both(cellin(Tt, 2), notin('B0')), beta1 - a13), ('B2p', cellin(Tt, 3), b2)],
                'avoid': [contains(1, 3), cellin(Tt, 1, 2), 'B1r', 'B2p']}
    steps[6] = {'picks': [('B1p', cellin(Tt, 1), b1)],
                'avoid': [contains(1, 3), cellin(Tt, 2, 3), both(both(cellin(Tt, 2), notin('B0')), notin('B1r')), 'B1p']}
    rest1 = both(cellin(Tt, 1), notin('B1p')); rest3 = both(cellin(Tt, 3), notin('B2p'))
    if split == 'A':
        steps[7] = {'picks': [('Q3', rest3, q3)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest1, 'Q3']}
        steps[8] = {'picks': [('Q1', rest1, q1)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest3, 'Q1']}
    else:   # split 'B': A7 avoids A13 ∪ rest1 ∪ rest3 (drop A23), A8 avoids A23 ∪ rest1 ∪ rest3 (drop A13)
        if a13 + c1 + c3 > T or a23 + c1 + c3 > T: return None
        steps[7] = {'avoid': [cellin(Tt, 1, 2), rest1, rest3]}
        steps[8] = {'avoid': [cellin(Tt, 2, 3), rest1, rest3]}
    hyps = [(mass(contains(1, 2)), a13, a13, (1, 2)), (mass(contains(1, 3)), a12, a12, (1, 3)), (mass(contains(2, 3)), a23, a23, (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(8, r, T, steps, intersecting=True, hyps=hyps)

if __name__ == '__main__':
    t0 = time.time()
    for a12 in (5, 6, 7, 8):
        for a13 in (2, 3, 4):
            for a23 in (0, 2, a13):
                if a23 > a13: continue
                won = None; tried = 0
                for split in ('A', 'B'):
                    for beta0 in range(0, T - a12 + 1):
                        for beta1 in range(a13, r - beta0 + 1):
                            sc = script8(a12, a13, a23, beta0, beta1, split)
                            if sc is None: continue
                            tried += 1
                            out = solve(sc, time_limit=180)
                            if out['status'].startswith('PROVER'): won = (split, beta0, beta1); break
                            if out['status'].startswith('UNKNOWN'): print("   unknown", (a12,a13,a23), split, beta0, beta1, flush=True)
                        if won: break
                    if won: break
                print(f"triple {(a12,a13,a23)}: {'WIN '+str(won) if won else 'no win'} (tried {tried}) [{time.time()-t0:.0f}s]", flush=True)
