# [templates#1] BREAK-IT referee (w9): EXACT certificate for the role-reduced relaxation of Theorem 2UB.
# Same reduction as w9_ref_templates1brk_milp.py (valid for ANY number of parts p):
#   role parts I,J (heavy pair), K (Q_b fails), L (Q_a fails), M (V(a,b) fails), identified by a set partition;
#   all other parts lumped into g_rest,h_rest >= 0; hypotheses (K1'),(K2') kept among role parts only; x_i <= 2 WLOG.
#   Separate systems for "canonical a or b inadmissible" (roles I,J only).
# Every disjunction is enumerated explicitly (leaf = identification pattern x positivity pattern of g,h on role
# parts x choice of the attained branch of (K1') x failing facet of Q_b, Q_a, V).  For each leaf the linear system
#       A v >= b  (non-strict),   C v > d  (strict)
# is shown infeasible by an EXACT Motzkin certificate (y,z >= 0, A^T y + C^T z = 0, b.y + d.z >= 0, and
# (z != 0 or b.y + d.z > 0)), found by HiGHS and then re-derived/verified in exact rational arithmetic.
# Positivity branch "g_i > 0" is relaxed to g_i >= 0 (only adds constraints -> still a relaxation).
import sys, itertools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

THR = F(sys.argv[1]) if len(sys.argv) > 1 else F(3, 4)
MUT = sys.argv[2] if len(sys.argv) > 2 else ''

def set_partitions(elems):
    if not elems:
        yield []; return
    first, rest = elems[0], elems[1:]
    for part in set_partitions(rest):
        for k in range(len(part)):
            yield part[:k] + [[first] + part[k]] + part[k + 1:]
        yield [[first]] + part

