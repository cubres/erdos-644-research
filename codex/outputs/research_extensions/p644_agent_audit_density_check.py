"""Stdlib-only exact certificate for the two-part quantitative density bridge.

Eight explicit positive two-type constructions and the hand 1:4:2 Fano lemma
are the entire construction menu. No complete support catalogue is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent / 'logs/astra_agent_audit_density'
D = 8
NAMES = 'x y l c a b g gamma'.split()

def K(c=0): return (Q(0),)*D + (Q(c),)
def V(i): return tuple(Q(j == i) for j in range(D))+(Q(0),)
def add(*args): return tuple(map(sum, zip(*args)))
def mul(c,a): return tuple(Q(c)*v for v in a)
def sub(a,b): return add(a,mul(-1,b))
def ge(a): return tuple(-v for v in a[:D]), a[-1]
def eq(a): return [ge(a),ge(mul(-1,a))]

SHAPES = {
 0:[('0','1'),('3/2','1/4')],
 1:[('1/4','3/2'),('1','0')],
 2:[('1/2','1'),('5/4','1/2'),('3/2','0')],
 5:[('0','3/2'),('1/2','5/4'),('1','1/2')],
 6:[('1/2','1'),('9/8','3/4'),('5/4','1/2'),('4/3','0')],
 7:[('0','4/3'),('1/2','5/4'),('3/4','9/8'),('1','1/2')],
 8:[('0','3/2'),('1','3/4')],
 9:[('3/4','1'),('3/2','0')],
}

def positive_constructions(root=ROOT):
    data=json.loads((root/'positive_templates.json').read_text())
    assert set(data)=={str(i) for i in SHAPES}
    for key,shape in SHAPES.items():
        item=data[str(key)];parents=item['parents'];colour=item['colour']
        shape=[tuple(map(Q,p)) for p in shape]
        assert 0<=colour<=127 and 1<=len(parents)<=14
        assert all(0<m<127 for m in parents)
        assert all(a|b!=127 for a in parents for b in parents)
        expected={(Q(0),Q(1)),(Q(1),Q(0))}
        for left,right in zip(shape,shape[1:]):
            a=left[1]-right[1];b=right[0]-left[0]
            assert a>0 and b>0
            expected.add((a/(a+b),b/(a+b)))
        certs={}
        for cert in item['primal']:
            direction=tuple(map(Q,cert['direction']))
            masses=list(map(Q,cert['masses']))
            assert direction in expected and direction not in certs
            assert len(masses)==len(parents) and min(masses)>=0
            demand=[direction[(colour>>j)&1] for j in range(7)]
            assert all(sum(v for v,m in zip(masses,parents) if m>>j&1)>=demand[j] for j in range(7))
            value=max(u*direction[0]+v*direction[1] for u,v in shape)
            assert sum(masses)==value
            certs[direction]=value
        assert set(certs)==expected
        # A common maximizing form on adjacent rays proves linearity of M there.
        rays=sorted(expected)
        for first,last in zip(rays,rays[1:]):
            assert any(all(u*d[0]+v*d[1]==certs[d] for d in (first,last)) for u,v in shape)
    return len(data)

def system():
    x,y,l,c,a,b,g,z=map(V,range(D));one=K(1)
    base=[]
    for v in (x,y,l,c,a,b,g,z): base.append(ge(v))
    for v in (l,c,a,b,g,z): base.append(ge(sub(one,v)))
    for v in (x,y): base.append(ge(sub(K(Q(7,4)),v)))
    base += [ge(sub(x,c)),ge(add(y,l,K(-1))),ge(sub(a,l)),ge(sub(b,a)),
             ge(sub(c,b)),ge(add(g,a,mul(-1,b))),ge(add(c,mul(-1,l),mul(-1,g)))]
    base += [ge(add(x,y,mul(-1,g),K(-Q(5,3)),mul(-1,z))),
             ge(add(mul(2,x),mul(2,y),mul(-1,g),K(-Q(7,2)),mul(-1,z))),
             ge(add(one,mul(-Q(4,7),y),mul(-1,a),mul(-1,z))),
             ge(add(b,mul(-Q(4,7),x),mul(-1,z)))]
    groups=[]
    groups.append(('left_cover',[eq(l),[ge(add(one,g,mul(-1,y),mul(-1,l)))]]))
    groups.append(('right_cover',[eq(sub(c,one)),[ge(add(c,g,mul(-1,x)))]]))
    for key,s,t in [(0,a,b),(1,l,b),(2,a,b),(5,a,b),(6,a,b),(7,a,b),(8,a,b),(9,a,b)]:
        alts=[]
        for u,v in SHAPES[key]:
            u,v=Q(u),Q(v)
            alts += [[ge(add(mul(u,s),mul(v,t),mul(-1,x),mul(-1,z)))],
                     [ge(add(mul(u,sub(one,s)),mul(v,sub(one,t)),mul(-1,y),mul(-1,z)))]]
        groups.append(('M'+str(key),alts))
    for name,A,B,C,X,Y in [('T_l_a_c',l,a,c,x,y),
                         ('R_l_b_c',sub(one,c),sub(one,b),sub(one,l),y,x)]:
        excesses=[add(C,mul(Q(1,2),A),mul(-1,X)),
                  add(B,mul(Q(1,2),C),mul(Q(1,4),A),mul(-1,X)),
                  add(one,mul(-1,A),mul(-1,Y)),
                  add(K(Q(3,2)),mul(-Q(1,2),A),mul(-1,B),mul(-1,Y)),
                  add(K(Q(7,4)),mul(-Q(1,4),A),mul(-1,B),mul(-Q(1,2),C),mul(-1,Y))]
        groups.append((name,[[ge(add(f,mul(-1,z)))] for f in excesses]))
    return base,groups

def check(root=ROOT):
    root=Path(root);construction_count=positive_constructions(root)
    base,groups=system();data=json.loads((root/'branch_certificate.json').read_text())
    stats={'nodes':0,'leaves':0,'multipliers':0}
    def visit(node,rows,used):
        stats['nodes']+=1
        if 'dual' in node:
            dual=[(i,Q(q)) for i,q in node['dual']]
            assert len({i for i,q in dual})==len(dual)
            assert dual and all(0<=i<len(rows) and q<0 for i,q in dual)
            lhs=[sum(q*rows[i][0][j] for i,q in dual) for j in range(D)]
            rhs=sum(q*rows[i][1] for i,q in dual)
            if node['kind']=='infeasible':assert lhs==[0]*D and rhs>0
            else:
                assert node['kind']=='nonpositive'
                assert lhs==[0]*(D-1)+[-1] and rhs>=0
            stats['leaves']+=1;stats['multipliers']+=len(dual)
            return
        idx=node['split'];assert 0<=idx<len(groups) and idx not in used
        assert len(node['children'])==len(groups[idx][1])
        for child,alternative in zip(node['children'],groups[idx][1]):
            visit(child,rows+alternative,used|{idx})
    visit(data['tree'],base,set())
    assert stats==data['statistics']
    print('PASS:',construction_count,'positive two-type constructions;',stats,
          '; every Boolean branch closed by exact rational arithmetic.')
    return stats

if __name__=='__main__':check()
