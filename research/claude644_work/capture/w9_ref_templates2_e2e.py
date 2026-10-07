# Referee w9, claim templates#2 (Theorem H2): INDEPENDENT exact end-to-end test.
# Differences from the attacker's tmpl/verify_h2.py:
#  * tau* computed by KILL-MAP enumeration (every type assigned a blocking coordinate with positive mass;
#    residual u_i = min assigned coordinate (sup, "just below"), unused coordinates full) -- not by cutoffs;
#  * template feasibility checked with min-mass functions derived from the supports' dual vertices
#    (w9_ref_templates2_supports.py), not with the closed formulas;
#  * generator also produces types heavy at BOTH heavy parts, boundary coordinates exactly 4x/7, types
#    heavy nowhere, arbitrary numbers of light parts (0..3), and an adversarial climb that minimises the
#    chosen template's slack subject to tau* >= 3/4.
#  * the survivor set S uses the claim's closed definition (b_l + a0_l <= x_l) AND the proof's strict one;
#    both maximisers are tested.
import sys, random, itertools
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
FOCUS = len(sys.argv) > 4 and sys.argv[4] == 'V'
import w9_ref_templates2_supports as SUP   # runs the support checks on import (asserts)

LIN = {}
LIN['Qb'] = set((sum(w[j] for j in [3, 4, 5, 6]), sum(w[j] for j in [0, 1, 2])) for w in SUP.fv)
LIN['H'] = set((sum(w), F(0)) for w in SUP.fv)
LIN['V'] = set((sum(w[j] for j in [2, 3, 4, 5, 6]), sum(w[j] for j in [0, 1])) for w in SUP.vv)
def M(name, s, t): return max(A * s + B * t for A, B in LIN[name])

def feas(name, a, b, x):  # rows of class a get a_i, class b get b_i; returns min slack over parts
    if name == 'Qa': name, a, b = 'Qb', b, a
    return min(x[i] - M(name, a[i], b[i]) for i in range(len(x)))

def tau_star(x, T):
    p = len(x); best = [None]
    N = sum(x)
    def rec(k, u):
        if k == len(T):
            c = N - sum(u)
            if best[0] is None or c < best[0]: best[0] = c
            return
        for i in range(p):
            if T[k][i] > 0:
                v = u[:]; v[i] = min(v[i], T[k][i]); rec(k + 1, v)
    rec(0, list(x))
    # also the sum<1 residuals (u free because sum u < 1): cost N-1 (dominated when kill maps exist, kept for safety)
    return min(best[0], N - 1)

def heavy(t, x, i): return 7 * t[i] > 4 * x[i]

