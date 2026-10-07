"""One prescribed outside-plus-neighborhood response probe.

Nonlinear optimization proposes only. The input has general row masks;
neither new row is assumed to stay in the previously known ground set.
"""
from fractions import Fraction as F
import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

def main():
 data=json.loads(Path('outputs/agent_global_distant_outside_survivor.json').read_text())
 masks=[a['mask'] for a in data['atoms']];w=np.array([float(F(a['mass'])) for a in data['atoms']]);n=len(w)
 caps=w.copy()
 for i in [5,6,9,10,14]:caps[i]=0
 caps[4]=.125
 assert abs(sum(w-caps)-.75)<1e-10
 active=np.flatnonzero(caps>0);nr=len(active);npairs=6
 mats=[]
 for ps in itertools.combinations(range(npairs),2):
  target=sum(3<<(2*p) for p in ps)
  mat=np.array([[int((masks[i]|masks[j])&target==target) for j in range(n)] for i in active])
  mats.append((ps,mat))
 def qs(x):return np.array([x[:nr]@a@x[nr:nr+n] for ps,a in mats])
 def jacqs(x):return np.array([np.r_[a@x[nr:nr+n],x[:nr]@a,-1] for ps,a in mats])
 overlap=np.zeros((n,nr+n+1));overlap[:,nr:nr+n]=np.eye(n)
 for j,i in enumerate(active):overlap[i,j]=1
 rsum=np.r_[np.ones(nr),np.zeros(n+1)];hsum=np.r_[np.zeros(nr),np.ones(n),0]
 cons=[{'type':'ineq','fun':lambda x:1-rsum@x,'jac':lambda x:-rsum},
       {'type':'ineq','fun':lambda x:1-hsum@x,'jac':lambda x:-hsum},
       {'type':'ineq','fun':lambda x:w-overlap@x,'jac':lambda x:-overlap},
       {'type':'ineq','fun':lambda x:qs(x)-x[-1],'jac':jacqs}]
 eta=1e-4;bounds=[(eta,u) for u in caps[active]]+[(eta,v) for v in w]+[(0,1)]
 rng=np.random.default_rng(644);best=None
 for j in range(40):
  r=caps[active]*rng.uniform(.3,.8,nr);r*=min(1,.95/r.sum())
  full=np.zeros(n);full[active]=r
  h=(w-full)*rng.uniform(.3,.8,n);h*=min(1,.95/h.sum())
  res=minimize(lambda x:-x[-1],np.r_[r,h,0],jac=lambda x:np.r_[np.zeros(nr+n),-1],
               bounds=bounds,constraints=cons,method='SLSQP',options={'maxiter':2000,'ftol':1e-12})
  if min(float(np.min(c['fun'](res.x))) for c in cons)>-1e-7 and (best is None or res.fun<best.fun):
   best=res;print('discovery',j,-res.fun,flush=True)
 assert best is not None
 r=np.zeros(n);r[active]=best.x[:nr];h=best.x[nr:nr+n]
 out={'status':'Numerical discovery only; not a certificate','input':'outputs/agent_global_distant_outside_survivor.json',
      'deletion_mass':.75,'R_upper':caps.tolist(),'R':r.tolist(),'S':h.tolist(),
      'outside_R':float(1-r.sum()),'outside_S':float(1-h.sum()),
      'minimum_new_Q':float(qs(best.x).min()),
      'Q_profile':[{'old_pairs':[i+1 for i in ps],'Q':float(q)} for (ps,a),q in zip(mats,qs(best.x))]}
 path=Path('outputs/agent_global_outside_control_probe.json');path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));print(path)

if __name__=='__main__':main()
