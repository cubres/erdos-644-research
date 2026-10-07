"""End-to-end exact check of the ADAPTIVE QUADRILATERAL LEMMA.
Type e on the 4 Fano lines missing a point p; three adaptive requests on the lines through p:
  c = min(x, 2x-2e) (per part), r1 <= c              cost kappa = sum (2e-x)^+
  r2 <= c - r1/2                                      cost kappa + (sum r1)/2
  r3 <= min(c, 2c - r1 - r2)                          cost <= kappa + (sum r1)/2
Adversarial answers: random vectors below the bounds with total 1 (when possible).  Verify the Fano
criterion (Lemma 7.63) in every part with exact rationals, and the request costs."""
import random
from fractions import Fraction as F
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
p0=0
S=[l for l in range(7) if p0 not in L[l]]; R=[l for l in range(7) if p0 in L[l]]
def rand_below(B,rng,total=1):
    # random vector 0<=v<=B with sum = total if sum B >= total (adversarial-ish: greedy fill random order)
    if sum(B) < total: return None
    v=[F(0)]*len(B); order=list(range(len(B))); rng.shuffle(order); rem=F(total)
    for i in order:
        take=min(B[i], rem*F(rng.randint(1,10),10)) if rng.random()<0.5 else min(B[i],rem)
        v[i]+=take; rem-=take
    for i in order:
        if rem==0: break
        take=min(B[i]-v[i],rem); v[i]+=take; rem-=take
    assert rem==0
    return v
rng=random.Random(7); ok=0; tested=0
for trial in range(20000):
    p=rng.randint(1,5)
    x=[F(rng.randint(1,40),20) for _ in range(p)]
    if sum(x)<F(7,4): continue
    # random type e with sum 1, e<=x
    e=rand_below(x,rng)
    if e is None: continue
    c=[min(xi,2*xi-2*ei) for xi,ei in zip(x,e)]
    kappa=sum(max(0,2*ei-xi) for xi,ei in zip(x,e))
    r1=rand_below(c,rng)
    if r1 is None: continue
    B2=[ci-a/2 for ci,a in zip(c,r1)]
    r2=rand_below(B2,rng)
    if r2 is None: continue
    B3=[min(ci,2*ci-a-b) for ci,a,b in zip(c,r1,r2)]
    r3=rand_below(B3,rng)
    if r3 is None: continue
    tested+=1
    cost1=sum(xi-ci for xi,ci in zip(x,c)); cost2=sum(xi-b for xi,b in zip(x,B2)); cost3=sum(xi-b for xi,b in zip(x,B3))
    assert cost1==kappa and cost2==kappa+F(1,2) and cost3<=kappa+F(1,2)
    rows={l:e for l in S}; rows[R[0]]=r1; rows[R[1]]=r2; rows[R[2]]=r3
    for i in range(p):
        w=[rows[l][i] for l in range(7)]
        assert max(w)<=x[i]
        for q in range(7): assert sum(w[l] for l in range(7) if q in L[l])<=2*x[i]
        assert sum(w)<=4*x[i]
    ok+=1
print('adaptive quadrilateral lemma: exact Fano criterion verified in',ok,'of',tested,'random adversarial runs')
