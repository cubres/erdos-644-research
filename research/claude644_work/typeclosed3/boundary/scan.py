"""float scan: for an adversary point, which candidate new types t produce a template (F all assignments of the
roles+t, V, T3, R) -- helper for designing requests.  best_margin(R, x, tau) -> (margin, name)"""
import sys, os, itertools, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import gen_cert as G
from gen_cert3 import rt_eval


def best_margin(R, x, tau, fk=7, rk=4):
    names = list(R); best = (np.inf, None)
    for k in range(1, min(fk, len(names)) + 1):
        combos = list(itertools.combinations(names, k))
        Rc = np.array([[R[n] for n in cb] for cb in combos])
        for pat in G.pattern_reps(k):
            Z = Rc[:, list(pat), :]
            mg = np.max(Z.sum(1) - 4 * x, axis=1)
            for l in G.LINES:
                mg = np.maximum(mg, np.max(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x, axis=1))
            j = int(np.argmin(mg))
            if mg[j] < best[0]: best = (float(mg[j]), 'F ' + ','.join(combos[j][p] for p in pat))
    for a in names:
        for b in names:
            if a != b:
                mg = max(np.max(R[a] + R[b] - x), np.max(1.25 * R[a] + 0.5 * R[b] - x))
                if mg < best[0]: best = (float(mg), 'V %s,%s' % (a, b))
    for t in itertools.combinations_with_replacement(names, 3):
        A, B, C = R[t[0]], R[t[1]], R[t[2]]; S = A + B + C
        mg = max(np.max(S - 2 * x), np.maximum(np.maximum(A, B), np.maximum(C, S / 2)).sum() / 2 - tau)
        if mg < best[0]: best = (float(mg), 'T3 ' + ','.join(t))
    r = rt_eval(R, names, x, tau, rk, tol=np.inf)
    if r and r[0][0] < best[0]: best = r[0]
    from gen_cert3 import w_eval
    r = w_eval(R, names, x, tol=np.inf)
    if r and r[0][0] < best[0]: best = r[0]
    return best


def load_adv(fn):
    d = json.load(open(fn)); v = d['v']
    x = np.array([v['x0'], v['x1'], v['x2']]); tau = v['tau']
    R = {}
    for k in v:
        if k.startswith('c') and k[-2] == '_': R.setdefault(k[1:-2], [0.0] * 3)[int(k[-1])] = v[k]
    return x, tau, {n: np.array(c) for n, c in R.items()}, v


if __name__ == '__main__':
    x, tau, R, v = load_adv(sys.argv[1])
    print('x', x.round(4), 'tau', round(tau, 4), 'base', best_margin(R, x, tau))
    # scan types with c_k = 0 along the edge
    for k in range(3):
        i, j = [q for q in range(3) if q != k]
        for t in np.linspace(max(0, 1 - x[j]), min(1, x[i]), 11):
            c = np.zeros(3); c[i] = t; c[j] = 1 - t
            R2 = dict(R); R2['T'] = c
            m = best_margin(R2, x, tau)
            print('c_%d=0' % k, c.round(3), '%.4f' % m[0], m[1])
