"""Discover rational duals for the reduced closed-two-part-type proof."""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import linprog
from p644_two_part_gap_check import systems,constructions


def run():
    root=Path('logs/astra_two_part_gap_central');shapes=constructions(root);records=[];started=time.time()
    objective=[0]*4+[-1,0,0]
    for key,choices,A,b in systems(root,shapes):
        M=np.asarray(A,dtype=float);rhs=np.asarray(b,dtype=float)
        result=linprog(objective,A_ub=M,b_ub=rhs,bounds=(None,None),method='highs')
        if result.status==2:
            phase=linprog([0]*7+[1],A_ub=np.column_stack([M,-np.ones(len(M))]),b_ub=rhs,
                          bounds=[(None,None)]*7+[(0,None)],method='highs')
            assert phase.status==0 and phase.fun>0
            raw=phase.ineqlin.marginals;kind='infeasible';bound=[0]*7
        else:
            assert result.status==0 and result.fun>=-1e-8,(key,choices,result.message,result.fun)
            raw=result.ineqlin.marginals;kind='nonpositive';bound=objective
        dual=[F(float(q)).limit_denominator(10000000) for q in raw];active=[(i,q) for i,q in enumerate(dual) if q]
        assert all(q<0 for i,q in active)
        assert all(sum(q*A[i][j] for i,q in active)==bound[j] for j in range(7))
        value=sum(q*b[i] for i,q in active);assert value>0 if kind=='infeasible' else value>=0
        records.append({'case':key,'choices':choices,'kind':kind,'dual':[[i,str(q)] for i,q in active]})
    (root/'exact_duals.json').write_text(json.dumps({'leaves':records,'elapsed':time.time()-started},indent=2))
    print('FINISHED',len(records),'exact duals; seconds',round(time.time()-started,2),flush=True)


if __name__=='__main__':run()
