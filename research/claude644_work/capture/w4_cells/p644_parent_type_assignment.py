"""Many-type assignment on a fixed, explicitly bad parent support.

Positive results are rationally reconstructed and checked. Solver rejection is
only discovery information. Row trimming makes upper type demands sufficient.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import milp,linprog,LinearConstraint,Bounds


def solve_support(types,caps,parents,seconds=3):
    types=[tuple(map(F,t)) for t in types];caps=list(map(F,caps))
    assert all(0<m<127 for m in parents) and all(a|b!=127 for a in parents for b in parents)
    n=len(types);p=len(caps);nc=len(parents);offset=nc*p;nv=offset+7*n
    A=[];lo=[];hi=[]
    def add(pairs,a,b):
        row=np.zeros(nv)
        for j,v in pairs:row[j]+=float(v)
        A.append(row);lo.append(a);hi.append(b)
    for i,cap in enumerate(caps):add([(i*nc+c,1) for c in range(nc)],-np.inf,float(cap))
    for j in range(7):
        add([(offset+j*n+a,1) for a in range(n)],1,1)
        for i in range(p):
            add([(i*nc+c,1) for c,m in enumerate(parents) if m>>j&1]
                +[(offset+j*n+a,-t[i]) for a,t in enumerate(types)],0,np.inf)
    integrality=np.array([0]*offset+[1]*(7*n));upper=np.array([np.inf]*offset+[1]*(7*n))
    res=milp(np.zeros(nv),integrality=integrality,bounds=Bounds(np.zeros(nv),upper),
             constraints=LinearConstraint(np.array(A),lo,hi),options={'time_limit':seconds})
    if res.x is None:return {'status':'NO_VERIFIED_WITNESS','scipy_status':res.status}
    labels=[max(range(n),key=lambda a:res.x[offset+j*n+a]) for j in range(7)]
    incidence=np.array([[int(m>>j&1) for m in parents] for j in range(7)])
    weights=[]
    for i,cap in enumerate(caps):
        fit=linprog(np.ones(nc),A_ub=-incidence,b_ub=[-float(types[a][i]) for a in labels],bounds=(0,None),method='highs')
        if not fit.success:return {'status':'NO_VERIFIED_WITNESS','reason':'reconstruction LP failed'}
        w=[F(float(v)).limit_denominator(1000000) for v in fit.x]
        if min(w)<0 or sum(w)>cap or any(sum(w[c] for c,m in enumerate(parents) if m>>j&1)<types[a][i] for j,a in enumerate(labels)):
            return {'status':'NO_VERIFIED_WITNESS','reason':'exact reconstruction failed'}
        weights.append(w)
    return {'status':'EXACT_POSITIVE','labels':labels,'parents':parents,'weights':[[str(v) for v in w] for w in weights]}


def solve(types,caps,seconds=3):
    menu=json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text())
    supports=sorted({tuple(v['parents']) for v in menu.values()},key=lambda s:(len(s),s))
    diagnostics=[]
    for parents in supports:
        result=solve_support(types,caps,list(parents),seconds)
        if result['status']=='EXACT_POSITIVE':return result
        diagnostics.append(result)
    return {'status':'NO_VERIFIED_WITNESS','diagnostics':diagnostics}


def expand_regions(witness,nodes,caps,global_labels):
    parents=witness['parents'];unique=sorted(set(global_labels));mapping={v:i for i,v in enumerate(unique)}
    assignment=[mapping[v] for v in global_labels];q=len(unique);nc=len(parents)
    initial=[[F(v) for v in nodes[j][1]] for j in unique]
    import random
    rng=random.Random(str(global_labels));best=None
    for trial in range(5):
        allweights=[];bounds=[[F(0)]*len(caps) for _ in unique]
        for i,cap in enumerate(caps):
            A=[];b=[]
            A.append([1]*nc+[0]*q);b.append(float(cap))
            for row,j in enumerate(assignment):
                A.append([-int(m>>row&1) for m in parents]+[int(k==j) for k in range(q)]);b.append(0)
            objective=[0]*nc+[-rng.randint(1,10) for _ in range(q)]
            result=linprog(objective,A_ub=A,b_ub=b,bounds=[(0,None)]*nc+[(float(t[i]),None) for t in initial],method='highs')
            if not result.success:break
            weights=[F(float(v)).limit_denominator(1000000) for v in result.x[:nc]]
            if min(weights)<0 or sum(weights)>cap:break
            rowloads=[sum(w for w,m in zip(weights,parents) if m>>row&1) for row in range(7)]
            for j in range(q):bounds[j][i]=min(rowloads[row] for row,v in enumerate(assignment) if v==j)
            if any(bounds[j][i]<initial[j][i] for j in range(q)):break
            allweights.append(weights)
        if len(allweights)!=len(caps):continue
        regions=[[j for j,node in enumerate(nodes) if all(F(v)<=u for v,u in zip(node[1],bound))] for bound in bounds]
        score=1
        for region in regions:score*=len(region)
        if best is None or score>best[0]:best=(score,bounds,regions,allweights)
    if best is None:return None
    _,bounds,regions,weights=best
    return {'assignment':assignment,'bounds':[[str(v) for v in row] for row in bounds],
            'regions':regions,'parents':parents,'weights':[[str(v) for v in row] for row in weights]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--cells',action='store_true');args=parser.parse_args()
    d=json.loads(Path(args.input).read_text());types=[hi for lo,hi in d['selected']] if args.cells else d['types']
    report=solve(types,d['capacities']);print(report)
    Path(args.input+'.parents.json').write_text(json.dumps(report,indent=2))
