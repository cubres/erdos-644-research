"""NUMERICAL: random tight staircases in the residual |H|=2 regime (parts 0 light, 1=j, 2=k).
A-types (p, 1-p-(thk+al), thk+al), B-types (q, thj+be, 1-q-thj-be); phi_A(d)+phi_B(d) < eps0 + d (condition (M))
made nearly tight at random breakpoints.  Checks exact-float tau*>3/4 and pair kills (42 fns)."""
import random, itertools, sys
from h2climb import tau_star, C42
def pk(a,b,x,eps=1e-9):
    return any(all(max(u*a[i]+v*b[i] for u,v in f)<=x[i]+eps for i in range(3)) for f in C42)
rng=random.Random(int(sys.argv[1])); n=0; unk=0
for trial in range(int(sys.argv[2])):
    x0=rng.uniform(0.02,0.5); xj=rng.uniform(0.76,1.5); xk=rng.uniform(0.76,1.5)
    if xj+xk<=2.25: continue
    thj=rng.uniform(2*xj/3,min(1,xj)); thk=rng.uniform(2*xk/3,min(1,xk))
    eps0=(xj-thj)+(xk-thk)-0.75
    if eps0<=0: continue
    x=[x0,xj,xk]
    # A minimiser light coord pA, B minimiser qB with pA+qB>x0 (residual), both <=4x0/7 and mass-feasible
    pA=rng.uniform(0,min(4*x0/7,1-thk)); qB=rng.uniform(0,min(4*x0/7,1-thj))
    if pA+qB<=x0: continue
    A=[(pA,1-pA-thk,thk)]; B=[(qB,thj,1-qB-thj)]
    # breakpoints: for delta in (x0-pA, x0], A needs types with a0<=x0-delta; split budget eps0+delta
    K=rng.randint(1,4); lam=rng.uniform(0,1)
    for k in range(1,K+1):
        d=x0*k/K                 # level delta
        tot=eps0+x0*(k-1)/K-1e-4  # serves s in [x0-d, x0-d_prev)
        fa=lam*tot*rng.uniform(0.9,1); fb=tot-fa
        pa=max(0,x0-d); 
        if x0-d< pA: A.append((pa,1-pa-thk-fa,thk+fa))
        if x0-d< qB: B.append((pa,thj+fb,1-pa-thj-fb))
    ts=[c for c in A+B if min(c)>=-1e-12 and all(c[i]<=x[i]+1e-12 for i in range(3)) and c[0]<=4*x0/7+1e-12]
    if len(ts)<len(A)+len(B): continue
    t=tau_star(ts,x)
    if t<=0.75: continue
    n+=1
    if not any(pk(a,b,x) for a,b in itertools.combinations(ts,2)):
        unk+=1; print('NO PAIR KILL',round(t,4),[round(v,4) for v in x],[[round(v,4) for v in c] for c in ts],flush=True)
print('families',n,'without pair kill',unk)
