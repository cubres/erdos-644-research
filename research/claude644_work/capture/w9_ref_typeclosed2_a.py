"""[typeclosed#2] part (a) + sanity of the library.
1. library sanity: note 7.79 family tau* = 483/640 exactly; it has a Fano bad tuple (3 super classes).
2. Fano plane not 2-colourable (dual form: every 2-colouring of the 7 LINES has a point whose 3 lines are
   monochromatic) -- exhaustive over 2^7.
3. (a) random exact test: 3 parts, part 0 4/7-light, every type super-heavy (>2/3 fill) at exactly one of j,k:
   exhaustive Fano search finds NO Fano tuple (as claimed).  Also check: with such families, the exact minimiser pair
   fails Q_b and Q_a (R1/R2), x_j+x_k>9/4 whenever d_j+d_k>3/4.
4. literal-statement caveat: adding an everywhere-4/7-light type keeps the minimiser pair failing Q_b,Q_a but a
   (homogeneous) Fano tuple exists -> (a) needs 'no everywhere-light type' (automatic in a counterexample).
5. sharpness of 2/3: classes heavy (>4/7) but not super-heavy can carry Fano tuples."""
import random, sys
from fractions import Fraction as F
from itertools import product
from w9_ref_typeclosed2_lib import *

# 1. note 7.79
X = [F(513, 8) / 80] * 3
T79 = [(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
T79 = [tuple(F(v, 80) for v in c) for c in T79]
ts, arg = tau_star(T79, X)
assert ts == F(483, 640), ts
fs = fano_search(T79, X)
assert fs is not None
S, sig, e = super_classes(T79, X)
print('7.79: tau*', ts, 'e', e, 'sum e', sum(e), 'pair sums', [e[0]+e[1], e[0]+e[2], e[1]+e[2]])
print('7.79 Fano rows (classes):', [[i for i in range(3) if r in S[i]] for r in fs])

# 2. 2-colourings of lines
PEN = [[l for l in range(7) if q in LINES[l]] for q in range(7)]
for col in product([0, 1], repeat=7):
    assert any(len(set(col[l] for l in pen)) == 1 for pen in PEN)
print('2-colourings of Fano lines: all 128 have a monochromatic pencil')
# 3-colourings without monochromatic pencil exist (so 3 classes can host Fano tuples)
n3 = sum(1 for col in product([0,1,2], repeat=7) if not any(len(set(col[l] for l in pen)) == 1 for pen in PEN))
print('3-colourings without monochromatic pencil:', n3)

# 3. random residual-regime families
def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
stat = dict(fam=0, tau_gt=0, fano=0, Qfail=0)
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 400):
    den = rng.choice([7, 12, 20, 30])
    x = [rnd(rng, F(1, 20), F(1), 20), rnd(rng, F(3, 4), F(3, 2), 30), rnd(rng, F(3, 4), F(3, 2), 30)]
    C = []
    for _ in range(rng.randint(2, 6)):
        for _t in range(200):
            h = rng.choice([1, 2]); o = 3 - h
            c0 = rnd(rng, 0, F(4, 7) * x[0], den)
            lo = 2 * x[h] / 3
            top = min(x[h], 1 - c0)
            if top <= lo: continue
            ch = lo + (top - lo) * F(rng.randint(1, den), den)
            co = 1 - c0 - ch
            if co < 0 or co > x[o] or 3 * co > 2 * x[o]: continue
            c = [c0, 0, 0]; c[h] = ch; c[o] = co
            C.append(tuple(c)); break
    if not C: continue
    stat['fam'] += 1
    assert fano_search(C, x) is None, (x, C)
    t, _ = tau_star(C, x)
    A = [c for c in C if 3 * c[2] > 2 * x[2]]; B = [c for c in C if 3 * c[1] > 2 * x[1]]
    if t > F(3, 4) and A and B:
        stat['tau_gt'] += 1
        thk = min(c[2] for c in A); thj = min(c[1] for c in B)
        assert (x[1] - thj) + (x[2] - thk) >= t
        assert x[1] + x[2] > F(9, 4)
        b = min(B, key=lambda c: c[1]); a = min(A, key=lambda c: c[2])
        assert x[1] < F(3, 2) * b[1] and x[2] < F(3, 2) * a[2]   # R1, R2 => Q_b, Q_a fail
        stat['Qfail'] += 1
print('(a) random residual families:', stat)

# 4. literal caveat: explicit example
x = [F(1, 2), F(13, 10), F(13, 10)]
a = (F(0), F(1, 10), F(9, 10)); b = (F(0), F(9, 10), F(1, 10)); l = (F(1, 5), F(2, 5), F(2, 5))
C = [a, b, l]
assert 3 * a[2] > 2 * x[2] and 3 * b[1] > 2 * x[1]
assert (x[1] - b[1]) + (x[2] - a[2]) > F(3, 4)
assert x[1] < F(3, 2) * b[1] and x[2] < F(3, 2) * a[2]
assert hom_fano(l, x) and fano_search(C, x) is not None
print('(4) caveat example: minimiser pair fails Q_b,Q_a (R1,R2) and G holds, but type', l,
      'is light everywhere -> homogeneous Fano tuple exists; tau* =', tau_star(C, x)[0])

# 5. sharpness: heavy-not-super classes can carry a Fano tuple even with 2 classes
found = 0
for trial in range(3000):
    x = [rnd(rng, F(1, 20), F(1), 20), rnd(rng, F(3, 4), F(3, 2), 20), rnd(rng, F(3, 4), F(3, 2), 20)]
    C = []
    for h in (1, 2):
        o = 3 - h
        ch = rnd(rng, F(4, 7) * x[h], F(2, 3) * x[h], 20)
        c0 = rnd(rng, 0, F(4, 7) * x[0], 20); co = 1 - ch - c0
        if co < 0 or co > x[o]: break
        c = [c0, 0, 0]; c[h] = ch; c[o] = co; C.append(tuple(c))
    if len(C) < 2 or any(hom_fano(c, x) for c in C): continue
    if fano_search(C, x):
        found += 1
        if found == 1: print('(5) example heavy-not-super 2-class Fano tuple: x', x, 'C', C)
print('(5) heavy-not-super 2-class families with a Fano tuple:', found)
