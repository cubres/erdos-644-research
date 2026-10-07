"""Exact (Fractions) re-check of a bal_adv.py adversary.  usage: python3 bal_verify.py adv.json
1. rationalise (limit_denominator 10^7) and restore equalities (unit mass on the largest free coordinate; minimiser
   coordinate = sigma); 2. check every hypothesis of the separated case-(A) model EXACTLY (no tolerance except the
   stated strict margins); 3. evaluate template badness exactly over the full menu: Fano with ANY assignment of the
   valid roles (DFS), 42 two-type functions, L5/T3, K4; 4. report min badness (> 0 means every template fails)."""
import sys, json, itertools
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from bal_adv import LINES, TTF

Q = lambda v: F(v).limit_denominator(10 ** 7)


def ev(expr, env):
    return sum(F(v).limit_denominator(10 ** 9) * (env[k] if k != 'c' else 1) for k, v in expr.items())


def rationalise(sol):
    x = [Q(v) for v in sol['x']]; sg = [Q(v) for v in sol['sigma']]; tau = Q(sol['tau'])
    roles = []
    for k, (r, spec, y) in enumerate(zip(sol['roles'], sol['spec'], sol['Y'])):
        c = [Q(v) for v in r]
        fixed = None
        if spec['kind'] == 'min':
            fixed = spec['cls']; c[fixed] = sg[fixed]
        j = max((i for i in range(3) if i != fixed), key=lambda i: c[i])
        c[j] = 1 - sum(c[i] for i in range(3) if i != j)
        roles.append(c)
    return x, sg, tau, roles


def check(sol, sep=True):
    if sol.get('mode') == 'gen':
        return check_gen(sol)
    x, sg, tau, roles = rationalise(sol)
    errs = []
    eta = F(sol['eta']).limit_denominator(10 ** 6)
    if not tau > F(3, 4): errs.append('tau')
    for i in range(3):
        if not (sg[i] > 2 * x[i] / 3 and sg[i] <= x[i]): errs.append('sigma%d' % i)
        if not x[i] - sg[i] > tau - F(3, 4) - F(1, 10 ** 6): errs.append('e%d>eta' % i)
    if sep:
        for i, j in itertools.combinations(range(3), 2):
            if x[i] + x[j] < F(3, 2) - F(1, 10 ** 7): errs.append('sep%d%d' % (i, j))
    if not sum(x) - sum(sg) >= tau: errs.append('E>=tau')
    env = {'tau': tau}
    for i in range(3):
        env['x%d' % i] = x[i]; env['s%d' % i] = sg[i]
    for k, c in enumerate(roles):
        for i in range(3): env['r%d_%d' % (k, i)] = c[i]
    valid = []
    for k, (c, spec, y) in enumerate(zip(roles, sol['spec'], sol['Y'])):
        if sum(c) != 1 or any(v < 0 or v > x[i] for i, v in enumerate(c)): errs.append('role%d unit/cap %s' % (k, [float(v) for v in c]))
        cls = y.index(1)
        if not c[cls] >= sg[cls]: errs.append('role%d class' % k)
        if spec['kind'] == 'min' and not (cls == spec['cls'] and c[cls] == sg[cls]): errs.append('role%d min' % k)
        v = True
        if spec['kind'] == 'req':
            u = [max(F(0), min([ev(e, env) for e in spec['u'][i]] + [x[i]])) for i in range(3)]
            cost = sum(x) - sum(u)
            if sol['Q'][k] == 1:
                if not cost <= tau: errs.append('role%d valid but cost %s > tau' % (k, float(cost - tau)))
                if not all(c[i] <= u[i] for i in range(3)): errs.append('role%d answer not in box %s' % (k, [float(c[i] - u[i]) for i in range(3)]))
            else:
                v = False
                if not cost > tau: errs.append('role%d void but cost <= tau' % k)
        valid.append(v)
    return errs, (x, sg, tau, roles, valid)


