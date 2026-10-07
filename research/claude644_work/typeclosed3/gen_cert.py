"""General exact branch-and-bound engine for role strategies in the SEPARATED regime (Lemma SEP), producing
independently checkable certificates (check_gen_cert.py).

Model.  Variables: x0..2, s0..2 (sigma), tau, and c<r>_<j> for every role r (coordinate j).
BASE rows (hypotheses): pair sums x_i + x_j >= 3/2 + pi0; sigma_i > 2x_i/3; sigma_i <= x_i; x_i - sigma_i > tau - 3/4
(Cor. C); sum e_i >= tau; tau > 3/4; for every role r: sum_j c_rj = 1, 0 <= c_rj <= x_j;
minimiser roles 'm<i>': c_ii = sigma_i.
DISJUNCTIONS (each must have one alternative true; an alternative = conjunction of rows):
  'cls r'      : role r lies in some class: {c_r0 >= sigma_0} | {c_r1 >= sigma_1} | {c_r2 >= sigma_2}
                 (every type is super-heavy somewhere and S_i = {c_i >= sigma_i} in the separated regime);
  'ans r i'    : (request roles, when valid) c_ri <= max(0, min_k e_rik):  {c_ri <= e_rik for all k} | {c_ri <= 0}
                 [for a void request the alternative 'void r ...' is available: see below]
  'val r'      : request r is valid or void.  valid <=> sum_i min(x_i, max_k (x_i - e_rik)) <= tau.
                 alternatives: 'valid' = for some S subset of parts: sum_{i in S} x_i + sum_{i not in S}(x_i - e_{r,i,k_i})
                 <= tau for ALL k-choices (one alternative per S; rows = all k-choices);
                 'void' = for some k-choice: for all S: sum_{S} x_i + sum_{not S}(x_i - e_{i,k_i}) > tau (one
                 alternative per k-choice).  The engine records in the path which alternative was taken; 'ans r i'
                 disjunctions and templates using r are required only in branches where r is valid -- to keep the
                 certificate format simple, every 'ans r i' and every template using r carries the extra alternatives
                 of 'void r' (so a void request makes them trivially satisfiable).
  templates   : failure disjunction (one strictly violated row) + the void alternatives of its request roles.
Leaves: exact Motzkin certificates.  usage: python3 gen_cert.py <strategy.json> <pi0> [out=..] [fk=4] [menu=F,V,T3]
strategy.json: {"roles": [{"name":"m0","kind":"min","cls":0}, {"name":"v0","kind":"req","u":[[expr..],[..],[..]],
               "always_valid": true}, ...]}   expr = {var: coef, 'c': const} over x*, s*, tau, c<role>_<j>.
"""
import sys, json, itertools, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def fano_autos():
    Ls = set(frozenset(l) for l in LINES); out = []
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[q] for q in l) in Ls for l in LINES):
            out.append(p)
    return out


AUT = fano_autos()
_PAT = {}


def pattern_reps(k):
    if k in _PAT: return _PAT[k]
    seen = set(); reps = []
    for pat in itertools.product(range(k), repeat=7):
        if len(set(pat)) != k or pat in seen: continue
        orb = set(tuple(pat[a[q]] for q in range(7)) for a in AUT)
        seen |= orb; reps.append(pat)
    _PAT[k] = reps
    return reps


def row(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))


def lin(*ds):
    out = {}
    for d in ds:
        for k, v in d.items(): out[k] = out.get(k, 0) + F(v)
    return out


def scale(d, a):
    return {k: F(v) * a for k, v in d.items()}


