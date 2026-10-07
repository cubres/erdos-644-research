"""Standard-library audit of exact SMT inputs and CPC assumptions.

Reconstructs the mathematical case systems without importing discovery code.
External Ethos checks proof inference; this checks that its assumptions really
belong to the independently reconstructed mathematical decision problem.
"""
from fractions import Fraction as Q
from pathlib import Path
import itertools,math,re,json,hashlib

NAMES='x0 x1 x2 a0 a1 a2 A0 A1 A2 b0 b1 b2 B0 B1 B2 gamma'.split()
INDEX={s:i for i,s in enumerate(NAMES)};DIM=17


def add(*aa):return tuple(sum(q) for q in zip(*aa))
def scale(c,a):return tuple(c*v for v in a)
def constant(c=0):return (Q(0),)*16+(Q(c),)
def variable(i):return tuple(Q(j==i) for j in range(17))
def minus(a,b):return add(a,scale(-1,b))
X=[variable(i) for i in range(3)];G=variable(15)
L=[[variable(3+6*k+i) for i in range(3)] for k in range(2)]
U=[[variable(6+6*k+i) for i in range(3)] for k in range(2)]


def primitive(a):
    d=1
    for v in a:d=d*v.denominator//math.gcd(d,v.denominator)
    z=[int(v*d) for v in a];g=0
    for v in z:g=math.gcd(g,abs(v))
    return tuple(Q(v,g or 1) for v in z)


def atom(op,a):
    a=primitive(a)
    if not any(a[:-1]):return ('true',) if {'le':a[-1]<=0,'lt':a[-1]<0,'eq':a[-1]==0}[op] else ('false',)
    if op=='eq' and next(v for v in a if v)!=abs(next(v for v in a if v)):a=scale(-1,a)
    return (op,a)


def boolean(op,terms):
    terms=set(terms)
    if op=='or':
        if ('true',) in terms:return ('true',)
        terms.discard(('false',))
    else:
        if ('false',) in terms:return ('false',)
        terms.discard(('true',))
    flat=set()
    for t in terms:
        if t[0]==op:flat.update(t[1])
        else:flat.add(t)
    if not flat:return ('false',) if op=='or' else ('true',)
    if len(flat)==1:return next(iter(flat))
    return (op,tuple(sorted(flat,key=repr)))


def ge(a):return atom('le',scale(-1,a))
def gt(a):return atom('lt',scale(-1,a))


