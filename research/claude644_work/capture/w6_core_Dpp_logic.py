r"""Logic check of Lemma D'' (anchored pencil, protruding anchor F and protruding host edges G2,G3).
Random instances: U, F (arbitrary, may protrude), labels on U as in the proof, G2,G3 arbitrary sets whose U-part
avoids the required classes (outside parts arbitrary), G3 also avoids (F&G2)\U; M1..M4 arbitrary sets avoiding
their classes and the lazy forbidden sets
  Forb2=(G3\U)&M1, Forb3=((G2\U)&M1)|((F\U)&M2), Forb4=((F\U)&M1)|((G2\U)&M2)|((G3\U)&M3).
Claim: the 7 sets F,G2,G3,M1..M4 have no transversal of size <= 2.  Also: dropping any one lazy rule fails."""
import random
def has2(G,V):
    for x in V:
        for y in V:
            if y<x: continue
            if all((x in g) or (y in g) for g in G): return True
    return False
def rs(pool,p,forbid=set()):
    return {v for v in pool if v not in forbid and random.random()<p}
def trial(drop=None):
    nU=random.randint(4,9); nO=random.randint(1,5)
    U=list(range(nU)); O=list(range(nU,nU+nO)); V=U+O
    lab={v:random.choice(['p0','a','ap','b','bp','c','cp']) for v in U}
    F={v for v in U if lab[v] in ('b','bp','c','cp') and random.random()<.8} | rs(O,.5)
    if not F: return None
    cls=lambda names:{v for v in U if lab[v] in names}
    G2=rs(U,.8,cls(('p0','b','bp')))|rs(O,.5)
    f3=cls(('p0','c','cp'))
    if drop!='G3': f3|=((F&G2)-set(U))
    G3=rs(U,.8,f3)|rs(O,.5,f3)
    Ou=set(O)
    M1=rs(V,.6,cls(('a','b','c')))
    f2=cls(('ap','bp','c'))
    if drop!='2': f2|=(G3&Ou)&M1
    M2=rs(V,.6,f2)
    f3m=cls(('ap','b','cp'))
    if drop!='3a': f3m|=(G2&Ou)&M1
    if drop!='3b': f3m|=(F&Ou)&M2
    M3=rs(V,.6,f3m)
    f4=cls(('a','bp','cp'))
    if drop!='4a': f4|=(F&Ou)&M1
    if drop!='4b': f4|=(G2&Ou)&M2
    if drop!='4c': f4|=(G3&Ou)&M3
    M4=rs(V,.6,f4)
    T=[F,G2,G3,M1,M2,M3,M4]
    if not all(T): return None
    return not has2(T,V)
random.seed(7)
for d in [None,'G3','2','3a','3b','4a','4b','4c']:
    c=f=0
    for _ in range(30000):
        r=trial(d)
        if r is None: continue
        c+=1
        if not r: f+=1
    print("drop",d,"trials",c,"tuples with a 2-transversal:",f)
