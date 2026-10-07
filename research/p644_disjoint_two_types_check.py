"""Independent exact audit of the nonintersecting two-fixed-type proof tree."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from p644_support_capacity_check import check_record


def base_matrix(k,l,states):
    p=len(states);width=3*p+1;gamma=width-1;rows=[];rhs=[]
    def add(entries,bound):
        row=[F(0)]*width
        for position,value in entries:row[position]+=F(value)
        rows.append(row);rhs.append(F(bound))
    a=[3*i for i in range(p)];b=[i+1 for i in a];x=[i+2 for i in a]
    add([(i,1) for i in a],1);add([(i,1) for i in b],1);add([(gamma,1)],1)
    for i,state in enumerate(states):
        add([(a[i],1),(b[i],1),(x[i],-1)],0)
        if state=='A':add([(b[i],1)],0);add([(gamma,1),(a[i],-1)],0)
        elif state=='B':add([(a[i],1)],0);add([(gamma,1),(b[i],-1)],0)
        else:
            assert state in ('ab','ba')
            add([(gamma,1),(a[i],-1)],0);add([(gamma,1),(b[i],-1)],0)
            small,big=(b[i],a[i]) if state=='ab' else (a[i],b[i])
            add([(small,1),(big,-1)],0)
            add([(x[i],-1),(small,1),(gamma,1)],-F(3,4))
    for i in range(p):
        for j in range(p):
            if i!=j and states[i]!='B' and states[j]!='A':
                add([(x[i],-1),(a[i],1),(x[j],-1),(b[j],1),(gamma,1)],-F(3,4))
    add([(x[0],1),(a[0],-F(3,2)),(b[0],-F(1,4)),(gamma,1)],0)
    add([(x[1],1),(a[1],-F(1,4)),(b[1],-F(3,2)),(gamma,1)],0)
    add([(x[k],1),(a[k],-F(6,5)),(b[k],-1),(gamma,1)],0)
    add([(x[l],1),(a[l],-1),(b[l],-F(6,5)),(gamma,1)],0)
    return rows,rhs,gamma


def dual_check(A,b,g,entry):
    y=list(map(F,entry['dual']));assert len(y)==len(A) and all(v<=0 for v in y)
    coefficients=[sum(v*row[j] for v,row in zip(y,A)) for j in range(len(A[0]))]
    bound=sum(v*w for v,w in zip(y,b));kind=entry.get('kind',entry.get('status'))
    if kind=='infeasible':assert bound>0 and all(v<=0 for v in coefficients)
    else:
        assert kind in ('nonpositive',)
        assert bound>=0 and all(v<=(-1 if j==g else 0) for j,v in enumerate(coefficients))


def run():
    base=Path(__file__).parent/'logs'
    roots=json.loads((base/'astra_disjoint_two_types_fano.json').read_text())
    tree=json.loads((base/'astra_two_type_recursive/tree.json').read_text())
    templates=json.loads((base/'astra_two_type_recursive/templates.json').read_text())
    shapes={}
    for key,item in templates.items():
        parents=item['parents'];assert parents and all(0<m<127 for m in parents)
        assert all(a|b!=127 for a in parents for b in parents)
        assert all(any(m>>j&1 for m in parents) for j in range(7))
        shape,_=check_record(item['record'],parents);shapes[int(key)]=shape
    expected=set()
    for p in (2,3,4):
        for k,l in product(range(p),repeat=2):
            if {0,1,k,l}!=set(range(p)):continue
            for states in product(('A','B','ab','ba'),repeat=p):
                if states[0] in ('A','ab') and states[1] in ('B','ba') and states[k]!='B' and states[l]!='A':
                    expected.add((k,l,states))
    found=set()
    for entry in roots['exact_nonpositive_cases']+roots['exact_positive_models']:
        key=(entry['k'],entry['l'],tuple(entry['states']));assert key in expected and key not in found;found.add(key)
        if 'dual' in entry:dual_check(*base_matrix(*key),entry)
    assert found==expected and len(found)==125
    nodes={n['id']:n for n in tree['nodes']};seen=set();leaves=0;splits=0
    def visit(number,k,l,states,witnesses):
        nonlocal leaves,splits
        assert number not in seen;seen.add(number);node=nodes[number]
        assert (node['k'],node['l'],tuple(node['states']))==(k,l,states)
        assert [tuple(w) for w in node['witnesses']]==witnesses
        A,b,g=base_matrix(k,l,states);p=len(states)
        for template,coordinate,facet in witnesses:
            u,v=shapes[template][facet];row=[F(0)]*(3*p+1)
            row[3*coordinate]=-u;row[3*coordinate+1]=-v;row[3*coordinate+2]=1;row[g]=1
            A.append(row);b.append(F(0))
        if node['status']!='split':dual_check(A,b,g,node);leaves+=1;return
        splits+=1;t=node['template'];assert t in shapes
        choices={(coordinate,state,facet) for coordinate in range(p+1)
                 for state in ([None] if coordinate<p else ['A','B','ab','ba'])
                 for facet in range(len(shapes[t]))}
        got=set()
        for child in node['children']:
            c,s,f=child['coordinate'],child['state'],child['facet'];assert (c,s,f) in choices and (c,s,f) not in got;got.add((c,s,f))
            expanded=states if c<p else states+(s,)
            visit(child['child'],k,l,expanded,witnesses+[(t,c,f)])
        assert got==choices
    assert len(tree['roots'])==len(roots['exact_positive_models'])==5
    for number,entry in zip(tree['roots'],roots['exact_positive_models']):visit(number,entry['k'],entry['l'],tuple(entry['states']),[])
    assert seen==set(nodes) and len(seen)==107 and leaves==101 and splits==6
    print('PASS: all 125 root cases; 120 root duals; complete 107-node refinement with 101 exact leaf duals and 6 splits; three construction templates independently checked.')


if __name__=='__main__':run()
