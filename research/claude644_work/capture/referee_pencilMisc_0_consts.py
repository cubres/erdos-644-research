#!/usr/bin/env python3
"""Referee check 3: exact integer bounds delivered by the pencil scheme.
Anchor with protrusion: F edge, U host, f=|F cap U|, g=|F \\ U|, N=|U|, q=tau(H[U]), t=tau(H).
Scheme bound B(N,f,g,t) = min over label counts of max pencil cost subject to m-costs <= t-1.
(7,2) => q <= B whenever some labelling is m-feasible.  Fallbacks always valid:
q <= N - 4 floor(N/7) (Lemma 7.88), q <= t, q <= N.
Reports the worst additive excess over the claimed main term
      Mterm = max(ceil(f/2), N - 2t + g + ceil(f/2)).
Also: disjoint pairs, and Lemma D at a critical host."""
import sys, functools
from math import ceil
def c2(x): return -(-x//2)
@functools.lru_cache(None)
def pareto(X, Y):
    S=set()
    for Fb in range(X+1):
        Fbp=X-Fb
        for Fc in range(Y+1):
            Fcp=Y-Fc
            A=max(Fb+Fc, Fbp+Fcp); B=max(Fbp+Fc, Fb+Fcp)
            S.add((A,B))
    P=[p for p in S if not any(o!=p and o[0]<=p[0] and o[1]<=p[1] for o in S)]
    return tuple(P)
def scheme(N,f,g,t):
    best=None
    for XQ in range(f+1):
        pen=max(XQ, f-XQ)
        for XP in range(g+1):
            X=XQ+XP; Y=f+g-X
            for A,B in pareto(X,Y):
                if A>t-1 or B>t-1: continue
                w=max(0, N-f-(t-1-A)-(t-1-B))
                v=w+pen
                if best is None or v<best: best=v
    return best
def fano(N): return N-4*(N//7)
maxN=int(sys.argv[1]) if len(sys.argv)>1 else 22
worst_scheme=-99; worst_all=-99; arg=None; arg2=None
for t in range(1, maxN+2):
    for N in range(0, maxN+1):
        for f in range(0, N+1):
            for g in range(0, maxN+1):
                if f+g==0: continue
                M=max(c2(f), N-2*t+g+c2(f))
                s=scheme(N,f,g,t)
                ub=min(fano(N), t, N)
                if s is not None:
                    if s-M>worst_scheme: worst_scheme=s-M; arg=(N,f,g,t,s,M)
                    ub=min(ub,s)
                if ub-M>worst_all: worst_all=ub-M; arg2=(N,f,g,t,ub,M,s)
print("anchor w/ protrusion: worst excess of scheme bound over main term (where m-feasible):",worst_scheme,arg)
print("anchor w/ protrusion: worst excess of min(scheme,Fano,t,N) over main term:",worst_all,arg2)
# disjoint pairs: U=G (f=0,g=|F|, N=|G|, q>=1).  scheme infeasible or q<=B.
viol=[]
for t in range(1,30):
    for a in range(1,40):
        for b in range(1,40):
            s=scheme(b,0,a,t)   # host = G (size b), anchor F (size a) outside
            # (7,2) needs q=tau(H[G])>=1 > s to be impossible, i.e. s>=1 or infeasible
            contradiction_possible = (s is not None and s<=0)
            exact = c2(a)+c2(b)<=t-1
            if contradiction_possible!=exact: viol.append((a,b,t,s))
print("disjoint pairs: scheme contradiction <=> ceil(f/2)+ceil(g/2)<=t-1 :", "OK" if not viol else viol[:5])
# Lemma D at critical host: N=e+t-1, f=e, g=0
worst=-99; worstD=None; rows=[]
for t in range(2,120):
    for e in range(1, 2*t+4):
        s=scheme(e+t-1, e, 0, t)
        if s is None: continue
        d=t-s   # (7,2) => d >= t-s
        claimed = 2*t-3*e/2
        corr = min(2*t-3*e/2, t-e/2)
        if (t-s)-claimed < worst or worstD is None: pass
        rows.append((t,e,t-s,claimed,corr))
m1=min(r[2]-r[3] for r in rows if 4*c2(c2(e:=r[1]))>=r[0]-1) if False else None
lo_claim_all=min(r[2]-r[3] for r in rows)
lo_claim_big=min(r[2]-r[3] for r in rows if r[1]>=r[0]-1)
lo_corr=min(r[2]-r[4] for r in rows)
print("critical host: min over (t,e) of [proved lower bound on d] - (2t-3e/2): all e:",lo_claim_all,"  e>=t-1:",lo_claim_big)
print("critical host: min of [proved d-lower bound] - min(2t-3e/2, t-e/2) over all e:",lo_corr)
ex=[r for r in rows if r[2]-r[3]<-5.5][:3]
print("examples where proved bound falls short of 2t-3e/2 by >5.5:",ex)
