"""Role-based MILP adversary for Th(3) strategies of the type "window blockers + requests" (wave typeclosed3).

Variables: x (3 capacities), sigma (class minima), tau (>= 3/4 + eta), t (thresholds of a maximal free box around H),
roles r = types c^r (unit, 0 <= c <= x) with binaries z^r_i (super-heavy at i).  Facts (F1)-(F6) of notes_strategy.md.
Role kinds:
  min   {'kind':'min','cls':i}                     class minimiser: z_i = 1, c_i = sigma_i
  blk   {'kind':'blk','facet':i}                   window blocker: c_i = t_i, c_j <= t_j - DT (j != i); with the lexicographic
                                                   box (order) the later parts get c_j <= 4x_j/7 instead
  req   {'kind':'req','u':[expr,expr,expr],'clip':True}  request: answer c <= max(u,0); valid iff cost(u) <= tau
                                                   (binary q; q = 0 => cost >= tau + 1e-6 and the role is void)
  free  {'kind':'free'}                            any type of K
expr = dict of linear terms over names: 'x0','x1','x2','s0'..,'tau','t0'..,'r<k>_<i>' (coordinate i of role k), 'c' (constant).
Templates (lazily added failure disjunctions, strictness eta2 normalised by x_i): 'F' all Fano assignments of roles to
points (Lemma 7.63), 'V' ordered pairs, 'TT' the 42 two-type functions, 'K4' (g <= x - (fa+fb+fc)/2, triangle ineqs).
Result INFEASIBLE => the strategy works numerically (to be certified exactly); ADVERSARY => configuration returned.
"""
import itertools, json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
M = 20.0


def fano_autos():
    """the 168 point permutations preserving LINES"""
    Ls = set(frozenset(l) for l in LINES); out = []
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[q] for q in l) in Ls for l in LINES):
            out.append(p)
    assert len(out) == 168
    return out


def pattern_reps(k):
    """orbit representatives (under Fano automorphisms) of patterns in {0..k-1}^7 using ALL k labels"""
    autos = fano_autos(); seen = set(); reps = []
    for pat in itertools.product(range(k), repeat=7):
        if len(set(pat)) != k or pat in seen:
            continue
        orb = set(tuple(pat[a[q]] for q in range(7)) for a in autos)
        seen |= orb; reps.append(pat)
    return reps


PATS = {k: pattern_reps(k) for k in (1, 2, 3)}
DT = 0.0       # blockers: b^i_j <= t_j (closed model: limits of strict blockers are legitimate)


def load_tt():
    from fractions import Fraction as Fr
    fn = '/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'
    d = json.load(open(fn))
    return [[(float(Fr(u)), float(Fr(v))) for u, v in d[k]['record']['vertices']] for k in sorted(d, key=int)]


class Model:
    def __init__(s):
        s.nv = 0; s.lb = []; s.ub = []; s.integ = []; s.rows = []; s.lo = []; s.hi = []; s.names = []

    def var(s, lb=0.0, ub=10.0, integer=False, name=''):
        s.lb.append(lb); s.ub.append(ub); s.integ.append(1 if integer else 0); s.names.append(name); s.nv += 1
        return s.nv - 1

    def add(s, coefs, lo=-np.inf, hi=np.inf):
        s.rows.append(dict(coefs)); s.lo.append(lo); s.hi.append(hi)

    def solve(s, time_limit=600):
        A = lil_matrix((len(s.rows), s.nv))
        for k, r in enumerate(s.rows):
            for j, c in r.items():
                A[k, j] += c
        return milp(c=np.zeros(s.nv), constraints=LinearConstraint(A.tocsr(), s.lo, s.hi),
                    integrality=np.array(s.integ), bounds=Bounds(s.lb, s.ub),
                    options={'time_limit': time_limit, 'disp': False})


