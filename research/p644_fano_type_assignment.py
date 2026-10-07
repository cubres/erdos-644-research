"""Find Fano bad tuples using any number of actual types or upper type bounds.

Discovery uses MILP only to choose seven row labels. Acceptance checks all
Fano capacity inequalities with exact rational arithmetic. A negative solver
answer is not an independently certified nonexistence result.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds

LINES=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))


def solve(types,caps,seconds=30):
    types=[tuple(map(F,t)) for t in types];caps=list(map(F,caps))
    n=len(types);p=len(caps);rows=[];lower=[];upper=[]
    def add(coeffs,lo,hi):
        row=np.zeros(7*n)
        for j,v in coeffs:row[j]+=float(v)
        rows.append(row);lower.append(lo);upper.append(hi)
    for j in range(7):add([(j*n+a,1) for a in range(n)],1,1)
    for i,x in enumerate(caps):
        for j in range(7):add([(j*n+a,t[i]) for a,t in enumerate(types)],-np.inf,float(x))
        for line in LINES:
            add([(j*n+a,t[i]) for j in line for a,t in enumerate(types)],-np.inf,float(2*x))
        add([(j*n+a,t[i]) for j in range(7) for a,t in enumerate(types)],-np.inf,float(4*x))
    res=milp(np.zeros(7*n),integrality=np.ones(7*n),bounds=Bounds(np.zeros(7*n),np.ones(7*n)),
             constraints=LinearConstraint(np.array(rows),lower,upper),options={'time_limit':seconds})
    report={'scipy_status':res.status,'message':res.message,'status':'UNKNOWN'}
    if res.x is not None:
        labels=[max(range(n),key=lambda a:res.x[j*n+a]) for j in range(7)]
        costs=[max(max(types[a][i] for a in labels),
                   max(sum(types[labels[j]][i] for j in line)/2 for line in LINES),
                   sum(types[a][i] for a in labels)/4) for i in range(p)]
        if all(v<=x for v,x in zip(costs,caps)):
            report.update(status='EXACT_POSITIVE',labels=labels,costs=list(map(str,costs)))
    if res.status==2:report['status']='NUMERICAL_INFEASIBILITY_ONLY'
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--cells',action='store_true')
    args=parser.parse_args();d=json.loads(Path(args.input).read_text())
    types=[hi for lo,hi in d['selected']] if args.cells else d['types']
    result=solve(types,d['capacities']);print(result)
    Path(args.input+'.fano.json').write_text(json.dumps(result,indent=2))
