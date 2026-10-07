# Finite rigid type sets: tau* and pair-template tests.  (templates agent)
import itertools
import numpy as np
from hub_lib import TWO, LINES, fano_template, fano_colourings
from scipy.optimize import linprog
def tau_rigid(x, T):
    """tau* of rigid finite type set T (list of vectors): N - sup{sum u : u free}; u_i in {x_i} u {t_i (as t_i - 0)}"""
    p = len(x); N = sum(x); best = N - 1
    cand = [sorted(set([x[i]] + [t[i] for t in T if t[i] > 0])) for i in range(p)]
    for u in itertools.product(*cand):
        # u_i = c means residual just below c when c is a type coordinate (blocks types with t_i >= c), or x_i
        ok = True
        for t in T:
            if all((t[i] < u[i]) or (u[i] == x[i] and t[i] <= x[i] and not any(tt[i] == x[i] for tt in []) ) for i in range(p)):
                # t fits unless some coordinate blocks: coordinate i blocks t iff u_i != x_i-sentinel and t_i >= u_i
                pass
            blocked = any(u[i] < x[i] + 1e-15 and t[i] >= u[i] - 1e-15 and not (u[i] == x[i] and t[i] < x[i]) for i in range(p) if not (u[i] == x[i] and t[i] <= x[i] and t[i] != x[i]))
            if not blocked: ok = False; break
        if ok: best = min(best, N - sum(u))
    return best
def tau_rigid2(x, T):
    """cleaner: choose for each part a cutoff c_i in {none} u {t_i>0}; part i blocks t iff t_i >= c_i; cost x_i - c_i."""
    p = len(x); N = sum(x); best = N - 1
    cand = [[None] + sorted(set(t[i] for t in T if t[i] > 1e-15)) for i in range(p)]
    for c in itertools.product(*cand):
        if all(any(c[i] is not None and t[i] >= c[i] - 1e-15 for i in range(p)) for t in T):
            best = min(best, sum(x[i] - c[i] for i in range(p) if c[i] is not None))
    return best
def feas(x, a, b, fs):
    return all(sum(cf * v for cf, v in zip(f, (a[i], b[i]))) <= x[i] + 1e-12 for i in range(len(x)) for f in fs)
def pair_menu(x, T, names=None):
    names = names or list(TWO)
    for i, a in enumerate(T):
        if all(7 * a[k] <= 4 * x[k] + 1e-12 for k in range(len(x))): return ('H', i)
    for name in names:
        fs = TWO[name]
        for i, a in enumerate(T):
            for j, b in enumerate(T):
                if i != j and feas(x, a, b, fs): return (name, i, j)
    return None
def fano_rigid(x, T, col):
    """Fano colouring with rigid types T[col[r]]: Lemma 7.63 per part"""
    p = len(x)
    for i in range(p):
        z = [T[col[r]][i] for r in range(7)]
        if max(z) > x[i] + 1e-12 or sum(z) > 4 * x[i] + 1e-12: return False
        if any(z[a] + z[b] + z[c] > 2 * x[i] + 1e-12 for a, b, c in LINES): return False
    return True