class Adv:
    def __init__(s, roles, eta=1e-2, eta2=1e-4, etas=1e-3, xmin=0.02, order=None, byx=False,
                 tmpl=('F', 'V', 'TT', 'K4'), box=True, extra=(), caseA=False, tp=True):
        s.m = m = Model(); s.eta2 = eta2; s.tmpl = tmpl; s.roles = roles; s.caseA = caseA
        if caseA: box = 'sigma'
        s.x = x = [m.var(xmin, 3.0, name='x%d' % i) for i in range(3)]
        s.sg = sg = [m.var(0.0, 1.0, name='s%d' % i) for i in range(3)]
        s.tau = tau = m.var(0.75 + eta, 3.0, name='tau')
        s.tb = tb = [m.var(0.0, 3.0, name='t%d' % i) for i in range(3)]
        s.names = {}
        for i in range(3):
            s.names['x%d' % i] = x[i]; s.names['s%d' % i] = sg[i]; s.names['t%d' % i] = tb[i]
        s.names['tau'] = tau
        for i in range(3):
            m.add({sg[i]: 1, x[i]: -2 / 3}, lo=etas)          # strict super-heavy class minimum
            m.add({sg[i]: 1, x[i]: -1}, hi=0)
        m.add({x[0]: 1, x[1]: 1, x[2]: 1, sg[0]: -1, sg[1]: -1, sg[2]: -1, tau: -1}, lo=0)   # identity map
        if byx:
            m.add({x[0]: 1, x[1]: -1}, hi=0); m.add({x[1]: 1, x[2]: -1}, hi=0)
        if tp:
            for i in range(3): m.add({x[i]: 1, tau: -2}, lo=-1.5)          # Theorem TP: x_i > 2(tau - 3/4)
        # window box
        s.box = box
        if box:
            for i in range(3):
                if box == 'sigma':
                    m.add({tb[i]: 1, sg[i]: -1}, lo=0)                       # Lemma L3: t >= sigma
                else:
                    m.add({tb[i]: 1, x[i]: -4 / 7}, lo=0)
                m.add({tb[i]: 1, x[i]: -1}, hi=0)
            m.add({x[0]: 1, x[1]: 1, x[2]: 1, tb[0]: -1, tb[1]: -1, tb[2]: -1, tau: -1}, lo=0)  # cost(t) >= tau
        s.order = order
        s.T = []; s.Z = []; s.Q = []
        for k, r in enumerate(roles):
            s.add_role(k, r)
        for e in extra:
            s.add_expr_row(e)
        s.added = set()

    # ---- linear expressions -------------------------------------------------------------------------
    def ex(s, expr):
        """expr dict name->coef ('c' constant) -> (coefs dict var->coef, constant)"""
        f = {}; const = 0.0
        for k, v in expr.items():
            if k == 'c':
                const += v
            else:
                j = s.names[k]; f[j] = f.get(j, 0) + v
        return f, const

    def add_expr_row(s, e):
        """e = (expr, lo, hi)"""
        f, c = s.ex(e[0]); s.m.add(f, lo=e[1] - c if e[1] is not None else -np.inf, hi=e[2] - c if e[2] is not None else np.inf)

    def add_role(s, k, r):
        m = s.m; x = s.x; sg = s.sg; tau = s.tau; tb = s.tb
        t = [m.var(0.0, 1.0, name='r%d_%d' % (k, i)) for i in range(3)]
        for i in range(3):
            s.names['r%d_%d' % (k, i)] = t[i]
        m.add({t[0]: 1, t[1]: 1, t[2]: 1}, lo=1, hi=1)
        z = [m.var(0, 1, integer=True) for i in range(3)]
        for i in range(3):
            m.add({t[i]: 1, x[i]: -1}, hi=0)
            m.add({t[i]: 1, sg[i]: -1, z[i]: -M}, lo=-M)          # z=1 => t_i >= sigma_i
            m.add({t[i]: 1, x[i]: -2 / 3, z[i]: -M}, hi=0)         # z=0 => t_i <= 2x_i/3
        m.add({z[0]: 1, z[1]: 1, z[2]: 1}, lo=1)                   # super-heavy somewhere (F2)
        if s.caseA:                                                # case (A): every type is blocked by the box t
            w = [m.var(0, 1, integer=True) for i in range(3)]
            for i in range(3): m.add({t[i]: 1, tb[i]: -1, w[i]: -M}, lo=-M)   # w=1 => c_i >= t_i
            m.add({w[0]: 1, w[1]: 1, w[2]: 1}, lo=1)
        kind = r['kind']; qv = None
        if kind == 'min':
            i = r['cls']; m.add({z[i]: 1}, lo=1); m.add({t[i]: 1, sg[i]: -1}, hi=0)
        elif kind == 'blk':
            assert s.box
            i = r['facet']; m.add({t[i]: 1, tb[i]: -1}, lo=0, hi=0)
            if s.box == 'sigma': m.add({z[i]: 1}, lo=1)                     # blocker in S_i (Lemma L3 (i))
            later = []
            if s.order is not None:
                later = s.order[s.order.index(i) + 1:]
            for j in range(3):
                if j == i:
                    continue
                if j in later:
                    m.add({t[j]: 1, x[j]: -4 / 7}, hi=0)
                else:
                    m.add({t[j]: 1, tb[j]: -1}, hi=-DT)
        elif kind == 'req':
            qv = m.var(0, 1, integer=True)
            clip = r.get('clip', True)
            wsum = {tau: -1}
            ws = []
            for i in range(3):
                f, c = s.ex(r['u'][i])
                if clip:
                    p = m.var(0, 1, integer=True)      # p=1 => expr >= 0 (u_i = expr); p=0 => expr <= 0 (u_i = 0)
                    g = dict(f); g[p] = g.get(p, 0) - M; m.add(g, lo=-c - M)       # p=1 => expr >= 0
                    g = dict(f); g[p] = g.get(p, 0) - M; m.add(g, hi=-c)            # p=0 => expr <= 0
                    w = m.var(0.0, 3.0)
                    # w = min(x_i - expr, x_i): w <= x_i - expr ; w <= x_i ; w >= x_i - expr - M(1-p) ; w >= x_i - M p
                    g = {w: 1, x[i]: -1}
                    for j, v in f.items(): g[j] = g.get(j, 0) + v
                    m.add(dict(g), hi=-c)
                    m.add({w: 1, x[i]: -1}, hi=0)
                    g2 = dict(g); g2[p] = g2.get(p, 0) - M; m.add(g2, lo=-c - M)
                    m.add({w: 1, x[i]: -1, p: M}, lo=0)
                    # answer: q=1 => t_i <= u_i : t_i <= expr + M(1-p) + M(1-q) ; t_i <= 0 + M p + M(1-q)
                    g = {t[i]: 1}
                    for j, v in f.items(): g[j] = g.get(j, 0) - v
                    g[p] = g.get(p, 0) + M; g[qv] = g.get(qv, 0) + M
                    m.add(g, hi=c + 2 * M)                       # t_i <= expr + M(1-p) + M(1-q)
                    m.add({t[i]: 1, p: -M, qv: M}, hi=M)         # t_i <= M p + M(1-q)
                    wsum[w] = 1
                else:
                    # u_i = expr (must be >= 0 implicitly through t_i >= 0 when q=1); cost term x_i - expr
                    wsum[x[i]] = wsum.get(x[i], 0) + 1
                    for j, v in f.items(): wsum[j] = wsum.get(j, 0) - v
                    ws.append(c)
                    g = {t[i]: 1}
                    for j, v in f.items(): g[j] = g.get(j, 0) - v
                    g[qv] = g.get(qv, 0) + M
                    m.add(g, hi=c + M)                           # t_i <= expr + M(1-q)
            cconst = sum(ws)
            # q=1 => cost <= tau ; q=0 => cost >= tau + 1e-6
            g = dict(wsum); g[qv] = g.get(qv, 0) + M; m.add(g, hi=-cconst + M)
            g = dict(wsum); g[qv] = g.get(qv, 0) + M; m.add(g, lo=-cconst + 1e-6)
            if r.get('force', False):
                m.add({qv: 1}, lo=1)
        elif kind == 'ureq':
            # u_i = max(0, min_k expr_ik) (x_i is always among the exprs); cost = sum_i (x_i - u_i);
            # valid (q=1) iff cost <= tau, then the answer satisfies c <= u.
            qv = m.var(0, 1, integer=True, name='q%d' % k); s.names['q%d' % k] = qv
            cost = {tau: -1}
            for i in range(3):
                exprs = r['u'][i]
                if isinstance(exprs, dict): exprs = [exprs]
                exprs = list(exprs) + [{'x%d' % i: 1}]                       # u_i <= x_i always
                u = m.var(0.0, 3.0, name='u%d_%d' % (k, i))
                p0 = m.var(0, 1, integer=True)                             # p0=1 : the min is <= 0, u = 0
                ps = [p0]; ns = []
                for e in exprs:
                    f, c = s.ex(e)
                    g = {u: 1}
                    for j, v in f.items(): g[j] = g.get(j, 0) - v
                    g1 = dict(g); g1[p0] = g1.get(p0, 0) - M; m.add(g1, hi=c)          # u <= expr + M p0
                    p = m.var(0, 1, integer=True); ps.append(p)
                    g2 = dict(g); g2[p] = g2.get(p, 0) - M; m.add(g2, lo=c - M)        # p=1 => u >= expr
                    n = m.var(0, 1, integer=True); ns.append(n)
                    g3 = dict(f); g3[n] = g3.get(n, 0) + M; m.add(g3, hi=M - c)         # n=1 => expr <= 0
                m.add({u: 1, p0: M}, hi=M)                                              # p0=1 => u <= 0
                m.add({p: 1 for p in ps}, lo=1)                                         # some p (or p0) active
                g = {p0: 1}
                for n in ns: g[n] = g.get(n, 0) - 1
                m.add(g, hi=0)                                                          # p0 <= sum n
                m.add({t[i]: 1, u: -1, qv: M}, hi=M)                                    # q=1 => c_i <= u_i
                cost[x[i]] = cost.get(x[i], 0) + 1; cost[u] = cost.get(u, 0) - 1
            g = dict(cost); g[qv] = M; m.add(g, hi=M)                       # q=1 => cost <= tau
            g = dict(cost); g[qv] = M; m.add(g, lo=1e-6)                    # q=0 => cost >= tau + 1e-6
            if r.get('force', False):
                m.add({qv: 1}, lo=1)
            if r.get('inclass') is not None:
                m.add({z[r['inclass']]: 1, qv: -1}, lo=0)                   # q=1 => in class S_o
            # EXTREMAL answer (lexicographic minimisation of coordinates r['lex']): the box
            # {w_i < c_i, w_j <= (c_j or u_j)} is free, so its cost >= tau:
            #   c_i <= x_i - tau + sum_{j != i} (x_j - v_j),  v_j = c_j for earlier lex coords, u_j otherwise
            uvars = [None] * 3
            for i in range(3):
                uvars[i] = [v for v, nm in enumerate(m.names) if nm == 'u%d_%d' % (k, i)][0]
            done = []
            for i in r.get('lex', []):
                g = {t[i]: 1, x[i]: -1, tau: 1, qv: M}
                for j in range(3):
                    if j == i: continue
                    g[x[j]] = g.get(x[j], 0) - 1
                    vj = t[j] if j in done else uvars[j]
                    g[vj] = g.get(vj, 0) + 1
                m.add(g, hi=M)
                done.append(i)
        elif kind == 'free':
            pass
        else:
            raise ValueError(kind)
        for e in r.get('extra', ()):
            s.add_expr_row(e)
        s.T.append(t); s.Z.append(z); s.Q.append(qv)

    # ---- templates -------------------------------------------------------------------------------------
    def forms(s, key):
        """list of (lin dict, rhs): template feasible iff all lin <= rhs. Failure = some lin >= rhs + eta2*x_i."""
        x, T = s.x, s.T; L = []
        if key[0] == 'F':
            pts = key[1:]
            for i in range(3):
                for l in LINES:
                    f = {x[i]: -2}
                    for p in l:
                        v = T[pts[p]][i]; f[v] = f.get(v, 0) + 1
                    L.append((f, i))
                f = {x[i]: -4}
                for p in range(7):
                    v = T[pts[p]][i]; f[v] = f.get(v, 0) + 1
                L.append((f, i))
        elif key[0] == 'V':
            a, b = key[1:]
            for i in range(3):
                L.append(({T[a][i]: 1, T[b][i]: 1, x[i]: -1}, i))
                L.append(({T[a][i]: 1.25, T[b][i]: 0.5, x[i]: -1}, i))
        elif key[0] == 'TT':
            a, b, fn = key[1:]
            for i in range(3):
                for u, v in s.tt[fn]:
                    f = {x[i]: -1}
                    if u: f[T[a][i]] = f.get(T[a][i], 0) + u
                    if v: f[T[b][i]] = f.get(T[b][i], 0) + v
                    L.append((f, i))
        elif key[0] == 'T3':       # L5 line-pencil: rows a,b,c on a line, four quad rows requested
            a, b, c = key[1:]
            for i in range(3):
                L.append(({T[a][i]: 1, T[b][i]: 1, T[c][i]: 1, x[i]: -2}, i))
            opts = []
            for i in range(3):
                opts.append([{T[a][i]: 0.5}, {T[b][i]: 0.5}, {T[c][i]: 0.5}, {T[a][i]: 0.25, T[b][i]: 0.25, T[c][i]: 0.25}])
            for ch in itertools.product(range(4), repeat=3):
                f = {s.tau: -1}
                for i in range(3):
                    for v, cf in opts[i][ch[i]].items(): f[v] = f.get(v, 0) + cf
                L.append((f, None))                                  # cost - tau >= eta2 (absolute)
        elif key[0] == 'K4':
            g, a, b, c = key[1:]
            for i in range(3):
                A_, B_, C_ = T[a][i], T[b][i], T[c][i]
                L.append(({A_: 1, B_: -1, C_: -1}, i)); L.append(({B_: 1, A_: -1, C_: -1}, i)); L.append(({C_: 1, A_: -1, B_: -1}, i))
                L.append(({T[g][i]: 1, A_: 0.5, B_: 0.5, C_: 0.5, x[i]: -1}, i))
        return L

    def fail_any(s, key):
        m = s.m; L = s.forms(key); bs = [m.var(0, 1, integer=True) for _ in L]
        cons = {b: 1 for b in bs}; nvoid = 0
        for j in set(key[1:] if key[0] != 'TT' else key[1:3]):
            if s.Q[j] is not None:
                cons[s.Q[j]] = cons.get(s.Q[j], 0) - 1; nvoid += 1
        m.add(cons, lo=1 - nvoid)
        for b, (f, i) in zip(bs, L):
            g = dict(f); g[b] = g.get(b, 0) - M
            if i is None:
                m.add(g, lo=s.eta2 - M)
            else:
                g[s.x[i]] = g.get(s.x[i], 0) - s.eta2; m.add(g, lo=-M)

    def eval_templates(s, X, maxk=3):
        """template keys feasible at solution X (tolerance eta2 normalised).  Fano: assignments using <= maxk distinct
        roles (roles deduplicated by value), patterns up to Fano automorphism."""
        n = len(s.T); xv = np.array([X[v] for v in s.x]); R = np.array([[X[v] for v in t] for t in s.T])
        valid = [s.Q[j] is None or X[s.Q[j]] > 0.5 for j in range(n)]
        groups = {}
        for j in range(n):
            if valid[j]:
                groups.setdefault(tuple(np.round(R[j], 6)), []).append(j)
        reps = [g[0] for g in groups.values()]
        out = []; tol = s.eta2

        def fano_ok(pts):
            for i in range(3):
                z = R[list(pts), i]
                if z.sum() > 4 * xv[i] * (1 + tol / 4): return False
                for l in LINES:
                    if z[l[0]] + z[l[1]] + z[l[2]] > 2 * xv[i] * (1 + tol / 2): return False
            return True
        if 'F' in s.tmpl:
            for k in range(1, maxk + 1):
                for combo in itertools.combinations(reps, k):
                    for pat in PATS[k]:
                        pts = tuple(combo[p] for p in pat)
                        if fano_ok(pts):
                            out.append(('F',) + pts)
        if 'V' in s.tmpl or 'TT' in s.tmpl:
            for a in reps:
                for b in reps:
                    if a == b:
                        continue
                    if 'V' in s.tmpl and all(max(R[a, i] + R[b, i], 1.25 * R[a, i] + 0.5 * R[b, i]) <= xv[i] * (1 + tol) for i in range(3)):
                        out.append(('V', a, b))
                    if 'TT' in s.tmpl:
                        for fn, vs in enumerate(s.tt):
                            if all(u * R[a, i] + v * R[b, i] <= xv[i] * (1 + tol) for i in range(3) for u, v in vs):
                                out.append(('TT', a, b, fn))
        if 'T3' in s.tmpl:
            tauv = X[s.tau]
            for a, b, c in itertools.combinations_with_replacement(reps, 3):
                S = R[a] + R[b] + R[c]
                if np.any(S > 2 * xv * (1 + tol / 2)): continue
                Mx = np.maximum(np.maximum(R[a], R[b]), np.maximum(R[c], S / 2))
                if Mx.sum() / 2 < tauv - tol:
                    out.append(('T3', a, b, c))
        if 'K4' in s.tmpl:
            for g in reps:
                for a, b, c in itertools.combinations([j for j in reps if j != g], 3):
                    ok = True
                    for i in range(3):
                        A_, B_, C_ = R[a, i], R[b, i], R[c, i]
                        if A_ > B_ + C_ + tol * xv[i] or B_ > A_ + C_ + tol * xv[i] or C_ > A_ + B_ + tol * xv[i]:
                            ok = False; break
                        if R[g, i] + 0.5 * (A_ + B_ + C_) > xv[i] * (1 + tol):
                            ok = False; break
                    if ok:
                        out.append(('K4', g, a, b, c))
        return out

    def run(s, maxit=400, tl=600, verbose=True, maxadd=300):
        s.tt = load_tt()
        t0 = time.time()
        for it in range(maxit):
            res = s.m.solve(tl)
            if res.x is None:
                st = 'INFEASIBLE' if res.status == 2 else 'STATUS%d' % res.status
                if verbose: print(' it', it, st, 'templates added', len(s.added), '%.0fs' % (time.time() - t0), flush=True)
                return st, None
            X = res.x
            new = [k for k in s.eval_templates(X) if k not in s.added]
            if verbose:
                print(' it', it, 'new templates', len(new), 'total', len(s.added), 'tau %.4f' % X[s.tau],
                      'x', np.round([X[v] for v in s.x], 3), '%.0fs' % (time.time() - t0), flush=True)
            if not new:
                viol = s.max_violation(X)
                if verbose: print(' max row violation at solution %.2e' % viol, flush=True)
                sol = s.extract(X); sol['rowviol'] = viol; sol['X'] = list(map(float, X))
                return 'ADVERSARY', sol
            # add a bounded number (prefer diverse kinds)
            for k in new[:maxadd]:
                s.fail_any(k); s.added.add(k)
        return 'MAXIT', None

    def max_violation(s, X):
        m = s.m; worst = 0.0
        for r, lo, hi in zip(m.rows, m.lo, m.hi):
            v = sum(c * X[j] for j, c in r.items())
            worst = max(worst, lo - v if lo > -np.inf else 0.0, v - hi if hi < np.inf else 0.0)
        return worst

    def extract(s, X):
        return {'x': [X[v] for v in s.x], 'sigma': [X[v] for v in s.sg], 'tau': X[s.tau], 't': [X[v] for v in s.tb],
                'roles': [[X[v] for v in t] for t in s.T], 'Z': [[int(round(X[v])) for v in z] for z in s.Z],
                'Q': [None if q is None else int(round(X[q])) for q in s.Q], 'spec': s.roles, 'box': s.box, 'caseA': s.caseA}


