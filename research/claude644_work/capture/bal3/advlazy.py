"""Lazy-template MILP adversary for the balanced 3-super-class regime (see advmilp.py for semantics).
Roles: 'min' (class minimiser), 'vert' (vertex V_z witness: t_z <= max(0,x_z - tau)),
'priv' (private-zone apex (delta_X,e_Y,e_Z)), 'edge' (edge point E_{X|Y}: t_X <= max(0, x_X - tau + e_Y), class Z),
'free' (any regime type).  Templates: T (a quad, b x2 pencil, c pencil), V(s,t), MP (b,b,c + requested quad).
Loop: solve, find templates feasible at the solution, add their failure disjunction, repeat."""
import itertools, numpy as np, sys, json
from scipy.optimize import milp, LinearConstraint, Bounds
M = 20.0
ETAS = 1e-3
class Model:
    def __init__(s):
        s.nv = 0; s.lb = []; s.ub = []; s.integ = []; s.rows = []; s.lo = []; s.hi = []; s.names = []
    def var(s, lb=0.0, ub=10.0, integer=False, name=''):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.names.append(name); s.nv += 1
        return s.nv - 1
    def add(s, coefs, lo=-np.inf, hi=np.inf):
        s.rows.append(coefs); s.lo.append(lo); s.hi.append(hi)
    def solve(s, time_limit=300):
        from scipy.sparse import lil_matrix
        A = lil_matrix((len(s.rows), s.nv))
        for k, r in enumerate(s.rows):
            for j, c in r.items(): A[k, j] += c
        return milp(c=np.zeros(s.nv), constraints=LinearConstraint(A.tocsr(), s.lo, s.hi), integrality=np.array(s.integ),
                    bounds=Bounds(s.lb, s.ub), options={'time_limit': time_limit, 'disp': False})
def lin(*terms):
    f = {}
    for c, v in terms: f[v] = f.get(v, 0) + c
    return f