def nullspace_exact(M):
    # M: list of rows (Fractions), returns basis of {v : M v = 0}
    M = [list(r) for r in M]; nr = len(M); nc = len(M[0]) if M else 0
    piv = []; r = 0
    for c in range(nc):
        pr = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(nr):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == nr: break
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * nc; v[fc] = F(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis

def verify(rows, y):
    # rows: list of (coefvec(list F), rhs F, strict bool); y: multipliers (F) >= 0
    n = len(rows[0][0])
    if any(v < 0 for v in y): return False
    comb = [sum(y[k] * rows[k][0][j] for k in range(len(rows))) for j in range(n)]
    if any(c != 0 for c in comb): return False
    val = sum(y[k] * rows[k][1] for k in range(len(rows)))
    zs = any(y[k] > 0 and rows[k][2] for k in range(len(rows)))
    return val > 0 or (val == 0 and zs)

def certify(rows):
    m = len(rows); n = len(rows[0][0])
    A = np.array([[float(c) for c in r[0]] for r in rows])     # A^T y = 0
    bvec = np.array([float(r[1]) for r in rows]); strict = np.array([1.0 if r[2] else 0.0 for r in rows])
    # max strict.y + b.y  s.t. A^T y = 0, b.y >= 0, sum y <= 1, y >= 0
    res = linprog(-(strict + bvec), A_ub=np.vstack([-bvec, np.ones(m)]), b_ub=[0, 1], A_eq=A.T, b_eq=np.zeros(n),
                  bounds=[(0, None)] * m, method='highs')
    if res.status != 0 or -res.fun < 1e-9:
        return None, 'lp'
    yf = res.x
    # try rationalisation
    y = [F(v).limit_denominator(10 ** 6) if v > 1e-10 else F(0) for v in yf]
    if verify(rows, y): return y, 'round'
    # exact re-solve on the support
    S = [k for k in range(m) if yf[k] > 1e-10]
    M = [[rows[k][0][j] for k in S] for j in range(n)]
    B = nullspace_exact(M)
    if len(B) == 1:
        v = B[0]; k0 = max(range(len(S)), key=lambda t: yf[S[t]])
        if v[k0] < 0: v = [-a for a in v]
        y = [F(0)] * m
        for t, k in enumerate(S): y[k] = v[t]
        if verify(rows, y): return y, 'null'
    # fallback: try each nullspace vector combination via least-squares projection of yf onto span(B)
    if B:
        Bm = np.array([[float(a) for a in b] for b in B]).T
        coef, *_ = np.linalg.lstsq(Bm, yf[S], rcond=None)
        cf = [F(c).limit_denominator(10 ** 6) for c in coef]
        v = [sum(cf[t] * B[t][r] for t in range(len(B))) for r in range(len(S))]
        y = [F(0)] * m
        for t, k in enumerate(S): y[k] = v[t]
        if verify(rows, y): return y, 'proj'
    return None, 'exactfail'

def leaves(pattern, mode):
    roles = {}
    for bi, blk in enumerate(pattern):
        for r in blk: roles[r] = bi
    q = len(pattern); I, J = roles['I'], roles['J']
    n = 3 * q + 2
    X = list(range(q)); G = list(range(q, 2 * q)); H = list(range(2 * q, 3 * q)); GR, HR = 3 * q, 3 * q + 1
    def vec(d):
        v = [F(0)] * n
        for k, c in d.items(): v[k] += F(c)
        return v
    def aexpr(i):   # returns (dict, const)
        d = {G[i]: 1}; c = F(0)
        fillpart = I if MUT == 'fillown' else J
        if i == fillpart:
            c += 1
            for j in range(q): d[G[j]] = d.get(G[j], 0) - 1
            d[GR] = d.get(GR, 0) - 1
        return d, c
    def bexpr(i):
        d = {H[i]: 1}; c = F(0)
        fillpart = J if MUT == 'fillown' else I
        if i == fillpart:
            c += 1
            for j in range(q): d[H[j]] = d.get(H[j], 0) - 1
            d[HR] = d.get(HR, 0) - 1
        return d, c
    def comb(*terms):
        d = {}; c = F(0)
        for k, (e, cc) in terms:
            k = F(k)
            for v, cf in e.items(): d[v] = d.get(v, 0) + k * cf
            c += k * cc
        return d, c
    xe = lambda i: ({X[i]: 1}, F(0))
    base = []
    def ge(expr, rhs, strict=False):    # expr >= rhs
        d, c = expr
        base.append((vec(d), F(rhs) - c, strict))
    for i in range(q):
        ge(({X[i]: -1}, F(0)), -2)                        # x_i <= 2
        ge(({G[i]: 1}, F(0)), 0); ge(({H[i]: 1}, F(0)), 0)
        ge(({X[i]: 1, G[i]: -1}, F(0)), 0); ge(({X[i]: 1, H[i]: -1}, F(0)), 0)
    ge(({GR: 1}, F(0)), 0); ge(({HR: 1}, F(0)), 0)
    gsum = {G[i]: -1 for i in range(q)}; gsum[GR] = -1; ge((gsum, F(0)), -1)
    hsum = {H[i]: -1 for i in range(q)}; hsum[HR] = -1; ge((hsum, F(0)), -1)
    ge(({G[I]: 1, X[I]: F(-4, 7)}, F(0)), 0, True)      # heavy
    ge(({H[J]: 1, X[J]: F(-4, 7)}, F(0)), 0, True)
    if mode == 'adm':
        fails = [[comb((1, xe(J)), (-1, aexpr(J))), comb((1, xe(I)), (-1, bexpr(I)))]]  # x - value < 0
    else:
        K, L, M = roles['K'], roles['L'], roles['M']
        fails = []
        if MUT != 'noQb':
            fails.append([comb((1, xe(K)), (F(-3, 2), bexpr(K))), comb((1, xe(K)), (-1, aexpr(K)), (F(-3, 4), bexpr(K)))])
        if MUT != 'noQa':
            fails.append([comb((1, xe(L)), (F(-3, 2), aexpr(L))), comb((1, xe(L)), (-1, bexpr(L)), (F(-3, 4), aexpr(L)))])
        if MUT != 'noV':
            fails.append([comb((1, xe(M)), (-1, aexpr(M)), (-1, bexpr(M))), comb((1, xe(M)), (F(-5, 4), aexpr(M)), (F(-1, 2), bexpr(M)))])
    forced_g = {I}; forced_h = {J}
    for zg in itertools.product([0, 1], repeat=q):
        if any(zg[i] == 0 for i in forced_g): continue
        for zh in itertools.product([0, 1], repeat=q):
            if any(zh[i] == 0 for i in forced_h): continue
            rows0 = list(base)
            for i in range(q):
                if zg[i] == 0: rows0.append((vec({G[i]: -1}), F(0), False))
                if zh[i] == 0: rows0.append((vec({H[i]: -1}), F(0), False))
            for i in range(q):
                for j in range(q):
                    if i != j and zg[i] and zh[j]:
                        rows0.append((vec({X[i]: 1, G[i]: -1, X[j]: 1, H[j]: -1}), THR, False))
            both = [i for i in range(q) if zg[i] and zh[i]]
            for wch in itertools.product([0, 1], repeat=len(both)):
                rows1 = list(rows0)
                for i, w in zip(both, wch):
                    rows1.append((vec({X[i]: 1, (G if w == 0 else H)[i]: -1}), THR, False))
                for fch in itertools.product(*[range(len(f)) for f in fails]):
                    rows2 = list(rows1)
                    for f, k in zip(fails, fch):
                        d, c = f[k]            # x - value + ... < 0  <=>  -(d.v + c) > 0
                        rows2.append((vec({v: -cf for v, cf in d.items()}), c, True))
                    yield (tuple(zg), tuple(zh), wch, fch), rows2

total = 0; how = {}; bad = []
for mode in ['adm', 'tmpl']:
    elems = ['I', 'J'] if mode == 'adm' else ['I', 'J', 'K', 'L', 'M']
    for pat in set_partitions(elems):
        for key, rows in leaves(pat, mode):
            total += 1
            y, h = certify(rows)
            how[h] = how.get(h, 0) + 1
            if y is None:
                bad.append((mode, pat, key, h))
                if len(bad) <= 10: print('NO CERTIFICATE', mode, pat, key, h, flush=True)
print(f'THR={THR} MUT={MUT!r}: {total} leaf systems; certificate route counts {how}; uncertified {len(bad)}')
print('RESULT:', 'EXACT CERTIFICATE: role-reduced relaxation infeasible -> 2UB holds for all p' if not bad else 'NOT CERTIFIED')
