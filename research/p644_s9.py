"""S9 family: like S8 but B0 (the part of A3 avoided together with A12) is split into two parts B0a, B0b,
avoided by two edges A4a, A4b.  Edges: 1=A1, 2=A3, 3=A2, 4=A4a, 5=A4b, 6=A5, 7=A6, 8=A7, 9=A8.
Needed exactly at a12 = 8 (units r/16) where S8's arithmetic fails by one unit."""
import sys, time
from p644_strategy import *
R, T = 16, 13
A12 = mass(contains(1, 3)); A13 = mass(contains(1, 2)); A23 = mass(contains(2, 3)); Tt = (1, 2, 3)

def script_S9(I1, I2, I3, beta0a, beta0b, beta1c):
    beta0 = beta0a + beta0b; beta2 = R - beta0 - beta1c
    for (a12, a13, a23) in [(a, b, c) for a in I1 for b in I2 for c in I3]:
        b2 = T - a12 - beta1c; b1 = T - a12 - beta2
        if beta1c < a13 or beta2 < a23 or b1 < 0 or b2 < 0: return None
        if b1 > R - a13 - a12 or b2 > R - a23 - a12: return None
        if a12 + beta0a > T or a12 + beta0b > T or beta0 > R - a13 - a23: return None
        rest1 = R - a13 - a12 - b1; rest3 = R - a23 - a12 - b2
        q3 = T - a13 - a23 - rest1; q1 = T - a13 - a23 - rest3
        if q3 < 0 or q1 < 0 or q3 > rest3 or q1 > rest1: return None
    b1_aff = Aff(T - beta2) - A12; b2_aff = Aff(T - beta1c) - A12
    rest1_aff = Aff(R) - A13 - A12 - b1_aff; rest3_aff = Aff(R) - A23 - A12 - b2_aff
    q3_aff = Aff(T) - A13 - A23 - rest1_aff; q1_aff = Aff(T) - A13 - A23 - rest3_aff
    rest1 = both(cellin(Tt, 1), notin('B1p')); rest3 = both(cellin(Tt, 3), notin('B2p'))
    steps = {3: {'avoid': [cellin((1, 2), 1, 2)]},
             4: {'picks': [('B0a', cellin(Tt, 2), beta0a)], 'avoid': [contains(1, 3), 'B0a']},
             5: {'picks': [('B0b', both(cellin(Tt, 2), notin('B0a')), beta0b)], 'avoid': [contains(1, 3), 'B0b']},
             6: {'picks': [('B1r', both(both(cellin(Tt, 2), notin('B0a')), notin('B0b')), Aff(beta1c) - A13), ('B2p', cellin(Tt, 3), b2_aff)],
                 'avoid': [contains(1, 3), cellin(Tt, 1, 2), 'B1r', 'B2p']},
             7: {'picks': [('B1p', cellin(Tt, 1), b1_aff)],
                 'avoid': [contains(1, 3), cellin(Tt, 2, 3), both(both(both(cellin(Tt, 2), notin('B0a')), notin('B0b')), notin('B1r')), 'B1p']},
             8: {'picks': [('Q3', rest3, q3_aff)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest1, 'Q3']},
             9: {'picks': [('Q1', rest1, q1_aff)], 'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), rest3, 'Q1']}}
    hyps = [(A13, I2[0], I2[1], (1, 2)), (A12, I1[0], I1[1], (1, 3)), (A23, I3[0], I3[1], (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(9, R, T, steps, intersecting=True, hyps=hyps)

if __name__ == '__main__':
    cells = [((8, 8), (5, 5), (3, 3)), ((8, 8), (8, 8), (3, 3)), ((7, 7), (7, 7), (2, 2)), ((8, 9), (5, 6), (3, 4))]
    for cell in cells:
        I1, I2, I3 = cell; t0 = time.time(); won = None; tried = 0
        for beta0a in range(0, T - I1[1] + 1):
            for beta0b in range(beta0a, T - I1[1] + 1):
                for beta1c in range(I2[1], R - beta0a - beta0b + 1):
                    sc = script_S9(I1, I2, I3, beta0a, beta0b, beta1c)
                    if sc is None: continue
                    tried += 1
                    out = solve(sc, time_limit=900, continuous=True)
                    print(f"   cell {cell} beta0=({beta0a},{beta0b}) beta1={beta1c}: {out['status']} [{time.time()-t0:.0f}s]", flush=True)
                    if out['status'].startswith('PROVER'): won = (beta0a, beta0b, beta1c); break
                if won: break
            if won: break
        print(f"CELL {cell}: {'WIN '+str(won) if won else 'no win'} (tried {tried}) [{time.time()-t0:.0f}s]", flush=True)
