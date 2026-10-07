"""Complete-support LP discovery with exact positive and negative certificates.

Two sliced boxes may have any number of parts. All 715 maximal supports and
all row assignments modulo support automorphisms are covered. A numerical
failure to reconstruct a rational certificate is UNKNOWN, never HAS_72.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, hstack, csr_matrix
from p644_support_lp_check import (rational_instance,permutation_maps,colour_representatives,
                                  matrix,rhs,check_primal,check_dual,trimmed_cells)


def rationalize(seq):
    for bound in (1000,100000,10000000,1000000000):
        yield [F(float(v)).limit_denominator(bound) for v in seq]


def solve(instance,output,catalogue='logs/astra_full_support_catalog.json'):
    started=time.time();x,boxes,rank=rational_instance(instance);p=len(x)
    data=json.loads(Path(catalogue).read_text());maps=permutation_maps()
    order=sorted(data['orbits'],key=lambda a:(len(a['maximal_cells']),a['truth_table']))
    cert={'instance':instance,'status':'IN_PROGRESS','supports':{}}
    if Path(output).exists():
        old=json.loads(Path(output).read_text())
        assert old['instance']==instance
        if old['status'] in ('BAD_TUPLE','HAS_72'):return old
        cert=old
    counts={'lp':0,'reused_dual':0,'completed_supports':len(cert['supports'])}
    for item in order:
        stem=item['truth_table']
        if stem in cert['supports']:continue
        parents=item['maximal_cells'];colours=colour_representatives(parents,maps)
        rows,n=matrix(parents,p);A=lil_matrix((len(rows),n),dtype=float)
        for i,row in enumerate(rows):
            for j,v in row.items():A[i,j]=v
        # Phase I: min t >= 0, A*v - t <= b, v >= 0.
        phase=hstack([A.tocsr(),csr_matrix(-np.ones((len(rows),1)))],format='csr')
        objective=np.zeros(n+1);objective[-1]=1
        duals=[];assigned={}
        for colour in colours:
            b=rhs(instance,colour);found=None
            for j,d in enumerate(duals):
                if sum(v*w for v,w in zip(d,b))>0:
                    found=j;counts['reused_dual']+=1;break
            if found is not None:assigned[str(colour)]=found;continue
            res=linprog(objective,A_ub=phase,b_ub=list(map(float,b)),bounds=(0,None),method='highs')
            counts['lp']+=1
            if res.status!=0:raise RuntimeError(('UNKNOWN LP status',stem,colour,res.message))
            if abs(res.fun)<1e-8:
                for v in rationalize(res.x[:-1]):
                    try:check_primal(rows,b,v,n)
                    except AssertionError:continue
                    cert={'instance':instance,'status':'BAD_TUPLE','truth_table':stem,'colour':colour,
                          'primal':list(map(str,v)),'trimmed_cells':trimmed_cells(instance,parents,colour,v),
                          'counts':counts,'elapsed':time.time()-started}
                    Path(output).write_text(json.dumps(cert,indent=2))
                    print('EXACT BAD TUPLE',stem,colour,counts,'seconds',round(time.time()-started,2),flush=True)
                    return cert
                raise RuntimeError(('UNKNOWN primal reconstruction',stem,colour))
            for d in rationalize(res.ineqlin.marginals):
                try:check_dual(rows,b,d,n)
                except AssertionError:continue
                duals.append(d);assigned[str(colour)]=len(duals)-1;break
            else:raise RuntimeError(('UNKNOWN dual reconstruction',stem,colour))
        cert['supports'][stem]={'duals':[list(map(str,d)) for d in duals],'colours':assigned}
        counts['completed_supports']+=1;cert['counts']=counts;cert['elapsed']=time.time()-started
        if counts['completed_supports']%25==0:
            Path(output).write_text(json.dumps(cert,indent=2))
            print(counts,'seconds',round(cert['elapsed'],2),flush=True)
    cert['status']='HAS_72';Path(output).write_text(json.dumps(cert,indent=2))
    print('EXACT HAS_72',counts,'seconds',round(time.time()-started,2),flush=True)
    return cert


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('instance');parser.add_argument('--output',required=True)
    parser.add_argument('--catalogue',default='logs/astra_full_support_catalog.json');args=parser.parse_args()
    solve(json.loads(Path(args.instance).read_text()),args.output,args.catalogue)
