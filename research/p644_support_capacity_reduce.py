"""Exact dominance reduction of the completed two-type capacity catalogue."""
from fractions import Fraction as F
from pathlib import Path
import json


def leq(a,b):
    if any(u>b[-1][0] or v>b[0][1] for u,v in a):return False
    return all((left[1]-right[1])*u+(right[0]-left[0])*v <= (left[1]-right[1])*left[0]+(right[0]-left[0])*left[1]
               for left,right in zip(b,b[1:]) for u,v in a)


def run():
    root=Path('logs/astra_support_capacity');unique={};counts=0
    for p in root.glob('*.json'):
        if p.name=='status.json':continue
        for row in json.loads(p.read_text()):
            vertices=tuple(tuple(map(F,q)) for q in row['vertices']);unique.setdefault(vertices,(row['truth_table'],row['colour']));counts+=1
    assert counts==54214
    minimal=[]
    for f in sorted(unique,key=lambda a:sum(x+y for x,y in a)/len(a)):
        if any(leq(g,f) for g in minimal):continue
        minimal=[g for g in minimal if not leq(f,g)]+[f]
    # Every discarded function is dominated by a retained one; check directly.
    coverage={}
    for f in unique:
        index=next(i for i,g in enumerate(minimal) if leq(g,f))
        coverage[';'.join(','.join(map(str,p)) for p in f)]=index
    assert all(not leq(a,b) for i,a in enumerate(minimal) for j,b in enumerate(minimal) if i!=j)
    data={'total_assignments':counts,'distinct_functions':len(unique),'minimal_functions':[
        {'vertices':[list(map(str,p)) for p in f],'witness':unique[f]} for f in minimal],
          'dominators':coverage}
    Path('logs/astra_support_capacity_minimal.json').write_text(json.dumps(data,indent=2))
    print('PASS: exact dominance reduction:',counts,'assignments;',len(unique),'functions;',len(minimal),'minimal functions.')


if __name__=='__main__':run()