class Adv:
    def __init__(s, roles, eta=1e-3, eta2=1e-4, tmpl=('T', 'V', 'MP'), xmin=0.0, unbal=None):
        s.m = m = Model(); s.eta2 = eta2; s.tmpl = tmpl
        s.x = x = [m.var(xmin, 1.5, name=f'x{i}') for i in range(3)]
        s.sg = sg = [m.var(0.0, 1.0, name=f's{i}') for i in range(3)]
        s.tau = tau = m.var(0.75 + eta, 3.0, name='tau')
        for i in range(3):
            m.add({sg[i]: 1, x[i]: -2/3}, lo=0); m.add({sg[i]: 1, x[i]: -1}, hi=0)
        if unbal is None:
            for i, j in itertools.combinations(range(3), 2):
                m.add({x[i]: 1, sg[i]: -1, x[j]: 1, sg[j]: -1}, hi=0.75)
        else:   # unbalanced: e_1 + e_2 >= 3/4 + unbal
            m.add({x[1]: 1, sg[1]: -1, x[2]: 1, sg[2]: -1}, lo=0.75 + unbal)
        d = {tau: 1}
        for i in range(3): d[x[i]] = -1; d[sg[i]] = 1
        m.add(d, hi=0)
        for i in range(3): m.add({tau: 1, x[i]: -1, sg[i]: 1}, hi=0.75)
        # class-level directional minima mu[X][Y] = inf{t_Y : t in S_X}; mu[X][X] = sigma_X
        s.mu = mu = [[(sg[X] if X == Y else m.var(0.0, 1.0, name=f'mu{X}{Y}')) for Y in range(3)] for X in range(3)]
        for X in range(3):
            for Y in range(3):
                if X != Y: m.add({mu[X][Y]: 1, x[Y]: -1}, hi=0)
        # every class-level blocking map (class X blocked at part pi[X]) costs >= tau, unless it blocks at a zero inf
        for pi in itertools.product(range(3), repeat=3):
            used = sorted(set(pi)); pre = {Y: [X for X in range(3) if pi[X] == Y] for Y in used}
            L = []
            for sel in itertools.product(*[pre[Y] for Y in used]):
                f = {tau: -1}
                for Y, X in zip(used, sel):
                    f[x[Y]] = f.get(x[Y], 0) + 1; f[mu[X][Y]] = f.get(mu[X][Y], 0) - 1
                L.append((f, 0))
            for X in range(3):
                if pi[X] != X: L.append(({mu[X][pi[X]]: -1}, -1e-7))      # mu <= 1e-7: map invalid
            bs = [m.var(0, 1, integer=True) for _ in L]; m.add({b: 1 for b in bs}, lo=1)
            for b, (f, r) in zip(bs, L):
                g = dict(f); g[b] = g.get(b, 0) - M; m.add(g, lo=r - M)
        s.T = []; s.Z = []; s.Q = []
        for r in roles:
            t = [m.var(0.0, 1.0) for i in range(3)]
            m.add({t[0]: 1, t[1]: 1, t[2]: 1}, lo=1, hi=1)
            z = [m.var(0, 1, integer=True) for i in range(3)]
            for i in range(3):
                m.add({t[i]: 1, x[i]: -1}, hi=0)
                m.add({t[i]: 1, sg[i]: -1, z[i]: -M}, lo=-M)     # z=1 => t_i >= sigma_i
                m.add({t[i]: 1, x[i]: -2/3, z[i]: -M}, hi=0)     # z=0 => t_i <= 2x_i/3
                m.add({t[i]: 1, x[i]: -2/3, z[i]: -M}, lo=ETAS - M)   # z=1 => t_i >= 2x_i/3 + ETAS (strict super-heavy)
            m.add({z[0]: 1, z[1]: 1, z[2]: 1}, lo=1)
            # class membership => traces >= class infima
            for X in range(3):
                for Y in range(3):
                    if X != Y: m.add({t[Y]: 1, mu[X][Y]: -1, z[X]: -M}, lo=-M)
            k = r['kind']
            if k == 'dmin':
                X, Y = r['cls'], r['dir']; m.add({z[X]: 1}, lo=1); m.add({t[Y]: 1, mu[X][Y]: -1}, hi=0)
            if k == 'min':
                c = r['cls']; m.add({z[c]: 1}, lo=1); m.add({t[c]: 1, sg[c]: -1}, hi=0)
            elif k == 'vert':
                zz = r['z']; q = m.var(0, 1, integer=True)
                m.add({t[zz]: 1, x[zz]: -1, tau: 1, q: -M}, hi=0); m.add({t[zz]: 1, q: M}, hi=M)
            elif k == 'priv':
                X = r['cls']; Y, Zc = [j for j in range(3) if j != X]
                m.add({z[X]: 1}, lo=1); m.add({z[Y]: 1}, hi=0); m.add({z[Zc]: 1}, hi=0)
                m.add({t[X]: 1, x[X]: -1, tau: 1, x[Y]: -1, sg[Y]: 1, x[Zc]: -1, sg[Zc]: 1}, hi=0)
            elif k == 'edge':
                X, Y = r['X'], r['Y']; Zc = 3 - X - Y
                m.add({z[X]: 1}, hi=0); m.add({z[Y]: 1}, hi=0); m.add({z[Zc]: 1}, lo=1)
                q = m.var(0, 1, integer=True)   # t_X <= max(0, x_X - tau + e_Y)
                m.add({t[X]: 1, x[X]: -1, tau: 1, x[Y]: -1, sg[Y]: 1, q: -M}, hi=0); m.add({t[X]: 1, q: M}, hi=M)
            qv = None
            if k == 'half':     # t <= x - T_j/2  (cost 1/2)
                j = r['of']
                for i in range(3): m.add({t[i]: 1, x[i]: -1, s.T[j][i]: 0.5}, hi=0)
            elif k == 'corner':  # corner of role j at its class X: t_X < sigma_X, t_Y <= x_Y - T_jY; valid iff cost<=tau
                j, X = r['of'], r['cls']; Y, Zc = [jj for jj in range(3) if jj != X]
                qv = m.var(0, 1, integer=True)
                # cost = T_jY + T_jZ + (x_X - sigma_X);  qv=1 => cost <= tau ; qv=0 => cost >= tau + 1e-6
                cst = {s.T[j][Y]: 1, s.T[j][Zc]: 1, x[X]: 1, sg[X]: -1, tau: -1}
                c1 = dict(cst); c1[qv] = M; m.add(c1, hi=M)
                c0 = dict(cst); c0[qv] = M; m.add(c0, lo=1e-6)
                # qv=1 => constraints
                m.add({z[X]: 1, qv: 1}, hi=1)
                for i in (Y, Zc):
                    m.add({t[i]: 1, x[i]: -1, s.T[j][i]: 1, qv: M}, hi=M)
            if k == 'lcorner':   # L+ corner of role j (class X) excluding class I: t_X<sigma_X, t_I<=min(x_I-a_I, sigma_I), t_J<=x_J-a_J
                j, X, I = r['of'], r['cls'], r['excl']; J = 3 - X - I
                qv = m.var(0, 1, integer=True)
                # cost1 = a_I + a_J + e_X ; cost2 = e_I + a_J + e_X ; valid iff both <= tau
                c1 = {s.T[j][I]: 1, s.T[j][J]: 1, x[X]: 1, sg[X]: -1, tau: -1}
                c2 = {x[I]: 1, sg[I]: -1, s.T[j][J]: 1, x[X]: 1, sg[X]: -1, tau: -1}
                for cc in (c1, c2):
                    f = dict(cc); f[qv] = f.get(qv, 0) + M; m.add(f, hi=M)
                bb = [m.var(0, 1, integer=True) for _ in range(2)]
                m.add({bb[0]: 1, bb[1]: 1, qv: 1}, lo=1)
                for b_, cc in zip(bb, (c1, c2)):
                    f = dict(cc); f[b_] = f.get(b_, 0) - M; m.add(f, lo=1e-6 - M)
                m.add({z[X]: 1, qv: 1}, hi=1); m.add({z[I]: 1, qv: 1}, hi=1)
                m.add({t[I]: 1, x[I]: -1, s.T[j][I]: 1, qv: M}, hi=M)
                m.add({t[J]: 1, x[J]: -1, s.T[j][J]: 1, qv: M}, hi=M)
            if k == 'escape':   # w escapes blocking map pi (dict role->part); valid iff cost(pi) <= tau
                pi = r['map']; used = sorted(set(pi.values()))
                qv = m.var(0, 1, integer=True)
                pre = {i: [j for j, p in pi.items() if p == i] for i in used}
                # qv=1 => for every selection, sum_i (x_i - T_sel(i),i) <= tau
                for sel in itertools.product(*[pre[i] for i in used]):
                    f = {tau: -1, qv: M}
                    for i, j in zip(used, sel):
                        f[x[i]] = f.get(x[i], 0) + 1; f[s.T[j][i]] = f.get(s.T[j][i], 0) - 1
                    m.add(f, hi=M)
                # qv=0 => some selection has sum >= tau + 1e-6
                sels = list(itertools.product(*[pre[i] for i in used]))
                bs = [m.var(0, 1, integer=True) for _ in sels]
                pairs = [(j, i) for i in used for j in pre[i]]
                bz = [m.var(0, 1, integer=True) for _ in pairs]
                for b, (j, i) in zip(bz, pairs):           # bz=1 => T_ji <= 2e-6 (map invalid there)
                    m.add({s.T[j][i]: 1, b: M}, hi=M + 2e-6)
                    m.add({s.T[j][i]: 1, qv: -2e-6, b: 0}, lo=0)
                for (j, i) in pairs: m.add({s.T[j][i]: 1, qv: -3e-6}, lo=0)   # qv=1 => T_ji >= 3e-6
                m.add(dict([(b, 1) for b in bs] + [(b, 1) for b in bz] + [(qv, 1)]), lo=1)
                for b, sel in zip(bs, sels):
                    f = {tau: -1, b: -M}
                    for i, j in zip(used, sel):
                        f[x[i]] = f.get(x[i], 0) + 1; f[s.T[j][i]] = f.get(s.T[j][i], 0) - 1
                    m.add(f, lo=1e-6 - M)
                # qv=1 => w_i <= T_ji - 1e-6 for j in pre[i]
                for i in used:
                    for j in pre[i]:
                        m.add({t[i]: 1, s.T[j][i]: -1, qv: M}, hi=M - 1e-6)
            s.T.append(t); s.Z.append(z); s.Q.append(qv)
        s.added = set()
    def fail_any(s, lins, key=None):
        m = s.m; bs = [m.var(0, 1, integer=True) for _ in lins]
        extra = {}
        if key is not None:
            for j in set(key[1:]):
                if s.Q[j] is not None: extra[s.Q[j]] = -1     # template void if role j invalid (qv=0)
        cons = {b: 1 for b in bs}; cons.update(extra)
        m.add(cons, lo=1 - len(extra))
        for b, (form, rhs) in zip(bs, lins):
            f = dict(form); f[b] = f.get(b, 0) - M
            m.add(f, lo=rhs + s.eta2 - M)
    def forms(s, key):
        x, tau, T = s.x, s.tau, s.T; L = []
        if key[0] == 'T':
            a, b, c = key[1:]
            for i in range(3):
                A, Bv, Cv = T[a][i], T[b][i], T[c][i]
                L += [(lin((2, A), (1, Bv), (-2, x[i])), 0), (lin((2, A), (1, Cv), (-2, x[i])), 0),
                      (lin((2, Bv), (1, Cv), (-2, x[i])), 0), (lin((4, A), (2, Bv), (1, Cv), (-4, x[i])), 0)]
        elif key[0] == 'V':
            a, b = key[1:]
            for i in range(3):
                L += [(lin((1, T[a][i]), (1, T[b][i]), (-1, x[i])), 0), (lin((1.25, T[a][i]), (0.5, T[b][i]), (-1, x[i])), 0)]
        elif key[0] == 'K4':   # 4-class template: g <= x - (fa+fb+fc)/2 and triangle inequalities fj <= fk + fl per part
            g, a, b, c = key[1:]
            for i in range(3):
                A_, B_, C_ = T[a][i], T[b][i], T[c][i]
                L += [(lin((1, A_), (-1, B_), (-1, C_)), 0), (lin((1, B_), (-1, A_), (-1, C_)), 0), (lin((1, C_), (-1, A_), (-1, B_)), 0),
                      (lin((1, T[g][i]), (0.5, A_), (0.5, B_), (0.5, C_), (-1, x[i])), 0)]
        elif key[0] == 'MP':
            b, c = key[1:]
            for i in range(3): L.append((lin((2, T[b][i]), (1, T[c][i]), (-2, x[i])), 0))
            for S in itertools.chain.from_iterable(itertools.combinations(range(3), k) for k in (1, 2, 3)):
                f = [(-4, tau)]
                for i in S: f += [(1, T[c][i]), (-2, T[b][i])]
                L.append((lin(*f), -3))
        return L
    def keys(s):
        n = len(s.T); K = []
        if 'T' in s.tmpl: K += [('T',) + k for k in itertools.product(range(n), repeat=3)]
        if 'V' in s.tmpl: K += [('V',) + k for k in itertools.permutations(range(n), 2)]
        if 'MP' in s.tmpl: K += [('MP',) + k for k in itertools.product(range(n), repeat=2)]
        if 'K4' in s.tmpl: K += [('K4', g) + k for g in range(n) for k in itertools.combinations(range(n), 3) if g not in k]
        return K
    def feasible_at(s, X, key):
        """template feasible at solution X (all forms <= rhs + tol)"""
        if any(s.Q[j] is not None and X[s.Q[j]] < 0.5 for j in set(key[1:])): return False
        return all(sum(c*X[v] for v, c in f.items()) <= r + s.eta2 for f, r in s.forms(key))
    def run(s, maxit=200, tl=300, verbose=True):
        for it in range(maxit):
            res = s.m.solve(tl)
            if res.x is None:
                return 'INFEASIBLE' if res.status == 2 else 'STATUS%d' % res.status, None
            X = res.x
            new = [k for k in s.keys() if k not in s.added and s.feasible_at(X, k)]
            if verbose: print(" it", it, "new templates", len(new), "total", len(s.added), flush=True)
            if not new:
                return 'ADVERSARY', {'x': [X[v] for v in s.x], 'sigma': [X[v] for v in s.sg], 'tau': X[s.tau],
                                     'T': [[X[v] for v in t] for t in s.T], 'Z': [[round(X[v]) for v in z] for z in s.Z]}
            for k in new:
                s.fail_any(s.forms(k), k); s.added.add(k)
        return 'MAXIT', None
