"""Referee w9, claim heavyparts#1: 'Fano feasibility ignores light parts (reduced model)'.
Independent exact checks (Fractions), own Fano labelling (rows = points of PG(2,2), lines {i,i+1,i+3} mod 7,
cells in complements of lines, as in note Lemma 7.63), own tau* from the free-residual definition (note sec.3):
  u free  <=>  no type a with a <= u   <=>  exists blocking map pi with u_{pi(a)} < a_{pi(a)} for every a.
Checks:
 (A) light-part safety constructively (no Lemma 7.63 'only if' direction): at a 4/7-light part, the homogeneous
     parent construction (seven point classes of mass x/7, row j = four classes off a line) gives every row load
     4x/7 >= z_j with total mass x; trimming gives exact loads.  Also the Lemma-7.63 inequalities hold.
 (B) Fano existence(C, x) == Fano existence(C|H, x|H) (exhaustive over all m^7 row assignments).
 (C) invariance: resample light traces (keep them light, keep sums 1 by moving mass among light parts) -> same answer.
 (D) tau*(C|H) >= tau*(C) exactly; record strictness.
 (E) per-part criterion cross-check vs float LP (scipy HiGHS) on random loads.
 (F) scope caveat: two-type (non-Fano) bad tuples are NOT light-part invariant: exact example with the
     42-function catalogue (heavy/astra_support_capacity_minimal.json).
 (G) edge case: a type with zero H-trace (everywhere light) -> no free residual in the reduced model.
"""
import itertools, random, json, sys
from fractions import Fraction as F

LINES = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]
assert all(len(L1 & L2) == 1 for L1 in LINES for L2 in LINES if L1 != L2)

def part_ok(z, x):
    if max(z) > x: return False
    if sum(z) > 4 * x: return False
    return all(sum(z[j] for j in L) <= 2 * x for L in LINES)

def fano_exists(x, T):
    m = len(T); p = len(x)
    # per part, precompute nothing; exhaustive
    for asg in itertools.product(range(m), repeat=7):
        if all(part_ok([T[a][i] for a in asg], x[i]) for i in range(p)):
            return asg
    return None

def tau_star(x, T):
    """None = +infinity (no free residual)."""
    p = len(x); X = sum(x)
    choices = [[i for i in range(p) if a[i] > 0] for a in T]
    if any(len(c) == 0 for c in choices): return None
    best = None
    for pi in itertools.product(*choices):
        caps = list(x)
        for j, i in enumerate(pi): caps[i] = min(caps[i], T[j][i])
        s = sum(caps)
        if best is None or s > best: best = s
    return X - best

def homog_light_construction(z, x):
    """explicit masses: class q (point q) mass x/7; row j gets the 4 classes off line LINES[j'] where we index rows by
    lines: row j <-> line LINES[j]; its load = 4x/7.  Return True iff loads >= z and total == x (exact)."""
    mass = [x / 7] * 7
    loads = [sum(mass[q] for q in range(7) if q not in LINES[j]) for j in range(7)]
    # two rows' cell sets: point q is in rows {j: q not in LINES[j]} = complement of a line's-dual: must be a line
    # complement in the row-labelling. check the cell of q, as a set of rows, is contained in a complement of a line
    for q in range(7):
        cell = frozenset(j for j in range(7) if q not in LINES[j])
        # rows are labelled by lines; the rows missing q are lines through... verify cell misses some 'row-line'
        # row-lines: a set of three rows whose lines share a point
        rowlines = [frozenset(j for j in range(7) if r in LINES[j]) for r in range(7)]
        assert any(not (cell & RL) for RL in rowlines)
        assert all(len(R1 & R2) == 1 for R1 in rowlines for R2 in rowlines if R1 != R2)
    return all(loads[j] >= z[j] for j in range(7)) and sum(mass) == x

def rnd_frac(lo, hi, den=60):
    a = int(lo * den) + 1; b = int(hi * den)
    if b < a: return F(a, den)
    return F(random.randint(a, b), den)

def random_instance(p, h, m):
    """h heavy parts (0..h-1), p-h light parts.  Types stochastic, light traces <= 4x/7."""
    while True:
        x = [F(random.randint(30, 90), 60) for _ in range(p)]
        T = []
        for _ in range(m):
            a = [F(0)] * p
            for j in range(h, p):
                a[j] = F(random.randint(0, int(F(4, 7) * x[j] * 120)), 120)
            rest = 1 - sum(a[h:])
            if rest < 0: break
            # distribute rest among heavy parts with a_i <= x_i
            w = [random.random() ** 2 for _ in range(h)]
            s = sum(w)
            vals = [F(int(rest * 120 * wi / s), 120) for wi in w]
            vals[0] += rest - sum(vals)
            if any(v < 0 or v > x[i] for i, v in enumerate(vals)): break
            a[:h] = vals
            T.append(a)
        if len(T) < m: continue
        # heavy parts must actually be heavy for some type (definition of H)
        H = [i for i in range(p) if any(7 * a[i] > 4 * x[i] for a in T)]
        if H != list(range(h)): continue
        return x, T

def resample_light(x, T, h):
    """keep heavy traces, redraw light traces keeping light and total mass per type."""
    p = len(x); out = []
    for a in T:
        Lmass = sum(a[h:])
        for _ in range(200):
            b = list(a[:h])
            caps = [F(4, 7) * x[j] for j in range(h, p)]
            if Lmass > sum(caps): return None
            w = [random.random() for _ in caps]
            # water-fill proportional then clip
            vals = [min(c, Lmass * wi / sum(w)) for c, wi in zip(caps, w)]
            r = Lmass - sum(vals)
            for k in range(len(vals)):
                add = min(caps[k] - vals[k], r); vals[k] += add; r -= add
            if r == 0:
                out.append(b + vals); break
        else:
            return None
    return out

