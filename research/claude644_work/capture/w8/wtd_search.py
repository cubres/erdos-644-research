"""Search: (p,2)-families S on n vertices (edges as bitmasks), max over weights w>=0 of
tau_w(S) subject to w(E)<=1 for every edge (and optional cap w_v<=c).  Discovery (float LP)."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog

def has_p2(edges, n, p):
    pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
    E = list(edges)
    for r in range(1, min(p, len(E))+1):
        for sub in itertools.combinations(E, r):
            if not any(all(e & q for e in sub) for q in pairs):
                return False
    return True

def min_transversals(edges, n):
    res = []
    for m in range(1, 1<<n):
        if all(e & m for e in edges):
            if not any((r & m) == r for r in res):
                res.append(m)
    return res

def best_weight(edges, n, cap=None):
    T = min_transversals(edges, n)
    # vars w_0..w_{n-1}, t ; maximize t
    c = np.zeros(n+1); c[-1] = -1
    A = []; b = []
    for J in T:
        row = np.zeros(n+1); row[-1] = 1
        for v in range(n):
            if J >> v & 1: row[v] = -1
        A.append(row); b.append(0)
    for e in edges:
        row = np.zeros(n+1)
        for v in range(n):
            if e >> v & 1: row[v] = 1
        A.append(row); b.append(1)
    bounds = [(0, cap)]*n + [(0, None)]
    r = linprog(c, A_ub=np.array(A), b_ub=b, bounds=bounds, method='highs')
    return -r.fun, r.x[:n]

def search(n, p, cap, iters, seed):
    rng = random.Random(seed)
    best = (0, None)
    allsets = list(range(1, 1<<n))
    for it in range(iters):
        m = rng.randint(2, 9)
        edges = set()
        tries = 0
        while len(edges) < m and tries < 200:
            tries += 1
            e = rng.choice(allsets)
            if e in edges: continue
            cand = edges | {e}
            if has_p2(cand, n, p): edges = cand
        edges = sorted(edges)
        # remove dominated (supersets) - keep all; value computed
        val, w = best_weight(edges, n, cap)
        # local improvement: try adding edges greedily
        improved = True
        while improved:
            improved = False
            for e in rng.sample(allsets, len(allsets)):
                if e in edges: continue
                cand = sorted(set(edges) | {e})
                if not has_p2(cand, n, p): continue
                v2, w2 = best_weight(cand, n, cap)
                if v2 > val + 1e-9:
                    edges, val, w = cand, v2, w2; improved = True; break
        if val > best[0] + 1e-9:
            best = (val, edges, w)
            print(f'it {it} val {val:.4f} edges {[bin(e)[2:].zfill(n)[::-1] for e in edges]} w {np.round(w,3)}', flush=True)
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]); p = int(sys.argv[2]); cap = None if sys.argv[3] == 'none' else float(sys.argv[3])
    search(n, p, cap, int(sys.argv[4]), int(sys.argv[5]))
