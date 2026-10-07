"""Discovery of five-rectangle capacity obstruction; no floating status is a proof."""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction

def antichains():
 inc=[sum(1<<t for t in range(32) if not (s&t==s or s&t==t)) for s in range(32)]
 def rec(chosen,remain):
  yield chosen
  while remain:
   bit=remain&-remain;remain^=bit;s=bit.bit_length()-1
   yield from rec(chosen+(s,),remain&inc[s])
 yield from rec((),(1<<32)-1)

def blocker(ac):
 cand=[s for s in range(32) if all(s&t for t in ac)]
 return tuple(s for s in cand if not any(t!=s and t&s==t for t in cand))

def run():
 perms=[tuple(sum(1<<p[j] for j in range(5) if s>>j&1) for s in range(32)) for p in itertools.permutations(range(5))]
 seen=set();rows=[]
 for ac in antichains():
  if not ac or ac==(0,) or ac in seen:continue
  seen.update(tuple(sorted(p[s] for s in ac)) for p in perms)
  bc=blocker(ac);types=list(ac)+list(bc);n=len(types)
  A=np.zeros((5,n+1));
  for i in range(5):
   for j,s in enumerate(types):A[i,j]=(s>>i)&1
   A[i,-1]=-1
  E=np.zeros((2,n+1));E[0,:len(ac)]=1;E[0,-1]=-1;E[1,len(ac):n]=1
  c=np.zeros(n+1);c[-1]=1
  res=linprog(c,A_ub=A,b_ub=np.zeros(5),A_eq=E,b_eq=[0,1],bounds=[(0,None)]*(n+1),method='highs')
  row={'a_types':ac,'b_types':bc,'status':int(res.status)}
  if res.success:
   row['minimum_a']=str(Fraction(float(res.fun)).limit_denominator(10000))
   row['masses']=[str(Fraction(float(v)).limit_denominator(10000)) for v in res.x]
   row['ubdual']=[str(Fraction(float(v)).limit_denominator(10000)) for v in res.ineqlin.marginals]
   row['eqdual']=[str(Fraction(float(v)).limit_denominator(10000)) for v in res.eqlin.marginals]
  rows.append(row)
 vals=[(Fraction(q['minimum_a']),q) for q in rows if q['status']==0];best=min(v[0] for v in vals)
 print('orbits',len(rows),'minimum',best,'optimal',sum(v[0]==best for v in vals),flush=True)
 print(json.dumps([q for v,q in vals if v==best],indent=2),flush=True)
 root=Path('logs/astra_agent_alternative');root.mkdir(exist_ok=True);(root/'rectangle5_discovery.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':run()
