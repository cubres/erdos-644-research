"""L(m; alpha, beta): min over cross-intersecting label families (A-labels, B-labels nonempty subsets of [m])
and distributions p (mass alpha) q (mass beta) of max_i load_i, load_i = p(S ni i)+q(S ni i).
Enumerate upsets A-family via antichains (generating sets); B = blocker (all sets meeting every generator).
LP per pair. Discovery (floating LP)."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

def subsets(m):
    return [S for S in range(1, 1<<m)]

def antichains(m):
    sets = subsets(m)
    res = []
    # brute force: enumerate antichains by recursion over sets ordered
    sets_sorted = sorted(sets, key=lambda s:(bin(s).count('1'), s))
    def rec(i, chosen):
        if i == len(sets_sorted):
            if chosen: res.append(list(chosen))
            return
        s = sets_sorted[i]
        rec(i+1, chosen)
        if all((s & c) != c and (s & c) != s for c in chosen):
            chosen.append(s); rec(i+1, chosen); chosen.pop()
    rec(0, [])
    return res

def L(m, alpha, beta, verbose=False):
    best = (1e9, None)
    allS = subsets(m)
    for gen in antichains(m):
        Afam = [S for S in allS if any((S & g) == g for g in gen)]   # upset generated
        Bfam = [S for S in allS if all(S & g for g in gen)]
        if not Bfam: continue
        # LP vars: p_S (S in Afam), q_S (S in Bfam), z; min z
        nA, nB = len(Afam), len(Bfam)
        nv = nA + nB + 1
        c = np.zeros(nv); c[-1] = 1
        Aub = []; bub = []
        for i in range(m):
            row = np.zeros(nv)
            for j,S in enumerate(Afam):
                if S >> i & 1: row[j] = 1
            for j,S in enumerate(Bfam):
                if S >> i & 1: row[nA+j] = 1
            row[-1] = -1
            Aub.append(row); bub.append(0)
        Aeq = [np.r_[np.ones(nA), np.zeros(nB), 0], np.r_[np.zeros(nA), np.ones(nB), 0]]
        beq = [alpha, beta]
        r = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0,None)]*nv, method='highs')
        if r.status == 0 and r.fun < best[0] - 1e-12:
            best = (r.fun, (gen, [(Afam[j], r.x[j]) for j in range(nA) if r.x[j]>1e-9], [(Bfam[j], r.x[nA+j]) for j in range(nB) if r.x[nA+j]>1e-9]))
    return best

if __name__ == '__main__':
    for m in range(1, 6):
        v, w = L(m, 1.0, 1.0)
        print(m, round(v,6), w)
