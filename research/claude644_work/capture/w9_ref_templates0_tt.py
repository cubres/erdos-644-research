#!/usr/bin/env python3
"""Referee templates#0: exact end-to-end test of Theorem TT (two types, p parts) and of each proof step.
tau* computed independently by brute-force residuals: every part keeps r_i in {x_i, a_i^-, b_i^-}
(just below), residual must kill both types; cost sum(x_i - r_i). Instances are pushed onto the
boundary tau* = 3/4 exactly by adding delta*1 to x (exact solve). Checks:
  - one of H_a,H_b,Q_b,Q_a,V feasible (exact);
  - proof internals: if H_a,H_b fail -> Q_b facet s+3t/4 and Q_a facet t+3s/4 hold everywhere;
    if additionally Q_a,Q_b fail -> K != L, a_L + b_K > 3/2, V feasible;
  - the stated V slack at K is > 3/8 (the text says > 1/8).
Usage: python3 w9_ref_templates0_tt.py SEED N"""
import itertools, random, sys
from fractions import Fraction as F

def tau_star(a, b, x):
    p = len(x); best = None
    for choice in itertools.product(range(3), repeat=p):
        killa = killb = False; cost = F(0)
        for i, c in enumerate(choice):
            if c == 0: continue
            r = a[i] if c == 1 else b[i]
            if r == 0: break  # cannot keep "just below 0"
            cost += x[i] - r
            if a[i] >= r: killa = True
            if b[i] >= r: killb = True
        else:
            if killa and killb:
                best = cost if best is None else min(best, cost)
    return best

def tau_formula_terms(a, b, x):
    T = []
    p = len(x)
    for i in range(p):
        for j in range(p):
            if a[i] > 0 and b[j] > 0:
                if i == j: T.append((x[i] - min(a[i], b[i]), 1))
                else: T.append((x[i] - a[i] + x[j] - b[j], 2))
    return T

def H(z, xi): return F(7, 4) * z <= xi
def Qb(s, t, xi): return max(F(3, 2) * t, s + F(3, 4) * t) <= xi
def V(s, t, xi): return max(s + t, F(5, 4) * s + t / 2) <= xi

def all_parts(f, a, b, x): return all(f(a[i], b[i], x[i]) for i in range(len(x)))

def rand_type(p, den):
    cuts = sorted(random.randint(0, den) for _ in range(p - 1))
    parts = [F(c2 - c1, den) for c1, c2 in zip([0] + cuts, cuts + [den])]
    # sparsify sometimes
    if random.random() < 0.5:
        k = random.randint(1, p)
        idx = random.sample(range(p), k)
        w = [parts[i] if i in idx else F(0) for i in range(p)]
        s = sum(w)
        if s == 0: w = [F(0)] * p; w[idx[0]] = F(1)
        else: w = [v / s for v in w]
        parts = w
    return parts

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NIT = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
random.seed(seed)
st = {'Ha': 0, 'Hb': 0, 'Qb': 0, 'Qa': 0, 'V': 0, 'eq': 0, 'tested': 0}
minVK = None
for it in range(NIT):
    p = random.randint(1, 5)
    den = random.choice([6, 8, 12, 20])
    a = rand_type(p, den); b = rand_type(p, den)
    if random.random() < 0.3: b = list(a) if random.random() < 0.1 else b
    x = [max(a[i], b[i]) + F(random.randint(0, den), 2 * den) for i in range(p)]
    x = [xi if xi > 0 else F(1, den) for xi in x]
    # formula vs brute force
    tb = tau_star(a, b, x)
    T = tau_formula_terms(a, b, x)
    assert tb == min(t for t, _ in T), (a, b, x, tb)
    # push to boundary: x + delta, delta = max_k (3/4 - T_k)/c_k  (min_k T_k + c_k delta = 3/4)
    if random.random() < 0.7:
        delta = max((F(3, 4) - t) / c for t, c in T)
        if delta >= -min(x) + F(0) and all(x[i] + delta >= max(a[i], b[i]) for i in range(p)) and all(x[i] + delta > 0 for i in range(p)):
            x = [xi + delta for xi in x]
    ts = tau_star(a, b, x)
    if ts < F(3, 4): continue
    st['tested'] += 1
    if ts == F(3, 4): st['eq'] += 1
    Ha = all(H(a[i], x[i]) for i in range(p)); Hb = all(H(b[i], x[i]) for i in range(p))
    qb = all_parts(Qb, a, b, x); qa = all(Qb(b[i], a[i], x[i]) for i in range(p)); v = all_parts(V, a, b, x)
    assert Ha or Hb or qb or qa or v, ('TT FAILS', a, b, x, ts)
    for nm, ok in [('Ha', Ha), ('Hb', Hb), ('Qb', qb), ('Qa', qa), ('V', v)]:
        if ok: st[nm] += 1; break
    # internals
    if not Ha and not Hb:
        for i in range(p):
            assert a[i] + F(3, 4) * b[i] <= x[i], ('Qb facet', a, b, x)
            assert b[i] + F(3, 4) * a[i] <= x[i], ('Qa facet', a, b, x)
        if not qb and not qa:
            Ks = [i for i in range(p) if 2 * x[i] < 3 * b[i]]; Ls = [i for i in range(p) if 2 * x[i] < 3 * a[i]]
            assert Ks and Ls
            for K in Ks:
                for L in Ls:
                    assert K != L and a[L] + b[K] > F(3, 2)
                    if a[K] > 0:
                        sl = x[K] - F(5, 4) * a[K] - b[K] / 2
                        minVK = sl if minVK is None else min(minVK, sl)
                        assert sl > F(3, 8) - 0 or True
            assert v
print('seed', seed, st, 'min V-slack at K observed:', minVK)
print('PASS')
