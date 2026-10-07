"""gen_certp.py -- exact lazy branch-and-bound certificates for SEP(h, L; pi0), the SEPARATED regime of Th(p),
p = h + L parts: heavy parts 0..h-1 (S_i != {}), light parts h..p-1 (every type has c_l <= 2x_l/3).
Generalises typeclosed3/boundary/gen_cert3.py (+ gen_cert.py / gen_cert2.py, whose LP / exact-certificate code is reused).
Checker: check_gen_certp.py (independent, std-lib, Fractions).

VARIABLES  x0..x{p-1}, s0..s{h-1} (sigma_i, heavy only), tau, c<role>_<j> (j < p).
BASE (facts of a counterexample, see notes_genp_sep.md [20:30]):
  heavy pairs  x_i + x_j >= 3/2 + pi0;  heavy i: s_i > 2x_i/3, s_i <= x_i, [erows] x_i - s_i >= tau - 3/4 (NON-strict;
  induction on h: needs SEP(h-1, L+1; pi0));  sum_{heavy} (x_i - s_i) >= tau;  tau > 3/4;  light l: x_l >= 0;
  every role r: sum_j c_rj = 1, 0 <= c_rj <= x_j, light l: c_rl <= 2x_l/3;  minimiser of class i: c_ri = s_i.
  REGION (spec): 'order' -> x_0 <= .. <= x_{h-1} and x_h <= .. <= x_{p-1}; 'xbox' [[i,lo,hi]]; 'pairs' [[i,j,lo,hi]].
ROLE DISJUNCTIONS  'cls r' (non-minimiser roles: c_ri >= s_i for some heavy i); requests 'val r', 'ans r i' as in gen_cert.
TEMPLATES (failure disjunctions; one alternative per strictly violated row, + void alternatives of request labels):
  'F l0,..,l6'   Fano tuple (Lemma 7.63): heavy part i: some line sum > 2x_i; any part: total > 4x_i.
                 (light parts: line sums are automatic, every row <= 2x_l/3.)
  'V a,b'        any part: a_i + b_i > x_i  or  5a_i/4 + b_i/2 > x_i.
  'W t:a,b'      two-type capacity function t of the 42-catalogue: any part i, efficient vertex (u,v): u a_i + v b_i > x_i.
  'R sh:ks:labs' one requested type f on P = SHAPES[sh] (1: {0}, 2: {0,1}, 3: triangle {0,1,3}, 4: quadrangle
                 {3,4,5,6} = L5/T3), labels on A = sorted complement.  ks = one char per part.
                 heavy part i: bounds = [(2x_i - sum_{A on l} c_i)/|l n P| for lines l meeting P (LINES order)] +
                   [(4x_i - sum_A c_i)/|P|]; ks[i] = 'x' (u_i = x_i) or digit (u_i = that bound);
                   success rows: A-only lines <= 2x_i, u_i <= every bound, u_i <= x_i, u_i >= 0.
                 light part l: tb = (4x_l - sum_A c_l)/|P|; ks[l] = 'x': u_l = x_l, success row 2x_l/3 <= tb;
                   ks[l] = '0': u_l = tb, success rows 0 <= u_l <= x_l.
                 global success row: sum_i (x_i - u_i) <= tau.
usage: python3 gen_certp.py <strategy.json> <pi0> [fk=7] [rk=4] [strong=4] [menu=F,V,R,W] [tag=..] [maxnodes=..]
       [resume=1]  -> certs/gcertp_<tag>_<pi0>.jsonl.gz  (or certs/gadvp_<tag>_<pi0>.json on an adversary)"""
import sys, os, json, itertools, time, gzip, pickle
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
TC3 = os.path.join(os.path.dirname(HERE), 'typeclosed3')
sys.path.insert(0, TC3)
import gen_cert as G                     # row, lin, scale, dedup, verify, gauss_cert, pattern_reps, AUT, LINES

LINES = G.LINES
row, lin, scale, dedup = G.row, G.lin, G.scale, G.dedup
SHAPES = {1: (0,), 2: (0, 1), 3: (0, 1, 3), 4: (3, 4, 5, 6)}


