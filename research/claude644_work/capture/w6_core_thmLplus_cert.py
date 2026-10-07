"""Certificate for THEOREM L+ (heavy-neighbourhood version of Theorem L).
For lam >= 0 and an edge E put N[E] = {F in H : |E & F| > lam} (heavy closed neighbourhood) and
delta = max_E tau(N[E]).  THEOREM L+: if H has (7,2) and t = tau(H), then NOT
     ( 3*delta <= t-1  and  2*lam + delta <= t-1  and  3*lam <= t-1 ).
Recipe: T(E) = a minimum transversal of N[E].  G1 any edge; G2 avoids T(G1); G3 avoids T(G1)uT(G2);
G4 avoids T(G1)uT(G2)uT(G3)  (so G1..G4 pairwise light: |Gi&Gj| <= lam, |I(mu)| <= 2 lam);
G5 avoids I5; G6 avoids I6 u T(G5) (so |G5&G6| <= lam); G7 avoids I7 u (G5&G6).
Check: random families where the three inequalities hold; the 7 edges are built in H and verified bad."""
import itertools, random, sys
from w6_core_lemmaQ_cert import MATCH, has_2transversal, avoid
def min_transversal(H, V):
    for s in range(len(V)+1):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(E & Ts for E in H): return Ts
def main(trials, seed=11):
    rnd = random.Random(seed); fams = 0; tuples = 0
    for _ in range(trials):
        n = rnd.randint(6, 10); V = list(range(n)); r = rnd.randint(2, 5)
        m = rnd.randint(6, 25)
        H = list(set(frozenset(rnd.sample(V, rnd.randint(max(1, r-1), r))) for _ in range(m)))
        t = len(min_transversal(H, V))
        for lam in range(0, 3):
            if 3*lam > t-1: continue
            Tn = {E: min_transversal([F for F in H if len(E & F) > lam], V) for E in H}
            delta = max(len(T) for T in Tn.values())
            if not (3*delta <= t-1 and 2*lam + delta <= t-1): continue
            fams += 1
            for G1 in H:
                G2 = avoid(H, Tn[G1]); G3 = avoid(H, Tn[G1] | Tn[G2]); G4 = avoid(H, Tn[G1] | Tn[G2] | Tn[G3])
                G = [G1, G2, G3, G4]
                assert all(len(G[a] & G[b]) <= lam for a in range(4) for b in range(a+1, 4))
                I = [set().union(*[G[a] & G[b] for (a, b) in M]) for M in MATCH]
                for order in itertools.permutations(range(3)):
                    I5, I6, I7 = I[order[0]], I[order[1]], I[order[2]]
                    G5 = avoid(H, I5); G6 = avoid(H, I6 | Tn[G5])
                    assert len(G5 & G6) <= lam
                    G7 = avoid(H, I7 | (G5 & G6))
                    assert None not in (G5, G6, G7)
                    assert not has_2transversal(G + [G5, G6, G7], V)
                    tuples += 1
    print(f"THEOREM L+ certificate PASS: {fams} (family,lam) instances meeting the hypotheses, {tuples} bad 7-tuples built")
if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
