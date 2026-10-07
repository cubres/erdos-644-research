"""Search for prover wins at budget T=13 (beta=13/16, r=16) over generalised FKW-type scripts.
Edges: 1=A1, 2=A3, 3=A2, then A4..A7 (and optionally A8).  For each reachable triple (a12,a13,a23)
try parameter choices; report triples with at least one legal winning script."""
import sys, time, itertools
from p644_strategy import *

k, r, T = 2, 16, 13
def script7(a12, a13, a23, u1, u3, beta0, beta1, avoid7=None):
    """Lemma-1-type 7-edge script with free parameters; returns None if illegal (budget/size)."""
    # step 3: A2 avoids A13 ∪ (u1 of A1\A3) ∪ (u3 of A3\A1); needs a13 + u1 + u3 <= T
    if a13 + u1 + u3 > T: return None
    if u1 > r - a13 or u3 > r - a13: return None
    # reachable: a12 <= r - a13 - u1 ; a23 <= r - a13 - u3
    if a12 > r - a13 - u1 or a23 > r - a13 - u3: return None
    Tt = (1, 2, 3)
    beta2 = r - beta0 - beta1
    if beta0 < 0 or beta1 < a13 or beta2 < a23: return None
    if a12 + beta0 > T: return None                      # A4 avoids A12 ∪ B0
    b2 = T - a12 - beta1; b1 = T - a12 - beta2
    if b1 < 0 or b2 < 0: return None
    if b1 > r - a13 - a12 or b2 > r - a23 - a12: return None   # B1' ⊆ A1−A13−A12, B2' ⊆ A2−A23−A12
    B4 = (2 * r - a12) - a12 - b1 - b2                         # |(A1∪A2) − A12 − B1' − B2'|
    if B4 > T: return None
    steps = {}
    steps[3] = {'picks': [('B1x', cellin((1, 2), 1), u1), ('B3x', cellin((1, 2), 2), u3)], 'avoid': [cellin((1, 2), 1, 2), 'B1x', 'B3x']}
    steps[4] = {'picks': [('B0', cellin(Tt, 2), beta0)], 'avoid': [contains(1, 3), 'B0']}
    steps[5] = {'picks': [('B1r', both(cellin(Tt, 2), notin('B0')), beta1 - a13), ('B2p', cellin(Tt, 3), b2)],
                'avoid': [contains(1, 3), cellin(Tt, 1, 2), 'B1r', 'B2p']}
    steps[6] = {'picks': [('B1p', cellin(Tt, 1), b1)],
                'avoid': [contains(1, 3), cellin(Tt, 2, 3), both(both(cellin(Tt, 2), notin('B0')), notin('B1r')), 'B1p']}
    steps[7] = {'avoid': [cellin(Tt, 1, 2), cellin(Tt, 2, 3), both(cellin(Tt, 1), notin('B1p')), both(cellin(Tt, 3), notin('B2p'))]}
    hyps = [(mass(contains(1, 2)), a13, a13, (1, 2)), (mass(contains(1, 3)), a12, a12, (1, 3)), (mass(contains(2, 3)), a23, a23, (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(7, r, T, steps, intersecting=True, hyps=hyps)

if __name__ == '__main__':
    t0 = time.time(); handled = {}; unhandled = []
    triples = [(a12, a13, a23) for a13 in range(1, r) for a12 in range(1, r) for a23 in range(0, r) if a12 + a13 <= r and a12 + a23 <= r and a13 + a23 <= r]
    # restrict to the region a12 >= a13 >= a23 (WLOG by relabelling the good triple) and good triple only
    triples = [t for t in triples if t[0] >= t[1] >= t[2]]
    print(f"{len(triples)} ordered triples (a12>=a13>=a23) to cover at T={T}", flush=True)
    for (a12, a13, a23) in triples:
        won = None; tried = 0
        for u1 in range(0, T + 1):
            for u3 in range(0, T + 1 - u1):
                for beta0 in range(0, T + 1):
                    for beta1 in range(a13, r + 1):
                        sc = script7(a12, a13, a23, u1, u3, beta0, beta1)
                        if sc is None: continue
                        tried += 1
                        out = solve(sc, time_limit=60)
                        if out['status'].startswith('PROVER'): won = (u1, u3, beta0, beta1); break
                    if won: break
                if won: break
            if won: break
        if won: handled[(a12, a13, a23)] = won
        else: unhandled.append(((a12, a13, a23), tried))
        print(f"  triple {(a12,a13,a23)}: {'WIN '+str(won) if won else 'no win'} (legal scripts tried: {tried}) [{time.time()-t0:.0f}s]", flush=True)
    print(f"handled {len(handled)} / {len(triples)}; unhandled: {[u[0] for u in unhandled]}")
