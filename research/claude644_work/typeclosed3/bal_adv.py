"""Fast MILP adversary for the SEPARATED regime of case (A) (x_i + x_j >= 3/2 for all pairs; Lemma SEP of notes_caseA.md):
classes S_0, S_1, S_2 disjoint, S_i = {c : c_i >= sigma_i}, sigma_i > 2x_i/3, box = sigma, blockers = minimisers,
E = sum e_i >= tau, e_i > eta.

Variables: x_i, sigma_i, tau; roles c^r (unit, 0 <= c <= x) with ONE class binary y^r_i (y=1 => c_i >= sigma_i).
Role kinds:
  {'kind':'min','cls':i}                     class minimiser (c_i = sigma_i, class i)
  {'kind':'free'}                            any type
  {'kind':'req','u':[[expr..],[expr..],[expr..]], 'force':bool}
        request: u_i = max(0, min(exprs + [x_i])); valid (q=1) iff cost = sum(x_i - u_i) <= tau; then c <= u.
        q=0 => cost >= tau + DQ.  'force' => q = 1 (only when validity is proved by hand).
  {'kind':'mono','cls':i}                    Corollary C window: a box w with cost(w) <= 3/4 + MONO_EPS containing this
        role (class i) and NO role of another class (disjunction per role).
expr: dict name -> coef over 'x0'..,'s0'..,'tau','r<k>_<i>','c'.
Templates (failure disjunctions with SHARED indicator binaries, strictness BETA absolute):
  'F'  Fano assignment of roles to the 7 points (<= FK distinct roles);  'TT' 42 two-type functions (incl. V);
  'T3' L5 line-pencil (3 rows on a line, 4 requested quad rows);  'K4'.
"""
import itertools, json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
M = 8.0
DQ = 1e-6


def fano_autos():
    Ls = set(frozenset(l) for l in LINES); out = []
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[q] for q in l) in Ls for l in LINES):
            out.append(p)
    return out


def pattern_reps(k, autos):
    seen = set(); reps = []
    for pat in itertools.product(range(k), repeat=7):
        if len(set(pat)) != k or pat in seen:
            continue
        # canonical relabelling not needed: combos are unordered sets but patterns are over ordered labels, keep all
        orb = set(tuple(pat[a[q]] for q in range(7)) for a in autos)
        seen |= orb; reps.append(pat)
    return reps


AUT = fano_autos()
PATS = {k: pattern_reps(k, AUT) for k in (1, 2, 3, 4, 5, 6, 7)}


def load_tt():
    from fractions import Fraction as Fr
    fn = '/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'
    d = json.load(open(fn))
    return [[(Fr(u), Fr(v)) for u, v in d[k]['record']['vertices']] for k in sorted(d, key=int)]


TTF = load_tt()
TT = [[(float(u), float(v)) for u, v in vs] for vs in TTF]


class Model:
    def __init__(s):
        s.lb = []; s.ub = []; s.integ = []; s.names = []
        s.ri = []; s.rj = []; s.rv = []; s.lo = []; s.hi = []; s.nr = 0

    def var(s, lb=0.0, ub=10.0, integer=False, name=''):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.names.append(name)
        return len(s.lb) - 1

    def add(s, coefs, lo=-np.inf, hi=np.inf):
        for j, c in coefs.items():
            if c != 0:
                s.ri.append(s.nr); s.rj.append(j); s.rv.append(c)
        s.lo.append(lo); s.hi.append(hi); s.nr += 1

    def solve(s, tl=600, obj=None):
        A = coo_matrix((s.rv, (s.ri, s.rj)), shape=(s.nr, len(s.lb))).tocsr()
        c = np.zeros(len(s.lb))
        if obj:
            for j, v in obj.items(): c[j] = v
        return milp(c=c, constraints=LinearConstraint(A, s.lo, s.hi), integrality=np.array(s.integ),
                    bounds=Bounds(s.lb, s.ub), options={'time_limit': tl, 'disp': False, 'mip_rel_gap': 1e-4})


