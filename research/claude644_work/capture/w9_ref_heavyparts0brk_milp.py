"""Referee w9, heavyparts#0 BRK, part F: MILP for
   sup tau*  over one-type-per-class families (3 types, type c super-heavy at part c, p parts),
   subject to NO mutual/cyclic conflict AND NO Fano tuple (so the obstruction is purely per-part totals).
All constraints are linear in (x,T) once disjunctions are fixed -> big-M MILP (HiGHS). Strict inequalities
use margin EPS.  The optimum is then rounded and re-certified EXACTLY (Fractions, brute force 3^7 maps,
exact tau*) with the independent functions of w9_ref_heavyparts0brk_random.py.
usage: python3 w9_ref_heavyparts0brk_milp.py p EPS [sumle1] [xmax]"""
import sys, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from fractions import Fraction as Fr
from w9_ref_heavyparts0brk_arccsp import PATSETS, minimal_hitting
import w9_ref_heavyparts0brk_random as R
MH = [set(F) for F in minimal_hitting()]
CL = 'ABC'

def solve(p, EPS, sumle1=False, xmax=3.0, BM=14.0, extra_rows=None):
    names = []; idx = {}
    def var(n):
        idx[n] = len(names); names.append(n); return idx[n]
    for i in range(p): var(('x', i))
    for c in range(3):
        for i in range(p): var(('T', c, i))
    var('t')
    ncont = len(names)
    rows = []   # (dict coef, lo, hi)
    X = lambda i: idx[('x', i)]; T = lambda c, i: idx[('T', c, i)]
    for c in range(3):
        rows.append(({T(c, i): 1 for i in range(p)}, (-np.inf if sumle1 else 1), 1))
        for i in range(p): rows.append(({T(c, i): 1, X(i): -1}, -np.inf, 0))
        rows.append(({T(c, c): 3, X(c): -2}, EPS, np.inf))
    def patsum(P, i):
        d = {}
        for ch in P: d[T(CL.index(ch), i)] = d.get(T(CL.index(ch), i), 0) + 1
        return d
    # no conflict: each minimal set has an allowed pattern
    for M in (MH if __import__('os').environ.get('CONTROL') != '1' else []):   # CONTROL=1: drop no-conflict
        ys = []
        for P in sorted(M):
            y = var(('y', tuple(sorted(M)), P)); ys.append(y)
            for i in range(p):
                d = patsum(P, i); d[X(i)] = d.get(X(i), 0) - 2; d[y] = BM
                rows.append((d, -np.inf, BM))
        rows.append(({y: 1 for y in ys}, 1, np.inf))
    # Fano-free: every (patset, count) is killed by a forbidden pattern or a violated total
    for ps, cnts in PATSETS.items():
        for n in cnts:
            zs = []
            for P in sorted(ps):
                for i in range(p):
                    z = var(('zp', P, i, n)); zs.append(z)
                    d = patsum(P, i); d[X(i)] = d.get(X(i), 0) - 2; d[z] = -BM
                    rows.append((d, EPS - BM, np.inf))
            for i in range(p):
                z = var(('zt', i, n)); zs.append(z)
                d = {T(c, i): n[c] for c in range(3)}; d[X(i)] = -4; d[z] = -BM
                rows.append((d, EPS - BM, np.inf))
            rows.append(({z: 1 for z in zs}, 1, np.inf))
    # FIX (entry 1): zero-trace indicators. v_ci=1 forces T_ci=0; a blocking map sending c to such a part is
    # INVALID (cannot block a zero trace), so its constraint is switched off.
    for c in range(3):
        for i in range(p):
            if i == c: continue
            v = var(('v', c, i)); rows.append(({T(c, i): 1, v: xmax}, -np.inf, xmax))
    # tau* >= t: for every blocking map pi some selection has sum_i (x_i - T_{s(i),i}) >= t
    for pi in itertools.product(range(p), repeat=3):
        classes = {}
        for c, i in enumerate(pi): classes.setdefault(i, []).append(c)
        parts = sorted(classes)
        ws = []
        for sel in itertools.product(*[classes[i] for i in parts]):
            w = var(('w', pi, sel)); ws.append(w)
            d = {idx['t']: -1, w: -BM}
            for i, c in zip(parts, sel):
                d[X(i)] = d.get(X(i), 0) + 1; d[T(c, i)] = d.get(T(c, i), 0) - 1
            rows.append((d, -BM, np.inf))
        d = {w: 1 for w in ws}
        for c, i in enumerate(pi):
            if i != c: d[idx[('v', c, i)]] = d.get(idx[('v', c, i)], 0) + 1
        rows.append((d, 1, np.inf))
    if extra_rows:
        for d, lo, hi in extra_rows: rows.append(({idx[k]: v for k, v in d.items()}, lo, hi))
    nv = len(names)
    A = np.zeros((len(rows), nv)); lo = np.zeros(len(rows)); hi = np.zeros(len(rows))
    for r, (d, l, h) in enumerate(rows):
        for k, v in d.items(): A[r, k] += v
        lo[r] = l; hi[r] = h
    cobj = np.zeros(nv); cobj[idx['t']] = -1
    lb = np.zeros(nv); ub = np.ones(nv)
    for i in range(p): ub[X(i)] = (1.5 if i < 3 else xmax); lb[X(i)] = 0.0   # super-heavy => x_c < 3/2
    lb[idx['t']] = 0; ub[idx['t']] = 10
    integ = np.array([0]*ncont + [1]*(nv - ncont))
    res = milp(cobj, constraints=LinearConstraint(A, lo, hi), integrality=integ, bounds=Bounds(lb, ub),
               options={'time_limit': float(__import__('os').environ.get('TL', 500)), 'mip_rel_gap': 1e-7})
    if res.x is None: return res, None, None, None
    xs = [res.x[X(i)] for i in range(p)]
    Ts = [[res.x[T(c, i)] for i in range(p)] for c in range(3)]
    return res, xs, Ts, res.x[idx['t']]

