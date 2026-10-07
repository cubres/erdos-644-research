# exact randomized check: two fixed types over p parts, tau*>=3/4 => Ha,Hb,Qa,Qb or V feasible
import random
from fractions import Fraction as F
random.seed(11)
def tau(x,a,b):
    p=len(x); best=None
    for i in range(p):
        if a[i]<=0: continue
        for j in range(p):
            if b[j]<=0: continue
            c = x[i]-min(a[i],b[i]) if i==j else x[i]-a[i]+x[j]-b[j]
            best=c if best is None or c<best else best
    return best
T={'Ha':lambda s,t:7*s/4,'Hb':lambda s,t:7*t/4,'Qb':lambda s,t:max(3*t/2,s+3*t/4),
   'Qa':lambda s,t:max(3*s/2,3*s/4+t),'V':lambda s,t:max(s+t,5*s/4+t/2)}
def comp(p,d):
    # random composition of 1 into p parts with denominator d, with zeros allowed
    cuts=sorted(random.randint(0,d) for _ in range(p-1))
    parts=[b-a for a,b in zip([0]+cuts,cuts+[d])]
    return [F(q,d) for q in parts]
from collections import Counter
C=Counter(); n=0
for it in range(300000):
    p=random.choice([2,2,3,3,4,5,6]); d=random.choice([4,6,8,12,20,24])
    a=comp(p,d); b=comp(p,d)
    if random.random()<0.3:
        # make disjoint-ish supports
        for i in range(p):
            if random.random()<0.5: a[i]=F(0)
        s=sum(a)
        if s==0: continue
        a=[q/s for q in a]
    x=[max(a[i],b[i])+F(random.randint(0,3*d),2*d)*random.choice([0,1,1]) for i in range(p)]
    t=tau(x,a,b)
    if t is None or t<F(3,4): continue
    n+=1
    w=[k for k,M in T.items() if all(M(a[i],b[i])<=x[i] for i in range(p))]
    assert w, ('FAIL',x,a,b,t)
    C[w[0] if len(w)==1 else 'multi']+=1
print('PASS',n,C)