class Strategy:
    def __init__(s, spec, pi0, fk=4, menu=('F', 'V', 'T3'), lazy=False):
        s.lazy = lazy
        s.spec = spec; s.roles = spec['roles']; s.pi0 = F(pi0); s.fk = fk; s.menu = menu
        s.mode = spec.get('mode', 'sep'); s.pairs = spec.get('pairs', [])
        s.names = [r['name'] for r in s.roles]
        s.VARS = ['x0', 'x1', 'x2', 's0', 's1', 's2', 'tau'] + (['t0', 't1', 't2'] if s.mode == 'caseA' else []) + \
            ['c%s_%d' % (nm, j) for nm in s.names for j in range(3)]
        s.VI = {v: k for k, v in enumerate(s.VARS)}
        s.BASE = s.base()
        s.D = {}
        s.build_disj()

    def c(s, r, j):
        return 'c%s_%d' % (r, j)

    def region_rows(s):
        """optional REGION restrictions (a certificate then proves the claim only on the region):
        'order': true -> x_0 <= x_1 <= x_2 (legitimate WLOG only for a strategy invariant under permuting the parts;
        the checker verifies the invariance); 'xbox': [[i, lo, hi], ...] -> lo <= x_i <= hi;
        'pairs' in sep mode: extra [i, j, lo, hi] bounds on x_i + x_j."""
        B = []
        sp = s.spec
        if sp.get('order'):
            B.append(row({'x1': 1, 'x0': -1}, 0)); B.append(row({'x2': 1, 'x1': -1}, 0))
        for i, lo, hi in sp.get('xbox', []):
            if lo is not None: B.append(row({'x%d' % i: 1}, F(lo)))
            if hi is not None: B.append(row({'x%d' % i: -1}, -F(hi)))
        if sp.get('taubox'):
            lo, hi = sp['taubox']
            if lo is not None: B.append(row({'tau': 1}, F(lo)))
            if hi is not None: B.append(row({'tau': -1}, -F(hi)))
        if s.mode == 'sep':
            for i, j, lo, hi in sp.get('pairs', []):
                if lo is not None: B.append(row({'x%d' % i: 1, 'x%d' % j: 1}, F(lo)))
                if hi is not None: B.append(row({'x%d' % i: -1, 'x%d' % j: -1}, -F(hi)))
        return B

    def base(s):
        if s.mode == 'caseA':
            return s.base_caseA() + s.region_rows()
        B = s.region_rows()
        for i, j in itertools.combinations(range(3), 2):
            B.append(row({'x%d' % i: 1, 'x%d' % j: 1}, F(3, 2) + s.pi0))
        for i in range(3):
            B.append(row({'s%d' % i: 1, 'x%d' % i: F(-2, 3)}, 0, True))
            B.append(row({'x%d' % i: 1, 's%d' % i: -1}, 0))
            B.append(row({'x%d' % i: 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4), True))
        B.append(row({'x0': 1, 'x1': 1, 'x2': 1, 's0': -1, 's1': -1, 's2': -1, 'tau': -1}, 0))
        B.append(row({'tau': 1}, F(3, 4), True))
        for r in s.roles:
            nm = r['name']
            B.append(row({s.c(nm, j): 1 for j in range(3)}, 1)); B.append(row({s.c(nm, j): -1 for j in range(3)}, -1))
            for j in range(3):
                B.append(row({s.c(nm, j): 1}, 0)); B.append(row({'x%d' % j: 1, s.c(nm, j): -1}, 0))
            if r['kind'] == 'min':
                i = r['cls']
                B.append(row({s.c(nm, i): 1, 's%d' % i: -1}, 0)); B.append(row({s.c(nm, i): -1, 's%d' % i: 1}, 0))
        return B

    def base_caseA(s):
        """case (A) of Theorem A1 (maximal free box t >= sigma with pure facet blockers), Corollary C, Theorem TP;
        spec 'pairs': [[i, j, lo, hi], ...] optional bounds on x_i + x_j (strings or null); pi0 unused."""
        B = []
        for i, j, lo, hi in s.pairs:
            if lo is not None: B.append(row({'x%d' % i: 1, 'x%d' % j: 1}, F(lo)))
            if hi is not None: B.append(row({'x%d' % i: -1, 'x%d' % j: -1}, -F(hi)))
        for i in range(3):
            B.append(row({'s%d' % i: 1, 'x%d' % i: F(-2, 3)}, 0, True))            # sigma_i > 2x_i/3
            B.append(row({'t%d' % i: 1, 's%d' % i: -1}, 0))                       # t_i >= sigma_i
            B.append(row({'x%d' % i: 1, 't%d' % i: -1}, 0))                       # t_i <= x_i
            B.append(row({'x%d' % i: 1, 't%d' % i: -1, 'tau': -1}, F(-3, 4), True))   # e'_i > eta (Cor. C)
            B.append(row({'x%d' % i: 1, 'tau': -2}, F(-3, 2), True))               # x_i > 2 eta (Thm TP)
        B.append(row({'x0': 1, 'x1': 1, 'x2': 1, 't0': -1, 't1': -1, 't2': -1, 'tau': -1}, 0))   # cost(t) >= tau
        B.append(row({'tau': 1}, F(3, 4), True))
        for r in s.roles:
            nm = r['name']
            B.append(row({s.c(nm, j): 1 for j in range(3)}, 1)); B.append(row({s.c(nm, j): -1 for j in range(3)}, -1))
            for j in range(3):
                B.append(row({s.c(nm, j): 1}, 0)); B.append(row({'x%d' % j: 1, s.c(nm, j): -1}, 0))
            if r['kind'] == 'min':
                i = r['cls']
                B.append(row({s.c(nm, i): 1, 's%d' % i: -1}, 0)); B.append(row({s.c(nm, i): -1, 's%d' % i: 1}, 0))
            if r['kind'] == 'blk':
                i = r['facet']
                B.append(row({s.c(nm, i): 1, 't%d' % i: -1}, 0)); B.append(row({s.c(nm, i): -1, 't%d' % i: 1}, 0))
                for j in range(3):
                    if j != i: B.append(row({'t%d' % j: 1, s.c(nm, j): -1}, 0, True))     # c_j < t_j
        return B

    def exprs(s, r, i):
        return [lin(e) for e in r['u'][i]]

    def void_alts(s, r):
        """alternatives expressing 'request r is void' (cost > tau)"""
        if r.get('always_valid'): return []
        per = []
        for i in range(3):
            per.append(s.exprs(r, i) + [{'x%d' % i: 1}])        # u_i <= x_i always
        alts = []
        for ks in itertools.product(*[range(len(p)) for p in per]):
            rows = []
            for S in itertools.product([0, 1], repeat=3):          # S_i = 1: part i contributes x_i (u_i = 0)
                d = {'tau': -1}; cst = F(0)
                for i in range(3):
                    if S[i]:
                        d = lin(d, {'x%d' % i: 1})
                    else:
                        e = dict(per[i][ks[i]]); cc = F(e.pop('c', 0))
                        d = lin(d, {'x%d' % i: 1}, scale(e, -1)); cst -= cc
                # sum > tau  <=>  d.v + cst > 0  <=> d.v > -cst
                rows.append(row(d, -cst, not r.get('strict')))     # strict request: void <=> cost >= tau
            alts.append(frozenset(rows))
        return alts

    def lex_alts(s, r):
        """EXTREMAL answer: r's answer minimises c_l (l = r['lex']) over the types in the box u; then the box
        {w_l < c_l, w_j <= u_j (j != l)} is free, so  (x_l - c_l) + sum_{j != l} cost_j(u) >= tau  with
        cost_j(u) = min(x_j, max_k (x_j - e_jk)).  Since sum_j min(x_j, max_k a_jk) = max_k min_S [...], this holds
        iff for SOME expression choice k: for ALL S subset of parts != l:
            (x_l - c_l) + sum_{j in S} x_j + sum_{j not in S} (x_j - e_{j,k_j}) >= tau."""
        l = r['lex']; nm = r['name']
        others = [j for j in range(3) if j != l]
        per = {j: s.exprs(r, j) + [{'x%d' % j: 1}] for j in others}
        alts = []
        for ks in itertools.product(*[range(len(per[j])) for j in others]):
            rows = []
            for S in itertools.product([0, 1], repeat=len(others)):
                d = {'x%d' % l: 1, s.c(nm, l): -1, 'tau': -1}; cst = F(0)
                for jj, j in enumerate(others):
                    if S[jj]:
                        d = lin(d, {'x%d' % j: 1})
                    else:
                        e = dict(per[j][ks[jj]]); cc = F(e.pop('c', 0))
                        d = lin(d, {'x%d' % j: 1}, scale(e, -1)); cst -= cc
                rows.append(row(d, -cst))
            alts.append(frozenset(rows))
        return alts

    def valid_alts(s, r):
        per = []
        for i in range(3):
            per.append(s.exprs(r, i) + [{'x%d' % i: 1}])
        alts = []
        for S in itertools.product([0, 1], repeat=3):
            rows = []
            for ks in itertools.product(*[range(len(p)) for p in per]):
                d = {'tau': 1}; cst = F(0)
                for i in range(3):
                    if S[i]:
                        d = lin(d, {'x%d' % i: -1})
                    else:
                        e = dict(per[i][ks[i]]); cc = F(e.pop('c', 0))
                        d = lin(d, {'x%d' % i: -1}, e); cst += cc
                # tau - cost >= 0  <=> d.v + cst >= 0
                rows.append(row(d, -cst, bool(r.get('strict'))))  # strict request: valid <=> cost < tau
            alts.append(frozenset(rows))
        return alts

    def build_disj(s):
        D = s.D
        byname = {r['name']: r for r in s.roles}
        s.byname = byname
        for r in s.roles:
            nm = r['name']
            if s.mode == 'caseA':
                for i in range(3):
                    D['gap %s %d' % (nm, i)] = [frozenset([row({'x%d' % i: F(2, 3), s.c(nm, i): -1}, 0)]),
                                                frozenset([row({s.c(nm, i): 1, 's%d' % i: -1}, 0)])]
                D['sh %s' % nm] = [frozenset([row({s.c(nm, i): 1, 's%d' % i: -1}, 0)]) for i in range(3)]
                D['bk %s' % nm] = [frozenset([row({s.c(nm, i): 1, 't%d' % i: -1}, 0)]) for i in range(3)]
            elif r['kind'] != 'min':
                D['cls %s' % nm] = [frozenset([row({s.c(nm, i): 1, 's%d' % i: -1}, 0)]) for i in range(3)]
            if r['kind'] == 'req':
                va = s.void_alts(r)
                if not r.get('always_valid'):
                    D['val %s' % nm] = s.valid_alts(r) + va
                for i in range(3):
                    ex = s.exprs(r, i)
                    if not ex: continue
                    rows = []
                    for e in ex:
                        e = dict(e); cc = F(e.pop('c', 0))
                        rows.append(row(lin(e, {s.c(nm, i): -1}), -cc, i in r.get('strict', [])))  # e - c_ri >= 0 (> 0 if strict part)
                    alts = [frozenset(rows), frozenset([row({s.c(nm, i): -1}, 0)])] + va
                    D['ans %s %d' % (nm, i)] = alts
                if r.get('lex') is not None:
                    assert not r.get('strict'), 'lex answers only for non-strict requests'
                    D['lex %s' % nm] = s.lex_alts(r) + [frozenset([row({s.c(nm, r['lex']): -1}, 0)])] + va
        # templates
        roles = s.names
        if s.lazy: return
        if 'F' in s.menu:
            for k in range(1, s.fk + 1):
                for combo in itertools.combinations(roles, k):
                    for pat in pattern_reps(k):
                        lab = [combo[p] for p in pat]
                        D['F ' + ','.join(lab)] = s.fano_fail(lab)
        if 'V' in s.menu:
            for a in roles:
                for b in roles:
                    if a != b: D['V %s,%s' % (a, b)] = s.v_fail(a, b)
        if 'T3' in s.menu:
            for t in itertools.combinations_with_replacement(roles, 3):
                D['T3 ' + ','.join(t)] = s.t3_fail(t)

    def tmpl_void(s, used):
        out = []
        for nm in sorted(set(used)):
            r = s.byname[nm]
            if r['kind'] == 'req': out += s.void_alts(r)
        return out

    def fano_fail(s, lab):
        alts = []
        for i in range(3):
            for l in LINES:
                d = {'x%d' % i: -2}
                for q in l: d = lin(d, {s.c(lab[q], i): 1})
                alts.append(frozenset([row(d, 0, True)]))
            d = {'x%d' % i: -4}
            for q in range(7): d = lin(d, {s.c(lab[q], i): 1})
            alts.append(frozenset([row(d, 0, True)]))
        return dedup(alts + s.tmpl_void(lab))

    def v_fail(s, a, b):
        alts = []
        for i in range(3):
            alts.append(frozenset([row({s.c(a, i): 1, s.c(b, i): 1, 'x%d' % i: -1}, 0, True)]))
            alts.append(frozenset([row({s.c(a, i): F(5, 4), s.c(b, i): F(1, 2), 'x%d' % i: -1}, 0, True)]))
        return dedup(alts + s.tmpl_void([a, b]))

    def t3_fail(s, t):
        alts = []
        for i in range(3):
            d = {'x%d' % i: -2}
            for q in t: d = lin(d, {s.c(q, i): 1})
            alts.append(frozenset([row(d, 0, True)]))
        per = []
        for i in range(3):
            ts = []
            for q in t:
                tt = {s.c(q, i): F(1, 2)}
                if tt not in ts: ts.append(tt)
            h = {}
            for q in t: h = lin(h, {s.c(q, i): F(1, 4)})
            if h not in ts: ts.append(h)
            per.append(ts)
        for ch in itertools.product(*per):
            d = lin({'tau': -1}, *ch)
            alts.append(frozenset([row(d, 0, True)]))
        return dedup(alts + s.tmpl_void(list(t)))


