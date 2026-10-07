"""NUMERICAL: adversarial repair in the residual |H|=2 regime.  Start: minimiser pair a,b with G,R1,R2 and
a0+b0>x0 (so Q_b,Q_a,V all fail; no pair kill checked).  Repeatedly take the cheapest free vector u (cost<=3/4)
and add a type c<=u (part 0 light, keeping a,b the minimisers) chosen among many random candidates so that NO
single or pair kill appears.  Success (tau*>3/4, no kill) would be a family needing >=3 actual types."""
import random, itertools, sys
from h2climb import single_killed, pair_killed
from h2resid import gen, tau_star_w
rng=random.Random(int(sys.argv[1])); stuck=0; succ=0; runs=0; depth=[]
for trial in range(int(sys.argv[2])):
    x,a,b=gen(rng)
    if single_killed(a,x) or single_killed(b,x) or pair_killed(a,b,x): continue
    runs+=1; ts=[a,b]; ok=False
    for it in range(15):
        t,u=tau_star_w(ts,x)
        if t>0.75+1e-9: ok=True; break
        cands=[]
        for tries in range(3000):
            c0=rng.uniform(0,min(u[0],4*x[0]/7)); c1=rng.uniform(0,min(u[1],1-c0)); c=(c0,c1,1-c0-c1)
            if c[2]>u[2] or c[2]<0 or c[2]>x[2]: continue
            if c[1]>4*x[1]/7 and c[1]<b[1]: continue
            if c[2]>4*x[2]/7 and c[2]<a[2]: continue
            if single_killed(c,x): continue
            if any(pair_killed(c,d,x) for d in ts): continue
            cands.append(c)
            if len(cands)>=20: break
        if not cands: break
        ts.append(rng.choice(cands))
    depth.append(len(ts))
    if ok:
        succ+=1; print('SUCCESS tau*',t,'x',x,'types',ts,flush=True)
    else: stuck+=1
print('runs',runs,'stuck',stuck,'success',succ,'max types',max(depth) if depth else None)