def main(seed=0, N=150):
    random.seed(seed)
    stats = dict(inst=0, fano=0, nofano=0, strict_tau=0, eq_tau=0, resampled=0, construct=0)
    for it in range(N):
        p = random.choice([3, 3, 4]); h = random.choice([1, 2, 2, 3]) if p == 4 else random.choice([1, 2, 2])
        m = 3
        x, T = random_instance(p, h, m)
        # (A) light safety constructive + inequalities for arbitrary 7-tuples of light traces
        for j in range(h, p):
            for asg in itertools.islice(itertools.product(range(m), repeat=7), 0, None, 97):
                z = [T[a][j] for a in asg]
                assert part_ok(z, x[j])
                assert homog_light_construction(z, x[j]); stats['construct'] += 1
        fx = fano_exists(x, T)
        xr = x[:h]; Tr = [a[:h] for a in T]
        fr = fano_exists(xr, Tr)
        assert (fx is None) == (fr is None), (x, T)
        if fr is not None:  # lift reduced tuple and check exactly in full model
            assert all(part_ok([T[a][i] for a in fr], x[i]) for i in range(p))
        stats['fano' if fx else 'nofano'] += 1
        t = tau_star(x, T); tr = tau_star(xr, Tr)
        assert t is not None
        assert tr is None or tr >= t, (x, T, t, tr)
        if tr is not None and tr > t: stats['strict_tau'] += 1
        else: stats['eq_tau'] += 1
        T2 = resample_light(x, T, h)
        if T2 is not None:
            f2 = fano_exists(x, T2)
            assert (f2 is None) == (fx is None)
            stats['resampled'] += 1
        stats['inst'] += 1
    print('seed', seed, stats)

def lp_crosscheck(n=300, seed=1):
    import numpy as np
    from scipy.optimize import linprog
    random.seed(seed)
    # parent cells = complements of row-lines (rows labelled by LINES index); row-lines as above
    rowlines = [frozenset(j for j in range(7) if r in LINES[j]) for r in range(7)]
    comps = [frozenset(range(7)) - RL for RL in rowlines]
    B = np.array([[1.0 if j in C else 0.0 for C in comps] for j in range(7)])
    bad = 0
    for _ in range(n):
        z = [random.random() * random.choice([0.3, 1, 1]) for _ in range(7)]
        res = linprog(np.ones(7), A_ub=-B, b_ub=-np.array(z), bounds=[(0, None)] * 7, method='highs')
        M = max(max(z), max(sum(z[j] for j in RL) for RL in rowlines) / 2, sum(z) / 4)
        if abs(res.fun - M) > 1e-9: bad += 1
    print('LP cross-check of Lemma 7.63 min-mass formula (row-lines labelling):', n, 'loads, mismatches', bad)

def caveat_pairs():
    D = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
    FUNCS = [[(F(u), F(v)) for u, v in f['vertices']] for f in D['minimal_functions']]
    def pair_ok(x, a, b):
        return [k for k, V in enumerate(FUNCS) if all(max(u * a[i] + v * b[i] for u, v in V) <= x[i] for i in range(len(x)))]
    # two types, parts A,B heavy, part L light for both but alpha_L+beta_L > x_L
    x = [F(6, 5), F(6, 5), F(19, 60)]
    al = [F(41, 50), F(0), F(9, 50)]; be = [F(0), F(41, 50), F(9, 50)]
    T = [al, be]
    assert all(7 * a[2] <= 4 * x[2] for a in T)
    H = [i for i in range(3) if any(7 * a[i] > 4 * x[i] for a in T)]
    print('caveat: x', x, 'H', H)
    full = pair_ok(x, al, be) + pair_ok(x, be, al) + pair_ok(x, al, al) + pair_ok(x, be, be)
    red = pair_ok(x[:2], al[:2], be[:2]) + pair_ok(x[:2], be[:2], al[:2]) + pair_ok(x[:2], al[:2], al[:2]) + pair_ok(x[:2], be[:2], be[:2])
    print('  two-type catalogue functions feasible: full model', len(full), ' reduced model', len(red))
    print('  Fano exists full', fano_exists(x, T) is not None, ' reduced', fano_exists(x[:2], [a[:2] for a in T]) is not None)
    print('  tau* full', tau_star(x, T), ' reduced', tau_star(x[:2], [a[:2] for a in T]))

def edge_zero_trace():
    x = [F(1), F(1), F(1)]
    g = [F(0), F(1, 2), F(1, 2)]    # light at parts 1,2 (1/2 <= 4/7)
    a = [F(4, 5), F(1, 10), F(1, 10)]  # heavy at part 0 only
    T = [a, g]
    H = [i for i in range(3) if any(7 * t[i] > 4 * x[i] for t in T)]
    Tr = [[t[i] for i in H] for t in T]; xr = [x[i] for i in H]
    print('edge case zero-H-trace type: H', H, 'reduced types', Tr, 'tau*(C)', tau_star(x, T),
          'tau*(C|H) =', 'infinity (no free residual)' if tau_star(xr, Tr) is None else tau_star(xr, Tr),
          'Fano full', fano_exists(x, T) is not None, 'Fano reduced', fano_exists(xr, Tr) is not None)

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    lp_crosscheck()
    caveat_pairs()
    edge_zero_trace()
    main(seed, N)
