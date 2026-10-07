# Referee w9 (BREAK-IT lens), claim templates#2 = Theorem H2. Library, exact rationals throughout.
#  * tau*(C) for a finite (hence closed) type set: branch-and-bound over cutoff vectors (a cut at value v in part i
#    kills every type with a_i >= v and costs x_i - v; an uncut part costs 0).  Independent of the attacker's
#    itertools enumeration and of the other referee's kill-map recursion.  Cross-checked against a brute
#    enumeration in selftest().
#  * EXPLICIT Venn-level realisation of H / Q_b / Q_a / V: per part a dict cell -> mass is built from the
#    constructive decompositions, and we check (i) no two cells (same cell twice included) cover all 7 rows,
#    (ii) every row's load >= its required coordinate, (iii) total mass <= x_i.  No closed-form feasibility
#    function is trusted.
import itertools, random
from fractions import Fraction as F

# ---------------- tau* ----------------
def tau_star(x, T):
    p = len(x); N = sum(x)
    best = [N - 1]   # residual of total mass < 1 contains no type (it is also dominated by a cutoff residual)
    idx = list(range(len(T)))
    def rec(i, alive, cost):
        if cost >= best[0]: return
        if not alive:
            best[0] = cost; return
        if i == p: return
        if i == p - 1:
            v = min(T[k][i] for k in alive)
            if v > 0:                                   # a cut 'just below v' needs v > 0 (residual mass >= 0)
                c = cost + x[i] - v
                if c < best[0]: best[0] = c
            return
        rec(i + 1, alive, cost)                        # no cut in part i
        for v in sorted(set(T[k][i] for k in alive)):
            if v <= 0: continue
            rest = [k for k in alive if T[k][i] < v]
            rec(i + 1, rest, cost + x[i] - v)
    rec(0, idx, F(0))
    return best[0]

def tau_brute(x, T):
    p = len(x); best = sum(x) - 1
    cand = [[None] + sorted(set(t[i] for t in T if t[i] > 0)) for i in range(p)]
    for c in itertools.product(*cand):
        if all(any(c[i] is not None and t[i] >= c[i] for i in range(p)) for t in T):
            best = min(best, sum(x[i] - c[i] for i in range(p) if c[i] is not None))
    return best

# ---------------- supports / explicit realisations ----------------
LINES = [frozenset(l) for l in [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]]
ALL7 = frozenset(range(7))
def fano_cell(l): return ALL7 - l

def add(d, cell, m):
    if m > 0: d[cell] = d.get(cell, F(0)) + m

def real_H(s):                       # 7 rows of one type, load s
    d = {}
    for l in LINES: add(d, fano_cell(l), s / 4)
    return d
QB_L = LINES[0]                      # b-rows = points 0,1,2 ; a-rows = 3,4,5,6
def real_Qb(s, t):                   # s = a-load (4 rows off L), t = b-load (3 rows on L)
    d = {}
    add(d, fano_cell(QB_L), max(F(0), s - 3 * t / 4))
    for l in LINES:
        if l != QB_L: add(d, fano_cell(l), t / 4)
    return d
QB_ROWS = {'a': [3, 4, 5, 6], 'b': [0, 1, 2]}
# V: rows b0=0,b1=1, w1..w4 = 2..5, z = 6
V_ROWS = {'a': [2, 3, 4, 5, 6], 'b': [0, 1]}
b0, b1, w1, w2, w3, w4, z = range(7)
V10 = [frozenset([b0, b1])] + [frozenset(c) for c in itertools.combinations([w1, w2, w3, w4, z], 4)] + \
      [frozenset([b0, w3, w4, z]), frozenset([b0, w1, w2, z]), frozenset([b1, w2, w4, z]), frozenset([b1, w1, w3, z])]
def real_V(s, t):                    # s = a-load (5 rows), t = b-load (2 rows)
    d = {}
    def p10(m):
        for c in itertools.combinations([w1, w2, w3, w4, z], 4): add(d, frozenset(c), m / 4)
    def p01(m): add(d, frozenset([b0, b1]), m)
    def p21(m):
        add(d, frozenset([w1, w2, w3, w4]), m)       # subset of the 4-subset cell, allowed (downset)
        for c in V10[6:]: add(d, c, m / 2)
    if 2 * t <= s: p21(t); p10(s - 2 * t)
    else: p21(s / 2); p01(t - s / 2)
    return d

def check_part(d, loads, cap):
    """d: cell->mass, loads: row->required. returns slack (cap - mass) or raises on structural failure."""
    cells = list(d)
    for c1 in cells:
        for c2 in cells:
            assert (c1 | c2) != ALL7, ('covering pair', c1, c2)
    for r, need in loads.items():
        got = sum(m for c, m in d.items() if r in c)
        assert got >= need, ('row underloaded', r, got, need)
    return cap - sum(d.values())

