"""Bounded exact-SMT discovery probes for mu >= 3*tau - 2.

UNSAT concerns the explicit necessary conditions encoded here; this is not
an independently replayable rational contradiction certificate.  The 42
positive two-type capacities are reused without replaying their catalogue.
"""
from pathlib import Path
from itertools import product, combinations, permutations
import argparse, json, sys, time
sys.path.insert(0, '/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3

def maximum(*xs):
    out=xs[0]
    for x in xs[1:]: out=z3.If(out>=x,out,x)
    return out

def minimum(*xs):
    out=xs[0]
    for x in xs[1:]: out=z3.If(out<=x,out,x)
    return out

def fano142(a,q,c):
    # One a-row, four q-rows, two c-rows.  The a,c,c rows lie on a
    # Fano line. Orbit masses d=a/4, b=max(0,c/2-a/4),
    # f=max(0,q-b-a/2) give load at least (a,q,c).
    return maximum(a,c+a/2,q+a/2,q+c/2+a/4)

def run(parts,types,timeout,central=False):
    s=z3.Solver();s.set(timeout=timeout)
    x=[z3.Real('x%d'%i)for i in range(parts)]
    a=[[z3.Real('a%d_%d'%(j,i))for i in range(parts)]for j in range(types)]
    t=z3.Real('tau')
    s.add(t>z3.RealVal('2/3'))
    for i in range(parts): s.add(x[i]>0)
    for row in a:
        s.add(z3.Sum(row)==1)
        for i in range(parts):s.add(row[i]>=0,row[i]<=x[i])
    # Each type must be blocked in at least one part; all assignments
    # give the exact continuous transversal minimum.
    for assignment in product(range(parts),repeat=types):
        terms=[];zeros=[]
        for i in range(parts):
            chosen=[a[j][i]for j in range(types)if assignment[j]==i]
            if chosen:
                terms.append(x[i]-minimum(*chosen))
                zeros += [v==0 for v in chosen]
        s.add(z3.Or(*(zeros+[t<=z3.Sum(terms)])))
    rows=json.loads((Path(__file__).parent/'logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
    for j,k in combinations(range(types),2):
        for row in rows:
            s.add(z3.Or(*[z3.RealVal(u)*a[j][i]+z3.RealVal(v)*a[k][i]>x[i]
                         for i in range(parts)for u,v in row['vertices']]))
    # Homogeneous Fano is included separately, also for one-type tests.
    for row in a:s.add(z3.Or(*[7*row[i]>4*x[i]for i in range(parts)]))
    for j,k,l in permutations(range(types),3):
        s.add(z3.Or(*[fano142(a[j][i],a[k][i],a[l][i])>x[i]for i in range(parts)]))
    mumap={(j,k):z3.Sum([maximum(0,a[j][i]+a[k][i]-x[i])for i in range(parts)])
           for j in range(types)for k in range(j,types)}
    mus=list(mumap.values())
    if central:
        for j in range(types):s.add(z3.Or(*[mumap[min(j,k),max(j,k)]<3*t-2 for k in range(types)]))
    else:s.add(z3.Or(*[mu<3*t-2 for mu in mus]))
    start=time.time();result=s.check()
    out={'parts':parts,'types':types,'centrality_target':central,'status':str(result),'elapsed_seconds':time.time()-start,
         'interpretation':'Discovery only: necessary positive constructions and exact blocker costs.'}
    if result==z3.sat:
        m=s.model()
        out.update(capacities=[str(m.eval(v))for v in x],
                   types_vectors=[[str(m.eval(v))for v in row]for row in a],
                   tau_lower_bound=str(m.eval(t)),
                   pair_intersections=[str(m.eval(mu))for mu in mus])
    elif result==z3.unknown:out['reason']=s.reason_unknown()
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parts',type=int,default=3)
    p.add_argument('--types',type=int,default=3);p.add_argument('--timeout',type=int,default=60000)
    p.add_argument('--central',action='store_true')
    a=p.parse_args();print(json.dumps(run(a.parts,a.types,a.timeout,a.central),indent=2))
