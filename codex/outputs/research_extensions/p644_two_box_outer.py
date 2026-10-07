"""Outer MILP discovery: can both orientations of M1 and M5 fail?

The parameter domain consists of two sliced boxes on three parts. This search
is numerical and cannot prove a theorem without an independently replayable
exact certificate. Its feasible points are rechecked separately.
"""
from fractions import Fraction as F
import itertools,json,time,math
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix


P=3;DIM=16;GAMMA=15


def const(v=0):
    a=[F(0)]*(DIM+1);a[-1]=F(v);return a


def var(i):
    a=const();a[i]=1;return a


def add(*args):return [sum(q) for q in zip(*args)]
def mul(t,a):return [t*v for v in a]
def sub(a,b):return add(a,mul(-1,b))
X=[var(i) for i in range(P)]
LO=[[var(3+6*k+i) for i in range(P)] for k in range(2)]
HI=[[var(6+6*k+i) for i in range(P)] for k in range(2)]


def dot(v,w):return sum(a*b for a,b in zip(v,w))


def support_forms(normals, rhs, direction):
    """All extreme dual majorants for a 2D support LP, exactly."""
    out=[]
    for i,n in enumerate(normals):
        vals=[F(direction[k],n[k]) for k in range(2) if n[k]]
        if vals and len(set(vals))==1 and vals[0]>=0 and all(n[k] or direction[k]==0 for k in range(2)):
            out.append(mul(vals[0],rhs[i]))
    for i,j in itertools.combinations(range(len(normals)),2):
        a,b=normals[i],normals[j];det=a[0]*b[1]-a[1]*b[0]
        if not det:continue
        s=F(direction[0]*b[1]-direction[1]*b[0],det)
        t=F(a[0]*direction[1]-a[1]*direction[0],det)
        if s>=0 and t>=0:out.append(add(mul(s,rhs[i]),mul(t,rhs[j])))
    unique=sorted(set(tuple(a) for a in out))
    # Parameters are nonnegative, so coefficientwise larger majorants can
    # never attain the minimum in preference to the smaller one.
    return [list(a) for a in unique if not any(b!=a and all(v<=w for v,w in zip(b,a)) for b in unique)]


def normalize(a):
    scale=1
    for c in a:scale=scale*c.denominator//math.gcd(scale,c.denominator)
    ints=[int(c*scale) for c in a];g=0
    for c in ints:g=math.gcd(g,abs(c))
    return tuple(F(c,g or 1) for c in ints)


