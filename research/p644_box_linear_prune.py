"""Discover exact linear branch eliminations for an audited box SMT input.

Numerical LPs propose sparse rational dual certificates; every accepted
elimination is checked exactly. This file is discovery, not the independent
mathematical-input or certificate audit.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from scipy.optimize import linprog
from p644_box_input_audit import commands,formula,NAMES


def load_input(path):
    predicates=set()
    for cmd in commands(path.read_text()):
        if cmd[0]=='assert':predicates.add(formula(cmd[1],{}))
    predicates.discard(('true',))
    base=[];groups=[]
    for pred in sorted(predicates,key=repr):
        if pred[0]=='or':groups.append(list(pred[1]))
        else:base.append(pred)
    return base,groups


def rows(atom):
    op,a=atom;row=list(a[:-1])+[F(op=='lt')];rhs=-a[-1]
    if op in ('lt','le'):return [(row,rhs)]
    assert op=='eq'
    return [(row,rhs),([-v for v in row],-rhs)]


def serialize_atom(atom):return [atom[0],list(map(str,atom[1]))]


def run(key,seconds=300):
    source=Path('logs/astra_two_box_general_3_mixed')/(key+'.smt2')
    root=Path('logs/astra_two_box_linear_prune');root.mkdir(exist_ok=True)
    base,groups=load_input(source);original_sizes=list(map(len,groups))
    n=17;objective=[0]*16+[-1]
    A=[];b=[]
    for atom in base:
        for row,rhs in rows(atom):A.append(row);b.append(rhs)
    # The new eta is a common margin for every originally strict atom.
    A.append([F(0)]*16+[F(1)]);b.append(F(1))
    A.append([F(0)]*16+[F(-1)]);b.append(F(0))
    matrix=np.asarray(A,dtype=float);rhsarray=np.asarray(b,dtype=float)
    def refit():
        nonlocal matrix,rhsarray
        matrix=np.asarray(A,dtype=float);rhsarray=np.asarray(b,dtype=float)
    def eliminate(atom=None):
        extra=[] if atom is None else rows(atom)
        M=matrix if not extra else np.vstack([matrix]+[np.asarray(row,dtype=float) for row,rhs in extra])
        h=rhsarray if not extra else np.concatenate([rhsarray,[float(rhs) for row,rhs in extra]])
        result=linprog(objective,A_ub=M,b_ub=h,bounds=[(None,None)]*n,method='highs')
        if result.status==2:
            phase=linprog([0]*n+[1],A_ub=np.column_stack([M,-np.ones(len(M))]),b_ub=h,
                          bounds=[(None,None)]*n+[(0,None)],method='highs')
            if phase.status!=0 or phase.fun<=1e-9:return None
            raw=phase.ineqlin.marginals;kind='infeasible';bound=[0]*n
        elif result.status==0 and result.fun>=-1e-9:
            raw=result.ineqlin.marginals;kind='nonpositive';bound=objective
        else:return None
        all_rows=A+[row for row,rhs in extra];all_rhs=b+[rhs for row,rhs in extra]
        for denominator in (1000000,1000000000):
            dual=[F(float(v)).limit_denominator(denominator) for v in raw]
            if any(v>0 for v in dual):continue
            active=[(i,v) for i,v in enumerate(dual) if v]
            if any(sum(v*all_rows[i][j] for i,v in active)!=bound[j] for j in range(n)):continue
            value=sum(v*all_rhs[i] for i,v in active)
            if value<0 or kind=='infeasible' and value<=0:continue
            return {'kind':kind,'dual':[[i,str(v)] for i,v in active]}
        return None
    steps=[];remaining=[list(range(len(g))) for g in groups];done=set();start=time.time();passes=0;closed=None
    cert=eliminate()
    if cert:closed={'base':cert}
    while closed is None and time.time()-start<seconds:
        changed=False;passes+=1
        for gi,group in enumerate(groups):
            if gi in done:continue
            if any(group[fi] in base for fi in remaining[gi]):done.add(gi);continue
            for fi in remaining[gi][:]:
                cert=eliminate(group[fi])
                if cert:
                    steps.append({'group':gi,'facet':fi,'certificate':cert})
                    remaining[gi].remove(fi);changed=True
            if len(remaining[gi])==0:closed={'empty_group':gi};break
            if len(remaining[gi])==1:
                fi=remaining[gi][0];steps.append({'force_group':gi,'facet':fi})
                base.append(group[fi]);done.add(gi)
                for row,rhs in rows(group[fi]):A.append(row);b.append(rhs)
                refit();changed=True
            if gi%8==0:
                print(key,'pass',passes,'group',gi,'removed',sum(original_sizes)-sum(map(len,remaining)),
                      'forced',len(done),'seconds',round(time.time()-start,2),flush=True)
        if not changed:break
    active=[gi for gi in range(len(groups)) if gi not in done]
    report={'case':key,'source':str(source),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'steps':steps,'remaining':remaining,'done':sorted(done),'closed':closed,
            'passes':passes,'seconds':time.time()-start,'original_sizes':original_sizes,
            'active_sizes':[len(remaining[gi]) for gi in active],
            'independent_verification':'PENDING'}
    (root/(key+'.json')).write_text(json.dumps(report,indent=2))
    def smt_number(v):
        v=F(v)
        if v<0:return '(- %s)'%smt_number(-v)
        return str(v.numerator) if v.denominator==1 else '(/ %d %d)'%(v.numerator,v.denominator)
    def render(atom):
        op,a=atom;terms=['(* %s %s)'%(smt_number(v),name) for name,v in zip(NAMES,a[:-1]) if v]
        if a[-1]:terms.append(smt_number(a[-1]))
        expr='(+ %s)'%' '.join(terms) if len(terms)>1 else terms[0] if terms else '0'
        return '(%s %s 0)'%({'lt':'<','le':'<=','eq':'='}[op],expr)
    text=['(declare-const %s Real)'%name for name in NAMES]
    text += ['(assert %s)'%render(atom) for atom in base]
    for gi in active:text.append('(assert (or %s))'%' '.join(render(groups[gi][fi]) for fi in remaining[gi]))
    if closed:text.append('(assert false)')
    text.append('(check-sat)');(root/(key+'.smt2')).write_text('\n'.join(text)+'\n')
    print('FINISHED',key,'closed',closed,'active sizes',report['active_sizes'],'seconds',round(report['seconds'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case');parser.add_argument('--seconds',type=float,default=300)
    args=parser.parse_args();run(args.case,args.seconds)
