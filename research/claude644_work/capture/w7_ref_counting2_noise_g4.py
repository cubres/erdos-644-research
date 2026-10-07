#!/usr/bin/env python3
"""w7_ref_counting2_noise_g4.py -- print one lex minimiser of K_n^k0 + f private noise, its core missing-set
types, G4 (missing pairs of core degree-4 vertices), and check D_noise = f*sum_j(deg_G4(j)-1) when no degree 5."""
import itertools, sys
sys.path.insert(0,'.')
from w7_ref_counting2_brk import pairs, cov_masks
from collections import Counter
for (n,k0,f) in [(6,4,1),(6,4,2),(5,3,1),(5,3,2)]:
    core=list(itertools.combinations(range(n),k0)); H=[]; nxt=n
    for S in core:
        E=sum(1<<v for v in S)
        for _ in range(f): E|=1<<nxt; nxt+=1
        H.append(E)
    verts=list(range(nxt)); best=None; mins=[]
    for F in itertools.combinations_with_replacement(range(len(H)),6):
        R=[H[j] for j in F]; Pi=pairs(R,verts); c=cov_masks(R,verts)
        key=(len(verts),len(Pi)) if any(c[v]==63 for v in verts) else (len(set(x for pr in Pi for x in pr)),len(Pi))
        if best is None or key<best: best=key; mins=[(R,Pi)]
        elif key==best: mins.append((R,Pi))
    out=Counter()
    for R,Pi in mins:
        Pis=set(Pi); P=set(x for pr in Pi for x in pr)
        W=[set(x for pr in pairs(R[:i]+R[i+1:],verts) if pr not in Pis for x in pr) for i in range(6)]
        d={v:sum((F>>v)&1 for F in R) for v in verts}
        miss={v:tuple(i for i in range(6) if not (R[i]>>v)&1) for v in range(n)}
        G4=set(miss[v] for v in range(n) if d[v]==4)
        deg5=any(d[v]==5 for v in range(n))
        Dn=sum(sum(v in w for w in W)+2*(v in P)-d[v] for v in verts if v>=n)
        degG4=[sum(j in e for e in G4) for j in range(6)]
        pred=f*sum(x-1 for x in degG4)
        out[(tuple(sorted(Counter(miss.values()).items())),len(G4),deg5,Dn,pred)]+=1
    print(f'K_{n}^{k0}+noise{f}: key {best}')
    for kk,vv in out.items(): print('   types',kk[0],'|G4|',kk[1],'deg5',kk[2],'Dnoise',kk[3],'pred f*sum(degG4-1)',kk[4],'count',vv)