def dedup(alts):
    out = []
    for a in alts:
        if a not in out: out.append(a)
    return out


class Engine:
    def __init__(s, S):
        s.S = S; s.nv = len(S.VARS)
        s.names = list(S.D.keys())
        # global row table: every distinct row once; alternatives = index arrays; vectorised evaluation
        ridx = {}; rows = []
        s.alt_rows = {}
        for nm, alts in S.D.items():
            lst = []
            for a in alts:
                ids = []
                for r in a:
                    if r not in ridx: ridx[r] = len(rows); rows.append(r)
                    ids.append(ridx[r])
                lst.append(np.array(sorted(ids), dtype=np.int64))
            s.alt_rows[nm] = lst
        s.GA, s.Gb, s.Gst = s.mat(rows) if rows else (np.zeros((0, s.nv)), np.zeros(0), np.zeros(0, dtype=bool))
        s.isrole = np.array([nm.split(' ')[0] in ('cls', 'val', 'ans', 'gap', 'sh', 'bk', 'lex') for nm in s.names])
        # flattened structure for reduceat: alternatives in order, disjunctions in order
        flat = []; alt_start = []; disj_start = []; nalt = 0
        for nm in s.names:
            disj_start.append(nalt)
            for ids in s.alt_rows[nm]:
                alt_start.append(len(flat)); flat.extend(ids.tolist() if len(ids) else [-1]); nalt += 1
        s.flat = np.array(flat, dtype=np.int64); s.alt_start = np.array(alt_start, dtype=np.int64); s.disj_start = np.array(disj_start, dtype=np.int64)
        s.nalt = nalt

    def disj_status(s, v, tol=1e-9):
        """per disjunction: (holds: some alternative true at v, score: max over alternatives of min row slack)"""
        if len(s.names) == 0:
            return np.zeros(0, dtype=bool), np.zeros(0)
        vals = s.GA @ v - s.Gb
        ok = np.where(s.Gst, vals > tol, vals >= -tol)
        okx = np.concatenate([ok, [True]]); valx = np.concatenate([vals, [1.0]])
        alt_ok = np.logical_and.reduceat(okx[s.flat], s.alt_start)
        alt_sl = np.minimum.reduceat(valx[s.flat], s.alt_start)
        d_ok = np.logical_or.reduceat(alt_ok, s.disj_start)
        d_sc = np.maximum.reduceat(alt_sl, s.disj_start)
        return d_ok, d_sc

    def mat(s, rows):
        A = np.zeros((len(rows), s.nv)); b = np.zeros(len(rows)); st = np.zeros(len(rows), dtype=bool)
        for r, (co, rhs, strict) in enumerate(rows):
            for k, v in co: A[r, s.S.VI[k]] = float(v)
            b[r] = float(rhs); st[r] = strict
        return A, b, st

    def lp(s, rows):
        A, b, st = s.mat(rows)
        n = s.nv
        Aub = np.hstack([-A, st[:, None].astype(float)]); bub = -b
        c = np.zeros(n + 1); c[-1] = -1
        res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(-5, 5)] * n + [(None, 1)], method='highs')
        if res.status == 2: return -np.inf, None
        if res.status != 0: return None, None
        return -res.fun, res.x[:n]

    def holds(s, alt, v, tol=1e-9):
        A, b, st = alt
        val = A @ v - b
        return bool(np.all(np.where(st, val > tol, val >= -tol)))

    def slack(s, alt, v):
        A, b, st = alt
        return float(np.min(A @ v - b)) if len(b) else 1.0

    def cert(s, rows):
        A, b, st = s.mat(rows)
        m = len(rows)
        res = linprog(-(b + st), A_ub=-b[None, :], b_ub=[0.0], A_eq=np.vstack([A.T, np.ones((1, m))]),
                      b_eq=np.concatenate([np.zeros(s.nv), [1.0]]), bounds=[(0, None)] * m, method='highs-ds')
        if res.status != 0 or -res.fun <= 1e-12: return None
        lam = res.x; Sup = [r for r in range(m) if lam[r] > 1e-10]
        rowsS = [rows[r] for r in Sup]
        from exact_lp import motzkin
        sol = gauss_cert(rowsS)
        if sol is not None and all(l >= 0 for l in sol) and verify(rowsS, sol):
            return [(rowsS[k], sol[k]) for k in range(len(rowsS)) if sol[k] != 0]
        sol = motzkin(rowsS, s.S.VARS)
        if sol is None:
            Sup = [r for r in range(m) if lam[r] > 1e-13]; rowsS = [rows[r] for r in Sup]
            sol = motzkin(rowsS, s.S.VARS)
        if sol is None:
            s.slow = getattr(s, 'slow', 0) + 1
            print('  (slow exact certificate on all %d rows)' % len(rows), flush=True)
            sol = motzkin(rows, s.S.VARS); rowsS = rows
            if sol is None: return None
        if not verify(rowsS, sol): return None
        return [(rowsS[k], sol[k]) for k in range(len(rowsS)) if sol[k] != 0]

    def run(s, maxnodes=10 ** 7, verbose=True, order_first=('cls', 'val', 'ans')):
        leaves = []; nodes = 0; t0 = time.time()
        stack = [((), [])]
        while stack:
            path, extra = stack.pop(); nodes += 1
            rows = s.S.BASE + extra
            beta, v = s.lp(rows)
            if beta is None:
                return 'LPERROR', path, None
            if beta <= 1e-9:
                c = s.cert(rows)
                if c is None: return 'CERTFAIL', path, None
                leaves.append((list(path), [[{k: str(x) for k, x in co}, str(rhs), st, str(l)] for (co, rhs, st), l in c]))
                continue
            d_ok, d_sc = s.disj_status(v)
            pick = None
            bad = np.nonzero(~d_ok)[0]
            rb = [k for k in bad if s.isrole[k]]
            if rb:
                pick = s.names[rb[0]]
            elif len(bad):
                k = bad[np.argmin(d_sc[bad])]            # template succeeding most robustly at v
                pick = s.names[k]
            if pick is None:
                return 'ADVERSARY', path, (beta, v)
            for ai, alt in enumerate(s.S.D[pick]):
                stack.append((path + ((pick, ai),), extra + list(alt)))
            if verbose and nodes % 500 == 0:
                print(' nodes %d leaves %d stack %d depth %d (%.0fs)' % (nodes, len(leaves), len(stack), len(path), time.time() - t0), flush=True)
            if nodes > maxnodes: return 'MAXNODES', None, None
        return 'CERTIFIED', leaves, nodes


