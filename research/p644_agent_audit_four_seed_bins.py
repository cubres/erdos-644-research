"""Discovery MILP for covering a four-row two-transversal graph by three bins.

No positive-cell cutoff: each Venn cell is divided between the seven nonempty
bin-membership patterns. Binary support flags only prohibit disjoint patterns
on adjacent cells. This is a complete continuous model for this fixed graph.
Numerical solver results remain discovery evidence, not an exact certificate.
"""
import argparse
import json
import time
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix


def graph(a, x, y, rank=1):
    # Xi is the old pair core opposite row i; old triple intersection is empty.
    p = [rank-a[(i+1)%3]-a[(i+2)%3] for i in range(3)]
    weights = list(x)+[a[i]-x[i] for i in range(3)]+list(y)+[p[i]-y[i] for i in range(3)]
    names = ['T%d'%i for i in range(3)]+['Z%d'%i for i in range(3)]+['Y%d'%i for i in range(3)]+['S%d'%i for i in range(3)]
    edges = list(combinations(range(3),2))
    for i in range(3):
        edges += [(i,9+i),(i,6+i),(3+i,6+i)]
        edges += [(i,3+j) for j in range(3) if i!=j]
    assert min(weights)>=-1e-9 and sum(x)+sum(y)<=rank+1e-9
    return names, [max(0,w) for w in weights], edges


def solve(a,x,y,seconds=30):
    names,weights,edges=graph(a,x,y)
    active=[i for i,w in enumerate(weights) if w>0 and
            any((i==u and weights[v]>0) or (i==v and weights[u]>0) for u,v in edges)]
    pairs=[(i,m) for i in active for m in range(1,8)]
    idx={v:j for j,v in enumerate(pairs)}
    n=len(pairs); q=2*n; rows=[]; lo=[]; hi=[]
    def add(terms,l=-np.inf,h=np.inf):
        rows.append(terms);lo.append(l);hi.append(h)
    for i in active:add({idx[i,m]:1 for m in range(1,8)},weights[i],weights[i])
    for j,(i,m) in enumerate(pairs):add({j:1,n+j:-weights[i]},h=0)
    for i,j in edges:
        if i not in active or j not in active:continue
        for m in range(1,8):
            for v in range(1,8):
                if not m&v:add({n+idx[i,m]:1,n+idx[j,v]:1},h=1)
    for b in range(3):
        row={idx[i,m]:1 for i,m in pairs if m&(1<<b)};row[q]=-1
        add(row,h=0)
    matrix=lil_matrix((len(rows),q+1))
    for r,row in enumerate(rows):
        for j,v in row.items():matrix[r,j]=v
    objective=np.zeros(q+1);objective[q]=1
    upper=np.array([weights[i] for i,m in pairs]+[1]*n+[sum(weights)])
    started=time.time()
    result=milp(objective,integrality=np.array([0]*n+[1]*n+[0]),bounds=Bounds(np.zeros(q+1),upper),
                constraints=LinearConstraint(matrix.tocsr(),lo,hi),options={'time_limit':seconds,'mip_rel_gap':0})
    out={'a':a,'x':x,'y':y,'weights':dict(zip(names,weights)),
         'minimum_good_triple_sum':sum(a),'new_good_triple_checks':[
             {'omitted_old_row':i,'is_good':x[i]==0,
              'sum':a[i]+sum(x[j]+y[j] for j in range(3) if j!=i)+2*x[i],
              'minimum_preserved':x[i]!=0 or a[i]+sum(x[j]+y[j] for j in range(3) if j!=i)>=sum(a)-1e-9}
             for i in range(3)],
         'status':result.message,'elapsed_seconds':time.time()-started,
         'q_upper':float(result.fun) if result.fun is not None else None,
         'q_lower':float(result.mip_dual_bound) if getattr(result,'mip_dual_bound',None) is not None else None,
         'interpretation':'Numerical discovery only; fixed four-row graph, three-bin cover.'}
    if result.x is not None:
        out['assignments']={names[i]:{str(m):float(result.x[idx[i,m]]) for m in range(1,8) if result.x[idx[i,m]]>1e-8} for i in active}
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=int,default=30)
    parser.add_argument('--case',choices=['boundary','intermediate','clustered'],default='intermediate')
    args=parser.parse_args()
    cases={'boundary':([.5,.5,.25],[.25,.25,0],[.25,.25,0]),
           'intermediate':([.49,.49,.24],[.25,.25,0],[.25,.25,0]),
           'clustered':([.5,.5,.5],[0,.25,.25],[0,0,0])}
    print(json.dumps(solve(*cases[args.case],seconds=args.seconds),indent=2))
