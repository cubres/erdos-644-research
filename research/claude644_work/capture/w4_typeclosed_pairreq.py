"""Fano pair+request tests via the exact Fano criterion (discovery).
Lines 0..6 (FANO_LINES); pattern[l] in {'a','b','R'}.  Supplied rows carry type a or b; requested
row l gets an upper bound U_l = x - d_l with sum_i d_{l,i} <= T (T < tau*).  Per part the Fano
criterion (rows<=x automatically, pencils <= 2x, total <= 4x) must hold with requested rows at their
bounds.  LP: minimise max_l sum_i d_{l,i}; success if < tau*.
"""
import itertools
import numpy as np
from scipy.optimize import linprog

LINES = [frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]

def fano_autos():
    Lset = set(LINES); out = []
    for perm in itertools.permutations(range(7)):
        if all(frozenset(perm[q] for q in L) in Lset for L in LINES):
            out.append([LINES.index(frozenset(perm[q] for q in L)) for L in LINES])
    return out
AUTOS = fano_autos()

def pattern_reps(symbols=('a', 'b', 'R')):
    reps = {}
    for pat in itertools.product(symbols, repeat=7):
        key = min(tuple(pat[g.index(l)] for l in range(7)) for g in AUTOS)
        reps.setdefault(key, pat)
    return list(reps.values())

def req_cost(pattern, types, x):
    """pattern: list of 7 entries, each an index into types or None (requested)."""
    p = len(x); R = [l for l in range(7) if pattern[l] is None]
    S = [l for l in range(7) if pattern[l] is not None]
    # fixed loads
    load = [[types[pattern[l]][i] if pattern[l] is not None else 0.0 for l in range(7)] for i in range(p)]
    if not R:
        ok = all(sum(load[i]) <= 4*x[i] + 1e-12 and all(sum(load[i][l] for l in range(7) if q in LINES[l]) <= 2*x[i] + 1e-12 for q in range(7)) for i in range(p))
        return 0.0 if ok else None
    nR = len(R); nv = p*nR + 1
    dv = lambda i, k: i*nR + k
    A = []; b = []
    for i in range(p):
        # total: sum_S load + sum_R (x - d) <= 4x  ->  -sum d <= 4x - sumS - nR x
        row = np.zeros(nv)
        for k in range(nR): row[dv(i, k)] = -1
        A.append(row); b.append(4*x[i] - sum(load[i][l] for l in S) - nR*x[i])
        for q in range(7):
            thr = [l for l in range(7) if q in LINES[l]]
            row = np.zeros(nv); const = 0.0
            for l in thr:
                if l in S: const += load[i][l]
                else:
                    const += x[i]; row[dv(i, R.index(l))] = -1
            A.append(row); b.append(2*x[i] - const)
    for k in range(nR):
        row = np.zeros(nv); row[-1] = -1
        for i in range(p): row[dv(i, k)] = 1
        A.append(row); b.append(0.0)
    bounds = [(0, x[i]) for i in range(p) for k in range(nR)] + [(0, None)]
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method='highs')
    if res.status != 0: return None
    return res.fun

PATS2 = None
def best_pair_request(types, x, tau, max_types=2, stop_below=None):
    """min request cost over ordered choices of <= max_types supplied types and Fano patterns."""
    global PATS2
    syms = ('a', 'b', 'R') if max_types == 2 else ('a', 'R')
    pats = pattern_reps(syms)
    best = (float('inf'), None)
    m = len(types)
    combos = itertools.product(range(m), repeat=max_types)
    for combo in combos:
        for pat in pats:
            pattern = [None if s == 'R' else combo[0 if s == 'a' else 1] for s in pat]
            c = req_cost(pattern, types, x)
            if c is not None and c < best[0]:
                best = (c, pattern)
                if stop_below is not None and c < stop_below: return best
    return best

if __name__ == '__main__':
    print(len(AUTOS), 'automorphisms;', len(pattern_reps()), 'pattern orbits (a,b,R)')
    T79 = [(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
    types = [[v/80 for v in t] for t in T79]; x = [513/640]*3
    print(best_pair_request(types, x, 483/640))
