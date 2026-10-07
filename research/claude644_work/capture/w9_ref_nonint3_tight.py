"""Referee w9, nonint#3: tightness of Lemma H / Prop B via the Prop C family (exact integers).
For k and delta, find the largest s such that some c satisfies Prop C's sufficient conditions (0),(1),(2)
plus the side conditions used for tau and Gamma (s>=2delta+1, c>=delta+1, c-delta>s, 2c<=k+s, c<=k).
Compare 7s with 5k-2delta (Prop B ceiling: 7s <= 5k-2delta+25) and the Lemma H host bound at U=core."""
from fractions import Fraction as Fr
def ok(k,s,c,d):
    if not (4*s<3*k and s>=2*d+1 and c>=d+1 and c-d>s and 2*c<=k+s and c<=k): return False
    for a in range(1,7):
        ca=c-a*d
        if not ((ca>s and (5-a)*s<2*k+ca) or ((6-a)*s<k+2*ca)): return False
    for a in range(1,6):
        for b in range(1,7-a):
            if not (4*(c-a*d)*(c-b*d) > (7-a-b)*s*s): return False
    return True
def best(k,d):
    for s in range((5*k)//7+5, -1, -1):
        for c in range((k+s)//2, d, -1):
            if ok(k,s,c,d): return s,c
    return None
k=1400
print('k',k)
last_tight=None
for d in range(0, k//8, 7):
    r=best(k,d)
    if r is None: print('delta',d,'none'); continue
    s,c=r; gap=5*k-2*d-7*s
    hostbound=Fr(5*(k+s)-2*d+38,12)
    print(f'delta/k={d/k:.3f} s={s} c={c}  5k-2d-7s={gap}  tau(H[U])=s+1={s+1}  LemmaH bound={float(hostbound):.2f}')
    if gap<=14: last_tight=d
print('tight (5k-2d-7s<=14) up to delta/k =', last_tight/k)
# the exact family k=140n, s=98n-1, c=119n-1, delta=7n
for n in range(1,60):
    assert ok(140*n,98*n-1,119*n-1,7*n), n
    k,s,d=140*n,98*n-1,7*n
    assert Fr(5*(k+s)-2*d+38,12) - (s+1) == Fr(33,12)
print('exact family k=140n: Prop C conditions hold n<60; Lemma H bound - tau(H[U]) = 33/12 exactly')
