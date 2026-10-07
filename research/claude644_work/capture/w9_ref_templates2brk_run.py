# Referee w9 (BREAK-IT), templates#2 / Theorem H2: counterexample search driver (exact rationals).
# usage: python3 w9_ref_templates2brk_run.py SEED N_GRID N_RAND N_CLIMB
#  GRID  : C = ALL lattice types (denominator D) in a union of random boxes (heavy lower bound at part 0 or 1,
#          random upper bounds), admissible (a <= x) and light (a_l <= 4x_l/7) at parts >= 2.  Dense closed sets
#          with massive ties and boundary coordinates (incl. exactly 4x/7).
#  RAND  : sparse random types with exact boundary values and forced ties.
#  every instance with tau* >= 3/4 is also pushed towards tau* = 3/4 EXACTLY by lowering x_0 or x_1.
#  recipe run 3 times with random tie-breaking + once with the strict survivor set; template verified at Venn level.
#  necessity/mutation counters: tau* in [0.70,3/4); b0 instead of b*; Q instead of V in case C.
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w9_ref_templates2brk_lib import *

seed, NG, NR, NC = map(int, sys.argv[1:5])
FOCUS = len(sys.argv) > 5 and sys.argv[5] == 'V'
WIDE = len(sys.argv) > 5 and sys.argv[5] == 'W'   # heavy capacities in [1/5, 9/5] (one heavy part may be tiny)
rng = random.Random(seed)
st = {'inst': 0, 'eq': 0, 'H': 0, 'Qb': 0, 'Qa': 0, 'V': 0, 'V_bs_ne_b0': 0, 'V_Lam_pos': 0,
      'mut_low_tau_fail': 0, 'mut_low_tau_n': 0, 'mut_b0_fail': 0, 'mut_b0_n': 0, 'mut_QinC_fail': 0}
minsl = {}

def compositions(D, p):
    if p == 1:
        yield (D,); return
    for k in range(D + 1):
        for r in compositions(D - k, p - 1): yield (k,) + r

def rq(lo, hi, d): return lo + (hi - lo) * F(rng.randint(0, d), d)

def gen_grid():
    p = rng.choice([2, 3, 3, 4, 4, 5]); D = {2: 24, 3: 12, 4: rng.choice([8, 10]), 5: 6}[p]
    x = [rq(F(1), F(8, 5), 20), rq(F(1), F(8, 5), 20)] + [rq(F(1, 20), F(6, 5), 20) for _ in range(p - 2)]
    if rng.random() < 0.3:   # capacities on the grid -> coordinates exactly 4x/7 possible when 7 | 4Dx ... use multiples of 7/4D
        x = [F(7 * rng.randint(1, 2 * D), 4 * D) if rng.random() < 0.5 else xi for xi in x]
        x[0] = max(x[0], F(1)); x[1] = max(x[1], F(1))
    boxes = []
    for _ in range(rng.randint(1, 3)):
        h = rng.randrange(2)
        lo = [F(0)] * p; hi = [F(1)] * p
        lo[h] = rq(4 * x[h] / 7, min(x[h], F(1)), 12) if rng.random() < 0.9 else F(0)
        for i in range(p):
            if i != h and rng.random() < 0.4: hi[i] = rq(F(0), F(1), 6)
            if i != h and rng.random() < 0.15: lo[i] = rq(F(0), F(1, 3), 6)
        boxes.append((lo, hi))
    T = []
    for c in compositions(D, p):
        a = [F(v, D) for v in c]
        if any(a[i] > x[i] for i in range(p)): continue
        if any(heavy(a, x, l) for l in range(2, p)): continue
        if any(all(lo[i] <= a[i] <= hi[i] for i in range(p)) for lo, hi in boxes): T.append(a)
    return x, T

def gen_rand():
    p = rng.choice([2, 3, 4, 5, 6]); d = rng.choice([6, 12, 20, 28])
    x = [rq(F(9, 10), F(8, 5), d), rq(F(9, 10), F(8, 5), d)] + [rq(F(1, 50), F(3, 2), d) for _ in range(p - 2)]
    if WIDE:
        big = rng.randrange(2); x[big] = rq(F(6, 5), F(9, 5), d); x[1 - big] = rq(F(1, 5), F(9, 5), d)
    if FOCUS:
        p = rng.choice([3, 3, 4, 5]); x = [rq(F(21, 20), F(3, 2), d), rq(F(21, 20), F(3, 2), d)] + \
            [rq(F(1, 50), F(1, 2) if rng.random() < 0.7 else F(3, 2), d) for _ in range(p - 2)]
    T = []
    for _ in range(rng.randint(2, 7)):
        h = rng.randrange(2); t = [F(0)] * p
        choices = [4 * x[h] / 7, rq(4 * x[h] / 7, min(x[h], F(1)), d), min(x[h], F(1)), 2 * x[h] / 3]
        if FOCUS: choices = [rq(2 * x[h] / 3, min(x[h], F(1)), d), min(x[h], F(1)), rq(F(1, 2), min(x[h], F(1)), d)]
        if T and rng.random() < 0.3: choices.append(rng.choice(T)[h])      # force ties
        t[h] = min(rng.choice(choices), F(1), x[h]); rest = 1 - t[h]
        others = [i for i in range(p) if i != h]; rng.shuffle(others)
        for j, i in enumerate(others):
            cap = min(rest, x[i] if i < 2 else 4 * x[i] / 7)
            if j == len(others) - 1: v = rest
            else: v = rng.choice([F(0), cap, rq(F(0), cap, d)])
            t[i] = v; rest -= v
        if rest != 0 or any(t[i] > x[i] or t[i] < 0 for i in range(p)) or any(heavy(t, x, l) for l in range(2, p)): continue
        if t not in T: T.append(t)
    return x, T

