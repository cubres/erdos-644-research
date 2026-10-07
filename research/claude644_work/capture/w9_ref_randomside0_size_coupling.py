# Referee w9, claim randomside#0: size lemma (i) and monotone coupling (ii). Exact checks on small instances.
from itertools import combinations
from fractions import Fraction as Fr
from math import comb, ceil, floor
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def L_of(N,k,T):
    best=Fr(0)
    for D in range(1,T+1):
        u=N-T+D
        if comb(u,k)==0: return None   # tau>=T impossible (vacuous)
        best=max(best,Fr(D*comb(N,k),comb(u,k)))
    return best

# (i) exact min |H| with tau>=T  == Turan number: every (N-T+1)-set contains an edge. ILP (integral, HiGHS exact on 0/1 small)
def min_size(N,k,T):
    E=list(combinations(range(N),k)); idx={e:i for i,e in enumerate(E)}
    u=N-T+1
    if u<k: return None
    rows=[]
    for U in combinations(range(N),u):
        r=np.zeros(len(E));
        for e in combinations(U,k): r[idx[e]]=1
        rows.append(r)
    A=np.array(rows)
    res=milp(c=np.ones(len(E)),constraints=LinearConstraint(A,1,np.inf),integrality=np.ones(len(E)),bounds=Bounds(0,1))
    return round(res.fun)
print("== (i) size lemma vs exact minimum |H| with tau>=T ==")
bad=0
for k in (2,3,4):
    for N in range(k+1,10 if k<4 else 9):
        for T in range(1,N-k+2):
            L=L_of(N,k,T); m=min_size(N,k,T)
            if L is None or m is None: continue
            ok = m>=L
            if not ok: bad+=1
            if not ok or (k,N) in [(2,7),(3,8),(4,8)]:
                print(f"k={k} N={N} T={T} L={float(L):.3f} ceilL={ceil(L)} exact_min={m} {'OK' if ok else 'VIOLATION'}")
print("size-lemma violations:",bad)

# (ii) exact P(m) for small K_N^(k); (7,2) defined as: every subfamily of <=7 edges has tau<=2.
def exact_P(N,k):
    E=list(combinations(range(N),k)); ne=len(E)
    hit=[]
    pts=[()]+[(a,) for a in range(N)]+list(combinations(range(N),2))
    for P in pts:
        msk=0
        for i,e in enumerate(E):
            if set(P)&set(e): msk|=1<<i
        hit.append(msk)
    full=(1<<ne)
    good=bytearray(full)
    order=sorted(range(full),key=lambda s:bin(s).count('1'))
    for s in order:
        c=bin(s).count('1')
        if c<=7:
            good[s]= any((s & ~h)==0 for h in hit)
        else:
            g=1; t=s
            while t:
                b=t&-t; t^=b
                if not good[s^b]: g=0; break
            good[s]=g
    cnt=[0]*(ne+1)
    for s in range(full):
        if good[s]: cnt[bin(s).count('1')]+=1
    P=[Fr(cnt[m],comb(ne,m)) for m in range(ne+1)]
    return ne,cnt,P

def binom_pmf(n,p,m): return comb(n,m)*p**m*(1-p)**(n-m)
print("== (ii) monotone coupling ==")
for (N,k) in [(5,2),(6,2),(5,3)]:
    ne,cnt,P=exact_P(N,k)
    mono=all(P[m]>=P[m+1] for m in range(ne))
    print(f"N={N} k={k} |K|={ne} P(m)=",[round(float(x),4) for x in P]," nonincreasing:",mono)
    worst=0
    for Lnum in range(1,4*ne+1):
        L=Fr(Lnum,4)                     # non-integer L allowed
        PL = P[ceil(L)] if ceil(L)<=ne else Fr(0)
        for rn in range(1,40):
            rho=Fr(rn,40)
            lhs=sum(binom_pmf(ne,rho,m)*P[m] for m in range(ceil(L),ne+1))
            assert lhs<=PL, (N,k,L,rho)
        rp = L/(2*ne)
        if rp<=1:
            rhs=2*sum(binom_pmf(ne,rp,m)*P[m] for m in range(ne+1))
            assert PL<=rhs,(N,k,L)
            if rhs>0: worst=max(worst,float(PL/rhs))
    print("   all (ii) inequalities hold; max P(L)/(2Pr_rho'[(7,2)]) =",round(worst,4))
