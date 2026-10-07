"""Float evaluator of ONE-REQUEST Fano templates (RT): a Fano assignment where the points of P carry copies of one
requested type f (box u = min over lines/total, cost <= tau => f exists), the other points carry named roles.
P shapes up to automorphism: 1 point, 2 points, triangle (3 non-collinear), quadrangle (= T3).
usage: python3 rt_eval.py <gadv.json> [roles subset]"""
import sys, json, itertools
import numpy as np
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
SHAPES = {'P1': (0,), 'P2': (0, 1), 'P3': (0, 1, 3), 'P4': (3, 4, 5, 6)}   # (0,1,3) triangle; {3,4,5,6} = compl. of line 012


def roles_from(v):
    R = {}
    for k in v:
        if k.startswith('c') and k[-2] == '_':
            R.setdefault(k[1:-2], [0.0] * 3)[int(k[-1])] = float(v[k])
    return {n: np.array(c) for n, c in R.items()}


def rt_margins(R, x, tau, shapes=SHAPES, top=5):
    names = list(R); M = np.array([R[n] for n in names]); n = len(names)
    out = []
    for sh, P in shapes.items():
        A = [p for p in range(7) if p not in P]
        best = []
        for asg in itertools.product(range(n), repeat=len(A)):
            row = {A[i]: M[asg[i]] for i in range(len(A))}
            worst = -np.inf; u = np.full(3, np.inf)
            for l in LINES:
                npl = sum(1 for p in l if p in P)
                s = sum((row[p] for p in l if p not in P), np.zeros(3))
                if npl == 0:
                    worst = max(worst, ((s - 2 * x) / x).max())
                else:
                    u = np.minimum(u, (2 * x - s) / npl)
            tot = sum((row[p] for p in A), np.zeros(3))
            u = np.minimum(u, (4 * x - tot) / len(P)); u = np.minimum(u, x)
            worst = max(worst, (-u / x).max())
            cost = (x - np.maximum(u, 0)).sum()
            worst = max(worst, cost - tau)
            best.append((worst, sh, tuple(names[a] for a in asg)))
        best.sort(key=lambda t: t[0]); out += best[:top]
    out.sort(key=lambda t: t[0])
    return out


if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); v = d['v']
    x = np.array([v['x0'], v['x1'], v['x2']], float); tau = float(v['tau'])
    R = roles_from(v)
    if len(sys.argv) > 2: R = {k: R[k] for k in sys.argv[2].split(',')}
    # dedupe identical roles
    U = {}
    for k, c in R.items():
        if not any(np.allclose(c, c2) for c2 in U.values()): U[k] = c
    print('x', x.round(4), 'tau', round(tau, 4), 'roles', {k: c.round(4).tolist() for k, c in U.items()})
    for m in rt_margins(U, x, tau, top=3)[:12]:
        print('%.5f %s %s' % m)
