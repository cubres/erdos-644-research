"""Symmetric (cyclic Z_N) search for k-uniform families with (7,2) and tau >= t. Orbit variables."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def solve(k,N,t,r=7,max_iter=100000,verbose=True):
    V=list(range(N)); edges=list(itertools.combinations(V,k))
    def rot(E,s): return tuple(sorted((x+s)%N for x in E))
    orb={}; orbits=[]
    for E in edges:
        if E in orb: continue
        o=set(rot(E,s) for s in range(N)); oi=len(orbits); orbits.append(sorted(o))
        for F in o: orb[F]=oi
    no=len(orbits); var=lambda oi: oi+1
    pairs=list(itertools.combinations(V,2)); pidx={p:i for i,p in enumerate(pairs)}
    main=Cadical153()
    for U in itertools.combinations(V,N-t+1):
        Us=set(U); cl=sorted(set(var(orb[E]) for E in edges if set(E)<=Us)); main.add_clause(cl)
    it=0; t0=time.time()
    while True:
        it+=1
        if not main.solve(): return None,it
        model=main.get_model(); chosen_orb=[oi for oi in range(no) if model[oi]>0]
        chosen=[E for oi in chosen_orb for E in orbits[oi]]
        Es=[set(E) for E in chosen]
        avoid=[frozenset(pi for pi,(x,y) in enumerate(pairs) if x not in S and y not in S) for S in Es]
        sub=Cadical153(); ok=True
        for pi in range(len(pairs)):
            cl=[i+1 for i in range(len(chosen)) if pi in avoid[i]]
            if not cl: ok=False; break
            sub.add_clause(cl)
        if not ok: return chosen,it
        card=CardEnc.atmost(lits=list(range(1,len(chosen)+1)), bound=r, top_id=len(chosen), encoding=EncType.seqcounter)
        for cl in card.clauses: sub.add_clause(cl)
        if sub.solve():
            sm=sub.get_model(); bad=[i for i in range(len(chosen)) if sm[i]>0]
            main.add_clause(sorted(set(-var(orb[chosen[i]]) for i in bad)))
            if verbose and it%200==0: print(f"   it {it} |H|={len(chosen)} orbits={len(chosen_orb)} {time.time()-t0:.0f}s",flush=True)
            if it>=max_iter: return 'TIMEOUT',it
        else: return chosen,it
if __name__=='__main__':
    k=int(sys.argv[1]); Ns=[int(x) for x in sys.argv[2].split(',')]; t=int(sys.argv[3])
    for N in Ns:
        t0=time.time(); res,it=solve(k,N,t)
        if res is None: print(f"cyclic k={k} N={N} tau>={t}: NO ({it} iters, {time.time()-t0:.0f}s)",flush=True)
        elif res=='TIMEOUT': print(f"cyclic k={k} N={N} tau>={t}: TIMEOUT",flush=True)
        else:
            print(f"cyclic k={k} N={N} tau>={t}: YES |H|={len(res)} ({it} iters, {time.time()-t0:.0f}s)",flush=True)
            open(f'p644_found_k{k}_N{N}_t{t}.txt','w').write('\n'.join(str(E) for E in res))
