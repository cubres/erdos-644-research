# Referee w9, randomside#0 (i): random + locally-minimal families on larger N (exact tau by brute force
# over vertex subsets), checking |H| >= L(tau(H)) and also |H| >= L(T) for every T<=tau.
import itertools, random, sys
from fractions import Fraction
from math import comb
def L_of(N,k,T):
    b=Fraction(0)
    for D in range(1,T+1):
        cu=comb(N-T+D,k)
        if cu==0: return None
        b=max(b,Fraction(D*comb(N,k),cu))
    return b
def tau(N,H):
    # H: list of bitmasks; tau = N - alpha
    for a in range(N,-1,-1):
        for S in itertools.combinations(range(N),a):
            m=sum(1<<v for v in S)
            if all(e & m != e for e in H): return N-a
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
viol=0; tight=0; cnt=0; worst=None
for trial in range(400):
    N=random.randint(6,11); k=random.randint(2,min(4,N-2))
    allE=[sum(1<<v for v in c) for c in itertools.combinations(range(N),k)]
    T=random.randint(1,N-k+1)
    random.shuffle(allE)
    H=[]
    for e in allE:
        H.append(e)
        if tau(N,H)>=T: break
    # prune to edge-minimal with tau>=T
    for e in list(H):
        H2=[f for f in H if f!=e]
        if tau(N,H2)>=T: H=H2
    t=tau(N,H); cnt+=1
    for TT in range(1,t+1):
        L=L_of(N,k,TT)
        if L is None or len(H)<L: viol+=1; print('VIOL',N,k,t,TT,len(H),L)
    L=L_of(N,k,t)
    r=Fraction(len(H))/L
    if worst is None or r<worst[0]: worst=(r,N,k,t,len(H),L)
    if len(H)==L: tight+=1
print('families',cnt,'violations',viol,'tight',tight,'min ratio |H|/L',float(worst[0]),worst[1:5],float(worst[5]))
