# recursive subdivision: each leaf piece has all vertices feasible for one template
import sys
from lib2 import *
Q = F(3,4)
BASE = [
 ([0,0,1,0], 0), ([0,0,-1,1], 0), ([0,0,0,-1], 1),
 ([1,0,-1,0], -Q), ([0,1,0,1], -1-Q), ([1,1,1,-1], -1-Q),
 ([1,0,0,-1], 0), ([0,1,1,0], -1),
]
PREF = [19,20,1,2,3,4,5,6,9,10,21,22,41,42] + [k for k in range(1,43) if k not in (19,20,1,2,3,4,5,6,9,10,21,22,41,42)]
if len(sys.argv)>1: PREF=[int(a) for a in sys.argv[1].split(',')]
def facets(k):
    # constraints of template k as cons (>=0): x - (u al + v be) >=0 ; y - (u(1-al)+v(1-be)) >= 0
    out=[]
    for u,v in FUNCS[k-1]:
        out.append(([1,0,-u,-v],0))
        out.append(([0,1,u,v],-(u+v)))
    return out
def ev(c,z): return sum(F(a)*b for a,b in zip(c[0],z))+F(c[1])
leaves=[]
def rec(cons, depth, path):
    V = vertices(cons,4)
    if not V: return True
    for k in PREF:
        if all(feasible(k-1,*v) for v in V):
            leaves.append((path,k,V)); return True
    if depth>8:
        print('DEPTH FAIL', path, V); return False
    # choose template maximizing #feasible vertices among PREF
    best = max(PREF, key=lambda k: sum(feasible(k-1,*v) for v in V))
    fc = facets(best)
    # partition: piece j = cons + {f_j<=0} + {f_i>=0 for i<j}
    ok=True
    for j,f in enumerate(fc):
        if all(ev(f,v)>=0 for v in V): continue
        neg = ([-a for a in f[0]], -f[1])
        piece = cons + [neg] + [fc[i] for i in range(j)]
        ok &= rec(piece, depth+1, path+[(best,j)])
    return ok
ok = rec(BASE,0,[])
print('OK' if ok else 'FAIL', len(leaves),'leaves')
from collections import Counter
print(Counter(k for _,k,_ in leaves))
for p,k,V in leaves: print(p,'->',k, len(V))

# verbose re-walk of the chain
print('--- detail ---')
def show(cons, depth):
    V = vertices(cons,4)
    ind='  '*depth
    print(ind, len(V),'vertices:', [tuple(str(c) for c in v) for v in V])
    for k in PREF:
        if all(feasible(k-1,*v) for v in V):
            print(ind,'LEAF template',k); return
