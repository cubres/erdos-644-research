"""Independent exact LP dual for the balanced first-response obstruction."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json


def check():
    labels=list(combinations(range(6),3))
    points=[sum(1<<j for j in S)|(64 if copy==0 else 0) for S in labels for copy in range(2)]
    target=sum(1<<j for j in (0,1,2,3,6))
    edges=[(i,j) for i,j in combinations(range(40),2) if (points[i]|points[j])&target==target]
    assert len(edges)==138;nv=40+len(edges);rows=[];rhs=[]
    for number,(i,j) in enumerate(edges):
        for endpoint in (i,j):rows.append({40+number:1,endpoint:-1});rhs.append(0)
    rows.append({i:1 for i in range(40)});rhs.append(20)
    for i in range(nv):rows.append({i:1});rhs.append(1)
    data=json.loads((Path(__file__).parent/'logs/astra_balanced_pair_exchange_dual.json').read_text())
    dual={i:Q(v) for i,v in data['dual']}
    assert len(dual)==len(data['dual']) and all(0<=i<len(rows) and v>0 for i,v in dual.items())
    total=[Q(0)]*nv
    for i,v in dual.items():
        for j,a in rows[i].items():total[j]+=v*a
    assert all(total[j]>=(1 if j>=40 else 0) for j in range(nv))
    value=sum(v*rhs[i] for i,v in dual.items());assert value==Q(data['upper'])==Q(315,4)
    assert (138-value)/4==Q(237,16)>10
    print('PASS: 138-edge graph reconstructed; exact LP upper315/4; after scaling, every second response has Q>=237m^2/16>10m^2 in the four-old-row cases.')


if __name__=='__main__':check()