# ---------------- role builders ----------------------------------------------------------------------------
def R(k, i=None, **kw):
    """coordinate name helper"""
    return 'r%d_%d' % (k, i)


def roles_basic(order=None):
    """3 class minimisers (roles 0,1,2) + 3 window blockers (roles 3,4,5)"""
    return [{'kind': 'min', 'cls': i} for i in range(3)] + [{'kind': 'blk', 'facet': i} for i in range(3)]


def req_empty(i):
    """request 'empty part i': u_i = 0, others x; valid iff x_i <= tau"""
    u = [({'x%d' % j: 1} if j != i else {'c': 0.0}) for j in range(3)]
    return {'kind': 'req', 'u': u, 'clip': False}


def req_vertex(i):
    """vertex request: u_i = max(x_i - 3/4, 0), others x; always valid (cost = min(3/4, x_i) < tau)"""
    u = [({'x%d' % j: 1} if j != i else {'x%d' % i: 1, 'c': -0.75}) for j in range(3)]
    return {'kind': 'req', 'u': u, 'clip': True, 'force': True}


def req_corner(k, X):
    """corner of role k at its class X: u_X = sigma_X (answer c_X <= sigma_X, i.e. not in S_X after strictness), u_j = x_j - c^k_j"""
    u = []
    for j in range(3):
        if j == X:
            u.append({'s%d' % X: 1, 'c': -DT})
        else:
            u.append({'x%d' % j: 1, R(k, j): -1})
    return {'kind': 'req', 'u': u, 'clip': True}


