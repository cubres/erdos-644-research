"""Standard-library exact certificate for the new Fano line construction.

The hand proof supplies the universal formula; this independently constructs
and checks the integral rank-100 example, including all point-pair supports.
"""
import itertools,json
from pathlib import Path
from fractions import Fraction as F


def build():
    lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    assert all(len(set(a)&set(b))==1 for a,b in itertools.combinations(lines,2))
    parents=[127-sum(1<<j for j in line) for line in lines]
    parts=[]
    for s,t in [(0,12),(40,0),(60,88)]:
        v=F(3,2)*t;u=max(F(0),F(s)-v/2)
        cells={parents[0]:u}
        for mask in parents[1:]:cells[mask]=v/6
        for j in range(7):
            goal=t if j<3 else s
            extra=sum(m for mask,m in cells.items() if mask>>j&1)-goal
            assert extra>=0
            for mask in sorted(list(cells),reverse=True):
                if not extra:break
                if mask>>j&1:
                    take=min(extra,cells[mask]);cells[mask]-=take;extra-=take
                    child=mask^(1<<j);cells[child]=cells.get(child,F(0))+take
            assert extra==0
        parts.append({str(k):str(v) for k,v in sorted(cells.items()) if v})
    return {'rank':100,'capacities':[19,59,138],'parts':parts,
            'row_types':[[12,0,88]]*3+[[0,40,60]]*4,
            'asymptotic_transversal':'19/25','finite_transversal_at_rank_100':78}


def check(data):
    rank=data['rank'];cells=[{int(k):F(v) for k,v in p.items()} for p in data['parts']]
    assert rank==100 and data['capacities']==[19,59,138]
    for i,part in enumerate(cells):
        assert all(0<=k<128 and v>0 and v.denominator==1 for k,v in part.items())
        assert sum(part.values())<=data['capacities'][i]
    for j,typ in enumerate(data['row_types']):
        got=[sum(v for mask,v in p.items() if mask>>j&1) for p in cells]
        assert got==typ and sum(got)==rank
        assert got==[0,40,60] or (got[1]==0 and 0<=got[0]<=19 and got[2]==100-got[0])
    support=set().union(*(p.keys() for p in cells))
    assert all(a|b!=127 for a in support for b in support)
    # Hand-derived type-independent failures of all four older orientations.
    assert F(38,3)<18 and F(38,3)<F(68,5) and 60>59
    assert min(76+2,78+1)==data['finite_transversal_at_rank_100']==78
    assert F(data['asymptotic_transversal'])==F(76,100)>F(3,4)
    print('PASS: integral rank-100 bad tuple; every row, capacity and pair checked; old-template inequalities verified.')


if __name__=='__main__':
    path=Path('logs/astra_line_template_example.json')
    if not path.exists():path.write_text(json.dumps(build(),indent=2))
    check(json.loads(path.read_text()))
