"""Certificate for THEOREM L++ (robust heavy-neighbourhood lemma).
lam, delta >= 0.  N[E] = {F in H: |E&F| > lam};  B = {E in H : tau(N[E]) > delta};  beta = tau(B) (0 if B empty).
THEOREM L++: if H has (7,2) and t = tau(H), then NOT all of
   3 delta <= t-1,  2 delta + beta <= t-1,  2 lam + beta <= t-1,  2 lam + delta <= t-1,  3 lam <= t-1.
Recipe (TB = min transversal of B, T(E) = min transversal of N[E], |T(E)| <= delta for E notin B):
 G1 notin B (exists: else beta = t); G2 avoids T(G1) u TB; G3 avoids T(G1) u T(G2) u TB;
 G4 avoids T(G1) u T(G2) u T(G3);  G5 avoids I5 u TB;  G6 avoids I6 u T(G5);  G7 avoids I7 u (G5&G6).
Consequence (lam = delta = floor((t-1)/3)... or small): tau(B) >= t - 2 max(lam, delta) whenever 3lam,3delta,2lam+delta <= t-1."""
import itertools, random, sys
from w6_core_lemmaQ_cert import MATCH, has_2transversal, avoid
from w6_core_thmLplus_cert import min_transversal
def main(trials, seed=13):
    rnd = random.Random(seed); inst = 0; tuples = 0
    for _ in range(trials):
        n = rnd.randint(6, 10); V = list(range(n)); r = rnd.randint(2, 5)
        m = rnd.randint(6, 25)
        H = list(set(frozenset(rnd.sample(V, rnd.randint(max(1, r-1), r))) for _ in range(m)))
        t = len(min_transversal(H, V))
        for lam in range(0, 3):
            Tn = {E: min_transversal([F for F in H if len(E & F) > lam], V) for E in H}
            for delta in range(0, 4):
                B = [E for E in H if len(Tn[E]) > delta]
                TB = min_transversal(B, V) if B else set()
                beta = len(TB)
                if not (3*delta <= t-1 and 2*delta+beta <= t-1 and 2*lam+beta <= t-1 and 2*lam+delta <= t-1 and 3*lam <= t-1):
                    continue
                inst += 1
                good = [E for E in H if E not in B]; assert good
                for G1 in good[:5]:
                    G2 = avoid(H, Tn[G1] | TB); assert G2 not in B
                    G3 = avoid(H, Tn[G1] | Tn[G2] | TB); assert G3 not in B
                    G4 = avoid(H, Tn[G1] | Tn[G2] | Tn[G3])
                    G = [G1, G2, G3, G4]
                    assert all(len(G[a] & G[b]) <= lam for a in range(4) for b in range(a+1, 4))
                    I = [set().union(*[G[a] & G[b] for (a, b) in M]) for M in MATCH]
                    for order in itertools.permutations(range(3)):
                        I5, I6, I7 = I[order[0]], I[order[1]], I[order[2]]
                        G5 = avoid(H, I5 | TB); assert G5 not in B
                        G6 = avoid(H, I6 | Tn[G5]); assert len(G5 & G6) <= lam
                        G7 = avoid(H, I7 | (G5 & G6))
                        assert None not in (G2, G3, G4, G5, G6, G7)
                        assert not has_2transversal(G + [G5, G6, G7], V)
                        tuples += 1
    print(f"THEOREM L++ certificate PASS: {inst} (family,lam,delta) instances meeting hypotheses, {tuples} bad 7-tuples built")
if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1500)
