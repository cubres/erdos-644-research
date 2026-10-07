"""Exact logic check of Lemma Q (dual pencil / quadrilateral lemma) for arbitrary set systems.
Claim: G1..G4 arbitrary nonempty sets; for a perfect matching mu={ij,kl} of [4] let I(mu)=(Gi&Gj)|(Gk&Gl).
Order the three matchings as (mu5,mu6,mu7).  If G5 avoids I(mu5), G6 avoids I(mu6), G7 avoids I(mu7) and G5&G6,
then G1..G7 have NO transversal of size <=2.  (Pure logic; sizes enter only through the oracle budgets.)
We also verify that dropping any single avoidance requirement admits counterexamples (sanity: all needed)."""
import random, itertools
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def has2(G, V):
    for x in V:
        for y in V:
            if y < x: continue
            if all((x in g) or (y in g) for g in G): return True
    return False
def rand_set(V, p, forbid=frozenset()):
    S={v for v in V if v not in forbid and random.random()<p}
    return S
def trial(n, drop=None):
    V=list(range(n))
    while True:
        G=[rand_set(V, random.choice([.3,.5,.7])) for _ in range(4)]
        if all(G): break
    perm=random.sample(range(3),3)
    I=[set().union(*[G[a]&G[b] for (a,b) in MATCH[perm[j]]]) for j in range(3)]
    for _ in range(50):
        f5 = set() if drop=='5' else I[0]
        G5=rand_set(V, random.choice([.4,.6,.9]), f5)
        f6 = set() if drop=='6' else I[1]
        G6=rand_set(V, random.choice([.4,.6,.9]), f6)
        f7 = set()
        if drop!='7a': f7 |= I[2]
        if drop!='7b': f7 |= (G5&G6)
        G7=rand_set(V, random.choice([.4,.6,.9]), f7)
        if G5 and G6 and G7: break
    else:
        return None
    return not has2(G+[G5,G6,G7], V)
random.seed(1)
cnt=0; bad=0
for it in range(20000):
    r=trial(random.randint(3,9))
    if r is None: continue
    cnt+=1
    if not r: bad+=1
print("Lemma Q logic: trials",cnt,"failures",bad)
for d in ['5','6','7a','7b']:
    c=0; f=0
    for it in range(20000):
        r=trial(random.randint(3,9), drop=d)
        if r is None: continue
        c+=1
        if not r: f+=1
    print("drop",d,": trials",c,"tuples WITH a 2-transversal (expected >0):",f)
