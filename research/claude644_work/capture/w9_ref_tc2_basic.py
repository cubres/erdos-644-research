# w9_ref_tc2_basic.py -- referee [typeclosed#2]: (1) Fano plane sanity + every 2-colouring of the 7 LINES has a
# monochromatic concurrent triple; (2) note 7.79 family: exact tau*, super-heavy classes, e_i, balanced check,
# excess bound (c) for each i, E+ (tau*(C^(i)) <= 3/4).
from fractions import Fraction as F
from itertools import combinations, product
from w9_ref_tc2_lib import *
# (1)
for a, b in combinations(range(7), 2):
    assert sum(1 for L in LINES if a in L and b in L) == 1
for l1, l2 in combinations(range(7), 2):
    assert len(set(LINES[l1]) & set(LINES[l2])) == 1
bad = 0
for col in product([0, 1], repeat=7):
    mono = any(col[l1] == col[l2] == col[l3] and set(LINES[l1]) & set(LINES[l2]) & set(LINES[l3])
               for l1, l2, l3 in combinations(range(7), 3))
    if not mono: bad += 1
print("2-colourings of lines with no monochromatic concurrent triple:", bad)
assert bad == 0
# (2) note 7.79
T = [(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
C = [tuple(F(v, 80) for v in t) for t in T]
x = (F(513, 640),) * 3
ts = tau_star(C, x)
print("7.79 tau* =", ts, "(expect 483/640)"); assert ts == F(483, 640)
sig = []; e = []
for i in range(3):
    S = [c for c in C if c[i] > F(2, 3) * x[i]]
    sig.append(min(c[i] for c in S)); e.append(x[i] - sig[-1])
cls = [[i for i in range(3) if c[i] > F(2, 3) * x[i]] for c in C]
print("super-heavy parts per type:", cls)
print("e =", e, " e/(3/4 units):", [float(v) for v in e])
print("pairwise sums:", [e[i] + e[j] for i, j in combinations(range(3), 2)], " total", sum(e))
for i in range(3):
    Ci = [c for c in C if c[i] <= F(2, 3) * x[i]]
    tci = tau_star(Ci, x)
    print(f"i={i}: tau*(C^(i))={tci} <=3/4? {tci <= F(3,4)};  excess bound tau* <= tau*(C^(i))+e_i: {ts <= tci + e[i]}")
