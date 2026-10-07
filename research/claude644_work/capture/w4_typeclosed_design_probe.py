"""Probe 'heavy design + light filler' families (discovery).  Parts = points; each type = heavy
fill phi on a block S (size k), light fill lam on a set T (disjoint), zero elsewhere; equal caps x.
Scan (phi, lam) grid; report tau*, and MILP bad-tuple status when tau*>3/4."""
import itertools, sys
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp, pair_bad, load_cap42
cap=load_cap42()
def fam(blocks, lights, n, phi, lam):
    # x determined by normalisation: x*(phi*|S| + lam*|T|) = 1  (use first block sizes)
    k=len(blocks[0]); m=len(lights[0])
    x=F(1)/(phi*k+lam*m)
    A=[]
    for S,T in zip(blocks,lights):
        a=[F(0)]*n
        for i in S: a[i]=phi*x
        for i in T: a[i]=lam*x
        A.append(tuple(a))
    return A,[x]*n
def run(name,blocks,lights,n):
    best=[]
    for phi in [F(k,20) for k in range(14,20)]:
        for lam in [F(k,20) for k in range(0,14)]:
            A,x=fam(blocks,lights,n,phi,lam)
            ts=tau_star(A,x)
            if ts is None or ts<=F(3,4): continue
            if any(pair_bad(a,b,x,cap) for a in A for b in A): st='pair'
            else: st=bad_tuple_milp(A,x,time_limit=60)[0]
            print(name,'phi',phi,'lam',lam,'x',float(x[0]),'tau*',float(ts),st,flush=True)
L=[[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]]
run('fano-lines/compl',L,[[i for i in range(7) if i not in l] for l in L],7)
K5=[list(e) for e in itertools.combinations(range(5),2)]
run('K5-edges/compl',K5,[[i for i in range(5) if i not in e] for e in K5],5)
K6=[list(e) for e in itertools.combinations(range(6),2)]
run('K6-edges/compl',K6,[[i for i in range(6) if i not in e] for e in K6],6)
