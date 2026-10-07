#!/usr/bin/env python3
"""Referee (independent) check of Anchored Theorem P.
(1) Direct convexity proof: if a in Adm with a <= u = x - 3a0/4, then b=(2a+a0)/3 satisfies 6b+a0 <= 4x.
(2) M_1 realization: given per-part (s=a0_i, t=b_i, x_i) with x_i >= max(s, s/4+3t/2), build parent cells
    (4 complements containing anchor row 0, 3 complements not containing it), trim rows to exact loads, and verify:
    loads exact, mass <= x_i, every cell inside a line complement (so no two cells cover all 7 rows).
Exact Fractions throughout."""
from fractions import Fraction as F
import random, itertools
random.seed(12345)
LINES=[{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
COMP=[frozenset(range(7))-L for L in LINES]
def rf(den=24,hi=48): return F(random.randint(0,hi),den)
fails=0; n1=0
for trial in range(20000):
    p=random.randint(1,5)
    x=[rf()+F(1,24) for _ in range(p)]
    a0=[min(x[i],rf()) for i in range(p)]
    a=[min(x[i]-F(3,4)*a0[i], rf()) for i in range(p)]
    a=[max(F(0),v) for v in a]
    b=[(2*a[i]+a0[i])/3 for i in range(p)]
    n1+=1
    if any(6*b[i]+a0[i]>4*x[i] for i in range(p)): fails+=1
print("(1) direct convexity step:",n1,"cases, failures",fails)
# (2) M_1 realization
f2=0; n2=0
anc=[c for c in COMP if 0 in c]; oth=[c for c in COMP if 0 not in c]
assert len(anc)==4 and len(oth)==3
for trial in range(20000):
    s=rf(); t=rf(); xi=max(s, s/4+F(3,2)*t)+rf(48,6)
    cells={}
    for c in anc: cells[c]=cells.get(c,F(0))+s/4
    Y=max(F(0),F(3,2)*t-F(3,4)*s)
    for c in oth: cells[c]=cells.get(c,F(0))+Y/3
    target=[s]+[t]*6
    # trim: for each row j, remove excess by moving mass from cells containing j to cell\{j}
    for j in range(7):
        load=sum(m for c,m in cells.items() if j in c)
        ex=load-target[j]
        assert ex>=0
        for c in list(cells):
            if ex==0: break
            if j in c and cells[c]>0:
                mv=min(ex,cells[c]); cells[c]-=mv; d=c-{j}; cells[d]=cells.get(d,F(0))+mv; ex-=mv
    n2+=1
    loads=[sum(m for c,m in cells.items() if j in c) for j in range(7)]
    mass=sum(cells.values())
    pos=[c for c,m in cells.items() if m>0]
    ok = loads==target and mass<=xi and all(any(c<=C for C in COMP) for c in pos) \
         and all(len(c1|c2)<7 for c1 in pos for c2 in pos)
    if not ok: f2+=1
print("(2) M_1 realization:",n2,"cases, failures",f2)
