"""
Triple Lemma check on (7,2) families with larger tau: seeds = random subfamilies of complete
r-uniform families on N<7r/4 points ((N,r) in {(6,4),(8,5),(9,6)}), augmented by extra
vertices and random edges of mixed sizes while preserving (7,2) (exact test).
Run: python3 test_triple_lemma2.py [trials]
"""
import random, itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib72 import *
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 60
random.seed(5)
checked = 0; hist = {}; tightcount = 0
for trial in range(trials):
    N, r = random.choice([(6, 4), (8, 5), (9, 6)])
    n = N + random.randint(0, 3)
    base = complete(N, r)
    H = random.sample(base, random.randint(len(base) // 2, len(base)))
    if not is_72(H, n): continue
    for _ in range(12):
        size = random.randint(max(2, r - 2), r)
        S = sum(1 << v for v in random.sample(range(n), size))
        if S in H: continue
        if is_72(H + [S], n): H.append(S)
    t = tau(H, n)
    gb = None
    for E, F, G in itertools.combinations(H, 3):
        if E & F & G: continue
        bound = (popcount(E | F | G) + 3) // 2
        if t > bound:
            print("VIOLATION", n, t, [bin(x) for x in (E, F, G)], flush=True); raise SystemExit(1)
        gb = bound - t if gb is None else min(gb, bound - t)
    checked += 1; hist[t] = hist.get(t, 0) + 1
    if gb is not None and gb <= 1: tightcount += 1
print("checked", checked, "tau hist", dict(sorted(hist.items())), "families with bound-tau<=1:", tightcount, flush=True)
