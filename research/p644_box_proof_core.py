"""Trim a second solver's input to assertions used by the first proof.

This is only a speed aid. The second proof must still be checked externally,
and every proof assumption is checked against the complete original input.
"""
from pathlib import Path
import json
from p644_box_input_audit import commands,formula


def render(e):
    return e if isinstance(e,str) else '('+' '.join(map(render,e))+')'


def extract(key,root=Path('logs/astra_box_case_pipeline')):
    root=Path(root);stem=root/key
    trees=list(commands(stem.with_suffix('.proof').read_text()))
    env={};asserted=[];todo=trees[:]
    while todo:
        e=todo.pop()
        if not isinstance(e,list) or not e:continue
        if e[0]=='let':
            for name,value in e[1]:
                assert name not in env or env[name]==value
                env[name]=value;todo.append(value)
            todo.append(e[2])
        elif e[0]=='asserted':asserted.append(e[1])
        else:todo.extend(e[1:])
    needed={formula(e,env) for e in asserted}
    selected=[];all_inputs=set()
    for cmd in commands(stem.with_suffix('.smt2').read_text()):
        if cmd[0]=='assert':
            c=formula(cmd[1],{});all_inputs.add(c)
            if c in needed:selected.append(cmd)
        elif cmd[0] in ('declare-fun','declare-const','set-logic'):selected.append(cmd)
    assert needed and needed<=all_inputs
    out='\n'.join(render(c) for c in selected if c[0]!='set-logic')+'\n(check-sat)\n'
    stem.with_suffix('.core.smt2').write_text(out)
    info={'case':key,'full_assertions':len(all_inputs),'core_assertions':len(needed)}
    stem.with_suffix('.core.json').write_text(json.dumps(info,indent=2));print(info,flush=True)


if __name__=='__main__':
    import sys
    for key in sys.argv[1:]:extract(key)
