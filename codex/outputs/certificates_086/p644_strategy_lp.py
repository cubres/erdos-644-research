"""Strict-support strategy verification by exact-checked LP discoveries.

On each branch of the named min-picks, atom masses form a convex polyhedron.
Supports can be united by averaging feasible vectors. Thus local piercing
and intersectingness can be checked on the maximal feasible support, with
no positive occupancy cutoff. Floating LPs discover points/duals, but every
used point and dual is checked with Fraction arithmetic; failed recovery
returns UNKNOWN. Request legality still needs a separate budget argument.

The inherited atom/pick expansion supplies the linear constraints. This
module does not use its occupancy indicators or 2-pierceability encoding.
"""
import itertools as it
import time
from fractions import Fraction as F
import numpy as np
from scipy.sparse import vstack,hstack,csr_matrix
from scipy.optimize import linprog
from p644_strategy import Script,Aff
from p644_strategy2 import build


def frac(v):return F(str(float(v)))


def exact_rows(A):
    return [[(int(A.indices[k]),frac(A.data[k])) for k in range(A.indptr[i],A.indptr[i+1])]
            for i in range(A.shape[0])]


def dot(row,x):return sum((v*x[j] for j,v in row),F(0))


def recover(values):return [F(float(v)).limit_denominator(10**7) for v in values]


def support_condition(script,support):
    if script.intersecting:
        for a,b in it.combinations(range(1,script.J+1),2):
            if not any(a in C and b in C for C in support):return ('disjoint forced pair',(a,b))
    for Q in it.combinations(range(1,script.J+1),min(script.J,7)):
        Q=frozenset(Q)
        if not any(Q<=A|B for A in support for B in support):return ('bad subfamily',tuple(sorted(Q)))
    return None


def branch_solve(script,m,pick_values,seconds=60,want=False):
    n=len(m['atoms']);nz=(1<<script.J)-1
    fixed=np.r_[np.ones(nz),pick_values]
    rhs=m['A'][:,n:]@fixed
    lo=m['lbs']-rhs;hi=m['ubs']-rhs;A=m['A'][:,:n].tocsr()
    eq=np.isfinite(lo)&np.isfinite(hi)&(lo==hi)
    upp=np.isfinite(hi)&~eq;low=np.isfinite(lo)&~eq
    Ae=A[eq];be=hi[eq];Au=vstack([A[upp],-A[low]],format='csr');bu=np.r_[hi[upp],-lo[low]]
    er=exact_rows(Ae);ur=exact_rows(Au);eb=list(map(frac,be));ub=list(map(frac,bu))
    start=time.monotonic();support=set();points=[]

    def verify_primal(x):
        return all(v>=0 for v in x) and all(dot(r,x)==b for r,b in zip(er,eb)) and all(dot(r,x)<=b for r,b in zip(ur,ub))

    def verify_dual(ye,yu,c,infeasible=False):
        if any(v>0 for v in yu):return False
        grad=[F(0)]*n
        for rows,weights in [(er,ye),(ur,yu)]:
            for row,v in zip(rows,weights):
                if v:
                    for j,a in row:grad[j]+=v*a
        val=sum(v*b for v,b in zip(ye,eb))+sum(v*b for v,b in zip(yu,ub))
        if infeasible:return val>0 and all(v<=0 for v in grad)
        return val>=0 and all(v<=int(w) for v,w in zip(grad,c))

    for count in range(1,2**script.J+2):
        if time.monotonic()-start>seconds:return {'status':'UNKNOWN','reason':'time limit'}
        c=np.array([-int(C not in support) for C,L in m['atoms']],dtype=float)
        q=linprog(c,A_ub=Au,b_ub=bu,A_eq=Ae,b_eq=be,bounds=(0,None),method='highs',options={'time_limit':max(1,seconds-(time.monotonic()-start))})
        if q.status==2:
            D=hstack([Au.T,Ae.T],format='csr');rhsdual=np.r_[bu,be]
            dq=linprog(np.zeros(len(rhsdual)),A_ub=vstack([D,csr_matrix(-rhsdual[None,:])]),
                       b_ub=np.r_[np.zeros(n),-1],bounds=[(None,0)]*len(bu)+[(None,None)]*len(be),method='highs')
            if dq.status!=0:return {'status':'UNKNOWN','reason':'Farkas discovery failed'}
            yu=recover(dq.x[:len(bu)]);ye=recover(dq.x[len(bu):])
            if not verify_dual(ye,yu,c,True):return {'status':'UNKNOWN','reason':'Farkas recovery failed'}
            return {'status':'EMPTY_BRANCH','lp_calls':count,'dual_eq':list(map(str,ye)),'dual_ub':list(map(str,yu))}
        if q.status!=0:return {'status':'UNKNOWN','reason':q.message}
        x=recover(q.x)
        if not verify_primal(x):return {'status':'UNKNOWN','reason':'exact primal recovery failed'}
        new={C for (C,L),v in zip(m['atoms'],x) if v>0}
        points.append(x);old=set(support);support.update(new)
        obstruction=support_condition(script,support)
        if obstruction is None:
            out={'status':'ADVERSARY SURVIVES','lp_calls':count,'support_cells':len(support)}
            if want:
                mean=[sum(P[j] for P in points)/len(points) for j in range(n)]
                assert verify_primal(mean)
                out['atoms']=[{'edges':sorted(C),'picks':sorted(L),'mass':str(v)} for (C,L),v in zip(m['atoms'],mean) if v>0]
            return out
        if support==old:
            ye=recover(q.eqlin.marginals);yu=recover(q.ineqlin.marginals)
            if not verify_dual(ye,yu,c):return {'status':'UNKNOWN','reason':'support dual recovery failed'}
            return {'status':'PROVER WINS','lp_calls':count,'obstruction':obstruction,
                    'support':[sorted(C) for C in sorted(support,key=lambda s:tuple(sorted(s)))],
                    'dual_eq':list(map(str,ye)),'dual_ub':list(map(str,yu))}
    return {'status':'UNKNOWN','reason':'support iteration bound'}


