"""Produce a pruned rational branch certificate for the new density bridge."""
from fractions import Fraction as Q
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import linprog
from p644_agent_audit_density_check import ROOT,D,SHAPES,system

def prepare():
    ROOT.mkdir(exist_ok=True)
    source=json.loads((Path(__file__).resolve().parent/'logs/astra_two_part_gap_central/templates.json').read_text())
    out={}
    for key,shape in SHAPES.items():
        item=source[str(key)];r=item['record']
        assert r['vertices']==[list(v) for v in shape]
        expected={(Q(0),Q(1)),(Q(1),Q(0))}
        shape=[tuple(map(Q,p)) for p in shape]
        for left,right in zip(shape,shape[1:]):
            a=left[1]-right[1];b=right[0]-left[0]
            expected.add((a/(a+b),b/(a+b)))
        out[str(key)]={'parents':item['parents'],'colour':r['colour'],'primal':[
            {'direction':q['direction'],'masses':q['primal']} for q in r['lp_certificates']
            if tuple(map(Q,q['direction'])) in expected]}
    (ROOT/'positive_templates.json').write_text(json.dumps(out,indent=2))

def run():
    prepare();base,groups=system();objective=np.array([0.]*(D-1)+[-1.])
    stats={'nodes':0,'leaves':0,'multipliers':0};started=time.time()
    order=sorted(range(len(groups)),key=lambda i:len(groups[i][1]))
    def solve(rows):
        A=np.array([a for a,b in rows],dtype=float);b=np.array([b for a,b in rows],dtype=float)
        res=linprog(objective,A_ub=A,b_ub=b,bounds=(None,None),method='highs')
        if res.status==2:
            phase=linprog([0.]*D+[1.],A_ub=np.column_stack([A,-np.ones(len(A))]),b_ub=b,
                          bounds=[(None,None)]*D+[(0,None)],method='highs')
            assert phase.status==0 and phase.fun>0
            raw=phase.ineqlin.marginals;target=[0]*D;kind='infeasible'
        elif res.status==0 and res.fun>=-1e-9:
            raw=res.ineqlin.marginals;target=[0]*(D-1)+[-1];kind='nonpositive'
        else:
            assert res.status==0,(res.message,res.status)
            return None
        dual=[(i,Q(float(v)).limit_denominator(10**9)) for i,v in enumerate(raw) if abs(v)>1e-12]
        assert all(q<0 for i,q in dual)
        assert [sum(q*rows[i][0][j] for i,q in dual) for j in range(D)]==target
        value=sum(q*rows[i][1] for i,q in dual)
        assert value>0 if kind=='infeasible' else value>=0
        return {'kind':kind,'dual':[[i,str(q)]for i,q in dual]}
    def visit(rows,remaining):
        stats['nodes']+=1
        cert=solve(rows)
        if cert is not None:
            stats['leaves']+=1;stats['multipliers']+=len(cert['dual']);return cert
        assert remaining, 'FEASIBLE FULL BRANCH'
        idx=remaining[0]
        node={'split':idx,'children':[visit(rows+alt,remaining[1:]) for alt in groups[idx][1]]}
        if stats['nodes']%1000<10:print('progress',stats,'seconds',round(time.time()-started,1),flush=True)
        return node
    tree=visit(base,order)
    result={'statistics':stats,'elapsed_seconds':time.time()-started,'tree':tree}
    (ROOT/'branch_certificate.json').write_text(json.dumps(result,separators=(',',':')))
    print('FINISHED',stats,'seconds',round(time.time()-started,2),flush=True)

if __name__=='__main__':run()
