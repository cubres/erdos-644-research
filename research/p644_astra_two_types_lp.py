"""Test a two-template dichotomy for intersecting two-type families.

If both the one-a/six-b and five-a/two-b Fano-downset templates fail,
retain their witnessing coordinates plus one coordinate forcing cross-type
intersection. Remaining coordinates contribute only to the total type sizes.
An LP optimizes a common strictness margin for each support/order case.
Positive solutions are explicit obstructions to the proposed dichotomy;
zero optima are not theorems until rational duals are checked.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def model(i,j,facet,states):
    n=len(states);N=3*n+1;g=N-1;rows=[];rhs=[]
    def add(d,b):
        r=[F(0)]*N
        for key,v in d.items():r[key]+=F(v)
        rows.append(r);rhs.append(F(b))
    aa=lambda k:3*k;bb=lambda k:3*k+1;xx=lambda k:3*k+2
    add({aa(k):1 for k in range(n)},1);add({bb(k):1 for k in range(n)},1)
    add({g:1},1)
    for k,state in enumerate(states):
        a,b,x=aa(k),bb(k),xx(k)
        add({a:1,x:-1},0);add({b:1,x:-1},0);add({x:1},2)
        if state=='A':add({b:1},0);add({g:1,a:-1},0)
        elif state=='B':add({a:1},0);add({g:1,b:-1},0)
        else:
            add({g:1,a:-1},0);add({g:1,b:-1},0)
            if state=='ab':add({b:1,a:-1},0);minimum=b
            else:add({a:1,b:-1},0);minimum=a
            add({minimum:1,x:-1,g:1},-F(3,4))
    for k in range(n):
        if states[k]=='B':continue
        for l in range(n):
            if l==k or states[l]=='A':continue
            add({xx(k):-1,aa(k):1,xx(l):-1,bb(l):1,g:1},-F(3,4))
    add({xx(0):1,aa(0):-1,bb(0):-1,g:1},0)
    # max(a0,b0)=a0 by the chosen orientation of the two types.
    add({xx(i):1,aa(i):-F(1,4),bb(i):-F(3,2),g:1},0)
    ca,cb=facet
    add({xx(j):1,aa(j):-ca,bb(j):-cb,g:1},0)
    c=[0]*N;c[g]=-1
    return rows,rhs,c


def main():
    results=[]
    for i,j in [(0,0),(0,1),(1,0),(1,1),(1,2)]:
        n=max(i,j)+1
        for facet in [(F(3,2),F(0)),(F(5,4),F(1,2)),(F(1,2),F(1))]:
            for rest in product(['A','B','ab','ba'],repeat=n-1):
                states=('ab',)+rest;A,b,c=model(i,j,facet,states)
                q=linprog(c,A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),bounds=(0,None),method='highs')
                case={'i':i,'j':j,'facet':list(map(str,facet)),'states':states}
                if q.status==0 and q.x[-1]>1e-8:
                    case.update(status='COUNTEREXAMPLE',margin=q.x[-1],values=q.x.tolist())
                    print(case,flush=True);results.append(case)
                elif q.status==0:
                    y=[F(float(v)).limit_denominator(10**6) for v in q.ineqlin.marginals]
                    ok=all(v<=0 for v in y) and sum(v*w for v,w in zip(y,b))>=0 and all(F(c[k])-sum(y[l]*A[l][k] for l in range(len(A)))>=0 for k in range(len(c)))
                    case.update(status='EXACT_ZERO_DUAL' if ok else 'UNCERTIFIED_ZERO',dual=list(map(str,y)));results.append(case)
                elif q.status==2:
                    mat=np.array(A,dtype=float);bv=np.array(b,dtype=float)
                    cert=linprog(np.zeros(len(A)),A_ub=np.vstack([mat.T,-bv[None,:]]),
                                 b_ub=np.r_[np.zeros(len(c)),-1],bounds=[(None,0)]*len(A),method='highs')
                    if cert.status!=0:raise ValueError('Farkas discovery failed')
                    y=[F(float(v)).limit_denominator(10**6) for v in cert.x]
                    assert all(v<=0 for v in y)
                    assert sum(v*w for v,w in zip(y,b))>0
                    assert all(sum(y[l]*A[l][k] for l in range(len(A)))<=0 for k in range(len(c)))
                    case.update(status='EXACT_INFEASIBLE_DUAL',dual=list(map(str,y)));results.append(case)
                else:raise ValueError(q.message)
    Path('logs/astra_two_type_dichotomy.json').write_text(json.dumps(results,indent=1))
    from collections import Counter
    print(Counter(r['status'] for r in results),flush=True)


if __name__=='__main__':main()