def lin(*pairs):
    d = {}
    for coefs in pairs:
        for j, c in coefs.items():
            d[j] = d.get(j, 0) + c
    return d


class BalAdv:
    def __init__(s, roles, eta=1e-2, beta=1e-3, etas=1e-3, xmin=0.75, sep=True, fk=4, menu=('F', 'TT', 'T3', 'K4'),
                 mono_eps=1e-3, xmax=1.5, extra=(), sepmargin=0.0):
        s.m = m = Model(); s.beta = beta; s.fk = fk; s.menu = menu; s.roles = roles
        s.eta = eta; s.etas = etas
        s.x = x = [m.var(xmin, xmax, name='x%d' % i) for i in range(3)]
        s.sg = sg = [m.var(0.0, 1.0, name='s%d' % i) for i in range(3)]
        s.tau = tau = m.var(0.75 + eta, 3.0, name='tau')
        s.names = {'tau': tau}
        for i in range(3):
            s.names['x%d' % i] = x[i]; s.names['s%d' % i] = sg[i]
            m.add({sg[i]: 1, x[i]: -2 / 3}, lo=etas)                  # sigma_i >= 2x_i/3 + etas
            m.add({sg[i]: 1, x[i]: -1}, hi=-eta)                      # e_i >= eta (Corollary C; strict in truth)
        if sep:
            for i, j in itertools.combinations(range(3), 2):
                m.add({x[i]: 1, x[j]: 1}, lo=1.5 + sepmargin)
        m.add({x[0]: 1, x[1]: 1, x[2]: 1, sg[0]: -1, sg[1]: -1, sg[2]: -1, tau: -1}, lo=0)   # E >= tau
        s.T = []; s.Y = []; s.Q = []; s.kind = []
        for k, r in enumerate(roles):
            s.add_role(k, r)
        for e in extra:
            f, c = s.ex(e[0]); m.add(f, lo=(e[1] - c) if e[1] is not None else -np.inf, hi=(e[2] - c) if e[2] is not None else np.inf)
        s.added = set()
        s.Lind = {}      # (multiset triple, part) -> binary : line sum >= 2x + beta
        s.Pind = {}      # (a, b, part, u, v) -> binary : u a_i + v b_i >= x_i + beta

    def ex(s, expr):
        f = {}; const = 0.0
        for k, v in expr.items():
            if k == 'c':
                const += v
            else:
                j = s.names[k]; f[j] = f.get(j, 0) + v
        return f, const

    def add_role(s, k, r):
        m = s.m; x = s.x; sg = s.sg; tau = s.tau
        c = [m.var(0.0, 1.5, name='r%d_%d' % (k, i)) for i in range(3)]
        for i in range(3):
            s.names['r%d_%d' % (k, i)] = c[i]
            m.add({c[i]: 1, x[i]: -1}, hi=0)
        m.add({c[0]: 1, c[1]: 1, c[2]: 1}, lo=1, hi=1)
        y = [m.var(0, 1, integer=True, name='y%d_%d' % (k, i)) for i in range(3)]
        m.add({y[0]: 1, y[1]: 1, y[2]: 1}, lo=1, hi=1)
        for i in range(3):
            m.add({c[i]: 1, sg[i]: -1, y[i]: -M}, lo=-M)             # y_i = 1 => c_i >= sigma_i
        kind = r['kind']; qv = None
        if kind == 'min':
            i = r['cls']; m.add({y[i]: 1}, lo=1); m.add({c[i]: 1, sg[i]: -1}, lo=0, hi=0)
        elif kind == 'free':
            pass
        elif kind == 'req':
            qv = m.var(0, 1, integer=True, name='q%d' % k); s.names['q%d' % k] = qv
            cost = {tau: -1}
            for i in range(3):
                exprs = list(r['u'][i]) + [{'x%d' % i: 1}]
                u = m.var(0.0, 3.0, name='u%d_%d' % (k, i)); s.names['u%d_%d' % (k, i)] = u
                p0 = m.var(0, 1, integer=True)
                ps = [p0]; ns = []
                for e in exprs:
                    f, cc = s.ex(e)
                    g = lin({u: 1}, {j: -v for j, v in f.items()})
                    m.add(lin(g, {p0: -M}), hi=cc)                      # u <= expr + M p0
                    p = m.var(0, 1, integer=True); ps.append(p)
                    m.add(lin(g, {p: -M}), lo=cc - M)                   # p=1 => u >= expr
                    n = m.var(0, 1, integer=True); ns.append(n)
                    m.add(lin(f, {n: M}), hi=M - cc)                     # n=1 => expr <= 0
                    # answer: q=1 => c_i <= expr  (u <= expr when p0 = 0; if p0 = 1, u = 0 and c_i <= u below)
                m.add({u: 1, p0: M}, hi=M)                               # p0=1 => u <= 0
                m.add({p: 1 for p in ps}, lo=1)
                m.add(lin({p0: 1}, {n: -1 for n in ns}), hi=0)          # p0 => some expr <= 0
                m.add({c[i]: 1, u: -1, qv: M}, hi=M)                     # q=1 => c_i <= u_i
                cost = lin(cost, {x[i]: 1, u: -1})
            m.add(lin(cost, {qv: M}), hi=M)                              # q=1 => cost <= tau
            m.add(lin(cost, {qv: M}), lo=DQ)                             # q=0 => cost >= tau + DQ
            if r.get('force', False):
                m.add({qv: 1}, lo=1)
            if r.get('cls') is not None:
                m.add({y[r['cls']]: 1}, lo=1)
        elif kind == 'mono':
            pass   # handled after all roles exist (needs the other roles): see add_mono
        else:
            raise ValueError(kind)
        s.T.append(c); s.Y.append(y); s.Q.append(qv); s.kind.append(kind)

    def finalize(s):
        """mono roles: box w, cost <= 3/4 + mono_eps, contains the role, excludes every role of another class"""
        m = s.m; x = s.x
        for k, r in enumerate(s.roles):
            if r['kind'] != 'mono':
                continue
            i = r['cls']; c = s.T[k]; y = s.Y[k]
            m.add({y[i]: 1}, lo=1)
            w = [m.var(0.0, 1.5) for _ in range(3)]
            for j in range(3):
                m.add({w[j]: 1, x[j]: -1}, hi=0); m.add({c[j]: 1, w[j]: -1}, hi=0)
            m.add({x[0]: 1, x[1]: 1, x[2]: 1, w[0]: -1, w[1]: -1, w[2]: -1}, hi=0.75 + r.get('eps', 1e-3))
            for k2 in range(len(s.roles)):
                if k2 == k: continue
                # if role k2 is valid and of class != i, then some coordinate c^{k2}_j >= w_j + 1e-6
                bs = [m.var(0, 1, integer=True) for _ in range(3)]
                g = {b: 1 for b in bs}; g[s.Y[k2][i]] = 1
                if s.Q[k2] is not None:
                    g[s.Q[k2]] = -1; m.add(g, lo=0)                    # sum b + y_i >= q
                else:
                    m.add(g, lo=1)
                for j in range(3):
                    m.add({s.T[k2][j]: 1, w[j]: -1, bs[j]: -M}, lo=1e-6 - M)

    # ---------------- shared failure indicators ----------------
    def line_ind(s, trip, i):
        key = (tuple(sorted(trip)), i)
        if key not in s.Lind:
            b = s.m.var(0, 1, integer=True)
            a1, a2, a3 = key[0]
            f = lin({s.T[a1][i]: 1}, {s.T[a2][i]: 1}, {s.T[a3][i]: 1}, {s.x[i]: -2, b: -M})
            s.m.add(f, lo=s.beta - M)                                   # b=1 => sum >= 2x_i + beta
            s.Lind[key] = b
        return s.Lind[key]

    def tot_ind(s, seven, i):
        key = ('tot', tuple(sorted(seven)), i)
        if key not in s.Lind:
            b = s.m.var(0, 1, integer=True)
            f = {s.x[i]: -4, b: -M}
            for a in seven: f[s.T[a][i]] = f.get(s.T[a][i], 0) + 1
            s.m.add(f, lo=s.beta - M)
            s.Lind[key] = b
        return s.Lind[key]

    def pair_ind(s, a, b, i, u, v):
        key = (a, b, i, u, v)
        if key not in s.Pind:
            z = s.m.var(0, 1, integer=True)
            f = {s.x[i]: -1, z: -M}
            if u: f[s.T[a][i]] = f.get(s.T[a][i], 0) + u
            if v: f[s.T[b][i]] = f.get(s.T[b][i], 0) + v
            s.m.add(f, lo=s.beta - M)
            s.Pind[key] = z
        return s.Pind[key]

    def voiders(s, roles_used):
        out = {}
        for j in set(roles_used):
            if s.Q[j] is not None:
                out[s.Q[j]] = out.get(s.Q[j], 0) - 1
        return out

    def add_fail(s, key):
        m = s.m
        if key[0] == 'F':
            pts = key[1:]
            inds = []
            for i in range(3):
                for l in LINES:
                    inds.append(s.line_ind([pts[q] for q in l], i))
                inds.append(s.tot_ind(pts, i))
            g = {}
            for b in inds: g[b] = g.get(b, 0) + 1
            vd = s.voiders(pts); g = lin(g, vd)
            m.add(g, lo=1 + sum(vd.values()))
        elif key[0] == 'TT':
            a, b, fn = key[1:]
            g = {}
            for i in range(3):
                for u, v in TT[fn]:
                    z = s.pair_ind(a, b, i, u, v); g[z] = g.get(z, 0) + 1
            vd = s.voiders((a, b)); g = lin(g, vd)
            m.add(g, lo=1 + sum(vd.values()))
        elif key[0] == 'T3':
            a, b, c = key[1:]
            g = {}
            for i in range(3):
                z = s.line_ind([a, b, c], i); g[z] = g.get(z, 0) + 1
            # or cost >= tau + beta: sum_j mu_j/2 >= tau + beta, mu_j <= chosen term
            zc = m.var(0, 1, integer=True); g[zc] = g.get(zc, 0) + 1
            mus = []
            for i in range(3):
                mu = m.var(0.0, 3.0); mus.append(mu)
                ds = [m.var(0, 1, integer=True) for _ in range(4)]
                m.add({d: 1 for d in ds}, lo=1)
                A_, B_, C_ = s.T[a][i], s.T[b][i], s.T[c][i]
                terms = [{A_: 1}, {B_: 1}, {C_: 1}]
                terms.append(lin({A_: .5}, {B_: .5}, {C_: .5}))
                for d, tm in zip(ds, terms):
                    m.add(lin({mu: 1}, {j: -v for j, v in tm.items()}, {d: M}), hi=M)   # d=1 => mu <= term
            f = {s.tau: -1, zc: -M}
            for mu in mus: f[mu] = f.get(mu, 0) + 0.5
            m.add(f, lo=s.beta - M)
            vd = s.voiders((a, b, c)); g = lin(g, vd)
            m.add(g, lo=1 + sum(vd.values()))
        elif key[0] == 'K4':
            gg, a, b, c = key[1:]
            L = []
            for i in range(3):
                A_, B_, C_ = s.T[a][i], s.T[b][i], s.T[c][i]
                L += [({A_: 1, B_: -1, C_: -1}, None), ({B_: 1, A_: -1, C_: -1}, None), ({C_: 1, A_: -1, B_: -1}, None),
                      (lin({s.T[gg][i]: 1}, {A_: .5, B_: .5, C_: .5}, {s.x[i]: -1}), None)]
            bs = [m.var(0, 1, integer=True) for _ in L]
            for bb, (f, _) in zip(bs, L):
                m.add(lin(f, {bb: -M}), lo=s.beta - M)
            g = {bb: 1 for bb in bs}
            vd = s.voiders((gg, a, b, c)); g = lin(g, vd)
            m.add(g, lo=1 + sum(vd.values()))
        s.added.add(key)

    # ---------------- evaluation at a solution ----------------
    def values(s, X):
        xv = np.array([X[v] for v in s.x]); R = np.array([[X[v] for v in t] for t in s.T])
        valid = [s.Q[j] is None or X[s.Q[j]] > 0.5 for j in range(len(s.T))]
        return xv, R, valid

    def eval_templates(s, X, tol=None, limit=400):
        """templates feasible at X up to tolerance (violation < beta/2 absolute)"""
        tol = s.beta / 2 if tol is None else tol
        xv, R, valid = s.values(X)
        n = len(R)
        groups = {}
        for j in range(n):
            if valid[j]:
                groups.setdefault(tuple(np.round(R[j], 7)), []).append(j)
        reps = [g[0] for g in groups.values()]
        out = []
        if 'F' in s.menu:
            for k in range(1, s.fk + 1):
                if len(reps) < k: break
                combos = np.array(list(itertools.combinations(reps, k)))
                for pat in PATS[k]:
                    idx = combos[:, list(pat)]                     # (C,7)
                    Z = R[idx]                                      # (C,7,3)
                    ok = np.all(Z.sum(1) <= 4 * xv + tol, axis=1)
                    for l in LINES:
                        ok &= np.all(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] <= 2 * xv + tol, axis=1)
                    for r in np.nonzero(ok)[0]:
                        out.append(('F',) + tuple(int(v) for v in idx[r]))
                        if len(out) >= limit: return out
        if 'TT' in s.menu:
            for a in reps:
                for b in reps:
                    if a == b: continue
                    for fn, vs in enumerate(TT):
                        if all(u * R[a, i] + v * R[b, i] <= xv[i] + tol for i in range(3) for u, v in vs):
                            out.append(('TT', a, b, fn))
        if 'T3' in s.menu:
            tauv = X[s.tau]
            for a, b, c in itertools.combinations_with_replacement(reps, 3):
                S = R[a] + R[b] + R[c]
                if np.any(S > 2 * xv + tol): continue
                Mx = np.maximum(np.maximum(R[a], R[b]), np.maximum(R[c], S / 2))
                if Mx.sum() / 2 < tauv + tol:
                    out.append(('T3', a, b, c))
        if 'K4' in s.menu:
            for g in reps:
                for a, b, c in itertools.combinations([j for j in reps if j != g], 3):
                    ok = True
                    for i in range(3):
                        A_, B_, C_ = R[a, i], R[b, i], R[c, i]
                        if A_ > B_ + C_ + tol or B_ > A_ + C_ + tol or C_ > A_ + B_ + tol or R[g, i] + 0.5 * (A_ + B_ + C_) > xv[i] + tol:
                            ok = False; break
                    if ok: out.append(('K4', g, a, b, c))
        return out

    def run(s, maxit=300, tl=600, verbose=True, maxadd=200, logf=None):
        s.finalize()
        t0 = time.time()
        for it in range(maxit):
            res = s.m.solve(tl)
            if res.x is None:
                st = 'INFEASIBLE' if res.status == 2 else 'STATUS%d' % res.status
                msg = ' it %d %s templates %d (%.0fs)' % (it, st, len(s.added), time.time() - t0)
                if verbose: print(msg, flush=True)
                return st, None
            X = res.x
            new = [k for k in s.eval_templates(X) if k not in s.added]
            if verbose:
                print(' it', it, 'new', len(new), 'total', len(s.added), 'tau %.4f' % X[s.tau],
                      'x', np.round([X[v] for v in s.x], 4), 'binaries', sum(s.m.integ), '%.0fs' % (time.time() - t0), flush=True)
            if not new:
                return 'ADVERSARY', s.extract(X)
            for k in new[:maxadd]:
                s.add_fail(k)
        return 'MAXIT', None

    def extract(s, X):
        return {'x': [X[v] for v in s.x], 'sigma': [X[v] for v in s.sg], 'tau': X[s.tau],
                'roles': [[X[v] for v in t] for t in s.T], 'Y': [[int(round(X[v])) for v in y] for y in s.Y],
                'Q': [None if q is None else int(round(X[q])) for q in s.Q], 'spec': s.roles,
                'U': {nm: X[j] for nm, j in s.names.items() if nm.startswith('u')},
                'beta': s.beta, 'etas': s.etas, 'eta': s.eta}


