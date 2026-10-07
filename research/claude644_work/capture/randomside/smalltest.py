# Small-scale tests: random k-uniform families H_rho on [N]; exact tau (MILP, HiGHS) and existence of a
# Fano-labelled bad 7-tuple (SAT: 7-colouring of V with an edge in every line window).
import numpy as np, itertools, sys, math, random
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Cadical153
LINES=[((i)%7,(i+1)%7,(i+3)%7) for i in range(7)]
def tau(N,E):
    A=np.zeros((len(E),N))
    for r,e in enumerate(E): A[r,list(e)]=1
    res=milp(c=np.ones(N),constraints=LinearConstraint(A,lb=1,ub=np.inf),integrality=np.ones(N),bounds=Bounds(0,1))
    return int(round(res.fun))
def fano_bad(N,E):
    # vars: x[v][p] = 1+v*7+p ; s[l][e] = 1+7N + l*len(E)+e
    xv=lambda v,p: 1+v*7+p
    sv=lambda l,e: 1+7*N+l*len(E)+e
    S=Cadical153()
    for v in range(N): S.add_clause([xv(v,p) for p in range(7)])
    for l in range(7):
        S.add_clause([sv(l,e) for e in range(len(E))])
        for ei,e in enumerate(E):
            for v in e:
                for p in LINES[l]: S.add_clause([-sv(l,ei),-xv(v,p)])
    # symmetry: vertex 0 colour 0 allowed wlog? (automorphism group transitive on points)
    S.add_clause([xv(0,0)])
    r=S.solve(); S.delete(); return r
def sample(N,k,rho,rng):
    M=math.comb(N,k); m=rng.binomial(M,rho)
    E=set()
    while len(E)<m: E.add(tuple(sorted(rng.choice(N,k,replace=False))))
    return list(E)
if __name__=="__main__":
    k=int(sys.argv[1]); trials=int(sys.argv[2]); seed=int(sys.argv[3]) if len(sys.argv)>3 else 0
    rng=np.random.default_rng(seed)
    stats={}
    for t in range(trials):
        N=int(rng.integers(int(1.75*k),int(3.2*k)+1))
        u=int(rng.integers(k,int(2.0*k)+1))   # target containment threshold u*
        rho=1.0/math.comb(u,k)
        if rho*math.comb(N,k)>4000: continue
        E=sample(N,k,rho,rng)
        if len(E)==0: continue
        ta=tau(N,E); fb=fano_bad(N,E)
        key=(ta,fb); stats[key]=stats.get(key,0)+1
        print(f"N={N} u*={u} |H|={len(E)} tau={ta} tau/k={ta/k:.3f} fano_bad={fb}",flush=True)
    print("SUMMARY k=",k)
    for ta in sorted(set(a for a,_ in stats)):
        print(f" tau={ta} ({ta/k:.3f}k): bad {stats.get((ta,True),0)}  no-Fano-bad {stats.get((ta,False),0)}")
