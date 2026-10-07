# Note Lemma 7.9 family (continuous, per k): parts X,Y,Z caps (0.40,1.39,0.99), types a=(0.2,0,0.8), b=(0,0.8,0.2).
# Intersecting, tau*/k = 39/50.  Sparsified at exp(-ck): tau_c, and exact-LP local rules (good-triple union, Lemma Q).
import numpy as np, itertools
from scipy.optimize import linprog
CAPS = {0: 0.40, 1: 1.39, 2: 0.99}
TYPES = {'a': {0: 0.2, 1: 0.0, 2: 0.8}, 'b': {0: 0.0, 1: 0.8, 2: 0.2}}
N = sum(CAPS.values())
def H(p):
    if p <= 0 or p >= 1: return 0.0
    return -p*np.log(p) - (1-p)*np.log(1-p)
def ent(w, u):  # ln(#u-profile subsets of a w-profile set)/k ; requires u <= w
    return sum(w[i]*H(u[i]/w[i]) for i in w if w[i] > 0)
def free_c(w, c):
    for u in TYPES.values():
        if all(u[i] <= w[i] + 1e-12 for i in w) and ent(w, u) > c: return False
    return True
def tau_c(c, step=0.005):
    best = 0.0
    grid = {i: np.arange(0, CAPS[i] + 1e-9, step) for i in CAPS}
    for wx in grid[0]:
        for wy in grid[1]:
            # for fixed wx, wy, |w| is maximised by the largest feasible wz: scan downwards
            for wz in grid[2][::-1]:
                w = {0: wx, 1: wy, 2: wz}
                if free_c(w, c):
                    best = max(best, wx + wy + wz); break
    return N - best
def lp_min(nsets, typenames, objective, extra_zero=()):
    """cells: (part i, subset S of range(nsets)); minimise objective(S) weighted sum subject to row profiles."""
    cells = [(i, S) for i in CAPS for r in range(0, nsets+1) for S in itertools.combinations(range(nsets), r)]
    nc = len(cells); cvec = np.array([objective(S) for i, S in cells])
    Aeq = []; beq = []
    for j in range(nsets):
        for i in CAPS:
            Aeq.append([1.0 if (ci == i and j in S) else 0.0 for ci, S in cells]); beq.append(TYPES[typenames[j]][i])
    Aub = []; bub = []
    for i in CAPS:
        Aub.append([1.0 if ci == i else 0.0 for ci, S in cells]); bub.append(CAPS[i])
    bounds = [(0, 0) if (S in extra_zero) else (0, None) for ci, S in cells]
    r = linprog(cvec, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method='highs')
    return r
def min_good_triple_union():
    best = None
    for tn in itertools.combinations_with_replacement('ab', 3):
        r = lp_min(3, tn, lambda S: 1.0 if len(S) > 0 else 0.0, extra_zero=[(0, 1, 2)])
        if r.status == 0 and (best is None or r.fun < best[0]): best = (r.fun, tn)
    return best
def min_Q4():
    best = None
    for tn in itertools.combinations_with_replacement('ab', 4):
        r = lp_min(4, tn, lambda S: len(S)*(len(S)-1)/2.0)
        if r.status == 0 and (best is None or r.fun < best[0]): best = (r.fun, tn)
    return best
if __name__ == '__main__':
    print('N/k =', N, ' tau_0 =', tau_c(0.0))
    print('min good-triple union (LP, per k):', min_good_triple_union())
    print('min 4-edge pairwise-intersection sum (LP, per k):', min_Q4())
    for c in [0.05, 0.1, 0.2, 0.25, 0.28, 0.3, 0.32, 0.35, 0.4, 0.45, 0.5]:
        print(f'c={c}: tau_c/k = {tau_c(c):.4f}', flush=True)
