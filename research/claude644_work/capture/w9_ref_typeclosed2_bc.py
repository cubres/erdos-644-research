"""[typeclosed#2] parts (b), (c).
(c1) unconditional inequality tau*(C) <= tau*(C^(i)) + e_i (every closed C, every part i with S_i != empty), exact,
     random families over p = 3, 4 parts incl. boundary types (c_i = 2x_i/3 exactly) and types super-heavy in 2 parts.
(c2) families with no pencil type (every type super-heavy somewhere): tau* <= sum_{i: S_i nonempty} e_i, hence
     N >= 3 sum e >= 3 tau*; and x_i <= 3/2 on parts with S_i nonempty.
(b1) dependency check (p=3): whenever tau*(C^(i)) > 3/4, run Theorem L+'s algorithm literally on C^(i) (parts j,k =
     the other two) and verify the produced bad tuple exactly (pencil+requests via Lemma 7.63, or V).
(b2) p=4: the L+ hypothesis fails for C^(i): exhibit note 7.79 (+ unused 4th part) with C^(3) = C, tau* = 483/640,
     three parts hosting super-heavy types."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *

def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

def rtype(rng, x, den):
    p = len(x)
    for _ in range(500):
        mode = rng.random()
        c = [F(0)] * p
        order = list(range(p)); rng.shuffle(order)
        rem = F(1)
        for m, i in enumerate(order):
            if m == p - 1:
                v = rem
            else:
                r = rng.random()
                if r < 0.15:
                    v = min(rem, 2 * x[i] / 3)          # boundary type
                elif r < 0.5:
                    v = min(rem, rnd(rng, 2 * x[i] / 3, x[i], den))
                else:
                    v = min(rem, rnd(rng, 0, x[i], den))
            c[i] = v; rem -= v
        if rem == 0 and all(0 <= c[i] <= x[i] for i in range(p)):
            return tuple(c)
    return None

def Lplus(Csub, x, j, k, T):
    """Theorem L+ algorithm on Csub (3 parts; every type c_i <= 2x_i/3 at the third part i). Returns (kind, rows)."""
    p = len(x)
    for e in Csub:
        if pencil_type(e, x):
            r = tuple(x[i] - F(3, 4) * e[i] for i in range(p))
            fs = [c for c in Csub if all(c[i] <= r[i] for i in range(p))]
            assert sum(x[i] - r[i] for i in range(p)) <= F(3, 4) * sum(e) and fs, 'request fails'
            f = fs[0]
            # pencil through point 0 = lines 0,1,2 get e; lines 3..6 get f
            rows = [e, e, e, f, f, f, f]
            assert fano_ok(rows, x), 'pencil tuple infeasible'
            return 'pencil', rows
    A = [c for c in Csub if 3 * c[k] > 2 * x[k]]; B = [c for c in Csub if 3 * c[j] > 2 * x[j]]
    assert all(c in A or c in B for c in Csub) and A and B
    sk = min(c[k] for c in A); sj = min(c[j] for c in B)
    assert (x[j] - sj) + (x[k] - sk) >= T > F(3, 4)
    a = min(A, key=lambda c: c[k])
    cost = sum(a[i] for i in range(p) if i != k) + x[k] - sk
    assert cost < F(3, 4), cost
    cs = [c for c in Csub if all(c[i] <= x[i] - a[i] for i in range(p) if i != k) and c[k] < sk]
    assert cs and all(c in B for c in cs)
    assert V_ok(a, cs[0], x)
    return 'V', (a, cs[0])

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
rng = random.Random(seed)
st = dict(fam=0, c1_checks=0, c1_tight=0, nopencil=0, c2=0, b1=0, b1_kinds={})
for trial in range(N):
    p = rng.choice([3, 3, 4])
    den = rng.choice([6, 12, 20])
    x = [rnd(rng, F(1, 10), F(3, 2), 30) for _ in range(p)]
    if sum(x) < 1: continue
    C = []
    nopen = rng.random() < 0.5
    for _ in range(rng.randint(2, 7 if p == 3 else 5)):
        c = rtype(rng, x, den)
        if c is None: continue
        if nopen and pencil_type(c, x): continue
        C.append(c)
    if not C: continue
    st['fam'] += 1
    t, _ = tau_star(C, x)
    S, sig, e = super_classes(C, x)
    for i in range(p):
        if S[i]:
            ti, _ = tau_star(restrict(C, x, [i]), x)
            assert t <= ti + e[i], (x, C, i, t, ti, e[i])
            st['c1_checks'] += 1
            if t == ti + e[i]: st['c1_tight'] += 1
    if not any(pencil_type(c, x) for c in C):
        st['nopencil'] += 1
        se = sum(v for v in e if v is not None)
        assert t <= se
        assert sum(x) >= 3 * se
        assert all(x[i] <= F(3, 2) for i in range(p) if S[i])
        st['c2'] += 1
    if p == 3:
        for i in range(3):
            Ci = restrict(C, x, [i])
            if not Ci: continue
            ti, _ = tau_star(Ci, x)
            if ti > F(3, 4):
                j, k = [m for m in range(3) if m != i]
                kind, _ = Lplus(Ci, x, j, k, ti)
                st['b1'] += 1; st['b1_kinds'][kind] = st['b1_kinds'].get(kind, 0) + 1
print('seed', seed, st)

# (b2)
X = [F(513, 8) / 80] * 3 + [F(1)]
T79 = [(0,54,26,0),(1,62,17,0),(8,43,29,0),(19,0,61,0),(28,1,51,0),(31,4,45,0),(44,32,4,0),(51,29,0,0),(58,21,1,0)]
T79 = [tuple(F(v, 80) for v in c) for c in T79]
C3 = restrict(T79, X, [3])
assert C3 == T79
t3, _ = tau_star(C3, X)
S, sig, e = super_classes(C3, X)
print('(b2) p=4: C^(3)=C, tau*(C^(3)) =', t3, '> 3/4; parts hosting super-heavy types:', [i for i in range(4) if S[i]],
      '-> L+ hypothesis (all but two parts 2/3-light) FAILS for C^(3)')
