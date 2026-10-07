import random, numpy as np
from twopart_search import tau2
def fast(n1,n2,J,k):
    best=-1
    for a in range(n1+1):
        js=[j for j in J if j<=a]
        b=n2 if not js else min(n2,k-1-max(js))
        if b>=0: best=max(best,a+b)
    return n1+n2-best
random.seed(3); bad=0
for _ in range(3000):
    k=random.randint(4,16); N=random.randint(k,2*k+4); n1=random.randint(0,N); n2=N-n1
    feas=[j for j in range(k+1) if j<=n1 and k-j<=n2]
    if not feas: continue
    J=[j for j in feas if random.random()<0.5] or [feas[0]]
    if tau2(n1,n2,J,k)!=fast(n1,n2,J,k): bad+=1
print("mismatches:",bad)
