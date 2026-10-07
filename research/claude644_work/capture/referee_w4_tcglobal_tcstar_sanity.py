# Non-vacuity: drop the b1nb2nE0 = empty hypothesis, or put g avoiding only part of T_A; failures must appear.
import random
def has2(sets, V):
    for x in V:
        rest=[S for S in sets if x not in S]
        if not rest: return True
        if set.intersection(*map(set,rest)): return True
    return False
random.seed(7); fa=fb=ta=tb=0
for _ in range(100000):
    n=random.randint(5,10); V=list(range(n)); p=0.45
    rs=lambda: frozenset(v for v in V if random.random()<p)
    E0,b1,b2,c1,c2=rs(),rs(),rs(),rs(),rs()
    if not all([E0,b1,b2,c1,c2]) or c1&c2&E0: continue
    DA=set(E0&((b1&c1)|(b2&c2))); DB=set(E0-DA)
    TA=DA|(b1&c1)|(b2&c2); TB=DB|(b1&c2)|(b2&c1)
    ra=[v for v in V if v not in TA]; rb=[v for v in V if v not in TB]
    if not ra or not rb: continue
    g=frozenset(ra); h=frozenset(rb)
    if b1&b2&E0:  # hypothesis dropped
        ta+=1; fa+=has2([E0,b1,b2,c1,c2,g,h],V)
    else:
        # weaken: g avoids only D_A u (b1nc1) (not b2nc2)
        TA2=DA|(b1&c1); ra2=[v for v in V if v not in TA2]
        if not ra2: continue
        tb+=1; fb+=has2([E0,b1,b2,c1,c2,frozenset(ra2),h],V)
print("hyp dropped: tested",ta,"2-pierceable",fa)
print("T_A weakened: tested",tb,"2-pierceable",fb)
