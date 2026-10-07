"""Search parity-check (code) families over F_2^r with 2^r value classes for (7,2) + tau >= 3k/4 + 2."""
import itertools, sys, time, numpy as np
from tc_lib import is72_code
def tau_vec(n, c, a, k):
    p=len(n); r=len(a)
    grids=np.meshgrid(*[np.arange(x+1) for x in n], indexing='ij')
    W=np.stack([g.ravel() for g in grids],axis=1)  # M x p
    tot=W.sum(1); dom=np.zeros(len(W),bool)
    for mask in range(1<<p):
        J=[i for i in range(p) if mask>>i&1]
        if (len(J)-k)%2 or len(J)>k: continue
        s=np.zeros(r,int)
        for i in J: s^=np.array(c[i])
        if tuple(s)!=tuple(a): continue
        inJ=np.array([mask>>i&1 for i in range(p)])
        ok=np.all(W[:,inJ==1]>=1,axis=1)
        mx=(W - ((W+inJ[None,:])%2)).sum(1)   # i in J: w-((w+1)%2) ; i not in J: w-(w%2)
        dom |= ok & (mx>=k)
    free=tot[~dom]
    return sum(n)-free.max()
if __name__=='__main__':
    r=int(sys.argv[1]); ks=[int(x) for x in sys.argv[2].split(',')]; extra=int(sys.argv[3]) if len(sys.argv)>3 else 2
    vals=list(itertools.product((0,1),repeat=r)); p=len(vals)
    for k in ks:
        best={}; t0=time.time(); tested=0
        for N in range((7*k+3)//4-1, (7*k)//4+2*r+3):
            for comp in itertools.combinations(range(N+p-1),p-1):
                n=[b-a_-1 for a_,b in zip((-1,)+comp, comp+(N+p-1,))]
                for a in vals:
                    if k%2==0 and a!=vals[0] and False: pass
                    t=tau_vec(n,vals,a,k)
                    if t >= 3*k/4+extra:
                        tested+=1
                        res=is72_code(n,vals,a,k)
                        if res[0] is not False:
                            print("*** k=%d N=%d n=%s a=%s tau=%d excess=%.2f (7,2)=%s"%(k,N,n,a,t,t-3*k/4,res[0]),flush=True)
            print("k=%d N=%d done, tested %d, %.0fs"%(k,N,tested,time.time()-t0),flush=True)
