# Referee w9, claim templates#1 (Theorem 2UB).  INDEPENDENT exact end-to-end check.
#  * tau* computed by note Lemma 7.56 (blocker pairs, all subsets S, upper bounds h = x), NOT the attacker formula.
#  * for every heavy pair (I,J): canonical a,b; membership a in U(g), b in U(h) checked from the definition.
#  * bad tuple built EXPLICITLY: per part, rational masses on cells of a support (Fano line complements for
#    H/Q_b/Q_a, the ten-cell V support); row loads recomputed by brute force; capacity checked; the union of all
#    positive cells over all parts checked pairwise for covering [7] (Venn criterion) by brute force.
#  * non-heavy case: explicit a in U(g), a <= 4x/7, homogeneous Fano.
# usage: python3 w9_ref_templates_2ub.py e2e SEED NT      (random exact instances, several samplers)
from fractions import Fraction as F
import itertools, random, sys

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
FANO_CELLS = [frozenset(set(range(7)) - set(l)) for l in LINES]
# V support: rows b0=0,b1=1, w1..w4=2..5, z=6
W = [2,3,4,5]; Z = 6
V_CELLS = {'bb': frozenset({0,1})}
for k, S in enumerate(itertools.combinations(W + [Z], 4)): V_CELLS['q%d' % k] = frozenset(S)
V_CELLS['m0a'] = frozenset({0,4,5,Z}); V_CELLS['m0b'] = frozenset({0,2,3,Z})   # b0 <-> {w3w4|w1w2}
V_CELLS['m1a'] = frozenset({1,3,5,Z}); V_CELLS['m1b'] = frozenset({1,2,4,Z})   # b1 <-> {w2w4|w1w3}

def noncovering(cells):
    cells = list(set(cells))
    for c1 in cells:
        for c2 in cells:
            if len(c1 | c2) == 7: return False
    return True
assert noncovering(FANO_CELLS) and noncovering(V_CELLS.values())

def build(kind, s, t):
    """masses {cell: m} in one part; row r demand: s for a-rows, t for b-rows (kind-specific row roles)."""
    m = {}
    def add(c, v):
        if v > 0: m[c] = m.get(c, 0) + v
    if kind == 'H':      # all 7 rows type a, load s
        for c in FANO_CELLS: add(c, s / 4)
        roles = ['a'] * 7
    elif kind in ('Qb', 'Qa'):   # rows on line (0,1,2) get the 3-type, the others the 4-type
        three, four = (t, s) if kind == 'Qb' else (s, t)
        L0 = FANO_CELLS[0]  # complement of line (0,1,2) = {3,4,5,6}
        add(L0, max(F(0), four - F(3, 4) * three))
        for c in FANO_CELLS[1:]: add(c, three / 4)
        roles = (['b'] * 3 + ['a'] * 4) if kind == 'Qb' else (['a'] * 3 + ['b'] * 4)
    elif kind == 'V':
        # (1,0): 1/4 on 4-subsets of W+z; (0,1): 1 on bb; (2,1): 1 on W, 1/2 on four mixed cells
        if t <= s / 2: lam, mu, nu = t, s - 2 * t, F(0)
        else: lam, mu, nu = s / 2, F(0), t - s / 2
        for k in range(5): add(V_CELLS['q%d' % k], mu / 4)
        add(V_CELLS['bb'], nu)
        add(frozenset(W), lam)
        for key in ('m0a', 'm0b', 'm1a', 'm1b'): add(V_CELLS[key], lam / 2)
        roles = ['b', 'b'] + ['a'] * 5
    return m, roles

def check_tuple(kind, x, a, b):
    """True iff the explicit construction of `kind` realises rows (types a,b) within capacities x."""
    allcells = []
    for i in range(len(x)):
        m, roles = build(kind, a[i], b[i])
        if sum(m.values()) > x[i]: return False
        for r in range(7):
            load = sum(v for c, v in m.items() if r in c)
            need = a[i] if roles[r] == 'a' else b[i]
            assert load >= need, (kind, i, r, load, need)   # construction always meets loads
        allcells += list(m)
    assert noncovering(allcells)
    return True

