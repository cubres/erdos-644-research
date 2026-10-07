"""MILP adversary: search parameters (x, sigma, tau) and role types that satisfy the balanced-regime consequences
of tau*>3/4 but defeat every template among the role types.  Infeasible => the strategy (roles + templates)
provably works (modulo exact re-verification).  Roles: list of dicts {'kind': 'min', 'cls': i} (class-i minimiser),
{'kind':'vert','z':z} (type with t_z <= x_z - tau), {'kind':'free'} (arbitrary type satisfying regime), plus
optional extra linear constraints supplied as callables."""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
class Model:
    def __init__(s):
        s.nv = 0; s.lb = []; s.ub = []; s.integ = []; s.rows = []; s.lo = []; s.hi = []; s.names = []
    def var(s, lb=0.0, ub=10.0, integer=False, name=''):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.names.append(name); s.nv += 1
        return s.nv - 1
    def add(s, coefs, lo=-np.inf, hi=np.inf):
        s.rows.append(coefs); s.lo.append(lo); s.hi.append(hi)
    def solve(s, time_limit=120):
        A = np.zeros((len(s.rows), s.nv))
        for k, r in enumerate(s.rows):
            for j, c in r.items(): A[k, j] += c
        res = milp(c=np.zeros(s.nv), constraints=LinearConstraint(A, s.lo, s.hi), integrality=np.array(s.integ),
                   bounds=Bounds(s.lb, s.ub), options={'time_limit': time_limit, 'disp': False})
        return res
