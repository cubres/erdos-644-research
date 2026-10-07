"""Exact rational LP-duality certificates.
Region: ineqs (dict,rhs): a.z <= rhs ;  eqs (dict,rhs): a.z == rhs.
Certificate for  max d.z <= h : y (nonneg, per ineq index) and ye (free, per eq index) with
      sum_r y_r a_r + sum_s ye_s a_s == d   and   sum y_r rhs_r + sum ye_s rhs_s <= h.
Certificate for emptiness: same with d == 0 and value < 0."""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
def tomat(cons, n):
    A = np.zeros((len(cons), n)); b = np.zeros(len(cons))
    for r, (d, rhs) in enumerate(cons):
        for k, v in d.items(): A[r, int(k)] = float(v)
        b[r] = float(rhs)
    return A, b
def lin_combo(cert, cons, eqs):
    y, ye = cert
    tot = {}; val = F(0)
    for r, c in y.items():
        if c < 0: return None, None
        d, rhs = cons[r]
        for k, v in d.items(): tot[k] = tot.get(k, 0) + c*v
        val += c*rhs
    for r, c in ye.items():
        d, rhs = eqs[r]
        for k, v in d.items(): tot[k] = tot.get(k, 0) + c*v
        val += c*rhs
    return {k: v for k, v in tot.items() if v != 0}, val
def check_max(cert, cons, eqs, d, h):
    tot, val = lin_combo(cert, cons, eqs)
    if tot is None: return False
    dd = {k: v for k, v in d.items() if v != 0}
    return tot == dd and val <= h
def check_empty(cert, cons, eqs):
    tot, val = lin_combo(cert, cons, eqs)
    return tot is not None and tot == {} and val < 0
