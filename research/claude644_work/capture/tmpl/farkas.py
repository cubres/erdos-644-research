# exact Farkas implication certificates: cons (list of (coef,const), meaning g>=0) imply f>=0 ?
import itertools
from fractions import Fraction as F
from lib2 import solve
def implies(cons, f, names=None):
    n=len(f[0]); best=None
    idx=range(len(cons))
    for r in range(0,n+1):
        for S in itertools.combinations(idx,r):
            # solve sum_{i in S} lam_i coef_i = f.coef  (n equations, r unknowns) least-squares exact: pick r eqs
            if r==0:
                if all(F(c)==0 for c in f[0]):
                    const=F(f[1]); 
                    if const>=0: return {},const
                continue
            for E in itertools.combinations(range(n),r):
                A=[[F(cons[i][0][e]) for i in S] for e in E]; b=[F(f[0][e]) for e in E]
                lam=solve(A,b)
                if lam is None or any(l<0 for l in lam): continue
                if any(sum(lam[k]*F(cons[i][0][e]) for k,i in enumerate(S))!=F(f[0][e]) for e in range(n)): continue
                const=F(f[1])-sum(lam[k]*F(cons[i][1]) for k,i in enumerate(S))
                if const>=0:
                    return {i:lam[k] for k,i in enumerate(S)},const
    return None
def fmt(c, vars=('x','y','al','be')):
    co,k=c; s=' + '.join(f'{F(a)}*{v}' for a,v in zip(co,vars) if F(a)!=0)
    return f'{s} + {F(k)} >= 0'

def implies2(cons, f):
    """LP-guided exact implication certificate. Returns (dict i->lambda, const) or None."""
    import numpy as np
    from scipy.optimize import linprog
    import itertools
    n=len(f[0]); m=len(cons)
    if m==0:
        return ({},F(f[1])) if all(F(c)==0 for c in f[0]) and F(f[1])>=0 else None
    Aeq=np.array([[float(cons[i][0][e]) for i in range(m)] for e in range(n)])
    beq=np.array([float(c) for c in f[0]])
    cobj=np.array([float(cons[i][1]) for i in range(m)])  # minimize sum lam*gconst  => const = fconst - that
    r=linprog(cobj,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*m,method='highs')
    if r.status!=0: return None
    if float(f[1])-r.fun < -1e-9: return None
    supp=[i for i in range(m) if r.x[i]>1e-10]
    # exact solve on support: find independent equation subset
    from lib2 import solve
    for E in itertools.combinations(range(n),len(supp)):
        A=[[F(cons[i][0][e]) for i in supp] for e in E]; b=[F(f[0][e]) for e in E]
        lam=solve(A,b)
        if lam is None: continue
        if any(l<0 for l in lam): continue
        if any(sum(lam[k]*F(cons[i][0][e]) for k,i in enumerate(supp))!=F(f[0][e]) for e in range(n)): continue
        const=F(f[1])-sum(lam[k]*F(cons[i][1]) for k,i in enumerate(supp))
        if const>=0: return ({i:lam[k] for k,i in enumerate(supp)},const)
    # fallback exhaustive
    return implies(cons,f)
