"""Targeted exact test of GGP in the V regime (R1: x_j<3b_j/2, R2: x_k<3a_k/2)."""
import random
from fractions import Fraction as F
from ggp_check import Qb,Qa,V,rmass
rng=random.Random(8); tested=0; vcount=0
for trial in range(300000):
    p=rng.randint(2,5); den=rng.choice([20,40,60,120])
    j,k=0,1
    # a heavy at k, b heavy at j, small rest
    ra=F(rng.randint(0,den//4),den); rb=F(rng.randint(0,den//4),den)
    ak=F(rng.randint(den//2,den),den); ak=min(ak,1-ra); bj=F(rng.randint(den//2,den),den); bj=min(bj,1-rb)
    a=[F(0)]*p; b=[F(0)]*p
    a[k]=ak; a[j]=1-ak-ra; b[j]=bj; b[k]=1-bj-rb
    if p>2:
        ma=rmass(p-2,rng,den); mb=rmass(p-2,rng,den)
        for i in range(2,p): a[i]=ra*ma[i-2]; b[i]=rb*mb[i-2]
    else:
        a[j]+=ra; b[k]+=rb
    x=[F(0)]*p
    x[j]=max(a[j],b[j])+F(rng.randint(0,40),80)*b[j]; x[k]=max(a[k],b[k])+F(rng.randint(0,40),80)*a[k]
    for i in range(2,p): x[i]=max(3*a[i]/2,3*b[i]/2,a[i]+b[i])+F(rng.randint(0,3),10)
    if not (4*x[k]<7*a[k] and 4*x[j]<7*b[j] and (x[j]-b[j])+(x[k]-a[k])>F(3,4)): continue
    tested+=1
    for name,f in (('Qb',Qb),('Qa',Qa),('V',V)):
        if all(f(a[i],b[i])<=x[i] for i in range(p)):
            vcount+=name=='V'; break
    else: raise AssertionError((x,a,b))
print('targeted GGP: all',tested,'instances covered; V needed in',vcount)