def certify(x, T, D):
    p = len(x)
    xq = [Fr(round(v*D), D) for v in x]; Tq = []
    for a in T:
        aq = [Fr(round(v*D), D) for v in a]; Tq.append(aq)
    adm = all(0 <= Tq[c][i] <= xq[i] for c in range(3) for i in range(p)) and all(sum(a) <= 1 for a in Tq)
    sup = all(3*Tq[c][c] > 2*xq[c] for c in range(3))
    Fb = R.forbidden(xq, Tq); conf = any(F <= Fb for F in MH)
    fano = R.feas(xq, Tq); ts = R.tau_star(xq, Tq)
    return dict(adm=adm, sup=sup, sums=[str(sum(a)) for a in Tq], conflict=conf, fano=fano, tau=ts,
                x=[str(v) for v in xq], T=[[str(v) for v in a] for a in Tq], F=sorted(Fb))

if __name__ == '__main__':
    p = int(sys.argv[1]); EPS = float(sys.argv[2]); sumle1 = len(sys.argv) > 3 and sys.argv[3] == '1'
    xmax = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    res, x, T, t = solve(p, EPS, sumle1, xmax)
    print('p=%d EPS=%g sumle1=%s xmax=%g status=%s' % (p, EPS, sumle1, xmax, res.message))
    if x is None: print('NO SOLUTION'); sys.exit()
    print('MILP opt t=%.6f  dual bound=%s' % (t, getattr(res, 'mip_dual_bound', None)))
    print(' x', [round(v, 6) for v in x]); print(' T', [[round(v, 6) for v in a] for a in T])
    for D in (10**4, 10**6):
        r = certify(x, T, D)
        print(' EXACT D=%d:' % D, {k: (str(v) if k == 'tau' else v) for k, v in r.items()}, ' tau*~%.6f' % float(r['tau']))
