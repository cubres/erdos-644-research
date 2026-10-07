"""Single-type request tests (discovery).  A support D (parent cells as 7-bit masks), a set S of
rows supplied with ONE fixed type e (same e on every supplied row), the other rows R requested
from the net.  Per part i: masses y_C >= 0 on parent cells, sum y_C <= x_i, supplied loads
sum_{C ni j} y_C >= e_i (j in S).  Request cost of row j in R: sum_i (x_i - sum_{C ni j} y^i_C).
Minimise t = max_{j in R} cost_j.  If t < tau*, the type e lies in a bad tuple (e on S rows, the
requested types on R rows): place each row inside its cells and trim.
"""
import itertools, json
import numpy as np
from scipy.optimize import linprog

FANO_LINES = [frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
# Fano support in "row" language: rows = lines (0..6); cell of a point q = set of lines NOT through q
FANO_CELLS = [sum(1 << l for l, L in enumerate(FANO_LINES) if q not in L) for q in range(7)]

def single_test(parents, S, e, x):
    """returns min t (float) or None if infeasible."""
    p = len(x); P = list(parents); nc = len(P)
    R = [j for j in range(7) if j not in S]
    if not R:
        return None
    nv = p*nc + 1
    A = []; b = []
    for i in range(p):
        row = np.zeros(nv); row[i*nc:(i+1)*nc] = 1; A.append(row); b.append(x[i])
        for j in S:
            row = np.zeros(nv)
            for k, C in enumerate(P):
                if C >> j & 1: row[i*nc+k] = -1
            A.append(row); b.append(-e[i])
    for j in R:
        row = np.zeros(nv); row[-1] = -1
        const = 0.0
        for i in range(p):
            const += x[i]
            for k, C in enumerate(P):
                if C >> j & 1: row[i*nc+k] -= 1
        # const - sum loads - t <= 0
        A.append(row); b.append(-const)
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, None)]*nv, method='highs')
    if res.status != 0: return None
    return res.fun

def fano_splits():
    """representatives of supplied-line sets S up to Fano automorphism (by brute force canonical form)."""
    # automorphisms of Fano acting on lines: generate via point permutations preserving lines
    pts = range(7)
    Lset = set(FANO_LINES)
    autos = []
    for perm in itertools.permutations(pts):
        if all(frozenset(perm[q] for q in L) in Lset for L in FANO_LINES):
            autos.append([FANO_LINES.index(frozenset(perm[q] for q in L)) for L in FANO_LINES])
    reps = {}
    for r in range(1, 7):
        for S in itertools.combinations(range(7), r):
            key = min(tuple(sorted(a[j] for j in S)) for a in autos)
            reps.setdefault(key, S)
    return list(reps.values())

if __name__ == '__main__':
    print(len(fano_splits()), fano_splits())
    x = [0.8, 0.8, 0.8]
    for e in ([0.54, 0.23, 0.23], [0.6, 0.2, 0.2], [0.7, 0.15, 0.15], [0.5, 0.5, 0.0], [0.55, 0.45, 0.0]):
        best = min((single_test(FANO_CELLS, S, e, x) or 9, S) for S in fano_splits())
        print(e, best)
