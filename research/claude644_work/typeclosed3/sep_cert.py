"""Exact branch-and-bound certificate for the SEPARATED regime with the three class minimisers only.

CLAIM SEP(pi0) [to be certified]: let x in R^3 with x_i + x_j >= 3/2 + pi0 for all pairs, sigma_i > 2x_i/3,
sigma_i <= x_i, tau > 3/4, e_i := x_i - sigma_i > tau - 3/4 (Corollary C), sum_i e_i >= tau, and three unit
vectors m^0, m^1, m^2 with 0 <= m^i <= x, m^i_i = sigma_i.  Then some template of the menu succeeds on {m^0,m^1,m^2}:
  'F' + pattern (7 labels in {0,1,2}): Fano, per part: every line sum <= 2x_i and total <= 4x_i (Lemma 7.63);
  'T3' a<=b<=c: L5 line-pencil, per part a_i+b_i+c_i <= 2x_i and sum_i max(a_i,b_i,c_i,(a_i+b_i+c_i)/2)/2 <= tau;
  'V' (a,b): 5 rows a, 2 rows b: a_i + b_i <= x_i and 5a_i/4 + b_i/2 <= x_i  (explicit support, templates_handproofs);
  (optional) 'TT' (a,b,fn): the 42 two-type capacity functions (note Thm 7.69).
Failure of a template = one of its rows violated STRICTLY.  The negation of the claim is a disjunctive system; the
tree branches on templates (one child per failure alternative) and every leaf is an infeasible linear system with
an exact Motzkin certificate: multipliers lam >= 0 over the leaf's rows (coef.v >= rhs, some strict) with
sum lam*coef = 0 and sum lam*rhs > 0, or = 0 with positive weight on a strict row.
Variables: x0..2, s0..2, tau, m<i>_<j> (i = class, j = part).
usage: python3 sep_cert.py <pi0> [menu=F,T3,V] [out=file]"""
import sys, json, itertools, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
VARS = ['x0', 'x1', 'x2', 's0', 's1', 's2', 'tau'] + ['m%d_%d' % (i, j) for i in range(3) for j in range(3)]
VI = {v: k for k, v in enumerate(VARS)}


def fano_autos():
    Ls = set(frozenset(l) for l in LINES); out = []
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[q] for q in l) in Ls for l in LINES):
            out.append(p)
    return out


AUT = fano_autos()


def patterns():
    """Fano patterns over labels {0,1,2} using all three labels, up to Fano automorphisms"""
    seen = set(); reps = []
    for pat in itertools.product(range(3), repeat=7):
        if len(set(pat)) != 3 or pat in seen: continue
        orb = set(tuple(pat[a[q]] for q in range(7)) for a in AUT)
        seen |= orb; reps.append(pat)
    return reps


def R(d, rhs, strict=False):
    """row: sum d[v]*v >= rhs (strict if flagged); stored as (frozenset of (var, Fraction)), rhs, strict"""
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))


def base_rows(pi0):
    B = []
    for i, j in itertools.combinations(range(3), 2):
        B.append(R({'x%d' % i: 1, 'x%d' % j: 1}, F(3, 2) + pi0))
    for i in range(3):
        B.append(R({'s%d' % i: 1, 'x%d' % i: F(-2, 3)}, 0, True))            # sigma_i > 2x_i/3
        B.append(R({'x%d' % i: 1, 's%d' % i: -1}, 0))                         # sigma_i <= x_i
        B.append(R({'x%d' % i: 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4), True))  # e_i > tau - 3/4
        B.append(R({'m%d_%d' % (i, i): 1, 's%d' % i: -1}, 0)); B.append(R({'m%d_%d' % (i, i): -1, 's%d' % i: 1}, 0))
        B.append(R({'m%d_%d' % (i, j): 1 for j in range(3)}, 1)); B.append(R({'m%d_%d' % (i, j): -1 for j in range(3)}, -1))
        for j in range(3):
            B.append(R({'m%d_%d' % (i, j): 1}, 0)); B.append(R({'x%d' % j: 1, 'm%d_%d' % (i, j): -1}, 0))
    B.append(R({'x0': 1, 'x1': 1, 'x2': 1, 's0': -1, 's1': -1, 's2': -1, 'tau': -1}, 0))   # E >= tau
    B.append(R({'tau': 1}, F(3, 4), True))                                                  # tau > 3/4
    return B


def viol(d):
    """failure alternative 'd.v > 0' as a strict row"""
    return R(d, 0, True)


TTV = None


