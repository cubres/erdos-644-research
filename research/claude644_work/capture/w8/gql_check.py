"""Exact random check of the GENERAL QUADRILATERAL LEMMA (GQL).
Fano point p; the 4 lines missing p carry arbitrary actual types Q1..Q4; the 3 lines through p are
requested adaptively in order mu1, mu2, mu3 (each p-line <-> perfect matching of the 4 quad lines).
Per part: c_mu = min(x, 2x - Qa - Qb, 2x - Qc - Qd), S = min(2x, 4x - sum Q)  (c_mu <= S/2).
  r1 <= c1                        cost K1 = sum (x - c1)
  r2 <= min(c2, S/2 - r1/2)       cost <= K2 + 1/2
  r3 <= min(c3, S - r1 - r2)      cost <= K3 + 1/2
Checks the Fano criterion (note Lemma 7.63: row<=x, every pencil<=2x, total<=4x) in every part, the
claimed cost bounds, and c_mu <= S/2, with exact rationals and adversarial random responses."""
import random, itertools
from fractions import Fraction as F
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
p0=0
QL=[l for l in range(7) if p0 not in L[l]]; PL=[l for l in range(7) if p0 in L[l]]
def matching_of(pl):
    # quad lines through the two other points of p-line pl
    q, q2 = [pt for pt in L[pl] if pt != p0]
    A = [k for k,l in enumerate(QL) if q in L[l]]; B = [k for k,l in enumerate(QL) if q2 in L[l]]
    assert len(A)==2 and len(B)==2 and set(A)|set(B)=={0,1,2,3}
    return A, B
MU = {pl: matching_of(pl) for pl in PL}
def rand_below(B,rng,total=1):
    if sum(B) < total: return None
    v=[F(0)]*len(B); order=list(range(len(B))); rng.shuffle(order); rem=F(total)
    for i in order:
        take=min(B[i], rem*F(rng.randint(1,10),10)) if rng.random()<0.5 else min(B[i],rem)
        v[i]+=take; rem-=take
    for i in order:
        if rem==0: break
        take=min(B[i]-v[i],rem); v[i]+=take; rem-=take
    return v
rng=random.Random(11); ok=0; tested=0
for trial in range(40000):
    p=rng.randint(1,5); x=[F(rng.randint(1,40),20) for _ in range(p)]
    Q=[rand_below(x,rng) for _ in range(4)]
    if any(q is None for q in Q): continue
    if rng.random()<0.3: Q[1]=Q[0]
    if rng.random()<0.3: Q[3]=Q[2]
    order=PL[:]; rng.shuffle(order)
    c={}
    for pl in PL:
        A,B=MU[pl]; c[pl]=[min(x[i],2*x[i]-Q[A[0]][i]-Q[A[1]][i],2*x[i]-Q[B[0]][i]-Q[B[1]][i]) for i in range(p)]
    S=[min(2*x[i],4*x[i]-sum(q[i] for q in Q)) for i in range(p)]
    assert all(c[pl][i]<=S[i]/2 for pl in PL for i in range(p))
    K={pl: sum(x[i]-c[pl][i] for i in range(p)) for pl in PL}
    l1,l2,l3=order
    r1=rand_below(c[l1],rng)
    if r1 is None: continue
    B2=[min(c[l2][i],S[i]/2-r1[i]/2) for i in range(p)]
    r2=rand_below(B2,rng)
    if r2 is None: continue
    B3=[min(c[l3][i],S[i]-r1[i]-r2[i]) for i in range(p)]
    r3=rand_below(B3,rng)
    if r3 is None: continue
    tested+=1
    assert all(b>=0 for b in B2+B3)
    assert sum(x[i]-B2[i] for i in range(p))<=K[l2]+F(1,2)
    assert sum(x[i]-B3[i] for i in range(p))<=K[l3]+F(1,2)
    rows={QL[k]:Q[k] for k in range(4)}; rows[l1]=r1; rows[l2]=r2; rows[l3]=r3
    for i in range(p):
        w=[rows[l][i] for l in range(7)]
        assert max(w)<=x[i] and sum(w)<=4*x[i]
        for q in range(7): assert sum(w[l] for l in range(7) if q in L[l])<=2*x[i]
    ok+=1
print('GQL: exact Fano criterion + cost bounds verified in',ok,'of',tested,'adversarial runs')
