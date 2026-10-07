"""Independent exact mathematical audit of a continuous type-cell SAT input.

The SAT proof is a separate dependency. No discovery module or numerical
library is imported. All cells, box clauses, pair exclusions and multi-type
region exclusions are reconstructed from rational definitions.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import json
from p644_support_capacity_check import check_record

LINES=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))


def audited_shapes(path):
    table=json.loads(path.read_text());result=[]
    for item in table.values():
        parents=item['parents'];assert all(0<a<127 for a in parents)
        assert all(a|b!=127 for a,b in product(parents,repeat=2))
        shape,_=check_record(item['record'],parents)
        for swap in (False,True):
            facets=[]
            for u,v in shape:
                if swap:u,v=v,u
                assert u>=0 and v>=0
                den=u.denominator*v.denominator//gcd(u.denominator,v.denominator)
                facets.append((int(u*den),int(v*den),den))
            result.append(facets)
    return result


def reconstruct_cells(r,caps):
    found={}
    for i,j in product(range(r),repeat=2):
        for verts in (((i,j,r-i-j),(i+1,j,r-i-j-1),(i,j+1,r-i-j-1)),
                      ((i+1,j,r-i-j-1),(i,j+1,r-i-j-1),(i+1,j+1,r-i-j-2))):
            if not all(all(0<=a<=x for a,x in zip(v,caps)) for v in verts):continue
            lo=tuple(min(v[h] for v in verts) for h in range(3));hi=tuple(max(v[h] for v in verts) for h in range(3))
            if all(7*a<=4*x for a,x in zip(hi,caps)):continue
            found[lo]=hi
    return found


def partner_boxes(upper,caps,shapes):
    boxes=set()
    for shape in shapes:
        limits=[];legal=True
        for a,cap in zip(upper,caps):
            limit=cap
            for u,v,d in shape:
                if v:limit=min(limit,(d*cap-u*a)//v)
                elif u*a>d*cap:legal=False;break
            if limit<0:legal=False
            limits.append(limit)
        if legal:boxes.add(tuple(limits))
    return [b for b in boxes if not any(b!=c and all(x<=y for x,y in zip(b,c)) for c in boxes)]


def expected_clauses(data,shapes):
    r=data['rank'];caps=data['capacities'];T=Q(data['threshold']);assert T.denominator==1
    nodes=[(tuple(lo),tuple(hi)) for lo,hi in data['cells']];n=len(nodes)
    expected=reconstruct_cells(r,caps)
    assert len(nodes)==len(expected) and len({lo for lo,hi in nodes})==n
    assert all(expected[lo]==hi for lo,hi in nodes)
    boxes={u for u in product(*[range(x+1) for x in caps]) if sum(u)==sum(caps)-T}
    assert boxes=={tuple(u) for u in data['boxes']} and len(boxes)==len(data['boxes'])
    for box in data['boxes']:
        # The section l<=a<=h, sum(a)=r meets a<=box exactly under these conditions.
        yield [j+1 for j,(lo,hi) in enumerate(nodes)
               if all(a<=b for a,b in zip(lo,box)) and sum(min(a,b) for a,b in zip(hi,box))>=r]
    assert not data['lazy']
    for i,(_,upper) in enumerate(nodes):
        boxes=partner_boxes(upper,caps,shapes)
        for j in range(i,n):
            if any(all(a<=b for a,b in zip(nodes[j][1],box)) for box in boxes):yield [-i-1,-j-1]
    nextvar=n;registry={}
    for entry in data['fano_clauses']:
        bounds=[tuple(map(Q,b)) for b in entry['bounds']];assignment=entry['assignment'];q=len(bounds)
        assert len(assignment)==7 and set(assignment)==set(range(q))
        assert all(v>=0 for b in bounds for v in b)
        if entry['kind']=='fano':
            for i,cap in enumerate(caps):
                row=[bounds[j][i] for j in assignment]
                assert max(row)<=cap and sum(row)<=4*cap
                assert all(sum(row[j] for j in line)<=2*cap for line in LINES)
        else:
            assert entry['kind']=='parents';parents=entry['parents'];weights=[list(map(Q,w)) for w in entry['weights']]
            assert all(0<a<127 for a in parents) and all(a|b!=127 for a,b in product(parents,repeat=2))
            assert len(weights)==3
            for i,(w,cap) in enumerate(zip(weights,caps)):
                assert len(w)==len(parents) and min(w)>=0 and sum(w)<=cap
                for row,j in enumerate(assignment):assert sum(v for v,m in zip(w,parents) if m>>row&1)>=bounds[j][i]
        regions=[[j for j,(_,hi) in enumerate(nodes) if all(a<=b for a,b in zip(hi,bound))] for bound in bounds]
        assert regions==entry['regions']
        rvars=[]
        for region in regions:
            key=tuple(region)
            if key not in registry:
                nextvar+=1;registry[key]=nextvar
                for cell in region:yield [-cell-1,nextvar]
            rvars.append(registry[key])
        assert rvars==entry['region_variables'];yield [-v for v in rvars]


def check(base,templates):
    base=Path(base);data=json.loads(base.with_suffix('.json').read_text());shapes=audited_shapes(Path(templates))
    assert data['sat'] is False
    with base.with_suffix('.cnf').open() as cnf:
        header=cnf.readline().split();assert header[:2]==['p','cnf'];nv,nc=map(int,header[2:]);count=0
        for expected in expected_clauses(data,shapes):
            line=list(map(int,cnf.readline().split()));assert line and line[-1]==0
            assert line[:-1]==expected,('clause mismatch',count)
            assert all(0<abs(v)<=nv for v in expected);count+=1
        assert count==nc and not cnf.read().strip()
    print('PASS: exact continuous-cell input audit;',len(data['cells']),'triangles;',len(data['boxes']),
          'residual queries;',len(data['fano_clauses']),'multi-type regions;',count,'CNF clauses. SAT proof remains a separate check.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('--templates',default='logs/astra_two_part_gap_central/templates.json');args=p.parse_args()
    check(args.base,args.templates)
