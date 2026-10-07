import random, itertools, sys
from h2climb import tau_star, single_killed, pair_killed, C42
rng=random.Random(int(sys.argv[1])); stats={}; cnt=0
def fnames(a,b,x,eps=1e-9):
    return [n for n,f in enumerate(C42) if all(max(u*a[i]+v*b[i] for u,v in f)<=x[i]+eps for i in range(3))]
for trial in range(int(sys.argv[2])):
    x0=rng.uniform(0.05,1.2); x1=rng.uniform(0.8,1.75); x2=rng.uniform(0.8,1.75)
    if x1+x2<2.25: continue
    sig=x1+x2-0.75
    th1=rng.uniform(2*x1/3,min(1,x1)); th2=sig-th1-rng.uniform(0,0.05)
    if not (2*x2/3<th2<=min(1,x2)): continue
    K=rng.randint(1,5); muA=rng.uniform(0,1); muB=rng.uniform(0,1-muA)
    top=4*x0/7; A=[]; B=[]
    for k in range(K+1):
        s=top*k/K
        hA=th2+muA*(top-s); hB=th1+muB*(top-s)
        if hA<=x2 and 1-s-hA>=0 and 1-s-hA<=x1: A.append((s,1-s-hA,hA))
        if hB<=x1 and 1-s-hB>=0 and 1-s-hB<=x2: B.append((s,hB,1-s-hB))
    x=[x0,x1,x2]; ts=A+B
    if not A or not B: continue
    t=tau_star(ts,x)
    if t<=0.75: continue
    cnt+=1
    # canonical candidates
    a_min=max(A,key=lambda c:c[0]); b_min=max(B,key=lambda c:c[0])  # minimisers (largest s)
    a0=min(A,key=lambda c:c[0]); b0=min(B,key=lambda c:c[0])
    for name,(a,b) in {'minmin':(a_min,b_min),'zero-zero':(a0,b0),'minA-zeroB':(a_min,b0),'zeroA-minB':(a0,b_min)}.items():
        if fnames(a,b,x): stats[name]=stats.get(name,0)+1
    # AB pairs vs AA / BB
    ab=any(fnames(a,b,x) for a in A for b in B); aa=any(fnames(a,b,x) for a,b in itertools.combinations(A,2)); bb=any(fnames(a,b,x) for a,b in itertools.combinations(B,2))
    stats['anyAB']=stats.get('anyAB',0)+ab; stats['anyAA']=stats.get('anyAA',0)+aa; stats['anyBB']=stats.get('anyBB',0)+bb
    # which s-levels: record sum of s for killed AB pairs, min over pairs
    ms=min([a[0]+b[0] for a in A for b in B if fnames(a,b,x)] or [9])
    stats.setdefault('min_s_sum_over_x0',[]).append(round(ms/x0,2))
print(cnt,{k:v for k,v in stats.items() if k!='min_s_sum_over_x0'}); import collections; print(sorted(collections.Counter(stats['min_s_sum_over_x0']).items())[:30])