M = 20.0
def build(roles, templates=("T", "V", "MP"), eta=1e-7, eta2=1e-6, xmax=1.5, extra=None, pure_class=False):
    m = Model()
    x = [m.var(0.0, xmax, name=f'x{i}') for i in range(3)]
    sg = [m.var(0.0, 1.0, name=f's{i}') for i in range(3)]
    tau = m.var(0.75 + eta, 3.0, name='tau')
    for i in range(3):
        m.add({sg[i]: 1, x[i]: -2/3}, lo=0)          # sigma >= 2x/3
        m.add({sg[i]: 1, x[i]: -1}, hi=0)            # sigma <= x
    for i, j in itertools.combinations(range(3), 2):
        m.add({x[i]: 1, sg[i]: -1, x[j]: 1, sg[j]: -1}, hi=0.75)   # e_i+e_j <= 3/4
    d = {tau: 1}
    for i in range(3): d[x[i]] = d.get(x[i], 0) - 1; d[sg[i]] = d.get(sg[i], 0) + 1
    m.add(d, hi=0)                                     # tau <= sum e
    for i in range(3): m.add({tau: 1, x[i]: -1, sg[i]: 1}, hi=0.75)   # tau <= 3/4 + e_i
    T = []
    for r in roles:
        t = [m.var(0.0, 1.0, name=f't{len(T)}_{i}') for i in range(3)]
        m.add({t[0]: 1, t[1]: 1, t[2]: 1}, lo=1, hi=1)
        z = [m.var(0, 1, integer=True) for i in range(3)]
        for i in range(3):
            m.add({t[i]: 1, x[i]: -1}, hi=0)
            m.add({t[i]: 1, sg[i]: -1, z[i]: -M}, lo=-M)          # z=1 => t_i >= sigma_i
            m.add({t[i]: 1, x[i]: -2/3, z[i]: -M}, hi=0)           # z=0 => t_i <= 2x_i/3
        m.add({z[0]: 1, z[1]: 1, z[2]: 1}, lo=1)
        if pure_class: m.add({z[0]: 1, z[1]: 1, z[2]: 1}, hi=1)
        if r['kind'] == 'min':
            c = r['cls']; m.add({z[c]: 1}, lo=1); m.add({t[c]: 1, sg[c]: -1}, hi=0)
        elif r['kind'] == 'vert':
            # request u = x - min(tau, x_z) e_z (cost <= tau): t_z <= max(0, x_z - tau)
            zz = r['z']; q = m.var(0, 1, integer=True)
            m.add({t[zz]: 1, x[zz]: -1, tau: 1, q: -M}, hi=0)      # q=0 => t_z <= x_z - tau
            m.add({t[zz]: 1, q: M}, hi=M)                            # q=1 => t_z <= 0
        elif r['kind'] == 'priv':
            # request (x_X - delta, sigma_Y-, sigma_Z-), delta = tau - e_Y - e_Z: witness in S_X only
            X = r['cls']; Y, Z = [k for k in range(3) if k != X]
            m.add({z[X]: 1}, lo=1); m.add({z[Y]: 1}, hi=0); m.add({z[Z]: 1}, hi=0)
            # t_X <= x_X - tau + (x_Y - s_Y) + (x_Z - s_Z)
            m.add({t[X]: 1, x[X]: -1, tau: 1, x[Y]: -1, sg[Y]: 1, x[Z]: -1, sg[Z]: 1}, hi=0)
        elif r['kind'] == 'cls':
            m.add({z[r['cls']]: 1}, lo=1)
        T.append(t)
    def fail_any(lins):
        """at least one of the linear forms (dict, rhs) must satisfy form > rhs (form >= rhs+eta2)"""
        bs = [m.var(0, 1, integer=True) for _ in lins]
        m.add({b: 1 for b in bs}, lo=1)
        for b, (form, rhs) in zip(bs, lins):
            f = dict(form); f[b] = f.get(b, 0) - M
            m.add(f, lo=rhs + eta2 - M)
    n = len(T)
    def lin(*terms):
        f = {}
        for c, v in terms: f[v] = f.get(v, 0) + c
        return f
    if 'T' in templates:
        for a, b, c in itertools.product(range(n), repeat=3):
            L = []
            for i in range(3):
                A, Bv, Cv = T[a][i], T[b][i], T[c][i]
                L.append((lin((2, A), (1, Bv), (-2, x[i])), 0))
                L.append((lin((2, A), (1, Cv), (-2, x[i])), 0))
                L.append((lin((2, Bv), (1, Cv), (-2, x[i])), 0))
                L.append((lin((4, A), (2, Bv), (1, Cv), (-4, x[i])), 0))
            fail_any(L)
    if 'V' in templates:
        for s_, t_ in itertools.permutations(range(n), 2):
            L = []
            for i in range(3):
                L.append((lin((1, T[s_][i]), (1, T[t_][i]), (-1, x[i])), 0))
                L.append((lin((1.25, T[s_][i]), (0.5, T[t_][i]), (-1, x[i])), 0))
            fail_any(L)
    if 'MP' in templates:
        for b, c in itertools.product(range(n), repeat=2):
            L = []
            for i in range(3):
                L.append((lin((2, T[b][i]), (1, T[c][i]), (-2, x[i])), 0))
            for S in itertools.chain.from_iterable(itertools.combinations(range(3), k) for k in (1, 2, 3)):
                f = [(-4, tau)]
                for i in S: f += [(1, T[c][i]), (-2, T[b][i])]
                L.append((lin(*f), -3))           # sum_S (c-2b) - 4tau > -3  <=> 3/4 + sum/4 > tau
            fail_any(L)
    if extra: extra(m, x, sg, tau, T)
    return m, x, sg, tau, T
def run(roles, **kw):
    m, x, sg, tau, T = build(roles, **kw)
    res = m.solve(kw.get('time_limit', 300) if False else 300)
    if res.x is None: return res.status, res.message, None
    X = res.x
    sol = {'x': [X[v] for v in x], 'sigma': [X[v] for v in sg], 'tau': X[tau], 'T': [[X[v] for v in t] for t in T]}
    return res.status, res.message, sol
if __name__ == '__main__':
    import sys, json
    roles = [{'kind': 'min', 'cls': i} for i in range(3)]
    st, msg, sol = run(roles)
    print(st, msg); print(json.dumps(sol))
