"""Coverage engine for a computer-assisted upper bound at budget T (units of r/16, r = 16).
For each interval cell C = [a12 in I1] x [a13 in I2] x [a23 in I3] of the good-triple space
(sorted region a12 >= a13 >= a23 >= 1), try script families whose pick sizes are AFFINE in
(a12, a13, a23) so that every move costs exactly <= T on the whole cell (checked arithmetically at
cell corners), and decide by the CONTINUOUS MILP whether the prover wins on the whole cell.
Script families:  L1 = 1999 Lemma-1 (7 edges);  S8 = 8-edge split of the last avoidance.
"""
import sys, time, itertools, json
from multiprocessing import Pool
from p644_strategy import *

R, T = 16, 13
A12 = mass(contains(1, 3)); A13 = mass(contains(1, 2)); A23 = mass(contains(2, 3))
Tt = (1, 2, 3)

def corners(I1, I2, I3):
    return [(a, b, c) for a in I1 for b in I2 for c in I3]

def script_L1(I1, I2, I3, beta1c):
    """beta0 = T - a12 (affine), |B1| = beta1c (const >= a13), |B2| = 16 - beta0 - beta1c = 3 + a12 - beta1c (affine),
    b2 = T - a12 - beta1c, b1 = T - a12 - |B2| = 10 - 2 a12 + beta1c, |B4| = 3R - 3T + a12 = 9 + a12 <= T  <=> a12 <= 4."""
    ok = True
    for (a12, a13, a23) in corners(I1, I2, I3):
        beta0 = T - a12; beta2 = R - beta0 - beta1c; b2 = T - a12 - beta1c; b1 = T - a12 - beta2
        if beta0 < 0 or beta1c < a13 or beta2 < a23 or b1 < 0 or b2 < 0: ok = False
        if b1 > R - a13 - a12 or b2 > R - a23 - a12: ok = False
        if 9 + a12 > T: ok = False
        if beta0 > R - a13 - a23: ok = False       # B0 must fit in A3 - A1 - A2
    if not ok: return None
    steps = {3: {'avoid': [cellin((1, 2), 1, 2)]},
             4: {'picks': [('B0', cellin(Tt, 2), Aff(T) - A12)], 'avoid': [contains(1, 3), 'B0']},
             5: {'picks': [('B1r', both(cellin(Tt, 2), notin('B0')), Aff(beta1c) - A13), ('B2p', cellin(Tt, 3), Aff(T - beta1c) - A12)],
                 'avoid': [contains(1, 3), cellin(Tt, 1, 2), 'B1r', 'B2p']},
             6: {'picks': [('B1p', cellin(Tt, 1), Aff(10 + beta1c) - A12 * 2)],
                 'avoid': [contains(1, 3), cellin(Tt, 2, 3), both(both(cellin(Tt, 2), notin('B0')), notin('B1r')), 'B1p']},
             7: {'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), both(cellin(Tt, 1), notin('B1p')), both(cellin(Tt, 3), notin('B2p'))]}}
    return steps, 7

def script_S8(I1, I2, I3, beta0c, beta1c):
    """8-edge: beta0, beta1 constants; b2 = T - a12 - beta1c, b1 = T - a12 - beta2 (beta2 = 16 - beta0c - beta1c);
    rest1 = cell1 \\ B1' has size 16 - a13 - a12 - b1 ; rest3 = 16 - a23 - a12 - b2.
    A7 avoids A13 ∪ A23 ∪ rest1 ∪ Q3 (|Q3| = T - a13 - a23 - |rest1|), A8 avoids A13 ∪ A23 ∪ rest3 ∪ Q1."""
    beta2 = R - beta0c - beta1c; ok = True
    for (a12, a13, a23) in corners(I1, I2, I3):
        b2 = T - a12 - beta1c; b1 = T - a12 - beta2
        if beta0c < 0 or beta1c < a13 or beta2 < a23 or b1 < 0 or b2 < 0: ok = False
        if b1 > R - a13 - a12 or b2 > R - a23 - a12: ok = False
        if a12 + beta0c > T or beta0c > R - a13 - a23: ok = False
        rest1 = R - a13 - a12 - b1; rest3 = R - a23 - a12 - b2
        q3 = T - a13 - a23 - rest1; q1 = T - a13 - a23 - rest3
        if q3 < 0 or q1 < 0 or q3 > rest3 or q1 > rest1: ok = False
    if not ok: return None
    b1_aff = Aff(T - beta2) - A12; b2_aff = Aff(T - beta1c) - A12
    rest1_aff = Aff(R) - A13 - A12 - b1_aff      # = 16 - a13 - a12 - (T - beta2 - a12) = 16 - a13 - T + beta2
    rest3_aff = Aff(R) - A23 - A12 - b2_aff
    q3_aff = Aff(T) - A13 - A23 - rest1_aff; q1_aff = Aff(T) - A13 - A23 - rest3_aff
    rest1 = both(cellin(Tt, 1), notin('B1p')); rest3 = both(cellin(Tt, 3), notin('B2p'))
    steps = {3: {'avoid': [cellin((1, 2), 1, 2)]},
             4: {'picks': [('B0', cellin(Tt, 2), beta0c)], 'avoid': [contains(1, 3), 'B0']},
             5: {'picks': [('B1r', both(cellin(Tt, 2), notin('B0')), Aff(beta1c) - A13), ('B2p', cellin(Tt, 3), b2_aff)],
                 'avoid': [contains(1, 3), cellin(Tt, 1, 2), 'B1r', 'B2p']},
             6: {'picks': [('B1p', cellin(Tt, 1), b1_aff)],
                 'avoid': [contains(1, 3), cellin(Tt, 2, 3), both(both(cellin(Tt, 2), notin('B0')), notin('B1r')), 'B1p']},
             7: {'picks': [('Q3', rest3, q3_aff)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest1, 'Q3']},
             8: {'picks': [('Q1', rest1, q1_aff)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest3, 'Q1']}}
    return steps, 8

def make(steps, J, I1, I2, I3):
    hyps = [(A13, I2[0], I2[1], (1, 2)), (A12, I1[0], I1[1], (1, 3)), (A23, I3[0], I3[1], (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(J, R, T, steps, intersecting=True, hyps=hyps)

def try_cell(cell):
    I1, I2, I3 = cell; t0 = time.time(); tried = 0
    cands = []
    for beta1c in range(I2[1], R + 1): cands.append(('L1', (beta1c,)))
    for beta0c in range(0, T - I1[1] + 1):
        for beta1c in range(I2[1], R - beta0c + 1): cands.append(('S8', (beta0c, beta1c)))
    for fam, par in cands:
        res = script_L1(I1, I2, I3, *par) if fam == 'L1' else script_S8(I1, I2, I3, *par)
        if res is None: continue
        steps, J = res; tried += 1
        out = solve(make(steps, J, I1, I2, I3), time_limit=240, continuous=True)
        if out['status'].startswith('PROVER'):
            return (cell, fam, par, tried, round(time.time() - t0))
    return (cell, None, None, tried, round(time.time() - t0))

if __name__ == '__main__':
    cells = []
    for a in range(1, R):          # a12 in [a, a+1]
        for b in range(1, a + 1):  # a13 in [b, b+1]  (sorted region a12 >= a13 >= a23)
            for c in range(1, b + 1):
                if a + 1 + b + 1 > R + 1 or a + 1 + c + 1 > R + 1 or b + 1 + c + 1 > R + 1: pass
                cells.append(((a, a + 1), (b, b + 1), (c, c + 1)))
    print(f"{len(cells)} unit cells in the sorted region; T={T}", flush=True)
    with Pool(6) as pool:
        for (cell, fam, par, tried, secs) in pool.imap_unordered(try_cell, cells):
            print(json.dumps({'cell': cell, 'win': fam, 'par': par, 'tried': tried, 's': secs}), flush=True)
