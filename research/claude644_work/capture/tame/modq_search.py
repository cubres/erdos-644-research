"""Mod-q sum families: parts i with value c_i in Z_q, edges = k-sets with sum_i u_i c_i = a (mod q).
Search part sizes for (7,2) with tau >= 3k/4 + extra.  Types enumerated explicitly -> tc_gen (general type sets)."""
import itertools, sys, time, numpy as np
from tc_gen import is72_gen
def types(n,c,a,k,q):
    out=[]
    for u in itertools.product(*[range(x+1) for x in n]):
        if sum(u)==k and sum(ui*ci for ui,ci in zip(u,c))%q==a: out.append(u)
    return out
def tau_T(n,T):
    Ta=np.array(T); N=sum(n)
    grids=np.meshgrid(*[np.arange(x+1) for x in n],indexing='ij'); W=np.stack([g.ravel() for g in grids],1)
    dom=np.zeros(len(W),bool)
    for t in Ta: dom|=np.all(W>=t,axis=1)
    return N-W.sum(1)[~dom].max()
q=int(sys.argv[1]); k=int(sys.argv[2]); extra=float(sys.argv[3]); c=list(range(q))   # one part per residue
t0=time.time(); tested=0
for N in range((7*k)//4-1,(7*k)//4+q+3):
    for comp in itertools.combinations(range(N+q-1),q-1):
        n=[b-a_-1 for a_,b in zip((-1,)+comp, comp+(N+q-1,))]
        for a in range(q):
            T=types(n,c,a,k,q)
            if not T: continue
            t=tau_T(n,T)
            if t<3*k/4+extra: continue
            tested+=1
            r=is72_gen(n,T)
            if r[0] is not False: print(f"*** q={q} k={k} N={N} n={n} a={a} tau={t} excess={t-3*k/4} (7,2)={r[0]}",flush=True)
    print(f"q={q} k={k} N={N} done tested={tested} {time.time()-t0:.0f}s",flush=True)
