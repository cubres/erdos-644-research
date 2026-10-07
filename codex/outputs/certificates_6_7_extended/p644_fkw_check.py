"""Validate the strategy verifier on FKW 1999: Theorem 2 Case 1 + Lemma 1 Case 1, r = 8k, budget 7k.
Edges placed in construction order: 1=A1, 2=A3, 3=A2, 4=A4, 5=A5, 6=A6, 7=A7.
We fix (a12, a13, a23) to constants (one MILP per triple) so all pick sizes are constants."""
import sys, time, math
from p644_strategy import *

def fkw_script(k, a12, a13, a23, budget_units):
    D = 8 * k
    B1sz = (k + a12) // 2; B2sz = (k + a12) - B1sz          # floor / ceil
    b2 = budget_units - a12 - B1sz; b1 = budget_units - a12 - B2sz
    steps = {}
    T = (1, 2, 3)   # all sets below are defined relative to the good triple A1=1, A3=2, A2=3
    steps[3] = {'picks': [('B1x', cellin((1, 2), 1), 4 * k - a13), ('B3x', cellin((1, 2), 2), 3 * k)],
                'avoid': [cellin((1, 2), 1, 2), 'B1x', 'B3x']}
    steps[4] = {'picks': [('B0', cellin(T, 2), budget_units - a12)],
                'avoid': [contains(1, 3), 'B0']}
    steps[5] = {'picks': [('B1r', both(cellin(T, 2), notin('B0')), B1sz - a13), ('B2p', cellin(T, 3), b2)],
                'avoid': [contains(1, 3), cellin(T, 1, 2), 'B1r', 'B2p']}
    steps[6] = {'picks': [('B1p', cellin(T, 1), b1)],
                'avoid': [contains(1, 3), cellin(T, 2, 3), both(both(cellin(T, 2), notin('B0')), notin('B1r')), 'B1p']}
    steps[7] = {'avoid': [cellin(T, 1, 2), cellin(T, 2, 3), both(cellin(T, 1), notin('B1p')), both(cellin(T, 3), notin('B2p'))]}
    hyps = [(mass(contains(1, 2)), a13, a13, (1, 2)), (mass(contains(1, 3)), a12, a12, (1, 3)), (mass(contains(2, 3)), a23, a23, (2, 3)),
            (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]   # good triple
    return Script(7, D, budget_units, steps, intersecting=True, hyps=hyps)

if __name__ == '__main__':
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 7 * k
    t0 = time.time(); wins = 0; survives = []; unknown = []
    for a13 in range(2 * k, 3 * k + 1):
        for a12 in range(a13, 4 * k + 1):
            for a23 in range(0, a13 + 1):
                if a13 + a23 > 5 * k: continue
                if 2 * a13 > k + a12: continue           # Lemma 1 Case 1
                sc = fkw_script(k, a12, a13, a23, budget)
                out = solve(sc, time_limit=300)
                tag = out['status'].split()[0]
                if tag == 'PROVER': wins += 1
                elif tag == 'ADVERSARY': survives.append((a12, a13, a23))
                else: unknown.append((a12, a13, a23))
    print(f"k={k} r={8*k} budget={budget} ({budget/(8*k):.4f} r): prover wins {wins}; adversary survives {len(survives)} {survives[:8]}; unknown {len(unknown)}  [{time.time()-t0:.0f}s]")
