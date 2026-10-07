#!/usr/bin/env python3
"""w9_ref_dense1_boundary.py -- referee w9, claim dense#1.  Boundary instances of the type-closed special case:
type-closed intersecting families (E0 smallest) with tau >= floor(3k/4)+12 for which the Corollary-Q proof chain does
NOT fire.  For each, search an INTEGER Fano-labelled bad 7-tuple directly (MILP over integer class sizes per part and a
choice of admissible type per line; no anchoring), then verify the tuple exactly.  If found, the family is not (7,2)
(so it is no counterexample to the stated 'floor(3k/4)+12').
Usage: python3 w9_ref_dense1_boundary.py SEED NINST"""
import sys, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import w9_ref_dense1_e2e as E

LINES = E.LINES

def minimal(types):
    out = []
    for t in sorted(set(types)):
        if not any(u[0] <= t[0] and u[1] <= t[1] for u in out): out.append(t)
    return out

def fano_milp(types, n):
    M = minimal(types); m = len(M)
    # vars: c[i][p] (14 ints), z[j][t] (7*m binaries)
    nv = 14 + 7 * m
    rows, lo, hi = [], [], []
    for i in range(2):
        r = np.zeros(nv); r[7 * i:7 * i + 7] = 1; rows.append(r); lo.append(n[i]); hi.append(n[i])
    for j in range(7):
        r = np.zeros(nv); r[14 + j * m:14 + (j + 1) * m] = 1; rows.append(r); lo.append(1); hi.append(1)
        for i in range(2):
            r = np.zeros(nv)
            for p in range(7):
                if p not in LINES[j]: r[7 * i + p] = 1
            for t in range(m): r[14 + j * m + t] = -M[t][i]
            rows.append(r); lo.append(0); hi.append(np.inf)
    ub = np.array([n[0]] * 7 + [n[1]] * 7 + [1] * (7 * m), dtype=float)
    res = milp(np.zeros(nv), constraints=LinearConstraint(np.array(rows), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(np.zeros(nv), ub), options={'time_limit': 60})
    if res.x is None: return None
    x = np.round(res.x).astype(int)
    c = [list(x[0:7]), list(x[7:14])]
    ch = [M[int(np.argmax(x[14 + j * m:14 + (j + 1) * m]))] for j in range(7)]
    # exact verification
    for j in range(7):
        for i in range(2):
            assert sum(c[i][p] for p in range(7) if p not in LINES[j]) >= ch[j][i]
        assert ch[j] in types
    assert sum(c[0]) == n[0] and sum(c[1]) == n[1]
    return c, ch

def main(seed, ninst):
    rng = random.Random(seed)
    found = nob = 0
    for it in range(ninst):
        k, e, x, S = E.gen(rng)
        n = (e, x); N = e + x
        types = S + [(e, 0)]
        tau = N - E.alpha_of(types, n)
        if 4 * tau < 3 * k + 48: continue          # tau < 3k/4 + 12
        st = dict(inst=0, lowfail=0, big=0, fired=0, tmplfail=0, critfail=0, roundfail=0, bffail=0,
                  mustfire=0, mustfire_fail=0, case1=0, case2=0, maxgap_nofire=-99)
        E.check(k, e, x, S, st)
        if st['fired']: continue
        res = fano_milp(types, n)
        tag = 'k%%4=%d tau-floor(3k/4)=%d' % (k % 4, tau - (3 * k) // 4)
        if res is None:
            nob += 1; print('NO FANO TUPLE FOUND', k, e, x, len(S), tag)
        else:
            found += 1; print('bad Fano tuple', k, e, x, len(S), tag, res[0], res[1])
    print('boundary instances: bad tuple found', found, ' not found', nob)

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
