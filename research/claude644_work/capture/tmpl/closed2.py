# Template tree search for arbitrary closed two-part type sets (note Thm 7.75), vars z=(x,y,l,a,b,c)
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
from lib2 import FUNCS
X,Y,L,A,B,C=range(6); NV=6
def lin(d,const=0):
    v=[0.0]*NV
    for k,c in d.items(): v[k]=float(c)
    return (v,float(const))
Q=0.75
def domain(case):
    l0,c1=case  # l0: l==0 ; c1: c==1
    W=[]  # weak  g>=0
    S=[]  # strict g>0
    W+= [lin({L:1}), lin({A:1,L:-1}), lin({B:1,A:-1}), lin({C:1,B:-1}), lin({C:-1},1),
         lin({X:1,C:-1}), lin({Y:1,L:1},-1)]
    if l0: W+=[lin({L:-1})]
    else: W+=[lin({X:1,L:-1},-Q)]         # x-l>=3/4
    if c1: W+=[lin({C:1},-1)]
    else: W+=[lin({Y:1,C:1},-1-Q)]        # y-1+c>=3/4
    W+=[lin({X:1,Y:1,A:1,B:-1},-1-Q)]     # gap: N-1-(b-a)>=3/4
    # Lemma 7.74 consequences (strict): a<1-4y/7, b>4x/7, b-a<delta, c-l<2delta, delta=N-7/4
    S+=[lin({A:-7,Y:-4},7), lin({B:7,X:-4}), lin({X:1,Y:1,B:-1,A:1},-1.75), lin({X:2,Y:2,C:-1,L:1},-3.5)]
    return W,S
TYPES=[L,A,B,C]
def cand_facets(k,s,t):
    # template k with a-rows type s, b-rows type t ; facets as g>=0
    out=[]
    for u,v in FUNCS[k-1]:
        u=float(u); v=float(v)
        out.append(lin({X:1, s:-u} if s==t else {X:1,s:-u,t:-v}) if s!=t else lin({X:1,s:-(u+v)}))
        # part2: u(1-s)+v(1-t)<=y  -> y + u s + v t - (u+v) >=0
        out.append(lin({Y:1,s:u,t:v},-(u+v)) if s!=t else lin({Y:1,s:u+v},-(u+v)))
    return out
def maxeps(W,S,viol):
    Aub=[];bub=[]
    for g,k in W: Aub.append([-x for x in g]+[0.0]); bub.append(k)
    for g,k in S: Aub.append([-x for x in g]+[1.0]); bub.append(k)
    for g,k in viol: Aub.append(list(g)+[1.0]); bub.append(-k)
    r=linprog([0.0]*NV+[-1.0],A_ub=Aub,b_ub=bub,bounds=[(None,None)]*NV+[(None,1.0)],method='highs')
    if r.status==2: return None
    if r.status!=0: return 1.0
    return -r.fun
POOL=[int(a) for a in sys.argv[2].split(',')] if len(sys.argv)>2 else [19,20,1,2,39,40,9,10,21,22,41,42,3,4,5,6]
CANDS=[(k,s,t) for k in POOL for s in TYPES for t in TYPES if not (s==t and k not in (19,20))]
leaves=0
def rec(W,S,viol,depth,path):
    global leaves
    m=maxeps(W,S,viol)
    if m is None or m<=1e-9: leaves+=1; return True
    if depth>12: print('DEPTH',path); return False
    best=None
    for cand in CANDS:
        if cand in [p[0] for p in path]: continue
        fac=cand_facets(*cand)
        fail=[f for f in fac if (lambda mm: mm is not None and mm>1e-9)(maxeps(W,S,viol+[f]))]
        if best is None or len(fail)<len(best[1]): best=(cand,fail)
        if len(fail)<=1: break
    cand,fail=best
    ok=True
    for j,f in enumerate(fail):
        ok&=rec(W,S,viol+[f],depth+1,path+[(cand,j)])
    return ok
for case in [(True,False),(False,False),(True,True)] if sys.argv[1]=='all' else [tuple(bool(int(c)) for c in sys.argv[1])]:
    W,S=domain(case); leaves=0
    ok=rec(W,S,[],0,[])
    print('case l0,c1=',case,'OK' if ok else 'FAIL','leaves',leaves,flush=True)
