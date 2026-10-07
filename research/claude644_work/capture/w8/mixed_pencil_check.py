"""Exact random check of the MIXED PENCIL LEMMA: rows e,e,f on the three lines through p0, the four
m-lines requested (non-adaptive) with bound d = x - max(max(e,f)/2, (2e+f)/4) per part.  Checks the Fano
criterion (Lemma 7.63) for arbitrary responses <= d, and cost(d) = 3/4 + sum((f-2e)^+)/4 (types of mass 1)."""
import random
from fractions import Fraction as F
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
p0=0; PEN=[l for l in range(7) if p0 in L[l]]; M=[l for l in range(7) if p0 not in L[l]]
def rand_below(B,rng,total=1):
    if sum(B)<total: return None
    v=[F(0)]*len(B); order=list(range(len(B))); rng.shuffle(order); rem=F(total)
    for i in order:
        take=min(B[i],rem*F(rng.randint(1,10),10)) if rng.random()<0.5 else min(B[i],rem); v[i]+=take; rem-=take
    for i in order:
        if rem==0: break
        take=min(B[i]-v[i],rem); v[i]+=take; rem-=take
    return v
rng=random.Random(5); ok=0
for t in range(30000):
    p=rng.randint(1,5); x=[F(rng.randint(1,40),20) for _ in range(p)]
    e=rand_below(x,rng); f=rand_below(x,rng)
    if e is None or f is None: continue
    if any(2*a+b>2*xi for a,b,xi in zip(e,f,x)): continue
    d=[xi-max(max(a,b)/2,(2*a+b)/4) for a,b,xi in zip(e,f,x)]
    assert all(v>=0 for v in d)
    assert sum(xi-v for xi,v in zip(x,d))==F(3,4)+sum(max(0,b-2*a) for a,b in zip(e,f))/4
    rows={PEN[0]:e,PEN[1]:e,PEN[2]:f}
    for l in M:
        r=rand_below(d,rng)
        if r is None: r=d[:]   # any vector <= d (mass irrelevant for the criterion)
        rows[l]=r
    for i in range(p):
        w=[rows[l][i] for l in range(7)]
        assert max(w)<=x[i] and sum(w)<=4*x[i]
        for q in range(7): assert sum(w[l] for l in range(7) if q in L[l])<=2*x[i]
    ok+=1
print('mixed pencil (e,e,f): exact Fano criterion + cost identity verified in',ok,'random cases')
