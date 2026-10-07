"""Search for dense G2 compositions surviving whole-cell third profiles.
Numerical discovery only; no infeasibility theorem is inferred from this scan.
"""
import sys,json,random,time
from itertools import combinations
from p644_agent_alternative_two_response_certificate import CELLS
from p644_agent_alternative_third_response import profile
from p644_agent_alternative_full_response import Model


def cells_for(g,M=20,h=0):
 cells=[]
 for name,mask,g1,coef,const in CELLS:
  w=coef*M+const;g2=g.get(name,0)
  if g2:cells.append((name+'2',mask|(64 if g1 else 0)|128,g2))
  if w>g2:cells.append((name+'n',mask|(64 if g1 else 0),w-g2))
 if h:cells.append(('G12fresh',64|128,h))
 if M+3>h:cells.append(('G1fresh',64,M+3-h))
 remaining=28*M+3-sum(g.values())-h
 if remaining>0:cells.append(('G2fresh',128,remaining))
 return cells


def best_profile(g,M=20,h=0,early=True):
 cells=cells_for(g,M,h);best=None
 for I in [(1,2,3),(0,3,5)]+[I for I in combinations(range(6),3) if I not in [(1,2,3),(0,3,5)]]:
  out=profile(cells,sum(1<<i for i in I),24*M)
  if out and (best is None or out.get('cost',1e9)<best['cost']):
   best=dict(out,rows=''.join(str(i+1) for i in I))
   if early and out.get('cost',1e9)<=21*M+12:break
 return best

if __name__=='__main__':
 count=int(sys.argv[1]) if len(sys.argv)>1 else 100
 M=20; rng=random.Random(644);model=Model(scale=8*M)
 high=None;feasible=0;start=time.time();records=[]
 for iteration in range(count):
  g={name:rng.randint(0,coef*M) for name,_,_,coef,_ in CELLS[:9] if name not in ['A-','B+']}
  h=rng.randint(0,M+3)
  if sum(g.values())+h>28*M+3:continue
  selected=[g.get(c[0],0) for c in model.cells]
  six,seven=model.evaluate(selected)
  if not all(row['lex_ok'] for row in six) or not all(row['two_pierceable'] for row in seven):continue
  feasible+=1
  out=best_profile(g,M,h)
  record={'iteration':iteration,'g':g,'h':h,'best':out}
  if high is None or out['cost']>high['best']['cost']:
   high=record;print('NEW',json.dumps(high),'seconds',time.time()-start,flush=True)
  if out['cost']>21*M+12:
   records.append(record);print('SURVIVOR',json.dumps(record),flush=True)
 print('DONE',iteration+1,feasible,'high',json.dumps(high),'seconds',time.time()-start)
 open('outputs/agent_third_response_dense_scan.json','w').write(json.dumps({'count':count,'feasible':feasible,'high':high,'survivors':records},indent=2)+'\n')