def shape_data(sh):
    P = SHAPES[sh]; A = [q for q in range(7) if q not in P]
    blines = [l for l in LINES if any(q in P for q in l)]
    alines = [l for l in LINES if not any(q in P for q in l)]
    return P, A, blines, alines


_RPAT = {}


def rpattern_reps(sh, k):
    """surjections A -> range(k) modulo the stabiliser of P in the Fano group"""
    key = (sh, k)
    if key in _RPAT: return _RPAT[key]
    P, A, _, _ = shape_data(sh)
    stab = [a for a in G.AUT if set(a[q] for q in P) == set(P)]
    pos = {q: i for i, q in enumerate(A)}
    seen = set(); reps = []
    for pat in itertools.product(range(k), repeat=len(A)):
        if len(set(pat)) != k or pat in seen: continue
        orb = set()
        for a in stab:
            img = [None] * len(A)
            for q in A: img[pos[a[q]]] = pat[pos[q]]
            orb.add(tuple(img))
        seen |= orb; reps.append(pat)
    _RPAT[key] = reps
    return reps


TTFILE = '/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'
_TT = None


def load_tt():
    global _TT
    if _TT is None:
        d = json.load(open(TTFILE))
        _TT = {k: [(F(u), F(v)) for u, v in d[k]['record']['vertices']] for k in sorted(d, key=int)}
    return _TT


def nz(d):
    return {k: v for k, v in d.items() if v != 0}