def tau_756(x, comps):
    """note Lemma 7.56 with upper bounds h = x; comps = list of lower-bound vectors."""
    p = len(x); N = sum(x)
    def blockers(l):
        B = [(frozenset([i]), x[i] - l[i]) for i in range(p) if l[i] > 0]
        for r in range(1, p + 1):
            for S in itertools.combinations(range(p), r):
                bb = 1 - sum(x[i] for i in range(p) if i not in S)
                if bb > 0: B.append((frozenset(S), sum(x[i] for i in S) - bb))
        return B
    B1, B2 = blockers(comps[0]), blockers(comps[1])
    best = None
    for S, al in B1:
        for T, be in B2:
            q = max(al, be, al + be - sum(x[i] for i in S & T))
            best = q if best is None or q < best else best
    return best

def in_upbox(a, g, x):
    return sum(a) == 1 and all(g[i] <= a[i] <= x[i] for i in range(len(x)))

def analyse(x, g, h):
    """returns list of (I,J,winner) or ('H',..); raises on any failure."""
    p = len(x); out = []
    for gen, nm in ((g, 'g'), (h, 'h')):
        if all(7 * gen[i] <= 4 * x[i] for i in range(p)):
            # explicit a in U(gen) with a <= 4x/7: greedy fill
            a = list(gen); rest = 1 - sum(gen)
            for i in range(p):
                add = min(rest, F(4, 7) * x[i] - a[i]); a[i] += add; rest -= add
            assert rest == 0 and in_upbox(a, gen, x)
            assert check_tuple('H', x, a, a)
            out.append(('H', nm)); return out
    Is = [i for i in range(p) if 7 * g[i] > 4 * x[i]]; Js = [j for j in range(p) if 7 * h[j] > 4 * x[j]]
    for I in Is:
        for J in Js:
            if I == J: raise AssertionError(('I==J', x, g, h))
            a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
            if not (in_upbox(a, g, x) and in_upbox(b, h, x)): raise AssertionError(('admissible', x, g, h, I, J))
            win = None
            for kind in ('Qb', 'Qa', 'V'):
                if check_tuple(kind, x, a, b): win = kind; break
            if win is None: raise AssertionError(('NO TEMPLATE', x, g, h, I, J, a, b))
            out.append((I, J, win))
    return out

def rq(rng, lo, hi, d):
    return lo + (hi - lo) * F(rng.randint(0, d), d)

def sample(rng, mode):
    p = rng.choice([2, 3, 4, 5, 6]); d = rng.choice([6, 7, 12, 28, 60, 84])
    if mode == 0:   # generic
        x = [rq(rng, F(1, 10), F(5, 2), d) for _ in range(p)]
        gs = []
        for _ in range(2):
            g = [rq(rng, 0, min(x[i], 1), d) if rng.random() < 0.5 else F(0) for i in range(p)]
            gs.append(g)
    elif mode == 1:  # several heavy coordinates, near-threshold capacities
        x = [rq(rng, F(1, 4), F(7, 4), d) for _ in range(p)]
        gs = []
        for _ in range(2):
            g = [F(0)] * p
            for i in rng.sample(range(p), rng.randint(1, min(3, p))):
                g[i] = rq(rng, F(4, 7) * x[i], min(x[i], 1), d)
            gs.append(g)
    else:            # sum-one-ish generators (TT limit) and point-like pieces
        x = [rq(rng, F(1, 5), F(2), d) for _ in range(p)]
        gs = []
        for _ in range(2):
            g = [F(0)] * p; rest = F(1)
            for i in rng.sample(range(p), p):
                v = min(rest, x[i], rq(rng, 0, 1, d)); g[i] = v; rest -= v
            if rng.random() < 0.5:
                i = rng.randrange(p); g[i] = g[i] * rq(rng, 0, 1, 4)
            gs.append(g)
    return x, gs[0], gs[1]

if __name__ == '__main__':
    seed = int(sys.argv[2]); NT = int(sys.argv[3])
    rng = random.Random(seed)
    stats = {}; n = 0; tries = 0; eq = 0
    while n < NT:
        tries += 1
        mode = tries % 3
        x, g, h = sample(rng, mode)
        if sum(g) > 1 or sum(h) > 1: continue
        hv = lambda gen: any(7 * gen[i] > 4 * x[i] for i in range(len(x)))
        if not (hv(g) and hv(h)) and rng.random() < 0.97: continue
        t = tau_756(x, [g, h])
        if t < F(3, 4): continue
        n += 1
        if t == F(3, 4): eq += 1
        for r in analyse(x, g, h):
            k = r[0] if r[0] == 'H' else (r[2], len(x))
            stats[k] = stats.get(k, 0) + 1
    print('seed', seed, 'tries', tries, 'instances', n, 'tau*=3/4 exactly', eq)
    print(sorted(stats.items(), key=str))
    print('ALL CHECKS PASSED')
