"""Referee w7 core#0: adversarial end-to-end test of Lemma Q (corrected statement).
Differences from attacker's cert: t ranges over ALL 1..tau (hypothesis is only 'every <=t-1 set avoided'),
k ranges over max|E|..max|E|+2 (rank <= k, not = k), oracle responses are EVERY edge avoiding the request
(exhaustive over G5,G6,G7 choices), Y is a random admissible subset.  Every resulting 7-tuple must have
no 2-transversal.  Also counts instances where hypotheses hold (for coverage) and checks the arithmetic
bound |G5&G6| <= max(0,k-t+1+|I6|) and |I7 u (G5&G6)| <= t-1 on every branch."""
import itertools, random, sys
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def tau(H,V):
    for s in range(len(V)+1):
        for T in itertools.combinations(V,s):
            Ts=set(T)
            if all(E&Ts for E in H): return s
def two_trans(G,V):
    return any(all((x in g) or (y in g) for g in G) for x in V for y in V if y>=x)
def main(trials,seed):
    rnd=random.Random(seed); hits=0; branches=0; fams=0
    for _ in range(trials):
        n=rnd.randint(4,9); V=list(range(n))
        kk=rnd.randint(1,n-1)
        H=list({frozenset(rnd.sample(V,rnd.randint(1,kk))) for _ in range(rnd.randint(3,12))})
        T0=tau(H,V); mk=max(len(E) for E in H); fams+=1
        for t in range(1,T0+1):
          for k in range(mk,mk+3):
            for quad in itertools.product(range(len(H)),repeat=4):
                if rnd.random()>0.2: continue
                G=[H[i] for i in quad]
                I=[set().union(*[G[a]&G[b] for a,b in M]) for M in MATCH]
                for order in itertools.permutations(range(3)):
                    I5,I6,I7=(I[o] for o in order)
                    if not(len(I5)<=t-1 and len(I6)<=t-1 and len(I7)<=t-1 and len(I6)+len(I7)<=2*t-k-2): continue
                    hits+=1
                    for G5 in [E for E in H if not E&I5]:
                        pool=list(G5-I6); m=min(len(pool),t-1-len(I6))
                        Y=set(rnd.sample(pool,m))
                        req6=I6|Y; assert len(req6)<=t-1
                        for G6 in [E for E in H if not E&req6]:
                            assert len(G5&G6)<=max(0,k-t+1+len(I6))
                            req7=I7|(G5&G6); assert len(req7)<=t-1
                            G7s=[E for E in H if not E&req7]; assert G7s
                            for G7 in G7s:
                                branches+=1
                                assert not two_trans(G+[G5,G6,G7],V),(H,quad,order,t,k)
    print(f"seed {seed}: {fams} families, {hits} hypothesis instances, {branches} oracle branches, 0 failures")
if __name__=='__main__':
    main(int(sys.argv[1]),int(sys.argv[2]))