def check_gen(sol):
    """general case (A): x, sigma, t, tau; roles with super-heavy/blocked flags; blockers; requests"""
    x = [Q(v) for v in sol['x']]; sg = [Q(v) for v in sol['sigma']]; tau = Q(sol['tau']); t = [Q(v) for v in sol['t']]
    roles = []
    for k, (r, spec) in enumerate(zip(sol['roles'], sol['spec'])):
        c = [Q(v) for v in r]; fixed = None
        if spec['kind'] == 'min': fixed = spec['cls']; c[fixed] = sg[fixed]
        if spec['kind'] == 'blk': fixed = spec['facet']; c[fixed] = t[fixed]
        j = max((i for i in range(3) if i != fixed), key=lambda i: c[i])
        c[j] = 1 - sum(c[i] for i in range(3) if i != j)
        roles.append(c)
    errs = []
    eta = tau - F(3, 4)
    if not tau > F(3, 4): errs.append('tau')
    for i in range(3):
        if not (sg[i] > 2 * x[i] / 3 and sg[i] <= t[i] <= x[i]): errs.append('sigma/t %d' % i)
        if not x[i] - t[i] > eta - F(1, 10 ** 6): errs.append("e'%d>eta" % i)
        if not x[i] > 2 * eta: errs.append('TP%d' % i)
    if not sum(x) - sum(t) >= tau - F(1, 10 ** 9): errs.append('cost(t)>=tau')
    env = {'tau': tau}
    for i in range(3):
        env['x%d' % i] = x[i]; env['s%d' % i] = sg[i]; env['t%d' % i] = t[i]
    for k, c in enumerate(roles):
        for i in range(3): env['r%d_%d' % (k, i)] = c[i]
    valid = []
    for k, (c, spec) in enumerate(zip(roles, sol['spec'])):
        if sum(c) != 1 or any(v < 0 or v > x[i] for i, v in enumerate(c)): errs.append('role%d unit/cap' % k)
        heavy = [c[i] > 2 * x[i] / 3 for i in range(3)]
        if not any(heavy): errs.append('role%d light everywhere' % k)
        for i in range(3):
            if heavy[i] and c[i] < sg[i]: errs.append('role%d in S_%d below sigma' % (k, i))
        if not any(c[i] >= t[i] for i in range(3)): errs.append('role%d not blocked by t' % k)
        if spec['kind'] == 'min' and not (heavy[spec['cls']] and c[spec['cls']] == sg[spec['cls']]): errs.append('role%d min' % k)
        if spec['kind'] == 'blk':
            i = spec['facet']
            if not (c[i] == t[i] and all(c[j] < t[j] for j in range(3) if j != i)): errs.append('role%d blk (strict)' % k)
        v = True
        if spec['kind'] == 'req':
            u = [max(F(0), min([ev(e, env) for e in spec['u'][i]] + [x[i]])) for i in range(3)]
            cost = sum(x) - sum(u)
            if sol['Q'][k] == 1:
                if not cost <= tau: errs.append('role%d valid but cost > tau' % k)
                if not all(c[i] <= u[i] for i in range(3)): errs.append('role%d answer not in box' % k)
            else:
                v = False
                if not cost > tau: errs.append('role%d void but cost <= tau' % k)
        valid.append(v)
    return errs, (x, sg, tau, roles, valid)


