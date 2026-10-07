"""Independent exact verification of the inherited two-type polygons.

Floating LPs only discover candidate basic solutions. Fraction/sympy checks
certify every mass, every edge size and every forbidden covering pair.
Coverage uses successive convex subtraction, avoiding exponential
inclusion-exclusion. Closed polygons covering the triangle up to area zero
cover all of it. The input is read once, so concurrent refinement is safe.
"""
import argparse
import itertools as it
import json
import time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import sympy as sp


def area(P):
    return abs(sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(P,P[1:]+P[:1])),F(0)))/2


def line(a,b):
    return (a[1]-b[1],b[0]-a[0],a[0]*b[1]-a[1]*b[0])


def clip(P,L):
    a,b,c=L;out=[]
    for X,Y in zip(P,P[1:]+P[:1]):
        x=a*X[0]+b*X[1]+c;y=a*Y[0]+b*Y[1]+c
        if x>=0:out.append(X)
        if (x<0<y) or (y<0<x):
            t=x/(x-y);out.append((X[0]+t*(Y[0]-X[0]),X[1]+t*(Y[1]-X[1])))
    return list(dict.fromkeys(out))


def subtract(P,Q):
    out=[];inside=P
    for X,Y in zip(Q,Q[1:]+Q[:1]):
        L=line(X,Y)
        outside=clip(inside,tuple(-v for v in L))
        if area(outside)>0:out.append(outside)
        inside=clip(inside,L)
        if not area(inside):break
    return out


def verify_vertex(types,support,d,c,delta):
    # Variables are original support masses AND legal singleton slack masses.
    full=frozenset(range(7));S=[(s,frozenset(v)) for s,v in support]
    assert all(s in (1,2) and v and v<full for s,v in S)
    assert all(a|b!=full for (_,a),(_,b) in it.product(S,repeat=2))
    val={'A1':(F(1),F(0)),'A2':(F(0),F(1)),
         's':(d,1-d),'t':(c,1-c)}
    targets=[val[t] for t in types]
    original=len(S)
    for side in (1,2):
        for j in range(7):
            v=frozenset([j])
            if targets[j][side-1] and all(v|w!=full for _,w in S):
                if (side,v) not in S:S.append((side,v))
    n=len(S);A=[];b=[]
    for side in (1,2):
        for j in range(7):
            A.append([int(s==side and j in v) for s,v in S]);b.append(targets[j][side-1])
    U=[[int(s==side) for s,v in S] for side in (1,2)]
    lower=[delta]*original+[F(0)]*(n-original)
    res=linprog(np.zeros(n),A_ub=np.array(U),b_ub=np.ones(2),
                A_eq=np.array(A),b_eq=np.array(list(map(float,b))),
                bounds=[(float(x),None) for x in lower],method='highs')
    if res.status!=0:raise ValueError(('numeric discovery failed',res.message,d,c))
    active=[(r,v) for r,v in zip(A,b)]
    for row in U:
        if abs(np.dot(row,res.x)-1)<1e-7:active.append((row,F(1)))
    for i,x in enumerate(lower):
        if abs(res.x[i]-float(x))<1e-7:
            row=[0]*n;row[i]=1;active.append((row,x))
    # Select independent active rows without assuming every near-tight row is tight.
    mat=sp.Matrix([r for r,_ in active]);pivots=mat.T.rref()[1]
    if len(pivots)!=n:raise ValueError(('insufficient active rank',len(pivots),n))
    square=sp.Matrix([active[i][0] for i in pivots]);rhs=sp.Matrix([sp.Rational(active[i][1]) for i in pivots])
    sol=[F(v) for v in square.inv()*rhs]
    assert all(x>=lo for x,lo in zip(sol,lower))
    assert all(sum(r[i]*sol[i] for i in range(n))==v for r,v in zip(A,b))
    assert all(sum(r[i]*sol[i] for i in range(n))<=1 for r in U)
    assert all(a|b!=full for (_,a),(_,b) in it.product(S,repeat=2))
    return [(s,sorted(v),str(x)) for (s,v),x in zip(S,sol) if x]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--out',default='logs/astra_cover_certificate.json')
    args=ap.parse_args();data=json.loads(Path(args.input).read_text());delta=F(data['delta']);gap=F(data['gap'])
    start=time.monotonic();R=[(gap,F(1,2)),(F(1,2),F(1,2)),(F(1,2),1-gap)]
    templates=data['templates'];polys=[[(F(x),F(y)) for x,y in t['poly']] for t in templates]
    # Verify all convex polygons are nondegenerate and counterclockwise.
    for P in polys:
        assert area(P)>0
        assert all(a*x+b*y+c>=0 for a,b,c in [line(U,V) for U,V in zip(P,P[1:]+P[:1])] for x,y in P)
    remaining=[R];used=[]
    for i in sorted(range(len(polys)),key=lambda i:area(polys[i]),reverse=True):
        before=sum(map(area,remaining),F(0));new=[]
        for P in remaining:new.extend(subtract(P,polys[i]))
        remaining=new;after=sum(map(area,remaining),F(0))
        assert after<=before
        if after<before:used.append(i)
        if len(used)%10==0 or not remaining:
            print('coverage',len(used),'used',len(remaining),'pieces',float(after),'area',round(time.monotonic()-start,1),'s',flush=True)
        if not remaining:break
    cert={'delta':str(delta),'gap':str(gap),'covered':not remaining,
          'remaining':[[[str(x),str(y)] for x,y in P] for P in remaining], 'templates':[]}
    for count,i in enumerate(used,1):
        t=templates[i];P=polys[i];vertices=[]
        for d,c in P:
            cells=verify_vertex(t['types'],t['support'],d,c,delta)
            vertices.append({'d':str(d),'c':str(c),'cells':cells})
        cert['templates'].append({'index':i,'types':t['types'],'vertices':vertices})
        if count%10==0:print('exact masses',count,'/',len(used),flush=True)
    Path(args.out).write_text(json.dumps(cert,indent=2))
    print('DONE exact coverage',cert['covered'],'verified templates',len(used),'remaining',len(remaining),'elapsed',round(time.monotonic()-start,1),flush=True)


if __name__=='__main__':main()
