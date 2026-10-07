"""Exact small cases of Erdos #644: does a k-uniform hypergraph on N vertices exist with
   (7,2)-property (every <=7 edges have a 2-point transversal) and tau >= t ?
   CEGAR: main SAT over edge variables with 'no (t-1)-transversal' clauses; lazily add
   'not all of these <=7 edges' clauses for bad subfamilies found by a set-cover SAT."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def solve(k, N, t, r=7, verbose=False, max_iter=200000):
    V=list(range(N))
    edges=list(itertools.combinations(V,k))
    idx={E:i+1 for i,E in enumerate(edges)}   # var ids 1..m
    m=len(edges)
    pairs=list(itertools.combinations(V,2))
    # avoid[E] = set of pair indices disjoint from E
    Eset=[set(E) for E in edges]
    avoid=[[pi for pi,(x,y) in enumerate(pairs) if x not in Es and y not in Es] for Es in Eset]
    main=Cadical153()
    # tau >= t : every (N-t+1)-subset U contains an edge
    for U in itertools.combinations(V, N-t+1):
        Us=set(U); main.add_clause([idx[E] for E in edges if set(E)<=Us])
    it=0; t0=time.time()
    while True:
        it+=1
        if not main.solve(): return None, it
        model=main.get_model(); chosen=[i for i in range(m) if model[i]>0]
        # find a bad subfamily of size <= r among chosen: set-cover of all pairs by avoid sets
        # sub-SAT: vars f_i (i in chosen), sum f_i <= r, for each pair some chosen f_i with pair in avoid[i]
        sub=Cadical153(); fvar={i:j+1 for j,i in enumerate(chosen)}
        ok=True
        for pi in range(len(pairs)):
            cl=[fvar[i] for i in chosen if pi in set(avoid[i])]
            if not cl: ok=False; break   # this pair is hit by every chosen edge -> family is 2-pierceable... fine
            sub.add_clause(cl)
        if not ok:
            # every subfamily pierced by that pair: whole family (7,2)-ok
            return [edges[i] for i in chosen], it
        card=CardEnc.atmost(lits=list(fvar.values()), bound=r, top_id=len(chosen), encoding=EncType.seqcounter)
        for cl in card.clauses: sub.add_clause(cl)
        if sub.solve():
            sm=sub.get_model(); bad=[i for i in chosen if sm[fvar[i]-1]>0]
            main.add_clause([-idx[edges[i]] for i in bad])
            if verbose and it%500==0: print(f"  iter {it}, |H|={len(chosen)}, bad size {len(bad)}, {time.time()-t0:.0f}s"); sys.stdout.flush()
            if it>=max_iter: return 'TIMEOUT', it
        else:
            return [edges[i] for i in chosen], it

if __name__=='__main__':
    k=int(sys.argv[1]); Ns=[int(x) for x in sys.argv[2].split(',')]; ts=[int(x) for x in sys.argv[3].split(',')]
    for N in Ns:
        for t in ts:
            t0=time.time(); res,it=solve(k,N,t)
            if res is None: print(f"k={k} N={N} tau>={t}: NO   ({it} iters, {time.time()-t0:.1f}s)")
            elif res=='TIMEOUT': print(f"k={k} N={N} tau>={t}: timeout")
            else: print(f"k={k} N={N} tau>={t}: YES  |H|={len(res)} ({it} iters, {time.time()-t0:.1f}s)  e.g. {res[:8]}{'...' if len(res)>8 else ''}")
            sys.stdout.flush()
