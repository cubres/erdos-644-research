"""Independent exact replay of the theory agent's restricted-menu obstruction."""
from fractions import Fraction as F
import itertools,json
from pathlib import Path
from anchor_pair_request import pair_best
x=[F(v,1000) for v in (755,780,750)]
T=[[F(v,1000) for v in r] for r in [(512,0,488),(404,521,75),(499,0,501)]]
lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
pencils=[[l for l,L in enumerate(lines) if q in L] for q in range(7)]
assert all(sum(t)==1 and all(0<=t[i]<=x[i] for i in range(3)) for t in T)
assert all(T[i][i]>2*x[i]/3 for i in range(3))
assert sum(x[i]-T[i][i] for i in range(3))==F(751,1000)
for asg in itertools.product(range(3),repeat=7):
 rows=[T[k] for k in asg]
 assert any(sum(t[i] for t in rows)>4*x[i] or any(sum(rows[j][i] for j in pencil)>2*x[i] for pencil in pencils) for i in range(3))
for a,b,c,d in itertools.product(T,repeat=4):
 assert any(max(a[i],b[i],c[i],(a[i]+b[i]+c[i])/2,d[i]+(b[i]+c[i])/2,d[i]+(a[i]+b[i]+c[i])/4)>x[i] for i in range(3))
source=Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json')
P=json.loads(source.read_text())['minimal_functions'];assert len(P)==42
for a,b in itertools.product(T,repeat=2):
 for p in P:assert any(any(F(u)*a[i]+F(v)*b[i]>x[i] for u,v in p['vertices']) for i in range(3))
costs=[]
for i,j in itertools.combinations(range(3),2):
 q=pair_best(x,T[i],T[j]);cost=min(sum(x)-1,q['cost']) if q else sum(x)-1
 assert cost>F(3,4);costs.append([i,j,str(cost)])
out={'status':'PASS','capacities':list(map(str,x)),'types':[list(map(str,t)) for t in T],'sum_own_slacks':'751/1000','no_Fano':True,'no_V4':True,'no_42_pair_template':True,'best_two_anchor_costs':costs,'scope':'Obstruction to a restricted three-minimum template/exchange menu; not a counterexample to Th(3).'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
