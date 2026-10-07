"""
Exact check of the Triple Lemma on actual (7,2) families (non-uniform allowed):
  E,F,G in H with E&F&G = empty  ==>  tau(H) <= floor((|E u F u G| + 3)/2).
Families: random (7,2)-preserving greedy growth from random seeds on n<=10 vertices,
edge sizes in [2,r].  (7,2) is tested exactly (set-cover DFS in lib72.py); tau exactly.
Run: python3 test_triple_lemma.py [trials]
"""
import random, itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib72 import *

trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
random.seed(11)
checked = 0; mingap = None; hist = {}
for trial in range(trials):
    n = random.randint(6, 10)
    r = random.randint(3, min(7, n - 1))
    H = []
    for _ in range(random.randint(10, 40)):
        size = random.randint(max(2, r - 2), r)
        S = sum(1 << v for v in random.sample(range(n), size))
        if S in H: continue
        if is_72(H + [S], n):
            H.append(S)
    t = tau(H, n)
    gap_best = None
    for E, F, G in itertools.combinations(H, 3):
        if E & F & G: continue
        bound = (popcount(E | F | G) + 3) // 2
        if t > bound:
            print("VIOLATION", n, t, [bin(x) for x in (E, F, G)], flush=True); raise SystemExit(1)
        g = bound - t
        if gap_best is None or g < gap_best: gap_best = g
    checked += 1
    hist[t] = hist.get(t, 0) + 1
    if gap_best is not None and (mingap is None or gap_best < mingap): mingap = gap_best
print("families checked:", checked, "tau histogram:", dict(sorted(hist.items())),
      "min (bound - tau) over families with a good triple:", mingap, flush=True)
