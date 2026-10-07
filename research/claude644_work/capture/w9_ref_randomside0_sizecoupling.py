# Referee w9, claim randomside#0: size lemma (i) and monotone coupling (ii). Exact, exhaustive on small cases.
import itertools, sys, numpy as np
from fractions import Fraction as Fr
from math import comb

def setup(N,k):
    E=list(itertools.combinations(range(N),k)); m=len(E)
    inside=np.zeros(1<<N,dtype=np.int64)
    for S in range(1<<N):
        msk=0
        for i,e in enumerate(E):
            if all((S>>v)&1 for v in e): msk|=1<<i
        inside[S]=msk
    return E,m,inside

def taus(N,m,inside,F):
    # tau = N - alpha, alpha = max |S| with F & inside[S]==0
    pc=np.array([bin(S).count('1') for S in range(1<<N)])
    alpha=np.zeros(len(F),dtype=np.int64)
    for S in np.argsort(pc):
        ok=(F & inside[S])==0
        alpha=np.where(ok,np.maximum(alpha,pc[S]),alpha)
    return N-alpha

def Lval(N,k,T):
    best=None
    for D in range(1,T+1):
        u=N-T+D; c=comb(u,k)
        if c==0: return None  # infinite
        v=Fr(D*comb(N,k),c)
        best=v if best is None or v>best else best
    return best

def seven2(N,k,E,m):
    # boolean array over all 2^m families: is (7,2) (every <=7 edges 2-pierceable)
    Pm=[]
    for x in range(N):
        for y in range(x,N):
            Pm.append(sum(1<<i for i,e in enumerate(E) if x in e or y in e))
    F=np.arange(1<<m,dtype=np.int64)
    pierce=np.zeros(1<<m,dtype=bool)
    full=(1<<m)-1
    for P in Pm: pierce|=(F & (full^P))==0
    pc=np.array([bin(f).count('1') for f in range(1<<m)])
    badmin=(~pierce)&(pc<=7)
    # superset closure: contains a bad <=7 subfamily
    cont=badmin.copy()
    for b in range(m):
        idx=F[(F>>b)&1==1]
        cont[idx]|=cont[idx^(1<<b)]
    return ~cont, pc

def run(N,k):
    E,m,inside=setup(N,k)
    F=np.arange(1<<m,dtype=np.int64)
    tau=taus(N,m,inside,F)
    ok7,pc=seven2(N,k,E,m)
    # (i)
    viol=0; tight=0
    maxT=int(tau.max())
    for T in range(1,maxT+1):
        L=Lval(N,k,T)
        sel=tau>=T
        mn=int(pc[sel].min())
        if L is None or mn < L: viol+=1; print('VIOLATION (i)',N,k,T,L,mn)
        if mn==-(-L.numerator//L.denominator): tight+=1
        print(f'N={N} k={k} T={T}: L={float(L):.4f} min|H| with tau>=T = {mn}')
    # (ii)
    Pm=[]
    for mm in range(m+1):
        s=pc==mm; Pm.append(Fr(int(ok7[s].sum()),int(s.sum())))
    mono=all(Pm[i]>=Pm[i+1] for i in range(m))
    print('P(m):',[str(p) for p in Pm],'nonincreasing:',mono)
    def prob(rho,event_by_size):  # sum over sizes
        return sum(Fr(comb(m,j))*rho**j*(1-rho)**(m-j)*event_by_size[j] for j in range(m+1))
    worst=None
    for T in range(1,maxT+1):
        L=Lval(N,k,T); cl=-(-L.numerator//L.denominator); fl=L.numerator//L.denominator
        rp=L/(2*comb(N,k)); assert rp<=1
        rhs=2*prob(rp,Pm)
        for rho in [Fr(i,20) for i in range(1,20)]+[Fr(1,100),Fr(99,100)]:
            # exact Pr[(7,2) & tau>=T]
            ev=[Fr(int((ok7&(tau>=T)&(pc==j)).sum()),comb(m,j)) for j in range(m+1)]
            lhs0=prob(rho,ev)
            lhs1=prob(rho,[Pm[j] if j>=L else 0 for j in range(m+1)])
            assert lhs0<=lhs1<=Pm[cl]<=rhs, (T,rho)
            assert Pm[fl]<=rhs or fl==L
        r=float(Pm[cl]/rhs) if rhs>0 else 0
        worst=max(worst or 0,r)
        print(f' T={T} ceilL={cl} P(ceilL)={float(Pm[cl]):.4g} 2Pr_rho\'={float(rhs):.4g}')
    print('ALL (ii) CHECKS PASS; max ratio P(L)/(2Pr_rho\') =',worst)
    # side condition: T > N-k+1
    T=N-k+2
    print('T=N-k+2 ->',Lval(N,k,T),'(no family has tau>=T; rho\' undefined: side condition T<=N-k+1 needed)')

for N,k in [(5,2),(6,2),(6,3),(7,2)]:
    print('=====',N,k); run(N,k)