def disj(name):
    """alternatives (each a frozenset of rows) of the named template's FAILURE"""
    kind, arg = name.split(' ', 1)
    alts = []
    if kind == 'F':
        pat = [int(c) for c in arg]
        for i in range(3):
            for l in LINES:
                d = {'x%d' % i: -2}
                for q in l: d['m%d_%d' % (pat[q], i)] = d.get('m%d_%d' % (pat[q], i), 0) + 1
                alts.append(frozenset([viol(d)]))
            d = {'x%d' % i: -4}
            for q in range(7): d['m%d_%d' % (pat[q], i)] = d.get('m%d_%d' % (pat[q], i), 0) + 1
            alts.append(frozenset([viol(d)]))
    elif kind == 'T3':
        a, b, c = [int(ch) for ch in arg]
        for i in range(3):
            d = {'x%d' % i: -2}
            for q in (a, b, c): d['m%d_%d' % (q, i)] = d.get('m%d_%d' % (q, i), 0) + 1
            alts.append(frozenset([viol(d)]))
        # cost > tau: for some choice of terms (one per part) sum term/2 - tau > 0
        terms = []
        for i in range(3):
            ti = [{'m%d_%d' % (q, i): F(1, 2)} for q in (a, b, c)]
            h = {}
            for q in (a, b, c): h['m%d_%d' % (q, i)] = h.get('m%d_%d' % (q, i), 0) + F(1, 4)
            ti.append(h)
            # dedupe identical terms
            u = []
            for t in ti:
                if t not in u: u.append(t)
            terms.append(u)
        for ch in itertools.product(*terms):
            d = {'tau': -1}
            for t in ch:
                for k, v in t.items(): d[k] = d.get(k, 0) + v
            alts.append(frozenset([viol(d)]))
    elif kind == 'V':
        a, b = [int(ch) for ch in arg]
        for i in range(3):
            alts.append(frozenset([viol({'m%d_%d' % (a, i): 1, 'm%d_%d' % (b, i): 1, 'x%d' % i: -1})]))
            alts.append(frozenset([viol({'m%d_%d' % (a, i): F(5, 4), 'm%d_%d' % (b, i): F(1, 2), 'x%d' % i: -1})]))
    elif kind == 'TT':
        a, b, fn = arg.split(',')
        a, b, fn = int(a), int(b), int(fn)
        for i in range(3):
            for u, v in TTV[fn]:
                d = {'x%d' % i: -1}
                if u: d['m%d_%d' % (a, i)] = d.get('m%d_%d' % (a, i), 0) + u
                if v: d['m%d_%d' % (b, i)] = d.get('m%d_%d' % (b, i), 0) + v
                alts.append(frozenset([viol(d)]))
    else:
        raise ValueError(name)
    # merge duplicate alternatives
    out = []
    for a_ in alts:
        if a_ not in out: out.append(a_)
    return out


def menu_names(menu):
    names = []
    if 'F' in menu:
        names += ['F ' + ''.join(map(str, p)) for p in patterns()]
    if 'T3' in menu:
        names += ['T3 ' + ''.join(map(str, t)) for t in itertools.combinations_with_replacement(range(3), 3)]
    if 'V' in menu:
        names += ['V %d%d' % (a, b) for a in range(3) for b in range(3) if a != b]
    if 'TT' in menu:
        names += ['TT %d,%d,%d' % (a, b, fn) for a in range(3) for b in range(3) if a != b for fn in range(len(TTV))]
    return names


def to_mat(rows):
    A = np.zeros((len(rows), len(VARS))); b = np.zeros(len(rows)); st = np.zeros(len(rows))
    for r, (co, rhs, s) in enumerate(rows):
        for k, v in co: A[r, VI[k]] = float(v)
        b[r] = float(rhs); st[r] = 1.0 if s else 0.0
    return A, b, st


def lp_margin(rows):
    """max beta s.t. A v >= b + beta*st, beta <= 1.  returns (beta, v)"""
    A, b, st = to_mat(rows)
    n = len(VARS)
    # variables v (free, bounded [-5,5]) and beta; minimise -beta;  -A v + st*beta <= -b
    Aub = np.hstack([-A, st[:, None]]); bub = -b
    c = np.zeros(n + 1); c[-1] = -1
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(-5, 5)] * n + [(None, 1)], method='highs')
    if res.status == 2:
        return -np.inf, None
    return -res.fun, res.x[:n]


def exact_cert(rows):
    """find exact Motzkin multipliers: float LP for the support, then exact nullspace solve (Fractions)."""
    A, b, st = to_mat(rows)
    m = len(rows)
    # maximise sum lam*b + sum lam*st  s.t. A^T lam = 0, lam >= 0, sum lam = 1
    c = -(b + st)
    res = linprog(c, A_ub=-b[None, :], b_ub=[0.0], A_eq=np.vstack([A.T, np.ones((1, m))]),
                  b_eq=np.concatenate([np.zeros(len(VARS)), [1.0]]), bounds=[(0, None)] * m, method='highs-ds')
    if res.status != 0 or -res.fun <= 1e-12:
        return None
    lam = res.x
    S = [r for r in range(m) if lam[r] > 1e-10]
    # exact: solve  sum_{r in S} lam_r coef_r = 0, sum lam_r = 1  (Fractions, Gaussian elimination); if the solution
    # space is larger than a point, fall back to rationalising the float solution restricted to S and re-solving
    rowsS = [rows[r] for r in S]
    sol = exact_solve(rowsS)
    if sol is not None and all(l >= 0 for l in sol) and verify_cert(rowsS, sol):
        return [(rowsS[k], sol[k]) for k in range(len(S)) if sol[k] != 0]
    sol = sympy_cert(rowsS)
    if sol is None:
        sol = sympy_cert(rows); rowsS = rows
        if sol is None: return None
    if not verify_cert(rowsS, sol):
        return None
    return [(rowsS[k], sol[k]) for k in range(len(rowsS)) if sol[k] != 0]


