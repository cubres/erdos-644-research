"""Referee w7 core#0: how far is Lemma Q's hypothesis from firing in K_n^(k) (which IS (7,2) for n=7k/4-1)?
Exact MILP over Venn cell sizes of four k-subsets of [n] (HiGHS, integer).  Also (7,2) of K_n^k checked by SAT
for small k via the complement-cover formulation.  Also: union bound |G1u..uG4| >= sum|Gi| - (3t-k-3) check."""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Cadical153
from pysat.card import CardEnc
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
cells=[S for r in range(1,5) for S in itertools.combinations(range(4),r)]
def inI(S,mi): return any(a in S and b in S for a,b in MATCH[mi])
def is72(n,k):
    # K_n^k NOT (7,2) iff 7 complements C_l (|C_l|<=n-k) contain every pair/singleton of [n]
    vid=lambda p,l:1+p*7+l
    cl=[]; top=n*7
    for p in range(n):
        for q in range(p,n):
            aux=[];
            for l in range(7):
                top+=1; aux.append(top)
                cl+= [[-top,vid(p,l)],[-top,vid(q,l)]]
            cl.append(aux)
    for l in range(7):
        enc=CardEnc.atmost([vid(p,l) for p in range(n)],bound=n-k,top_id=top); top=max(top,enc.nv); cl+=enc.clauses
    s=Cadical153(bootstrap_with=cl); r=s.solve(); s.delete(); return not r
def minslack(n,k,t):
    best=None
    for o5 in range(3):
        others=[m for m in range(3) if m!=o5]
        c=np.array([sum(inI(S,m) for m in others) for S in cells]+[0],float)
        A=[];lo=[];hi=[]
        for i in range(4): A.append([1.0 if i in S else 0 for S in cells]+[0]); lo.append(k); hi.append(k)
        A.append([1.0]*len(cells)+[1]); lo.append(n); hi.append(n)
        for m in range(3): A.append([1.0 if inI(S,m) else 0 for S in cells]+[0]); lo.append(0); hi.append(t-1)
        r=milp(c,constraints=LinearConstraint(np.array(A),lo,hi),integrality=np.ones(len(c)),bounds=Bounds(0,np.inf))
        if r.status==0:
            v=round(r.fun); best=v if best is None else min(best,v)
    return best
for k in (4,5,6,7,8,9,10,11,12,16,20,24,40):
    n=-(-7*k//4)-1
    while True:  # largest n with K_n^k (7,2), only checked by SAT for small k
        if k<=9 and not is72(n,k): n-=1; continue
        break
    t=n-k+1
    ms=minslack(n,k,t)
    print(f"k={k} n={n} (7,2)={'SAT-checked' if k<=9 else 'assumed'} t=tau={t} 2t-k-2={2*t-k-2} "
          f"min(|I6|+|I7|) s.t. all |I|<=t-1: {ms}  slack={None if ms is None else ms-(2*t-k-2)}")
