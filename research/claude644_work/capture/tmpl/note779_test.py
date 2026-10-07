# Test the template menu on note Prop 7.79's nine-type three-part family (exact rationals).
import itertools
from fractions import Fraction as F
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
raw = [(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
T = [tuple(F(v, 80) for v in t) for t in raw]
x = [F(513, 640)] * 3
print('heavy parts per type:', [[i for i in range(3) if 7 * t[i] > 4 * x[i]] for t in T])
def fano_ok(col):
    for i in range(3):
        z = [T[col[r]][i] for r in range(7)]
        if max(z) > x[i] or sum(z) > 4 * x[i] or any(z[a] + z[b] + z[c] > 2 * x[i] for a, b, c in LINES): return False
    return True
TF = [(1, F(1,2), F(1,4)), (1, 0, F(1,2)), (0, 1, F(1,2)), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] for i in range(3) for f in TF)
Tw = [tr for tr in itertools.permutations(range(9), 3) if T_ok(*[T[k] for k in tr])]
print('T(A,B,C) triples working:', len(Tw), Tw[:10])
# all Fano colourings with <= 3 distinct types
Ls = [frozenset(L) for L in LINES]
auts = [q for q in itertools.permutations(range(7)) if all(frozenset(q[j] for j in L) in Ls for L in Ls)]
cnt = {}
for types in itertools.combinations(range(9), 3):
    for col in itertools.product(types, repeat=7):
        if fano_ok(col):
            k = len(set(col)); cnt[k] = cnt.get(k, 0) + 1
            if k <= 3 and cnt[k] <= 3: print('Fano with', k, 'types:', col)
print('fano colourings (<=3 types) found by #types:', cnt)
print('note witness (4,2,1,4,8,8,1):', fano_ok((4,2,1,4,8,8,1)))
