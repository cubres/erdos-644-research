"""Exact rational upper-allocation check; no optimizer or positive cutoff."""
from fractions import Fraction as F
import json
from pathlib import Path

allocation = {
    1: ['0','2/3','1/3','0'],
    2: ['1/3','2/3','0','0'],
    3: ['0','0','2','0'],
    4: ['1','0','0','0'],
    5: ['0','2','0','0'],
    6: ['2','0','0','0'],
    7: ['0','0','0','1'],
    8: ['0','0','1','0'],
    9: ['2','0','0','0'],
    10:['0','2','0','0'],
    11:['0','0','0','1'],
    12:['0','0','2','0'],
    13:['0','0','0','1'],
    14:['0','0','0','1'],
}
x = {(m,c):F(v) for m, row in allocation.items() for c,v in enumerate(row)}
assert all(v>=0 for v in x.values())
for m in range(1,15):
    expected = 2 if bin(m).count('1')==2 else 1
    assert sum(x[m,c] for c in range(4))==expected
budgets=[sum(v for (m,c),v in x.items() if c&bit) for bit in (1,2)]
eligible={
    (m,c) for (m,c),v in x.items() if v>0 and any(
        w>0 and m|n==15 and c&d==0 for (n,d),w in x.items())
}
residual=sum(x[p] for p in eligible)
assert budgets==[F(28,3),F(28,3)]
assert residual==F(28,3)
out={'status':'EXACT_PASS','certificate_scope':'upper allocation at 28/3 only; not optimality',
     'budgets':list(map(str,budgets)),'residual':str(residual),
     'allocation':{str(m):row for m,row in allocation.items()},
     'eligible_type_codes':[list(p) for p in sorted(eligible)]}
path=Path(__file__).resolve().parent.parent/'outputs'/'agent_twenty_triples_two_request_exact.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print('EXACT_PASS budgets=28/3,28/3 residual=28/3')