def failure_facets(couplings,flip=False):
    """Forms f>0 equivalent to failure for a pair of box types.

    Couplings are (u,v,w): u*a_i+v*b_i <= w*x_i.
    Summing 2D coordinate polygons preserves the finite set of edge normals.
    """
    first,second=(1,0) if flip else (0,1)
    fail=[]
    for i in range(P):
        for u,v,w in couplings:
            fail.append(sub(add(mul(u,LO[first][i]),mul(v,LO[second][i])),mul(w,X[i])))
    normals=[(-1,0),(0,-1),(1,0),(0,1)]+[(u,v) for u,v,w in couplings]
    dirs=sorted(set((u//math.gcd(u,v),v//math.gcd(u,v)) for u,v in [(1,0),(0,1)]+[(u,v) for u,v,w in couplings]))
    for d in dirs:
        choices=[]
        for i in range(P):
            rhs=[mul(-1,LO[first][i]),mul(-1,LO[second][i]),HI[first][i],HI[second][i]]
            rhs +=[mul(w,X[i]) for u,v,w in couplings]
            choices.append(support_forms(normals,rhs,d))
        for q in itertools.product(*choices):fail.append(sub(const(sum(d)),add(*q)))
    return [list(a) for a in sorted(set(normalize(a) for a in fail))]


def blockers(k):
    out=[]
    for i in range(P):out.append((1<<i,LO[k][i],sub(X[i],LO[k][i])))
    for mask in range(1,1<<P):
        rhs=sub(const(1),add(*(HI[k][i] for i in range(P) if not mask>>i&1)) if mask!=(1<<P)-1 else const())
        cost=sub(add(*(X[i] for i in range(P) if mask>>i&1)),rhs)
        out.append((mask,rhs,cost))
    return out


def base_system(tight=False,compact=False,symmetry=True,line_template=False):
    # All constraints here are affine forms >= 0; disjunctions are lists.
    single=[];groups=[];gamma=var(GAMMA)
    for k in range(2):
        for i in range(P):
            single.extend([sub(HI[k][i],LO[k][i]),sub(X[i],HI[k][i])])
            if tight:
                single.append(sub(add(LO[k][i],*(HI[k][j] for j in range(P) if i!=j)),const(1)))
                single.append(sub(const(1),add(HI[k][i],*(LO[k][j] for j in range(P) if i!=j))))
        single.extend([sub(const(1),add(*LO[k])),sub(add(*HI[k]),const(1))])
    if tight and symmetry:
        single.extend(sub(X[i+1],X[i]) for i in range(P-1))
        single.append(sub(add(*LO[1]),add(*LO[0])))
    if compact:
        assert tight
        # Canonical bounds make singleton min-sum blockers redundant; full
        # blockers all give the same bound N-1. Keep the three coordinate
        # blockers and three two-coordinate sum blockers per component.
        single.append(sub(sub(add(*X),const(F(7,4))),gamma))
        pools=[blockers(k)[:3]+[v for v in blockers(k)[3:] if bin(v[0]).count('1')==2] for k in range(2)]
    else:pools=[blockers(k) for k in range(2)]
    for (s,r,a),(t,q,b) in itertools.product(*pools):
        cap=add(*(X[i] for i in range(P) if (s&t)>>i&1)) if s&t else const()
        groups.append([mul(-1,r),mul(-1,q),sub(sub(a,const(F(3,4))),gamma),
                       sub(sub(b,const(F(3,4))),gamma),
                       sub(sub(sub(add(a,b),cap),const(F(3,4))),gamma)])
    # Intersectingness within each component, and between components.
    for k in range(2):
        choices=[sub(mul(2,LO[k][i]),X[i]) for i in range(P)]
        for mask in range(1<<P):
            choices.append(sub(const(2),add(*(mul(2,HI[k][i]) if mask>>i&1 else X[i] for i in range(P)))))
        groups.append([sub(a,gamma) for a in choices])
    groups.append([sub(a,gamma) for a in failure_facets([(1,1,1)])])
    # Four sufficient bad-tuple constructions must all fail.
    templates=[[(1,6,4)],[(3,0,2),(5,2,4),(1,2,2)]]
    if line_template:templates.append([(0,3,2),(4,3,4)])
    for coupling in templates:
        for flip in (False,True):
            groups.append([sub(a,gamma) for a in failure_facets(coupling,flip)])
    return single,groups


def solve(seconds=120,tight=False):
    started=time.time();single,groups=base_system(tight)
    sizes=[len(g) for g in groups];n=DIM+sum(sizes);nr=len(single)+sum(sizes)+len(groups)
    A=lil_matrix((nr,n));lb=np.full(nr,-np.inf);ub=np.full(nr,np.inf)
    lower=[0]*DIM;upper=[2]*3+[1]*12+[F(1,4)]
    if tight:
        lower[:3]=[F(1,100)]*3;lower[GAMMA]=F(1,10000)
    row=0;binary=DIM
    for a in single:
        A[row,:DIM]=list(map(float,a[:-1]));lb[row]=-float(a[-1]);row+=1
    for group in groups:
        ids=[]
        for a in group:
            # Minimum over the entire bounded continuous parameter box.
            amin=float(a[-1])+sum(float(v)*float(upper[i] if v<0 else lower[i]) for i,v in enumerate(a[:-1]))
            M=max(0,-amin)+1
            A[row,:DIM]=list(map(float,a[:-1]));A[row,binary]=-M
            lb[row]=-float(a[-1])-M;row+=1;ids.append(binary);binary+=1
        for j in ids:A[row,j]=1
        lb[row]=1;row+=1
    assert row==nr
    objective=np.zeros(n);objective[GAMMA]=-1
    print('Outer system',n,'variables',nr,'rows; largest disjunction',max(sizes),flush=True)
    res=milp(objective,integrality=[0]*DIM+[1]*(n-DIM),
             bounds=Bounds(list(map(float,lower))+[0]*(n-DIM),list(map(float,upper))+[1]*(n-DIM)),
             constraints=LinearConstraint(A.tocsr(),lb,ub),
             options={'time_limit':seconds,'mip_rel_gap':1e-8})
    out={'status':int(res.status),'message':res.message,'elapsed':time.time()-started,'tight':tight,
         'continuous':None if res.x is None else res.x[:DIM].tolist(),
         'objective':None if res.fun is None else float(res.fun),'group_sizes':sizes,
         'mip_gap':None if getattr(res,'mip_gap',None) is None else float(res.mip_gap),
         'mip_dual_bound':None if getattr(res,'mip_dual_bound',None) is None else float(res.mip_dual_bound)}
    Path('logs/astra_two_box_outer%s.json'%('_tight' if tight else '')).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--tight',action='store_true')
    ar=ap.parse_args();solve(ar.seconds,ar.tight)
