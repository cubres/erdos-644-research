# Referee w7 / core#1: is the side condition 2(k-t+1)<=t-1 needed in the partner-pair corollary?
# Search (CEGAR, pysat) for a (7,2) family, rank k, tau=t, containing partner pairs (E1,F1),(E2,F2)
# (|E_i & F_i| <= |E_i|-t+1) with cross-overlap |E1&E2|+|F1&F2|+|E1&F2|+|F1&E2| <= 2t-k-2.
import itertools, sys
from pysat.solvers import Cadical153
def popc(x): return bin(x).count('1')
def bm(s): return sum(1<<v for v in s)
def find_bad(edges,n):
    # DFS for <=7 edges with no 2-point transversal; pairs include x==y
    pairs=[(1<<x)|(1<<y) for x in range(n) for y in range(x,n)]
    def dfs(chosen,surv):
        if not surv: return chosen
        if len(chosen)==7: return None
        # pair with fewest avoiders
        best=None
        for p in surv:
            av=[e for e in edges if not e&p]
            if best is None or len(av)<len(best[1]): best=(p,av)
            if len(av)<=1: break
        for e in best[1]:
            r=dfs(chosen+[e],[p for p in surv if p&e])
            if r: return r
        return None
    return dfs([],pairs)
def tau(edges,n):
    for s in range(n+1):
        for c in itertools.combinations(range(n),s):
            m=bm(c)
            if all(e&m for e in edges): return s
def search(n,k,t,planted,T):
    cand=[bm(c) for r in range(1,k+1) for c in itertools.combinations(range(n),r) if bm(c)&bm(T)]
    idx={e:i+1 for i,e in enumerate(cand)}
    S=Cadical153()
    for e in planted: S.add_clause([idx[e]])
    for c in itertools.combinations(range(n),t-1):   # tau>=t
        m=bm(c); S.add_clause([idx[e] for e in cand if not e&m])
    it=0
    while S.solve():
        it+=1
        model=set(l for l in S.get_model() if l>0)
        edges=[e for e in cand if idx[e] in model]
        bad=find_bad(edges,n)
        if bad is None:
            return edges,it
        S.add_clause([-idx[e] for e in set(bad)])
    return None,it
k=int(sys.argv[1]) if len(sys.argv)>1 else 4
t=3
# edges of size 3: partner needs |E&F|<=|E|-t+1=1
E1,F1,E2,F2=bm([0,1,2]),bm([2,3,4]),bm([5,6,7]),bm([7,8,9])
n=int(sys.argv[2]) if len(sys.argv)>2 else 10
res,it=search(n,k,t,[E1,F1,E2,F2],[2,7,n-1])
print('k',k,'n',n,'iterations',it)
if res:
    tt=tau(res,n)
    print('FOUND (7,2) family, |H|=',len(res),'tau=',tt,'edges',[sorted(v for v in range(n) if e>>v&1) for e in res])
    print('recheck bad:',find_bad(res,n),' cross-overlap=',popc(E1&E2)+popc(F1&F2)+popc(E1&F2)+popc(F1&E2),
          ' 2t-k-2=',2*tt-k-2,' partner ok:',popc(E1&F1)<=3-tt+1 and popc(E2&F2)<=3-tt+1,
          ' side cond 2(k-t+1)<=t-1:',2*(k-tt+1)<=tt-1)
else: print('UNSAT: no such family with this planted quadruple / transversal T')
