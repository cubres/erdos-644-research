"""Fano assignment orbits through set partitions, avoiding m**7 storage.

This affects discovery only; every emitted tuple is checked by the original
exact checker. The construction enumerates set partitions up to Fano symmetry,
then injective colorings of their blocks modulo the induced stabilizer group.
"""
import itertools
import numpy as np
from heavylib import LPERMS

def normalize(t):
    labels = {}; out = []
    for x in t:
        if x not in labels: labels[x] = len(labels)
        out.append(labels[x])
    return tuple(out)

def act(p, g):
    q = [0]*7
    for i in range(7): q[g[i]] = p[i]
    return tuple(q)

def partitions(prefix=(0,)):
    if len(prefix) == 7:
        yield prefix; return
    for j in range(max(prefix)+2):
        yield from partitions(prefix+(j,))

_structure = None
_cache = {}
def structure():
    global _structure
    if _structure is not None: return _structure
    seen = set(); out = []
    for p in partitions():
        if p in seen: continue
        b = max(p)+1
        orbit = {normalize(act(p,g)) for g in LPERMS}
        seen.update(orbit)
        stabilizer = []
        for g in LPERMS:
            q = act(p,g)
            if normalize(q) == p:
                mapping = [None]*b
                for j in range(7): mapping[p[j]] = q[j]
                stabilizer.append(tuple(mapping))
        perms = []; seen_perm = set()
        for a in itertools.permutations(range(b)):
            if a in seen_perm: continue
            perms.append(a)
            seen_perm.update(tuple(a[h[j]] for j in range(b)) for h in stabilizer)
        out.append((p,b,perms))
    _structure = out
    return out

def reparr(m):
    if m not in _cache:
        out=[]
        for p,b,perms in structure():
            if b > m: continue
            for cols in itertools.combinations(range(m),b):
                for perm in perms:
                    out.append(tuple(cols[perm[p[j]]] for j in range(7)))
        _cache[m] = np.array(out,dtype=np.int64)
    return _cache[m]

if __name__ == '__main__':
    import time
    from heavylib import reparr as old
    for m in range(1,10):
        t=time.time(); a=reparr(m)
        canonical=lambda p:min(act(p,g) for g in LPERMS)
        # m<=6 compares exact orbit representatives; later counts use Burnside.
        if m<=6: assert {canonical(p) for p in a} == {canonical(p) for p in old(m)}
        assert len(a)==len(old(m))
        burnside=0
        for g in LPERMS:
            seen=set(); cycles=0
            for i in range(7):
                if i in seen: continue
                cycles+=1; j=i
                while j not in seen: seen.add(j); j=g[j]
            burnside+=m**cycles
        assert len(a)*len(LPERMS)==burnside
        print(m,len(a),round(time.time()-t,3),flush=True)
    for m in (10,11,12):
        t=time.time();a=reparr(m);print(m,len(a),round(time.time()-t,3),flush=True)
