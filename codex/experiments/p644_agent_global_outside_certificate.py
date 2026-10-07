"""Generate exact dual/box certificate for one conditional response lemma.

Floating-point LP chooses a proof. Fraction arithmetic verifies every
certified leaf bound before export. A separate checker should reconstruct
the model and tree; successful generation is not a general Erdős bound.
"""
from fractions import Fraction as F
import heapq,itertools,json
from pathlib import Path
import numpy as np
import p644_agent_global_outside_full_envelope as model

T=[(0,0,0,0,1),(0,0,0,1,0),(0,1,1,0,0),(0,1,1,1,1),
   (1,0,0,1,1),(1,1,1,1,1),(1,0,1,0,0),(1,0,1,1,1),
   (1,1,0,0,0),(1,1,0,1,1)]
W=list(map(F,['1/4','1/4','1/4','1/4','6/25','6/25','1/4','1/100','1/4','1/100']))
RI=[0,1,2,4,5,8,9]
RU=list(map(F,['1/4','1/4','1/8','1/8','6/25','1/4','1/100']))
N,M=len(RI),len(W);NV=N+M+N*M+1;TI=NV-1;TARGET=F(6,25)
def pij(i,j):return N+M+i*M+j

def exact_model(lo,hi):
 rows=[]
 def row(co,bd,label):rows.append((co,F(bd),label))
 row({i:F(1) for i in range(N)},1,'rank_R')
 row({N+j:F(1) for j in range(M)},1,'rank_H')
 for i,j in enumerate(RI):row({i:F(1),N+j:F(1)},W[j],f'cell_{j}')
 for i in range(N):
  for j in range(M):
   p=pij(i,j);l,u=lo[i],hi[i];v=W[j]
   row({p:F(-1),N+j:l},0,f'mcc_lower0_{i}_{j}')
   row({p:F(-1),N+j:u,i:v},u*v,f'mcc_lower1_{i}_{j}')
   row({p:F(1),N+j:-u},0,f'mcc_upper0_{i}_{j}')
   row({p:F(1),N+j:-l,i:-v},-l*v,f'mcc_upper1_{i}_{j}')
  row({**{pij(i,j):F(1) for j in range(M)},i:F(-1)},0,f'rlt_R_{i}')
 for j in range(M):row({**{pij(i,j):F(1) for i in range(N)},N+j:F(-1)},0,f'rlt_H_{j}')
 for a,b in itertools.combinations(range(5),2):
  co={pij(i,j):F(-int(T[RI[i]][a]!=T[j][a] and T[RI[i]][b]!=T[j][b])) for i in range(N) for j in range(M)}
  co[TI]=F(1);row(co,0,f'Q_{a}_{b}')
 bounds=list(zip(lo,hi))+[(F(0),w) for w in W]+[(F(0),hi[i]*W[j]) for i in range(N) for j in range(M)]+[(F(0),F(1))]
 return rows,bounds

def dual_certificate(lo,hi,res):
 rows,bounds=exact_model(lo,hi)
 y=[F(max(0.,-v)).limit_denominator(10**10) for v in res.ineqlin.marginals]
 assert len(y)==len(rows)
 rem=[F(0)]*NV;rem[TI]=F(1);ub=F(0)
 sparse=[]
 for ix,(z,(co,bd,label)) in enumerate(zip(y,rows)):
  if not z:continue
  sparse.append([ix,str(z)]);ub+=z*bd
  for j,v in co.items():rem[j]-=z*v
 ub+=sum((d*(bounds[j][1] if d>0 else bounds[j][0]) for j,d in enumerate(rem)),F(0))
 return ub,sparse

def main():
 rootlo=[F(0)]*N;roothi=RU
 nodes=[];queue=[];bounds=[];lpcalls=0
 def add(lo,hi):
  nonlocal lpcalls
  ni=len(nodes);node={'lo':list(map(str,lo)),'hi':list(map(str,hi))};nodes.append(node)
  if sum(lo)>1:
   node['kind']='rank_empty';return ni
  res=model.lp(np.array(list(map(float,lo))),np.array(list(map(float,hi))))
  lpcalls+=1
  assert res.success, (ni,res.message)
  ub,dual=dual_certificate(lo,hi,res)
  if ub<TARGET:
   node.update(kind='dual_leaf',upper=str(ub),multipliers=dual);bounds.append(ub)
  else:heapq.heappush(queue,(-float(ub),ni,lo,hi,res))
  return ni
 add(rootlo,roothi)
 while queue:
  _,ni,lo,hi,res=heapq.heappop(queue)
  rv=res.x[:N];hv=res.x[N:N+M];p=res.x[N+M:TI].reshape(N,M)
  errs=(np.abs(p-rv[:,None]*hv)*sum(model.QS)).sum(axis=1)
  i=int(np.argmax(errs))
  if hi[i]-lo[i]<F(1,10**7):i=max(range(N),key=lambda j:hi[j]-lo[j])
  mid=(lo[i]+hi[i])/2;left_hi=hi.copy();left_hi[i]=mid;right_lo=lo.copy();right_lo[i]=mid
  left=add(lo,left_hi);right=add(right_lo,hi)
  nodes[ni].update(kind='split',axis=i,mid=str(mid),children=[left,right])
  assert len(nodes)<100000
 out={'claim':'Conditional twelve-row paired-Q response exclusion; not a general Erdos bound',
      'scale':'k=1; all quantities rational', 'target':str(TARGET),
      'old_pair_labels':[1,2,3,4,6], 'old_atom_types':T,'old_atom_masses':list(map(str,W)),
      'R_atom_indices':RI,'root_R_upper':list(map(str,RU)),
      'variable_order':'R7, H10, product R_i H_j row-major70, t',
      'inequality_order':[label for co,bd,label in exact_model(rootlo,roothi)[0]],
      'dual_rule':'For Ax<=b, bounds l<=x<=u, y>=0: t<=y.b+sum_j max((e_t-A^T y)_j*l_j,(e_t-A^T y)_j*u_j).',
      'nodes':nodes,'total_nodes':len(nodes),'lp_calls':lpcalls,
      'dual_leaves':len(bounds),'rank_empty_leaves':sum(n['kind']=='rank_empty' for n in nodes),
      'maximum_leaf_upper':str(max(bounds)),'minimum_strict_margin':str(TARGET-max(bounds))}
 path=Path('outputs/agent_global_outside_certificate.json');path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k in ['total_nodes','lp_calls','dual_leaves','rank_empty_leaves','maximum_leaf_upper','minimum_strict_margin']},indent=2))
 print('max upper',float(max(bounds)),'min margin',float(TARGET-max(bounds)))
 print(path)

if __name__=='__main__':main()
