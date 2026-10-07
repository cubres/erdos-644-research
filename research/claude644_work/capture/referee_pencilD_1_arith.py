#!/usr/bin/env python3
"""Referee arithmetic for Lemma D / D' (exact integers, fractions).
1. For every (e,|R|,t,m) in a box with 2ceil(e/4)+m <= t-1: build the explicit balanced
   allocation, check all four m-line loads <= t-1 and pencil loads <= stated bound.
2. Compare the stated bound with the exact optimum of the labelling scheme (all splits).
3. Critical-host corollary: |R|=t-1. For every q allowed by Lemma D (q <= bound) check
   t <= 3e/4 + d/2 + 11/4 (+m for D'), d=t-q. Report violations and verify the corrected form
   t <= max(2c + d, 3c + m + (d+1)/2).
"""
from fractions import Fraction as Fr
from math import ceil
def quarters(e):
    b,r=divmod(e,4); return [b+1]*r+[b]*(4-r)   # eb,eb',ec,ec'
def stated(e,R,t,m=0):
    c=ceil(e/4); return max(2*c, R+6*c+2*m-2*t+2)
def alloc(e,R,t,m):
    eb,ebp,ec,ecp=quarters(e); c=ceil(e/4)
    cap=t-1-2*c-m
    ra=min(cap,(R+1)//2); rap=min(cap,R-ra); w=R-ra-rap
    loads=[ra+eb+ec+m, rap+ebp+ec+m, rap+eb+ecp+m, ra+ebp+ecp+m]   # M1..M4 (each carries m in D')
    pencil=w+max(eb+ebp,ec+ecp)
    return loads,pencil,w
def optimum(e,R,t,m):
    best=None
    for eb in range(e+1):
        for ebp in range(e-eb+1):
            for ec in range(e-eb-ebp+1):
                ecp=e-eb-ebp-ec
                ra=min(t-1-m-eb-ec,t-1-m-ebp-ecp); rap=min(t-1-m-ebp-ec,t-1-m-eb-ecp)
                if ra<0 or rap<0: continue
                w=max(0,R-ra-rap); v=w+max(eb+ebp,ec+ecp)
                best=v if best is None else min(best,v)
    return best
viol_alloc=0; worse=0; n=0
for m in range(0,4):
  for t in range(2,26):
    for e in range(1,30):
      c=ceil(e/4)
      if 2*c+m>t-1: continue
      for R in range(0,45):
        n+=1
        loads,pencil,w=alloc(e,R,t,m)
        if max(loads)>t-1 or pencil>stated(e,R,t,m) or w<0: viol_alloc+=1
        if e<=16 and R<=30:
            o=optimum(e,R,t,m)
            if o>stated(e,R,t,m): worse+=1
print(f"cases {n}: allocation violations {viol_alloc}, optimum>stated {worse}")
# corollary
bad=[];badfix=0;tot=0
for m in range(0,4):
  for t in range(2,60):
    for e in range(1,80):
      c=ceil(e/4)
      if 2*c+m>t-1: continue
      B=stated(e,t-1,t,m)
      for q in range(1,min(B,t)+1):
        d=t-q; tot+=1
        if Fr(t) > Fr(3*e,4)+Fr(d,2)+Fr(11,4)+m: bad.append((m,t,e,q,d,4*c>=t))
        if Fr(t) > max(Fr(2*c+d), Fr(3*c+m)+Fr(d+1,2)): badfix+=1
print(f"corollary checks {tot}: stated-corollary failures {len(bad)}; corrected-form failures {badfix}")
print("any failure with 4ceil(e/4)>=t ?", any(x[5] for x in bad))
print("sample failures (m,t,e,q,d):",[x[:5] for x in bad[:8]])
# failures restricted to e >= t - something
print("min t-e among failures:",min(x[1]-x[2] for x in bad) if bad else None)
