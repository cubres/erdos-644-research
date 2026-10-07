#!/usr/bin/env python3
"""w5_dense_multiO_templates.py -- EXPLORATORY exact-integer test.  Model: E0 = one part (cap e, anchor type
(e,0,...,0)), O split into m parts.  Random intersecting type sets with continuous tau* > 3r/4 (found by a
simple hill-climb on tau*).  For each, test (i) full anchorability (Lemma 7.63, all assignments) and
(ii) whether the TWO TEMPLATES of the two-part proof suffice: balanced (one type with a<=e/2 on all six) or
star-small (type g1 on a star, g2 on the opposite triangle), i.e. anchorable() restricted to <=2 non-anchor types.
Usage: seed restarts m r"""
import sys, random, itertools
from w5_dense_anchor_climb import anchorable, tau_star, intersecting
seed, R, m, r = (int(v) for v in sys.argv[1:5]); random.seed(seed)
def rand_type(e, xs):
    for _ in range(100):
        a = random.randint(1, e); rest = r - a
        b = [0]*len(xs)
        for _ in range(rest):
            j = random.randrange(len(xs))
            if b[j] < xs[j]: b[j] += 1
        return [a] + b
def ok(G, caps):
    return all(all(0 <= g[i] <= caps[i] for i in range(len(caps))) and sum(g) <= r and g[0] >= 1 for g in G)
res = dict(inst=0, full_fail=0, twotemplate_fail=0)
for rs in range(R):
    e = random.randint(3*r//4 + 1, r); xs = [random.randint(r//4, r) for _ in range(m)]
    caps = [e] + xs
    G = [rand_type(e, xs) for _ in range(random.randint(3, 6))]
    anchor = [e] + [0]*m
    def score(G):
        allG = [anchor] + G
        if not intersecting(allG, caps): return -1
        return tau_star(allG, caps)
    cur = score(G)
    for it in range(6000):
        H = [list(g) for g in G]; i = random.randrange(len(H)); j, l = random.sample(range(m+1), 2)
        d = random.choice([1, 2, 3])
        if random.random() < 0.2: H[i] = rand_type(e, xs)
        elif H[i][j] >= d: H[i][j] -= d; H[i][l] += d
        if not ok(H, caps): continue
        s = score(H)
        if s >= cur: G, cur = H, s
    print("restart", rs, "caps", caps, "tau*/r", cur/r, flush=True)
    if 4*cur <= 3*r: continue
    res['inst'] += 1
    allG = [anchor] + G
    full = anchorable(allG, caps, 0)
    if full is None:
        res['full_fail'] += 1; print("FULL FAIL (non-anchorable, tau*>3r/4):", caps, allG, cur, flush=True); continue
    two = False
    for g1, g2 in itertools.product(G, repeat=2):
        if anchorable([anchor, g1, g2], caps, 0) is not None: two = True; break
    if not two:
        res['twotemplate_fail'] += 1; print("two-type templates insufficient:", caps, allG, "tau*", cur, "full", full, flush=True)
print(res)
