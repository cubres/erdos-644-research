#!/usr/bin/env python3
"""w5_dense_twopart_general_templates.py -- EXPLORATORY exact-integer test for GENERAL two-part anchored models:
two parts (caps x1,x2), non-uniform types (u,v) with u+v <= r, intersecting, continuous tau* > 3r/4; EVERY type is
tried as the anchor.  Checks (i) full anchorability (Lemma 7.63) and (ii) whether <= 2 distinct non-anchor
types (plus copies of the anchor) suffice.  Random staircase-style generation + hill-climb on tau*.
Usage: seed restarts r"""
import sys, random, itertools
from w5_dense_anchor_climb import anchorable, tau_star, intersecting
seed, R, r = (int(v) for v in sys.argv[1:4]); random.seed(seed)
res = dict(fam=0, anchors=0, full_fail=0, two_fail=0)
for rs in range(R):
    x1 = random.randint(r//3, 2*r); x2 = random.randint(r//3, 2*r); caps = [x1, x2]
    def rt():
        s = random.randint(3*r//4, r); u = random.randint(max(0, s - x2), min(s, x1)); return [u, s - u]
    G = [rt() for _ in range(random.randint(3, 6))]
    def sc(G):
        if not intersecting(G, caps) or any(sum(g) == 0 for g in G): return -1
        return tau_star(G, caps)
    cur = sc(G)
    for it in range(3000):
        H = [list(g) for g in G]; m = random.random()
        if m < 0.15 and len(H) < 7: H.append(rt())
        elif m < 0.25 and len(H) > 2: H.pop(random.randrange(len(H)))
        else:
            g = random.randrange(len(H)); d = random.choice([-2,-1,1,2]); j = random.randrange(2)
            H[g][j] += d
            if random.random() < 0.5: H[g][1-j] -= d
        if any(h[0] < 0 or h[1] < 0 or h[0] > x1 or h[1] > x2 or sum(h) > r for h in H): continue
        s = sc(H)
        if s >= cur: G, cur = H, s
    if 4*cur <= 3*r: continue
    res['fam'] += 1
    for ai in range(len(G)):
        res['anchors'] += 1
        if anchorable(G, caps, ai) is None:
            res['full_fail'] += 1; print("FULL FAIL", caps, G, "anchor", G[ai], "tau*", cur, flush=True); continue
        others = [g for j, g in enumerate(G) if j != ai]
        ok2 = any(anchorable([G[ai], g1, g2], caps, 0) is not None for g1, g2 in itertools.combinations_with_replacement(others, 2)) \
              or anchorable([G[ai]], caps, 0) is not None
        if not ok2:
            res['two_fail'] += 1; print("needs >=3 types:", caps, G, "anchor", G[ai], "tau*/r", cur/r, flush=True)
print(res, flush=True)