class StratP:
    def __init__(s, spec, pi0, fk=7, rk=4, menu=('F', 'V', 'R', 'W')):
        s.spec = spec; s.pi0 = F(pi0); s.fk = fk; s.rk = rk; s.menu = tuple(menu)
        s.h = int(spec['h']); s.L = int(spec.get('L', 0)); s.p = s.h + s.L
        s.HV = list(range(s.h)); s.LT = list(range(s.h, s.p))
        s.erows = bool(spec.get('erows', True))
        s.roles = spec['roles']; s.names = [r['name'] for r in s.roles]
        s.byname = {r['name']: r for r in s.roles}
        s.VARS = ['x%d' % i for i in range(s.p)] + ['s%d' % i for i in s.HV] + ['tau'] + \
            ['c%s_%d' % (n, j) for n in s.names for j in range(s.p)]
        s.VI = {v: k for k, v in enumerate(s.VARS)}
        s.BASE = s.base()
        s.D = {}
        s.build_role_disj()

    @staticmethod
    def X(i):
        return 'x%d' % i

    def c(s, r, j):
        return 'c%s_%d' % (r, j)

    def base(s):
        X = s.X; B = []; sp = s.spec
        for i, j in itertools.combinations(s.HV, 2):
            B.append(row({X(i): 1, X(j): 1}, F(3, 2) + s.pi0))
        for i in s.HV:
            B.append(row({'s%d' % i: 1, X(i): F(-2, 3)}, 0, True))
            B.append(row({X(i): 1, 's%d' % i: -1}, 0))
            if s.erows:
                B.append(row({X(i): 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4)))
        d = {'tau': -1}
        for i in s.HV: d = lin(d, {X(i): 1, 's%d' % i: -1})
        B.append(row(d, 0))
        B.append(row({'tau': 1}, F(3, 4), True))
        for l in s.LT: B.append(row({X(l): 1}, 0))
        if sp.get('order'):
            for grp in (s.HV, s.LT):
                for a, b in zip(grp, grp[1:]): B.append(row({X(b): 1, X(a): -1}, 0))
        for i, lo, hi in sp.get('xbox', []):
            if lo is not None: B.append(row({X(i): 1}, F(lo)))
            if hi is not None: B.append(row({X(i): -1}, -F(hi)))
        for i, j, lo, hi in sp.get('pairs', []):
            if lo is not None: B.append(row({X(i): 1, X(j): 1}, F(lo)))
            if hi is not None: B.append(row({X(i): -1, X(j): -1}, -F(hi)))
        for r in s.roles:
            n = r['name']
            B.append(row({s.c(n, j): 1 for j in range(s.p)}, 1)); B.append(row({s.c(n, j): -1 for j in range(s.p)}, -1))
            for j in range(s.p):
                B.append(row({s.c(n, j): 1}, 0)); B.append(row({X(j): 1, s.c(n, j): -1}, 0))
            for l in s.LT:
                B.append(row({X(l): F(2, 3), s.c(n, l): -1}, 0))
            if r['kind'] == 'min':
                i = r['cls']; assert i in s.HV
                B.append(row({s.c(n, i): 1, 's%d' % i: -1}, 0)); B.append(row({s.c(n, i): -1, 's%d' % i: 1}, 0))
            elif r['kind'] == 'dmin':
                i = r['cls']; assert i in s.HV and r['dir'] != i
                B.append(row({s.c(n, i): 1, 's%d' % i: -1}, 0))          # d in S_i
            elif r['kind'] == 'lmin':
                # t = lexmin over S_i of (c_l, c_i), l = dir.  t in S_i, and the box w_l = t_l (closed), w_i = t_i - e,
                # w_j = s_j - e (heavy j not in {i,l}) is free:  (x_l - t_l) + (x_i - t_i) + sum_j (x_j - s_j) >= tau
                i = r['cls']; l = r['dir']; assert i in s.HV and l != i
                B.append(row({s.c(n, i): 1, 's%d' % i: -1}, 0))
                d = {s.X(l): 1, s.c(n, l): -1, s.X(i): 1, s.c(n, i): -1, 'tau': -1}
                for k in s.HV:
                    if k not in (i, l): d = lin(d, {s.X(k): 1, 's%d' % k: -1})
                B.append(row(d, 0))
            else:
                assert r['kind'] == 'req'
        return B

    # ---------------- requests (as gen_cert, p parts) ----------------
    def exprs(s, r, i):
        return [lin(e) for e in r['u'][i]] + [{s.X(i): F(1)}]

    def void_alts(s, r):
        if r['kind'] != 'req' or r.get('always_valid'): return []
        per = [s.exprs(r, i) for i in range(s.p)]
        alts = []
        for ks in itertools.product(*[range(len(q)) for q in per]):
            rows = []
            for S in itertools.product([0, 1], repeat=s.p):
                d = {'tau': F(-1)}; cst = F(0)
                for i in range(s.p):
                    if S[i]: d = lin(d, {s.X(i): 1})
                    else:
                        e = dict(per[i][ks[i]]); cc = F(e.pop('c', 0))
                        d = lin(d, {s.X(i): 1}, scale(e, -1)); cst -= cc
                rows.append(row(d, -cst, not r.get('strict')))
            alts.append(frozenset(rows))
        return alts

    def valid_alts(s, r):
        per = [s.exprs(r, i) for i in range(s.p)]
        alts = []
        for S in itertools.product([0, 1], repeat=s.p):
            rows = []
            for ks in itertools.product(*[range(len(q)) for q in per]):
                d = {'tau': F(1)}; cst = F(0)
                for i in range(s.p):
                    if S[i]: d = lin(d, {s.X(i): -1})
                    else:
                        e = dict(per[i][ks[i]]); cc = F(e.pop('c', 0))
                        d = lin(d, {s.X(i): -1}, e); cst += cc
                rows.append(row(d, -cst, bool(r.get('strict'))))
            alts.append(frozenset(rows))
        return alts

    def build_role_disj(s):
        D = s.D
        for d in s.roles:
            if d['kind'] != 'lmin': continue
            # 'lm t r': r not in S_i | r_l > t_l | (r_l >= t_l and r_i >= t_i)     [lex minimality]
            # 'lfree t': t_l <= 0 | (x_l - t_l) + sum_{heavy k not in {i,l}} e_k >= tau   [as dfree]
            dn = d['name']; i = d['cls']; l = d['dir']
            for r in s.roles:
                if r['name'] == dn: continue
                rn = r['name']
                D['lm %s %s' % (dn, rn)] = [frozenset([row({'s%d' % i: 1, s.c(rn, i): -1}, 0, True)]),
                                            frozenset([row({s.c(rn, l): 1, s.c(dn, l): -1}, 0, True)]),
                                            frozenset([row({s.c(rn, l): 1, s.c(dn, l): -1}, 0),
                                                       row({s.c(rn, i): 1, s.c(dn, i): -1}, 0)])]
            cost = {s.X(l): 1, s.c(dn, l): -1, 'tau': -1}
            for k in s.HV:
                if k not in (i, l): cost = lin(cost, {s.X(k): 1, 's%d' % k: -1})
            D['lfree %s' % dn] = [frozenset([row({s.c(dn, l): -1}, 0)]), frozenset([row(cost, 0)])]
        for d in s.roles:
            if d['kind'] != 'dmin': continue
            # d = argmin{c_l : c in S_i} (l = dir).  'dm d r': r not in S_i (r_i < s_i) or r_l >= d_l.
            # 'dfree d': d_l <= 0 or (x_l - d_l) + sum_{k heavy, k not in {i,l}} (x_k - s_k) >= tau.
            dn = d['name']; i = d['cls']; l = d['dir']
            for r in s.roles:
                if r['name'] == dn: continue
                rn = r['name']
                D['dm %s %s' % (dn, rn)] = [frozenset([row({'s%d' % i: 1, s.c(rn, i): -1}, 0, True)]),
                                            frozenset([row({s.c(rn, l): 1, s.c(dn, l): -1}, 0)])]
            cost = {s.X(l): 1, s.c(dn, l): -1, 'tau': -1}
            for k in s.HV:
                if k not in (i, l): cost = lin(cost, {s.X(k): 1, 's%d' % k: -1})
            D['dfree %s' % dn] = [frozenset([row({s.c(dn, l): -1}, 0)]), frozenset([row(cost, 0)])]
        for r in s.roles:
            n = r['name']
            if r['kind'] in ('min', 'dmin', 'lmin'): continue
            D['cls %s' % n] = [frozenset([row({s.c(n, i): 1, 's%d' % i: -1}, 0)]) for i in s.HV]
            va = s.void_alts(r)
            if not r.get('always_valid'):
                D['val %s' % n] = s.valid_alts(r) + va
            for i in range(s.p):
                ex = r['u'][i]
                if not ex: continue
                rows = []
                for e in ex:
                    e = lin(e); cc = F(e.pop('c', 0))
                    rows.append(row(lin(e, {s.c(n, i): -1}), -cc, i in r.get('strict', [])))
                D['ans %s %d' % (n, i)] = [frozenset(rows), frozenset([row({s.c(n, i): -1}, 0)])] + va

    def tmpl_void(s, used):
        out = []
        for n in sorted(set(used)): out += s.void_alts(s.byname[n])
        return out

    # ---------------- template failure disjunctions ----------------
    def fano_fail(s, lab):
        alts = []
        for i in range(s.p):
            if i in s.HV:
                for l in LINES:
                    d = {s.X(i): F(-2)}
                    for q in l: d = lin(d, {s.c(lab[q], i): 1})
                    alts.append(frozenset([row(d, 0, True)]))
            d = {s.X(i): F(-4)}
            for q in range(7): d = lin(d, {s.c(lab[q], i): 1})
            alts.append(frozenset([row(d, 0, True)]))
        return dedup(alts + s.tmpl_void(lab))

    def v_fail(s, a, b):
        alts = []
        for i in range(s.p):
            alts.append(frozenset([row({s.c(a, i): 1, s.c(b, i): 1, s.X(i): -1}, 0, True)]))
            alts.append(frozenset([row({s.c(a, i): F(5, 4), s.c(b, i): F(1, 2), s.X(i): -1}, 0, True)]))
        return dedup(alts + s.tmpl_void([a, b]))

    def w_fail(s, t, a, b):
        alts = []
        for i in range(s.p):
            for u, v in load_tt()[t]:
                alts.append(frozenset([row(lin({s.c(a, i): u}, {s.c(b, i): v}, {s.X(i): -1}), 0, True)]))
        return dedup(alts + s.tmpl_void([a, b]))

    def r_fail(s, sh, ks, labs):
        P, A, blines, alines = shape_data(sh)
        assert len(ks) == s.p and len(labs) == len(A)
        lab = dict(zip(A, labs)); nP = len(P)
        alts = []; us = []
        for i in range(s.p):
            xi = s.X(i)
            tot = {xi: F(4, nP)}
            for q in A: tot = lin(tot, {s.c(lab[q], i): F(-1, nP)})
            if i in s.HV:
                bounds = []
                for l in blines:
                    n = sum(1 for q in l if q in P)
                    d = {xi: F(2, n)}
                    for q in l:
                        if q not in P: d = lin(d, {s.c(lab[q], i): F(-1, n)})
                    bounds.append(d)
                bounds.append(tot)
                u = {xi: F(1)} if ks[i] == 'x' else bounds[int(ks[i])]
                for l in alines:
                    d = {xi: F(-2)}
                    for q in l: d = lin(d, {s.c(lab[q], i): 1})
                    alts.append(frozenset([row(d, 0, True)]))
                for b in bounds + [{xi: F(1)}]:
                    d = nz(lin(u, scale(b, -1)))
                    if d: alts.append(frozenset([row(d, 0, True)]))
                alts.append(frozenset([row(scale(u, -1), 0, True)]))
            else:
                if ks[i] == 'x':
                    u = {xi: F(1)}
                    alts.append(frozenset([row(nz(lin({xi: F(2, 3)}, scale(tot, -1))), 0, True)]))
                else:
                    assert ks[i] == '0'
                    u = tot
                    alts.append(frozenset([row(nz(lin(u, {xi: F(-1)})), 0, True)]))
                    alts.append(frozenset([row(scale(u, -1), 0, True)]))
            us.append(u)
        d = {'tau': F(-1)}
        for i in range(s.p): d = lin(d, {s.X(i): 1}, scale(us[i], -1))
        alts.append(frozenset([row(nz(d), 0, True)]))
        return dedup(alts + s.tmpl_void(labs))

    def template_disj(s, nm):
        kind, arg = nm.split(' ', 1)
        if kind == 'F': return s.fano_fail(arg.split(','))
        if kind == 'V':
            a, b = arg.split(','); return s.v_fail(a, b)
        if kind == 'W':
            t, ab = arg.split(':'); a, b = ab.split(','); return s.w_fail(t, a, b)
        if kind == 'R':
            sh, ks, labs = arg.split(':'); return s.r_fail(int(sh), ks, labs.split(','))
        raise ValueError(nm)


