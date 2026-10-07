"""Referee w7 core#0 BREAK-IT: ALL Lemma-Q quadruples (multisets of 4 subsets of [n] of size<=k meeting the hypotheses
for some order), up to S_n, written to a json for exhaustive CEGAR.  usage: n k t mode"""
import itertools, json, sys
sys.path.insert(0,'.')
from w7_ref_core0_brk_cegar import hyp
n,k,t=map(int,sys.argv[1:4]); mode=sys.argv[4]
sets=[frozenset(c) for r in range(1,k+1) for c in itertools.combinations(range(n),r)]
perms=list(itertools.permutations(range(n)))
seen=set(); reps=[]
for q in itertools.combinations_with_replacement(range(len(sets)),4):
    G=[sets[i] for i in q]
    if hyp(G,t,k,mode) is None: continue
    key=tuple(sorted(tuple(sorted(g)) for g in G))
    if key in seen: continue
    orb=set()
    for p in perms:
        orb.add(tuple(sorted(tuple(sorted(p[x] for x in g)) for g in G)))
    seen|=orb; reps.append([sorted(g) for g in G])
json.dump(reps,open(f'w7_ref_core0_brk_orbits_{n}_{k}_{t}_{mode}.json','w'))
print(n,k,t,mode,'orbits',len(reps))
