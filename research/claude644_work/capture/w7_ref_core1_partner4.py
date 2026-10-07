# faster CEGAR: negative phases (small models), several bad subfamilies blocked per iteration
import sys, itertools, random
from pysat.solvers import Cadical153, Glucose4
def popc(x): return bin(x).count('1')
def bm(s): return sum(1<<v for v in s)
def find_bad(edges,n,rng=None,limit=7):
    pairs=[(1<<x)|(1<<y) for x in range(n) for y in range(x,n)]
    def dfs(chosen,surv):
        if not surv: return chosen
        if len(chosen)==limit: return None
        best=None
        for p in surv:
            av=[e for e in edges if not e&p]
            if best is None or len(av)<len(best[1]): best=(p,av)
            if len(av)<=1: break
        av=best[1][:]
        if rng: rng.shuffle(av)
        for e in av:
            r=dfs(chosen+[e],[p for p in surv if p&e])
            if r: return r
        return None
    return dfs([],pairs)
def tau(edges,n):
    for s in range(n+1):
        for c in itertools.combinations(range(n),s):
            m=bm(c)
            if all(e&m for e in edges): return s
k=4;t=3;n=12
quad=([0,1,2,3],[2,3,4,5],[6,7,8,9],[8,9,10,11]); P=[bm(q) for q in quad]
W=bm([2,3,8,9])
rng=random.Random(1)
reps=[(2,8,x) for x in range(n) if x not in (2,8)]+[(0,4,8),(2,6,10)]
for T in reps:
    T=tuple(sorted(T))
    cand=[bm(c) for r in range(1,k+1) for c in itertools.combinations(range(n),r) if bm(c)&bm(T) and bm(c)&W]
    for e in P:
        if e not in cand: cand.append(e)
    idx={e:i+1 for i,e in enumerate(cand)}
    S=Glucose4()
    for e in P: S.add_clause([idx[e]])
    for c in itertools.combinations(range(n),t-1):
        m=bm(c); S.add_clause([idx[e] for e in cand if not e&m])
    S.set_phases([-idx[e] for e in cand])
    it=0; found=None
    while S.solve():
        it+=1
        model=set(l for l in S.get_model() if l>0)
        edges=[e for e in cand if idx[e] in model]
        bad=find_bad(edges,n)
        if bad is None: found=edges; break
        S.add_clause([-idx[e] for e in set(bad)])
        for _ in range(3):
            b2=find_bad(edges,n,rng)
            if b2: S.add_clause([-idx[e] for e in set(b2)])
    print('T',T,'iters',it,'FOUND' if found else 'UNSAT',flush=True)
    if found:
        tt=tau(found,n)
        print(' tau',tt,'|H|',len(found),[sorted(v for v in range(n) if e>>v&1) for e in found])
        print(' recheck bad (limit 7):',find_bad(found,n)); break
