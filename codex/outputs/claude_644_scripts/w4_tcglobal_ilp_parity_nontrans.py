#!/usr/bin/env python3
"""w4_tcglobal_ilp_parity_nontrans.py -- decisive consistency test of TC* on the FKW parity family
(k-subsets of an n-set S meeting a fixed k-set X in an odd number; tau = n-k: a set T is a transversal iff
|T| >= n-k+1, or |T| = n-k and S\\T meets X evenly).  ILP (HiGHS) over cell counts: find E0, quartering and
b1,b2,c1,c2 (all edges, TC trace conditions) with BOTH T_A and T_B NON-transversals.  TC* + (7,2) predicts
INFEASIBLE.  Also the same for complete families K_N^(k) (non-transversal iff |T| <= N-k) at and above 3k/4.
Usage: python3 w4_tcglobal_ilp_parity_nontrans.py"""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
M4 = list(itertools.product([0,1], repeat=4)); LOCS = ['E1','E2','E3','E4','W']
def build(colors, k, parity):
    allowed = []
    for c in colors:
        for l in LOCS:
            for m in M4:
                b1,b2,c1,c2 = m
                if l in ('E1','E2') and b1: continue
                if l in ('E3','E4') and b2: continue
                if l in ('E1','E3') and c1: continue
                if l in ('E2','E4') and c2: continue
                allowed.append((c,l,m))
    return allowed
def inTA(l,m): return l in ('E1','E4') or (l=='W' and ((m[0] and m[2]) or (m[1] and m[3])))
def inTB(l,m): return l in ('E2','E3') or (l=='W' and ((m[0] and m[3]) or (m[1] and m[2])))
def run(colors, k, tau, parity):
    allowed = build(colors, k, parity); idx = {a:i for i,a in enumerate(allowed)}; nz = len(allowed)
    # extra vars: yE0, y1..y4 (edge parity), for A and B: d, w, y  -> 5 + 6
    nv = nz + 11
    A, lo, hi = [], [], []
    def row(): return np.zeros(nv)
    for c, sz in colors.items():
        r = row()
        for a in allowed:
            if a[0]==c: r[idx[a]] = 1
        A.append(r); lo.append(sz); hi.append(sz)
    r = row()
    for a in allowed:
        if a[1]!='W': r[idx[a]] = 1
    A.append(r); lo.append(k); hi.append(k)
    if parity:
        r = row()
        for a in allowed:
            if a[1]!='W' and a[0]=='X': r[idx[a]] = 1
        r[nz] = -2; A.append(r); lo.append(1); hi.append(1)
    for j in range(4):
        r = row()
        for a in allowed:
            if a[2][j]: r[idx[a]] = 1
        A.append(r); lo.append(k); hi.append(k)
        if parity:
            r = row()
            for a in allowed:
                if a[2][j] and a[0]=='X': r[idx[a]] = 1
            r[nz+1+j] = -2; A.append(r); lo.append(1); hi.append(1)
    for side, f, off in (('A', inTA, nz+5), ('B', inTB, nz+8)):
        d, w, y = off, off+1, off+2
        r = row()
        for a in allowed:
            if f(a[1], a[2]): r[idx[a]] = 1
        if parity:
            # |T| <= tau-1 + d ; |X\T| = 2y + w ; w >= d ; d,w binary
            r[d] = -1; A.append(r); lo.append(-np.inf); hi.append(tau-1)
            r2 = row()
            for a in allowed:
                if a[0]=='X' and not f(a[1],a[2]): r2[idx[a]] = 1
            r2[y] = -2; r2[w] = -1; A.append(r2); lo.append(0); hi.append(0)
            r3 = row(); r3[w] = 1; r3[d] = -1; A.append(r3); lo.append(0); hi.append(np.inf)
        else:
            A.append(r); lo.append(-np.inf); hi.append(tau-1)
    ub = np.full(nv, 1000.0)
    for off in (nz+5, nz+8): ub[off] = 1; ub[off+1] = 1
    res = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(np.zeros(nv), ub))
    return res.status
if __name__ == '__main__':
    for (n,k) in [(22,12),(29,16),(36,20)]:
        st = run({'X':k,'Y':n-k}, k, n-k, True)
        print(f"parity n={n},k={k},tau={n-k}: status {st} ({'INFEASIBLE as predicted' if st==2 else 'FEASIBLE?!'})")
    for (N,k) in [(20,12),(27,16),(34,20)]:
        st = run({'Z':N}, k, N-k+1, False)
        print(f"complete K_{N}^({k}) tau={N-k+1}: status {st} ({'INFEASIBLE as predicted' if st==2 else 'FEASIBLE?!'})")
    # sanity: complete family ABOVE the threshold (not (7,2)): expect FEASIBLE (TC fires)
    for (N,k) in [(21,12),(28,16)]:
        st = run({'Z':N}, k, N-k+1, False)
        print(f"complete K_{N}^({k}) tau={N-k+1} (not (7,2)): status {st} ({'feasible: TC* fires' if st==0 else 'infeasible'})")
