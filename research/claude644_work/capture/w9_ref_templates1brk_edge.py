# [templates#1] BREAK-IT referee (w9): EXACT edge-case end-to-end test of Theorem 2UB.
# Independent code: tau* by brute force over cut patterns (u_i = c^- for c in {x_i, g_i, h_i}, plus the sum<1
# blocker N-1), pushed DOWN onto tau*=3/4 exactly; canonical pair for EVERY heavy pair (I,J); a bad seven-tuple
# realised with EXPLICIT exact cell masses (Fano line-complement support for H/Q_b/Q_a, ten-cell support for V),
# brute-force row loads, capacity, and pairwise non-covering of the support.
# Generators focus on edge cases: g_I = 1, |g| = 1, g_i = x_i (generator at capacity), coordinates exactly at
# 4x_i/7 (non-heavy boundary), several heavy parts per generator, many small tail coordinates, p up to 9,
# the narrow K != J window (g_I > 9/10), and nested/overlapping generators (g <= h).
import random, itertools, sys
from fractions import Fraction as F
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NT = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
rng = random.Random(seed)
Q34 = F(3, 4)

def tau_star(x, g, h):
    p = len(x); best = sum(x) - 1
    cand = [sorted({x[i], g[i], h[i]} - {F(0)}) for i in range(p)]
    # u_i = c^- blocks a type iff a_i >= c; uncut part: c = +inf
    for pat in itertools.product(*[[None] + c for c in cand]):
        cost = sum(x[i] - c for i, c in enumerate(pat) if c is not None)
        if cost >= best: continue
        def blocked(gen):
            # every type a in U(gen) (gen <= a <= x, sum 1) has a_i >= c_i for some cut i, or no type fits
            # a type fits under u iff gen_i < c_i for all cut i and sum_i min(x_i, c_i^-) >= 1 (c^- -> sup)
            if any(c is not None and gen[i] >= c for i, c in enumerate(pat)): return True
            cap = sum((x[i] if c is None else c) for i, c in enumerate(pat))
            ncut = sum(c is not None for c in pat)
            return cap < 1 or (cap == 1 and ncut > 0)
        if blocked(g) and blocked(h): best = cost
    return best

