"""Resumable recursive splitting of saved exact linear-arithmetic cases.

Every split uses all children of an OR already asserted at the parent. This
is a complete logical partition (overlap is harmless). UNKNOWN leaves remain
open. Generated solver proofs still require separate external verification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


def refine(source, choices, seconds=10):
    source=Path(source);root=source.parent/(source.stem+'_refine');root.mkdir(exist_ok=True)
    z3.set_param(proof=True)
    assertions=z3.parse_smt2_file(str(source));ors=[q for q in assertions if z3.is_or(q)]
    for i in choices:assert 0<=i<len(ors)
    solver=z3.SolverFor('QF_LRA');solver.set(timeout=int(seconds*1000));solver.add(*assertions)
    counts={'unsat':0,'sat':0,'unknown':0,'split':0,'cached':0};started=time.time()

    def visit(path,depth):
        key='root' if not path else '_'.join('%d-%d'%q for q in path)
        target=root/(key+'.json');text=solver.to_smt2();digest=hashlib.sha256(text.encode()).hexdigest()
        old=None
        if target.exists():
            old=json.loads(target.read_text())
            if old.get('input_sha256')==digest and old['answer'] in ('sat','unsat'):
                counts[old['answer']]+=1;counts['cached']+=1;return old['answer']
        begin=time.time()
        prior_split=(old is not None and old.get('input_sha256')==digest and old.get('answer')=='split'
                     and depth<len(choices) and old.get('or_index')==choices[depth])
        answer=z3.unknown if prior_split else solver.check()
        record={'path':path,'answer':str(answer),'seconds':time.time()-begin,'input_sha256':digest}
        if answer==z3.unsat:
            proof=solver.proof().sexpr();(root/(key+'.proof')).write_text(proof)
            (root/(key+'.smt2')).write_text(text)
            record['proof_sha256']=hashlib.sha256(proof.encode()).hexdigest()
            record['external_verification']='PENDING';counts['unsat']+=1
        elif answer==z3.sat:
            record['model']=str(solver.model());(root/(key+'.smt2')).write_text(text);counts['sat']+=1
        elif depth<len(choices):
            index=choices[depth];clause=ors[index];children=[];counts['split']+=1
            record.update(answer='split',or_index=index,arity=clause.num_args())
            for child in range(clause.num_args()):
                solver.push();solver.add(clause.arg(child))
                result=visit(path+[(index,child)],depth+1);children.append(result);solver.pop()
            record['children']=children
            record['subtree_status']='unsat' if all(q=='unsat' for q in children) else 'open'
        else:
            record['reason']=solver.reason_unknown();counts['unknown']+=1
            (root/(key+'.smt2')).write_text(text)
        target.write_text(json.dumps(record,indent=2))
        status=record.get('subtree_status',record['answer'])
        print(key,status,round(record['seconds'],3),'counts',counts,flush=True)
        (root/'status.json').write_text(json.dumps({'counts':counts,'elapsed':time.time()-started,'source':str(source),'split_or_indices':choices},indent=2))
        return status

    status=visit([],0)
    print('FINISHED',status,counts,flush=True)
    return status


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('--or-indices',type=int,nargs='+',required=True)
    parser.add_argument('--seconds',type=float,default=10);args=parser.parse_args()
    refine(args.source,args.or_indices,args.seconds)
