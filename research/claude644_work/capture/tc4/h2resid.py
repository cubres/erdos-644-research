"""NUMERICAL: residual |H|=2 regime generator.  Part 0 light.  Start with minimiser pair a (2-heavy), b (1-heavy)
with G, R1 (x1<3b1/2), R2 (x2<3a2/2), a0+b0>x0 (V fails at the light part).  Repair tau*>3/4 by repeatedly adding a
random type inside the corner of the cheapest free vector (keeping part 0 light, keeping a,b the minimisers:
new 1-heavy types have c1>=b1, new 2-heavy types c2>=a2).  Then report which kills exist."""
import random, itertools, sys
from h2climb import tau_star, single_killed, pair_killed
def tau_star_w(types,x):
    p=len(x); N=sum(x); best=[-1,None]
    cand=[sorted(set(t[i] for t in types if t[i]>1e-12)) for i in range(p)]
    def rec(i,alive,acc,gs):
        if i==p:
            if not alive and acc>best[0]: best[0]=acc; best[1]=gs[:]
            return
        if acc+sum(x[i:])<=best[0]: return
        rec(i+1,alive,acc+x[i],gs+[x[i]])
        for g in cand[i]: rec(i+1,[t for t in alive if t[i]<g-1e-12],acc+g,gs+[g-1e-9])
    rec(0,types,0.0,[]); return N-best[0],best[1]
def gen(rng):
    while True:
        x0=rng.uniform(0.1,1.0); x1=rng.uniform(0.9,1.75); x2=rng.uniform(0.9,1.75)
        b1=rng.uniform(2*x1/3,min(1,x1)); a2=rng.uniform(2*x2/3,min(1,x2))
        if not (x1+x2>0.75+b1+a2): continue
        a0=rng.uniform(3*x0/7,min(4*x0/7,1-a2)); b0=rng.uniform(3*x0/7,min(4*x0/7,1-b1))
        if a0+b0<=x0: continue
        a=(a0,1-a0-a2,a2); b=(b0,b1,1-b0-b1)
        x=[x0,x1,x2]
        if any(a[i]>x[i] or b[i]>x[i] or a[i]<0 or b[i]<0 for i in range(3)): continue
        return x,a,b
def repair(x,a,b,rng,maxadd=12):
    ts=[a,b]
    for it in range(maxadd):
        t,u=tau_star_w(ts,x)
        if t>0.75+1e-9: return ts,t
        # random type c <= u (corner), sum 1, light in 0, respecting minimisers
        for tries in range(2000):
            c0=rng.uniform(0,min(u[0],4*x[0]/7)); c1=rng.uniform(0,min(u[1],1-c0)); c2=1-c0-c1
            c=(c0,c1,c2)
            if c2>u[2]+1e-12 or c2<0: continue
            if c1>4*x[1]/7 and c1<b[1]: continue
            if c2>4*x[2]/7 and c2<a[2]: continue
            if all(7*c[i]<=4*x[i] for i in range(3)): continue
            ts.append(c); break
        else: return ts,None
    t,u=tau_star_w(ts,x); return ts,(t if t>0.75 else None)
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1); stats={}; n=0
for trial in range(3000):
    x,a,b=gen(rng); ts,t=repair(x,a,b,rng)
    if t is None: continue
    n+=1; kinds=[]
    for i,c in enumerate(ts):
        if single_killed(c,x): kinds.append(('S',i))
    for i,j in itertools.combinations(range(len(ts)),2):
        if pair_killed(ts[i],ts[j],x): kinds.append(('P',i,j))
    key='none' if not kinds else ('single' if any(k[0]=='S' for k in kinds) else 'pair')
    stats[key]=stats.get(key,0)+1
    if key=='none': print('NO single/pair kill',t,x,ts,flush=True)
print('families',n,stats)
