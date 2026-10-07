"""Independent standard-library certificate for arbitrary closed two-part types.

Reconstructs the hand-proved necessary endpoint/gap conditions, certifies
every used bad-support construction, and exhausts every linear branch of
three small saved cores. The fourth endpoint case follows by swapping parts.
No numerical solver or SMT proof inference is trusted by this checker.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import json
import p644_box_input_audit as algebra
from p644_support_capacity_check import check_record
algebra.INDEX={s:i for i,s in enumerate('x y l c gamma a b'.split())}
add,minus,scale,K,var=algebra.add,algebra.minus,algebra.scale,algebra.constant,algebra.variable
ge,gt,atom,boolean=algebra.ge,algebra.gt,algebra.atom,algebra.boolean


def expected(key,shapes):
    x,y,l,c,g,a,b=map(var,range(7));one=K(1);delta=add(x,y,K(-Q(7,4)))
    out={ge(x),ge(y),ge(minus(K(Q(7,4)),x)),ge(minus(K(Q(7,4)),y)),ge(l),ge(minus(one,c)),
         ge(minus(c,l)),ge(minus(x,c)),ge(add(y,l,K(-1))),gt(g),ge(minus(one,g)),
         ge(minus(delta,g)),ge(add(scale(2,delta),l,scale(-1,c),scale(-1,g)))}
    if key[0]=='1':out.add(atom('eq',l))
    else:out.update([ge(minus(l,g)),ge(add(x,scale(-1,l),K(-Q(3,4)),scale(-1,g)))])
    if key[1]=='1':out.add(atom('eq',minus(c,one)))
    else:out.update([ge(add(one,scale(-1,c),scale(-1,g))),ge(add(y,c,K(-Q(7,4)),scale(-1,g)))])
    out.update([ge(minus(a,l)),ge(minus(b,a)),ge(minus(c,b)),
                ge(add(one,scale(-Q(4,7),y),scale(-1,a),scale(-1,g))),
                ge(add(b,scale(-Q(4,7),x),scale(-1,g))),ge(add(delta,a,scale(-1,b),scale(-1,g)))])
    for shape in shapes:
        for s,t in product([l,a,b,c],repeat=2):
            choices=[]
            for u,v in shape:
                choices.extend([ge(add(scale(u,s),scale(v,t),scale(-1,x),scale(-1,g))),
                                ge(add(scale(u,minus(one,s)),scale(v,minus(one,t)),scale(-1,y),scale(-1,g)))])
            out.add(boolean('or',choices))
    out.discard(('true',));return out


def systems(root,shapes):
    for key in ('00','10','11'):
        predicates={algebra.formula(cmd[1],{}) for cmd in algebra.commands((root/(key+'.core.smt2')).read_text()) if cmd[0]=='assert'}
        assert predicates<=expected(key,shapes),('unjustified core assumption',key)
        simple=[];groups=[]
        for f in sorted(predicates,key=repr):
            if f[0]=='or':groups.append(list(f[1]))
            else:simple.append(f)
        for choices in product(*[range(len(g)) for g in groups]):
            A=[];rhs=[]
            for f in simple+[group[j] for group,j in zip(groups,choices)]:
                op,v=f;assert not any(v[7:-1]);row=list(v[:7]);bound=-v[-1]
                if op=='lt':assert row==[Q(0)]*4+[Q(-1),Q(0),Q(0)] and bound==0
                A.append(row);rhs.append(bound)
                if op=='eq':A.append([-q for q in row]);rhs.append(-bound)
            yield key,choices,A,rhs


def constructions(root):
    data=json.loads((root/'templates.json').read_text());shapes=[]
    for key in sorted(data,key=int):
        item=data[key];parents=item['parents']
        assert 1<=len(parents)<=14 and all(0<m<127 for m in parents)
        assert all(a|b!=127 for a in parents for b in parents)
        assert all(any(m>>j&1 for m in parents) for j in range(7))
        shape,_=check_record(item['record'],parents);shapes.append(shape)
    assert len(shapes)==42;return shapes


def check(root=None):
    root=Path(root) if root else Path(__file__).parent/'logs/astra_two_part_gap_central'
    shapes=constructions(root);data=json.loads((root/'exact_duals.json').read_text());records=data['leaves'];seen=set()
    for number,(key,choices,A,b) in enumerate(systems(root,shapes)):
        entry=records[number];assert entry['case']==key and entry['choices']==list(choices)
        signature=(key,choices);assert signature not in seen;seen.add(signature)
        dual={i:Q(v) for i,v in entry['dual']};assert len(dual)==len(entry['dual'])
        assert all(0<=i<len(A) and v<0 for i,v in dual.items())
        total=[sum(v*A[i][j] for i,v in dual.items()) for j in range(7)]
        value=sum(v*b[i] for i,v in dual.items())
        if entry['kind']=='infeasible':assert total==[0]*7 and value>0
        else:
            assert entry['kind']=='nonpositive';assert total==[0]*4+[-1,0,0] and value>=0
    assert len(seen)==len(records)==640
    print('PASS: 640 exhaustive rational dual leaves; all core assumptions reconstructed; 42 bad-support constructions checked; endpoint case 01 is the part-swap of 10.')


if __name__=='__main__':check()