def check(x, T, stats):
    p = len(x)
    ts = tau_star(x, T)
    if ts < F(3, 4): return None
    assert not any(heavy(t, x, l) for t in T for l in range(2, p))
    if any(all(not heavy(t, x, i) for i in range(p)) for t in T):
        t0 = next(t for t in T if all(not heavy(t, x, i) for i in range(p)))
        sl = min(x[i] - M('H', t0[i], 0) for i in range(p)); assert sl >= 0
        stats['H'] += 1; return ('H', sl)
    C1 = [t for t in T if heavy(t, x, 0)]; C2 = [t for t in T if heavy(t, x, 1)]
    assert C1 and C2, 'some C_i empty with tau*>=3/4'
    assert not any(heavy(t, x, 0) and heavy(t, x, 1) for t in T), 'double-heavy type with tau*>=3/4'
    a0 = min(C1, key=lambda t: t[0]); b0 = min(C2, key=lambda t: t[1])
    th1, th2 = a0[0], b0[1]; d1, d2 = x[0] - th1, x[1] - th2
    assert d1 + d2 >= F(3, 4) and th1 + th2 > 1 and x[0] + x[1] > F(7, 4)
    if 3 * th2 <= 2 * x[1]:
        sl = feas('Qb', a0, b0, x); assert sl >= 0, ('Qb fails', x, T); stats['Qb'] += 1; return ('Qb', sl)
    if 3 * th1 <= 2 * x[0]:
        sl = feas('Qa', a0, b0, x); assert sl >= 0, ('Qa fails', x, T); stats['Qa'] += 1; return ('Qa', sl)
    assert th1 + th2 > F(3, 2) and d1 > F(3, 4) - th2 / 2
    Lam = sum(a0[l] for l in range(2, p))
    Sc = [b for b in C2 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
    Ss = [b for b in C2 if all(b[l] + a0[l] < x[l] for l in range(2, p))]
    assert Ss, 'strict survivor set empty'
    out = None
    for S in (Sc, Ss):
        bs = max(S, key=lambda b: x[1] - b[1])
        if bs is not b0: stats['V_bstar_ne_b0'] = stats.get('V_bstar_ne_b0', 0) + 1
        assert x[1] - bs[1] >= F(3, 4) - d1 - Lam, 'residual bound (2)'
        sl = feas('V', a0, bs, x); assert sl >= 0, ('V fails', x, T)
        # the proof's per-part margins: part1 > 0 strictly, part2 > 0 strictly; light parts >= 0
        out = sl if out is None else min(out, sl)
    stats['V'] += 1
    return ('V', out)

def rnd(rng, lo, hi, d): return lo + (hi - lo) * F(rng.randint(0, d), d)

def gen_type(rng, x, d, mode):
    p = len(x); t = [F(0)] * p
    order = []
    if mode in (0, 2): order.append(0)
    if mode in (1, 2): order.append(1)
    rest = F(1)
    for h in order:
        lo = (2 * x[h] / 3 if FOCUS else 4 * x[h] / 7) if rng.random() < 0.8 else F(0)
        hi = min(x[h], rest)
        if hi < lo: return None
        v = rnd(rng, lo, hi, d) if rng.random() < 0.85 else (4 * x[h] / 7 if rng.random() < 0.5 else hi)
        v = min(v, rest); t[h] = v; rest -= v
    others = [i for i in range(p) if i not in order]; rng.shuffle(others)
    for idx, i in enumerate(others):
        cap = min(x[i], rest) if i < 2 else min(4 * x[i] / 7, rest)
        if idx == len(others) - 1: v = rest
        else: v = rnd(rng, F(0), cap, d) if rng.random() < 0.6 else cap
        if v > x[i] or (i >= 2 and v > 4 * x[i] / 7): return None
        t[i] = v; rest -= v
    if rest != 0: return None
    return t

def gen(rng):
    p = rng.choice([2, 3, 3, 4, 4, 5]); d = rng.choice([8, 12, 24, 60])
    x = [rnd(rng, F(4, 5), F(8, 5), d), rnd(rng, F(4, 5), F(8, 5), d)] + \
        [rnd(rng, F(1, 20), F(2, 5) if (FOCUS and rng.random() < 0.7) else F(6, 5), d) for _ in range(p - 2)]
    nT = rng.randint(2, 6 if p <= 3 else (5 if p == 4 else 4))
    T = []
    for _ in range(40):
        if len(T) >= nT: break
        mode = rng.choices([0, 1, 2, 3], [45, 45, 5, 0 if FOCUS else 5])[0]
        t = gen_type(rng, x, d, mode)
        if t is not None and t not in T: T.append(t)
    return x, T

def mutate(rng, x, T):
    x = x[:]; T = [t[:] for t in T]
    d = rng.choice([12, 24, 60, 120])
    if rng.random() < 0.4:
        i = rng.randrange(len(x)); x[i] = max(F(1, 50), x[i] + (F(rng.randint(-6, 6), d)))
    else:
        k = rng.randrange(len(T)); i, j = rng.sample(range(len(x)), 2)
        dv = F(rng.randint(1, 6), d); dv = min(dv, T[k][i])
        T[k][i] -= dv; T[k][j] += dv
    if any(t[i] > x[i] or t[i] < 0 for t in T for i in range(len(x))): return None
    if any(heavy(t, x, l) for t in T for l in range(2, len(x))): return None
    return x, T

def main():
    seed = int(sys.argv[1]); NR = int(sys.argv[2]); NCLIMB = int(sys.argv[3])
    rng = random.Random(seed)
    stats = {'H': 0, 'Qb': 0, 'Qa': 0, 'V': 0}; n = 0; tries = 0
    worst = {}
    while n < NR:
        tries += 1
        x, T = gen(rng)
        if len(T) < 2: continue
        r = check(x, T, stats)
        if r is None: continue
        n += 1
        if r[0] not in worst or r[1] < worst[r[0]][0]: worst[r[0]] = (r[1], x, T)
    print('random: tries', tries, 'instances', n, stats, flush=True)
    for k, v in worst.items(): print('  min slack', k, v[0], float(v[0]))
    # adversarial climbs: minimise slack of the chosen template among tau*>=3/4 instances (V case preferred)
    for c in range(NCLIMB):
        while True:
            x, T = gen(rng)
            if len(T) >= 2:
                r = check(x, T, stats)
                if r is not None and r[0] != 'H' and (not FOCUS or r[0] == 'V'): break
        cur = r
        for it in range(400):
            m = mutate(rng, x, T)
            if m is None: continue
            r2 = check(m[0], m[1], stats)
            if r2 is None or r2[0] == 'H' or (FOCUS and r2[0] != 'V'): continue
            if r2[1] <= cur[1]: x, T = m; cur = r2
        print('climb', c, 'final template', cur[0], 'slack', cur[1], float(cur[1]), 'p', len(x), 'ntypes', len(T),
              flush=True)
    print('stats', stats, 'ALL CHECKS PASSED')

if __name__ == '__main__':
    main()
