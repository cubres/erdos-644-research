"""Biased exact end-to-end test of THEOREM L: types drawn heavy (mode 'heavy': fill>4/7) or SUPER-heavy
(mode 'super': fill>2/3) in part 1 or 2, light in part 0, to exercise the Q and V branches."""
import random, sys
from fractions import Fraction as F
from thmL_e2e import tau_star_w, proof
def rtype(x,rng,den,ub,thr):
    for _ in range(600):
        h=rng.choice([1,2]); o=3-h
        lo_h=thr*x[h]
        c0=F(rng.randint(0,den),den)*min(ub[0],4*x[0]/7)
        top=min(ub[h],x[h],1-c0)
        if top<=lo_h: continue
        ch=lo_h+(top-lo_h)*F(rng.randint(1,den),den)
        co=1-c0-ch
        if not (0<=co<=min(ub[o],x[o])): continue
        c=[c0,None,None]; c[h]=ch; c[o]=co
        if min(c)<0 or any(c[i]>x[i] for i in range(3)): continue
        return tuple(c)
    return None
rng=random.Random(int(sys.argv[1])); stats={}; fam=0; thr=F(2,3) if sys.argv[3]=='super' else F(4,7)
for trial in range(int(sys.argv[2])):
    den=rng.choice([12,20,30])
    x=[F(rng.randint(1,24),40), F(rng.randint(28,62),40), F(rng.randint(28,62),40)]
    ts=[]; ub=list(x)
    for it in range(16):
        if ts:
            t,g=tau_star_w(ts,x)
            if t>F(3,4): break
            ub=[(g[i]-F(1,2000)) if g[i] is not None else x[i] for i in range(3)]
        c=rtype(x,rng,den,ub,thr)
        if c is None: break
        ts.append(c)
    if not ts: continue
    t,_=tau_star_w(ts,x)
    if t<=F(3,4): continue
    fam+=1; r=proof(ts,x); stats[r]=stats.get(r,0)+1
print('mode',sys.argv[3],'families',fam,stats)
