# [templates#1] BREAK-IT referee (w9): COMPLETE role-reduced MILP search for a counterexample to Theorem 2UB.
#
# Reduction (hand, valid for ANY number of parts p): a counterexample to 2UB for a heavy pair (I,J) consists of
#   * canonical a = g+(1-|g|)e_J, b = h+(1-|h|)e_I NOT admissible (a_J > x_J or b_I > x_I), or
#   * a part K where Q_b fails, a part L where Q_a fails, a part M where V(a,b) fails.
# Keep only the "role" parts {I,J,K,L,M} (identified according to a set partition), lump all other parts into
# rest masses g_rest, h_rest >= 0 (they only enter through |g|, |h|).  Every hypothesis (K1'),(K2') among role parts
# is kept; those involving other parts and (K0) are dropped -> a RELAXATION.  Hence: if the relaxed MILP has
# max margin eps <= 0 for every identification pattern, there is no counterexample for any p.
# WLOG x_i <= 2 (lowering x_i > 2 to 2 keeps all hypotheses: x_i-g_i >= 1 >= 3/4, i is never heavy, never a
# template failure since all template values are <= 7/4, never an admissibility failure since a_J,b_I <= 1).
# NUMERICAL (HiGHS MILP), complete over all real parameters in the relaxation.
import sys, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def set_partitions(elems):
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for part in set_partitions(rest):
        for k in range(len(part)):
            yield part[:k] + [[first] + part[k]] + part[k + 1:]
        yield [[first]] + part

THR = float(sys.argv[1]) if len(sys.argv) > 1 else 0.75
MUT = sys.argv[2] if len(sys.argv) > 2 else ''     # mutation: noV, noQa, noQb, fillown
BIG = 10.0