# ---------------- role builders ----------------
def R(k, i):
    return 'r%d_%d' % (k, i)


def mins():
    return [{'kind': 'min', 'cls': i} for i in range(3)]


def req(u, **kw):
    d = {'kind': 'req', 'u': u}; d.update(kw); return d


def req_vertex(i):
    """u_i = x_i - 3/4 (others x): cost min(x_i, 3/4) <= 3/4 < tau: always valid"""
    u = [[] for _ in range(3)]; u[i] = [{'x%d' % i: 1, 'c': -0.75}]
    return req(u, force=True, tag='vert%d' % i)


def req_pencil(k):
    """f <= x - 3 g/4 for role g = k: cost 3/4 always valid"""
    u = [[{'x%d' % i: 1, R(k, i): -0.75}] for i in range(3)]
    return req(u, force=True, tag='pen%d' % k)


def req_mp(b, c):
    """MP(b,b,c) quad request (L5 with a = b): d <= x - max(b, c, (2b+c)/2)/2 ... here the Lemma 7.63 box"""
    u = [[{'x%d' % i: 1, R(b, i): -0.5, R(c, i): -0.25}, {'x%d' % i: 1, R(c, i): -0.5}] for i in range(3)]
    return req(u, tag='mp%d_%d' % (b, c))


