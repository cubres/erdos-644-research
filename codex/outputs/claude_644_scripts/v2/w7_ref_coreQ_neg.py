# Negative controls: (a) with triple cells present, requesting only I(mu) (ignoring low vertices) can fail;
# (b) compare Lemma Q (rank-lazy) vs referee's QZ (capacity) condition coverage.
import random, itertools, sys
from w7_ref_coreQ_e2e import MATCH,popc,tau,two_pierceable,A,Iset
stats=dict(naive_try=0,naive_fail=0,Q_only=0,QZ_only=0,both=0)
def run(seed):
    rng=random.Random(10**6+seed)
    n=rng.randint(8,12); k=rng.randint(3,6); m=rng.randint(6,30)
    edges=list({sum(1<<v for v in rng.sample(range(n),rng.randint(max(1,k-2),k))) for _ in range(m)})
    t=tau(edges,n)
    if 2*t-k-2<0: return
    for _ in range(1500):
        G=tuple(rng.choice(edges) for _ in range(4))
        I=[Iset(G,mu) for mu in MATCH]
        T=0
        for (a,b,c) in itertools.combinations(range(4),3): T|=G[a]&G[b]&G[c]
        if T and all(popc(x)<=t-1 for x in I):
            # adversarial oracle choice: try all oracle triples, look for a 2-pierceable one
            c=[[e for e in edges if not e&x] for x in I]
            stats['naive_try']+=1
            if any(not two_pierceable(list(G)+[a,b,d],n) is False for a in c[0][:6] for b in c[1][:6] for d in c[2][:6]):
                stats['naive_fail']+=1
        # coverage comparison
        Q=False
        for o5 in range(3):
            o6,o7=[x for x in range(3) if x!=o5]
            if popc(I[o5])<=t-1 and popc(I[o6])<=t-1 and popc(I[o7])<=t-1 and popc(I[o6])+popc(I[o7])<=2*t-k-2: Q=True
        Zs=0
        for x in range(n):
            if T>>x&1:
                for y in range(n):
                    if len(A(y,G))<=1 and (A(x,G)|A(y,G))==frozenset(range(4)): Zs|=1<<y
        cap=[t-1-popc(x) for x in I]
        QZ=min(cap)>=0 and popc(Zs)<=sum(cap)
        if Q and QZ: stats['both']+=1
        elif Q: stats['Q_only']+=1
        elif QZ: stats['QZ_only']+=1
for s in range(int(sys.argv[1])): run(s)
print(stats)
