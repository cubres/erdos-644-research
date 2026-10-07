import json, sys, time
from fractions import Fraction as F
from w4_typeclosed_lib import bad_tuple_milp
k = sys.argv[1]
d = json.load(open(f'w4_cells/logs/astra_continuous_type_cells/40_{k}_T30_fano_regions_parents.json'))
types = [tuple(s[1]) for s in d['selected']]
caps = d['capacities']
t0 = time.time()
st, assign, cells = bad_tuple_milp(types, caps, time_limit=300)
print(k, st, assign and [types[a] for a in assign], round(time.time()-t0,1))
if cells:
    for (i,S),v in sorted(cells.items()): print(i, bin(S)[2:].zfill(7)[::-1], round(v,3))