def req_generic(u):
    return {'kind': 'req', 'u': u, 'clip': True}


def ureq(u, **kw):
    """u[i] = list of linear exprs (u_i = max(0, min of them))"""
    d = {'kind': 'ureq', 'u': u}; d.update(kw); return d


def req_mp(b, c):
    """mixed-pencil request for roles b (twice) and c on a line: d <= x - b/2 - c/4 and d <= x - c/2 (Lemma 7.63);
    the Fano tuple (b,b,c,d,d,d,d) is then feasible iff 2b + c <= 2x per part.  cost = 3/4 + sum (c-2b)^+/4."""
    u = []
    for i in range(3):
        u.append([{'x%d' % i: 1, R(b, i): -0.5, R(c, i): -0.25}, {'x%d' % i: 1, R(c, i): -0.5}])
    return ureq(u)


def xreq(u, lex, **kw):
    d = {'kind': 'ureq', 'u': u, 'lex': list(lex)}; d.update(kw); return d


def lexbox_roles(order=(0, 1, 2)):
    """the three blockers of the lexicographic maximal free box around H as extremal request answers:
    b^{o0}: min c_{o0} over c <= (x_{o0}, 4x_{o1}/7, 4x_{o2}/7);  b^{o1}: min c_{o1} over c <= (b^{o0}_{o0}, x_{o1}, 4x_{o2}/7);
    b^{o2}: min c_{o2} over c <= (b^{o0}_{o0}, b^{o1}_{o1}, x_{o2}).  Each request is valid iff its cost < tau
    (else that facet is INF: the corresponding role is void).  Roles are appended in this order; k0 = index of the first."""
    o0, o1, o2 = order
    def col(i, base=None):
        return base if base is not None else {'x%d' % i: 1}
    out = []
    u = [None] * 3; u[o0] = [{'x%d' % o0: 1}]; u[o1] = [{'x%d' % o1: 4 / 7}]; u[o2] = [{'x%d' % o2: 4 / 7}]
    out.append(xreq(u, [o0], tag='lexblk%d' % o0))
    return out


