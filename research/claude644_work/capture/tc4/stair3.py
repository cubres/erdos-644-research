import random, itertools, sys, collections
from h2climb import tau_star, C42
rng=random.Random(int(sys.argv[1])); cnt=collections.Counter(); ex=0
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
    if tau_star(ts,x)<=0.75: continue
    a=max(A,key=lambda c:c[0]); b=min(B,key=lambda c:c[0])
    G=a[2]+b[1]<sig
    f=fnames(a,b,x); cnt[(G,tuple(f[:3]))]+=1
    if not G and ex<5: ex+=1; print('x',[round(v,3) for v in x],'a',[round(v,3) for v in a],'b',[round(v,3) for v in b],'fns',f)
print(cnt.most_common(12))