# ---------------- numeric template evaluation (heuristic only; soundness comes from the exact rows) ----------------
def eval_templates(S, R, names, x, tau, top_f=4, top_r=4, top_w=2, tol=1e-9):
    """returns dict kind -> sorted list of (margin, name) of templates with margin <= tol (most robust first)"""
    hv = np.array([i in S.HV for i in range(S.p)])
    out = {'F': [], 'V': [], 'R': [], 'W': []}
    if 'F' in S.menu:
        for k in range(1, min(S.fk, len(names)) + 1):
            combos = list(itertools.combinations(names, k))
            Rc = np.array([[R[n] for n in cb] for cb in combos])
            for pat in G.pattern_reps(k):
                Z = Rc[:, list(pat), :]
                mg = np.max(Z.sum(1) - 4 * x, axis=1)
                for l in LINES:
                    ls = Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x
                    mg = np.maximum(mg, np.max(ls[:, hv], axis=1))
                for j in np.argsort(mg)[:top_f]:
                    if mg[j] <= tol: out['F'].append((float(mg[j]), 'F ' + ','.join(combos[j][q] for q in pat)))
    if 'V' in S.menu:
        for a in names:
            for b in names:
                if a == b: continue
                mg = max(np.max(R[a] + R[b] - x), np.max(1.25 * R[a] + 0.5 * R[b] - x))
                if mg <= tol: out['V'].append((float(mg), 'V %s,%s' % (a, b)))
    if 'W' in S.menu and len(names) >= 2:
        K = np.array([R[n] for n in names])
        for t, verts in load_tt().items():
            U = np.array([[float(u), float(v)] for u, v in verts])
            val = U[:, 0][:, None, None, None] * K[None, :, None, :] + U[:, 1][:, None, None, None] * K[None, None, :, :] - x
            m = val.max(axis=(0, 3)); np.fill_diagonal(m, np.inf)
            for f in np.argsort(m, axis=None)[:top_w]:
                ia, ib = divmod(int(f), len(names))
                if m[ia, ib] <= tol: out['W'].append((float(m[ia, ib]), 'W %s:%s,%s' % (t, names[ia], names[ib])))
    if 'R' in S.menu:
        lt = ~hv
        for sh in (1, 2, 3, 4):
            P, A, blines, alines = shape_data(sh)
            nb = len(blines); nP = len(P); pos = {q: j for j, q in enumerate(A)}
            for k in range(1, min(S.rk, len(A), len(names)) + 1):
                combos = list(itertools.combinations(names, k))
                Rc = np.array([[R[n] for n in cb] for cb in combos])
                for pat in rpattern_reps(sh, k):
                    Z = Rc[:, list(pat), :]
                    C = len(combos)
                    mg = np.full(C, -np.inf)
                    for l in alines:
                        ls = Z[:, pos[l[0]]] + Z[:, pos[l[1]]] + Z[:, pos[l[2]]] - 2 * x
                        mg = np.maximum(mg, np.max(ls[:, hv], axis=1))
                    tot = (4 * x - Z.sum(1)) / nP                                  # (C,p)
                    B = []
                    for l in blines:
                        n = sum(1 for q in l if q in P)
                        B.append((2 * x - sum(Z[:, pos[q]] for q in l if q not in P)) / n)
                    B.append(tot)
                    B.append(np.broadcast_to(x, tot.shape))
                    B = np.stack(B, 0)                                             # (nb+2, C, p)
                    kk = np.argmin(B, axis=0); u = np.min(B, axis=0)
                    # light parts: 'x' if tot >= 2x/3 (cost 0), else u = tot
                    lx = tot >= 2 * x / 3
                    u = np.where(lt[None, :], np.where(lx, x, tot), u)
                    mg = np.maximum(mg, np.max(-u, axis=1))
                    mg = np.maximum(mg, (x - u).sum(1) - tau)
                    for j in np.argsort(mg)[:top_r]:
                        if mg[j] > tol: break
                        ks = ''
                        for i in range(S.p):
                            if hv[i]: ks += 'x' if kk[j, i] == nb + 1 else str(int(kk[j, i]))
                            else: ks += 'x' if lx[j, i] else '0'
                        out['R'].append((float(mg[j]), 'R %d:%s:%s' % (sh, ks, ','.join(combos[j][q] for q in pat))))
    for k in out: out[k].sort()
    return out


