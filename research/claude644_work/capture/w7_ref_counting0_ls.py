#!/usr/bin/env python3
"""w7_ref_counting0_ls.py n k iters seed -- NUMERICAL local search for lex-min (|P7|,|Pi7|) 7-tuples of K_n^(k)
(blocks = complements, size n-k), then report hypothesis status at all distinct best tuples found."""
import sys, random, itertools
import w7_ref_counting0_complete as C
n, k, iters, seed = map(int, sys.argv[1:5]); b = n - k
rng = random.Random(seed)
prs = list(itertools.combinations(range(n), 2))
def key(blocks):
    cov = [sum(1 for B in blocks if u in B and v in B) for (u, v) in prs]
    Pi = [pr for pr, c in zip(prs, cov) if c == 0]
    return (len(set(x for pr in Pi for x in pr)), len(Pi))
best = None; bests = []
for rest in range(iters):
    blocks = [set(rng.sample(range(n), b)) for _ in range(7)]
    cur = key(blocks); T = 2.0
    for step in range(4000):
        j = rng.randrange(7); out = rng.choice(sorted(blocks[j])); inn = rng.choice([v for v in range(n) if v not in blocks[j]])
        blocks[j].remove(out); blocks[j].add(inn)
        new = key(blocks)
        dv = (new[0] - cur[0]) * 100 + (new[1] - cur[1])
        if dv <= 0 or rng.random() < pow(2.718, -dv / T): cur = new
        else: blocks[j].remove(inn); blocks[j].add(out)
        T = max(0.05, T * 0.999)
        if best is None or cur < best: best = cur; bests = []
        if cur == best and len(bests) < 200: bests.append([set(B) for B in blocks])
res = [C.exact_check(n, k, bl) for bl in bests]
print('n k', n, k, 'best (P,Pi) found', best, 'tuples', len(res), 'hyp true in', sum(r['hyp'] for r in res),
      'refined true in', sum(r['hyp2'] for r in res), 'max avg bound', max(r['sum_bound_over7'] for r in res), 't', n - k + 1)
print('D7 values', sorted(set(r['D7'] for r in res)))