# ---------- exact simplex (Bland) for: min c.v  s.t.  M v == r, v >= 0 ----------
def simplex_eq(c, M, r):
    m = len(M); n = len(c)
    # phase 1 with artificials
    M = [row[:] for row in M]; r = r[:]
    for i in range(m):
        if r[i] < 0: M[i] = [-v for v in M[i]]; r[i] = -r[i]
    tab = [M[i] + [F(1) if j == i else F(0) for j in range(m)] + [r[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    N = n + m
    def pivot(pr, pc):
        pv = tab[pr][pc]; tab[pr] = [v / pv for v in tab[pr]]
        for i in range(m):
            if i != pr and tab[i][pc] != 0:
                f = tab[i][pc]; tab[i] = [a - f*b for a, b in zip(tab[i], tab[pr])]
        basis[pr] = pc
    def run(cost, allowed):
        while True:
            # reduced costs
            cb = [cost[b] for b in basis]
            best = None
            for j in range(N):
                if not allowed[j] or j in basis: continue
                rc = cost[j] - sum(cb[i]*tab[i][j] for i in range(m))
                if rc < 0: best = j; break
            if best is None: return 'opt'
            pr = None; bestratio = None
            for i in range(m):
                if tab[i][best] > 0:
                    ratio = tab[i][-1] / tab[i][best]
                    if bestratio is None or ratio < bestratio or (ratio == bestratio and basis[i] < basis[pr]):
                        bestratio = ratio; pr = i
            if pr is None: return 'unb'
            pivot(pr, best)
    cost1 = [F(0)]*n + [F(1)]*m
    run(cost1, [True]*N)
    if sum(tab[i][-1] for i in range(m) if basis[i] >= n) != 0: return 'inf', None, None
    # drive artificials out
    for i in range(m):
        if basis[i] >= n:
            for j in range(n):
                if tab[i][j] != 0: pivot(i, j); break
    cost2 = list(c) + [F(0)]*m
    st = run(cost2, [True]*n + [False]*m)
    if st == 'unb': return 'unb', None, None
    v = [F(0)]*n
    for i in range(m):
        if basis[i] < n: v[basis[i]] = tab[i][-1]
    return 'opt', v, sum(ci*vi for ci, vi in zip(c, v))
def dual_small(cons, eqs, S, d, n):
    """min sum y_r rhs_r + sum ye rhs  s.t. sum y a_r + sum ye a_s == d, y>=0 over support S (ineq idx), ye free."""
    E = list(range(len(eqs)))
    # variables: y_r (r in S), ye+_s, ye-_s
    cols = []; cost = []
    for r in S: cols.append(cons[r][0]); cost.append(cons[r][1])
    for s_ in E: cols.append(eqs[s_][0]); cost.append(eqs[s_][1])
    for s_ in E: cols.append({k: -v for k, v in eqs[s_][0].items()}); cost.append(-eqs[s_][1])
    keys = sorted(set(k for col in cols for k in col) | set(d.keys()))
    M = [[F(col.get(k, 0)) for col in cols] for k in keys]
    rr = [F(d.get(k, 0)) for k in keys]
    st, v, val = simplex_eq([F(c) for c in cost], M, rr)
    if st != 'opt': return None
    y = {r: v[a] for a, r in enumerate(S) if v[a] != 0}
    ye = {}
    for a, s_ in enumerate(E):
        c_ = v[len(S)+a] - v[len(S)+len(E)+a]
        if c_ != 0: ye[s_] = c_
    return (y, ye), val
def prove_max(cons, eqs, d, h, n, tol=1e-9, extra=6):
    A, b = tomat(cons, n); Ae, be = tomat(eqs, n)
    c = np.zeros(n)
    for k, v in d.items(): c[int(k)] = -float(v)
    res = linprog(c, A_ub=A if len(cons) else None, b_ub=b if len(cons) else None, A_eq=Ae if len(eqs) else None,
                  b_eq=be if len(eqs) else None, bounds=[(None, None)]*n, method='highs')
    if res.status != 0: return None
    lam = -res.ineqlin.marginals if len(cons) else np.zeros(0)
    order = np.argsort(-lam)
    for thr in (1e-10, 1e-13):
        S = [int(r) for r in order if lam[r] > thr]
        # add some near-active constraints for robustness
        slack = b - A @ res.x
        near = [int(r) for r in np.argsort(slack)[:len(S)+extra] if int(r) not in S]
        for SS in (S, S + near):
            out = dual_small(cons, eqs, SS, d, n)
            if out is None: continue
            cert, val = out
            if val <= h and check_max(cert, cons, eqs, d, h): return cert
    # full exact fallback
    out = dual_small(cons, eqs, list(range(len(cons))), d, n)
    if out is not None and out[1] <= h and check_max(out[0], cons, eqs, d, h): return out[0]
    return None
def prove_empty(cons, eqs, n):
    """phase-1: min s st a.z - s <= rhs. dual gives Farkas."""
    A, b = tomat(cons, n); Ae, be = tomat(eqs, n)
    A2 = np.hstack([A, -np.ones((len(cons), 1))]); c = np.zeros(n+1); c[-1] = 1
    Ae2 = np.hstack([Ae, np.zeros((len(eqs), 1))]) if len(eqs) else None
    res = linprog(c, A_ub=A2, b_ub=b, A_eq=Ae2, b_eq=be if len(eqs) else None,
                  bounds=[(None, None)]*n + [(0, None)], method='highs')
    if res.status != 0 or res.fun <= 1e-12: return None
    lam = -res.ineqlin.marginals
    order = np.argsort(-lam)
    for thr in (1e-10, 1e-13):
        S = [int(r) for r in order if lam[r] > thr]
        slack = b - A @ res.x[:n] + res.x[n]
        near = [int(r) for r in np.argsort(slack)[:len(S)+6] if int(r) not in S]
        for SS in (S, S+near):
            cert = farkas_small(cons, eqs, SS, n)
            if cert is not None and check_empty(cert, cons, eqs): return cert
    cert = farkas_small(cons, eqs, list(range(len(cons))), n)
    if cert is not None and check_empty(cert, cons, eqs): return cert
    return None
def farkas_small(cons, eqs, S, n):
    E = list(range(len(eqs)))
    cols = []; cost = []
    for r in S: cols.append(cons[r][0]); cost.append(cons[r][1])
    for s_ in E: cols.append(eqs[s_][0]); cost.append(eqs[s_][1])
    for s_ in E: cols.append({k: -v for k, v in eqs[s_][0].items()}); cost.append(-eqs[s_][1])
    keys = sorted(set(k for col in cols for k in col))
    M = [[F(col.get(k, 0)) for col in cols] for k in keys]
    rr = [F(0) for k in keys]
    # normalisation sum_{r in S} y_r == 1
    M.append([F(1)]*len(S) + [F(0)]*(2*len(E))); rr.append(F(1))
    st, v, val = simplex_eq([F(c) for c in cost], M, rr)
    if st != 'opt' or val >= 0: return None
    y = {r: v[a] for a, r in enumerate(S) if v[a] != 0}
    ye = {}
    for a, s_ in enumerate(E):
        c_ = v[len(S)+a] - v[len(S)+len(E)+a]
        if c_ != 0: ye[s_] = c_
    return (y, ye)
