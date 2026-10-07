"""Adversarial search for counterexamples to the Gap-Triple conjecture (p parts; discovery, floats).

Gap-Triple(p): capacities x; thresholds t with 4x_i/7 < t_i <= x_i and cost sum(x - t) > 3/4;
blocking types b^1..b^p (unit, 0<=b<=x) with b^i_i >= t_i and b^i_j < t_j (j != i).
Claim: some Fano assignment of {b^i} (Lemma 7.63) or some V(b^i, b^j) is feasible.

badness(config) = min over templates of max normalized constraint violation (>0 => all templates fail).
The adversary maximizes badness over configs satisfying the constraints (penalty for violated constraints).
"""
import numpy as np, itertools, sys
from scipy.optimize import minimize

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def make_assign(m):
    A = np.array(list(itertools.product(range(m), repeat=7)), dtype=int)
    # keep all (no symmetry reduction; fine for m<=4)
    return A


def template_badness(B, x, A):
    """B: m x p types; x: p. returns min over Fano assignments and V pairs of max normalized violation."""
    m, p = B.shape
    worst = np.full(len(A), -np.inf)
    for i in range(p):
        z = B[:, i][A]                     # (nA, 7)
        viol = (z.sum(1) - 4 * x[i]) / x[i]
        worst = np.maximum(worst, viol)
        for l in LINES:
            worst = np.maximum(worst, (z[:, l[0]] + z[:, l[1]] + z[:, l[2]] - 2 * x[i]) / x[i])
    best = worst.min()
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            v = max(max(B[a, i] + B[b, i] - x[i], 1.25 * B[a, i] + 0.5 * B[b, i] - x[i]) / x[i] for i in range(p))
            best = min(best, v)
    return best


def decode(v, p):
    """v -> (x, t, B). x_i = 0.05 + softplus; t_i = x_i*(4/7 + 3/7*sigmoid); blockers built from free params."""
    v = np.asarray(v)
    x = 0.02 + np.log1p(np.exp(v[:p]))
    s = 1 / (1 + np.exp(-v[p:2 * p]))
    t = x * (4 / 7 + (3 / 7) * s)
    B = np.zeros((p, p))
    k = 2 * p
    for i in range(p):
        # own coordinate in [t_i, x_i]; others in [0, t_j) scaled; then must sum to 1 -> penalty
        k += 1                      # (unused parameter kept for dimension stability)
        B[i, i] = t[i]              # blocker touches its facet exactly
        for j in range(p):
            if j != i:
                B[i, j] = t[j] * 0.999 / (1 + np.exp(-v[k])); k += 1
    return x, t, B


def objective(v, p, A):
    x, t, B = decode(v, p)
    pen = 0.0
    pen += sum(abs(B[i].sum() - 1) for i in range(p)) * 50
    cost = (x - t).sum()
    pen += max(0.0, 0.75 + 1e-3 - cost) * 50
    return -template_badness(B, x, A) + pen


def run(p=3, restarts=200, seed=0):
    rng = np.random.default_rng(seed)
    A = make_assign(p)
    dim = 2 * p + p * p
    best = (-np.inf, None)
    for r in range(restarts):
        v0 = rng.normal(0, 1.5, dim)
        res = minimize(objective, v0, args=(p, A), method='Nelder-Mead',
                       options={'maxiter': 4000, 'xatol': 1e-7, 'fatol': 1e-9})
        x, t, B = decode(res.x, p)
        feas = all(abs(B[i].sum() - 1) < 1e-4 for i in range(p)) and (x - t).sum() > 0.75
        bad = template_badness(B, x, A)
        if feas and bad > best[0]:
            best = (bad, (x, t, B))
            print('restart %d badness %.5f cost %.4f x=%s' % (r, bad, (x - t).sum(), np.round(x, 4)), flush=True)
    return best


if __name__ == '__main__':
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    bad, (x, t, B) = run(p, R, seed)
    print('BEST badness', bad)
    print('x', x.tolist()); print('t', t.tolist()); print('B', B.tolist())
