"""Independent exact replay of whole-cell first-request response obstructions.

Reconstructs all five edges, verifies gaps and minimum-sum restrictions, and
uses the independently written two-cover formula on the actual positive cells.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
from p644_pair_cover_check import concept_cost


def check(path):
    data=json.loads(Path(path).read_text());budget=F(data['budget']);items=data['results']
    masses=list(map(F,items[0]['masses']));masks=items[0]['masks'];n=len(masses)
    expected={s for s in range(1<<n) if sum(v for i,v in enumerate(masses) if s>>i&1)<=budget
              and all(masses[i]>0 for i in range(n) if s>>i&1)}
    assert len(expected)==data['legal_requests']
    found=set();best=None
    for entry in items:
        assert entry['status']=='sat' and entry['request'] not in found
        request=entry['request'];found.add(request);h=list(map(F,entry['response']))
        assert entry['masks']==masks and list(map(F,entry['masses']))==masses
        assert request in expected and len(h)==n and sum(h)<=500
        assert all(0<=v<=m and (not request>>i&1 or v==0) for i,(v,m) in enumerate(zip(h,masses)))
        cells=[]
        for mask,m,v in zip(masks,masses,h):
            if m-v>0:cells.append((mask,m-v))
            if v>0:cells.append((mask|16,v))
        if sum(h)<500:cells.append((16,500-sum(h)))
        assert all(sum(v for mask,v in cells if mask>>i&1)==500 for i in range(5))
        pairs={(i,j):sum(v for mask,v in cells if mask>>i&1 and mask>>j&1) for i,j in combinations(range(5),2)}
        assert all(v<lo or v>hi for v in pairs.values() for lo,hi in ((98,106),(F(267,2),178),(216,237)))
        for triple in combinations(range(5),3):
            if not any(all(mask>>i&1 for i in triple) for mask,v in cells):
                assert sum(pairs[i,j] for i,j in combinations(triple,2))>=429
        adj=[sum(1<<j for j,(other,w) in enumerate(cells) if i!=j and mask|other==31)
             for i,(mask,v) in enumerate(cells)]
        used=[i for i,a in enumerate(adj) if a]
        graph=[sum(1<<j for j,old in enumerate(used) if adj[i]>>old&1) for i in used]
        weights=[cells[i][1] for i in used]
        value=concept_cost(graph,weights)
        assert value==F(entry['exact_final_budget']) and value>budget
        best=value if best is None else min(best,value)
    assert found==expected
    print('PASS:',len(found),'whole-cell requests; all exact legal responses satisfy the gaps and minimum-sum bounds; minimum finishing budget',best,'>',budget)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('summary');args=parser.parse_args();check(args.summary)
