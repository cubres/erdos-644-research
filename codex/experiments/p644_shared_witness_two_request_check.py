"""Exact two-request cover lemma for the two-parameter clean-A profile.
Standard library. Affine coefficients are(a,b,e), with a>=0 and1<=e<=b.
This checks a feasible strategy, not an optimizer lower bound.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import json

def add(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(len(vs[0])))

lines = [frozenset(t) for t in combinations(range(7), 3)
         if (t[0]+1) ^ (t[1]+1) ^ (t[2]+1) == 0]
rows = [2, 4, 5, 6]
cells = defaultdict(lambda: (0, 0))
for line in lines:
    mask = sum(1 << j for j, r in enumerate(rows) if r not in line)
    if 0 not in line:
        cells[mask] = add(cells[mask], (1, 3))
    else:
        cells[mask] = add(cells[mask], (1, 0))
        for h in sorted(set(range(7)) - line):
            mask2 = sum(1 << j for j, r in enumerate(rows) if r not in line | {h})
            cells[mask2] = add(cells[mask2], (0, 1))
expected = {1:(0,1), 2:(0,1), 3:(1,2), 5:(1,4), 6:(1,4), 8:(1,3),
            9:(0,1), 10:(0,1), 11:(1,3), 12:(0,2), 13:(1,1), 14:(1,1)}
assert dict(cells) == expected
assert 15 not in cells and 7 not in cells
# Outside0 points cannot be endpoints: the1111 type is absent. They are
# never requested and therefore need not be given any finite mass here.
allocation = {
    1:{1:(0,1,0)}, 2:{1:(0,1,0)}, 3:{1:(1,2,0)},
    5:{0:(1,4,0)}, 6:{2:(1,4,0)}, 8:{0:(1,3,0)},
    9:{2:(0,1,-1), 3:(0,0,1)}, 10:{1:(0,1,0)},
    11:{2:(1,3,0)}, 12:{1:(0,2,-1), 3:(0,0,1)},
    13:{3:(1,1,0)}, 14:{1:(1,1,0)},
}
for mask in cells:
    assert add(*allocation[mask].values()) == cells[mask] + (0,)
parts = [(s,q,v) for s,opts in allocation.items() for q,v in opts.items()]
requests = [add(*(v for s,q,v in parts if q & d)) for d in [1,2]]
assert requests == [(3,9,1), (3,9,1)]
active = [(s,q,v) for s,q,v in parts
          if any((s | t) == 15 and (q & r) == 0 for t,r,w in parts)]
endpoint = add(*(v for s,q,v in active))
assert endpoint == (3,12,-2)
# All parts nonnegative for a>=0,b>=1,0<=e<=b: check e/b=0 and1.
assert all(ca >= 0 and cb >= 0 and cb+ce >= 0 for s,q,(ca,cb,ce) in parts)
# Each witness row has rank4a+12b.
for row in range(1,7):
    rank = (0,0)
    for line in lines:
        if 0 not in line:
            if row not in line: rank = add(rank,(1,3))
        else:
            if row not in line: rank = add(rank,(1,0))
            for h in set(range(7))-line:
                if row not in line | {h}: rank = add(rank,(0,1))
    assert rank == (4,12)
# Replay the actual transport specialization a3300,b100,e1 exactly.
transport = json.loads(Path('outputs/agent_shared_witness_transport_discovery.json').read_text())
actual = defaultdict(int)
for cell in transport['cells']:
    mask = sum(bool(cell['witness_mask'] & (1 << (r-1))) << j for j,r in enumerate(rows))
    actual[mask] += cell['weight']
assert {s:w for s,w in actual.items() if s} == {s:3300*ca+100*cb for s,(ca,cb) in cells.items()}
finite = [(s,q,3300*ca+100*cb+ce) for s,q,(ca,cb,ce) in parts
          if 3300*ca+100*cb+ce > 0]
endmass = sum(w for s,q,w in finite if any((s | t) == 15 and (q & r) == 0 for t,r,ww in finite))
assert endmass == 11098
out = {
    'status':'EXACT_PASS', 'parameters':'integers a>=0,b>=1,1<=e<=b',
    'witness_profile':'four noneligible classes a+3b; three eligible bases a; twelve eligible defects b',
    'witness_row_rank':'k0=4a+12b', 'four_rows':['W2','W4','W5','W6'],
    'common_intersection':0, 'outside_zero_class':'arbitrary and irrelevant',
    'request_sizes':['3a+9b+e','3a+9b+e'],
    'residual_endpoint_upper':'3a+12b-2e',
    'global_endpoint_minimum_assumption':'at least3a+12b',
    'main_consequence':'tau<=3a+9b+1=3k0/4+1',
    'deficit_extension':'if p>=3a+12b-g and0<=g<2b, take e=floor(g/2)+1',
    'specialization_a33b':'tau<=108b+1',
    'b100_cost':10801, 'b100_residual_endpoint_upper':11098,
    'allocation':{format(s,'04b'):{str(q):v for q,v in opts.items()} for s,opts in allocation.items()},
    'active_parts':[(format(s,'04b'),q,v) for s,q,v in active],
}
Path('outputs/agent_shared_witness_two_request_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['allocation','active_parts']},indent=2))
