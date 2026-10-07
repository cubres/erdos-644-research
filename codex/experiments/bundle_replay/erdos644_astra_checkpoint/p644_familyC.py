"""Family C probe for the clustered regime a12 >= r/2 at budget T = 13 (r = 16, continuous masses).
Every edge A_j (j >= 3) avoids W = A1 ∩ A2 entirely and spends the leftover budget (T - a12) on one
or two cells of the current configuration (chosen from a menu); random search over menus/amounts.
A 'win' = MILP infeasible on the whole interval cell."""
import sys, time, random, json, itertools
from p644_strategy import *
R, T = 16, 13
A12 = mass(contains(1, 3)); A13 = mass(contains(1, 2)); A23 = mass(contains(2, 3))

def menu(j):
    """candidate cells (predicates) outside W for step j, over placed edges 1..j-1 (1=A1, 3=A2 by convention? no: here 1=A1, 2=A2, then 3..j-1)"""
    placed = list(range(1, j))
    cands = []
    # A1\A2, A2\A1
    cands.append(('A1-W', cellin((1, 2), 1))); cands.append(('A2-W', cellin((1, 2), 2)))
    # intersections of previous new edges outside A1∪A2, and inside A1\W or A2\W
    prev = [e for e in placed if e >= 3]
    for s in range(1, len(prev) + 1):
        for S in itertools.combinations(prev, s):
            base = tuple(placed)
            cands.append((f'out∩{S}', cellin(base, *S)))                          # in exactly S among placed (outside A1,A2)
            cands.append((f'A1∩{S}', cellin(base, 1, *S)))                       # in A1 (not A2) and exactly S
            cands.append((f'A2∩{S}', cellin(base, 2, *S)))
    return cands

def random_script(I1, I2, I3, J, rng):
    a12hi = I1[1]; left = T - a12hi
    steps = {3: {'avoid': [contains(1, 2)]}}   # A3 avoids W (we do not fix A3's traces; the cell hyps fix a13,a23)
    desc = {}
    for j in range(4, J + 1):
        cands = menu(j)
        kA, predA = rng.choice(cands)
        if rng.random() < 0.5 or left < 2:
            picks = [(f'P{j}', predA, left)]; desc[j] = [(kA, left)]
        else:
            kB, predB = rng.choice(cands); u = rng.randint(1, left - 1)
            picks = [(f'P{j}a', predA, u), (f'P{j}b', predB, left - u)]; desc[j] = [(kA, u), (kB, left - u)]
        steps[j] = {'picks': picks, 'avoid': [contains(1, 2)] + [p[0] for p in picks]}
    return steps, desc

def cell_script(steps, J, I1, I2, I3):
    # edges: 1=A1, 2=A2, 3=A3 ; hyps: a12 = |A1∩A2| in I1 ; a13 = |A1∩A3| in I2 ; a23 = |A2∩A3| in I3 ; a123 = 0
    hyps = [(mass(contains(1, 2)), I1[0], I1[1], (1, 2)), (mass(contains(1, 3)), I2[0], I2[1], (1, 3)), (mass(contains(2, 3)), I3[0], I3[1], (2, 3)), (mass(contains(1, 2, 3)), 0, 0, (1, 2, 3))]
    return Script(J, R, T, steps, intersecting=True, hyps=hyps)

if __name__ == '__main__':
    cells = [((8, 9), (3, 4), (2, 3)), ((10, 11), (2, 3), (1, 2)), ((12, 13), (2, 3), (1, 2))]
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    J = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    for cell in cells:
        I1, I2, I3 = cell; t0 = time.time(); won = None
        for t in range(tries):
            steps, desc = random_script(I1, I2, I3, J, rng)
            out = solve(cell_script(steps, J, I1, I2, I3), time_limit=120, continuous=True)
            if out['status'].startswith('PROVER'):
                won = desc; print(f"WIN cell {cell} J={J}: {desc}", flush=True); break
        print(f"cell {cell} J={J}: {'WIN' if won else 'no win in '+str(tries)+' random scripts'} [{time.time()-t0:.0f}s]", flush=True)
