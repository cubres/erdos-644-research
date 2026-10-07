"""Exact (Fractions) re-verification of an adversary configuration produced by roles3.py, plus inspection.
usage: python3 verify_adv.py adv.json [order|-]
Checks (exactly, after rationalisation with equalities restored): unit/capacity, super-heavy dichotomy w.r.t. sigma,
identity map sum e >= tau, window box (t >= 4x/7, cost >= tau), blockers (b^i_i = t_i, b^i_j < t_j / <= 4x_j/7),
requests (validity <=> cost <= tau; answer <= u).  Template badness (float, all Fano assignments, V, 42 TT, K4)
must be >= 1e-4 (normalised).  Then: tau*(roles) and cheapest escape box (a request nobody answers)."""
import sys, json, itertools
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from tc3lib import tau_star, LINES
from roles3 import load_tt, DT

Q = lambda v: Fr(v).limit_denominator(10 ** 7)
TOL = Fr(1, 10 ** 6)


def ge(a, b):
    return a >= b - TOL


def le(a, b):
    return a <= b + TOL



def rationalise(sol):
    x = [Q(v) for v in sol['x']]; tau = Q(sol['tau']); t = [Q(v) for v in sol['t']]; sg = [Q(v) for v in sol['sigma']]
    roles = []
    for k, (r, spec) in enumerate(zip(sol['roles'], sol['spec'])):
        c = [Q(v) for v in r]
        fixed = None
        if spec['kind'] == 'blk':
            fixed = spec['facet']; c[fixed] = t[fixed]
        elif spec['kind'] == 'min':
            fixed = spec['cls']; c[fixed] = sg[fixed]
        # restore unit mass on the largest non-fixed coordinate
        j = max((i for i in range(3) if i != fixed), key=lambda i: c[i])
        c[j] = 1 - sum(c[i] for i in range(3) if i != j)
        roles.append(c)
    return x, sg, tau, t, roles


def ev(expr, env):
    return sum(Fr(v) * (env[k] if k != 'c' else 1) for k, v in expr.items())


def check(sol, order=None, etas=Fr(1, 1000), verbose=True):
    x, sg, tau, t, roles = rationalise(sol)
    env = {'tau': tau}
    for i in range(3):
        env['x%d' % i] = x[i]; env['s%d' % i] = sg[i]; env['t%d' % i] = t[i]
    for k, c in enumerate(roles):
        for i in range(3): env['r%d_%d' % (k, i)] = c[i]
        env['q%d' % k] = Fr(1) if (sol['Q'][k] is None or sol['Q'][k] == 1) else Fr(0)
    errs = []
    N = sum(x)
    if not tau > Fr(3, 4): errs.append('tau')
    for i in range(3):
        if not (ge(sg[i] - 2 * x[i] / 3, etas) and le(sg[i], x[i])): errs.append('sigma%d' % i)
    if not ge(sum(x) - sum(sg), tau): errs.append('identity map')
    for i in range(3):
        lowb = sg[i] if sol.get('box') == 'sigma' else 4 * x[i] / 7
        if not (ge(t[i], lowb) and le(t[i], x[i])): errs.append('t%d range' % i)
    if not ge(N - sum(t), tau): errs.append('box cost')
    Z = sol['Z']; Qv = sol['Q']
    for k, (c, spec) in enumerate(zip(roles, sol['spec'])):
        if sum(c) != 1 or any(v < -TOL or v > x[i] + TOL for i, v in enumerate(c)): errs.append('role%d unit/cap' % k)
        for i in range(3):
            if Z[k][i]:
                if not ge(c[i], sg[i]): errs.append('role%d z%d' % (k, i))
            else:
                if not le(c[i], 2 * x[i] / 3): errs.append('role%d light%d' % (k, i))
        if not any(Z[k]): errs.append('role%d not superheavy' % k)
        kind = spec['kind']
        if kind == 'min':
            if not (Z[k][spec['cls']] and c[spec['cls']] == sg[spec['cls']]): errs.append('role%d min' % k)
        elif kind == 'blk':
            i = spec['facet']
            later = order[order.index(i) + 1:] if order else []
            for j in range(3):
                if j == i: continue
                if j in later:
                    if not le(c[j], 4 * x[j] / 7): errs.append('role%d blk later %d' % (k, j))
                else:
                    if not le(c[j], t[j] - Fr(DT).limit_denominator(10**7)): errs.append('role%d blk strict %d' % (k, j))
        elif kind == 'ureq':
            u = []
            for i in range(3):
                ex_ = spec['u'][i]
                if isinstance(ex_, dict): ex_ = [ex_]
                u.append(max(Fr(0), min([ev(e, env) for e in ex_] + [x[i]])))
            cost = sum(x[i] - u[i] for i in range(3))
            if Qv[k]:
                if not le(cost, tau): errs.append('role%d ureq valid but cost>tau' % k)
                if not all(le(c[i], u[i]) for i in range(3)): errs.append('role%d ureq answer' % k)
                done = []
                for i in spec.get('lex', []):
                    bound = x[i] - tau + sum(x[j] - (c[j] if j in done else u[j]) for j in range(3) if j != i)
                    if not le(c[i], bound): errs.append('role%d lex%d' % (k, i))
                    done.append(i)
            else:
                if not cost > tau - TOL: errs.append('role%d ureq invalid but cost<=tau' % k)
            if Qv[k] and spec.get('inclass') is not None and not Z[k][spec['inclass']]: errs.append('role%d inclass' % k)
            for e, lo, hi in spec.get('extra', ()):
                val = ev(e, env)
                if lo is not None and not ge(val, lo): errs.append('role%d extra lo' % k)
                if hi is not None and not le(val, hi): errs.append('role%d extra hi' % k)
        elif kind == 'req':
            u = [ev(e, env) for e in spec['u']]
            if spec.get('clip', True): u = [max(v, 0) for v in u]
            cost = sum(x[i] - u[i] for i in range(3))
            if Qv[k]:
                if not le(cost, tau): errs.append('role%d req valid but cost>tau' % k)
                if not all(le(c[i], u[i]) for i in range(3)): errs.append('role%d answer' % k)
            else:
                if not cost > tau - TOL: errs.append('role%d req invalid but cost<=tau' % k)
    if verbose:
        print('exact constraint errors:', errs if errs else 'NONE')
    return errs, (x, sg, tau, t, roles)


