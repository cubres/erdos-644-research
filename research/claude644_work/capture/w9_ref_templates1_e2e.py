# Referee w9, claim templates#1 (Theorem 2UB).  Independent EXACT end-to-end check.
# Independent of tmpl/verify_twoupbox.py:
#  * tau* computed from the note's Lemma 7.56 blocker formula (all subsets S), not the 2UB closed form;
#  * templates are checked by EXPLICIT cell masses (Fano line complements / the ten V cells), exact row
#    loads and part masses, and a brute-force Venn check that no two used cells cover all seven rows;
#  * instances: generic random generators (any support), attacker-like heavy ones, and boundary instances
#    pushed to tau* = 3/4 exactly by capacity shrinking; p = 2..7.
# Usage: python3 w9_ref_templates1_e2e.py SEED N [mode]   mode in {main, below, mutate}
import random, itertools, sys
from fractions import Fraction as F

FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
ROWS = frozenset(range(7))
COMP = [ROWS - set(l) for l in FANO]           # parent cells of Fano support

def tau_star(x, gens):
    """Note Lemma 7.56 with l=g, h=x (up-box)."""
    p = len(x); N = sum(x)
    def blockers(g):
        B = [(frozenset([i]), x[i]-g[i]) for i in range(p) if g[i] > 0]
        for r in range(1, p+1):
            for S in itertools.combinations(range(p), r):
                b = 1 - sum(x[i] for i in range(p) if i not in S)
                if b > 0: B.append((frozenset(S), sum(x[i] for i in S) - b))
        return B
    B1, B2 = blockers(gens[0]), blockers(gens[1])
    return min(max(al, be, al+be-sum(x[i] for i in S & T)) for S, al in B1 for T, be in B2)

def check_tuple(x, types, cellmass):
    """types: 7 type vectors; cellmass: per part dict cell->mass. Exact Venn + loads + capacities."""
    p = len(x)
    used = set()
    for i in range(p):
        tot = sum(cellmass[i].values())
        if tot > x[i]: return False, 'cap %d' % i
        for j in range(7):
            load = sum(m for c, m in cellmass[i].items() if j in c)
            if load < types[j][i]: return False, 'load row %d part %d' % (j, i)
        used |= {c for c, m in cellmass[i].items() if m > 0}
    for c1 in used:
        for c2 in used:
            if c1 | c2 == ROWS: return False, 'cover'
    return True, 'ok'

def fano_masses(z):
    """Explicit Fano realisation of loads z (7 rows) -- only the two patterns used here."""
    raise NotImplementedError

def H_real(x, a):
    types = [a]*7
    cm = [{c: a[i]/4 for c in COMP} for i in range(len(x))]
    return check_tuple(x, types, cm)

def Q_real(x, s_type, t_type):
    """three t_type rows on line L=FANO[0], four s_type rows off L (note Lemma 7.57 masses)."""
    L = FANO[0]
    types = [t_type if j in L else s_type for j in range(7)]
    cm = []
    for i in range(len(x)):
        s, t = s_type[i], t_type[i]
        v = F(3, 2)*t; u = max(F(0), s - F(3, 4)*t)
        d = {}
        for l, c in zip(FANO, COMP):
            if l == L: d[c] = d.get(c, 0) + u
            else: d[c] = d.get(c, 0) + v/6
        cm.append(d)
    return check_tuple(x, types, cm)

# V: rows 0=b0, 1=b1 (type b); 2..5 = w1..w4, 6 = z (type a)
b0, b1, w1, w2, w3, w4, z = range(7)
A5 = [frozenset(S) for S in itertools.combinations([w1, w2, w3, w4, z], 4)]
BB = frozenset([b0, b1]); W = frozenset([w1, w2, w3, w4])
MIX = [frozenset([b0, w3, w4, z]), frozenset([b0, w1, w2, z]), frozenset([b1, w2, w4, z]), frozenset([b1, w1, w3, z])]
def V_real(x, a, b):
    types = [b, b] + [a]*5
    cm = []
    for i in range(len(x)):
        s, t = a[i], b[i]
        d = {}
        def add(c, m):
            if m: d[c] = d.get(c, 0) + m
        if 2*t <= s:   # t*(2,1) + (s-2t)*(1,0)
            add(W, t); [add(c, t/2) for c in MIX]; [add(c, (s-2*t)/4) for c in A5]
        else:          # (s/2)*(2,1) + (t-s/2)*(0,1)
            add(W, s/2); [add(c, s/4) for c in MIX]; add(BB, t - s/2)
        cm.append(d)
    return check_tuple(x, types, cm)

def in_U(a, g, x):
    return sum(a) == 1 and all(g[i] <= a[i] <= x[i] for i in range(len(x)))

HEAVYP = 0.9
def rnd(rng, lo, hi, d): return lo + (hi-lo)*F(rng.randint(0, d), d)