def fano_best(Rs, x):
    """exact min over ALL assignments of rows to the 7 points of the max violation (line - 2x, total - 4x);
    branch and bound with the current best as bound.  Returns (value, assignment)."""
    n = len(Rs)
    best = [None, None]
    assign = [None] * 7
    by_last = {}
    for l in LINES: by_last.setdefault(max(l), []).append(l)

    def rec(k, tot, worst):
        if best[0] is not None and worst >= best[0]:
            return
        if k == 7:
            w = max(worst, max(tot[i] - 4 * x[i] for i in range(3)))
            if best[0] is None or w < best[0]:
                best[0] = w; best[1] = tuple(assign)
            return
        for idx in range(n):
            c = Rs[idx]; assign[k] = idx
            w = worst
            for l in by_last.get(k, []):
                for i in range(3):
                    w = max(w, Rs[assign[l[0]]][i] + Rs[assign[l[1]]][i] + Rs[assign[l[2]]][i] - 2 * x[i])
            rec(k + 1, [tot[i] + c[i] for i in range(3)], w)
        assign[k] = None
    rec(0, [F(0)] * 3, F(-10))
    return best[0], best[1]


def badness(x, tau, roles, valid):
    Rs = [roles[j] for j in range(len(roles)) if valid[j]]
    idx = [j for j in range(len(roles)) if valid[j]]
    # dedupe
    uniq = []; uidx = []
    for j, c in zip(idx, Rs):
        if c not in uniq: uniq.append(c); uidx.append(j)
    res = {}
    fb, fa = fano_best(uniq, x)
    res['F'] = (fb, tuple(uidx[a] for a in fa) if fa else None)
    best = (F(10), None)
    for a in range(len(uniq)):
        for b in range(len(uniq)):
            if a == b: continue
            for fn, vs in enumerate(TTF):
                w = max(u * uniq[a][i] + v * uniq[b][i] - x[i] for i in range(3) for u, v in vs)
                if w < best[0]: best = (w, ('TT', uidx[a], uidx[b], fn))
    res['TT'] = best
    best = (F(10), None)
    for a, b, c in itertools.combinations_with_replacement(range(len(uniq)), 3):
        A, B, C = uniq[a], uniq[b], uniq[c]
        w = max(A[i] + B[i] + C[i] - 2 * x[i] for i in range(3))
        cost = sum(max(A[i], B[i], C[i], (A[i] + B[i] + C[i]) / 2) for i in range(3)) / 2
        w = max(w, cost - tau)
        if w < best[0]: best = (w, ('T3', uidx[a], uidx[b], uidx[c]))
    res['T3'] = best
    best = (F(10), None)
    for g in range(len(uniq)):
        for a, b, c in itertools.combinations([j for j in range(len(uniq)) if j != g], 3):
            w = F(-10)
            for i in range(3):
                A, B, C = uniq[a][i], uniq[b][i], uniq[c][i]
                w = max(w, A - B - C, B - A - C, C - A - B, uniq[g][i] + (A + B + C) / 2 - x[i])
            if w < best[0]: best = (w, ('K4', uidx[g], uidx[a], uidx[b], uidx[c]))
    res['K4'] = best
    return res


if __name__ == '__main__':
    sol = json.load(open(sys.argv[1]))
    errs, (x, sg, tau, roles, valid) = check(sol)
    print('exact hypothesis errors:', errs if errs else 'NONE')
    print('x', [float(v) for v in x], 'N %.5f tau %.5f' % (float(sum(x)), float(tau)), 'sigma-2x/3', [float(sg[i] - 2 * x[i] / 3) for i in range(3)],
          'e', [float(x[i] - sg[i]) for i in range(3)])
    if sol.get('mode') == 'gen': print('t', [float(v) for v in sol['t']], "e'", [float(x[i]) - sol['t'][i] for i in range(3)])
    for k, (c, spec, v) in enumerate(zip(roles, sol['spec'], valid)):
        print(' role', k, spec.get('tag', spec['kind']), spec.get('cls', spec.get('facet', '')), [round(float(a), 5) for a in c], 'Y', sol['Y'][k], 'W', sol['W'][k] if 'W' in sol else '', '' if v else 'VOID')
    res = badness(x, tau, roles, valid)
    for k, (w, arg) in res.items():
        print(' %s: min violation %.6f at %s' % (k, float(w), arg))
    print('OVERALL badness (min over menu):', float(min(w for w, _ in res.values())))