last = [None]
def run_recipes(x, T, tag):
    """returns min slack over the randomised recipe runs (non-H), or None if tau*<3/4"""
    out = None
    for r in range(4):
        try:
            res = recipe(x, T, rng=(rng if r < 3 else None), strict_S=(r == 3))
        except Fail as e:
            print('FAIL (intermediate claim)', e, x, T, flush=True); raise
        if res is None: return None
        name, sl, info = res
        if r == 0: last[0] = name
        if sl < 0:
            print('COUNTEREXAMPLE: template', name, 'slack', sl, x, T, flush=True); raise SystemExit(1)
        if r == 0:
            st[name] += 1
            if name == 'V':
                a0, bs, b0 = info
                if bs is not b0: st['V_bs_ne_b0'] += 1
                if any(a0[l] > 0 for l in range(2, len(x))): st['V_Lam_pos'] += 1
                # mutation: b0 instead of b*, and Q templates instead of V
                st['mut_b0_n'] += 1
                if template_slack('V', a0, b0, x) < 0: st['mut_b0_fail'] += 1
                if template_slack('Qb', a0, bs, x) < 0 and template_slack('Qa', a0, bs, x) < 0: st['mut_QinC_fail'] += 1
        if name != 'H':
            key = (tag, name)
            if key not in minsl or sl < minsl[key][0]: minsl[key] = (sl, x, T)
            out = sl if out is None else min(out, sl)
    return out if out is not None else F(10)

def low_tau_mutation(x, T):
    ts = tau_star(x, T)
    if not (F(7, 10) <= ts < F(3, 4)): return
    # pretend tau* >= 3/4: run the recipe's choices and see whether its template fails
    p = len(x)
    if any(not any(heavy(t, x, i) for i in range(p)) for t in T): return
    C1 = [t for t in T if heavy(t, x, 0)]; C2 = [t for t in T if heavy(t, x, 1)]
    if not C1 or not C2 or any(heavy(t, x, 0) and heavy(t, x, 1) for t in T): return
    st['mut_low_tau_n'] += 1
    a0 = min(C1, key=lambda t: t[0]); b0 = min(C2, key=lambda t: t[1])
    ok = False
    for nm in ('Qb', 'Qa'):
        if template_slack(nm, a0, b0, x) >= 0: ok = True
    S = [b for b in C2 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
    if S:
        bs = max(S, key=lambda b: x[1] - b[1])
        if template_slack('V', a0, bs, x) >= 0: ok = True
    if not ok: st['mut_low_tau_fail'] += 1

def push_equal(x, T, tag):
    """lower x_0 or x_1 by tau*-3/4 repeatedly; keep types admissible (drop inadmissible ones)."""
    for _ in range(5):
        ts = tau_star(x, T)
        if ts < F(3, 4): return
        if ts == F(3, 4):
            st['eq'] += 1; return
        i = rng.randrange(2)
        x = x[:]; x[i] -= ts - F(3, 4)
        if x[i] <= 0: return
        T = [t for t in T if t[i] <= x[i]]
        if len(T) < 1: return
        st['inst'] += 1
        if run_recipes(x, T, tag + '_push') is None: return

def mutate(x, T):
    x = x[:]; T = [t[:] for t in T]; p = len(x)
    d = rng.choice([24, 60, 120, 420])
    if rng.random() < 0.35:
        i = rng.randrange(p); x[i] = max(F(1, 100), x[i] + F(rng.randint(-5, 5), d))
    else:
        k = rng.randrange(len(T)); i, j = rng.sample(range(p), 2)
        dv = min(F(rng.randint(1, 5), d), T[k][i]); T[k][i] -= dv; T[k][j] += dv
        if rng.random() < 0.2 and len(T) < 7: T.append(T[k][:]); T[k][i] += dv; T[k][j] -= dv
    if any(t[i] > x[i] or t[i] < 0 for t in T for i in range(p)): return None
    if any(heavy(t, x, l) for t in T for l in range(2, p)): return None
    return x, T

ng = nr = 0; tries = 0
while ng < NG:
    tries += 1
    x, T = gen_grid()
    if len(T) < 1: continue
    if len(T) > 700: continue
    low_tau_mutation(x, T)
    r = run_recipes(x, T, 'grid')
    if r is None: continue
    ng += 1; st['inst'] += 1
    push_equal(x, T, 'grid')
    if ng % 50 == 0: print('grid', ng, st, flush=True)
while nr < NR:
    x, T = gen_rand()
    if len(T) < 2: continue
    low_tau_mutation(x, T)
    r = run_recipes(x, T, 'rand')
    if r is None: continue
    nr += 1; st['inst'] += 1
    push_equal(x, T, 'rand')
    if nr % 2000 == 0: print('rand', nr, st, flush=True)
# adversarial climbs: minimise the recipe template's slack (non-H), tau* >= 3/4 maintained
for c in range(NC):
    while True:
        x, T = gen_rand()
        if len(T) < 2: continue
        r = run_recipes(x, T, 'climb')
        if r is not None and r < F(10) and (not FOCUS or last[0] == 'V'): break
    cur = r
    for it in range(300):
        m = mutate(x, T)
        if m is None: continue
        r2 = run_recipes(m[0], m[1], 'climb')
        if r2 is None or r2 == F(10) or (FOCUS and last[0] != 'V'): continue
        if r2 <= cur: x, T, cur = m[0], m[1], r2
    print('climb', c, 'final min slack', cur, float(cur), 'p', len(x), 'n', len(T), flush=True)
print('FINAL', st)
for k, v in sorted(minsl.items()): print('  min slack', k, v[0], float(v[0]))
print('ALL CHECKS PASSED')