def gauss_cert(rowsS):
    """unique solution of sum lam coef = 0, sum lam = 1 on the support (Fractions Gauss-Jordan), else None"""
    k = len(rowsS)
    used = sorted(set(v for co, rhs, st in rowsS for v, c in co))
    M = [[dict(co).get(v, F(0)) for co, rhs, st in rowsS] + [F(0)] for v in used] + [[F(1)] * k + [F(1)]]
    r = 0; piv = []
    for col in range(k):
        p = next((rr for rr in range(r, len(M)) if M[rr][col] != 0), None)
        if p is None: return None                      # dependent columns: not unique
        M[r], M[p] = M[p], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for rr in range(len(M)):
            if rr != r and M[rr][col] != 0:
                f = M[rr][col]; M[rr] = [a - f * b for a, b in zip(M[rr], M[r])]
        piv.append(col); r += 1
    if any(M[rr][-1] != 0 for rr in range(r, len(M))): return None
    return [M[i][-1] for i in range(k)]


def sympy_cert(rowsS, VARS):
    import sympy
    from sympy.solvers.simplex import lpmax
    n = len(rowsS); lam = sympy.symbols('l0:%d' % n)
    cons = []
    for v in VARS:
        e = sum(sympy.Rational(dict(co).get(v, 0)) * lam[i] for i, (co, rhs, s_) in enumerate(rowsS))
        if e != 0: cons.append(sympy.Eq(e, 0))
    cons += [l >= 0 for l in lam]; cons.append(sum(lam) <= 1)
    cons.append(sum(sympy.Rational(rhs) * lam[i] for i, (co, rhs, s_) in enumerate(rowsS)) >= 0)
    obj = sum((sympy.Rational(rhs) + (1 if s_ else 0)) * lam[i] for i, (co, rhs, s_) in enumerate(rowsS))
    try:
        val, sol = lpmax(obj, cons)
    except Exception:
        return None
    if val <= 0: return None
    return [F(str(sympy.Rational(sol[l]))) for l in lam]


