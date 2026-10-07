# Referee w9, claim randomside#0 part (i): size lemma.
# Exhaustive exact check: for every k-uniform H on [N] (small N,k), and every T<=tau(H),
#   |H| >= L(T) := max_{1<=D<=T} D*C(N,k)/C(N-T+D,k)    (exact Fractions).
# Also reports min |H| per tau (Turan-type numbers) vs L, and a MUTATION (D -> D+1 in numerator)
# to show the test has power.
import itertools, sys
from fractions import Fraction
from math import comb
import numpy as np

def L_of(N,k,T,mut=0):
    best=Fraction(0)
    for D in range(1,T+1):
        u=N-T+D
        cu=comb(u,k)
        if cu==0: return None   # vacuous (T > N-k+1)
        best=max(best,Fraction((D+mut)*comb(N,k),cu))
    return best

def run(N,k):
    edges=list(itertools.combinations(range(N),k))
    E=len(edges)
    emask=[sum(1<<v for v in e) for e in edges]
    # tau via: tau(H) = N - alpha(H); alpha = max vertex set containing no edge.
    # For each vertex subset S, edges inside S: bitmask over edges.
    inside=np.zeros(1<<N,dtype=np.int64)
    for S in range(1<<N):
        m=0
        for i,em in enumerate(emask):
            if em & S == em: m|=1<<i
        inside[S]=m
    pc=np.array([bin(S).count('1') for S in range(1<<N)])
    order=np.argsort(-pc,kind='stable')
    minsize={}
    viol=0; mutviol=0
    Ls={T:L_of(N,k,T) for T in range(0,N+1)}
    Lm={T:L_of(N,k,T,1) for T in range(0,N+1)}
    for H in range(1<<E):
        # alpha = largest S with inside[S] & H == 0
        a=0
        for S in order:
            if inside[S] & H == 0:
                a=pc[S]; break
        tau=N-a; h=bin(H).count('1')
        if tau not in minsize or h<minsize[tau]: minsize[tau]=h
    for tau,h in sorted(minsize.items()):
        for T in range(1,tau+1):
            L=Ls[T]
            if L is None or h < L: viol+=1; print('VIOLATION',N,k,tau,T,h,L)
            if Lm[T] is not None and h < Lm[T]: mutviol+=1
    print(f'N={N} k={k} families={1<<E} minsize-by-tau={minsize}')
    print('   L(T):',{T:(float(Ls[T]) if Ls[T] is not None else None) for T in range(1,N+1)})
    print(f'   violations={viol}  mutation(D+1) violations={mutviol}')
    return viol

tot=0
for N,k in [(4,2),(5,2),(6,2),(5,3),(6,4),(6,5),(5,4)]:
    tot+=run(N,k)
print('TOTAL violations',tot)
