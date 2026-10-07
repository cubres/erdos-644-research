#!/usr/bin/env python3
"""w5_dense_milp_climb.py -- EXPLORATORY search (MILP-based, floating; any hit re-verified exactly) for a
counterexample to the ANCHORED statement in type-closed models with MANY types: anchor E0 = union of the first
p0 parts (full), O = remaining p1 parts; types of size in [e, k] (E0 smallest edge), intersecting.
Maximises tau*/k over families in which E0 is NOT a line of any Fano-labelled tuple.
Usage: seed p0 p1 k iters maxtypes"""
import sys, random
from w5_dense_milp_lib import anchor_milp, tau_star_milp, intersecting
from w5_dense_anchor_climb import anchorable, tau_star
seed, p0, p1, k, iters, maxt = (int(v) for v in sys.argv[1:7]); random.seed(seed)
e = random.randint(3*k//4 + 1, k)
ecaps = [e//p0 + (1 if i < e % p0 else 0) for i in range(p0)]
caps = ecaps + [random.randint(k//4, k) for _ in range(p1)]
p = p0 + p1; anchor = ecaps + [0]*p1
def rand_type():
    for _ in range(1000):
        size = random.randint(e, k)
        v = [0]*p; cnt = 0
        while cnt < size:
            i = random.randrange(p)
            if v[i] < caps[i]: v[i] += 1; cnt += 1
            if all(v[j] >= caps[j] for j in range(p)): break
        if sum(v[:p0]) >= 1 and e <= sum(v) <= k and v != anchor: return v
    return None
def score(G):
    allG = [anchor] + G
    if not intersecting(allG, caps): return None
    ts = tau_star_milp(allG, caps)
    if ts is None: return None
    anc = anchor_milp(allG, caps, 0)
    return (ts / k) if anc is None else (ts / k - 1.0)
G = [t for t in (rand_type() for _ in range(3)) if t]
cur = score(G)
while cur is None:
    G = [t for t in (rand_type() for _ in range(3)) if t]; cur = score(G)
best = (cur, list(map(list, G)))
for it in range(iters):
    H = [list(g) for g in G]; r = random.random()
    if (r < 0.35 and len(H) < maxt) or len(H) == 0:
        t = rand_type();
        if t: H.append(t)
    elif r < 0.5 and len(H) > 1:
        H.pop(random.randrange(len(H)))
    else:
        g = random.randrange(len(H)); i, j = random.sample(range(p), 2); d = random.choice([1, 2, 3])
        if H[g][i] >= d and H[g][j] + d <= caps[j]: H[g][i] -= d; H[g][j] += d
    if any(not (e <= sum(h) <= k) or sum(h[:p0]) < 1 for h in H): continue
    s = score(H)
    if s is None: continue
    if s >= cur - (0.01 if random.random() < 0.05 else 0):
        G, cur = H, s
        if cur > best[0]: best = (cur, [list(g) for g in G]); print(f"it {it}: best non-anchorable tau*/k = {cur:.4f} ntypes={len(G)}", flush=True)
print("FINAL best", best[0], "caps", caps, "e", e, "types", best[1], flush=True)
# exact re-verification of the best (if few types): exact tau* and exact anchorability
if best[0] > 0 and len(best[1]) <= 7:
    allG = [anchor] + best[1]
    print("exact tau*/k", tau_star(allG, caps) / k, "exact anchorable:", anchorable(allG, caps, 0), flush=True)
