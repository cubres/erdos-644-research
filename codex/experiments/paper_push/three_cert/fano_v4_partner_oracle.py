"""Exact Fano/V4 one-response terminal oracle for finitely many known types.

Fano row6 is the response U (the automorphism group is transitive on rows).
The six other rows use known unit types, with repetition. All arithmetic in
capacity generation, downbox union, escape orthants, and requests is rational.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
from v4_escape_boxes import v4_cap,maximal_boxes,escape_orthants,best_free_box
LINES=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
PENCILS=tuple(tuple(l for l,L in enumerate(LINES) if q in L) for q in range(7))
FREE=6
ANCHOR_PENCILS=tuple(p for p in PENCILS if FREE not in p)
RESPONSE_PAIRS=tuple(tuple(l for l in p if l!=FREE) for p in PENCILS if FREE in p)

def fano_cap(x,types,assignment):
    assert len(assignment)==6
    rows=[types[j] for j in assignment]
    if any(sum(rows[j][i] for j in p)>2*x[i] for p in ANCHOR_PENCILS for i in range(3)):
        return None
    return tuple(min([x[i],4*x[i]-sum(row[i] for row in rows)]+[2*x[i]-sum(rows[j][i] for j in p) for p in RESPONSE_PAIRS]) for i in range(3))

def candidates(x,types):
    out={}
    for roles in product(range(len(types)),repeat=3):
        cap=v4_cap(x,*(types[j] for j in roles))
        if min(cap)>=0 and sum(cap)>=1:out.setdefault(cap,{'kind':'V4','roles':roles})
    for assignment in product(range(len(types)),repeat=6):
        cap=fano_cap(x,types,assignment)
        if cap is not None and min(cap)>=0 and sum(cap)>=1:
            out.setdefault(cap,{'kind':'FANO','assignment':assignment})
    return out

def analyse(x,types):
    x=tuple(map(F,x));types=[tuple(map(F,t)) for t in types]
    assert len(x)==3
    assert all(sum(t)==1 and all(0<=t[i]<=x[i] for i in range(3)) for t in types)
    boxes=maximal_boxes(candidates(x,types));corners=escape_orthants(x,boxes)
    cost,u,attained=best_free_box(x,corners)
    if cost>sum(x)-1:cost=sum(x)-1;u=None;attained=False
    out={'capacities':x,'types':types,'boxes':boxes,'escape_corners':corners,
         'request_cost':cost,'retained_box':u,'closed_box_free':attained,
         'closes_at_three_quarters':cost<=F(3,4)}
    check_result(out)
    return out

def check_result(r):
    x,types=r['capacities'],r['types']
    for cap,info in r['boxes']:
        expected=(v4_cap(x,*(types[i] for i in info['roles'])) if info['kind']=='V4'
                  else fano_cap(x,types,info['assignment']))
        assert cap==expected and min(cap)>=0 and sum(cap)>=1
    assert r['escape_corners']==escape_orthants(x,r['boxes'])
    u=r['retained_box']
    if u is None:assert r['request_cost']==sum(x)-1 and not r['closed_box_free'];return
    assert all(0<=v<=cap for v,cap in zip(u,x))
    assert r['request_cost']==sum(x)-sum(u)
    # An exact closed request excludes each surviving escape orthant. The
    # infimal alternative permits infinitesimal decreases at positive bounds.
    if r['closed_box_free']:
        assert all(any(v<low or (v==low and strict) for v,(low,strict) in zip(u,c)) for c in r['escape_corners'])
    else:
        assert all(any(v<low or (v==low and (strict or low>0)) for v,(low,strict) in zip(u,c)) for c in r['escape_corners'])

def encoded(r):return json.dumps(r,default=str,indent=2)
if __name__=='__main__':
    p=Path(sys.argv[1]);d=json.loads(p.read_text());r=analyse(d['capacities'],d['types'])
    out=p.with_name(p.stem+'.fano_v4_partner.json');out.write_text(encoded(r)+'\n')
    print('EXACT',len(r['boxes']),'maximal boxes',len(r['escape_corners']),'escape orthants; cost',r['request_cost'],'closed',r['closed_box_free'])
    print('retained',r['retained_box']);print(out)