def req_discard(a, c):
    """discard route: H <= min(2x - a - c, a + c) so that T3(a, c, H) has line sum <= 2x and H satisfies the
    triangle inequality H <= a + c; T3(a,c,H) then fails only through |a_j - c_j| > H_j (lower bounds)."""
    u = [[{'x%d' % i: 2, R(a, i): -1, R(c, i): -1}, {R(a, i): 1, R(c, i): 1}] for i in range(3)]
    return req(u, tag='disc%d_%d' % (a, c))


def req_6p1(pts):
    """Fano: actual roles at points 1..6 (pts[q-1]), requested point 0"""
    PEN0 = [l for l in LINES if 0 in l]
    u = []
    for i in range(3):
        ex = []
        for l in PEN0:
            d = {'x%d' % i: 2}
            for q in l:
                if q == 0: continue
                k = R(pts[q - 1], i); d[k] = d.get(k, 0) - 1
            ex.append(d)
        d = {'x%d' % i: 4}
        for q in range(1, 7):
            k = R(pts[q - 1], i); d[k] = d.get(k, 0) - 1
        ex.append(d)
        u.append(ex)
    return req(u, tag='6+1', pts=list(pts))


class GenAdv(BalAdv):
    """General case (A) (no separation assumption): variables x, sigma, t (maximal free box >= sigma), tau.
    Each role: super-heavy binaries z_i (z=1 => c_i >= sigma_i, z=0 => c_i <= 2x_i/3), sum z >= 1; blocked binaries
    w_i (w=1 => c_i >= t_i), sum w >= 1 (case (A): every type blocked by t), w_i <= z_i.
    Kinds: 'min' (z_i = 1, c_i = sigma_i), 'blk' (facet i: c_i = t_i, c_j <= t_j - dt for j != i), 'req', 'free', 'mono'
    ('mono' cls i: box of cost <= 3/4 + eps containing the role and no role with w_j = 1 for j != i ... i.e. only pure
    B_i types: Corollary C).  Facts: t_i >= sigma_i, cost(t) = sum (x_i - t_i) >= tau, e'_i = x_i - t_i >= eta (Cor. C),
    x_i >= 2 eta + xtp (Theorem TP), sigma_i >= 2x_i/3 + etas."""

    def __init__(s, roles, eta=1e-2, beta=1e-3, etas=1e-3, xmin=0.02, fk=4, menu=('F', 'TT', 'T3', 'K4'),
                 xmax=1.5, dt=0.0, extra=(), pairs=None):
        s.m = m = Model(); s.beta = beta; s.fk = fk; s.menu = menu; s.roles = roles
        s.eta = eta; s.etas = etas; s.dt = dt
        s.x = x = [m.var(max(xmin, 2 * eta + 1e-6), xmax, name='x%d' % i) for i in range(3)]
        s.sg = sg = [m.var(0.0, 1.0, name='s%d' % i) for i in range(3)]
        s.tb = tb = [m.var(0.0, 1.5, name='t%d' % i) for i in range(3)]
        s.tau = tau = m.var(0.75 + eta, 3.0, name='tau')
        s.names = {'tau': tau}
        for i in range(3):
            s.names['x%d' % i] = x[i]; s.names['s%d' % i] = sg[i]; s.names['t%d' % i] = tb[i]
            m.add({sg[i]: 1, x[i]: -2 / 3}, lo=etas)
            m.add({tb[i]: 1, sg[i]: -1}, lo=0)
            m.add({tb[i]: 1, x[i]: -1}, hi=-eta)                      # e'_i >= eta
            m.add({x[i]: 1, tau: -2}, lo=-1.5 + 1e-6)                 # x_i > 2 eta (Theorem TP)
        m.add({x[0]: 1, x[1]: 1, x[2]: 1, tb[0]: -1, tb[1]: -1, tb[2]: -1, tau: -1}, lo=0)   # cost(t) >= tau
        if pairs is not None:        # list of (i, j, lo, hi) bounds on x_i + x_j
            for i, j, lo, hi in pairs:
                m.add({x[i]: 1, x[j]: 1}, lo=lo if lo is not None else -np.inf, hi=hi if hi is not None else np.inf)
        s.T = []; s.Y = []; s.W = []; s.Q = []; s.kind = []
        for k, r in enumerate(roles):
            s.add_role(k, r)
        for e in extra:
            f, c = s.ex(e[0]); m.add(f, lo=(e[1] - c) if e[1] is not None else -np.inf, hi=(e[2] - c) if e[2] is not None else np.inf)
        s.added = set(); s.Lind = {}; s.Pind = {}

    def add_role(s, k, r):
        m = s.m; x = s.x; sg = s.sg; tau = s.tau; tb = s.tb
        c = [m.var(0.0, 1.5, name='r%d_%d' % (k, i)) for i in range(3)]
        for i in range(3):
            s.names['r%d_%d' % (k, i)] = c[i]
            m.add({c[i]: 1, x[i]: -1}, hi=0)
        m.add({c[0]: 1, c[1]: 1, c[2]: 1}, lo=1, hi=1)
        z = [m.var(0, 1, integer=True, name='z%d_%d' % (k, i)) for i in range(3)]
        w = [m.var(0, 1, integer=True, name='w%d_%d' % (k, i)) for i in range(3)]
        m.add({z[0]: 1, z[1]: 1, z[2]: 1}, lo=1)
        m.add({w[0]: 1, w[1]: 1, w[2]: 1}, lo=1)
        for i in range(3):
            m.add({c[i]: 1, sg[i]: -1, z[i]: -M}, lo=-M)                 # z=1 => c_i >= sigma_i
            m.add({c[i]: 1, x[i]: -2 / 3, z[i]: -M}, hi=0)                # z=0 => c_i <= 2x_i/3
            m.add({c[i]: 1, tb[i]: -1, w[i]: -M}, lo=-M)                  # w=1 => c_i >= t_i
            m.add({w[i]: 1, z[i]: -1}, hi=0)
        kind = r['kind']; qv = None
        if kind == 'min':
            i = r['cls']; m.add({z[i]: 1}, lo=1); m.add({c[i]: 1, sg[i]: -1}, lo=0, hi=0)
        elif kind == 'blk':
            i = r['facet']; m.add({c[i]: 1, tb[i]: -1}, lo=0, hi=0); m.add({w[i]: 1}, lo=1)
            for j in range(3):
                if j != i:
                    m.add({c[j]: 1, tb[j]: -1}, hi=-s.dt); m.add({w[j]: 1}, hi=0)
        elif kind in ('free', 'mono'):
            pass
        elif kind == 'req':
            qv = m.var(0, 1, integer=True, name='q%d' % k); s.names['q%d' % k] = qv
            cost = {tau: -1}
            for i in range(3):
                exprs = list(r['u'][i]) + [{'x%d' % i: 1}]
                u = m.var(0.0, 3.0, name='u%d_%d' % (k, i)); s.names['u%d_%d' % (k, i)] = u
                p0 = m.var(0, 1, integer=True)
                ps = [p0]; ns = []
                for e in exprs:
                    f, cc = s.ex(e)
                    g = lin({u: 1}, {j: -v for j, v in f.items()})
                    m.add(lin(g, {p0: -M}), hi=cc)
                    p = m.var(0, 1, integer=True); ps.append(p)
                    m.add(lin(g, {p: -M}), lo=cc - M)
                    n = m.var(0, 1, integer=True); ns.append(n)
                    m.add(lin(f, {n: M}), hi=M - cc)
                m.add({u: 1, p0: M}, hi=M)
                m.add({p: 1 for p in ps}, lo=1)
                m.add(lin({p0: 1}, {n: -1 for n in ns}), hi=0)
                m.add({c[i]: 1, u: -1, qv: M}, hi=M)
                cost = lin(cost, {x[i]: 1, u: -1})
            m.add(lin(cost, {qv: M}), hi=M)
            m.add(lin(cost, {qv: M}), lo=DQ)
            if r.get('force', False):
                m.add({qv: 1}, lo=1)
        else:
            raise ValueError(kind)
        s.T.append(c); s.Y.append(z); s.W.append(w); s.Q.append(qv); s.kind.append(kind)

    def finalize(s):
        m = s.m; x = s.x
        for k, r in enumerate(s.roles):
            if r['kind'] != 'mono':
                continue
            i = r['cls']; c = s.T[k]
            for j in range(3):
                m.add({s.W[k][j]: 1}, lo=1 if j == i else 0, hi=1 if j == i else 0)   # pure B_i
            wb = [m.var(0.0, 1.5) for _ in range(3)]
            for j in range(3):
                m.add({wb[j]: 1, x[j]: -1}, hi=0); m.add({c[j]: 1, wb[j]: -1}, hi=0)
            m.add({x[0]: 1, x[1]: 1, x[2]: 1, wb[0]: -1, wb[1]: -1, wb[2]: -1}, hi=0.75 + r.get('eps', 1e-3))
            for k2 in range(len(s.roles)):
                if k2 == k: continue
                # every valid role in the box is a pure B_i type: if role k2 has w_j = 1 for some j != i, it is outside
                for j in range(3):
                    if j == i: continue
                    bs = [m.var(0, 1, integer=True) for _ in range(3)]
                    g = {b: 1 for b in bs}; g[s.W[k2][j]] = -1
                    if s.Q[k2] is not None:
                        g[s.Q[k2]] = -1; m.add(g, lo=-1)
                    else:
                        m.add(g, lo=0)
                    for jj in range(3):
                        m.add({s.T[k2][jj]: 1, wb[jj]: -1, bs[jj]: -M}, lo=1e-6 - M)

    def extract(s, X):
        d = BalAdv.extract(s, X)
        d['t'] = [X[v] for v in s.tb]; d['W'] = [[int(round(X[v])) for v in w] for w in s.W]
        d['mode'] = 'gen'; d['Y'] = [[int(round(X[v])) for v in z] for z in s.Y]
        return d
