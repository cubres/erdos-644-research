#!/usr/bin/env python3
"""
NUMERICAL exploration (floating LP, scipy/HiGHS): how far does the six-plus-one Fano
construction alone force stability for type-closed families?

Continuous type-closed model, rank 1, r parts with capacities n (N = sum n).
Six-plus-one lemma: for an admissible trace s with s <= 2n/3, the box
      u(s) = min(n, 4n - 6s)      (coordinatewise)
contains no admissible trace (else 6 copies of s + one v form a bad Fano tuple), hence
      tau* <= N - sum_i min(n_i, 4n_i - 6 s_i).
Bootstrap: if tau* >= t0 then S avoids R(t0) = {s in simplex : s <= 2n/3,
sum_i min(n_i,4n_i-6s_i) > N - t0}, a convex set.  Any inverted simplex {s <= w} inside
R(t0) is then a free box, so tau* <= N - sum w.  If the largest such box has size
> N - t0, t0 is refuted.  t61(n) := the threshold (bisection).
Compare with 3/4 - 3*eta (eta = N - 7/4) and with the Fano bound 3N/7.
"""
import numpy as np, itertools, sys
from scipy.optimize import linprog

def wmax(n, t0, eps=1e-9):
    r = len(n); N = sum(n)
    # variables: w (r), m (r*r) ; sigma = sum w - 1
    nv = r + r * r
    c = np.zeros(nv); c[:r] = -1.0              # maximize sum w
    A = []; b = []
    def row():
        return np.zeros(nv)
    # sum w >= 1  -> -sum w <= -1
    a = row(); a[:r] = -1; A.append(a); b.append(-1.0)
    for j in range(r):
        for i in range(r):
            # vertex v^j = w - sigma e_j ; sigma = sum(w) - 1
            # v^j_i <= 2 n_i /3
            a = row(); a[i] += 1
            if i == j:
                a[:r] -= 1; rhs = 2 * n[i] / 3 - 1.0   # w_j - (sum w - 1) <= 2n_j/3
            else:
                rhs = 2 * n[i] / 3
            A.append(a); b.append(rhs)
            # v^j_j >= 0 : -(w_j - sum w + 1) <= 0
            if i == j:
                a = row(); a[i] -= 1; a[:r] += 1; A.append(a); b.append(1.0)
            # m_ij <= n_i
            a = row(); a[r + i * r + j] = 1; A.append(a); b.append(n[i])
            # m_ij <= 4 n_i - 6 v^j_i
            a = row(); a[r + i * r + j] = 1; a[i] += 6
            if i == j:
                a[:r] -= 6; rhs = 4 * n[i] - 6.0     # 4n_j - 6(w_j - sum w + 1)
            else:
                rhs = 4 * n[i]
            A.append(a); b.append(rhs)
        # sum_i m_ij >= N - t0 + eps
        a = row()
        for i in range(r):
            a[r + i * r + j] = -1
        A.append(a); b.append(-(N - t0 + eps))
    bounds = [(0, n[i]) for i in range(r)] + [(None, None)] * (r * r)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    if res.status != 0:
        return None
    return -res.fun

def t61(n, lo=0.0, hi=None, iters=50):
    N = sum(n)
    if hi is None:
        hi = 3 * N / 7 + 1e-9          # Fano bound always holds
    # t0 refuted iff wmax(t0) > N - t0
    def refuted(t0):
        W = wmax(n, t0)
        return W is not None and W > N - t0 + 1e-12
    if not refuted(hi):
        return hi
    a, b = lo, hi
    for _ in range(iters):
        mid = (a + b) / 2
        if refuted(mid):
            b = mid
        else:
            a = mid
    return b

if __name__ == "__main__":
    np.random.seed(1)
    print("symmetric capacities n_i = N/r:  t61 vs 3/4-3eta and the r-part formula 3(r-1)N/(7r-6)")
    for r in (2, 3, 4, 5, 6, 7, 8):
        for N in (1.75, 1.76, 1.77, 1.78, 1.79, 1.80, 1.82, 1.85):
            n = [N / r] * r
            v = t61(n)
            print(f" r={r} N={N:.2f}: t61={v:.4f}   3/4-3eta={0.75-3*(N-1.75):.4f}  "
                  f"3(r-1)N/(7r-6)={3*(r-1)*N/(7*r-6):.4f}  max(6-3N,that)={max(6-3*N,3*(r-1)*N/(7*r-6)):.4f}")
    print()
    print("random capacities (r=3,4,5): largest t61 found for each N-band (Fano regime N<1.8)")
    for r in (3, 4, 5, 6):
        best = {}
        for trial in range(1500):
            N = np.random.uniform(1.75, 1.80)
            x = np.random.dirichlet(np.ones(r)) * N
            if min(x) < 0.02:
                continue
            v = t61(list(x))
            band = round((N - 1.75) / 0.01)
            if band not in best or v > best[band][0]:
                best[band] = (v, list(np.round(x, 4)), N)
        for band in sorted(best):
            v, x, N = best[band]
            print(f" r={r} N~{1.75+0.01*band:.2f}: max t61={v:.4f} at n={x} (N={N:.4f}); 3/4-3eta={0.75-3*(N-1.75):.4f}")