def lexbox_sigma_roles_at(k0, order=(0, 1, 2)):
    """lexicographic maximal free box ABOVE the class box (Lemma L3 with lex tie-breaking), as extremal answers:
    b^{o0} = argmin c_{o0} over {c_{o1} <= 2x_{o1}/3, c_{o2} <= 2x_{o2}/3} (so b^{o0} in S_{o0}), request cost (x_{o1}+x_{o2})/3;
    b^{o1} = argmin c_{o1} over {c_{o0} <= t_{o0}, c_{o2} <= 2x_{o2}/3} with b^{o1} in S_{o1} (extra: z = 1);
    b^{o2} = argmin c_{o2} over {c_{o0} <= t_{o0}, c_{o1} <= t_{o1}} with b^{o2} in S_{o2}.
    An invalid request (cost >= tau) = INF facet (small-pair case); later requests then use x there."""
    o0, o1, o2 = order
    def ref(k, i):
        return {R(k, i): 1, 'q%d' % k: -M, 'c': M}
    r0 = [None] * 3; r0[o0] = [{'x%d' % o0: 1}]; r0[o1] = [{'x%d' % o1: 2 / 3}]; r0[o2] = [{'x%d' % o2: 2 / 3}]
    r1 = [None] * 3; r1[o0] = [ref(k0, o0)]; r1[o1] = [{'x%d' % o1: 1}]; r1[o2] = [{'x%d' % o2: 2 / 3}]
    r2 = [None] * 3; r2[o0] = [ref(k0, o0)]; r2[o1] = [ref(k0 + 1, o1)]; r2[o2] = [{'x%d' % o2: 1}]
    out = []
    for kk, (rr, o) in enumerate(((r0, o0), (r1, o1), (r2, o2))):
        role = xreq(rr, [o], tag='sigblk%d' % o, inclass=o)      # inclass: z_o = 1 when valid
        out.append(role)
    return out


