"""Independent exact audit of the one-step partner-budget obstruction.

This is a limitation of that necessary-condition test, not a lower bound
above 3/4 for (7,2)-families. An actual bad pair is checked as well.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from p644_support_capacity_check import check_record


def run():
    root=Path(__file__).parent/'logs';menu=json.loads((root/'astra_two_part_gap_central/templates.json').read_text())
    data=json.loads((root/'astra_partner_budget_barrier.json').read_text());seen=set();counts={}
    for entry in data['certificates']:
        key=entry['template'];assert key in menu and key not in seen;seen.add(key)
        item=menu[key];parents=item['parents'];assert all(a|b!=127 for a in parents for b in parents)
        shape,_=check_record(item['record'],parents)
        rows=[];bounds=[]
        for coordinate in range(6):
            rows.append([Q(i==coordinate) for i in range(6)]);bounds.append(Q(4,5))
        rows.extend([[1,1,1,0,0,0],[-1,-1,-1,0,0,0],[0,0,0,-1,-1,-1]])
        bounds.extend([Q(1),Q(-1),-Q(33,20)])
        for coordinate in range(3):
            for u,v in shape:
                rows.append([v if i==coordinate else u if i==coordinate+3 else Q(0) for i in range(6)])
                bounds.append(Q(4,5))
        dual={i:Q(v) for i,v in entry['dual']};assert len(dual)==len(entry['dual'])
        assert all(0<=i<len(rows) and v<0 for i,v in dual.items())
        combined=[sum(v*rows[i][j] for i,v in dual.items()) for j in range(6)]
        value=sum(v*bounds[i] for i,v in dual.items());assert value==Q(entry['certified_lower_bound'])
        if entry['kind']=='infeasible':assert all(v<=0 for v in combined) and value>0
        else:assert entry['kind']=='bound' and all(v<=(-1 if j==0 else 0) for j,v in enumerate(combined)) and value>=-Q(8,15)
        counts[entry['kind']]=counts.get(entry['kind'],0)+1
    assert seen==set(menu) and len(seen)==42
    threshold=Q(27,50);cap=Q(4,5)
    assert threshold>Q(8,15) and threshold>Q(4,7)*cap
    assert 3*cap-max(Q(1),3*threshold)==Q(39,50)>Q(3,4)
    a=[threshold,Q(23,100),Q(23,100)];b=[Q(23,100),threshold,Q(23,100)]
    target=tuple([(Q(1,2),Q(1)),(Q(9,8),Q(3,4)),(Q(5,4),Q(1,2)),(Q(4,3),Q(0))])
    witnesses=[]
    for key,item in menu.items():
        if tuple(tuple(map(Q,q)) for q in item['record']['vertices'])==target:witnesses.append(key)
    assert witnesses and sum(a)==sum(b)==1 and max(a)==max(b)==threshold
    costs=[max(u*s+v*t for u,v in target) for s,t in zip(a,b)]
    assert max(costs)<cap
    print('PASS: all 42 exact partner-box duals',counts,'coordinate bound 8/15; obstruction coefficient 39/50; actual bad pair via W',witnesses,'with costs',list(map(str,costs)),flush=True)


if __name__=='__main__':run()
