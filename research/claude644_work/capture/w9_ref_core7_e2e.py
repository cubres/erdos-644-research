"""Referee core#7 end-to-end: random families H (n<=11), t=tau(H) exact.  For quads G1..G4 in H with empty common
intersection and each matching order, pick G5 in H avoiding I5, G6 in H avoiding I6, G7 in H avoiding
I7 | (G5&G6&U_A) (all found edges of H).  Check brute-force that G1..G7 have no 2-transversal.  Also count cases where
Lemma Q's stronger requirement (G7 avoids I7 | (G5&G6)) has NO solution G7 in H but Lemma T's does (strictness)."""
import itertools, random
pc=lambda x: bin(x).count('1')
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def tau(E,n):
    for s in range(n+1):
        for S in itertools.combinations(range(n),s):
            m=sum(1<<v for v in S)
            if all(e&m for e in E): return s
def two_pierce(G,n):
    for x in range(n):
        for y in range(x,n):
            m=(1<<x)|(1<<y)
            if all(g&m for g in G): return True
    return False
rnd=random.Random(11); inst=0; tuples=0; strict=0
for trial in range(400):
    n=rnd.randint(7,11); k=rnd.randint(2,min(6,n-1)); m=rnd.randint(8,45)
    E=list({sum(1<<v for v in rnd.sample(range(n),rnd.randint(max(1,k-2),k))) for _ in range(m)})
    t=tau(E,n); inst+=1
    for _ in range(60):
        G=[rnd.choice(E) for _ in range(4)]
        if G[0]&G[1]&G[2]&G[3]: continue
        UA=G[0]|G[1]|G[2]|G[3]
        for order in itertools.permutations(range(3)):
            I=[]
            for j in range(3):
                (a,b),(c,d)=MATCH[order[j]]; I.append((G[a]&G[b])|(G[c]&G[d]))
            c5=[e for e in E if not e&I[0]]; c6=[e for e in E if not e&I[1]]
            if not c5 or not c6: continue
            g5=rnd.choice(c5); g6=rnd.choice(c6)
            c7=[e for e in E if not e&(I[2]|(g5&g6&UA))]
            if not c7: continue
            g7=rnd.choice(c7)
            assert not two_pierce(G+[g5,g6,g7],n)
            tuples+=1
            if not [e for e in E if not e&(I[2]|(g5&g6))]: strict+=1
print(f"PASS: {inst} random families, {tuples} Lemma-T 7-tuples built from actual edges, none 2-pierceable;"
      f" {strict} of them had no Lemma-Q completion (G7 avoiding I7|(G5&G6)) in H")
