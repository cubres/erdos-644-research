"""NUMERICAL: |H|=2 residual regime.  3 parts: part 0 LIGHT (every type c_0 <= 4x_0/7), parts 1,2 heavy.
Maximise tau*(C) over (x, m types) subject to: no hom-Fano type, no pencil/QL single, no pair killed by the
42 two-type functions, GQL(e,e,f,f) or mixed pencil.  (All these are valid bad-tuple producers when tau*>3/4.)
Reports best tau*; if > 3/4, the family needs >= 3 actual types."""
import random, sys, math, itertools
import numpy as np
from cap42 import load
C42=[[(float(u),float(v)) for u,v in f] for f in load()]
def tau_star(types,x):
    p=len(x); N=sum(x); best=-1
    cand=[sorted(set(t[i] for t in types if t[i]>1e-12)) for i in range(p)]
    def rec(i,alive,acc):
        nonlocal best
        if i==p:
            if not alive and acc>best: best=acc
            return
        if acc+sum(x[i:])<=best: return
        rec(i+1,alive,acc+x[i])
        for g in cand[i]: rec(i+1,[t for t in alive if t[i]<g-1e-12],acc+g)
    rec(0,types,0.0); return N-best
def single_killed(c,x,eps=1e-9):
    if all(7*c[i]<=4*x[i]+eps for i in range(3)): return True
    if all(3*c[i]<=2*x[i]+eps for i in range(3)): return True
    if sum(max(0,2*c[i]-x[i]) for i in range(3))<=0.25+eps: return True
    return False
def pair_killed(a,b,x,eps=1e-9):
    for f in C42:
        if all(max(u*a[i]+v*b[i] for u,v in f)<=x[i]+eps for i in range(3)): return True
    K2=sum(max(0,2*a[i]-x[i],2*b[i]-x[i]) for i in range(3)); K1=sum(max(0,a[i]+b[i]-x[i]) for i in range(3))
    if K2<=0.75+eps and K1<=0.25+eps: return True
    for e,f in ((a,b),(b,a)):
        if all(2*e[i]+f[i]<=2*x[i]+eps and f[i]<=2*e[i]+eps for i in range(3)): return True
    return False
def valid(types,x):
    for c in types:
        if c[0]>4*x[0]/7+1e-12 or any(c[i]>x[i]+1e-12 for i in range(3)) or single_killed(c,x): return False
    for a,b in itertools.combinations(types,2):
        if pair_killed(a,b,x): return False
    return True
def rand_type(x,rng):
    for _ in range(100):
        c0=rng.uniform(0,min(4*x[0]/7,1)); r=1-c0; c1=rng.uniform(max(0,r-x[2]),min(x[1],r)); c=(c0,c1,r-c1)
        if c[2]<=x[2]+1e-12 and c[2]>=0: return c
    return None
def climb(m,rng,iters=4000):
    while True:
        x=[rng.uniform(0.2,1.2),rng.uniform(0.5,1.75),rng.uniform(0.5,1.75)]
        ts=[rand_type(x,rng) for _ in range(m)]
        if None in ts: continue
        if valid(ts,x): break
    cur=tau_star(ts,x); T=0.02
    for it in range(iters):
        x2=[max(0.05,v+rng.gauss(0,0.03)) for v in x]; ts2=[]
        for c in ts:
            if rng.random()<0.5:
                d=[rng.gauss(0,0.03) for _ in range(3)]; s=sum(d)/3; c=tuple(max(0,c[i]+d[i]-s) for i in range(3)); s=sum(c); c=tuple(v/s for v in c)
            ts2.append(c)
        if not valid(ts2,x2): continue
        v=tau_star(ts2,x2)
        if v>cur or rng.random()<math.exp((v-cur)/T): x,ts,cur=x2,ts2,v
        T=max(0.001,T*0.999)
    return cur,x,ts
if __name__=='__main__':
    m=int(sys.argv[1]); seed=int(sys.argv[2]); rng=random.Random(seed); best=(-1,)
    for r in range(int(sys.argv[3]) if len(sys.argv)>3 else 20):
        res=climb(m,rng)
        if res[0]>best[0]: best=res; print('best',round(res[0],4),[round(v,4) for v in res[1]],[[round(v,4) for v in c] for c in res[2]],flush=True)
    print('FINAL',best[0])