def verify(rowsS, lam):
    tot = {}
    for (co, rhs, st), l in zip(rowsS, lam):
        if l < 0: return False
        for k, v in co: tot[k] = tot.get(k, 0) + l * v
    if any(v != 0 for v in tot.values()): return False
    val = sum(l * rhs for (co, rhs, st), l in zip(rowsS, lam))
    sw = sum(l for (co, rhs, st), l in zip(rowsS, lam) if st)
    return val > 0 or (val == 0 and sw > 0)


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2])
    kw = dict(a.split('=') for a in sys.argv[3:])
    S = Strategy(spec, pi0, fk=int(kw.get('fk', 4)), menu=tuple(kw.get('menu', 'F,V,T3').split(',')))
    E = Engine(S)
    print('strategy', sys.argv[1], 'roles', S.names, 'pi0', pi0, 'disjunctions', len(S.D), flush=True)
    t0 = time.time()
    st, a, b = E.run()
    print(st, '(%.0fs)' % (time.time() - t0))
    if st == 'CERTIFIED':
        out = kw.get('out', 'certs/gcert_%s_%s.json' % (sys.argv[1].split('/')[-1].replace('.json', ''), str(pi0).replace('/', '_')))
        json.dump({'pi0': str(pi0), 'strategy': spec, 'fk': S.fk, 'menu': list(S.menu), 'leaves': a}, open(out, 'w'))
        print('leaves', len(a), 'nodes', b, '->', out)
    elif st == 'ADVERSARY':
        beta, v = b
        print('path', a)
        print('beta %.6g' % beta, {k: round(float(x), 5) for k, x in zip(S.VARS, v)})
        json.dump({'path': a, 'v': dict(zip(S.VARS, map(float, v))), 'beta': beta}, open('certs/gadv_%s_%s.json' % (sys.argv[1].split('/')[-1].replace('.json', ''), str(pi0).replace('/', '_')), 'w'))
    else:
        print(a)
