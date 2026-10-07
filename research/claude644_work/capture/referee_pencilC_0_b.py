#!/usr/bin/env python3
"""Referee check of Lemma C on ACTUAL (7,2) families (exact (7,2) test).

Grow random families on n vertices by adding random edges that keep (7,2)
(exact: no <=7 edges without a <=2 transversal, via set-cover DFS), until
growth stalls.  Then for every U subset V check
   tau(H[U]) <= |U| - 4*min(floor((t-1)/3), floor(|U|/6))      (Lemma C, both forms)
   and tau(H[U]) <= 2*ceil(|U|/6) when 3*ceil(|U|/6) <= t-1.
Also record the tightest slack observed.
"""
import itertools, random, sys

def tau_mask(masks, n):
    if not masks: return 0
    for s in range(n + 1):
        for T in itertools.combinations(range(n), s):
            tm = 0
            for i in T: tm |= 1 << i
            if all(m & tm for m in masks): return s

def is72(masks, n):
    """True iff every <=7 edges have a transversal of size <=2."""
    covers = [1 << i for i in range(n)] + [(1 << i) | (1 << j) for i, j in itertools.combinations(range(n), 2)]
    # need: no choice of <=7 edges such that every cover S is disjoint from one of them
    def dfs(alive, depth):
        # alive: list of covers not yet killed
        if not alive: return True  # found bad tuple
        if depth == 7: return False
        S = alive[0]
        for m in set(masks):
            if not (m & S):
                nxt = [c for c in alive if c & m]
                if dfs(nxt, depth + 1): return True
        return False
    return not dfs(covers, 0)

def grow(rng, n, lo, hi, tries):
    masks = []
    for _ in range(tries):
        sz = rng.randint(lo, hi)
        m = 0
        for i in rng.sample(range(n), sz): m |= 1 << i
        if m in masks: continue
        if is72(masks + [m], n):
            masks.append(m)
    return masks

def main(fams=40, seed=3):
    rng = random.Random(seed)
    worst = None
    checked = 0
    tdist = {}
    for f in range(fams):
        n = rng.randint(8, 10)
        lo = rng.randint(2, 5); hi = rng.randint(lo, min(n - 1, lo + 3))
        masks = grow(rng, n, lo, hi, rng.randint(60, 160))
        t = tau_mask(masks, n)
        tdist[t] = tdist.get(t, 0) + 1
        for r in range(n + 1):
            for U in itertools.combinations(range(n), r):
                um = sum(1 << i for i in U)
                HU = [m for m in masks if m & ~um == 0]
                q = tau_mask(HU, n)
                N = len(U)
                u = min((t - 1) // 3, N // 6)
                bound = N - 4 * u
                assert q <= bound, ("VIOLATION i", t, q, N, U)
                c6 = -(-N // 6)
                if 3 * c6 <= t - 1:
                    assert q <= 2 * c6, ("VIOLATION ii", t, q, N, U)
                checked += 1
                if (t - 1) // 3 >= 1 and N >= 6:
                    sl = bound - q
                    if worst is None or sl < worst[0]: worst = (sl, t, q, N)
    print("families:", fams, "t distribution:", tdist, "U checked:", checked, "min slack (u>=1):", worst)

if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))