def sample_heavy(rng):
    p = rng.choice([2, 3, 3, 4, 4, 5, 6, 7]); d = rng.choice([6, 8, 12, 24, 60])
    x = [rnd(rng, F(1, 10), F(2), d) for _ in range(p)]
    I, J = rng.sample(range(p), 2)
    gens = []
    for H in (I, J):
        g = [F(0)]*p
        g[H] = rnd(rng, min(F(1), 4*x[H]/7), min(F(1), x[H]), d)
        budget = 1 - g[H]
        for i in rng.sample(range(p), p):
            if i != H and rng.random() < 0.6 and budget > 0:
                v = min(budget, x[i]) * rnd(rng, F(0), F(1), d); g[i] = v; budget -= v
        gens.append(g)
    return x, gens

def sample(rng):
    if rng.random() < 0.7: return sample_heavy(rng)
    p = rng.choice([2, 3, 3, 4, 4, 5, 6, 7]); d = rng.choice([6, 8, 12, 24, 60])
    x = [rnd(rng, F(1, 10), F(2), d) for _ in range(p)]
    gens = []
    for _ in range(2):
        g = [F(0)]*p
        if rng.random() < HEAVYP:   # heavy-style
            H = rng.randrange(p); g[H] = rnd(rng, min(F(1), 4*x[H]/7), min(F(1), x[H]), d)
        for i in range(p):
            if g[i] == 0 and rng.random() < 0.5:
                g[i] = rnd(rng, F(0), min(x[i], F(1)), d)
        # rescale if sum > 1
        s = sum(g)
        if s > 1: g = [gi/s for gi in g]
        gens.append(g)
    return x, gens

def push_to_boundary(rng, x, gens, target=F(3, 4), steps=6):
    x = list(x)
    for _ in range(steps):
        t = tau_star(x, gens)
        if t <= target: break
        i = rng.randrange(len(x))
        room = x[i] - max(gens[0][i], gens[1][i], 0)
        dlt = min(t - target, room) * rng.choice([F(1), F(1), F(1, 2)])
        if dlt > 0: x[i] -= dlt
    return x

def run(seed, NT, mode):
    rng = random.Random(seed)
    st = {'n': 0, 'H': 0, 'Qb': 0, 'Qa': 0, 'V': 0, 'eq34': 0, 'pairs': 0, 'mutfail': 0, 'belowfail': 0}
    while st['n'] < NT:
        x, gens = sample(rng)
        if rng.random() < 0.5: x = push_to_boundary(rng, x, gens)
        g, h = gens
        t = tau_star(x, gens)
        if mode == 'below':
            if not (F(7, 10) <= t < F(3, 4)): continue
        elif t < F(3, 4): continue
        st['n'] += 1; st['eq34'] += (t == F(3, 4))
        ok_any = False
        for gen, other in ((g, h), (h, g)):
            if all(7*gen[i] <= 4*x[i] for i in range(len(x))):
                a = list(gen); rest = 1 - sum(a)
                for i in range(len(x)):
                    add = min(rest, 4*x[i]/7 - a[i]); a[i] += add; rest -= add
                assert rest == 0 or mode == 'below', 'H fill'
                if rest == 0:
                    assert in_U(a, gen, x); r = H_real(x, a); assert r[0], r
                    ok_any = True
        if ok_any: st['H'] += 1; continue
        Is = [i for i in range(len(x)) if 7*g[i] > 4*x[i]]; Js = [i for i in range(len(x)) if 7*h[i] > 4*x[i]]
        for I in Is:
            for J in Js:
                if mode == 'below' and I == J: continue
                assert I != J
                st['pairs'] += 1
                a = list(g); b = list(h)
                if mode == 'mutate':  # WRONG canonical choice: fill own heavy part (if room) -- expect failures
                    a[I] += 1 - sum(g); b[J] += 1 - sum(h)
                    if not (in_U(a, g, x) and in_U(b, h, x)): st['mutfail'] += 1; continue
                else:
                    a[J] += 1 - sum(g); b[I] += 1 - sum(h)
                    if mode == 'main': assert in_U(a, g, x) and in_U(b, h, x), ('adm', x, g, h, I, J)
                    elif not (in_U(a, g, x) and in_U(b, h, x)): st['belowfail'] += 1; continue
                res = [('Qb', Q_real(x, a, b)[0]), ('Qa', Q_real(x, b, a)[0]), ('V', V_real(x, a, b)[0])]
                good = [k for k, r in res if r]
                if mode == 'main':
                    assert good, ('FAIL', x, g, h, I, J)
                    if (I, J) == (Is[0], Js[0]): st[good[0]] += 1
                elif not good:
                    st['mutfail' if mode == 'mutate' else 'belowfail'] += 1
    return st

if __name__ == '__main__':
    seed = int(sys.argv[1]); NT = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'main'
    st = run(seed, NT, mode)
    print('seed', seed, 'mode', mode, st, 'DONE' + (' ALL CHECKS PASSED' if mode == 'main' else ''))