def lexbox_roles_at(k0, order=(0, 1, 2)):
    """roles k0, k0+1, k0+2.  If an earlier blocker is void (its request invalid: facet INF) the later requests use
    x there (expr r + M(1-q), cut by the implicit u <= x).  Each blocker's own coordinate is > 4x/7 (extra row)."""
    o0, o1, o2 = order
    def ref(k, i):
        return {R(k, i): 1, 'q%d' % k: -M, 'c': M}
    r0 = [None] * 3; r0[o0] = [{'x%d' % o0: 1}]; r0[o1] = [{'x%d' % o1: 4 / 7}]; r0[o2] = [{'x%d' % o2: 4 / 7}]
    r1 = [None] * 3; r1[o0] = [ref(k0, o0)]; r1[o1] = [{'x%d' % o1: 1}]; r1[o2] = [{'x%d' % o2: 4 / 7}]
    r2 = [None] * 3; r2[o0] = [ref(k0, o0)]; r2[o1] = [ref(k0 + 1, o1)]; r2[o2] = [{'x%d' % o2: 1}]
    out = []
    for kk, (rr, o) in enumerate(((r0, o0), (r1, o1), (r2, o2))):
        role = xreq(rr, [o], tag='lexblk%d' % o)
        role['extra'] = [({R(k0 + kk, o): 1, 'x%d' % o: -4 / 7, 'q%d' % (k0 + kk): M}, M, None)]   # q=1 => c_o >= 4x_o/7
        out.append(role)
    return out


def req_box_side(i, j):
    """request just outside the window on facets i,j: u_i = t_i, u_j = t_j (answers: blockers of the third facet,
    'c_k >= t_k'); cost = (x_i - t_i) + (x_j - t_j).  Combined with 'extra' rows to select a specific blocker."""
    u = []
    for l in range(3):
        if l in (i, j): u.append([{'t%d' % l: 1, 'c': -DT}])
        else: u.append([{'x%d' % l: 1}])
    return ureq(u)


if __name__ == '__main__':
    pass