class EngineP(G.Engine):
    def __init__(s, S, lpbox=20.0):
        G.Engine.__init__(s, S)
        s.rv = {n: [S.VI[S.c(n, j)] for j in range(S.p)] for n in S.names}
        s.xv = [S.VI['x%d' % i] for i in range(S.p)]
        s.cache = {}
        s.void_rows = {r['name']: [s.mat(list(a)) for a in S.void_alts(r)] for r in S.roles if r['kind'] == 'req'}
        s.bounds = [((0, lpbox) if (v[0] == 'x' and int(v[1:]) in S.LT) else (-5, 5)) for v in S.VARS]
        s.strong = 4

    def lp(s, rows):
        A, b, st = s.mat(rows)
        n = s.nv
        Aub = np.hstack([-A, st[:, None].astype(float)]); bub = -b
        c = np.zeros(n + 1); c[-1] = -1
        res = linprog(c, A_ub=Aub, b_ub=bub, bounds=s.bounds + [(None, 1)], method='highs')
        if res.status == 2: return -np.inf, None
        if res.status != 0: return None, None
        return -res.fun, res.x[:n]

    def cert(s, rows):
        """exact Motzkin certificate: rationalise the float dual first (verified exactly), else gen_cert's exact path"""
        A, b, st = s.mat(rows)
        m = len(rows)
        res = linprog(-(b + st), A_ub=-b[None, :], b_ub=[0.0], A_eq=np.vstack([A.T, np.ones((1, m))]),
                      b_eq=np.concatenate([np.zeros(s.nv), [1.0]]), bounds=[(0, None)] * m, method='highs-ds')
        if res.status == 0 and -res.fun > 1e-12:
            lam = res.x
            for den in (60, 1000, 10 ** 5):
                sup = [r for r in range(m) if lam[r] > 1e-9]
                ls = [F(float(lam[r])).limit_denominator(den) for r in sup]
                rowsS = [rows[r] for r in sup]
                if all(l >= 0 for l in ls) and G.verify(rowsS, ls):
                    return [(rowsS[k], ls[k]) for k in range(len(rowsS)) if ls[k] != 0]
        return G.Engine.cert(s, rows)

    def is_void(s, n, v):
        return any(s.holds(a, v) for a in s.void_rows.get(n, []))

    def disj(s, nm):
        if nm in s.S.D: return s.S.D[nm]
        if nm not in s.cache: s.cache[nm] = s.S.template_disj(nm)
        return s.cache[nm]

    def evaluate(s, v, **kw):
        S = s.S
        x = v[s.xv]; tau = v[S.VI['tau']]
        valid = [n for n in S.names if not s.is_void(n, v)]
        R = {n: v[s.rv[n]] for n in valid}
        return eval_templates(S, R, valid, x, tau, **kw)

    def candidates(s, v, k=4):
        ev = s.evaluate(v)
        fv = sorted(ev['F'] + ev['V'])
        out = []
        for m, nm in fv[:k] + ev['R'][:k] + ev['W'][:2]:
            if nm not in out: out.append(nm)
        return out

    def pick_template(s, rows, v):
        cands = s.candidates(v, k=s.strong if s.strong else 1)
        if not cands: return None
        if not s.strong: return cands[0]
        best = None
        s.infeas = set()
        for nm in cands:
            feas = 0; inf = set()
            for ai, alt in enumerate(s.disj(nm)):
                b2, v2 = s.lp(rows + list(alt))
                if b2 is not None and b2 > 1e-9: feas += 1
                elif b2 is not None: inf.add(ai)
                if best is not None and feas >= best[0]: break
            if best is None or feas < best[0]: best = (feas, nm); s.infeas = inf
            if best[0] == 0: break
        return best[1]


