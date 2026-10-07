"""Size-restricted families: B = {A subset S, |A|=r, |A ∩ X| in R}. Compute tau exactly and test (7,2) via SAT set-cover."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def tau_restricted(nS, x, r, R):
    # U is B-free iff for m=|U|, u=|U∩X|: achievable |A∩X| for A⊂U, |A|=r is [max(0, r-(m-u)), min(u,r)] ∩ [0,r]; free iff no value in R (or m<r)
    best=0
    for m in range(nS+1):
        for u in range(0, min(x,m)+1):
            if m-u > nS-x: continue
            if m<r: free=True
            else:
                lo=max(0, r-(m-u)); hi=min(u,r)
                free = not any(v in R for v in range(lo,hi+1))
            if free: best=max(best,m)
    return nS-best
def has_72(nS, x, r, R, p=7):
    S=list(range(nS)); X=set(range(x))
    edges=[E for E in itertools.combinations(S,r) if len(X.intersection(E)) in R]
    if len(edges)==0: return None, edges
    pairs=list(itertools.combinations(S,2))
    sub=Cadical153(); n=len(edges); Es=[set(E) for E in edges]
    for (a,b) in pairs:
        cl=[i+1 for i in range(n) if a not in Es[i] and b not in Es[i]]
        if not cl: return True, edges  # pair {a,b} covers every edge
        sub.add_clause(cl)
    card=CardEnc.atmost(lits=list(range(1,n+1)), bound=p, top_id=n, encoding=EncType.seqcounter)
    for cl in card.clauses: sub.add_clause(cl)
    if sub.solve():
        m=sub.get_model(); bad=[edges[i] for i in range(n) if m[i]>0]
        return False, bad
    return True, edges
if __name__=='__main__':
    r=int(sys.argv[1]); target=int(sys.argv[2])
    patterns={}
    for m in [2,3,4]:
        for a in range(m): patterns[f'≡{a} mod {m}']=set(v for v in range(r+1) if v%m==a)
    for a in range(1,r): patterns[f'>={a}']=set(range(a,r+1)); patterns[f'<={a}']=set(range(0,a+1))
    for a in range(0,r):
        for b in range(a+1,r+1): patterns[f'in[{a},{b}]']=set(range(a,b+1))
    for a in range(r+1): patterns[f'={a}']={a}
    for a in range(r+1):
        for b in range(a+2,r+1): patterns[f'in{{{a},{b}}}']={a,b}
    found=[]
    t0=time.time(); tested=0
    for nS in range(int(1.75*r)-1, int(1.75*r)+3):
        for x in range(1,nS):
            for name,R in patterns.items():
                tau=tau_restricted(nS,x,r,R)
                if tau<target: continue
                ok,wit=has_72(nS,x,r,R); tested+=1
                if ok:
                    found.append((nS,x,name,tau,len(wit))); print(f"FOUND (7,2) family: |S|={nS} |X|={x} R={name} tau={tau} |B|={len(wit)}",flush=True)
    print(f"r={r}: tested {tested} candidate families with tau>={target}; found {len(found)} with (7,2). [{time.time()-t0:.0f}s]")
