# PG(2,q) (q prime) : Q' (no triple cell, max |I(mu)|<=t-1) exhibits a bad 7-tuple of lines for q=2,3,5,7.
import itertools
from w7_ref_coreQ_e2e import MATCH,popc,two_pierceable,Iset
def pg(q):
    pts=[]; 
    for v in itertools.product(range(q),repeat=3):
        if any(v):
            f=next(x for x in v if x); inv=pow(f,q-2,q)
            w=tuple(x*inv%q for x in v)
            if w not in pts: pts.append(w)
    idx={p:i for i,p in enumerate(pts)}
    lines=[sum(1<<idx[p] for p in pts if sum(a*b for a,b in zip(L,p))%q==0) for L in pts]
    return len(pts),lines
for q in (2,3,5,7):
    n,L=pg(q); t=q+1  # tau of PG(2,q) lines
    for G in itertools.combinations(L,4):
        if any(a&b&c for a,b,c in itertools.combinations(G,3)): continue
        I=[Iset(G,mu) for mu in MATCH]
        assert all(popc(x)<=t-1 for x in I)
        O=[next(l for l in L if not l&x) for x in I]
        print('q',q,'k=t=',t,'|I|',[popc(x) for x in I],'7-tuple 2-pierceable?',two_pierceable(list(G)+O,n)); break