def polygon_fail(couplings,reverse=False):
    """Independent two-variable LP-dual projection."""
    first,second=(1,0) if reverse else (0,1)
    normals=[(-1,0),(0,-1),(1,0),(0,1)]+[(u,v) for u,v,w in couplings]
    directions=set()
    for u,v in [(1,0),(0,1)]+[(u,v) for u,v,w in couplings]:
        g=math.gcd(u,v);directions.add((u//g,v//g))
    failure=[]
    for i in range(3):
        for u,v,w in couplings:failure.append(add(scale(u,L[first][i]),scale(v,L[second][i]),scale(-w,X[i])))
    for target in directions:
        choices=[]
        for i in range(3):
            rhs=[scale(-1,L[first][i]),scale(-1,L[second][i]),U[first][i],U[second][i]]+[scale(w,X[i]) for u,v,w in couplings]
            forms=set()
            # All conic representations using one or two independent normals.
            for inds in itertools.chain(((j,) for j in range(len(normals))),itertools.combinations(range(len(normals)),2)):
                if len(inds)==1:
                    j=inds[0];n=normals[j]
                    nonzero=next((k for k in range(2) if n[k]),None)
                    if nonzero is None:continue
                    weight=Q(target[nonzero],n[nonzero])
                    if weight>=0 and all(weight*n[k]==target[k] for k in range(2)):forms.add(scale(weight,rhs[j]))
                else:
                    j,k=inds;a,b=normals[j],normals[k];det=a[0]*b[1]-a[1]*b[0]
                    if not det:continue
                    w=Q(target[0]*b[1]-target[1]*b[0],det)
                    v=Q(a[0]*target[1]-a[1]*target[0],det)
                    if w>=0 and v>=0:forms.add(add(scale(w,rhs[j]),scale(v,rhs[k])))
            choices.append([a for a in forms if not any(b!=a and all(u<=v for u,v in zip(b,a)) for b in forms)])
        for selected in itertools.product(*choices):failure.append(minus(constant(sum(target)),add(*selected)))
    return set(primitive(f) for f in failure)


def expected(case,line=False):
    result=set()
    for i in range(16):
        result.add(ge(variable(i)))
        result.add(ge(minus(constant(2 if i<3 else Q(1,4) if i==15 else 1),variable(i))))
    result.add(gt(G))
    for k in range(2):
        for i in range(3):
            for f in [minus(U[k][i],L[k][i]),minus(X[i],U[k][i]),
                      minus(add(L[k][i],*(U[k][j] for j in range(3) if j!=i)),constant(1)),
                      minus(constant(1),add(U[k][i],*(L[k][j] for j in range(3) if j!=i)))]:result.add(ge(f))
        result.add(ge(minus(constant(1),add(*L[k]))));result.add(ge(minus(add(*U[k]),constant(1))))
    result.add(ge(add(*X,constant(-Q(7,4)),scale(-1,G))))
    blockers=[]
    for k in range(2):
        bb=[(1<<i,L[k][i],minus(X[i],L[k][i])) for i in range(3)]
        for omitted in range(3):
            mask=7^(1<<omitted);threshold=minus(constant(1),U[k][omitted])
            cost=minus(add(*(X[i] for i in range(3) if i!=omitted)),threshold)
            bb.append((mask,threshold,cost))
        blockers.append(bb)
    for (s,r,a),(t,q,b) in itertools.product(*blockers):
        overlap=add(*(X[i] for i in range(3) if (s&t)>>i&1)) if s&t else constant()
        result.add(boolean('or',[ge(scale(-1,r)),ge(scale(-1,q))]+[
            ge(add(cost,constant(-Q(3,4)),scale(-1,G))) for cost in (a,b,minus(add(a,b),overlap))]))
    for k in range(2):
        failure=[minus(scale(2,L[k][i]),X[i]) for i in range(3)]
        for choice in itertools.product((False,True),repeat=3):
            failure.append(minus(constant(2),add(*(scale(2,U[k][i]) if choice[i] else X[i] for i in range(3)))))
        result.add(boolean('or',[ge(minus(f,G)) for f in failure]))
    menus=[([(1,1,1)],False), ([(1,6,4)],False), ([(1,6,4)],True),
           ([(3,0,2),(5,2,4),(1,2,2)],False), ([(3,0,2),(5,2,4),(1,2,2)],True)]
    if line:menus.extend([([(0,3,2),(4,3,4)],False),([(0,3,2),(4,3,4)],True)])
    for couplings,rev in menus:result.add(boolean('or',[ge(minus(f,G)) for f in polygon_fail(couplings,rev)]))
    for i,state in enumerate(case):
        for k in range(2):result.add(gt(L[k][i]) if state>>k&1 else atom('eq',L[k][i]))
    for i in range(2):
        if case[i]==case[i+1]:result.add(ge(minus(X[i+1],X[i])))
    result.discard(('true',));return result


TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]|[^\s();]+')


def commands(text):
    stack=[]
    for match in TOKEN.finditer(text):
        t=match.group()
        if t.startswith(';'):continue
        if t=='(':stack.append([])
        elif t==')':
            a=stack.pop()
            if stack:stack[-1].append(a)
            else:yield a
        elif stack:stack[-1].append(t)
        else:raise AssertionError(('stray token',t))
    assert not stack


def bind(expr,env,callback):
    new=env.copy()
    for key,value in expr[1]:new[key]=expand(value,env)
    return callback(expr[2],new)


def expand(e,env):
    if isinstance(e,str):return env.get(e,e)
    if e[0]=='let':return bind(e,env,expand)
    return [expand(q,env) for q in e]


def affine(e,env):
    if isinstance(e,str):
        if e in INDEX:return variable(INDEX[e])
        if e in env:return affine(env[e],env)
        return constant(Q(e))
    op=e[0]
    if op=='let':return bind(e,env,affine)
    if op=='+':return add(*(affine(t,env) for t in e[1:]))
    if op=='-':
        terms=[affine(t,env) for t in e[1:]]
        return scale(-1,terms[0]) if len(terms)==1 else add(terms[0],*(scale(-1,t) for t in terms[1:]))
    if op=='*':
        factor=Q(1);term=constant(1)
        for t in e[1:]:
            a=affine(t,env)
            if any(a[:-1]):
                assert not any(term[:-1]);term=a
            else:factor*=a[-1]
        return scale(factor,term)
    if op=='/':
        a,b=[affine(t,env) for t in e[1:]];assert not any(b[:-1]);return scale(1/b[-1],a)
    raise AssertionError(('unsupported arithmetic',op))


def neg(f):
    op=f[0]
    if op=='true':return ('false',)
    if op=='false':return ('true',)
    if op=='le':return atom('lt',scale(-1,f[1]))
    if op=='lt':return atom('le',scale(-1,f[1]))
    if op=='eq':return ('ne',f[1])
    if op in ('and','or'):return boolean('or' if op=='and' else 'and',[neg(t) for t in f[1]])
    raise AssertionError(op)


def formula(e,env):
    if isinstance(e,str):
        if e in ('true','false'):return (e,)
        return formula(env[e],env)
    op=e[0]
    if op=='let':return bind(e,env,formula)
    if op in ('and','or'):return boolean(op,[formula(t,env) for t in e[1:]])
    if op=='not':return neg(formula(e[1],env))
    if op in ('<=','<','>=','>','='):
        a,b=[affine(t,env) for t in e[1:]]
        return atom({'<=':'le','<':'lt','>=':'le','>':'lt','=':'eq'}[op],minus(b,a) if op in ('>=','>') else minus(a,b))
    raise AssertionError(('unsupported Boolean',op))


def audit(key,root=Path('logs/astra_box_case_pipeline')):
    case=tuple(map(int,key[:3]));line=key.endswith('_line')
    target=expected(case,line);actual=set()
    for cmd in commands((root/key).with_suffix('.smt2').read_text()):
        if cmd[0]=='assert':actual.add(formula(cmd[1],{}))
    actual.discard(('true',))
    assert target==actual,('input mismatch',key,len(target-actual),len(actual-target))
    result={'case':key,'input_assertions':len(actual),'input_reconstructed':True}
    proof=(root/key).with_suffix('.cpc')
    if proof.exists():
        env={};assumptions=[]
        for cmd in commands(proof.read_text()):
            if cmd[0]=='define':
                assert cmd[2]==[],('parameterized definition',cmd[:3])
                env[cmd[1]]=cmd[3]
            elif cmd[0]=='assume':assumptions.append(formula(cmd[2],env))
        assert assumptions and all(f in actual or f==('true',) for f in assumptions),('unmatched proof assumption',key)
        result['proof_assumptions']=len(assumptions);result['proof_assumptions_match']=True
    return result


def main():
    root=Path('logs/astra_box_case_pipeline')
    cases=['000','001','003','011','012','013_line','033','111','112','113','123','133','333']
    reps={min(tuple(sorted(q)),tuple(sorted({0:0,1:2,2:1,3:3}[v] for v in q))) for q in itertools.product(range(4),repeat=3)}
    assert {tuple(map(int,k[:3])) for k in cases}==reps and len(reps)==13
    out=[]
    for key in cases:
        result=audit(key,root);out.append(result);print('PASS',result,flush=True)
    (root/'independent_input_audit.json').write_text(json.dumps({'support_patterns':64,'support_orbits':13,'cases':out},indent=2))


if __name__=='__main__':main()
