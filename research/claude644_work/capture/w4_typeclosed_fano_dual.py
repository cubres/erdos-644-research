"""Exact vertices of the Fano dual polytope P_F = {w in R^7_{>=0} (lines): sum_{l not through q} w_l <= 1 for all points q}.
Mixed-Fano (lazy) feasibility in a part: max_{w vertex} w.loads <= x_i."""
import itertools
from fractions import Fraction as F
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
# constraints: rows: for q: sum_{l: q not in L[l]} w_l <= 1 ; and -w_l <= 0
cons=[]
for q in range(7): cons.append(([1 if q not in L[l] else 0 for l in range(7)],1))
for l in range(7): cons.append(([-1 if m==l else 0 for m in range(7)],0))
def solve(rows):
    # gaussian elimination exact 7x7
    M=[[F(v) for v in r[0]]+[F(r[1])] for r in rows]
    n=7
    for c in range(n):
        piv=next((r for r in range(c,n) if M[r][c]!=0),None)
        if piv is None: return None
        M[c],M[piv]=M[piv],M[c]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]/M[c][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return [M[i][n]/M[i][i] for i in range(n)]
verts=set()
for rows in itertools.combinations(cons,7):
    w=solve(rows)
    if w is None: continue
    if all(sum(a*b for a,b in zip(r,w))<=rhs for r,rhs in cons): verts.add(tuple(w))
print(len(verts))
from collections import Counter
for w in sorted(verts, key=lambda w:(sum(1 for v in w if v>0), w)):
    supp=[l for l in range(7) if w[l]>0]
    conc = len(supp)==3 and len(frozenset.intersection(*[L[l] for l in supp]))==1
    print([str(v) for v in w], 'support',supp,'concurrent' if conc else '')
