"""Exact random stress test of GGP-MASS: G weakened to (x_j-b_j)+(x_k-a_k) > (3/4)max(m_a,m_b), m = mass on {j,k}."""
import random
from fractions import Fraction as F
Qb=lambda s,t: max(3*t/2, s+3*t/4); Qa=lambda s,t: max(3*s/2, t+3*s/4); V=lambda s,t: max(s+t, 5*s/4+t/2)
rng=random.Random(9); tested=0; cnt={'Qb':0,'Qa':0,'V':0}
for trial in range(400000):
    p=rng.randint(2,4); den=rng.choice([20,40,60,120]); j,k=0,1
    ra=F(rng.randint(0,den//2),den); rb=F(rng.randint(0,den//2),den)
    ak=F(rng.randint(0,den),den)*(1-ra); bj=F(rng.randint(0,den),den)*(1-rb)
    a=[F(0)]*p; b=[F(0)]*p; a[k]=ak; a[j]=1-ra-ak; b[j]=bj; b[k]=1-rb-bj
    if p>2:
        for i in range(2,p): a[i]=ra/(p-2); b[i]=rb/(p-2)
    else:
        a[j]+=0; b[k]+=0   # masses < 1 allowed as abstract loads
    x=[max(a[i],b[i])+F(rng.randint(0,60),80)*max(a[i],b[i],F(1,10)) for i in range(p)]
    for i in range(2,p): x[i]=max(3*a[i]/2,3*b[i]/2,a[i]+b[i])+F(rng.randint(0,3),20)
    M=max(a[j]+a[k],b[j]+b[k])
    if not (4*x[k]<7*a[k] and 4*x[j]<7*b[j] and (x[j]-b[j])+(x[k]-a[k])>F(3,4)*M): continue
    tested+=1
    for n,f in (('Qb',Qb),('Qa',Qa),('V',V)):
        if all(f(a[i],b[i])<=x[i] for i in range(p)): cnt[n]+=1; break
    else: raise AssertionError((x,a,b))
print('GGP-mass verified on',tested,'instances',cnt)
