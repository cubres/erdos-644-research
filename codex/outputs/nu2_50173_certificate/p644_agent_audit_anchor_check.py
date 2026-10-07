"""Independent stdlib input reconstruction, CPC binding, and Ethos replay.

No SMT solver and no discovery/export module is imported. All constants and
support constraints are reconstructed directly from the finite construction.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,math,re,subprocess,tempfile,time

WORK=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work')
ROOT=Path(__file__).parent/'logs/astra_agent_audit_anchor_exact'
SETS={side:{sum(1<<i for i in s):set(s) for r in range(minimum,7)
            for s in combinations(range(6),r)}for side,minimum in [('a',3),('b',2)]}
NAMES={side+'_'+str(m)for side in SETS for m in SETS[side]}

def add(*terms):
    out={}
    for a in terms:
        for k,v in a.items():out[k]=out.get(k,Q(0))+v
    return {k:v for k,v in out.items()if v}
def scale(c,a):return {k:c*v for k,v in a.items()if c*v}
def const(c):return {'':Q(c)}if c else {}
def var(n):assert n in NAMES;return {n:Q(1)}
def sub(a,b):return add(a,scale(-1,b))
def atom(op,a):
    den=1
    for v in a.values():den=den*v.denominator//math.gcd(den,v.denominator)
    terms=sorted((k,int(v*den))for k,v in a.items()if v);g=0
    for _,v in terms:g=math.gcd(g,abs(v))
    terms=tuple((k,v//(g or 1))for k,v in terms)
    if not any(k for k,v in terms):
        c=dict(terms).get('',0)
        return ('true',)if {'le':c<=0,'lt':c<0,'eq':c==0}[op]else('false',)
    if op=='eq' and terms[0][1]<0:terms=tuple((k,-v)for k,v in terms)
    return op,terms
def boolean(op,terms):
    flat=set()
    for t in terms:
        if t[0]==op:flat.update(t[1])
        else:flat.add(t)
    absorbing=('true',)if op=='or'else('false',)
    identity=('false',)if op=='or'else('true',)
    if absorbing in flat:return absorbing
    flat.discard(identity)
    if not flat:return identity
    if len(flat)==1:return next(iter(flat))
    return op,tuple(sorted(flat,key=repr))
def le(a,b):return atom('le',sub(a,b))
def eq(a,b):return atom('eq',sub(a,b))

def expected():
    ans={le({},var(n))for n in NAMES}
    for side in SETS:ans.add(eq(add(*(var(side+'_'+str(m))for m in SETS[side])),const(121800)))
    aa=list(SETS['a'])
    for i,m in enumerate(aa):
        for n in aa[i+1:]:
            if SETS['a'][m].isdisjoint(SETS['a'][n]):
                ans.add(boolean('or',[eq(var('a_'+str(m)),{}),eq(var('a_'+str(n)),{})]))
        for n in SETS['b']:
            if SETS['a'][m].isdisjoint(SETS['b'][n]):
                ans.add(boolean('or',[eq(var('a_'+str(m)),{}),eq(var('b_'+str(n)),{})]))
    intervals=[(18200,54586),(57660,57660),(60914,61054),(64155,75845),
               (78946,79086),(82340,82340),(85414,121800)]
    traces=[]
    for i in range(6):
        da=add(*(var('a_'+str(m))for m,s in SETS['a'].items()if i in s))
        db=add(*(var('b_'+str(m))for m,s in SETS['b'].items()if i in s))
        ans.add(eq(add(da,db),const(103600)))
        t=sub(const(121800),da);traces.append(t)
        ans.add(boolean('or',[boolean('and',[le(const(lo),t),le(t,const(hi))])for lo,hi in intervals]))
    for i in range(5):ans.add(le(traces[i],traces[i+1]))
    return ans

TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]|[^\s();]+')
def commands(text):
    stack=[]
    for match in TOKEN.finditer(text):
        t=match.group()
        if t.startswith(';'):continue
        if t=='(':stack.append([])
        elif t==')':
            assert stack;a=stack.pop()
            if stack:stack[-1].append(a)
            else:yield a
        elif stack:stack[-1].append(t)
        else:raise AssertionError(('stray token',t))
    assert not stack
def expand(e,env):
    if isinstance(e,str):return env.get(e,e)
    if e[0]=='let':
        new=env.copy()
        for n,v in e[1]:new[n]=expand(v,env)
        return expand(e[2],new)
    return [expand(v,env)for v in e]
def affine(e,env):
    if isinstance(e,str):
        if e in NAMES:return var(e)
        if e in env:return affine(env[e],env)
        return const(Q(e))
    if e[0]=='let':return affine(expand(e,env),{})
    op=e[0];v=[affine(t,env)for t in e[1:]]
    if op=='+':return add(*v)
    if op=='-':return scale(-1,v[0])if len(v)==1 else add(v[0],*(scale(-1,t)for t in v[1:]))
    if op=='/':assert len(v)==2 and not any(v[1]);return scale(1/v[1].get('',0),v[0])
    if op=='*':
        out=const(1)
        for a in v:
            if any(a):assert not any(out);out=scale(out.get('',0),a)
            else:out=scale(a.get('',0),out)
        return out
    raise AssertionError(('unsupported arithmetic',e))
def formula(e,env):
    if isinstance(e,str):
        if e in ('true','false'):return(e,)
        return formula(env[e],env)
    op=e[0]
    if op=='let':return formula(expand(e,env),{})
    if op in('and','or'):return boolean(op,[formula(t,env)for t in e[1:]])
    if op in('<=','<','>=','>','='):
        a,b=[affine(t,env)for t in e[1:]]
        return atom({'<=':'le','<':'lt','>=':'le','>':'lt','=':'eq'}[op],sub(b,a)if op in('>=','>')else sub(a,b))
    raise AssertionError(('unsupported formula',e))

def check(root,ethos,signatures):
    start=time.time();root=Path(root)
    source=(root/'residual.smt2').read_text();proof=(root/'residual.cpc').read_text()
    target=expected();actual=set();declared=set()
    for cmd in commands(source):
        if cmd[0]=='assert':actual.add(formula(cmd[1],{}))
        elif cmd[0]=='declare-fun':assert cmd[2:]==[[],'Real'];declared.add(cmd[1])
        else:assert cmd[0]in('check-sat','set-info')
    assert declared==NAMES
    assert actual==target,('input mismatch',len(target-actual),len(actual-target))
    env={};assumptions=[];proof_names=set();counts={}
    allowed={'include','declare-const','define','assume','assume-push','step','step-push','step-pop'}
    for cmd in commands(proof):
        op=cmd[0];assert op in allowed;counts[op]=counts.get(op,0)+1
        if op=='define':assert cmd[2]==[];assert cmd[1]not in env;env[cmd[1]]=cmd[3]
        elif op=='assume':assumptions.append(formula(cmd[2],env))
        elif op=='declare-const':assert cmd[2]=='Real';proof_names.add(cmd[1])
    assert proof_names==NAMES
    assert assumptions and all(a in target or a==('true',)for a in assumptions)
    assert counts.get('include')==2
    assert counts.get('assume-push',0)+counts.get('step-push',0)==counts.get('step-pop',0)
    assert not re.search(r':rule\s+(?:trust|hole|oracle)\b',proof)
    assert re.search(r'^\(step\s+\S+\s+false\s+:rule\s+',proof.rstrip().splitlines()[-1])
    lines=proof.splitlines(keepends=True);assert all(lines[i].startswith('(include ')for i in(0,1))
    sig=Path(signatures).resolve()
    portable='(include "%s")\n(include "%s")\n'%(sig/'Cpc.eo',sig/'expert/CpcExpert.eo')+''.join(lines[2:])
    # The temporary directory is newly created and contains only this proof.
    with tempfile.TemporaryDirectory(prefix='p644-new-anchor-proof-')as tmp:
        p=Path(tmp)/'residual.cpc';p.write_text(portable)
        r=subprocess.run([str(Path(ethos).resolve()),str(p)],capture_output=True,text=True,timeout=240)
    assert r.returncode==0 and r.stdout.strip()=='correct',(r.returncode,r.stdout,r.stderr)
    report={'status':'PASS','source_reconstructed':True,'source_assertions':len(target),
            'proof_assumptions_bound':len(assumptions),'external_checker':'Ethos: correct',
            'conclusion':'false','elapsed_seconds':time.time()-start,
            'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'proof_sha256':hashlib.sha256(proof.encode()).hexdigest()}
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(ROOT))
    p.add_argument('--ethos',default=str(WORK/'proof_checkers/ethos-0.2.4/ethos'))
    p.add_argument('--signatures',default=str(WORK/'proof_checkers/cvc5-1.4.0-signatures/cpc'))
    p.add_argument('--report');a=p.parse_args();result=check(a.root,a.ethos,a.signatures)
    if a.report:Path(a.report).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
