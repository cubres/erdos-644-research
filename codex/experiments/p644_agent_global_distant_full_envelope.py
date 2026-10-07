"""Discovery LP envelopes for one particular forced-response state.

Uses rigorous relaxation mathematics but floating-point LP output here is
not yet an exact certificate. No general Erdős bound is asserted.
"""
import itertools,json
import numpy as np
from scipy.optimize import linprog

# A is averaged across the two flip states. Remaining atom order follows
# B_G, B_H, C_H, F_H, D_G, D_H, E_G, E_H.
T=[[(0,0,0,0,1)],[(0,0,0,1,1)],[(0,1,1,0,0)],[(0,1,1,1,0)],
   [(1,0,0,1,1)],[(1,1,1,1,1)],[(1,0,1,0,0)],[(1,0,1,1,1)],
   [(1,1,0,0,0)],[(1,1,0,1,1)]]
W=np.array([.25,.25,.25,.25,.24,.24,.25,.01,.25,.01])
RI=[0,1,3,5,8,9];RU=np.array([.25,.25,.25,.24,.25,.01])
N=len(RI);M=len(W);NV=N+M+N*M+1;TI=NV-1
def pij(i,j):return N+M+i*M+j
def graph(ps):
 return np.array([[sum(all(s[p]!=t[p] for p in ps) for s in T[a] for t in T[b])/len(T[a])/len(T[b]) for b in range(M)] for a in RI])
QS=[graph(ps) for ps in itertools.combinations(range(5),2)]

def lp(lo,hi,ret=False):
 a=[];b=[]
 def row(co,bd):
  x=np.zeros(NV)
  for i,v in co.items():x[i]=v
  a.append(x);b.append(bd)
 row({i:1 for i in range(N)},1)
 row({N+j:1 for j in range(M)},1)
 for i,j in enumerate(RI):row({i:1,N+j:1},W[j])
 for i in range(N):
  for j in range(M):
   p=pij(i,j);l,u=lo[i],hi[i];v=W[j]
   row({p:-1,N+j:l},0)
   row({p:-1,N+j:u,i:v},u*v)
   row({p:1,N+j:-u},0)
   row({p:1,N+j:-l,i:-v},-l*v)
  # R_i times sum_j H_j <= R_i.
  row({**{pij(i,j):1 for j in range(M)},i:-1},0)
 for j in range(M):
  row({**{pij(i,j):1 for i in range(N)},N+j:-1},0)
 for q in QS:row({**{pij(i,j):-q[i,j] for i in range(N) for j in range(M)},TI:1},0)
 bounds=list(zip(lo,hi))+[(0,w) for w in W]+[(0,None)]*(N*M)+[(0,None)]
 obj=np.zeros(NV);obj[TI]=-1
 r=linprog(obj,A_ub=a,b_ub=b,bounds=bounds,method='highs')
 if ret:return r,np.array(a),np.array(b),bounds
 return r

if __name__=='__main__':
 import heapq,time
 r=lp(np.zeros(N),RU)
 print('root',r.success,-r.fun,'r',r.x[:N],flush=True)
 queue=[(r.fun,0,np.zeros(N),RU,r)];serial=1;count=0;t0=time.time()
 bestbound=-r.fun
 while queue and count<100000:
  neg,_,lo,hi,r=heapq.heappop(queue);bound=-neg
  if bound<.24-1e-8:continue
  # Select r whose actual product discrepancy contributes most.
  rv=r.x[:N];hv=r.x[N:N+M];prod=r.x[N+M:TI].reshape(N,M)
  actual=np.array([rv@q@hv for q in QS])
  if actual.min()>=.24+1e-7:
   print('numerical_survivor',actual.min(),'R',rv,'H',hv,flush=True)
   break
  error=np.abs(prod-rv[:,None]*hv[None,:])*sum(QS)
  i=int(np.argmax(error.sum(axis=1)))
  if hi[i]-lo[i]<1e-7:i=int(np.argmax(hi-lo))
  mid=(lo[i]+hi[i])/2
  for side in range(2):
   nl,nu=lo.copy(),hi.copy()
   if side==0:nu[i]=mid
   else:nl[i]=mid
   nr=lp(nl,nu);count+=1
   if nr.success and -nr.fun>=.24-1e-8:
    heapq.heappush(queue,(nr.fun,serial,nl,nu,nr));serial+=1
  if count%1000==0:print('nodes',count,'queue',len(queue),'upper',-queue[0][0] if queue else 0,'seconds',time.time()-t0,flush=True)
 print('discovery result',count,len(queue),-queue[0][0] if queue else 'no surviving boxes',flush=True)
