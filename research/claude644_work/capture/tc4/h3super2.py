import random, sys, itertools, collections
exec(open('h3super.py').read().split("rng=random.Random")[0])
from h2climb import C42
rng=random.Random(int(sys.argv[1])); cnt=collections.Counter(); n=0
V=lambda s,t: max(s+t,5*s/4+t/2)
for trial in range(int(sys.argv[2])):
    x=[rng.uniform(0.5,1.5) for _ in range(3)]
    if sum(x)<=2.25: continue
    ts=[]; ub=list(x)
    for it in range(14):
        if ts:
            t,g=tau_star_w(ts,x)
            if t>0.75: break
            ub=[min(g[i],x[i]) for i in range(3)]
        c=rtype(x,rng,ub)
        if c is None: break
        ts.append(c)
    if not ts: continue
    t,_=tau_star_w(ts,x)
    if t<=0.75: continue
    S=[[c for c in ts if 3*c[i]>2*x[i]] for i in range(3)]
    if not all(S): continue
    n+=1
    sig=[min(c[i] for c in S[i]) for i in range(3)]; e=[x[i]-sig[i] for i in range(3)]
    pairsum=max(e[i]+e[j] for i,j in itertools.combinations(range(3),2))
    fam=set()
    for a,b in itertools.permutations(ts,2):
        for nn,f in enumerate(C42):
            if all(max(u*a[i]+v*b[i] for u,v in f)<=x[i]+1e-9 for i in range(3)): fam.add(nn)
    fano=any(n_<36 and n_ not in (12,13,14,15,20,21,22,23,24,25,26,27) for n_ in fam)
    vk=any(n_ in (76,77,78,79) for n_ in fam)
    cnt[('pairsum>3/4' if pairsum>0.75 else 'balanced', 'V' if vk else '-', 'someFano?' if fano else '-')]+=1
print(n,cnt)
