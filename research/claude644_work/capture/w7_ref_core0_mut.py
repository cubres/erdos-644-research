"""Referee w7 core#0: mutation tests.  (M1) relax sum condition to 2t-k-1: does the recipe break (some oracle branch
with no G7, or a 2-coverable 7-tuple)?  (M2) drop Y (G6 avoids only I6): same question under the TRUE hypotheses.
(M3) drop G7's avoidance of G5&G6 (G7 avoids only I7): are 2-coverable 7-tuples produced?"""
import itertools, random, sys
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def tau(H,V):
    for s in range(len(V)+1):
        for T in itertools.combinations(V,s):
            if all(E&set(T) for E in H): return s
def two_trans(G,V): return any(all((x in g) or (y in g) for g in G) for x in V for y in V if y>=x)
rnd=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 7)
cnt={'M1_noG7':0,'M1_cov':0,'M1_inst':0,'M2_noG7':0,'M2_cov':0,'M2_inst':0,'M3_cov':0,'M3_inst':0}
ex={}
for _ in range(1500):
    n=rnd.randint(4,9); V=list(range(n)); kk=rnd.randint(1,n-1)
    H=list({frozenset(rnd.sample(V,rnd.randint(1,kk))) for _ in range(rnd.randint(3,12))})
    t=tau(H,V); k=max(len(E) for E in H)
    for quad in itertools.product(range(len(H)),repeat=4):
        if rnd.random()>0.3: continue
        G=[H[i] for i in quad]; I=[set().union(*[G[a]&G[b] for a,b in M]) for M in MATCH]
        for o in itertools.permutations(range(3)):
            I5,I6,I7=(I[x] for x in o)
            base=len(I5)<=t-1 and len(I6)<=t-1 and len(I7)<=t-1
            if not base: continue
            s=len(I6)+len(I7)
            for mode in ('M1','M2','M3'):
                if mode=='M1' and s!=2*t-k-1: continue
                if mode in('M2','M3') and s>2*t-k-2: continue
                cnt[mode+'_inst']+=1
                for G5 in [E for E in H if not E&I5]:
                    pool=list(G5-I6)
                    Y=set() if mode=='M2' else set(rnd.sample(pool,min(len(pool),t-1-len(I6))))
                    for G6 in [E for E in H if not E&(I6|Y)]:
                        req7=I7 if mode=='M3' else I7|(G5&G6)
                        G7s=[E for E in H if not E&req7]
                        if not G7s:
                            cnt[mode+'_noG7']+=1; ex.setdefault(mode+'_noG7',(sorted(map(sorted,H)),quad,o,t,k)); continue
                        for G7 in G7s:
                            if two_trans(G+[G5,G6,G7],V):
                                cnt[mode+'_cov']+=1; ex.setdefault(mode+'_cov',(sorted(map(sorted,H)),quad,o,t,k))
print(cnt)
for key,v in ex.items(): print(key,v)
