"""Adversarial greedy completion of an adversary's role set to a REAL family (covering all boxes of cost < tau):
repeatedly find the cheapest free box of the current family and insert the type in that box that keeps the
template badness (Fano <= 4 distinct types, 42 two-type functions, T3) as large as possible.  If at some step every
candidate creates a template, the templates found show what real families near the adversary are forced to contain.
usage: python3 core_complete.py <gadv.json | badv.json> [tau_target] [samples] [seed]"""
import sys, json, itertools
import numpy as np
from bal_adv import LINES, PATS, TT


def tau_star_box(K, x):
    """float tau* with the cheapest blocking thresholds (None = INF)"""
    K = np.asarray(K); n = len(K); best = (np.inf, None)
    c0 = sorted(set(K[:, 0][K[:, 0] > 0])) + [None]; c1 = sorted(set(K[:, 1][K[:, 1] > 0])) + [None]
    for t0 in c0:
        b0 = (K[:, 0] >= t0 - 1e-15) if t0 is not None else np.zeros(n, bool)
        for t1 in c1:
            b1 = (K[:, 1] >= t1 - 1e-15) if t1 is not None else np.zeros(n, bool)
            unb = ~(b0 | b1); cost = (x[0] - t0 if t0 is not None else 0) + (x[1] - t1 if t1 is not None else 0)
            if not unb.any():
                t2 = None
            else:
                r = K[unb, 2]
                if (r <= 0).any(): continue
                t2 = r.min(); cost += x[2] - t2
            if cost < best[0]: best = (cost, (t0, t1, t2))
    return best


def badness(K, x, tau, fk=4):
    K = np.asarray(K); n = len(K); best = (np.inf, None)
    for k in range(1, min(fk, n) + 1):
        combos = np.array(list(itertools.combinations(range(n), k)))
        for pat in PATS[k]:
            idx = combos[:, list(pat)]; Z = K[idx]
            mg = np.max(Z.sum(1) - 4 * x, axis=1)
            for l in LINES:
                mg = np.maximum(mg, np.max(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x, axis=1))
            j = int(np.argmin(mg))
            if mg[j] < best[0]: best = (float(mg[j]), ('F', tuple(int(v) for v in idx[j])))
    for a in range(n):
        for b in range(n):
            if a == b: continue
            for fn, vs in enumerate(TT):
                mg = max(u * K[a, i] + v * K[b, i] - x[i] for i in range(3) for u, v in vs)
                if mg < best[0]: best = (mg, ('TT', a, b, fn))
    for a, b, c in itertools.combinations_with_replacement(range(n), 3):
        S = K[a] + K[b] + K[c]
        mg = max(np.max(S - 2 * x), np.maximum(np.maximum(K[a], K[b]), np.maximum(K[c], S / 2)).sum() / 2 - tau)
        if mg < best[0]: best = (float(mg), ('T3', a, b, c))
    return best


def box_vertices(w):
    V = []
    for free in range(3):
        o = [i for i in range(3) if i != free]
        for bits in itertools.product([0, 1], repeat=2):
            c = np.zeros(3)
            for i, bb in zip(o, bits): c[i] = w[i] if bb else 0.0
            c[free] = 1 - c.sum()
            if -1e-12 <= c[free] <= w[free] + 1e-12: V.append(c)
    return np.array(V)


def main():
    d = json.load(open(sys.argv[1]))
    tau_t = float(sys.argv[2]) if len(sys.argv) > 2 else None
    ns = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    if 'v' in d:
        v = d['v']; x = np.array([v['x%d' % i] for i in range(3)]); tau = v['tau']
        names = sorted(set(k[1:].rsplit('_', 1)[0] for k in v if k.startswith('c')))
        K = [np.array([v['c%s_%d' % (n, j)] for j in range(3)]) for n in names]
    else:
        x = np.array(d['x']); tau = d['tau']
        K = [np.array(r) for r, q in zip(d['roles'], d['Q']) if q is None or q == 1]
    tau_t = tau_t or tau
    K = [np.clip(c, 0, x) for c in K]
    print('x', np.round(x, 4), 'tau target %.4f' % tau_t, 'start badness', badness(np.array(K), x, tau_t))
    for step in range(40):
        cost, thr = tau_star_box(np.array(K), x)
        if cost >= tau_t - 1e-9:
            print('COVERING REACHED: tau* %.4f with %d types, badness %s' % (cost, len(K), badness(np.array(K), x, tau_t)))
            json.dump({'x': x.tolist(), 'K': [c.tolist() for c in K], 'tau': tau_t}, open('core_family.json', 'w'))
            return
        w = np.array([x[i] if thr[i] is None else thr[i] - 1e-7 for i in range(3)])
        V = box_vertices(w)
        cands = [V[i] for i in range(len(V))] + [rng.dirichlet(np.ones(len(V)) * 0.5) @ V for _ in range(ns)]
        cands = [c for c in cands if np.any(c > 2 * x / 3 + 1e-9)]      # super-heavy somewhere (pencil)
        if not cands:
            print('free box', np.round(w, 4), 'contains NO super-heavy type -> pencil template forced'); return
        scored = []
        for c in cands:
            b = badness(np.array(K + [c]), x, tau_t)
            scored.append((b[0], c, b[1]))
        scored.sort(key=lambda r: -r[0])
        b0, c0, arg = scored[0]
        print('step %d: free box cost %.4f w=%s  best insert %s badness %.5f (%s)' % (step, cost, np.round(w, 4), np.round(c0, 4), b0, arg))
        if b0 < 0:
            print('EVERY candidate in the box creates a template; best one:', arg)
            json.dump({'x': x.tolist(), 'K': [c.tolist() for c in K], 'box': w.tolist(), 'tau': tau_t}, open('core_stuck.json', 'w'))
            return
        K.append(c0)


if __name__ == '__main__':
    main()
