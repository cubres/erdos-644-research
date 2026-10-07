#!/usr/bin/env python3
"""w4_tcglobal_fanodown_lp.py -- does a two-type type-closed family contain a Fano-LABELLED (downset) bad tuple?
Exploratory (scipy LP, floating point). Rows = 7 Fano lines; each row gets a type; per part, safe cells are
subsets of the 4 lines missing some point. Feasible LP in every part => continuous realization of a Fano-labelled
bad tuple (types-closed family).  Usage: python3 w4_tcglobal_fanodown_lp.py"""
import itertools
import numpy as np
from scipy.optimize import linprog
pts = range(7)
lines = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
safe = set()
for p in pts:
    miss = [i for i,l in enumerate(lines) if p not in l]
    for r in range(1,5):
        for c in itertools.combinations(miss, r):
            safe.add(frozenset(c))
safe = sorted(safe, key=lambda s: (len(s), sorted(s)))
def part_feasible(loads, cap):
    # variables m_sigma >=0; sum_{sigma ni l} m = loads[l]; sum m <= cap
    A_eq = np.array([[1.0 if l in s else 0.0 for s in safe] for l in range(7)])
    b_eq = np.array(loads, dtype=float)
    A_ub = np.ones((1, len(safe))); b_ub = np.array([cap], dtype=float)
    r = linprog(np.zeros(len(safe)), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    return r.status == 0
def fano_labelled_exists(types, caps):
    found = []
    for assign in itertools.product(range(len(types)), repeat=7):
        ok = True
        for P in range(len(caps)):
            if not part_feasible([types[assign[l]][P] for l in range(7)], caps[P]):
                ok = False; break
        if ok: found.append(assign)
    return found
if __name__ == '__main__':
    # note Lemma 7.9 family: parts X,Y,Z sizes 40,139,99; types a=(20,0,80), b=(0,80,20); tau/k -> 39/50
    types = [(20,0,80),(0,80,20)]
    caps = (40,139,99)
    f = fano_labelled_exists(types, caps)
    print("Lemma 7.9 family: Fano-labelled (downset) assignments feasible:", len(f), f[:5])
