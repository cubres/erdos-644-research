# Corollary check on actual (7,2) families: every 4-multiset of edges has S>=min(t,floor(3(2t-k-2)/2)+1)
# and tau_f <= 6k/min(...). Families: parity family (small), complete families, greedy random (7,2) families.
import itertools, random, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from w7_ref_coreQ_e2e import tau, two_pierceable, popc
def is72(edges,n):
    for r in range(1,8):
        for c in itertools.combinations(edges,r):
            if not two_pierceable(list(c),n): return False
    return True
def is72_new(edges,new,n):
    for r in range(0,7):
        for c in itertools.combinations(edges,r):
            if not two_pierceable(list(c)+[new],n): return False
    return True
def check(edges,n,k,name):
    t=tau(edges,n)
    if 2*t-k-2<0: print(name,'t',t,'k',k,'skip (2t-k-2<0)'); return
    mm=min(t,(3*(2*t-k-2))//2+1)
    mins=min(sum(popc(G[i]&G[j]) for i,j in itertools.combinations(range(4),2)) for G in itertools.combinations_with_replacement(edges,4))
    # tau_f via LP (fractional cover)
    A=np.array([[ (e>>v)&1 for v in range(n)] for e in edges]); 
    r=linprog(np.ones(n),A_ub=-A,b_ub=-np.ones(len(edges)),bounds=[(0,None)]*n,method='highs')
    print(name,'n',n,'k',k,'|H|',len(edges),'tau',t,'bound m',mm,'min S',mins,'OK' if mins>=mm else 'VIOLATION','tau_f %.4f <= 6k/m=%.3f'%(r.fun,6*k/mm))
# parity family, k=1 version: 4-subsets of 8-set with odd intersection with fixed 4-set
n=8; F=0b1111
par=[sum(1<<v for v in c) for c in itertools.combinations(range(8),4) if popc(sum(1<<v for v in c)&F)%2==1]
check(par,8,4,'parity(4 of 8)')
for (n,k) in [(6,4),(8,5),(9,6),(11,7)]:
    E=[sum(1<<v for v in c) for c in itertools.combinations(range(n),k)]
    if len(E)<=120: check(E,n,k,'K_%d^%d'%(n,k))
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
cnt=0
for trial in range(int(sys.argv[2]) if len(sys.argv)>2 else 40):
    n=rng.randint(7,9); k=rng.randint(3,5)
    edges=[]
    for _ in range(60):
        e=sum(1<<v for v in rng.sample(range(n),rng.randint(k-1,k)))
        if e in edges: continue
        if len(edges)>=14: break
        if is72_new(edges,e,n): edges.append(e)
    check(edges,n,k,'greedy%d'%trial)