def roles_from(spec):
    R = []
    for k in spec.split(','):
        if k == 'min': R += [{'kind': 'min', 'cls': i} for i in range(3)]
        if k == 'vert': R += [{'kind': 'vert', 'z': z} for z in range(3)]
        if k == 'priv': R += [{'kind': 'priv', 'cls': i} for i in range(3)]
        if k == 'edge': R += [{'kind': 'edge', 'X': X, 'Y': Y} for X, Y in itertools.permutations(range(3), 2)]
        if k == 'dmin': R += [{'kind': 'dmin', 'cls': X, 'dir': Y} for X, Y in itertools.permutations(range(3), 2)]
    # adaptive roles refer to minimiser roles (must be first three)
    for k in spec.split(','):
        if k == 'halfmin': R += [{'kind': 'half', 'of': i} for i in range(3)]
        if k == 'cornermin': R += [{'kind': 'corner', 'of': i, 'cls': i} for i in range(3)]
        if k == 'lcornermin': R += [{'kind': 'lcorner', 'of': X, 'cls': X, 'excl': I} for X in range(3) for I in range(3) if I != X]
    return R
if __name__ == '__main__':
    spec = sys.argv[1]; eta = float(sys.argv[2]); tm = tuple(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] != '-' else ('T', 'V', 'MP')
    ub = float(sys.argv[4]) if len(sys.argv) > 4 else None
    A = Adv(roles_from(spec), eta=eta, tmpl=tm, unbal=ub)
    st, sol = A.run()
    print(spec, eta, tm, st); print(json.dumps(sol))
    if sol:
        sys.path.insert(0, '.'); import blockmap
        print(" real tau* of roles:", blockmap.best_block(sol['x'], sol['T']))
