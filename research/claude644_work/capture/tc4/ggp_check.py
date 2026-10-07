"""Exact random stress test of the GENERALISED GAP-PAIR LEMMA (GGP), typeclosed run 4.
p parts, distinguished parts j (b heavy) and k (a heavy).  a,b >= 0, sum 1, a,b <= x.
 H1: 4x_k < 7a_k ; H2: 4x_j < 7b_j ; G: (x_j-b_j)+(x_k-a_k) > 3/4 ;
 L: every other part i: max(3a_i/2, 3b_i/2, a_i+b_i) <= x_i.
Claim: Q_b [per part max(3t/2, s+3t/4)], Q_a [max(3s/2, t+3s/4)] or V(a,b) [max(s+t, 5s/4+t/2)]
(s = a-load, t = b-load) is feasible in every part.  Also checks the proof's intermediate claims:
b_j+a_k>1; Q_b can fail only by 3b_j/2>x_j; Q_a only by 3a_k/2>x_k."""
import random
from fractions import Fraction as F
Qb=lambda s,t: max(3*t/2, s+3*t/4)
Qa=lambda s,t: max(3*s/2, t+3*s/4)
V=lambda s,t: max(s+t, 5*s/4+t/2)
def rmass(p,rng,den):
    cuts=sorted(rng.randint(0,den) for _ in range(p-1)); pts=[0]+cuts+[den]
    return [F(pts[i+1]-pts[i],den) for i in range(p)]
rng=random.Random(7); tested=0; which={'Qb':0,'Qa':0,'V':0}
for trial in range(400000):
    p=rng.randint(2,5); den=rng.choice([12,20,30,60,97])
    a=rmass(p,rng,den); b=rmass(p,rng,den)
    if rng.random()<0.5:  # bias: concentrate
        j,k=0,1
    j,k=rng.sample(range(p),2)
    x=[max(a[i],b[i])+F(rng.randint(0,60),40) for i in range(p)]
    if rng.random()<0.5:
        x[j]=F(rng.randint(int(4*b[j]*40)//7, int(7*b[j]*40)//4+1),40); x[k]=F(rng.randint(int(4*a[k]*40)//7, int(7*a[k]*40)//4+1),40)
    if any(x[i]<max(a[i],b[i]) for i in range(p)): continue
    if not (4*x[k]<7*a[k] and 4*x[j]<7*b[j] and (x[j]-b[j])+(x[k]-a[k])>F(3,4)): continue
    if not all(max(3*a[i]/2,3*b[i]/2,a[i]+b[i])<=x[i] for i in range(p) if i not in (j,k)): continue
    tested+=1
    assert b[j]+a[k]>1
    for i in range(p):
        if i!=j: assert Qb(a[i],b[i])<=x[i]
        if i!=k: assert Qa(a[i],b[i])<=x[i]
    assert Qb(a[j],b[j])<=x[j] or 3*b[j]/2>x[j]
    assert Qa(a[k],b[k])<=x[k] or 3*a[k]/2>x[k]
    ok=False
    for name,f in (('Qb',Qb),('Qa',Qa),('V',V)):
        if all(f(a[i],b[i])<=x[i] for i in range(p)): which[name]+=1; ok=True; break
    assert ok,(x,a,b,j,k)
print('GGP verified exactly on',tested,'random instances; first feasible template counts',which)
