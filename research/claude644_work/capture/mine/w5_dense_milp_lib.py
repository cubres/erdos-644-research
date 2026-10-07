#!/usr/bin/env python3
"""w5_dense_milp_lib.py -- MILP (scipy/HiGHS, floating) helpers for type-closed models with many types.
 anchor_milp(types, caps, a0): is there an assignment of types to the six non-anchor Fano lines satisfying note
   Lemma 7.63 (rows <= caps, pencil sums <= 2caps, total <= 4caps) with the anchor type a0 on line L?
   Returns the assignment (list of 6 type indices) or None.  Any returned assignment is re-verified EXACTLY
   with integer arithmetic (verify_assignment).  Infeasibility is floating-point (NUMERICAL).
 tau_star_milp(types, caps): continuous tau* = N - sup{sum u : u free}, via a disjunctive MILP (floating).
 intersecting(types, caps): exact."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PENC = [[j for j,l in enumerate(LINES) if q in l] for q in range(7)]
def verify_assignment(types, caps, rows):
    p = len(caps)
    for i in range(p):
        loads = [types[r][i] for r in rows]
        if max(loads) > caps[i] or sum(loads) > 4*caps[i]: return False
        for pen in PENC:
            if sum(loads[j] for j in pen) > 2*caps[i]: return False
    return True
def anchor_milp(types, caps, a0):
    T = np.array(types, dtype=float); p = len(caps); nt = len(types); X = np.array(caps, dtype=float)
    nv = 6*nt  # x[l,g], l = line 1..6
    A = []; lo = []; hi = []
    for l in range(6):
        row = np.zeros(nv); row[l*nt:(l+1)*nt] = 1; A.append(row); lo.append(1); hi.append(1)
    for i in range(p):
        # rows <= cap: enforce by forbidding types with g_i > cap (none should exist)
        for pen in PENC:
            row = np.zeros(nv); const = 0.0
            for j in pen:
                if j == 0: const += T[a0, i]
                else: row[(j-1)*nt:j*nt] += T[:, i]
            A.append(row); lo.append(-np.inf); hi.append(2*X[i] - const)
        row = np.zeros(nv)
        for j in range(1, 7): row[(j-1)*nt:j*nt] += T[:, i]
        A.append(row); lo.append(-np.inf); hi.append(4*X[i] - T[a0, i])
    res = milp(c=np.zeros(nv), constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(0, 1))
    if res.status != 0 or res.x is None: return None
    xs = np.round(res.x).astype(int).reshape(6, nt)
    rows = [a0] + [int(np.argmax(xs[l])) for l in range(6)]
    if not verify_assignment(types, caps, rows): raise RuntimeError("MILP solution failed exact verification")
    return rows[1:]
def tau_star_milp(types, caps):
    T = np.array(types, dtype=float); p = len(caps); nt = len(types); X = np.array(caps, dtype=float)
    # variables: u_i (p), y[g,i] binary (nt*p): y=1 means u_i <= g_i (type g killed in part i)
    nv = p + nt*p; c = np.zeros(nv); c[:p] = -1
    A = []; lo = []; hi = []
    M = X.max() + 1
    for g in range(nt):
        row = np.zeros(nv)
        for i in range(p):
            if T[g, i] > 0: row[p + g*p + i] = 1
        A.append(row); lo.append(1); hi.append(np.inf)
        for i in range(p):
            r2 = np.zeros(nv); r2[i] = 1; r2[p + g*p + i] = M
            A.append(r2); lo.append(-np.inf); hi.append(T[g, i] + M)
    integ = np.concatenate([np.zeros(p), np.ones(nt*p)])
    ub = np.concatenate([X, np.ones(nt*p)])
    for g in range(nt):
        for i in range(p):
            if T[g, i] == 0: ub[p + g*p + i] = 0
    res = milp(c=c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=integ, bounds=Bounds(0, ub))
    if res.status != 0: return None
    return X.sum() + res.fun  # N - sup
def intersecting(types, caps):
    p = len(caps)
    return all(any(types[a][i] + types[b][i] > caps[i] for i in range(p)) for a in range(len(types)) for b in range(a, len(types)))
if __name__ == '__main__':
    from w5_dense_anchor_climb import anchorable, tau_star
    import random
    random.seed(3); bad = 0
    for _ in range(200):
        caps = [random.randint(5, 20) for _ in range(3)]
        types = [[random.randint(0, c) for c in caps] for _ in range(random.randint(2, 4))]
        if any(sum(t) == 0 for t in types): continue
        a0 = 0
        e1 = anchorable(types, caps, a0) is None; e2 = anchor_milp(types, caps, a0) is None
        t1 = tau_star(types, caps); t2 = tau_star_milp(types, caps)
        if e1 != e2 or abs(t1 - t2) > 1e-6: bad += 1; print("mismatch", caps, types, e1, e2, t1, t2)
    print("crosscheck mismatches:", bad)
