"""Independent standard-library replay of rational disjunct pruning.

The source is reconstructed by the independent mathematical input audit.
Strict inequalities share a fresh positive margin. Sparse rational Farkas
vectors certify every deleted alternative; forced alternatives are recorded.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
from p644_box_input_audit import commands,formula,boolean
from p644_two_box_general_audit import target


def predicates(path):
    return {formula(c[1],{}) for c in commands(path.read_text()) if c[0]=='assert'}-{('true',)}


def replay(key):
    root=Path('logs/astra_two_box_linear_prune');data=json.loads((root/(key+'.json')).read_text())
    source=Path(data['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==data['input_sha256']
    original=predicates(source);assert original==target(tuple(map(int,key)),mixed=True)
    simple=[];choices=[]
    for f in sorted(original,key=repr):
        (choices if f[0]=='or' else simple).append(list(f[1]) if f[0]=='or' else f)
    assert list(map(len,choices))==data['original_sizes']
    inequalities=[]
    def append(f,out):
        op,v=f;lhs=list(v[:-1])+[Q(op=='lt')];rhs=-v[-1]
        assert op in ('le','lt','eq');out.append((lhs,rhs))
        if op=='eq':out.append(([-a for a in lhs],-rhs))
    for f in simple:append(f,inequalities)
    inequalities += [([Q(0)]*16+[Q(1)],Q(1)),([Q(0)]*16+[Q(-1)],Q(0))]
    def dual_check(cert,facet=None):
        rr=inequalities[:]
        if facet is not None:append(facet,rr)
        dual={i:Q(v) for i,v in cert['dual']}
        assert len(dual)==len(cert['dual']) and all(0<=i<len(rr) and v<0 for i,v in dual.items())
        kind=cert['kind'];assert kind in ('infeasible','nonpositive')
        combined=[sum(v*rr[i][0][j] for i,v in dual.items()) for j in range(17)]
        wanted=[Q(0)]*17
        if kind=='nonpositive':wanted[-1]=-1
        assert combined==wanted
        rhs=sum(v*rr[i][1] for i,v in dual.items())
        assert rhs>0 if kind=='infeasible' else rhs>=0
    remaining=[set(range(len(g))) for g in choices];forced=set();count=0
    for step in data['steps']:
        if 'group' in step:
            g,f=step['group'],step['facet'];assert g not in forced and f in remaining[g]
            dual_check(step['certificate'],choices[g][f]);remaining[g].remove(f);count+=1
        else:
            g,f=step['force_group'],step['facet'];assert g not in forced and remaining[g]=={f}
            forced.add(g);simple.append(choices[g][f]);append(choices[g][f],inequalities)
    assert [sorted(q) for q in remaining]==data['remaining']
    done=set(data['done']);assert forced<=done
    for g in done-forced:assert any(choices[g][f] in simple for f in remaining[g])
    closed=data['closed']
    if closed:
        if 'base' in closed:dual_check(closed['base'])
        else:assert not remaining[closed['empty_group']]
    expected=set(simple)
    for g,group in enumerate(choices):
        if g not in done:expected.add(boolean('or',[group[f] for f in remaining[g]]))
    if closed:expected.add(('false',))
    expected.discard(('true',))
    assert predicates(root/(key+'.smt2'))==expected
    proof=root/(key+'.cpc')
    if proof.exists():
        env={};assumptions=[]
        for cmd in commands(proof.read_text()):
            if cmd[0]=='define':assert cmd[2]==[];env[cmd[1]]=cmd[3]
            elif cmd[0]=='assume':assumptions.append(formula(cmd[2],env))
        assert assumptions and all(f in expected or f==('true',) for f in assumptions)
    print('PASS',key,'exact branch eliminations',count,'forced',len(forced),'source and reduced input reconstructed',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('cases',nargs='*',default=['033','123','333'])
    args=parser.parse_args()
    for key in args.cases:replay(key)
