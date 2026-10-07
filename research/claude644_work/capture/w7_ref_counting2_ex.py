#!/usr/bin/env python3
"""w7_ref_counting2_ex.py -- referee w7 counting#2: structured families.
(a) complete K_n^k (n<=7k/4-ish) and (b) complete core K_n^{k0} with f PRIVATE noise points per edge
('complete core plus private noise').  For every lex minimiser: union size, D, degree-hypothesis status,
the union bound min_i(|U|-|F_i|+2) vs 7.92's (6k+D+sum delta)/8, and T1-T5 of w7_ref_counting2_bf."""
import itertools, sys
from collections import Counter
import w7_ref_counting2_bf as B

def run(H, n, label):
    H = sorted(set(H)); k = max(B.pc(E) for E in H)
    B.VM[0] = 0
    for E in H: B.VM[0] |= E
    best=None; mins=[]
    for F in itertools.combinations_with_replacement(range(len(H)), 6):
        R=[H[j] for j in F]; Pi=B.pairs_of(R,n)
        assert Pi
        P=set(x for pr in Pi for x in pr); key=(len(P),len(Pi))
        if best is None or key<best: best=key; mins=[(R,Pi)]
        elif key==best: mins.append((R,Pi))
    t=B.tau(H,n) if n<=12 else None
    st=Counter(); prof=Counter()
    for (R,Pi) in mins:
        D=B.analyse(H,n,R,Pi,t,k,st)
        U=0
        for F in R: U|=F
        ub=min(B.pc(U)-B.pc(F)+2 for F in R)
        prof[(D,B.pc(U),ub,len(set(R)))]+=1
    print(label,'k',k,'t',t,'key',best,'#min',len(mins),'profile (D,|U|,unionbound,#distinct rows):count',dict(prof),dict(st))

if __name__=='__main__':
    # complete families
    for (n,k) in [(5,3),(6,4),(7,4),(8,5)]:
        H=[sum(1<<v for v in S) for S in itertools.combinations(range(n),k)]
        run(H,n,f'K_{n}^{k}')
    # K_6^4 core + f private noise per edge (15 edges)
    for f in (1,):
        n0,k0=6,4
        core=list(itertools.combinations(range(n0),k0)); H=[]; nxt=n0
        for S in core:
            E=sum(1<<v for v in S)
            for _ in range(f): E|=1<<nxt; nxt+=1
            H.append(E)
        run(H,nxt,f'K_6^4+noise{f}')
    # K_5^3 core + f noise
    for f in (1,2):
        n0,k0=5,3
        core=list(itertools.combinations(range(n0),k0)); H=[]; nxt=n0
        for S in core:
            E=sum(1<<v for v in S)
            for _ in range(f): E|=1<<nxt; nxt+=1
            H.append(E)
        run(H,nxt,f'K_5^3+noise{f}')
