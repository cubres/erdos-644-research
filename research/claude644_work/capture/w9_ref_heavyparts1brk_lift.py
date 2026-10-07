"""Referee w9, claim heavyparts#1 (BREAK-IT lens), part 2. Exact.
 (i)  LOSSLESS LIFT: every sub-stochastic instance on parts H is the reduction of a stochastic instance:
      add ONE light part L of capacity Xl >= 7/4 and >= 1 + X_H, pad each type with 1 - sum(a) <= 1 <= 4Xl/7.
      Check exactly: tau*(lifted) == tau*(reduced) and the set of Fano-feasible assignments coincides.
      => 'tau*>3/4 => Fano' for sub-stochastic reduced models is EQUIVALENT to the stochastic statement
         (the reduction neither loses nor gains truth).  Applied also to the attacker's H3-cex.
 (ii) SCOPE: deletion of a light part does NOT preserve feasibility of NON-Fano bad tuples.
      Explicit exact example with the note's six-versus-one construction (note 7.65 l.2012: cells = the six
      5-subsets of rows 1..6 with mass a_i/5 each + the singleton {7} with mass b_i; condition 6a/5+b <= x),
      whose cell family is checked to be pairwise non-covering (bad).  Feasible after deleting the light
      part, infeasible before; Fano status unchanged.
 (iii) INTEGRALITY: in a finite family a light part is not automatically free: seven rows of load 1 in a
      part of 2 points (7*1 <= 4*2, so 4/7-light) have NO Fano-downset realisation; 3 points suffice.
"""
import itertools, random
from fractions import Fraction as F
import importlib.util, os
spec = importlib.util.spec_from_file_location('ex', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'w9_ref_heavyparts1brk_exact.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
LINES = ex.LINES

def fano_set(x, T, parts):
    return {asg for asg in itertools.product(range(len(T)), repeat=7) if ex.asg_ok(x, T, asg, parts)}

def lift(xH, TH):
    XH = sum(xH); Xl = max(F(7, 4), 1 + XH) + F(1, 3)
    x = list(xH) + [Xl]
    T = [list(a) + [1 - sum(a)] for a in TH]
    return x, T

def part_i(rng):
    ok = 0; n = 0
    for it in range(150):
        p = rng.randint(1, 3); m = rng.randint(1, 3)
        xH = [ex.rnd_frac(rng, 0.1, 1.6) for _ in range(p)]
        TH = []
        for _ in range(m):
            a = [xH[i] * ex.rnd_frac(rng, 0, 1) for i in range(p)]
            s = sum(a)
            if s > 1: a = [v / s for v in a]
            if sum(a) == 0: a[0] = xH[0] / 2
            TH.append(a)
        x, T = lift(xH, TH)
        assert all(sum(a) == 1 for a in T) and all(a[-1] * 7 <= 4 * x[-1] for a in T)
        r = ex.tau_M1(xH, TH, list(range(p))); o = ex.tau_M1(x, T, list(range(p + 1)))
        fr = fano_set(xH, TH, range(p)); fo = fano_set(x, T, range(p + 1))
        n += 1; ok += (r == o and fr == fo)
        if not (r == o and fr == fo): print('LIFT MISMATCH', xH, TH, r, o)
    print('(i) lossless lift: %d/%d exact matches (tau* equal and Fano assignment sets equal)' % (ok, n))
    # attacker's H3-cex (stochastic already, 3 parts, part C tiny but HEAVY -> must NOT be deleted)
    x = [F(5, 4), F(5, 4), F(3, 200)]
    T = [[F(3, 20), F(17, 20), F(0)], [F(17, 20), F(3, 20), F(0)], [F(84, 100), F(15, 100), F(1, 100)]]
    Hp = [i for i in range(3) if any(7 * a[i] > 4 * x[i] for a in T)]
    print('    H3-cex: heavy parts', Hp, 'tau*', ex.tau_M1(x, T, [0, 1, 2]), 'Fano assignments', len(fano_set(x, T, range(3))))
    # what if someone (wrongly) deleted the tiny part C because it is tiny? gamma restricted to A,B
    print('    H3-cex with tiny heavy part C wrongly deleted: Fano assignments', len(fano_set(x, T, [0, 1])),
          ' tau*(A,B only)', ex.tau_M1(x, T, [0, 1]))

def bad_cells(cells):
    full = frozenset(range(7))
    return all(frozenset(S) | frozenset(Tt) != full for S in cells for Tt in cells)

def part_ii():
    cells = [tuple(c) for c in itertools.combinations(range(6), 5)] + [(6,)]
    assert bad_cells(cells)
    # parts A (heavy), B (tiny, heavy), L (light).  type a -> six rows, type b -> seventh row.
    x = [F(1), F(3, 10), F(1)]
    a = [F(3, 5), F(0), F(2, 5)]            # a_A=.6 > 4/7 heavy; a_L=.4 <= 4/7
    b = [F(1, 5), F(8, 35), F(4, 7)]        # b_B=8/35 > 4(3/10)/7=6/35 heavy; b_L = 4/7 exactly (boundary light)
    assert sum(a) == 1 and sum(b) == 1
    xA, xL = x[0], x[2]
    assert 7 * a[2] <= 4 * xL and 7 * b[2] <= 4 * xL and 7 * a[0] > 4 * xA and 7 * b[1] > 4 * x[1]
    def six_one_ok(parts, x):
        # explicit masses: a_i/5 on each of the six 5-cells, b_i on {7}; loads & capacity checked exactly
        for i in parts:
            mass = {c: a[i] / 5 for c in cells[:6]}; mass[(6,)] = b[i]
            loads = [sum(v for c, v in mass.items() if r in c) for r in range(7)]
            assert loads == [a[i]] * 6 + [b[i]]
            if sum(mass.values()) > x[i]: return False
        return True
    print('(ii) six-vs-one (non-Fano, bad cells verified): reduced (L deleted):', six_one_ok([0, 1], x),
          ' original:', six_one_ok([0, 1, 2], x), ' [L-part needs 6a/5+b = %s > x_L = %s]' % (6 * a[2] / 5 + b[2], xL))
    T = [a, b]
    print('     Fano assignment sets equal before/after deletion:', fano_set(x, T, [0, 1]) == fano_set(x, T, [0, 1, 2]),
          ' #Fano =', len(fano_set(x, T, [0, 1, 2])),
          ' tau* orig/red:', ex.tau_M1(x, T, [0, 1, 2]), ex.tau_M1(x, T, [0, 1]))

def part_iii():
    comps = [frozenset(range(7)) - frozenset(L) for L in LINES]
    def realisable(npts):
        # each point gets a row set inside some line complement; need every row covered (then trim to load 1)
        subsets = set()
        for C in comps:
            for r in range(1, 5):
                for S in itertools.combinations(sorted(C), r): subsets.add(frozenset(S))
        for choice in itertools.product(list(subsets), repeat=npts):
            if frozenset().union(*choice) == frozenset(range(7)): return True
        return False
    print('(iii) integral Fano realisation of 7 rows of load 1: 2 points ->', realisable(2), '; 3 points ->', realisable(3))

if __name__ == '__main__':
    part_i(random.Random(5)); part_ii(); part_iii()
