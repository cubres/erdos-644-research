"""Refine the five surviving nonintersecting two-type cases with M5."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from p644_disjoint_two_types import constraints


def run():
    roots=json.loads(Path('logs/astra_disjoint_two_types_fano.json').read_text())['exact_positive_models']
    out=[];models=[]
    for root in roots:
        assert root['parts']==2
        k,l=root['k'],root['l'];states=tuple(root['states']);flip=(k==l==1)
        for r in range(3):
            choices=[states] if r<2 else [states+(q,) for q in ('A','B','ab','ba')]
            for expanded in choices:
                for u,v in ((F(3,2),F(0)),(F(5,4),F(1,2)),(F(1,2),F(1))):
                    if flip:u,v=v,u
                    p=len(expanded);A,b,g=constraints(p,k,l,expanded,True)
                    row=[F(0)]*(3*p+1);row[3*r]=-u;row[3*r+1]=-v;row[3*r+2]=1;row[g]=1
                    A.append(row);b.append(F(0));objective=[0]*(3*p)+[-1]
                    key={'k':k,'l':l,'base_states':states,'states':expanded,'coordinate':r,'facet':[str(u),str(v)],'flip':flip}
                    result=linprog(objective,A_ub=np.array(A,dtype=float),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
                    if result.status==2:
                        phase=linprog([0]*len(objective)+[1],A_ub=np.column_stack([np.array(A,dtype=float),-np.ones(len(A))]),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
                        assert phase.status==0 and phase.fun>0
                        dual=[F(float(v)).limit_denominator(1000000) for v in phase.ineqlin.marginals]
                        assert all(v<=0 for v in dual) and sum(v*w for v,w in zip(dual,b))>0
                        assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=0 for j in range(len(objective)))
                        key.update(dual=list(map(str,dual)),kind='infeasible');out.append(key)
                    elif result.status==0 and result.fun>=-1e-8:
                        dual=[F(float(v)).limit_denominator(1000000) for v in result.ineqlin.marginals]
                        assert all(v<=0 for v in dual) and sum(v*w for v,w in zip(dual,b))>=0
                        assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=objective[j] for j in range(len(objective)))
                        key.update(dual=list(map(str,dual)),kind='nonpositive');out.append(key)
                    else:
                        assert result.status==0
                        point=[F(float(v)).limit_denominator(1000000) for v in result.x]
                        assert point[g]>0 and all(sum(v*w for v,w in zip(row,point))<=rhs for row,rhs in zip(A,b))
                        key['point']=list(map(str,point));models.append(key)
    report={'exact_nonpositive_cases':out,'exact_positive_models':models}
    Path('logs/astra_disjoint_two_types_refine.json').write_text(json.dumps(report,indent=2))
    print('Refined cases',len(out)+len(models),'nonpositive',len(out),'positive',len(models),flush=True)
    if models:print('First remaining method gap:',models[0],flush=True)


if __name__=='__main__':run()
