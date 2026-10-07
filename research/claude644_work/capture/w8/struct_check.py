"""Claim?: every (p,2) family has a transversal of size <=2 or a transversal contained in an edge.
Random maximal families; exhaustive check of the claim for each."""
import random, sys, itertools
from wtd_search import has_p2

def check(edges, n):
    full = (1<<n) - 1
    tr = lambda m: all(e & m for e in edges)
    for a in range(n):
        for b in range(a, n):
            if tr((1<<a)|(1<<b)): return True
    return any(tr(e) for e in edges)

def run(n, p, iters, seed):
    rng = random.Random(seed); allsets = list(range(1, 1<<n)); fails = 0; nontriv = 0
    for it in range(iters):
        order = rng.sample(allsets, len(allsets))
        # bias to small sets sometimes
        if rng.random() < 0.5: order.sort(key=lambda s: bin(s).count('1') + rng.random()*3)
        edges = []
        for e in order:
            if has_p2(edges + [e], n, p): edges.append(e)
            if len(edges) > 14: break
        # reduce to inclusion-minimal edges (supersets irrelevant for transversals but matter for 'inside an edge')
        if not check(edges, n):
            fails += 1
            print('FAIL', [bin(e)[2:].zfill(n)[::-1] for e in edges], flush=True)
            if fails > 5: break
        # nontrivial: not intersecting and tau>=3
    print('done', n, p, iters, 'fails', fails)
run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