# ---------- explicit supports ----------
LINES = [frozenset(s) for s in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
FANO_CELLS = [frozenset(range(7)) - l for l in LINES]
assert all(len(c1 | c2) < 7 for c1 in FANO_CELLS for c2 in FANO_CELLS)
# V support on rows 0..6: b0=0,b1=1,w1..w4=2..5,z=6
b0, b1, w1, w2, w3, w4, z = range(7)
A5 = [w1, w2, w3, w4, z]
V_CELLS = [frozenset({b0, b1})] + [frozenset(A5) - {r} for r in A5] + \
          [frozenset({b0, w3, w4, z}), frozenset({b0, w1, w2, z}), frozenset({b1, w2, w4, z}), frozenset({b1, w1, w3, z})]
assert all(len(c1 | c2) < 7 for c1 in V_CELLS for c2 in V_CELLS)

def fano_masses(rowload):
    # rowload: dict row(point)->load; find masses on line complements by the explicit formulas below
    raise NotImplementedError

def realise(kind, s, t):
    """return (cells, masses, rows_a, rows_b) realising loads >= s on a-rows, >= t on b-rows in one part"""
    if kind == 'Ha':
        return FANO_CELLS, [s / 4] * 7, list(range(7)), []
    if kind == 'Hb':
        return FANO_CELLS, [t / 4] * 7, [], list(range(7))
    if kind in ('Qb', 'Qa'):
        L = LINES[0]
        brows = sorted(L); arows = sorted(set(range(7)) - L)
        ss, tt = (s, t) if kind == 'Qb' else (t, s)     # ss: load of the 4 off-L rows, tt: of the 3 L rows
        u = max(F(0), ss - 3 * tt / 4); v = tt / 4
        masses = [u if l == L else v for l in LINES]
        if kind == 'Qb': return FANO_CELLS, masses, arows, brows
        return FANO_CELLS, masses, brows, arows
    if kind == 'V':
        m = [F(0)] * 10
        def addcomb(lam, which):
            if which == '10':
                for k in range(1, 6): m[k] += lam / 4
            elif which == '01':
                m[0] += lam
            else:  # (2,1): 1 on W={w1..w4} (= cell A5 minus z, index of z is 5 -> k=5), 1/2 on mixed cells
                m[1 + A5.index(z)] += lam
                for k in range(6, 10): m[k] += lam / 2
        if t <= s / 2:
            addcomb(t, '21'); addcomb(s - 2 * t, '10')
        else:
            addcomb(s / 2, '21'); addcomb(t - s / 2, '01')
        return V_CELLS, m, A5, [b0, b1]
    raise ValueError

def check_tuple(kind, a, b, x):
    for i in range(len(x)):
        cells, masses, ra, rb = realise(kind, a[i], b[i])
        assert all(mm >= 0 for mm in masses)
        if sum(masses) > x[i]: return False
        load = [sum(mm for c, mm in zip(cells, masses) if r in c) for r in range(7)]
        if any(load[r] < a[i] for r in ra) or any(load[r] < b[i] for r in rb):
            raise AssertionError('realisation bug')
    return True

def formula(kind, s, t):
    return {'Ha': 7 * s / 4, 'Hb': 7 * t / 4, 'Qb': max(3 * t / 2, s + 3 * t / 4),
            'Qa': max(3 * s / 2, t + 3 * s / 4), 'V': max(s + t, 5 * s / 4 + t / 2)}[kind]

def rnd(lo, hi, d):
    return lo + (hi - lo) * F(rng.randint(0, d), d)

def gen_instance():
    p = rng.choice([2, 3, 3, 4, 4, 5, 6, 7, 9]); d = rng.choice([6, 7, 12, 14, 28, 60])
    x = [rnd(F(1, 7), F(7, 4), d) for _ in range(p)]
    mode = rng.choice(['gI1', 'sum1', 'cap', 'bnd', 'multi', 'tail', 'window', 'nested', 'plain'])
    gens = []
    for side in range(2):
        g = [F(0)] * p
        H = rng.randrange(p)
        if mode == 'gI1' and side == 0:
            x[H] = max(x[H], F(1)) if rng.random() < .5 else rnd(F(1), F(7, 4), d); g[H] = F(1)
        elif mode == 'window' and side == 0:
            g[H] = rnd(F(9, 10), F(1), d); x[H] = max(x[H], g[H]); x[H] = min(x[H], 7 * g[H] / 4 - F(1, 1000))
            x[H] = max(x[H], g[H])
        else:
            g[H] = rnd(4 * x[H] / 7, min(F(1), x[H]), d)
        for i in range(p):
            if i == H: continue
            r = rng.random()
            if mode == 'cap' and r < .3: g[i] = min(x[i], F(1, 3))
            elif mode == 'bnd' and r < .5: g[i] = 4 * x[i] / 7
            elif mode == 'multi' and r < .4: g[i] = rnd(4 * x[i] / 7, x[i], d)
            elif mode == 'tail' and r < .8: g[i] = rnd(F(0), x[i] / 10, d)
            elif r < .5: g[i] = rnd(F(0), x[i] * rng.choice([F(1, 5), F(1, 2), F(1)]), d)
        if sum(g) > 1:
            # rescale non-heavy coordinates
            rest = sum(g) - g[H]
            if g[H] > 1: return None
            if rest > 0:
                f = (1 - g[H]) / rest * rng.choice([F(1), F(9, 10), F(1, 2)])
                g = [gi if i == H else gi * f for i, gi in enumerate(g)]
        if mode == 'sum1' and rng.random() < .7:
            others = [i for i in range(p) if i != H]
            if others:
                k = rng.choice(others); g[k] += 1 - sum(g)
                if g[k] > x[k]: return None
        gens.append(g)
    g, h = gens
    if mode == 'nested':
        h = [max(gi, hi) for gi, hi in zip(g, h)]
        if sum(h) > 1: return None
    if any(gi > xi for gi, xi in zip(g, x)) or any(hi > xi for hi, xi in zip(h, x)): return None
    if sum(g) > 1 or sum(h) > 1: return None
    return x, g, h, mode

stats = {}
n = tries = 0; eq = 0; pairs = 0
while n < NT:
    tries += 1
    inst = gen_instance()
    if inst is None: continue
    x, g, h, mode = inst
    t = tau_star(x, g, h)
    if t < Q34: continue
    # push down onto tau* = 3/4
    for _ in range(3 * len(x)):
        if t == Q34: break
        i = rng.randrange(len(x)); dlt = t - Q34
        lowest = max(g[i], h[i])
        nx = max(lowest, x[i] - dlt)
        if nx == x[i]: continue
        x2 = list(x); x2[i] = nx
        t2 = tau_star(x2, g, h)
        if t2 >= Q34: x, t = x2, t2
    n += 1; eq += (t == Q34)
    stats[mode] = stats.get(mode, 0) + 1
    p = len(x)
    Hg = all(7 * g[i] <= 4 * x[i] for i in range(p)); Hh = all(7 * h[i] <= 4 * x[i] for i in range(p))
    if Hg or Hh:
        # H: build a in U(g) with a <= 4x/7 greedily
        gen = g if Hg else h
        a = list(gen); room = 1 - sum(a)
        for i in range(p):
            add = min(room, 4 * x[i] / 7 - a[i]); a[i] += add; room -= add
        assert room == 0, 'H: cannot complete'
        assert check_tuple('Ha', a, a, x); stats['H'] = stats.get('H', 0) + 1
        continue
    Is = [i for i in range(p) if 7 * g[i] > 4 * x[i]]; Js = [i for i in range(p) if 7 * h[i] > 4 * x[i]]
    for I in Is:
        for J in Js:
            pairs += 1
            assert I != J, ('I==J', x, g, h)
            a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
            assert sum(a) == 1 and sum(b) == 1
            assert all(g[i] <= a[i] <= x[i] for i in range(p)), ('a inadmissible', x, g, h, I, J)
            assert all(h[i] <= b[i] <= x[i] for i in range(p)), ('b inadmissible', x, g, h, I, J)
            ok = None
            for kind in ['Qb', 'Qa', 'V']:
                f_ok = all(formula(kind, a[i], b[i]) <= x[i] for i in range(p))
                e_ok = check_tuple(kind, a, b, x)
                assert f_ok == e_ok, ('formula/realisation mismatch', kind)
                if e_ok: ok = kind; break
            assert ok is not None, ('COUNTEREXAMPLE', x, g, h, I, J)
            key = ok + ('_KneJ' if ok == 'V' and any(2 * x[k] < 3 * b[k] for k in range(p) if k != J) else '')
            stats[key] = stats.get(key, 0) + 1
print(f'seed {seed}: {n} instances with tau*>=3/4 ({eq} with tau*=3/4 exactly), {pairs} heavy pairs, tries {tries}')
print('stats', dict(sorted(stats.items())))
print('ALL CHECKS PASSED')
