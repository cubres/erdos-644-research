"""Explore two convex type intervals over two parts.

Discovery with exact rational dual recovery. No theorem unless every case
is closed and the reduction and an independent replay are supplied.
COUNTEREXAMPLE denotes a failure of a proposed template condition, never a
counterexample to Erdős Problem644. The complete intersecting proof is now
Theorem7.54 in note_644.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,numpy as np
from scipy.optimize import linprog


def model(left_zero,right_one,failures,intersection=None,pure_failure=None,strip_failure=None):
    # x,y are part capacities; [l,a] and [b,c] are the type intervals.
    x,y,l,a,b,c,g=range(7);rows=[];rhs=[]
    def add(d,v):
        r=[F(0)]*7
        for k,w in d.items():r[k]+=F(w)
        rows.append(r);rhs.append(F(v))
    add({g:1},1);add({l:1,a:-1},0);add({a:1,b:-1},0);add({b:1,c:-1},0);add({c:1},1)
    add({c:1,x:-1},0);add({l:-1,y:-1},-1)
    # No homogeneous Fano tuple: the first interval is below, the second above.
    add({a:7,y:4,g:1},7);add({x:4,b:-7,g:1},0)
    # The central empty interval gives a transversal of this infimum cost.
    add({x:-1,y:-1,a:-1,b:1,g:1},-F(7,4))
    if left_zero:add({l:1},0)
    else:
        add({l:-1,g:1},0);add({l:1,x:-1,g:1},-F(3,4))
    if right_one:add({c:-1},-1)
    else:
        add({c:1,g:1},1);add({y:-1,c:-1,g:1},-F(7,4))
    # Failure of M1(left,right) and M1(right,left).
    for orient,fail in enumerate(failures):
        if orient==0:lower={l:1,b:6};upper={a:1,c:6}
        else:lower={b:1,l:6};upper={c:1,a:6}
        if fail=='low':add({**upper,y:4,g:1},7)
        else:add({**{k:-v for k,v in lower.items()},x:4,g:1},0)
    if intersection is not None:
        # Either the ground set has size<2 (all pairs intersect), or each
        # interval of sums lies strictly below2-y or strictly above x.
        if intersection=='small':add({x:1,y:1,g:1},2)
        else:
            add({x:-1,y:-1},-2)
            for low,high,side in zip([{l:2},{l:1,b:1},{b:2}],[{a:2},{a:1,c:1},{c:2}],intersection):
                if side=='low':add({**high,y:1,g:1},2)
                else:add({**{k:-v for k,v in low.items()},x:1,g:1},0)
    if pure_failure is not None:
        # M5(0,b) needs y>=max(3/2,7/4-b/2); its other-part
        # inequalities follow from type feasibility. Reflect for c=1.
        side,facet=pure_failure
        if side=='left':
            assert left_zero
            if facet==0:add({y:1,g:1},F(3,2))
            else:add({y:1,b:F(1,2),g:1},F(7,4))
        else:
            assert right_one
            if facet==0:add({x:1,g:1},F(3,2))
            else:add({x:1,a:-F(1,2),g:1},F(5,4))
    if strip_failure is not None:
        side,li,ui=strip_failure
        if side=='left':assert left_zero
        else:assert right_one
        lower=[(F(1),{y:-F(2,3)}),(F(7,5),{y:-F(4,5),b:-F(2,5)}),(F(3),{y:-2,b:-2})]
        upper=[(F(0),{a:1}),(F(0),{x:F(2,3)}),(F(0),{x:F(4,5),b:-F(2,5)}),(F(0),{x:2,b:-2})]
        def reflect(form):
            const,coeff=form;out={}
            if side=='left':return const,coeff
            for k,v in coeff.items():
                if k in [x,y]:j=y if k==x else x;out[j]=out.get(j,F(0))+v
                else:
                    assert k in [a,b];j=b if k==a else a;const+=v;out[j]=out.get(j,F(0))-v
            return const,out
        lc,lr=reflect(lower[li]);uc,ur=reflect(upper[ui]);row={g:1}
        for k,v in ur.items():row[k]=row.get(k,F(0))+v
        for k,v in lr.items():row[k]=row.get(k,F(0))-v
        add(row,lc-uc)
    return rows,rhs,[0]*6+[-1]


def solve_case(args):
    A,b,c=model(**args);mat=np.array(A,dtype=float);bv=np.array(b,dtype=float)
    q=linprog(c,A_ub=mat,b_ub=bv,bounds=(0,None),method='highs')
    if q.status==0 and q.x[-1]>1e-8:
        v=[F(float(z)).limit_denominator(10**6) for z in q.x]
        assert min(v)>=0 and all(sum(aa*bb for aa,bb in zip(r,v))<=s for r,s in zip(A,b))
        return {'status':'COUNTEREXAMPLE','values':list(map(str,v))}
    if q.status==0:
        dual=[F(float(z)).limit_denominator(10**6) for z in q.ineqlin.marginals]
        assert all(z<=0 for z in dual) and sum(z*w for z,w in zip(dual,b))>=0
        assert all(sum(z*r[j] for z,r in zip(dual,A))<=c[j] for j in range(7))
        return {'status':'EXACT_ZERO_DUAL','dual':list(map(str,dual))}
    assert q.status==2,q.message
    w=linprog(np.zeros(len(A)),A_ub=np.vstack([mat.T,-bv[None,:]]),b_ub=np.r_[np.zeros(7),-1],bounds=[(None,0)]*len(A),method='highs')
    assert w.status==0
    dual=[F(float(z)).limit_denominator(10**6) for z in w.x]
    assert all(z<=0 for z in dual) and sum(z*v for z,v in zip(dual,b))>0
    assert all(sum(z*r[j] for z,r in zip(dual,A))<=0 for j in range(7))
    return {'status':'EXACT_INFEASIBLE_DUAL','dual':list(map(str,dual))}


def run():
    records=[]
    for zero,one,fails in product([False,True],[False,True],product(['low','high'],repeat=2)):
        for inter in ['small']+list(product(['low','high'],repeat=3)):
            case={'left_zero':zero,'right_one':one,'failures':fails,'intersection':inter}
            q=solve_case(case);records.append({'case':case,**q})
            if q['status']=='COUNTEREXAMPLE':print(case,q,flush=True)
    from collections import Counter
    print(Counter(q['status'] for q in records),flush=True)
    Path('logs/astra_two_intervals_m1.json').write_text(json.dumps(records,indent=1))
    proof=[]
    for record in records:
        if record['status']!='COUNTEREXAMPLE':proof.append(record);continue
        case=record['case'];side='left' if case['left_zero'] else 'right'
        for li,ui in product(range(3),range(4)):
            subcase={**case,'strip_failure':(side,li,ui)}
            q=solve_case(subcase);proof.append({'case':subcase,**q})
            if q['status']=='COUNTEREXAMPLE':print('STILL OPEN',subcase,q,flush=True)
    print('COMPLETE MENU',Counter(q['status'] for q in proof),flush=True)
    Path('logs/astra_two_intervals_certificate.json').write_text(json.dumps(proof,indent=1))


if __name__=='__main__':run()
