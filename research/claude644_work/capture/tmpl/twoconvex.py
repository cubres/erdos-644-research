# two sliced boxes over p parts: do pairs + small template set suffice?
import random, itertools, sys
import numpy as np
from scipy.optimize import linprog
from lib2 import FUNCS
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
p=int(sys.argv[1]) if len(sys.argv)>1 else 3
SMALL={'Ha':[(1.75,0)],'Hb':[(0,1.75)],'Qb':[(0,1.5),(1,0.75)],'Qa':[(1.5,0),(0.75,1)],
       'V':[(1,1),(1.25,0.5)],"V'":[(1,1),(0.5,1.25)]}
ALL={f'f{k+1}':[(float(u),float(v)) for u,v in f] for k,f in enumerate(FUNCS)}
def tighten(l,h):
    l=list(l);h=list(h)
    for _ in range(3):
        for i in range(p):
            l[i]=max(l[i],1-sum(h[j] for j in range(p) if j!=i))
            h[i]=min(h[i],1-sum(l[j] for j in range(p) if j!=i))
    return l,h
def blockers(x,l,h):
    B=[]
    for i in range(p):
        if l[i]>1e-12: B.append(({i},x[i]-l[i]))
    for r in range(1,p+1):
        for S in itertools.combinations(range(p),r):
            bb=1-sum(h[i] for i in range(p) if i not in S)
            if bb>1e-12: B.append((set(S),sum(x[i] for i in S)-bb))
    return B
def tau(x,boxes):
    B1=blockers(x,*boxes[0]); B2=blockers(x,*boxes[1]); best=9
    for S,al in B1:
        for T,be in B2:
            best=min(best,max(al,be,al+be-sum(x[i] for i in S&T)))
    return best
def pair_feasible(x,boxA,boxB,facets):
    # variables s (p), t (p): s in boxA, t in boxB, facets u s_i + v t_i <= x_i
    lA,hA=boxA; lB,hB=boxB
    A=[];b=[]
    for i in range(p):
        for u,v in facets:
            row=[0.0]*(2*p); row[i]=u; row[p+i]=v; A.append(row); b.append(x[i])
    Aeq=[[1.0]*p+[0.0]*p,[0.0]*p+[1.0]*p]; beq=[1,1]
    bounds=[(lA[i],hA[i]) for i in range(p)]+[(lB[i],hB[i]) for i in range(p)]
    r=linprog([0]*(2*p),A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
    return r.status==0
stats={'n':0,'small':0,'all':0,'none':0}
for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 2000):
    x=[random.uniform(0.3,1.6) for _ in range(p)]
    boxes=[]
    for j in range(2):
        l=[random.choice([0,random.uniform(0,0.8)]) for _ in range(p)]
        h=[min(x[i],l[i]+random.uniform(0,1)) for i in range(p)]
        l,h=tighten(l,h)
        if any(l[i]>h[i]+1e-12 for i in range(p)) or sum(l)>1 or sum(h)<1: break
        boxes.append((l,h))
    if len(boxes)<2: continue
    if sum(x)<=1.75: continue
    t=tau(x,boxes)
    if t<=0.75: continue
    stats['n']+=1
    comps=[(boxes[0],boxes[1]),(boxes[1],boxes[0]),(boxes[0],boxes[0]),(boxes[1],boxes[1])]
    ok=any(pair_feasible(x,A_,B_,f) for A_,B_ in comps for f in SMALL.values())
    if ok: stats['small']+=1; continue
    ok2=any(pair_feasible(x,A_,B_,f) for A_,B_ in comps for f in ALL.values())
    if ok2: stats['all']+=1; print('needs other template', [round(v,3) for v in x], boxes, round(t,4)); continue
    stats['none']+=1; print('NO PAIR', [round(v,3) for v in x], boxes, round(t,4))
print(stats)
