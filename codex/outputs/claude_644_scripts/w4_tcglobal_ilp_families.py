#!/usr/bin/env python3
"""w4_tcglobal_ilp_families.py -- TC* tightness on symmetric (7,2) families via an exact ILP over cell counts
(scipy.optimize.milp / HiGHS; integer solution re-verified exactly in pure Python).
Families: (a) complete K_N^(k); (b) FKW parity family: k-subsets of an n-set S meeting a fixed k-set X oddly.
Variables: for colour c (X / Y=S\\X), location l in {E1,E2,E3,E4,W} and membership m in {0,1}^4 of (b1,b2,c1,c2),
the count z[c,l,m].  Constraints: E0 = E1u..uE4 is an edge (|E0|=k, parity), each of b1,b2,c1,c2 is an edge,
TC trace conditions (b1nE0 in E3uE4, b2nE0 in E1uE2, c1nE0 in E2uE4, c2nE0 in E1uE3).
Objective: minimize M >= |T_A|, |T_B| with T_A = E1uE4u((b1nc1)u(b2nc2)), T_B = E2uE3u((b1nc2)u(b2nc1)).
TC* (+(7,2)) predicts min M >= tau.  Usage: python3 w4_tcglobal_ilp_families.py"""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
M4 = list(itertools.product([0,1], repeat=4))
LOCS = ['E1','E2','E3','E4','W']
def solve(colors, k, parity_color=None, extra_forbid=None):
    # colors: dict name->size ; parity_color: name whose intersection with every edge must be odd
    keys = [(c,l,m) for c in colors for l in LOCS for m in M4]
    # forbid trace violations
    allowed = []
    for (c,l,m) in keys:
        b1,b2,c1,c2 = m
        ok = True
        if l in ('E1','E2') and b1: ok = False
        if l in ('E3','E4') and b2: ok = False
        if l in ('E1','E3') and c1: ok = False
        if l in ('E2','E4') and c2: ok = False
        if ok: allowed.append((c,l,m))
    idx = {key:i for i,key in enumerate(allowed)}
    nz = len(allowed)
    # extra integer vars: M, and parity helpers y0..y4 (for E0 and four edges)
    nv = nz + 1 + 5
    iM = nz; iy = nz+1
    A, lo, hi = [], [], []
    def row(): return np.zeros(nv)
    for c, sz in colors.items():
        r = row()
        for key in allowed:
            if key[0]==c: r[idx[key]] = 1
        A.append(r); lo.append(sz); hi.append(sz)
    # E0 size
    r = row()
    for key in allowed:
        if key[1] != 'W': r[idx[key]] = 1
    A.append(r); lo.append(k); hi.append(k)
    if parity_color:
        r = row()
        for key in allowed:
            if key[1] != 'W' and key[0]==parity_color: r[idx[key]] = 1
        r[iy] = -2; A.append(r); lo.append(1); hi.append(1)
    for j in range(4):
        r = row()
        for key in allowed:
            if key[2][j]: r[idx[key]] = 1
        A.append(r); lo.append(k); hi.append(k)
        if parity_color:
            r = row()
            for key in allowed:
                if key[2][j] and key[0]==parity_color: r[idx[key]] = 1
            r[iy+1+j] = -2; A.append(r); lo.append(1); hi.append(1)
    # T_A, T_B
    rA, rB = row(), row()
    for key in allowed:
        c,l,m = key; b1,b2,c1,c2 = m
        if l in ('E1','E4'): rA[idx[key]] = 1
        if l in ('E2','E3'): rB[idx[key]] = 1
        if l == 'W':
            if (b1 and c1) or (b2 and c2): rA[idx[key]] = 1
            if (b1 and c2) or (b2 and c1): rB[idx[key]] = 1
    rA[iM] = -1; rB[iM] = -1
    A += [rA, rB]; lo += [-np.inf, -np.inf]; hi += [0, 0]
    cvec = np.zeros(nv); cvec[iM] = 1
    res = milp(cvec, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(np.zeros(nv), np.full(nv, 1000)))
    if res.status != 0: return None
    x = np.round(res.x).astype(int)
    # exact re-verification of the integer solution
    sol = {key: int(x[idx[key]]) for key in allowed if x[idx[key]]}
    E0 = sum(v for (c,l,m),v in sol.items() if l!='W')
    assert E0 == k
    for j in range(4):
        assert sum(v for (c,l,m),v in sol.items() if m[j]) == k
        if parity_color: assert sum(v for (c,l,m),v in sol.items() if m[j] and c==parity_color) % 2 == 1
    TA = sum(v for (c,l,m),v in sol.items() if l in ('E1','E4') or (l=='W' and ((m[0] and m[2]) or (m[1] and m[3]))))
    TB = sum(v for (c,l,m),v in sol.items() if l in ('E2','E3') or (l=='W' and ((m[0] and m[3]) or (m[1] and m[2]))))
    return max(TA,TB), TA, TB, sol
if __name__ == '__main__':
    for (N,k) in [(6,4),(9,5),(13,8),(20,12),(27,16)]:
        t = N-k+1
        r = solve({'Z':N}, k)
        print(f"complete K_{N}^({k}): tau={t}  min max(|T_A|,|T_B|) = {r[0]}  (T_A,T_B)=({r[1]},{r[2]})")
    # FKW parity family m=3: 12-subsets of a 22-set meeting fixed 12-set X oddly; tau = 10 (note Prop 2.6: (7,2))
    for (n,k,tau) in [(22,12,10),(29,16,13)]:
        r = solve({'X':k,'Y':n-k}, k, parity_color='X')
        print(f"parity family n={n},k={k}: tau={tau}  min max(|T_A|,|T_B|) = {r[0]}  (T_A,T_B)=({r[1]},{r[2]})")