def template_slack(name, a, b, x):
    """Exact explicit realisation of template name with type a (and b) in every part; returns min slack over parts
    (>= 0 iff realised).  Q_a = Q_b with a,b exchanged."""
    sl = None
    for i in range(len(x)):
        if name == 'H':
            d = real_H(a[i]); loads = {r: a[i] for r in range(7)}
        elif name == 'Qb':
            d = real_Qb(a[i], b[i]); loads = {r: a[i] for r in QB_ROWS['a']}; loads.update({r: b[i] for r in QB_ROWS['b']})
        elif name == 'Qa':
            d = real_Qb(b[i], a[i]); loads = {r: b[i] for r in QB_ROWS['a']}; loads.update({r: a[i] for r in QB_ROWS['b']})
        elif name == 'V':
            d = real_V(a[i], b[i]); loads = {r: a[i] for r in V_ROWS['a']}; loads.update({r: b[i] for r in V_ROWS['b']})
        s = check_part(d, loads, x[i])
        sl = s if sl is None else min(sl, s)
    return sl

def heavy(t, x, i): return 7 * t[i] > 4 * x[i]

# ---------------- the recipe of Theorem H2 ----------------
class Fail(Exception): pass

def recipe(x, T, rng=None, strict_S=False):
    """Apply the H2 recipe to finite C=T (parts 0,1 heavy, 2.. light), with RANDOM tie-breaking if rng given.
    Returns (template, slack, info).  Raises Fail with a message if any claimed intermediate fact is violated."""
    p = len(x)
    pick = (lambda L: rng.choice(L)) if rng else (lambda L: L[0])
    ts = tau_star(x, T)
    if ts < F(3, 4): return None
    for t in T:
        for l in range(2, p):
            if heavy(t, x, l): raise Fail('hypothesis violated (heavy light coordinate)')
    light = [t for t in T if not any(heavy(t, x, i) for i in range(p))]
    if light:
        t0 = pick(light); return ('H', template_slack('H', t0, None, x), None)
    C1 = [t for t in T if heavy(t, x, 0)]; C2 = [t for t in T if heavy(t, x, 1)]
    if not C1 or not C2: raise Fail('C_i empty with tau*>=3/4')
    if any(heavy(t, x, 0) and heavy(t, x, 1) for t in T): raise Fail('double heavy type')
    th1 = min(t[0] for t in C1); th2 = min(t[1] for t in C2)
    a0 = pick([t for t in C1 if t[0] == th1]); b0 = pick([t for t in C2 if t[1] == th2])
    d1, d2 = x[0] - th1, x[1] - th2
    if not (d1 + d2 >= F(3, 4)): raise Fail('(1)')
    if not (th1 + th2 > 1): raise Fail('F1')
    if 3 * th2 <= 2 * x[1]:
        return ('Qb', template_slack('Qb', a0, b0, x), None)
    if 3 * th1 <= 2 * x[0]:
        return ('Qa', template_slack('Qa', a0, b0, x), None)
    if not (th1 + th2 > F(3, 2) and th1 > F(1, 2) and th2 > F(1, 2) and d1 > F(3, 4) - th2 / 2): raise Fail('case C facts')
    Lam = sum(a0[l] for l in range(2, p))
    if strict_S: S = [b for b in C2 if all(b[l] + a0[l] < x[l] for l in range(2, p))]
    else: S = [b for b in C2 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
    if not S: raise Fail('S empty')
    rho = max(x[1] - b[1] for b in S)
    bs = pick([b for b in S if x[1] - b[1] == rho])
    if not (rho >= F(3, 4) - d1 - Lam): raise Fail('(2)')
    return ('V', template_slack('V', a0, bs, x), (a0, bs, b0))

def selftest(seed=0, n=300):
    rng = random.Random(seed)
    for _ in range(n):
        p = rng.randint(2, 4); D = rng.choice([6, 10, 12])
        x = [F(rng.randint(D // 3, 2 * D), D) for _ in range(p)]
        T = []
        for _ in range(rng.randint(1, 6)):
            w = [rng.randint(0, 5) for _ in range(p)]
            if sum(w) == 0: continue
            t = [F(v, sum(w)) for v in w]
            if all(t[i] <= x[i] for i in range(p)): T.append(t)
        if not T: continue
        assert tau_star(x, T) == tau_brute(x, T), (x, T)
    # support sanity: realisations reproduce the claimed closed forms exactly
    for s in [F(k, 7) for k in range(8)]:
        for t in [F(k, 5) for k in range(6)]:
            assert sum(real_Qb(s, t).values()) == max(3 * t / 2, s + 3 * t / 4)
            assert sum(real_V(s, t).values()) == max(s + t, 5 * s / 4 + t / 2)
            assert sum(real_H(s).values()) == 7 * s / 4
            template_slack('Qb', [s], [t], [F(10)]); template_slack('V', [s], [t], [F(10)]); template_slack('H', [s], None, [F(10)])
    print('selftest OK')

if __name__ == '__main__':
    selftest()
