import itertools, sys
sys.path.insert(0,'heavy')
from heavylib import LINES, PENCIL
def pat(cols,q): return ''.join(sorted(cols[l] for l in PENCIL[q]))
res={}
for cols in itertools.product('ABC',repeat=7):
    pats=[pat(cols,q) for q in range(7)]
    if any(p in ('AAA','BBB','CCC') for p in pats): continue
    key=tuple(sorted(set(pats)))
    sizes=tuple(cols.count(c) for c in 'ABC')
    from collections import Counter
    res.setdefault(key,set()).add((sizes,tuple(sorted(Counter(pats).items()))))
for k,v in sorted(res.items()):
    print(k, v)
