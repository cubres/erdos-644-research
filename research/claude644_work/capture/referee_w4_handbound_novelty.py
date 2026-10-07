# Referee: are the S1/S2 label templates already among the note's static templates?
import json, itertools, glob, os
def canon(t):
    best=None
    for perm in itertools.permutations(range(4)):
        def pm(m): return sum(1<<perm[i] for i in range(4) if m>>i&1)
        for sp in itertools.permutations(range(3)):
            c=tuple(tuple(sorted(pm(m) for m in t[sp[i]])) for i in range(3))
            if best is None or c<best: best=c
    return best
S1=[[9,14],[5,14],[3,14]]
S2=[[3,9],[14],[10]]
c1,c2=canon(S1),canon(S2)
found={}
root='/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/'
nfiles=0; alltemps=set()
def walk(o,f):
    if isinstance(o,dict):
        for k,v in o.items():
            if 'template' in k.lower() and isinstance(v,list):
                for t in v:
                    try:
                        if isinstance(t,dict): t=t.get('labels') or t.get('template') or t
                        if isinstance(t,list) and len(t)==3 and all(isinstance(a,list) for a in t):
                            alltemps.add(canon(t)); 
                            if canon(t)==c1: found.setdefault('S1',set()).add(f)
                            if canon(t)==c2: found.setdefault('S2',set()).add(f)
                    except Exception: pass
            walk(v,f)
    elif isinstance(o,list):
        for v in o: walk(v,f)
for f in glob.glob(root+'**/*.json',recursive=True):
    if os.path.getsize(f)>50_000_000: continue
    try: d=json.load(open(f))
    except Exception: continue
    nfiles+=1; walk(d,f)
print('files',nfiles,'distinct canonical templates',len(alltemps))
print('S1 canon',c1,'S2 canon',c2)
for k,v in found.items(): print(k,'FOUND in',len(v),'files e.g.',sorted(v)[:3])
print(sorted(alltemps))
for k,v in found.items():
    print(k, [os.path.basename(f) for f in sorted(v) if 'certificates_31_36' in f or 'erdos644_astra_checkpoint/logs' in f][:40])
