# exact test: does domain (list of cons in (x,y,al,be)) lie in union of template regions F_t, t in S?
import itertools
from lib2 import *
def tfacets(k):
    out=[]
    for u,v in FUNCS[k-1]:
        out.append(([1,0,-u,-v],0)); out.append(([0,1,u,v],-(u+v)))
    return out
def maxeps(cons, viol):
    # variables (x,y,al,be,eps); cons >=0 ; viol f<=-eps i.e. -f - eps >= 0 ; eps<=1
    C=[(c+[0],k) for c,k in cons]+[([-a for a in f]+[-1],-k) for f,k in viol]+[([0,0,0,0,-1],1)]
    V=vertices(C,5)
    if not V: return None
    return max(v[4] for v in V)
def covered(cons, S, verbose=False):
    fac=[tfacets(k) for k in S]
    bad=[]
    for combo in itertools.product(*[range(len(f)) for f in fac]):
        viol=[fac[i][j] for i,j in enumerate(combo)]
        m=maxeps(cons,viol)
        if m is not None and m>0:
            bad.append((combo,m))
            if not verbose: return False,bad
    return len(bad)==0,bad
