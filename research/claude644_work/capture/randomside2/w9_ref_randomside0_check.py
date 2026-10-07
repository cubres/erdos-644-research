# Referee check for claim randomside#0 (size lemma + monotone coupling). Exact arithmetic.
# Part A: exhaustive over ALL k-uniform families on [N] for (N,k) in {(5,2),(6,2),(5,3),(6,3)}:
#   (i) min |H| over tau(H)>=T  vs  L(T) = max_D D C(N,k)/C(N-T+D,k)
#   (ii) for many rational rho: Pr_rho[(7,2)&tau>=T] <= Pr_rho[(7,2)&|H|>=L] <= P(ceil L) <= 2 Pr_{rho'}[(7,2)]
#   and P(m) nonincreasing.
# Part B: (i) for k=2, N<=40 via Turan (min edges with alpha<=N-T = C(N,2)-t(N,N-T)); k=3,4 small N via MILP.
import itertools, sys, numpy as np
from fractions import Fraction as F
from math import comb, ceil, floor

def Lval(N,k,T):
    best=None
    for D in range(1,T+1):
        u=N-T+D
        if comb(u,k)==0: return None
        v=F(D*comb(N,k),comb(u,k))
        if best is None or v>best: best=v
    return best

def exhaustive(N,k):
    edges=list(itertools.combinations(range(N),k)); E=len(edges)
    masks=np.arange(1<<E,dtype=np.int64)
    pc=np.zeros(1<<E,dtype=np.int64)
    for b in range(E): pc+= (masks>>b)&1
    # alpha
    alpha=np.zeros(1<<E,dtype=np.int64)
    for S in range(1<<N):
        ins=0
        for i,e in enumerate(edges):
            if all((S>>x)&1 for x in e): ins|=1<<i
        s=bin(S).count('1')
        ok=(masks & ins)==0
        alpha=np.where(ok & (alpha<s), s, alpha)
    tau=N-alpha
    # tau<=2 test for small masks
    hits=[]
    for c in list(itertools.combinations(range(N),2))+[(x,) for x in range(N)]:
        h=0
        for i,e in enumerate(edges):
            if set(c)&set(e): h|=1<<i
        hits.append(h)
    full=(1<<E)-1
    good=np.zeros(1<<E,dtype=bool)
    for p in range(E+1):
        M=masks[pc==p]
        if p<=7:
            r=np.zeros(len(M),dtype=bool)
            for h in hits: r|= (M & (full^h))==0
            if p==0: r[:]=True
        else:
            r=np.ones(len(M),dtype=bool)
            for b in range(E):
                sel=((M>>b)&1)==1
                r[sel]&=good[M[sel]^(1<<b)]
        good[pc==p]=r
    # sanity: for masks <=7 good iff tau<=2 ; for all masks good iff every <=7 subfamily tau<=2 (DP)
    assert np.all(good[pc<=7]==(tau[pc<=7]<=2))
    return E,pc,tau,good

def poly_prob(counts,E,rho):
    return sum(F(c)*rho**m*(1-rho)**(E-m) for m,c in enumerate(counts))

bad=0
for (N,k) in [(5,2),(6,2),(5,3),(6,3)]:
    E,pc,tau,good=exhaustive(N,k)
    cnt72=[int(np.sum(good&(pc==m))) for m in range(E+1)]
    P=[F(cnt72[m],comb(E,m)) for m in range(E+1)]
    mono=all(P[m]>=P[m+1] for m in range(E))
    print(f"N={N} k={k} E={E} P(m) nonincreasing: {mono}; P={[str(x) for x in P]}")
    if not mono: bad+=1
    for T in range(1,N-k+2):
        L=Lval(N,k,T)
        mn=int(pc[tau>=T].min())
        okA= mn>=L
        # which D attains L
        Ds=[D for D in range(1,T+1) if F(D*comb(N,k),comb(N-T+D,k))==L]
        print(f"  T={T}: min|H| with tau>=T = {mn}, L={L} (~{float(L):.3f}, argmax D={Ds}), (i) holds: {okA}")
        if not okA: bad+=1
        Lc=ceil(L)
        cA=[int(np.sum(good&(tau>=T)&(pc==m))) for m in range(E+1)]
        cB=[cnt72[m] if m>=L else 0 for m in range(E+1)]
        rhop=L/(2*comb(N,k))
        rhs=2*poly_prob(cnt72,E,rhop)
        for rho in [F(i,40) for i in range(1,40)]+[F(1,1000),F(999,1000)]:
            a=poly_prob(cA,E,rho); b=poly_prob(cB,E,rho)
            if not (a<=b<=P[Lc]<=rhs):
                print("   VIOLATION",N,k,T,rho,float(a),float(b),float(P[Lc]),float(rhs)); bad+=1
        print(f"     P(ceilL)={float(P[Lc]):.4g}  2Pr_rho'={float(rhs):.4g}  max_rho Pr[(7,2)&tau>=T] ok")
# Part B
print("Part B: k=2 Turan check N<=40")
def turan(n,r):  # edges of Turan graph T(n,r)
    q,s=divmod(n,r); parts=[q+1]*s+[q]*(r-s)
    return (n*n-sum(p*p for p in parts))//2
for N in range(3,41):
    for T in range(1,N):
        # min edges with tau>=T <=> alpha<=N-T <=> complement K_{N-T+1}-free: max complement edges = t(N,N-T)
        mn=comb(N,2)-turan(N,N-T)
        L=Lval(N,2,T)
        if not mn>=L: print("VIOLATION k=2",N,T,mn,L); bad+=1
print("Part B done k=2")
from scipy.optimize import milp, LinearConstraint, Bounds
for (N,k) in [(7,3),(8,3),(9,3),(8,4),(9,4),(10,4),(10,5)]:
    edges=list(itertools.combinations(range(N),k)); idx={e:i for i,e in enumerate(edges)}
    for T in range(2,N-k+2):
        u=N-T+1
        rows=[]
        for S in itertools.combinations(range(N),u):
            r=np.zeros(len(edges))
            for e in itertools.combinations(S,k): r[idx[e]]=1
            rows.append(r)
        A=np.array(rows)
        res=milp(c=np.ones(len(edges)),constraints=LinearConstraint(A,lb=1,ub=np.inf),integrality=np.ones(len(edges)),bounds=Bounds(0,1))
        mn=round(res.fun); L=Lval(N,k,T)
        flag="" if mn>=L else "VIOLATION"
        if flag: bad+=1
        print(f"  N={N} k={k} T={T}: Turan min={mn} L={float(L):.3f} {flag}")
print("TOTAL VIOLATIONS:",bad)
