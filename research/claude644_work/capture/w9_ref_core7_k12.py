"""Referee core#7: Lemma T applicability scan in the (7,2) family K_12^(7) (tau=6; note 7.126 core with m=2)
and in K_9^(5) (tau=5), using bitmasks; exhaustive over G5,G6 for each sampled quad with |I5|,|I6|<=tau-1.
In a complete family G5 can be any k-set avoiding I5; Lemma T applicable iff some G5,G6 give |I7 | (G5&G6&UA)| <= n-k.
Min over G5,G6 of |G5&G6&UA \\ I7| computed exactly by enumeration.  Logic => never applicable."""
import itertools, random
pc=lambda x: bin(x).count('1')
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def scan(n,k,samples,seed=3):
    rnd=random.Random(seed); t=n-k+1
    E=[sum(1<<v for v in c) for c in itertools.combinations(range(n),k)]
    good=0; app=0; mins=[]
    for _ in range(samples):
        G=rnd.sample(E,4)
        if G[0]&G[1]&G[2]&G[3]: continue
        UA=G[0]|G[1]|G[2]|G[3]
        for order in itertools.permutations(range(3)):
            I=[]
            for j in range(3):
                (a,b),(c,d)=MATCH[order[j]]; I.append((G[a]&G[b])|(G[c]&G[d]))
            if pc(I[0])>t-1 or pc(I[1])>t-1 or pc(I[2])>t-1: continue
            good+=1
            c5=[e for e in E if not e&I[0]]; c6=[e for e in E if not e&I[1]]
            m=min(pc(I[2]|(g5&g6&UA)) for g5 in c5 for g6 in c6)
            mins.append(m)
            if m<=t-1: app+=1
    return t,good,app,(min(mins) if mins else None)
for n,k,s in [(9,5,20000),(12,7,200000)]:
    print(f"K_{n}^({k}):",scan(n,k,s))
