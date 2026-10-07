import itertools
from threebox_fano import LPERMS
_C = {}
def reps(m):
    if m in _C: return _C[m]
    seen = set(); out = []
    for b in itertools.product(range(m), repeat=7):
        if b in seen: continue
        out.append(b)
        for lp in LPERMS:
            nb = [None]*7
            for i in range(7): nb[lp[i]] = b[i]
            seen.add(tuple(nb))
    _C[m] = out; return out
