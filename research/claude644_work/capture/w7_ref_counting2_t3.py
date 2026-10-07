#!/usr/bin/env python3
"""w7_ref_counting2_t3.py -- counting#2 referee: tau>=3 families (subfamilies of K_5^3 / K_6^4 / K_7^5-like cores
plus random extra edges reaching OUTSIDE vertices), filtered to (7,2) and tau>=3; runs T1-T5 of w7_ref_counting2_bf."""
import itertools, random, sys
from collections import Counter
import w7_ref_counting2_bf as B
seed=int(sys.argv[1]); nf=int(sys.argv[2]); rng=random.Random(seed)
st=Counter(); st['tmax']=0; tries=0
while st['fam']<nf:
    tries+=1
    n0,k=rng.choice([(5,3),(6,4)])
    core=[sum(1<<v for v in S) for S in itertools.combinations(range(n0),k)]
    H=rng.sample(core, rng.randint(6, min(len(core), 9 if k==3 else 8)))
    n=n0+rng.randint(1,3)
    for _ in range(rng.randint(1,3)):
        H.append(sum(1<<v for v in rng.sample(range(n), k)))
    H=sorted(set(H)); B.VM[0]=0
    for E in H: B.VM[0]|=E
    if B.tau(H,n)<3: continue
    before=st['fam']
    B.run_family(H,n,st)
    if st['fam']>before: print('fam',st['fam'],'|H|',len(H),dict(st),flush=True)
print('tries',tries,dict(st))
