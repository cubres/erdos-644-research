"""Exact infeasibility certificates for systems  {a.z < b (strict)} u {c.z <= d}  (Motzkin transposition):
find y>=0 (strict rows), w>=0 with y^T A + w^T C = 0 and y^T b + w^T d <= 0, and (y != 0 or y^T b + w^T d < 0).
Multipliers are found with HiGHS (max t s.t. a.z + t <= b) and then recomputed EXACTLY by rational linear
algebra (sympy) on the dual support; the certificate is then checked in exact arithmetic."""
from fractions import Fraction as F
import numpy as np, sympy as sp
from scipy.optimize import linprog
def certify(rows, VARS):
    n = len(VARS); ix = {v: i for i, v in enumerate(VARS)}
    M = len(rows)
    A = np.zeros((M + 1, n + 1)); b = np.zeros(M + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, ix[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[M, n] = 1.0; b[M] = 1.0                    # t <= 1
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)]*(n + 1), method='highs')
    if res.status == 2: tstar = -np.inf
    elif res.status != 0: return None, "lp status %d" % res.status
    else: tstar = -res.fun
    if tstar > 1e-9: return False, "feasible t*=%g" % tstar
    if res.status != 0: return None, "infeasible LP (no duals)"
    duals = -res.ineqlin.marginals            # >= 0
    supp = [k for k in range(M + 1) if duals[k] > 1e-10]
    # exact: unknowns lambda_k (k in supp) >= 0 with sum_k lambda_k * [A_k | b_k] giving 0 on z-columns,
    # 1 on t column (normalisation), and value sum lambda_k b_k <= 0.  Solve the equality system exactly.
    def ex(k, j):
        if k == M: return F(1) if j == n else F(0)
        coef, rhs, st = rows[k]
        if j == n: return F(1) if st else F(0)
        return F(coef.get(VARS[j], 0))
    Mat = sp.Matrix([[sp.Rational(ex(k, j)) for k in supp] for j in range(n + 1)])
    rhsv = sp.Matrix([0]*n + [1])
    sol, params = Mat.gauss_jordan_solve(rhsv)
    if params.shape[0] > 0:
        # choose free params = float duals rationalised
        subs = {}
        for pi, prm in enumerate(params):
            subs[prm] = 0
        # try: set free params to values matching duals as best as possible
        guess = [sp.Rational(F(duals[k]).limit_denominator(10**6)) for k in supp]
        # least effort: substitute params with guess components where param index corresponds
        free_idx = [i for i in range(len(supp)) if all(sol[i].has(p) is False for p in []) ]
        sol = sol.subs({prm: guess[i] for i, prm in enumerate(params) if i < len(guess)})
    lam = [F(str(v)) for v in sol]
    if any(v < 0 for v in lam): return None, "negative exact multiplier"
    # exact check
    for j in range(n):
        if sum(l * ex(k, j) for l, k in zip(lam, supp)) != 0: return None, "stationarity fails"
    tsum = sum(l * ex(k, n) for l, k in zip(lam, supp))
    val = sum(l * (F(rows[k][1]) if k < M else F(1)) for l, k in zip(lam, supp))
    ystrict = sum(l for l, k in zip(lam, supp) if k < M and rows[k][2])
    u = sum(l for l, k in zip(lam, supp) if k == M)
    # dual feasibility: tsum == 1 ; certificate value = val - u = sum over real rows of lam*b
    realval = val - u
    ok = (tsum == 1) and (realval < 0 or (realval <= 0 and ystrict > 0))
    return (True if ok else None), "cert value %s, strict weight %s" % (realval, ystrict)
