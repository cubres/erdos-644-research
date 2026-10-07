# print, for a given order and m, the adversary's best responses to every prover first-move etc. (depth-limited)
import sys, itertools
sys.path.insert(0, '.')
from discrete_game import make_solver, bounded_vectors
from fano import *

def explore(tl, budgets, m, depth=2):
    tl = [frozenset(L) for L in tl]
    val = make_solver(tl, budgets, m)
    n = 7
    def is_safe(S): return not any(L <= S for L in tl)
    def dead(S, j): return is_safe(S | frozenset(range(j, n)))
    def moves(j, state):
        pats = [(frozenset(p), c) for p, c in state]
        mm = budgets[j] * m
        forced = [c if not is_safe(p | {j}) else 0 for p, c in pats]
        out = []
        for z in itertools.product(*[range(f, c + 1) for (p, c), f in zip(pats, forced)]):
            avail = [c - zz for (p, c), zz in zip(pats, z)]
            reps = []
            for g in bounded_vectors(avail, mm):
                newd = {}
                for (p, c), gg in zip(pats, g):
                    if c - gg > 0: newd[p] = newd.get(p, 0) + c - gg
                    if gg > 0:
                        q = p | {j}; newd[q] = newd.get(q, 0) + gg
                fresh = mm - sum(g)
                if fresh > 0:
                    q = frozenset({j}); newd[q] = newd.get(q, 0) + fresh
                ns = tuple(sorted((tuple(sorted(p)), c) for p, c in newd.items() if not dead(p, j + 1)))
                reps.append((g, ns, val(j + 1, ns)))
            out.append((z, sum(z), reps))
        return pats, out
    def show(j, state, d, indent=''):
        if j == n or d == 0: return
        if budgets[j] == 0:
            show(j + 1, state, d, indent); return
        pats, out = moves(j, state)
        v = val(j, state)
        print(indent + f"step {j} state {[(p, c) for p, c in state]} value {v}")
        for z, cost, reps in out:
            w = max([cost] + [r[2] for r in reps])
            best = max(reps, key=lambda r: r[2])
            print(indent + f"  avoid {dict((tuple(sorted(p)), zz) for (p, c), zz in zip(pats, z) if zz)} cost {cost} -> worst {w}; adversary best reuse {dict((tuple(sorted(p)), gg) for (p, c), gg in zip(pats, best[0]) if gg)} -> {best[2]}")
            if w == v and d > 1:
                show(j + 1, best[1], d - 1, indent + '    ')
    show(0, (), depth)

if __name__ == '__main__':
    tl = eval(sys.argv[1]); mode = sys.argv[2]; m = int(sys.argv[3]); d = int(sys.argv[4])
    budgets = [1] * 7 if mode == 'u' else [0] + [1] * 6
    explore(tl, budgets, m, d)
