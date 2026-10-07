# Exact discrete protrusion game (integer vertices, budget m per protruding step).
# Val(j, state) = min over avoid-vectors Z of max(|Z|, max over adversary moves of Val(j+1, state')).
import sys, itertools
from functools import lru_cache
sys.path.insert(0, '.')
from fano import *

def make_solver(tlines, budgets, m_scale=1):
    n = 7
    tl = [frozenset(L) for L in tlines]
    def is_safe(S):
        return not any(L <= S for L in tl)
    # a pattern is 'dead' (can never become forced again) if S union (all steps >= j) is safe
    def dead(S, j):
        fut = S | frozenset(range(j, n))
        return is_safe(fut)
    @lru_cache(maxsize=None)
    def val(j, state):
        # state: tuple of (pattern(frozenset as sorted tuple), count), sorted
        if j == n:
            return 0
        m = budgets[j] * m_scale
        pats = [(frozenset(p), c) for p, c in state]
        if m == 0:
            # no outside mass at this step: nothing to avoid, nothing changes
            return val(j + 1, state)
        # forced counts
        forced = [c if not is_safe(p | {j}) else 0 for p, c in pats]
        best = None
        ranges = [range(f, c + 1) for (p, c), f in zip(pats, forced)]
        for z in itertools.product(*ranges):
            cost = sum(z)
            if best is not None and cost >= best:
                continue
            avail = [c - zz for (p, c), zz in zip(pats, z)]
            # adversary: choose g <= avail, sum g <= m; rest fresh
            worst = cost
            for g in bounded_vectors(avail, m):
                newd = {}
                used = sum(g)
                for (p, c), gg in zip(pats, g):
                    if c - gg > 0:
                        newd[p] = newd.get(p, 0) + c - gg
                    if gg > 0:
                        q = p | {j}
                        newd[q] = newd.get(q, 0) + gg
                fresh = m - used
                if fresh > 0:
                    q = frozenset({j})
                    newd[q] = newd.get(q, 0) + fresh
                # drop dead patterns
                newstate = tuple(sorted((tuple(sorted(p)), c) for p, c in newd.items() if not dead(p, j + 1)))
                v = val(j + 1, newstate)
                if v > worst:
                    worst = v
                    if best is not None and worst >= best:
                        break
            if best is None or worst < best:
                best = worst
        return best
    return val

def bounded_vectors(avail, m):
    # all integer vectors g with 0<=g_i<=avail_i and sum<=m
    def rec(i, rem):
        if i == len(avail):
            yield ()
            return
        for x in range(0, min(avail[i], rem) + 1):
            for rest in rec(i + 1, rem - x):
                yield (x,) + rest
    yield from rec(0, m)

if __name__ == '__main__':
    import time
    mode = sys.argv[1]
    mmax = int(sys.argv[2])
    reps = {}
    for order in itertools.permutations(range(7)):
        t = tuple(sorted(tuple(sorted(L)) for L in relabel(LINES, order)))
        reps.setdefault(t, order)
    results = []
    for t in reps:
        tlines = [frozenset(L) for L in t]
        budgets = [1] * 7 if mode == 'u' else [0] + [1] * 6
        row = []
        for m in range(1, mmax + 1):
            val = make_solver(tlines, budgets, m)
            t0 = time.time()
            row.append(val(0, ()))
        results.append((row, t))
        print(row, t, flush=True)
