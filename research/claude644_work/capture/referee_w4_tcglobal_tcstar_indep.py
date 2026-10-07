# Independent referee check of TC* (two-step form): brute force, exact.
# For random hypergraphs and ALL configs (E0,b1,b2,c1,c2) meeting hypotheses, random split,
# if neither T_A nor T_B is a transversal, for EVERY g23 avoiding T_A and g14 avoiding T_B
# check that {E0,b1,b2,c1,c2,g23,g14} has no transversal of size <= 2.
import random, itertools, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
def has2(edges, V):
    for x in V:
        for y in V:
            if all((x in e) or (y in e) for e in edges): return True
    return False
checked=0; fires=0
for trial in range(400):
    n=random.randint(5,10); V=range(n)
    m=random.randint(4,12)
    H=[frozenset(random.sample(V,random.randint(1,n-1))) for _ in range(m)]
    H=list(set(H))
    for E0 in H:
      for b1,b2,c1,c2 in itertools.product(H,repeat=4):
        if b1&b2&E0 or c1&c2&E0: continue
        A=E0&((b1&c1)|(b2&c2)); B=E0&((b1&c2)|(b2&c1))
        assert not (A&B)
        free=list(E0-A-B)
        for _ in range(2):
            DA=set(A)|{x for x in free if random.random()<.5}; DB=set(E0)-DA
            TA=DA|(b1&c1)|(b2&c2); TB=DB|(b1&c2)|(b2&c1)
            gA=[g for g in H if not g&TA]; gB=[g for g in H if not g&TB]
            checked+=1
            if gA and gB:
                fires+=1
                for g23 in gA:
                    for g14 in gB:
                        tup=[E0,b1,b2,c1,c2,g23,g14]
                        if has2(tup,V):
                            print("FAIL",E0,b1,b2,c1,c2,g23,g14,DA); sys.exit(1)
print("configs",checked,"both-nontransversal cases",fires,"all bad tuples: OK")
