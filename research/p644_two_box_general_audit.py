"""Independent mathematical-input audit for the general three-part two-box search."""
from pathlib import Path
import itertools
import json
from p644_box_input_audit import (expected,boolean,ge,minus,polygon_fail,G,L,U,X,
                                scale,constant,add,commands,formula)


def target(case,mixed=False):
    result=expected(case,line=True)
    cross=boolean('or',[ge(minus(f,G)) for f in polygon_fail([(1,1,1)])])
    assert cross in result;result.remove(cross)
    if mixed:
        for f in polygon_fail([(1,1,1)]):result.add(ge(scale(-1,f)))
    for k in range(2):
        failures=[minus(scale(7,L[k][i]),scale(4,X[i])) for i in range(3)]
        for choices in itertools.product((False,True),repeat=3):
            failures.append(minus(constant(7),add(*(scale(7,U[k][i]) if choices[i] else scale(4,X[i]) for i in range(3)))))
        result.add(boolean('or',[ge(minus(f,G)) for f in failures]))
    menus=[[(3,0,2),(4,3,4),(1,2,2)],[(2,3,3),(8,3,6)],[(6,5,5)],
           [(5,6,6),(4,3,4),(4,0,3)],[(2,5,4),(1,1,1)]]
    for menu in menus:
        for flip in (False,True):result.add(boolean('or',[ge(minus(f,G)) for f in polygon_fail(menu,flip)]))
    return result


def audit(key,root=Path('logs/astra_two_box_general_3'),mixed=False):
    wanted=target(tuple(map(int,key)),mixed);actual=set()
    for command in commands((root/key).with_suffix('.smt2').read_text()):
        if command[0]=='assert':actual.add(formula(command[1],{}))
    actual.discard(('true',));assert wanted==actual,('input mismatch',key,len(wanted-actual),len(actual-wanted))
    result={'case':key,'input_assertions':len(actual),'input_reconstructed':True}
    proof=(root/key).with_suffix('.cpc')
    if proof.exists():
        env={};assumptions=[]
        for command in commands(proof.read_text()):
            if command[0]=='define':
                assert command[2]==[];env[command[1]]=command[3]
            elif command[0]=='assume':assumptions.append(formula(command[2],env))
        assert assumptions and all(f in actual or f==('true',) for f in assumptions)
        result.update(proof_assumptions=len(assumptions),proof_assumptions_match=True)
    return result


def main(mixed=False):
    cases=sorted({min(tuple(sorted(s)),tuple(sorted({0:0,1:2,2:1,3:3}[v] for v in s))) for s in itertools.product(range(4),repeat=3)})
    assert len(cases)==13
    results=[]
    for case in cases:
        key=''.join(map(str,case));root=Path('logs/astra_two_box_general_3'+('_mixed' if mixed else ''))
        row=audit(key,root,mixed);results.append(row);print('PASS',row,flush=True)
    (root/'input_audit.json').write_text(json.dumps(results,indent=2))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--mixed',action='store_true');args=parser.parse_args();main(args.mixed)
