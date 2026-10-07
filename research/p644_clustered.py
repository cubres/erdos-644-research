"""Clustered family for a12 >= r/2 (units of r/16, r=16, T=13, continuous masses).
Two disjoint edges cannot exist in an intersecting family, but two edges A1,A2 with a12 >= 8 still leave
each of A1\A2, A2\A1 of size <= 8.  Anchor W = A1 ∩ A2 (mass a12).  Every further edge Aj (j>=3) MUST meet
both A1 and A2 (intersecting); to have tau large it should avoid W where possible.  We build a
Fano-like sub-structure on A1\A2, A2\A1 and the outside.  Sound picks (min(size,host)).
Strategy family CL(par): A3 avoids W; A4..A8 each avoid W plus a chosen union of earlier cells of total
budget T - (mass in W they are forced to keep = 0, since they avoid W) = T; the picks form a Fano
complement on the 7 edges restricted to (A1\A2) ∪ (A2\A1) ∪ outside.
Here we just verify, per cell, whether the MOST AGGRESSIVE avoidance (each Aj avoids W and all previously
built structure it can within budget T) already forces a bad 7-tuple."""
import sys, time, itertools
from p644_strategy import *
R, T = 16, 13

def cluster_script(I1, I2, I3, J, avoid_plan):
    """avoid_plan[j] = list of predicate-builders taking (placed) -> predicate, plus optional pick sizes.
    We keep it simple: each Aj (j>=3) avoids W (=A1∩A2) entirely, PLUS a set 'S_j' of size (T - 0) chosen
    from the menu (subset of union of A1\\A2, A2\\A1, and previous new-edge cells outside W)."""
    steps = {3: {'avoid': [contains(1, 2)]}}
    for j in range(4, J + 1):
        picks = []; avoids = [contains(1, 2)]
        for idx, (name, pred, size) in enumerate(avoid_plan.get(j, [])):
            pn = f'C{j}_{idx}'; picks.append((pn, pred, size)); avoids.append(pn)
        steps[j] = {'picks': picks, 'avoid': avoids}
    hyps = [(mass(contains(1, 2)), I1[0], I1[1], (1, 2)), (mass(contains(1, 3)), I2[0], I2[1], (1, 3)),
            (mass(contains(2, 3)), I3[0], I3[1], (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(J, R, T, steps, intersecting=True, hyps=hyps)

def fano_on_two_parts(I1, I2, I3, u):
    """Aim: 7 edges whose restriction to (A1\\A2)∪(A2\\A1)∪outside is a Fano complement.
    We prescribe A4..A8 (5 more edges; A1=1,A2=2,A3=3 already) via avoidances of prior cells of size u each
    in A1\\A2 and outside, mirroring the Fano lines.  Parameter u sets how much each edge spends."""
    A1m2 = cellin((1, 2), 1); A2m1 = cellin((1, 2), 2)
    plan = {}
    # A4 avoids (u of A1\A2) and (u of A2\A1)  [Fano: line through the A3-axis]
    plan[4] = [('n', A1m2, u), ('n', A2m1, u)]
    # A5 avoids (u of A1\A2 outside A4's avoid) and (u of cell{3,4} outside)
    for j in range(5, 9):
        prev = tuple(range(3, j))
        plan[j] = [('n', A1m2, u), ('n', cellin(tuple(range(1, j)), *prev), u)]
    return plan

if __name__ == '__main__':
    cells = [((8, 9), (3, 4), (2, 3)), ((10, 11), (2, 3), (1, 2)), ((12, 13), (2, 3), (1, 2)),
             ((8, 9), (8, 9), (3, 4)), ((14, 15), (1, 2), (1, 2))]
    for cell in cells:
        I1, I2, I3 = cell; t0 = time.time(); won = None
        for u in range(1, T + 1):
            for J in (7, 8):
                plan = fano_on_two_parts(I1, I2, I3, u)
                plan = {j: v for j, v in plan.items() if j <= J}
                sc = cluster_script(I1, I2, I3, J, plan)
                out = solve(sc, time_limit=180, continuous=True)
                if out['status'].startswith('PROVER'):
                    won = (u, J); print(f"WIN cell {cell}: u={u} J={J} [{time.time()-t0:.0f}s]", flush=True); break
            if won: break
        print(f"CELL {cell}: {'WIN '+str(won) if won else 'no win'} [{time.time()-t0:.0f}s]", flush=True)
