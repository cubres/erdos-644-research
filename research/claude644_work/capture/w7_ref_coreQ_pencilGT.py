# Pointwise pencil closure <=> good triple with admissible labelling. Check: every cell vector
# (n1,n2,n3,n12,n13,n23) with union <= 2t-3 is admissible (GT*), and list failures at union = 2t-2.
# Exact: integer program solved by exhaustive search over class splits (small t).
import itertools
from functools import lru_cache
PTS=['a','A','b','B','c','C']   # A=a', etc.
ML=[('a','b','c'),('A','B','c'),('A','b','C'),('a','B','C')]
OPT={'1':'bBcC','2':'aAcC','3':'aAbB','12':'cC','13':'bB','23':'aA'}
def admissible(cells,t):
    # cells: dict type->size ; search load vectors
    types=list(cells)
    def splits(n,opts):
        # all ways to distribute n among opts
        if len(opts)==1: yield {opts[0]:n}; return
        for x in range(n+1):
            for r in splits(n-x,opts[1:]):
                d=dict(r); d[opts[0]]=d.get(opts[0],0)+x; yield d
    def rec(i,load):
        if i==len(types):
            return all(sum(load[p] for p in L)<=t-1 for L in ML)
        for d in splits(cells[types[i]],list(OPT[types[i]])):
            nl=dict(load)
            for p,x in d.items(): nl[p]+=x
            if all(sum(nl[p] for p in L)<=t-1 for L in ML) and rec(i+1,nl): return True
        return False
    return rec(0,{p:0 for p in PTS})
for t in range(2,7):
    bad_le=0; bad_eq=[]
    for tot in (2*t-3,2*t-2):
        for c in itertools.product(range(tot+1),repeat=6):
            if sum(c)!=tot: continue
            cells=dict(zip(['1','2','3','12','13','23'],c))
            if not admissible(cells,t):
                if tot==2*t-3: bad_le+=1
                else: bad_eq.append(c)
    print('t',t,'inadmissible at union 2t-3:',bad_le,'| at 2t-2:',len(bad_eq), bad_eq[:6])
