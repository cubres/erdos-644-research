#!/usr/bin/env python3
"""w7_ref_counting0_bf_t3.py -- referee counting#0: same exhaustive checks as w7_ref_counting0_bf.py but on
families with tau >= 3: random <=13-edge subfamilies of K_n^(k) (and mixed-rank perturbations) filtered to
(7,2) and tau>=3.  Usage: SEED NFAM"""
import itertools, random, sys
from collections import Counter
import w7_ref_counting0_bf as B
seed = int(sys.argv[1]); NF = int(sys.argv[2])
rng = random.Random(seed)
stats = Counter(); stats['tmax'] = 0
tries = 0
while stats['fam'] < NF:
    tries += 1
    n, k = rng.choice([(6, 4), (7, 5), (8, 5), (8, 6), (9, 6), (9, 5), (10, 6)])
    allE = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)]
    m = rng.randint(6, 13)
    H = rng.sample(allE, m)
    if rng.random() < 0.3:  # shrink some edges (rank <= k, non-uniform)
        H = [E & ~(1 << rng.choice([v for v in range(n) if (E >> v) & 1])) if rng.random() < .3 else E for E in H]
    H = sorted(set(H))
    if B.tau(H, n) < 3: continue
    B.run_family(H, n, stats, rng)
print('seed', seed, 'tries', tries, dict(stats))
print('ALL (a)-(d) CHECKS PASS on every minimiser')
