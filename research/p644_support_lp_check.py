"""Exact, standard-library checks for the complete bad-support LP pipeline.

The supporting catalogue is independently certified by
p644_support_catalog_check.py. No floating-point status is a certificate here.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import json


def rational_instance(instance):
    x=list(map(F,instance['capacities']))
    boxes=[(list(map(F,b[0])),list(map(F,b[1]))) for b in instance['boxes']]
    rank=F(instance['rank']);p=len(x)
    assert rank>0 and all(a>0 for a in x) and len(boxes)==2
    for lo,hi in boxes:
        assert len(lo)==len(hi)==p
        assert all(0<=a<=b<=c for a,b,c in zip(lo,hi,x))
        assert sum(lo)<=rank<=sum(hi)
    return x,boxes,rank


def permutation_maps():
    return [[sum(1<<perm[i] for i in range(7) if m>>i&1) for m in range(128)]
            for perm in permutations(range(7))]


def colour_representatives(parents, maps):
    target=set(parents)
    actions=[a for a in maps if all(a[m] in target for m in parents)]
    assert actions
    todo=set(range(128));reps=[]
    while todo:
        c=min(todo);reps.append(c);todo.difference_update(a[c] for a in actions)
    return reps


def matrix(parents,p):
    """A v <= b with nonnegative parent masses and row excesses above lo.

    Rows, in order: capacity and seven cover rows for each part; all upper
    bounds on row excesses; two rank inequalities for every row.
    """
    nparent=len(parents);n=p*(nparent+7);rows=[]
    w=lambda i,j:p*nparent+7*i+j
    for i in range(p):
        rows.append({i*nparent+t:1 for t in range(nparent)})
        for j in range(7):
            row={i*nparent+t:-1 for t,m in enumerate(parents) if m>>j&1}
            row[w(i,j)]=1;rows.append(row)
    for i in range(p):
        for j in range(7):rows.append({w(i,j):1})
    for j in range(7):
        rows.append({w(i,j):1 for i in range(p)})
        rows.append({w(i,j):-1 for i in range(p)})
    return rows,n


def rhs(instance,colour):
    x,boxes,rank=rational_instance(instance);p=len(x);b=[]
    for i in range(p):
        b.append(x[i]);b.extend(-boxes[colour>>j&1][0][i] for j in range(7))
    for i in range(p):
        for j in range(7):
            lo,hi=boxes[colour>>j&1];b.append(hi[i]-lo[i])
    for j in range(7):
        v=rank-sum(boxes[colour>>j&1][0]);b.extend([v,-v])
    return b


def check_primal(rows,b,values,n):
    assert len(values)==n and all(v>=0 for v in values)
    assert len(rows)==len(b)
    assert all(sum(a*values[j] for j,a in row.items())<=c for row,c in zip(rows,b))


def check_dual(rows,b,values,n):
    assert len(values)==len(rows) and all(v<=0 for v in values)
    total=[F(0)]*n
    for row,y in zip(rows,values):
        for j,a in row.items():total[j]+=a*y
    assert all(v<=0 for v in total)
    value=sum(a*v for a,v in zip(b,values));assert value>0
    return value


def trimmed_cells(instance,parents,colour,values):
    """Realize exact row sizes by splitting parent cells and trimming rows."""
    x,boxes,rank=rational_instance(instance);p=len(x);q=len(parents);out=[]
    for i in range(p):
        cells={m:values[i*q+t] for t,m in enumerate(parents) if values[i*q+t]>0}
        for j in range(7):
            wanted=boxes[colour>>j&1][0][i]+values[p*q+7*i+j]
            excess=sum(v for m,v in cells.items() if m>>j&1)-wanted
            assert excess>=0
            for m in sorted(list(cells)):
                if not excess:break
                if not m>>j&1:continue
                amount=min(excess,cells[m]);cells[m]-=amount
                smaller=m^(1<<j);cells[smaller]=cells.get(smaller,F(0))+amount
                excess-=amount
            assert excess==0
        assert sum(cells.values())<=x[i]
        out.append({m:v for m,v in cells.items() if m and v})
    occupied=set().union(*(set(c) for c in out))
    assert all(a|b!=127 for a in occupied for b in occupied)
    for j in range(7):
        loads=[sum(v for m,v in cells.items() if m>>j&1) for cells in out]
        lo,hi=boxes[colour>>j&1]
        assert sum(loads)==rank and all(a<=v<=b for a,v,b in zip(lo,loads,hi))
    return [{str(m):str(v) for m,v in sorted(c.items())} for c in out]


def check_certificate(path,catalogue):
    cert=json.loads(Path(path).read_text());data=json.loads(Path(catalogue).read_text())
    instance=cert['instance'];p=len(instance['capacities']);rational_instance(instance)
    supports={q['truth_table']:q for q in data['orbits']}
    if cert['status']=='BAD_TUPLE':
        item=supports[cert['truth_table']];parents=item['maximal_cells']
        rows,n=matrix(parents,p);b=rhs(instance,cert['colour']);v=list(map(F,cert['primal']))
        check_primal(rows,b,v,n)
        cells=trimmed_cells(instance,parents,cert['colour'],v)
        assert cells==cert['trimmed_cells']
        print('PASS: exact bad seven-tuple, with explicitly trimmed cells.',flush=True)
        return
    assert cert['status']=='HAS_72'
    # For this unrestricted certificate every one of the 715 supports is used.
    assert len(supports)==715 and set(cert['supports'])==set(supports)
    maps=permutation_maps();checked=0
    for stem,entry in cert['supports'].items():
        parents=supports[stem]['maximal_cells'];expected=colour_representatives(parents,maps)
        rows,n=matrix(parents,p);duals=[list(map(F,d)) for d in entry['duals']]
        assert set(map(int,entry['colours']))==set(expected)
        for c in expected:
            d=duals[entry['colours'][str(c)]];check_dual(rows,rhs(instance,c),d,n);checked+=1
    print('PASS: all 715 supports and',checked,'component assignments have exact Farkas certificates.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('certificate')
    parser.add_argument('--catalogue',default=str(Path(__file__).parent/'logs/astra_full_support_catalog.json'))
    args=parser.parse_args();check_certificate(args.certificate,args.catalogue)
