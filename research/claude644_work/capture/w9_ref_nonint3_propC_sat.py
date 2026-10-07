"""Referee w9, nonint#3: independent SAT check (pysat, Cadical/Glucose) that small Prop C families are (7,2),
supporting the tightness claim of Lemma H/Prop B. H = C(U,k) u C(U1,k) u C(U2,k); a 7-tuple = j core rows,
a K1-rows, b K2-rows (repeats allowed, so exactly 7 rows covers all <=7-subfamilies). SAT <=> bad tuple exists.
Row-lex symmetry breaking is NOT used (plain encoding, independent of nonint2/fat797_sat.py)."""
import sys, itertools, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
def instance(k,s,c,d):
    U=list(range(k+s)); C1=U[:c]; C2=U[c:2*c]; nxt=k+s
    D1=list(range(nxt,nxt+k-c)); nxt+=k-c; D2=list(range(nxt,nxt+k-c)); nxt+=k-c
    X1=list(range(nxt,nxt+d)); nxt+=d; X2=list(range(nxt,nxt+d)); nxt+=d
    return {'core':U,'K1':C1+D1+X1,'K2':C2+D2+X2}, nxt
def has_bad(k,s,c,d,j,a,bb):
    G,N=instance(k,s,c,d); types=['core']*j+['K1']*a+['K2']*bb
    pool=IDPool(); cnf=CNF()
    m={(r,v):pool.id(('m',r,v)) for r,t in enumerate(types) for v in G[t]}
    for r,t in enumerate(types):
        lits=[m[(r,v)] for v in G[t]]
        cnf.extend(CardEnc.equals(lits=lits,bound=k,vpool=pool,encoding=EncType.seqcounter).clauses)
    for x in range(N):
        for y in range(x,N):
            cl=[]
            for r in range(7):
                z=pool.id(('z',r,x,y)); cl.append(z)
                for v in {x,y}:
                    if (r,v) in m: cnf.append([-z,-m[(r,v)]])
            cnf.append(cl)
    with Solver(name='cadical153',bootstrap_with=cnf.clauses) as S:
        res=S.solve()
        if res:
            M=set(l for l in S.get_model() if l>0)
            rows=[frozenset(v for v in G[t] if m[(r,v)] in M) for r,t in enumerate(types)]
            P=set().union(*rows)
            assert not any(all((x in E) or (y in E) for E in rows) for x in P for y in P)  # verify badness
            assert all(len(E)==k for E in rows)
        return res
def check(k,s,c,d):
    t0=time.time(); found=None
    for j in range(8):
        for a in range(8-j):
            bb=7-j-a
            if a<bb: continue      # mirror symmetry K1<->K2
            if has_bad(k,s,c,d,j,a,bb): found=(j,a,bb); break
        if found: break
    print(f'(k,s,c,delta)=({k},{s},{c},{d}): ', 'BAD tuple (j,a,b)=%s'%(found,) if found else '(7,2) holds [UNSAT all compositions]', f'{time.time()-t0:.1f}s', flush=True)
for inst in sys.argv[1:]:
    check(*map(int,inst.split(',')))
