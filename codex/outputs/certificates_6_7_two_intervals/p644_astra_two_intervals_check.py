"""Independent exact two-interval certificate replay; standard library only.

Reconstruct the complete endpoint/intersection/template-failure case split,
derive every matrix from affine functions, and check rational LP duals.
Read with the two-part, two-convex-component hand reduction in note_644.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import json


def values(case,v):
    x,y,l,a,b,c,g=v
    out=[g-1,l-a,a-b,b-c,c-1,c-x,1-l-y,
         7*a+4*y+g-7,4*x-7*b+g,F(7,4)-x-y-a+b+g]
    out+=([l] if case['left_zero'] else [g-l,F(3,4)+l-x+g])
    out+=([1-c] if case['right_one'] else [c+g-1,F(7,4)-y-c+g])
    f1,f2=case['failures']
    out.append(a+6*c+4*y+g-7 if f1=='low' else 4*x-l-6*b+g)
    out.append(c+6*a+4*y+g-7 if f2=='low' else 4*x-b-6*l+g)
    inter=case['intersection']
    if inter=='small':out.append(x+y+g-2)
    else:
        out.append(2-x-y)
        for low,high,side in zip([2*l,l+b,2*b],[2*a,a+c,2*c],inter):
            out.append(high+y+g-2 if side=='low' else x-low+g)
    if 'strip_failure' in case:
        side,li,ui=case['strip_failure']
        if side=='left':assert case['left_zero'];xx,yy,aa,bb=x,y,a,b
        else:assert case['right_one'];xx,yy,aa,bb=y,x,1-b,1-a
        lower=[1-2*yy/3,(7-4*yy-2*bb)/5,3-2*yy-2*bb]
        upper=[aa,2*xx/3,(4*xx-2*bb)/5,2*xx-2*bb]
        out.append(upper[ui]-lower[li]+g)
    return out


def expected_cases():
    cases=[]
    for zero,one in product([False,True],repeat=2):
        for failures in product(['low','high'],repeat=2):
            for inter in ['small']+list(product(['low','high'],repeat=3)):
                case={'left_zero':zero,'right_one':one,'failures':failures,'intersection':inter}
                expand=failures==('high','low') and (
                    (zero and not one and inter in ['small',('low','low','high')]) or
                    (one and not zero and inter in ['small',('low','high','high')]))
                if expand:
                    for li,ui in product(range(3),range(4)):
                        cases.append({**case,'strip_failure':('left' if zero else 'right',li,ui)})
                else:cases.append(case)
    assert len(cases)==188
    return cases


def main():
    records=json.loads((Path(__file__).parent/'logs/astra_two_intervals_certificate.json').read_text())
    def key(c):return json.dumps(c,sort_keys=True,separators=(',',':'))
    expected={key(c):c for c in expected_cases()}
    assert len(records)==len(expected)==188
    assert {key(r['case']) for r in records}==set(expected)
    counts=Counter()
    for record in records:
        case=record['case'];zero=[F(0)]*7;constants=values(case,zero)
        columns=[]
        for j in range(7):
            e=list(zero);e[j]=F(1)
            columns.append([u-v for u,v in zip(values(case,e),constants)])
        A=list(zip(*columns));rhs=[-v for v in constants]
        dual=list(map(F,record['dual']));assert len(dual)==len(A)
        assert all(v<=0 for v in dual)
        lhs=[sum(y*r[j] for y,r in zip(dual,A)) for j in range(7)]
        bound=sum(y*b for y,b in zip(dual,rhs))
        status=record['status'];counts[status]+=1
        if status=='EXACT_ZERO_DUAL':assert bound>=0 and all(v<=(-1 if j==6 else 0) for j,v in enumerate(lhs))
        else:assert status=='EXACT_INFEASIBLE_DUAL' and bound>0 and max(lhs)<=0
    assert counts=={'EXACT_INFEASIBLE_DUAL':167,'EXACT_ZERO_DUAL':21}
    ex=json.loads((Path(__file__).parent/'logs/astra_two_intervals_example.json').read_text())
    capacities=list(map(F,ex['capacities']));types=list(map(F,ex['row_types']))
    parts=[{int(m):F(v) for m,v in p.items()} for p in ex['parts']]
    assert capacities==[F(1,2),F(181,122)] and types==[F(41,122)]*2+[F(1,10)]*5
    occupied=set()
    for i,part in enumerate(parts):
        assert all(0<=m<=127 and v>0 for m,v in part.items())
        assert sum(part.values())<=capacities[i]
        for j in range(7):
            assert sum(v for m,v in part.items() if m>>j&1)==(types[j] if i==0 else 1-types[j])
        occupied.update(m for m in part if m)
    assert all(a|b!=127 for a in occupied for b in occupied)
    assert all((v*ex['integral_scale']).denominator==1 for part in parts for v in part.values())
    assert all((v*ex['integral_scale']).denominator==1 for v in capacities)
    x,y=capacities;a=F(29,244);b=F(41,122)
    assert x+y<2 and 0<F(1,10)<a<b
    assert min(x+y-1+a-b,y-1+b)==F(ex['transversal_coefficient'])==F(187,244)>F(3,4)
    assert max(x,y-1+a,min(x+y-1-b,y-1+b))==F(ex['two_type_upper'])==F(79,122)<F(3,4)
    print('PASS: all188endpoint/intersection/template cases;167exact infeasibility duals and21exact nonpositive-margin duals')
    print('CERTIFICATE: an intersecting two-part family with two convex type intervals and tau*>3/4 has a bad seven-tuple, with the hand reduction')
    print('PASS: explicit rational bad tuple; exact row and part masses, pair obstruction, and integer scale',ex['integral_scale'])
    print('SCOPE: two parts; arbitrary part capacities. More than two parts and the general3/4problem remain open.')


if __name__=='__main__':main()
