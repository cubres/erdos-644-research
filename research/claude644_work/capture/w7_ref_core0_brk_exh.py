"""Referee w7 core#0 BREAK-IT: exhaustive CEGAR over all orbit representatives of Lemma-Q quadruples
(from w7_ref_core0_brk_orbits.py).  For each: SAT over all rank<=k families on [n] with tau>=t containing G1..G4,
(7,2) added lazily with exact set-cover MILP. UNSAT for all => exact certificate of Lemma Q (resp. of the relaxed
hypothesis) for this (n,k,t).  usage: n k t mode"""
import itertools, json, sys
sys.path.insert(0,'.')
from w7_ref_core0_brk_cegar import bad_subfamily
from pysat.solvers import Cadical153
n,k,t=map(int,sys.argv[1:4]); mode=sys.argv[4]
reps=json.load(open(f'w7_ref_core0_brk_orbits_{n}_{k}_{t}_{mode}.json'))
sets=[frozenset(c) for r in range(1,k+1) for c in itertools.combinations(range(n),r)]
idx={S:i+1 for i,S in enumerate(sets)}
unsat=0; cex=[]; iters=0
for G in reps:
    G=[frozenset(g) for g in G]
    s=Cadical153()
    for g in G: s.add_clause([idx[g]])
    for B in itertools.combinations(range(n),t-1):
        Bs=set(B); s.add_clause([idx[S] for S in sets if not (S&Bs)])
    while True:
        iters+=1
        if not s.solve(): unsat+=1; break
        m=s.get_model(); H=[S for S in sets if m[idx[S]-1]>0]
        bad=bad_subfamily(H,n)
        if bad is None:
            cex.append(([sorted(g) for g in G],[sorted(E) for E in H])); break
        s.add_clause([-idx[H[j]] for j in bad])
    s.delete()
print(f'EXH n={n} k={k} t={t} mode={mode}: orbits {len(reps)}, UNSAT {unsat}, counterexamples {len(cex)}, cegar iters {iters}')
for c in cex[:3]: print('CEX G=',c[0],'\n   H=',c[1])