def badness(x, roles, valid, tt, menu=('F', 'V', 'TT', 'K4', 'T3'), maxk=3, tau=None):
    """min over templates of max normalised violation (float); > 0 means all fail.  Fano: <= maxk distinct roles."""
    from roles3 import PATS
    xv = np.array([float(v) for v in x]); R = np.array([[float(v) for v in c] for c in roles]); n = len(roles)
    idx = [j for j in range(n) if valid[j]]
    best = np.inf; arg = None
    if 'F' in menu:
        for k in range(1, maxk + 1):
            for combo in itertools.combinations(idx, k):
                for pat in PATS[k]:
                    pts = [combo[p] for p in pat]
                    w = -np.inf
                    for i in range(3):
                        z = R[pts, i]
                        w = max(w, (z.sum() - 4 * xv[i]) / xv[i])
                        for l in LINES:
                            w = max(w, (z[l[0]] + z[l[1]] + z[l[2]] - 2 * xv[i]) / xv[i])
                    if w < best: best, arg = w, ('F',) + tuple(pts)
    for a in idx:
        for b in idx:
            if a == b: continue
            if 'V' in menu:
                v = max(max(R[a, i] + R[b, i], 1.25 * R[a, i] + 0.5 * R[b, i]) / xv[i] - 1 for i in range(3))
                if v < best: best, arg = v, ('V', a, b)
            if 'TT' in menu:
                for fn, vs in enumerate(tt):
                    v = max((u * R[a, i] + w * R[b, i]) / xv[i] - 1 for i in range(3) for u, w in vs)
                    if v < best: best, arg = v, ('TT', a, b, fn)
    if 'T3' in menu and tau is not None:
        for a, b, c in itertools.combinations_with_replacement(idx, 3):
            S = R[a] + R[b] + R[c]
            v = np.max(S / xv - 2)
            Mx = np.maximum(np.maximum(R[a], R[b]), np.maximum(R[c], S / 2))
            v = max(v, Mx.sum() / 2 - float(tau))
            if v < best: best, arg = v, ('T3', a, b, c)
    if 'K4' in menu:
        for g in idx:
            for a, b, c in itertools.combinations([j for j in idx if j != g], 3):
                v = -np.inf
                for i in range(3):
                    A_, B_, C_ = R[a, i], R[b, i], R[c, i]
                    v = max(v, (A_ - B_ - C_) / xv[i], (B_ - A_ - C_) / xv[i], (C_ - A_ - B_) / xv[i],
                            (R[g, i] + 0.5 * (A_ + B_ + C_)) / xv[i] - 1)
                if v < best: best, arg = v, ('K4', g, a, b, c)
    return best, arg


def inspect(x, sg, tau, t, roles, valid):
    """report: tau*(roles) with the cheapest blocking map; distances."""
    K = [tuple(c) for c, v in zip(roles, valid) if v]
    ts, tt_ = tau_star(K, x, want=True)
    print('tau*(valid roles) = %.4f (tau = %.4f); cheapest block thresholds' % (float(ts), float(tau)),
          [None if v is None else round(float(v), 4) for v in tt_])
    return ts, tt_


if __name__ == '__main__':
    sol = json.load(open(sys.argv[1]))
    order = None
    if len(sys.argv) > 2 and sys.argv[2] != '-':
        order = tuple(int(c) for c in sys.argv[2])
    errs, (x, sg, tau, t, roles) = check(sol, order)
    valid = [q is None or q == 1 for q in sol['Q']]
    print('x', [round(float(v), 4) for v in x], 'N %.4f' % float(sum(x)), 'tau %.4f' % float(tau), 'sigma', [round(float(v), 4) for v in sg], 'e', [round(float(x[i] - sg[i]), 4) for i in range(3)])
    print('t', [round(float(v), 4) for v in t], 'cost %.4f' % float(sum(x) - sum(t)), '4x/7', [round(float(4 * v / 7), 4) for v in x], '2x/3', [round(float(2 * v / 3), 4) for v in x])
    for k, (c, spec, v) in enumerate(zip(roles, sol['spec'], valid)):
        print(' role', k, spec['kind'], spec.get('cls', spec.get('facet', '')), [round(float(a), 4) for a in c], 'Z', sol['Z'][k], '' if v else 'VOID')
    b, arg = badness(x, roles, valid, load_tt(), tau=tau)
    if sol.get('caseA'):
        blocked = [any(c[i] >= t[i] - TOL for i in range(3)) for c in roles]
        print('case A: roles blocked by t:', all(blocked), '' if all(blocked) else [k for k, bb in enumerate(blocked) if not bb])
    print('template badness (min over menu of max normalised violation): %.5f at %s' % (b, arg))
    inspect(x, sg, tau, t, roles, valid)