def describe(S, v):
    d = {k: round(float(v[S.VI[k]]), 5) for k in ['x%d' % i for i in range(S.p)] + ['s%d' % i for i in S.HV] + ['tau']}
    roles = {n: [round(float(v[S.VI[S.c(n, j)]]), 5) for j in range(S.p)] for n in S.names}
    return d, roles


def main():
    spec_fn = sys.argv[1]; pi0 = F(sys.argv[2])
    kw = dict(a.split('=') for a in sys.argv[3:])
    spec = json.load(open(spec_fn))
    menu = tuple(kw.get('menu', 'F,V,R,W').split(','))
    S = StratP(spec, pi0, fk=int(kw.get('fk', 7)), rk=int(kw.get('rk', 4)), menu=menu)
    E = EngineP(S, lpbox=float(kw.get('lpbox', 20)))
    E.strong = int(kw.get('strong', 4))
    tag = kw.get('tag', os.path.basename(spec_fn).replace('.json', ''))
    tagp = str(pi0).replace('/', '_')
    cdir = os.path.join(HERE, 'certs'); os.makedirs(cdir, exist_ok=True)
    fin = os.path.join(cdir, 'gcertp_%s_%s.jsonl.gz' % (tag, tagp))
    body = fin + '.body'; ck = fin + '.ck.pkl'
    logf = open(os.path.join(HERE, 'logs', 'gcp_%s_%s.log' % (tag, tagp)), 'a')

    def say(m):
        print(m, flush=True); logf.write(time.strftime('%H:%M:%S ') + m + '\n'); logf.flush()

    maxnodes = int(kw.get('maxnodes', 10 ** 9))
    if kw.get('resume', '0') == '1':
        st = pickle.load(open(ck, 'rb')); stack = st['stack']; nodes = st['nodes']; nleaves = st['nleaves']; stats = st['stats']
        # read every gzip member (each resume appends one); the last may be truncated by a crash
        import zlib
        raw = open(body, 'rb').read(); data = b''
        while raw:
            dco = zlib.decompressobj(16 + zlib.MAX_WBITS)
            try: data += dco.decompress(raw)
            except zlib.error: break
            if not dco.eof: break
            raw = dco.unused_data
        data = data[:data.rfind(b'\n') + 1]
        have = data.count(b'\n')
        if have < nleaves:
            say('BODY SHORT: %d readable leaves < checkpoint %d -- run repair_bodies.py first' % (have, nleaves)); return 2
        tmp = body + '.tmp'
        with gzip.open(tmp, 'wb') as fo:
            fo.write(b'\n'.join(data.split(b'\n')[:nleaves]) + b'\n')
            fo.flush(); os.fsync(fo.fileno())
        os.replace(tmp, body)
        out = gzip.open(body, 'at')
        say('RESUME nodes %d leaves %d stack %d' % (nodes, nleaves, len(stack)))
    else:
        stack = [((), [])]; nodes = 0; nleaves = 0; stats = {}
        out = gzip.open(body, 'wt')
        say('START %s h=%d L=%d pi0=%s roles=%s menu=%s fk=%d rk=%d strong=%d erows=%s order=%s' % (
            spec_fn, S.h, S.L, pi0, S.names, menu, S.fk, S.rk, E.strong, S.erows, bool(spec.get('order'))))
    t0 = time.time(); last_ck = nodes
    while stack:
        ent = stack.pop(); nodes += 1
        path, extra = ent[0], ent[1]
        rows = S.BASE + extra
        if len(ent) > 2 and ent[2]:                  # known LP-infeasible from strong branching: certify directly
            c = E.cert(rows)
            if c is not None:
                out.write(json.dumps((list(path), [[{k: str(q) for k, q in co}, str(rhs), st_, str(l)] for (co, rhs, st_), l in c])) + '\n')
                nleaves += 1
                continue
        beta, v = E.lp(rows)
        if beta is None:
            say('LPERROR at %s' % (path,)); return 2
        if beta <= 1e-9:
            c = E.cert(rows)
            if c is None:
                say('CERTFAIL at %s' % (path,)); return 2
            out.write(json.dumps((list(path), [[{k: str(q) for k, q in co}, str(rhs), st_, str(l)] for (co, rhs, st_), l in c])) + '\n')
            nleaves += 1
            continue
        d_ok, d_sc = E.disj_status(v)
        bad = np.nonzero(~d_ok)[0]
        pick = E.names[bad[0]] if len(bad) else None
        E.infeas = set()
        if pick is None:
            pick = E.pick_template(rows, v)
        if pick is None:
            d, roles = describe(S, v)
            ev = E.evaluate(v, tol=1.0)                    # nearly-working templates (margins > 0)
            near = {k: ev[k][:4] for k in ev}
            say('ADVERSARY at depth %d (nodes %d leaves %d) beta %.6g' % (len(path), nodes, nleaves, beta))
            say('  vars %s' % d); say('  roles %s' % roles); say('  nearly-working %s' % near)
            json.dump({'v': dict(zip(S.VARS, map(float, v))), 'beta': beta, 'path': list(path), 'near': near,
                       'spec': spec, 'pi0': str(pi0)},
                      open(os.path.join(cdir, 'gadvp_%s_%s.json' % (tag, tagp)), 'w'))
            out.close()
            return 1
        kind = pick.split(' ')[0]
        stats[kind] = stats.get(kind, 0) + 1
        for ai, alt in enumerate(E.disj(pick)):
            stack.append((path + ((pick, ai),), extra + list(alt), ai in E.infeas))
        if nodes - last_ck >= 5000:
            last_ck = nodes
            out.flush(); os.fsync(out.fileno())          # body lines counted by the checkpoint must be on disk
            with open(ck + '.tmp', 'wb') as fck:
                pickle.dump({'stack': stack, 'nodes': nodes, 'nleaves': nleaves, 'stats': stats}, fck)
                fck.flush(); os.fsync(fck.fileno())
            os.replace(ck + '.tmp', ck)
            say('nodes %d leaves %d stack %d depth %d stats %s (%.0fs)' % (nodes, nleaves, len(stack), len(path), stats, time.time() - t0))
        if nodes >= maxnodes:
            say('MAXNODES'); out.close(); return 3
    out.close()
    with gzip.open(fin, 'wt') as fo, gzip.open(body, 'rt') as fi:
        fo.write(json.dumps({'pi0': str(pi0), 'strategy': spec, 'fk': S.fk, 'rk': S.rk, 'menu': list(menu),
                             'format': 'jsonl-p1'}) + '\n')
        import shutil
        shutil.copyfileobj(fi, fo)
        fo.flush(); os.fsync(fo.fileno())
    os.remove(body)
    if os.path.exists(ck): os.remove(ck)
    say('CERTIFIED leaves %d nodes %d branch stats %s -> %s (%.0fs)' % (nleaves, nodes, stats, fin, time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
