"""Exhaustive 2-part type-closed families: parts (n1,n2), type set J subset {j: 0<=j<=k} (j = |E cap P1|).
Find (7,2) ones with tau >= 3k/4 + extra."""
import sys, time, itertools
from tc_gen import is72_gen
def tau2(n1,n2,J,k):
    # alpha = max a+b, a<=n1,b<=n2, no j in J with j<=a and k-j<=b
    best=-1
    for a in range(n1+1):
        for b in range(n2+1):
            if a+b<=best: continue
            if not any(j<=a and k-j<=b for j in J): best=a+b
    return n1+n2-best
k=int(sys.argv[1]); extra=float(sys.argv[2]); t0=time.time(); found=0; tested=0
for N in range((7*k)//4-1,(7*k)//4+6):
    for n1 in range(0,N+1):
        n2=N-n1
        feas=[j for j in range(k+1) if j<=n1 and k-j<=n2]
        # tau depends only on J; enumerate J subsets of feas (minimal types matter: J is an antichain? no, all profiles exact)
        for mask in range(1,1<<len(feas)):
            J=[feas[t] for t in range(len(feas)) if mask>>t&1]
            t=tau2(n1,n2,J,k)
            if t<3*k/4+extra: continue
            tested+=1
            r=is72_gen([n1,n2],[(j,k-j) for j in J])
            if r[0] is not False:
                found+=1; print(f"*** k={k} N={N} n=({n1},{n2}) J={J} tau={t} excess={t-3*k/4} (7,2)={r[0]}",flush=True)
    print(f"k={k} N={N} done tested={tested} found={found} {time.time()-t0:.0f}s",flush=True)
