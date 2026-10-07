#!/usr/bin/env python3
"""Referee check 3b: (i) scheme-bound excess over main term, random sample to size 60;
(ii) m-infeasible region handled by min(Fano,t,N), exhaustive to N=150."""
import random, functools
def c2(x): return -(-x//2)
@functools.lru_cache(None)
def pareto(X, Y):
    S=set()
    for Fb in range(X+1):
        for Fc in range(Y+1):
            S.add((max(Fb+Fc, X-Fb+Y-Fc), max(X-Fb+Fc, Fb+Y-Fc)))
    return tuple(p for p in S if not any(o!=p and o[0]<=p[0] and o[1]<=p[1] for o in S))
@functools.lru_cache(None)
def minmax(T):
    # minimal max(A,B) over all X+Y=T : feasibility iff <= t-1
    return min(max(p) for X in range(T+1) for p in pareto(X,T-X))
def scheme(N,f,g,t):
    best=None
    for XQ in range(f+1):
        pen=max(XQ,f-XQ)
        if best is not None and pen>=best: continue
        for XP in range(g+1):
            X=XQ+XP; Y=f+g-X
            for A,B in pareto(X,Y):
                if A>t-1 or B>t-1: continue
                v=max(0,N-f-(t-1-A)-(t-1-B))+pen
                if best is None or v<best: best=v
    return best
fano=lambda N: N-4*(N//7)
random.seed(7); worst=-9; arg=None
for _ in range(4000):
    t=random.randint(1,45); N=random.randint(0,60); f=random.randint(0,N); g=random.randint(0,60)
    if f+g==0: continue
    s=scheme(N,f,g,t)
    if s is None: continue
    M=max(c2(f),N-2*t+g+c2(f))
    if s-M>worst: worst=s-M; arg=(N,f,g,t,s,M)
print("random sample: worst scheme excess",worst,arg)
print("minmax(T) - ceil(T/2) for T<60:",sorted(set(minmax(T)-c2(T) for T in range(60))))
worst=-9; arg=None
for t in range(1,160):
    for T in range(1,2*t+10):
        if minmax(T)<=t-1: continue   # feasible: scheme applies
        for N in range(0,151):
            for f in range(0,min(N,T)+1):
                g=T-f
                M=max(c2(f),N-2*t+g+c2(f))
                ub=min(fano(N),t,N)
                if ub-M>worst: worst=ub-M; arg=(N,f,g,t,ub,M)
print("infeasible region: worst excess of min(Fano,t,N) over main term:",worst,arg)
