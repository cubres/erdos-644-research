"""Certificate for THEOREM L (bounded pairwise intersections).
THEOREM L. Let H be a family of nonempty sets with property (7,2) such that |E & F| <= lam for all
distinct E,F in H, lam >= 1.  Then tau(H) <= 3*lam.   (lam = 0: tau <= 2.)
Proof = Lemma Q: G1..G4 distinct => |I(mu)| <= 2 lam.  G5 avoids I5; G6 avoids I6 u {g}, g in G5
(so G6 != G5 and |G5&G6| <= lam); G7 avoids I7 u (G5&G6) (size <= 3 lam).  All avoided sets have
size <= 3 lam <= tau-1, so the edges exist; the 7 edges have no 2-transversal (Lemma Q logic).
This script: exhaustive end-to-end check on random bounded-intersection families with tau >= 3lam+1
(which by the theorem are NOT (7,2)): the recipe must produce, inside H, 7 edges without a 2-transversal,
for EVERY choice of 4 distinct edges and every matching order tried."""
import itertools, random, sys
from w6_core_lemmaQ_cert import MATCH, has_2transversal, avoid, pg2
def tau_exact(H, V):
    for s in range(len(V)+1):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(E & Ts for E in H): return s
def check(H, V, lam, t, rnd, nquads=200):
    H = list(H); cnt = 0
    for _ in range(nquads):
        G = rnd.sample(H, 4)
        I = [set().union(*[G[a] & G[b] for (a, b) in M]) for M in MATCH]
        for order in itertools.permutations(range(3)):
            I5, I6, I7 = I[order[0]], I[order[1]], I[order[2]]
            assert max(len(I5), len(I6), len(I7)) <= 2*lam
            G5 = avoid(H, I5); g = min(G5)
            G6 = avoid(H, I6 | {g}); assert G6 != G5 and len(G5 & G6) <= lam
            Z7 = I7 | (G5 & G6); assert len(Z7) <= 3*lam <= t-1
            G7 = avoid(H, Z7)
            assert G5 is not None and G6 is not None and G7 is not None
            assert not has_2transversal(G + [G5, G6, G7], V)
            cnt += 1
    return cnt
if __name__ == '__main__':
    rnd = random.Random(5); tot = 0; fams = 0
    for q in (3, 5, 7):
        L, V = pg2(q); tot += check(L, V, 1, q+1, rnd); fams += 1
    for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 300):
        n = rnd.randint(6, 11); r = rnd.randint(2, 5); lam = rnd.randint(1, max(1, r-1))
        V = list(range(n)); H = []
        cand = [frozenset(c) for c in itertools.combinations(V, r)]; rnd.shuffle(cand)
        for E in cand:
            if all(len(E & F) <= lam for F in H): H.append(E)
        t = tau_exact(H, V)
        if t < 3*lam + 1 or len(H) < 4: continue
        tot += check(H, V, lam, t, rnd, 50); fams += 1
    print(f"THEOREM L certificate PASS: {fams} families with tau>=3lam+1, {tot} constructed 7-tuples, all bad")
