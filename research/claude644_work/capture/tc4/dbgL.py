import random, sys
from fractions import Fraction as F
from thmL_e2e import tau_star_w, proof
src=open('thmL_e2e2.py').read().split("rng=random.Random")[0]
exec(src)
rng=random.Random(int(sys.argv[1])); thr=F(2,3) if sys.argv[3]=='super' else F(4,7); fam=0; stats={}
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
    fam+=1
    try: r=proof(ts,x); stats[r]=stats.get(r,0)+1
    except AssertionError as e:
        A=[c for c in ts if 7*c[2]>4*x[2]]; B=[c for c in ts if 7*c[1]>4*x[1]]
        print('FAIL',e,[str(v) for v in x],[[str(v) for v in c] for c in ts],'tau*',t,'thk',min(c[2] for c in A),'thj',min(c[1] for c in B)); break
print(fam,stats)