def sympy_cert(rowsS):
    """exact LP (sympy simplex): max sum lam*(rhs + strict) s.t. sum lam coef = 0, sum lam*rhs >= 0, lam >= 0, sum lam <= 1"""
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


def exact_solve(rowsS):
    """unique solution of lam . coef = 0 (per variable), sum lam = 1, via Fractions Gauss-Jordan; if not unique,
    choose the free variables = 0 (a basic solution)."""
    k = len(rowsS)
    M = []
    for v in VARS:
        M.append([dict(co).get(v, F(0)) for co, rhs, s in rowsS] + [F(0)])
    M.append([F(1)] * k + [F(1)])
    # Gauss-Jordan
    piv = []; r = 0
    M = [row[:] for row in M]
    for col in range(k):
        p = None
        for rr in range(r, len(M)):
            if M[rr][col] != 0: p = rr; break
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for rr in range(len(M)):
            if rr != r and M[rr][col] != 0:
                f = M[rr][col]; M[rr] = [a - f * b for a, b in zip(M[rr], M[r])]
        piv.append(col); r += 1
        if r == len(M): break
    for rr in range(r, len(M)):
        if M[rr][-1] != 0: return None      # inconsistent
    lam = [F(0)] * k
    for i, col in enumerate(piv):
        lam[col] = M[i][-1]
    return lam


def verify_cert(rowsS, lam):
    tot = {}
    for (co, rhs, s), l in zip(rowsS, lam):
        if l < 0: return False
        for kk, v in co: tot[kk] = tot.get(kk, 0) + l * v
    if any(v != 0 for v in tot.values()): return False
    val = sum(l * rhs for (co, rhs, s), l in zip(rowsS, lam))
    sw = sum(l for (co, rhs, s), l in zip(rowsS, lam) if s)
    return val > 0 or (val == 0 and sw > 0)


def row_val(row, v):
    co, rhs, s = row
    return sum(float(c) * v[VI[k]] for k, c in co) - float(rhs)


def main():
    global TTV
    pi0 = F(sys.argv[1])
    kw = dict(a.split('=') for a in sys.argv[2:])
    menu = kw.get('menu', 'F,T3,V').split(',')
    if 'TT' in menu:
        from bal_adv import TTF
        TTV = TTF
    names = menu_names(menu)
    D = {nm: disj(nm) for nm in names}
    BASE = base_rows(pi0)
    print('pi0', pi0, 'menu', menu, 'templates', len(names), flush=True)
    leaves = []; t0 = time.time(); nodes = 0; maxdepth = 0
    stack = [((), [])]          # (path of (name, alt index), extra rows)
    while stack:
        path, extra = stack.pop()
        nodes += 1
        rows = BASE + extra
        beta, v = lp_margin(rows)
        if beta <= 1e-9:
            cert = exact_cert(rows)
            if cert is None:
                print('FAILED exact certificate at depth', len(path), 'beta', beta, flush=True)
                json.dump({'path': path}, open('sep_cert_fail.json', 'w'))
                return
            leaves.append((list(path), [[{k: str(c) for k, c in co}, str(rhs), s, str(l)] for (co, rhs, s), l in cert]))
            continue
        # choose a template that SUCCEEDS at v (all failure alternatives violated at v), most robustly
        used = set(nm for nm, _ in path)
        best = None
        for nm in names:
            if nm in used: continue
            worst = max(max(row_val(r, v) for r in alt) for alt in D[nm])   # >0 means some failure row holds at v
            if worst <= 1e-12:
                key = (worst, len(D[nm]))
                if best is None or key < best[0]: best = (key, nm)
        if best is None:
            print('ADVERSARY at depth', len(path), 'beta %.6g' % beta, 'v', dict(zip(VARS, np.round(v, 6))), flush=True)
            json.dump({'path': path, 'v': list(v), 'beta': beta}, open('sep_cert_adv.json', 'w'))
            return
        nm = best[1]
        for ai, alt in enumerate(D[nm]):
            stack.append((path + ((nm, ai),), extra + list(alt)))
        maxdepth = max(maxdepth, len(path) + 1)
        if nodes % 2000 == 0:
            print(' nodes %d leaves %d stack %d depth %d (%.0fs)' % (nodes, len(leaves), len(stack), maxdepth, time.time() - t0), flush=True)
    out = kw.get('out', 'sep_cert_%s.json' % str(pi0).replace('/', '_'))
    json.dump({'pi0': str(pi0), 'menu': menu, 'vars': VARS, 'leaves': leaves}, open(out, 'w'))
    print('CERTIFIED: leaves %d nodes %d maxdepth %d (%.0fs) -> %s' % (len(leaves), nodes, maxdepth, time.time() - t0, out))


if __name__ == '__main__':
    main()
