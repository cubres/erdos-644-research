"""Discover exact duals for the one-step partner-budget obstruction."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def run():
    menu=json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text());records=[]
    for key in sorted(menu,key=int):
        shape=[tuple(map(F,q)) for q in menu[key]['record']['vertices']];A=[];b=[]
        for i in range(6):
            row=[F(0)]*6;row[i]=1;A.append(row);b.append(F(4,5))
        A += [[F(1)]*3+[F(0)]*3,[-F(1)]*3+[F(0)]*3,[F(0)]*3+[-F(1)]*3]
        b += [F(1),-F(1),-F(33,20)]
        for i in range(3):
            for u,v in shape:
                row=[F(0)]*6;row[i]=v;row[i+3]=u;A.append(row);b.append(F(4,5))
        obj=[-1,0,0,0,0,0];M=np.asarray(A,dtype=float);rhs=list(map(float,b))
        result=linprog(obj,A_ub=M,b_ub=rhs,bounds=(0,None),method='highs')
        if result.status==2:
            phase=linprog([0]*6+[1],A_ub=np.column_stack([M,-np.ones(len(M))]),b_ub=rhs,bounds=(0,None),method='highs')
            assert phase.status==0 and phase.fun>0
            raw=phase.ineqlin.marginals;kind='infeasible';objective=[0]*6
        else:
            assert result.status==0 and result.fun>=-8/15-1e-8
            raw=result.ineqlin.marginals;kind='bound';objective=obj
        dual=[F(float(v)).limit_denominator(10000000) for v in raw];active=[(i,v) for i,v in enumerate(dual) if v]
        assert all(v<0 for i,v in active)
        assert all(sum(v*A[i][j] for i,v in active)<=objective[j] for j in range(6))
        bound=sum(v*b[i] for i,v in active)
        assert bound>0 if kind=='infeasible' else bound>=-F(8,15)
        records.append({'template':key,'kind':kind,'dual':[[i,str(v)] for i,v in active],'certified_lower_bound':str(bound)})
    data={'certificates':records,'coordinate_upper_bound':'8/15','family_threshold':'27/50','family_tau':'39/50'}
    Path('logs/astra_partner_budget_barrier.json').write_text(json.dumps(data,indent=2));print('FINISHED',len(records),'exact dual certificates',flush=True)


if __name__=='__main__':run()
