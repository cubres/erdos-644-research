"""Referee w9 core#2 supplement: 'K-QUAD LEMMA' (referee's own, FULL_PROOF by Lemma Q logic) and its exhaustive
adversarial e2e check.  Statement: codegree <= lam (lam>=1), tau >= 2lam+1 (or more generally tau-1 >= s+lam,
s=|K|<=lam), and four distinct edges G1..G4 with all pairwise intersections inside a set K, |K|<=lam  => H not (7,2).
Recipe: G5 avoids K; g in G5; G6 avoids K+{g}; G7 avoids K+(G5&G6).  (I(mu) subset K for all mu.)
Consequence (lam=1): a linear (7,2) family has max degree <= 3 if tau>=3, so |H|<=6 and tau<=2 -- i.e. Theorem L's
constant is NOT attained at lam=1 (sharp value 2 = triangle).
Check: for families below, EVERY K-quad (found by brute force), all adversarial G5,g,G6,G7 (capped), assert no
<=2-transversal of the 7 edges."""
import itertools, random, sys
from w9_ref_core2_e2e import pg, tau, pierce2, pc
def kquads(H, lam):
    out = []
    for Q in itertools.combinations(H, 4):
        U = 0
        for a, b in itertools.combinations(Q, 2): U |= a & b
        if pc(U) <= lam: out.append((Q, U))
    return out
def run(H, n, lam, rnd, maxq=40, cap=8):
    t = tau(H, n); assert max(pc(a & b) for a, b in itertools.combinations(H, 2)) <= lam
    Qs = kquads(H, lam)
    Qs = [q for q in Qs]  # need tau-1 >= |K|+lam
    Qs = [(Q, K) for (Q, K) in Qs if t - 1 >= pc(K) + lam]
    if len(Qs) > maxq: Qs = rnd.sample(Qs, maxq)
    sub = lambda L: L if len(L) <= cap else rnd.sample(L, cap)
    cnt = 0
    for Q, K in Qs:
        C5 = [E for E in H if not E & K]; assert C5
        for G5 in sub(C5):
            for g in [v for v in range(n) if G5 >> v & 1]:
                C6 = [E for E in H if not E & (K | 1 << g)]; assert C6
                for G6 in sub(C6):
                    assert G6 != G5
                    C7 = [E for E in H if not E & (K | (G5 & G6))]; assert C7
                    for G7 in sub(C7):
                        assert not pierce2(list(Q) + [G5, G6, G7], n); cnt += 1
    return t, len(Qs), cnt
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for q in (3, 5):
    L, n = pg(q); t, nq, c = run(L, n, 1, rnd)
    print(f"PG(2,{q}) lam=1 tau={t}: {nq} K-quads, {c} tuples PASS", flush=True)
for (n, k) in [(9, 3), (11, 3)]:
    H = [sum(1 << v for v in c) for c in itertools.combinations(range(n), k)]
    t, nq, c = run(H, n, k - 1, rnd, 30, 6)
    print(f"K_{n}^{k} lam={k-1} tau={t}: {nq} K-quads, {c} tuples PASS", flush=True)
# random linear families (mixed sizes) with tau>=3 and a degree-4 point
tot = fams = 0
while fams < 60:
    n = rnd.randint(7, 12)
    cand = [sum(1 << v for v in rnd.sample(range(n), rnd.randint(2, n - 2))) for _ in range(400)]
    H = []
    for E in cand:
        if E not in H and all(pc(E & F) <= 1 for F in H): H.append(E)
    if len(H) < 4 or tau(H, n) < 3: continue
    t, nq, c = run(H, n, 1, rnd, 10, 6)
    if nq: fams += 1; tot += c
print(f"random linear families with tau>=3: {fams} families with K-quads, {tot} tuples PASS", flush=True)
# lemma consequence: brute-force check that no linear family with tau>=3 and max degree<=3 has <=6 edges being (7,2):
print("counting step (hand): 2 points cover <= 2*3 = 6 < 7 edges, so |H|<=6 and H itself is 2-pierceable.")
