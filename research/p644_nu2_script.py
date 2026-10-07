"""Erdős #644 — matching number 2, budget 3r/4: machine check of the six-edge lemma.

Lemma (hand proof).  A1 ∩ A2 = ∅, A3 any edge with a13 + a23 <= 3T - 2r (= r/4 at T = 3r/4).
Put B1' ⊆ A1 - A13 with |B1'| = T - a23, B2' ⊆ A2 - A23 with |B2'| = T - a13, and take
   A5 avoiding A13 ∪ B2',   A6 avoiding A23 ∪ B1',   A7 avoiding (A1 - B1') ∪ (A2 - B2').
Then {A1, A2, A3, A5, A6, A7} is not 2-pierceable.  Edge indices here: 1=A1, 2=A2, 3=A3, 4=A5, 5=A6, 6=A7.
"""
import sys, time
from p644_strategy import *

def nu2_six(D, T, a13, a23):
    Tr = (1, 2, 3)
    steps = {}
    steps[4] = {'picks': [('B2p', cellin(Tr, 2), T - a13)], 'avoid': [contains(1, 3), 'B2p']}
    steps[5] = {'picks': [('B1p', cellin(Tr, 1), T - a23)], 'avoid': [contains(2, 3), 'B1p']}
    steps[6] = {'avoid': [both(contains(1), notin('B1p')), both(contains(2), notin('B2p'))]}
    hyps = [(mass(contains(1, 2)), 0, 0, (1, 2)), (mass(contains(1, 3)), a13, a13, (1, 3)),
            (mass(contains(2, 3)), a23, a23, (2, 3))]
    return Script(6, D, T, steps, intersecting=False, hyps=hyps)

if __name__ == '__main__':
    D = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cont = '--cont' in sys.argv
    t0 = time.time(); wins = []; surv = []; unk = []
    for a13 in range(0, D + 1):
        for a23 in range(0, a13 + 1):
            sc = nu2_six(D, T, a13, a23)
            out = solve(sc, time_limit=300, continuous=cont)
            tag = out['status'].split()[0]
            (wins if tag == 'PROVER' else surv if tag == 'ADVERSARY' else unk).append((a13, a23))
    print(f"r={D} T={T} continuous={cont}: prover wins at {len(wins)} pairs (a13>=a23): {wins}")
    print(f"  adversary survives at {len(surv)}: {surv[:20]}{'...' if len(surv) > 20 else ''}; unknown {unk}  [{time.time()-t0:.0f}s]")
    # legality on the boundary case
    for (a13, a23) in [(4, 0), (2, 2), (3, 1)]:
        if a13 + a23 <= 3 * T - 2 * D:
            print(f"  budget report ({a13},{a23}):", check_budget(nu2_six(D, T, a13, a23)))
