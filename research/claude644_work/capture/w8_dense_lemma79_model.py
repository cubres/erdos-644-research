#!/usr/bin/env python3
"""w8_dense_lemma79_model.py -- the note's Lemma 7.9 family (parts X,Y,Z = 40,139,99; types a=(20,0,80),
b=(0,80,20); rank 100; intersecting; tau/k -> 39/50; NO Fano-complement tuple) seen through the ANCHORED
profile model with E0 = a type-a edge as ONE homogeneous part:  parts (E0, X'=X\E0, Y, Z'=Z\E0) = (100,20,139,19).
A random a-subset of E0 meets X in a/5 and Z in 4a/5 (continuum), so the robust types are two segments
   A(a) = (a, 20-a/5, 0, 80-4a/5),  a in [76.25,100]   (rank 100; A(100) = anchor)
   B(a) = (a, 0, 80, 20-4a/5),      a in [1.25, 25]    (rank 100 + a/5  <-- rank loss from homogenising E0)
Checks: (1) tau*(types of rank <= r) for r in [100,105] (MILP, floating) vs 3r/4;
        (2) no anchored Fano configuration: LP over the 2^6 segment patterns (floating; consistent with the
            note's exact statement that the family has no Fano-complement tuple)."""
import numpy as np
from scipy.optimize import linprog
from w5_dense_milp_lib import tau_star_milp
caps = [100, 20, 139, 19]
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PENC = [[j for j,l in enumerate(LINES) if q in l] for q in range(7)]
def A(a): return [a, 20 - a/5, 0, 80 - 4*a/5]
def B(a): return [a, 0, 80, 20 - 4*a/5]
for rho in [0, 1, 2, 3, 4, 4.5, 4.9, 5]:
    r = 100 + rho
    G = [A(a) for a in np.arange(76.25, 100.001, 0.25)] + [B(a) for a in np.arange(1.25, 25.001, 0.25) if 100 + a/5 <= r + 1e-9]
    ts = tau_star_milp(G, caps)
    print(f'r={r:6.2f}  tau*={ts:7.3f}  3r/4={0.75*r:7.3f}  ratio={ts/r:.4f}')
# (2) anchored config LP per pattern
feas = 0
for mask in range(64):
    # variables: a_1..a_6 ; type on line j = A or B
    lo = []; hi = []
    for j in range(6):
        if mask >> j & 1: lo.append(76.25); hi.append(100)
        else: lo.append(1.25); hi.append(25)
    Aub = []; bub = []
    def coef(j, i):   # coordinate i of type on line j+1 as (slope, const) in a_j
        if mask >> j & 1: return [(1,0), (-0.2,20), (0,0), (-0.8,80)][i]
        return [(1,0), (0,0), (0,80), (-0.8,20)][i]
    for i in range(4):
        anchor_i = 100 if i == 0 else 0
        rows = [[0]*6 for _ in range(7)]; const = [0]*7
        const[0] = anchor_i
        for j in range(6):
            s, c = coef(j, i); rows[j+1][j] = s; const[j+1] = c
        # each line load <= cap
        for l in range(1, 7):
            Aub.append(rows[l]); bub.append(caps[i] - const[l])
        for pen in PENC:
            Aub.append([sum(rows[l][v] for l in pen) for v in range(6)]); bub.append(2*caps[i] - sum(const[l] for l in pen))
        Aub.append([sum(rows[l][v] for l in range(7)) for v in range(6)]); bub.append(4*caps[i] - sum(const))
    res = linprog(np.zeros(6), A_ub=np.array(Aub), b_ub=np.array(bub), bounds=list(zip(lo, hi)), method='highs')
    if res.status == 0: feas += 1; print('FEASIBLE pattern', bin(mask), res.x)
print('anchored-config patterns feasible:', feas, 'of 64')
