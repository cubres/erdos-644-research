# End-to-end exact check of: closed two-part type sets with tau*>3/4 have a bad tuple
# via  homogeneous Fano  or  Gap-Pair Lemma (Q_a, Q_b, V(a,b)).
import random
from fractions import Fraction as F
from itertools import product
random.seed(7)
def tau2(x,y,C):
    # exact tau* for finite type set C (first-part sizes), two parts: kill-map formula
    # each type t=(t,1-t) killed at part1 (needs t>0) with u1<t, or part2 (needs t<1) with u2<1-t
    # optimal: choose threshold: u1 < m1 kills types with t>=... ; enumerate: set K1 killed in part 1 = {t > s} style
    ts=sorted(C); best=None
    # killed-at-part1 set must be an up-set in t (if t killed at part1 with u1<t then all t'>=t also killed); similarly part2 kills down-set
    for i in range(len(ts)+1):
        low=ts[:i]; high=ts[i:]   # low killed in part 2, high killed in part 1
        if any(t==0 for t in high) or any(t==1 for t in low): continue
        cost=F(0)
        if high: cost+=x-min(high)
        if low: cost+=y-(1-max(low))
        best=cost if best is None or cost<best else best
    # also total<1 option is included (i splits) -- N-1-gap covers it; add N-1 explicitly for safety
    best=min(best, x+y-1)
    return best
def Mq(s,t): return max(3*t/2, s+3*t/4)          # t-rows on a line, s-rows on quad
def MV(s,t): return max(s+t, 5*s/4+t/2)
def ok2(M,x,y,s,t): return M(s,t)<=x and M(1-s,1-t)<=y
cnt=0; used={'hom':0,'Qb':0,'Qa':0,'V':0}
for it in range(300000):
    d=random.choice([10,12,20,24,40,60])
    x=F(random.randint(d//2,2*d),d); y=F(random.randint(d//2,2*d),d)
    k=random.randint(1,5)
    C=set()
    for _ in range(k):
        t=F(random.randint(0,d),d)
        if t<=x and 1-t<=y: C.add(t)
    if not C: continue
    T=tau2(x,y,C)
    if T<=F(3,4): continue
    cnt+=1
    lo=1-4*y/7; hi=4*x/7
    if any(lo<=t<=hi for t in C): used['hom']+=1; continue
    below=[t for t in C if t<lo]; above=[t for t in C if t>hi]
    assert below and above, ('one-sided',x,y,C,T)
    a=max(below); b=min(above)
    assert b-a < x+y-F(7,4), ('gap',x,y,C,T)
    if ok2(Mq,x,y,a,b): used['Qb']+=1
    elif ok2(Mq,x,y,b,a): used['Qa']+=1
    elif ok2(MV,x,y,a,b): used['V']+=1
    else: raise SystemExit(('FAIL',x,y,C,T,a,b))
print('PASS',cnt,used)
# direct stress test of the Gap-Pair Lemma hypotheses
used={'Qb':0,'Qa':0,'V':0}; n=0
for it in range(400000):
    d=random.choice([24,48,96,120,1000])
    a=F(random.randint(0,d),d); b=F(random.randint(0,d),d)
    if a>b: a,b=b,a
    x=F(random.randint(0,7*d),4*d); y=F(random.randint(0,7*d),4*d)
    if not (4*y<7*(1-a) and 4*x<7*b and b-a<x+y-F(7,4)): continue
    n+=1
    if ok2(Mq,x,y,a,b): used['Qb']+=1
    elif ok2(Mq,x,y,b,a): used['Qa']+=1
    elif ok2(MV,x,y,a,b): used['V']+=1
    else: raise SystemExit(('LEMMA FAIL',x,y,a,b))
print('Gap-Pair direct PASS',n,used)
