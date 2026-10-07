"""Discovery at fixed maximal-small triple, exact response coordinates and templates."""
from fractions import Fraction as F
import sys,json,time
from pathlib import Path
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt')
from p644_minimum_response_synth import template_pool,z3,np
OUT=Path(__file__).parent
labels,forms,matrix=template_pool()
print('templates',len(labels),flush=True)
def run(partial,minimum=False):
 p,e,f,g=z3.Reals('p e f g');variables=[p,e,f,g]
 s=z3.SolverFor('QF_LRA');s.set(timeout=60000)
 original=[27143,9408,22912];x=original[partial];y,z=[a for i,a in enumerate(original) if i!=partial]
 caps=[64000-x-y,64000-x-z,64000-y-z]
 s.add(p>=0,p<=4679,e>=0,e<=caps[0],f>=0,f<=caps[1],g>=0,g<=caps[2],p+e+f+g<=64000)
 if minimum:s.add(p+e+g>=x+z,p+f+g>=x+y)
 for trace in (p+e,p+f,g):
  for lo,hi in ():
   s.add(z3.Or(trace<str(lo),trace>str(hi)))
  s.add(z3.Or(trace<=27143,trace>32000))
 weights=[p,x-p,z3.RealVal(y),z3.RealVal(z),e,f,g,caps[2]-g]
 selected=[];result=None
 for step in range(64000):
  answer=s.check()
  if answer!=z3.sat:
   result={'status':str(answer),'steps':step}
   if answer==z3.unsat:(OUT/f'next_hole_nogaps_p{partial}_min{int(minimum)}.smt2').write_text(s.to_smt2())
   break
  model=s.model();point=[F(str(model.eval(v,model_completion=True))) for v in variables]
  pw=[point[0],x-point[0],F(y),F(z),point[1],point[2],point[3],caps[2]-point[3]]
  scores=(matrix@np.array(list(map(float,pw)))).max(axis=1)/12
  order=np.argsort(scores);winner=None
  for j in order:
   val=max(sum(a*b for a,b in zip(row,pw)) for row in forms[j])/12
   if val<=54784:winner=int(j);break
   if scores[j]>54784.001:break
  if winner is None:
   exact=[max(sum(a*b for a,b in zip(row,pw)) for row in fs)/12 for fs in forms]
   assert min(exact)>54784
   result={'status':'EXACT_MENU_HOLE','point':list(map(str,point)),'minimum_budget':str(min(exact)),'all_response_cells_positive':all(a>0 for a in pw)};break
  selected.append(winner)
  s.add(z3.Or(*[z3.Sum(*[int(a)*b for a,b in zip(row,weights)])>12*54784 for row in forms[winner]]))
  print('partial',partial,'min',minimum,'step',step,'point',list(map(str,point)),'winner',winner,'budget',str(val),flush=True)
 result=result or {'status':'LIMIT'}
 result.update(minimum=minimum,partial=partial,triple=[x,y,z],selected=[{'id':j,'labels':labels[j],'forms':forms[j]} for j in selected])
 (OUT/f'next_hole_nogaps_p{partial}_min{int(minimum)}.json').write_text(json.dumps(result,indent=2))
 print('RESULT',json.dumps({k:v for k,v in result.items() if k!='selected'}),flush=True)
for minimum in [False,True]:
 for partial in range(3):run(partial,minimum)
