"""NUMERICAL: residual |H|=2 staircase families.  Part 0 light; A-types (s, 1-s-hA(s), hA(s)), B-types
(s, hB(s), 1-s-hB(s)) for s on a grid of [0, 4x0/7]; hA(s)=th2+muA*(4x0/7-s), hB(s)=th1+muB*(4x0/7-s).
Report tau* (exact float enumeration) and whether any single/pair kill exists (42 fns, GQL, MP, pencil, QL)."""
import random, itertools, sys
from h2climb import tau_star, single_killed, pair_killed
rng=random.Random(int(sys.argv[1])); cnt=0; nokill=0; best=0
for trial in range(int(sys.argv[2])):
    x0=rng.uniform(0.05,1.2); x1=rng.uniform(0.8,1.75); x2=rng.uniform(0.8,1.75)
    if x1+x2<2.25: continue
    sig=x1+x2-0.75
    th1=rng.uniform(2*x1/3,min(1,x1)); th2=sig-th1-rng.uniform(0,0.05)
    if not (2*x2/3<th2<=min(1,x2)): continue
    K=rng.randint(1,5); muA=rng.uniform(0,1); muB=rng.uniform(0,1-muA)
    top=4*x0/7; ts=[]
    for k in range(K+1):
        s=top*k/K
        hA=th2+muA*(top-s); hB=th1+muB*(top-s)
        if hA<=x2 and 1-s-hA>=0 and 1-s-hA<=x1: ts.append((s,1-s-hA,hA))
        if hB<=x1 and 1-s-hB>=0 and 1-s-hB<=x2: ts.append((s,hB,1-s-hB))
    x=[x0,x1,x2]
    if len(ts)<2: continue
    t=tau_star(ts,x)
    if t<=0.75: continue
    cnt+=1
    killed=any(single_killed(c,x) for c in ts) or any(pair_killed(a,b,x) for a,b in itertools.combinations(ts,2))
    if not killed:
        nokill+=1
        if t>best: best=t; print('NO PAIR KILL tau*',round(t,4),'x',[round(v,4) for v in x],'types',[[round(v,4) for v in c] for c in ts],flush=True)
print('families tau*>3/4:',cnt,' without single/pair kill:',nokill)
