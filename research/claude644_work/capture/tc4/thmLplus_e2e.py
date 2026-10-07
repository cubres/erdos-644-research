"""EXACT end-to-end test of THEOREM L+ : part 0 is 2/3-light for every type (c_0 <= 2x_0/3).
Proof algorithm: (i) a type <= 2x/3 everywhere -> pencil lemma (bad tuple with requests, valid as tau*>3/4);
(ii) else A = k-SUPER-heavy (c_k>2x_k/3), B = j-super-heavy; a = argmin_A c_k; corner u=(x_i-a_i (i!=k), <theta_k);
 witness c must exist and lie in B; V(a,c) must be feasible.  All asserted exactly."""
import random, sys
from fractions import Fraction as F
from thmL_e2e import tau_star_w, V, feasible
def proof(ts,x,j=1,k=2):
    if any(all(3*c[i]<=2*x[i] for i in range(3)) for c in ts): return 'pencil'
    A=[c for c in ts if 3*c[k]>2*x[k]]; B=[c for c in ts if 3*c[j]>2*x[j]]
    assert all(c in A or c in B for c in ts) and A and B
    thk=min(c[k] for c in A); thj=min(c[j] for c in B); a=min(A,key=lambda c:c[k])
    assert (x[j]-thj)+(x[k]-thk)>F(3,4) and x[j]+x[k]>F(9,4)
    assert 1+x[k]-2*thk<F(3,4)
    cs=[c for c in ts if all(c[i]<=x[i]-a[i] for i in range(3) if i!=k) and c[k]<thk]
    assert cs; c=cs[0]; assert c in B
    assert feasible(V,a,c,x); return 'V'
def rtype(x,rng,den,ub):
    for _ in range(600):
        h=rng.choice([1,2]); o=3-h
        c0=F(rng.randint(0,den),den)*min(ub[0],2*x[0]/3)
        lo_h=2*x[h]/3; top=min(ub[h],x[h],1-c0)
        if top<=lo_h: continue
        ch=lo_h+(top-lo_h)*F(rng.randint(1,den),den); co=1-c0-ch
        c=[c0,None,None]; c[h]=ch; c[o]=co
        if min(c)<0 or any(c[i]>x[i] for i in range(3)) or co>ub[o]: continue
        return tuple(c)
    return None
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1])); stats={}; fam=0
    for trial in range(int(sys.argv[2])):
        den=rng.choice([12,20,30])
        x=[F(rng.randint(1,40),40), F(rng.randint(28,62),40), F(rng.randint(28,62),40)]
        ts=[]; ub=list(x)
        for it in range(16):
            if ts:
                t,g=tau_star_w(ts,x)
                if t>F(3,4): break
                ub=[(g[i]-F(1,2000)) if g[i] is not None else x[i] for i in range(3)]
            c=rtype(x,rng,den,ub)
            if c is None: break
            ts.append(c)
        if not ts: continue
        t,_=tau_star_w(ts,x)
        if t<=F(3,4): continue
        fam+=1; r=proof(ts,x); stats[r]=stats.get(r,0)+1
    print('L+ families',fam,stats)