def solve(script,time_limit=60,want=False,max_branches=4096):
    relaxed=Script(script.J,script.D,script.budget,script.steps,intersecting=False,hyps=script.hyps)
    if hasattr(script,'final_picks'):relaxed.final_picks=script.final_picks
    m=build(relaxed,continuous=True,eps=0,subfamilies=[])
    choices=[]
    for name,(host,placed,size) in m['pickhost'].items():
        zero=(isinstance(size,Aff) and not size.terms and size.const==0) or (not isinstance(size,Aff) and size==0)
        choices.append([1] if zero else [0,1])
    count=np.prod([len(c) for c in choices],dtype=int) if choices else 1
    if count>max_branches:return {'status':'UNKNOWN','reason':f'{count} pick branches exceed limit'}
    branches=[]
    for ys in it.product(*choices):
        out=branch_solve(script,m,ys,seconds=time_limit,want=want);out['pick_values']=ys
        if out['status']=='ADVERSARY SURVIVES':return out
        branches.append(out)
    if any(b['status']=='UNKNOWN' for b in branches):return {'status':'UNKNOWN','branches':branches}
    return {'status':'PROVER WINS','branches':branches,'n_atoms':len(m['atoms'])}


if __name__=='__main__':
    import json
    from p644_explore8 import script8
    from p644_strategy import mass,contains
    tests=[]
    sc=script8(5,2,2,0,8,'A')
    tests.append(('inherited_eight_edge',sc))
    tests.append(('unconstrained_intersecting',Script(7,16,13,{},intersecting=True)))
    tests.append(('tiny_common_cell',Script(7,1,1,{},intersecting=True,hyps=[
        (mass(contains(*range(1,8))),1e-6,1e-6),
        (mass(lambda E,L,placed:2<=len(E)<=6),0,0)])))
    report=[]
    for name,S in tests:
        start=time.monotonic();out=solve(S,time_limit=60,want=True)
        print(name,out['status'],round(time.monotonic()-start,2),'seconds',flush=True)
        report.append({'name':name,'result':out})
    from pathlib import Path
    Path('logs/astra_strategy_lp_checks.json').write_text(json.dumps(report,indent=1))
