"""Targeted discovery for a global maximum-imbalance bound.

Unlike max_imbalance.py, the old state imbalance t need not equal the global
bound M. A response obeys all three replacement imbalance bounds and all
three globally propagated pair-overlap gaps. Linear programming is numerical
discovery. A failed request can subsequently be proved by exact inequalities.

The box-simplex vertex menu does NOT exhaust a union-of-polyhedra containment
problem; passing the menu is only a precisely delimited one-response barrier.
"""
from itertools import product, combinations
import json
import numpy as np
from scipy.optimize import linprog

TYPES = list(product((0, 1), repeat=3))
EVEN = [i for i, z in enumerate(TYPES) if sum(z) % 2 == 0]
PAIRS = list(combinations(range(3), 2))
ROWS = np.array(TYPES, dtype=float).T
OPPOSITE = np.array([[int(z[i] == z[j]) for z in TYPES] for i, j in PAIRS])


def state(v, t):
    w = np.zeros(8)
    for z, x in zip(EVEN, v):
        w[z], w[7-z] = x+t, x
    return w


def vertices(w, T=.75):
    seen = set()
    for bits in product((0, 1), repeat=8):
        u = w * bits
        for j in range(8):
            d = u.copy()
            d[j] = T - sum(d[i] for i in range(8) if i != j)
            if d[j] < -1e-8 or d[j] > w[j]+1e-8:
                continue
            d = np.clip(d, 0, w)
            key = tuple(np.round(d, 10))
            if key not in seen:
                seen.add(key)
                yield d


def response(w, u, M, T=.75):
    u = np.clip(u, 0, w)
    a = OPPOSITE @ w / 2
    A = np.r_[OPPOSITE, -OPPOSITE]
    rhs = np.r_[a+M, M-a]
    bands = [(0, M), (T-M, 1-T+M), (1-M, 1)]
    lower = ROWS @ u
    upper = np.minimum(ROWS @ w, lower+1-T)
    allowed = [[j for j, (lo, hi) in enumerate(bands)
                if lo <= hi+1e-9 and lo <= upper[i]+1e-9 and hi >= lower[i]-1e-9]
               for i in range(3)]
    for modes in product(*allowed):
        lo = np.array([bands[j][0] for j in modes])
        hi = np.array([bands[j][1] for j in modes])
        r = linprog(np.zeros(8), A_ub=np.r_[A, ROWS, -ROWS],
                    b_ub=np.r_[rhs, hi, -lo], A_eq=[np.ones(8)], b_eq=[1],
                    bounds=list(zip(u, w)), method='highs')
        if r.success:
            return {'g': r.x.tolist(), 'modes': modes}
        if r.status != 2:
            raise RuntimeError(r.message)
    return None


def check(v, t, M, T=.75, random=0):
    w = state(v, t)
    count = 0
    menu = list(vertices(w, T))
    rng = np.random.default_rng(2644)
    random_menu = [np.clip(rng.dirichlet(np.ones(3)) @
                          np.array([menu[j] for j in rng.integers(len(menu), size=3)]), 0, w)
                   for _ in range(random)]
    for u in menu + random_menu:
        count += 1
        if response(w, u, M, T) is None:
            return {'M': M, 't': t, 'v': list(v), 'count': count, 'bad': u.tolist()}
    return {'M': M, 't': t, 'v': list(v), 'count': count, 'bad': None}


def regularized_states(M, draws=10, seed=644):
    """Vertices exposed by random objectives on the exact regularized polytope."""
    # variables v0,v1,v2,v3,t
    A, b = [], []
    for i, j in combinations(range(4), 2):
        row = np.zeros(5)
        row[i] = row[j] = row[4] = 1
        A.extend([row, -row])
        b.extend([.25+M, M-.75])
    for i in [0, 3]:
        row = np.zeros(5)
        row[i] = row[4] = -1
        A.append(row)
        b.append(-.375)
    bounds = [(0, None)]*4 + [(.5-M, M)]
    rng = np.random.default_rng(seed)
    seen = set()
    for objective in list(np.eye(5))+list(-np.eye(5))+list(rng.normal(size=(draws, 5))):
        r = linprog(objective, A_ub=A, b_ub=b, A_eq=[[1, 1, 1, 1, 2]],
                    b_eq=[1], bounds=bounds, method='highs')
        if not r.success:
            raise RuntimeError(r.message)
        key = tuple(np.round(r.x, 10))
        if key not in seen:
            seen.add(key)
            yield r.x[:4], r.x[4]


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--M', type=float, default=1/3)
    p.add_argument('--draws', type=int, default=12)
    p.add_argument('--uniform', action='store_true')
    p.add_argument('--random', type=int, default=0)
    args = p.parse_args()
    states = [(np.repeat(.125, 4), .25)] if args.uniform else regularized_states(args.M, args.draws)
    for v, t in states:
        print(json.dumps(check(v, t, args.M, random=args.random)), flush=True)
