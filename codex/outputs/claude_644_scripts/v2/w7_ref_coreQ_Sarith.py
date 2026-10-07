# Corollary arithmetic: if S=sum_{i<j}|Gi n Gj| <= min(t,floor(3(2t-k-2)/2)+1)-1 then Lemma Q's condition holds
# for mu5 = argmax |I(mu)|; checked on random 4-tuples of random families (exact ints), then the tuple is built.
import random, itertools
from w7_ref_coreQ_e2e import MATCH,popc,tau,two_pierceable,A,Iset
hits=0; bad=0
for seed in range(400):
    rng=random.Random(777+seed); n=rng.randint(8,12); k=rng.randint(3,7)
    edges=list({sum(1<<v for v in rng.sample(range(n),rng.randint(1,k))) for _ in range(rng.randint(6,40))})
    t=tau(edges,n)
    if 2*t-k-2<0: continue
    m=min(t,(3*(2*t-k-2))//2+1)
    for _ in range(2000):
        G=tuple(rng.choice(edges) for _ in range(4))
        S=sum(popc(G[i]&G[j]) for i,j in itertools.combinations(range(4),2))
        if S<=m-1:
            I=sorted(popc(Iset(G,mu)) for mu in MATCH)
            hits+=1
            if not (I[2]<=t-1 and I[1]<=t-1 and I[0]+I[1]<=2*t-k-2): bad+=1; print('ARITH FAIL',S,I,t,k)
print('S<m tuples',hits,'arith failures',bad)
