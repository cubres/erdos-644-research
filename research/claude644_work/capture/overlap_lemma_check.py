#!/usr/bin/env python3
"""
Randomized test of the constructive procedure behind "Lemma A_omega" (overlap form):

  H any family, U a vertex set with a Fano partition U = V_0 u ... u V_6 (points of PG(2,2)),
  lines l_1..l_7 ordered with l_1,l_2,l_3 non-concurrent.  For j=1..7 request an edge
  G_j of H avoiding
      A_j = L_{l_j}  u  F_j  u  {y_i : i<j}
  where L_l = union of V_p (p in l), y_i is a chosen point of G_i (forces distinct edges),
  and F_j = { x not in U : sigma_{<j}(x) u {l_j} covers all 7 Fano points },
  sigma_{<j}(x) = lines l_i (i<j) with x in G_i.
Claim tested: whenever all seven requests are answered, G_1..G_7 have NO transversal of
size <= 2.  (The lemma then follows: |F_j| <= sum_{i<i'<j} |(G_i cap G_i') \ U| <= 15 omega,
so |A_j| <= |U|-4floor(|U|/7) + 15 omega + 6 < tau(H) makes every request answerable.)
Also records that |F_j| never exceeds the number of outside points lying in >= 2 earlier
responses (the counting step).
Run: python3 -B overlap_lemma_check.py
"""
import random, itertools

LINES = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]

def covers_all(lines):
    u = set()
    for l in lines:
        u |= l
    return len(u) == 7

def order_lines():
    # l1,l2,l3 non-concurrent
    for perm in itertools.permutations(range(7)):
        a, b, c = (LINES[perm[0]], LINES[perm[1]], LINES[perm[2]])
        if not (a & b & c):
            return [LINES[i] for i in perm]

ORDER = order_lines()

def two_pierceable(edges):
    verts = sorted(set().union(*edges))
    for a in range(len(verts)):
        for b in range(a, len(verts)):
            x, y = verts[a], verts[b]
            if all(x in E or y in E for E in edges):
                return True
    return False

def run_once(rng):
    nv = rng.randint(12, 26)
    V = list(range(nv))
    usize = rng.randint(7, min(14, nv - 1))
    U = rng.sample(V, usize)
    outside = [v for v in V if v not in U]
    # Fano partition of U (balanced)
    lab = {}
    for idx, x in enumerate(U):
        lab[x] = idx % 7
    # random family: many random edges of random sizes
    H = []
    for _ in range(rng.randint(40, 400)):
        sz = rng.randint(2, max(2, nv // 2))
        H.append(frozenset(rng.sample(V, sz)))
    H = list(set(H))
    G = []
    Fsizes = []
    for j, lj in enumerate(ORDER):
        sig = {x: [ORDER[i] for i in range(j) if x in G[i]] for x in outside}
        F = {x for x in outside if covers_all(sig[x] + [lj])}
        multi = {x for x in outside if len(sig[x]) >= 2}
        assert F <= multi
        Fsizes.append(len(F))
        L = {x for x in U if lab[x] in lj}
        Y = set(next(iter(sorted(Gi))) for Gi in G)
        A = L | F | Y
        cands = [E for E in H if not (E & A)]
        if not cands:
            return "stuck", None
        G.append(rng.choice(cands))
    assert len(set(G)) == 7
    bad = not two_pierceable(G)
    return ("completed_bad" if bad else "COMPLETED_BUT_PIERCEABLE"), Fsizes

if __name__ == "__main__":
    rng = random.Random(9230)
    stats = {}
    maxF = 0
    for t in range(4000):
        res, Fs = run_once(rng)
        stats[res] = stats.get(res, 0) + 1
        if Fs:
            maxF = max(maxF, max(Fs))
    print(stats, "max |F_j| seen:", maxF)
    assert stats.get("COMPLETED_BUT_PIERCEABLE", 0) == 0
    print("PASS: every completed run produced 7 distinct edges with no 2-transversal")
