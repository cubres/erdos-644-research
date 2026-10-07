from fractions import Fraction as Fr
import json, itertools
from tc3lib import *
d=json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_three_part_two_type_barrier.json'))
K=[tuple(Fr(v,80) for v in t) for t in d['types']]
x=[Fr(513,640)]*3
tau,t=tau_star(K,x,want=True); print('tau*',tau,float(tau),'opt thresholds',t)
print('fano (all 9):', fano_search(K,x)); print('V:', v_search(K,x))
H=[Fr(4,7)*xi for xi in x]
print('H window (4x/7):',[float(h) for h in H],' any type in H:',[k for k,c in enumerate(K) if all(c[i]<=H[i] for i in range(3))])
boxes=maximal_free_boxes_containing(K,x,H)
print('free boxes around H:',len(boxes))
for cost,tt,bl in boxes[:12]:
    blk=sorted(set(sum(bl,[])))
    sub=[K[k] for k in blk]
    fs=fano_search(sub,x); vs=v_search(sub,x)
    print(' cost %.4f t=%s blockers=%s tau*(blk)=%.4f fano=%s V=%s'%(float(cost),[None if v is None else float(v) for v in tt],bl,float(tau_star(sub,x)),fs and [blk[i] for i in fs],vs and [blk[i] for i in vs]))
# which triples/quads of types have a Fano tuple
for r in (3,4):
    good=[s for s in itertools.combinations(range(9),r) if fano_search([K[i] for i in s],x)]
    print(r,'-subsets with a Fano tuple:',len(good),good[:10])
