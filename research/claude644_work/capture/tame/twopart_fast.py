"""Fast exhaustive 2-part type-closed search.  Box (a,b) is free for J iff J cap [k-b, a] = empty, so
b_max(a) = min(n2, k-1-jstar(a)) with jstar(a) = max{j in J: j<=a} (b_max = n2 if none); alpha = max_a a+b_max(a)."""
import sys, time, numpy as np
from tc_gen import is72_gen
k=int(sys.argv[1]); extra=float(sys.argv[2]); t0=time.time()
for N in range((7*k)//4-1,(7*k)//4+6):
    tested=found=0
    for n1 in range(0,N+1):
        n2=N-n1
        feas=[j for j in range(k+1) if j<=n1 and k-j<=n2]
        L=len(feas)
        if L==0: continue
        masks=np.arange(1,1<<L,dtype=np.int64)
        alpha=np.full(len(masks),-1,dtype=np.int64)
        for a in range(n1+1):
            # jstar(a): largest feas index t with feas[t]<=a and bit t set
            cnt=sum(1 for j in feas if j<=a)
            sub=masks & ((1<<cnt)-1)
            has=sub>0
            hb=np.zeros(len(masks),dtype=np.int64)
            hb[has]=np.floor(np.log2(sub[has].astype(np.float64))).astype(np.int64)
            jstar=np.array(feas,dtype=np.int64)[hb]
            b=np.where(has, np.minimum(n2, k-1-jstar), n2)
            ok=b>=0
            val=np.where(ok, a+b, -1)
            alpha=np.maximum(alpha,val)
        tau=N-alpha
        idx=np.nonzero(tau>=3*k/4+extra)[0]
        for i in idx:
            J=[feas[t] for t in range(L) if (int(masks[i])>>t)&1]
            tested+=1
            r=is72_gen([n1,n2],[(j,k-j) for j in J])
            if r[0] is not False:
                found+=1; print(f"*** k={k} N={N} n=({n1},{n2}) J={J} tau={int(tau[i])} excess={tau[i]-3*k/4} (7,2)={r[0]}",flush=True)
    print(f"k={k} N={N} done tested={tested} found={found} {time.time()-t0:.0f}s",flush=True)