def solve(pattern, mode):
    # pattern: list of blocks of role names; mode 'tmpl' (K,L,M failures) or 'adm' (admissibility failure)
    roles = {}
    for bi, blk in enumerate(pattern):
        for r in blk: roles[r] = bi
    q = len(pattern)
    names = []
    def var(n):
        names.append(n); return len(names) - 1
    X = [var(f'x{i}') for i in range(q)]; G = [var(f'g{i}') for i in range(q)]; Hh = [var(f'h{i}') for i in range(q)]
    gr = var('grest'); hr = var('hrest'); eps = var('eps')
    zg = [var(f'zg{i}') for i in range(q)]; zh = [var(f'zh{i}') for i in range(q)]; w = [var(f'w{i}') for i in range(q)]
    rows = []; lo = []; hi = []
    nv = lambda: None
    def add(coefs, l, h):
        r = np.zeros(len(names) + 16);
        for k, c in coefs: r[k] += c
        rows.append(r); lo.append(l); hi.append(h)
    binaries = zg + zh + w
    fb = []   # failure-choice binaries
    I, J = roles['I'], roles['J']
    # a_i, b_i as linear expressions: dict var->coef, const
    def aexpr(i):
        e = {G[i]: 1.0}; c = 0.0
        if MUT == 'fillown':
            if i == I:
                c += 1.0;
                for j in range(q): e[G[j]] = e.get(G[j], 0) - 1.0
                e[gr] = e.get(gr, 0) - 1.0
        elif i == J:
            c += 1.0
            for j in range(q): e[G[j]] = e.get(G[j], 0) - 1.0
            e[gr] = e.get(gr, 0) - 1.0
        return e, c
    def bexpr(i):
        e = {Hh[i]: 1.0}; c = 0.0
        if MUT == 'fillown':
            if i == J:
                c += 1.0
                for j in range(q): e[Hh[j]] = e.get(Hh[j], 0) - 1.0
                e[hr] = e.get(hr, 0) - 1.0
        elif i == I:
            c += 1.0
            for j in range(q): e[Hh[j]] = e.get(Hh[j], 0) - 1.0
            e[hr] = e.get(hr, 0) - 1.0
        return e, c
    def lin(*terms):  # terms: (coef, (dict,const)) -> (dict,const)
        d = {}; c = 0.0
        for k, (e, cc) in terms:
            for v, cf in e.items(): d[v] = d.get(v, 0) + k * cf
            c += k * cc
        return d, c
    Xe = lambda i: ({X[i]: 1.0}, 0.0)
    def geq(expr, rhs, extra=()):   # expr >= rhs + sum(coef*var) for relax terms in extra
        d, c = expr
        coefs = list(d.items()) + [(v, -cf) for v, cf in extra]
        add(coefs, rhs - c, np.inf)
    # basic bounds / sums
    for i in range(q):
        geq(lin((1, Xe(i)), (-1, ({G[i]: 1.0}, 0.0))), 0.0)   # g <= x
        geq(lin((1, Xe(i)), (-1, ({Hh[i]: 1.0}, 0.0))), 0.0)
        add([(G[i], 1.0), (zg[i], -1.0)], -np.inf, 0.0)          # g_i <= zg_i
        add([(Hh[i], 1.0), (zh[i], -1.0)], -np.inf, 0.0)
    add([(G[i], 1.0) for i in range(q)] + [(gr, 1.0)], -np.inf, 1.0)
    add([(Hh[i], 1.0) for i in range(q)] + [(hr, 1.0)], -np.inf, 1.0)
    # (K1') if zg_i=zh_i=1: x_i-g_i >= THR or x_i-h_i >= THR   (w_i chooses)
    for i in range(q):
        # x_i - g_i >= THR - BIG*(1-w_i) - BIG*(2-zg-zh)
        add([(X[i], 1), (G[i], -1), (w[i], -BIG), (zg[i], -BIG), (zh[i], -BIG)], THR - 3 * BIG, np.inf)
        add([(X[i], 1), (Hh[i], -1), (w[i], BIG), (zg[i], -BIG), (zh[i], -BIG)], THR - 2 * BIG, np.inf)
    # (K2') i != j
    for i in range(q):
        for j in range(q):
            if i != j:
                add([(X[i], 1), (G[i], -1), (X[j], 1), (Hh[j], -1), (zg[i], -BIG), (zh[j], -BIG)], THR - 2 * BIG, np.inf)
    # heaviness (strict, margin eps): g_I >= 4x_I/7 + eps, h_J >= 4x_J/7 + eps
    add([(G[I], 1), (X[I], -4 / 7), (eps, -1)], 0.0, np.inf)
    add([(Hh[J], 1), (X[J], -4 / 7), (eps, -1)], 0.0, np.inf)
    def fail_or(exprs):   # at least one expr >= eps  (expr is (dict,const) meaning value - x > 0)
        bs = [var(f'f{len(names)}') for _ in exprs]
        for bvar, ex in zip(bs, exprs):
            d, c = ex
            add(list(d.items()) + [(eps, -1), (bvar, -BIG)], -c - BIG, np.inf)   # ex - eps >= -BIG(1-b)
        add([(bv, 1.0) for bv in bs], 1.0, np.inf)
        fb.extend(bs)
    if mode == 'adm':
        J_, I_ = J, I
        fail_or([lin((1, aexpr(J_)), (-1, Xe(J_))), lin((1, bexpr(I_)), (-1, Xe(I_)))])
    else:
        K, L, M = roles['K'], roles['L'], roles['M']
        if MUT != 'noQb':
            fail_or([lin((1.5, bexpr(K)), (-1, Xe(K))), lin((1, aexpr(K)), (0.75, bexpr(K)), (-1, Xe(K)))])
        if MUT != 'noQa':
            fail_or([lin((1.5, aexpr(L)), (-1, Xe(L))), lin((1, bexpr(L)), (0.75, aexpr(L)), (-1, Xe(L)))])
        if MUT != 'noV':
            fail_or([lin((1, aexpr(M)), (1, bexpr(M)), (-1, Xe(M))), lin((1.25, aexpr(M)), (0.5, bexpr(M)), (-1, Xe(M)))])
    n = len(names)
    A = np.array([r[:n] for r in rows])
    lb = np.zeros(n); ub = np.full(n, np.inf)
    for i in range(q): ub[X[i]] = 2.0; ub[G[i]] = 1.0; ub[Hh[i]] = 1.0
    ub[gr] = 1.0; ub[hr] = 1.0
    lb[eps] = -1.0; ub[eps] = 1.0
    integ = np.zeros(n)
    for v in binaries + fb: integ[v] = 1; ub[v] = 1.0
    c = np.zeros(n); c[eps] = -1.0
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integ, bounds=Bounds(lb, ub),
               options={'mip_rel_gap': 0, 'time_limit': 300})
    if res.x is None:
        return None, res.status, None
    sol = {names[k]: res.x[k] for k in range(n)}
    return -res.fun, res.status, sol

best = -9; worst_pat = None
cnt = 0
for mode in ['adm', 'tmpl']:
    elems = ['I', 'J'] if mode == 'adm' else ['I', 'J', 'K', 'L', 'M']
    for pat in set_partitions(elems):
        val, st, sol = solve(pat, mode)
        cnt += 1
        tag = 'INFEASIBLE' if val is None else f'{val:.3e}'
        if val is not None and val > 1e-5:
            print('POSITIVE', mode, pat, tag, {k: round(v, 5) for k, v in sol.items() if not k.startswith(('z', 'w', 'f'))}, flush=True)
        if val is not None and val > best:
            best = val; worst_pat = (mode, pat)
print(f'THR={THR} MUT={MUT!r}: {cnt} MILPs, max margin eps* = {best:.3e} at {worst_pat}')
print('RESULT:', 'NO COUNTEREXAMPLE (eps*<=1e-5, HiGHS tolerance)' if best <= 1e-5 else 'COUNTEREXAMPLE FOUND IN RELAXATION')
