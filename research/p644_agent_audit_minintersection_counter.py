"""Exact two-type obstruction to mu >= tau/3 above density 2/3.

Uses the previously certified completeness theorem for the 42 capacity
functions; does not replay or independently assert catalogue completeness.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

root=Path(__file__).resolve().parent
rows=json.loads((root/'logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
assert len(rows)==42
k,x,y,d,c=map(Q,(200,14,339,0,10))
records=[]
for i,row in enumerate(rows):
    shape=[tuple(map(Q,p))for p in row['vertices']]
    first=max(u*d+v*c for u,v in shape)
    second=max(u*(k-d)+v*(k-c)for u,v in shape)
    margin=max(first-x,second-y)
    assert margin>0
    records.append({'index':i,'first_capacity':str(first),
                    'second_capacity':str(second),'exclusion_margin':str(margin)})
assert min(Q(r['exclusion_margin'])for r in records)==1
tau=x+y-k-(c-d)
pair_values={}
for name,a,b in [('low-low',d,d),('low-high',d,c),('high-high',c,c)]:
    pair_values[name]=max(0,a+b-x)+max(0,2*k-a-b-y)
assert pair_values=={'low-low':Q(61),'low-high':Q(51),'high-high':Q(47)}
assert tau==143 and tau>2*k/3 and tau-3*min(pair_values.values())==2
print(json.dumps({'status':'PASS','dependency':'Theorem 7.69 complete 42-capacity criterion',
                  'rank_unit':200,'part_units':[14,339],'first_part_type_units':[0,10],
                  'tau_at_scale_m':'143m+2','minimum_pair_intersection_at_scale_m':'47m',
                  'tau_minus_three_mu':'2m+2','exclusions':records},indent=2))
