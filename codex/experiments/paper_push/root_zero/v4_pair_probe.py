"""Discovery only: two proposed V4 orientations from global/zero minimizers."""
import numpy as np,json,itertools
from scipy.optimize import linprog
from pathlib import Path
# x,y,z,sY,sZ,hY,hZ,pY,pZ,eta
n=10
v=np.eye(n);x,y,z,sY,sZ,hY,hZ,pY,pZ,eta=v
one=np.zeros(n)
A=[];b=[]
def le(row,rhs=0):A.append(row);b.append(rhs)
le(2*y-3*sY);le(2*z-3*sZ)
le(sY-hY);le(sZ-hZ)
le(sY-y);le(sZ-z);le(hY-y);le(hZ-z)
le(sY+pY,1);le(sZ+pZ,1);le(pY-x);le(pZ-x)
le(-pY-sY-z,-1);le(-pZ-sZ-y,-1)
le(-y-z+sY+sZ,-.75)
le(-x-y-z+hY+hZ+eta,-.75)
le(x-pY-pZ+eta)
# encode each profile as (vector,constant) percoordinate
Z=(one,0)
GY=[(pY,0),(sY,0),(-pY-sY,1)]
GZ=[(pZ,0),(-pZ-sZ,1),(sZ,0)]
UY=[Z,(hY,0),(-hY,1)]
UZ=[Z,(-hZ,1),(hZ,0)]
def facets(d,a,bb,c):
 result=[]
 for i,cap in enumerate([x,y,z]):
  for weights in [(0,1,0,0),(0,0,1,0),(0,0,0,1),(0,.5,.5,.5),(1,0,.5,.5),(1,.25,.25,.25)]:
   row=-cap.copy();const=0
   for w,typ in zip(weights,[d,a,bb,c]): row+=w*typ[i][0];const+=w*typ[i][1]
   result.append((row,const))
 return result
fs=[facets(UZ,GZ,GY,UY),facets(UY,GY,GZ,UZ)]
bounds=[(0,.25),(.75,1.5),(.75,1.5)]+[(0,1)]*6+[(0,None)]
sols=[]
for ia,ib in itertools.product(range(18),repeat=2):
 aa=list(A);bb=list(b)
 for j,i in enumerate([ia,ib]):
  f,c=fs[j][i];aa.append(-f+eta);bb.append(c)
 r=linprog(-eta,A_ub=aa,b_ub=bb,bounds=bounds,method='highs')
 if r.success and r.x[-1]>1e-8:
  sols.append({'facets':[ia,ib],'point':r.x.tolist()})
  break
print(json.dumps({'status':'survivor' if sols else 'all_closed_numerically','sols':sols},indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(sols,indent=2))
