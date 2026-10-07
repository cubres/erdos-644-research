"""Block-parity families: V = B0 (free) u B1..Br, edges = k-sets with |E cap Bj| = a_j mod 2 (j=1..r).
Search all block sizes / targets for (7,2) with tau >= 3k/4 + extra."""
import itertools, sys, time
from code_search import tau_vec
from tc_lib import is72_code
r=int(sys.argv[1]); ks=[int(x) for x in sys.argv[2].split(',')]; extra=float(sys.argv[3])
vals=[tuple(0 for _ in range(r))]+[tuple(1 if b==j else 0 for b in range(r)) for j in range(r)]
p=len(vals)
for k in ks:
    t0=time.time(); tested=0; best=None
    for N in range((7*k)//4-1,(7*k)//4+2*r+4):
        for comp in itertools.combinations(range(N+p-1),p-1):
            n=[b-a_-1 for a_,b in zip((-1,)+comp, comp+(N+p-1,))]
            if any(x==0 for x in n[1:]): continue
            if list(n[1:])!=sorted(n[1:]): continue   # blocks symmetric up to target relabel -> keep all targets
            for a in itertools.product((0,1),repeat=r):
                t=tau_vec(n,vals,a,k)
                if t<3*k/4+extra: continue
                tested+=1
                res=is72_code(n,vals,a,k)
                if res[0] is not False:
                    print(f"*** k={k} N={N} n={n} a={a} tau={t} excess={t-3*k/4} (7,2)={res[0]}",flush=True)
        print(f"k={k} N={N} done tested={tested} {time.time()-t0:.0f}s",flush=True)
