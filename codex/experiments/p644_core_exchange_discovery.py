"""Bounded finite obstruction search for minimum-cover extension."""
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

N=8
ALL=(1<<N)-1
PAIRS=[sum(1<<x for x in c) for c in itertools.combinations(range(N),2)]
TRIPLES=[sum(1<<x for x in c) for c in itertools.combinations(range(N),3)]

def cover_number(blocks):
    A=np.array([[int(p&b==p) for b in blocks] for p in PAIRS], dtype=float)
    r=milp(np.ones(len(blocks)), integrality=np.ones(len(blocks)),
           bounds=Bounds(np.zeros(len(blocks)),np.ones(len(blocks))),
           constraints=LinearConstraint(A,np.ones(len(PAIRS)),np.full(len(PAIRS),np.inf)),
           options={'time_limit':30})
    if r.status != 0: raise RuntimeError(str(r))
    return round(r.fun)

def maximal(blocks):
    return sorted(b for b in set(blocks) if not any(b!=c and b&c==b for c in blocks))

def tau_covers(edges,U):
    pts=[x for x in range(N) if U>>x&1]
    for q in range(len(pts)+1):
        covers=[sum(1<<x for x in c) for c in itertools.combinations(pts,q)
                if all(sum(1<<x for x in c)&e for e in edges)]
        if covers:return q,covers

blocks=TRIPLES[:]
while True:
    changed=False
    for b in blocks:
        for x in range(N):
            if b>>x&1: continue
            nb=b|(1<<x)
            trial=maximal([c for c in blocks if c!=b]+[nb])
            if cover_number(trial)>=8:
                blocks=trial
                changed=True
                print('enlarge',b,nb,len(blocks),flush=True)
                break
        if changed:break
    if not changed:break

# Choose an inclusion-minimal covering of every triple.
while True:
    changed=False
    for b in blocks:
        trial=[c for c in blocks if c!=b]
        if all(any(a&c==a for c in trial) for a in TRIPLES):
            blocks=trial
            changed=True
            break
    if not changed:break

edges=[ALL^b for b in blocks]
t,global_covers=tau_covers(edges,ALL)
failures=[]
for U in range(1,ALL):
    core=[e for e in edges if e&U==e]
    if not core:continue
    q,covers=tau_covers(core,U)
    if q>=t:continue
    for C in covers:
        if not any(C&T==C for T in global_covers):
            failures.append({'U':U,'q':q,'C':C,'core':core})
result={'n':N,'blocks':blocks,'edges':edges,'tau':t,'global_covers':global_covers,
        'pair_cover_number':cover_number(blocks),'extension_failures':failures}
path=Path('outputs/agent_core_exchange_lifting_discovery.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
