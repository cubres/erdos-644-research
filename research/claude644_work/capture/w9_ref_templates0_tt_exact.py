#!/usr/bin/env python3
"""Referee w9 [templates#0]: EXACT statement-level test of Theorem TT.
For fixed rational types a,b (sum 1) over p parts, the capacities x range over ALL of R^p (not sampled):
a counterexample x exists iff for some assignment T -> failing part i_T of the five templates
  H_a (7s/4), H_b (7t/4), Q_b=max(3t/2,s+3t/4), Q_a=max(3s/2,t+3s/4), V=max(s+t,5s/4+t/2)
the upper bounds x_i < U_i := min_{T: i_T=i} T(a_i,b_i) are compatible with admissibility x_i>=max(a_i,b_i)
and with (K1),(K2) (tau*>=3/4, non-strict).  All lower-bound constraints are monotone increasing in x, so
compatibility is decided exactly at the supremum point x=U (capped coordinates) / +inf (uncapped):
  admissibility: max(a_i,b_i) < U_i;  each K-constraint: value at sup > 3/4 if it involves a capped
  coordinate, automatically true otherwise.
Also: tau* computed by brute force over single/pair blocking residuals to double-check the K1/K2 formula
(independently: residual r kills type a iff r_i<a_i for some i; cost = sum(x-r)).
Modes: grid p den  (all pairs of compositions)   |   rand p den n seed.
"""
import itertools, random, sys
from fractions import Fraction as F
INF = None
def T_vals(s, t):
    return [F(7, 4) * s, F(7, 4) * t, max(F(3, 2) * t, s + F(3, 4) * t), max(F(3, 2) * s, t + F(3, 4) * s),
            max(s + t, F(5, 4) * s + t / 2)]
NAMES = ['Ha', 'Hb', 'Qb', 'Qa', 'V']
def counterexample(a, b):
    p = len(a)
    mv = [T_vals(a[i], b[i]) for i in range(p)]
    for assign in itertools.product(range(p), repeat=5):
        U = [INF] * p
        for T, i in enumerate(assign):
            v = mv[i][T]
            U[i] = v if U[i] is INF else min(U[i], v)
        ok = True
        for i in range(p):
            if U[i] is not INF and not (max(a[i], b[i]) < U[i]):
                ok = False; break
        if not ok:
            continue
        # K1
        for i in range(p):
            if a[i] > 0 and b[i] > 0 and U[i] is not INF:
                if not (U[i] - min(a[i], b[i]) > F(3, 4)):
                    ok = False; break
        if not ok:
            continue
        for i in range(p):
            if a[i] == 0: continue
            for j in range(p):
                if j == i or b[j] == 0: continue
                if U[i] is INF or U[j] is INF:
                    # if one is uncapped the constraint can be met (x -> large) -- only if the capped one is
                    # admissible, already ensured; strictly: LHS unbounded -> fine
                    continue
                if not ((U[i] - a[i]) + (U[j] - b[j]) > F(3, 4)):
                    ok = False; break
            if not ok: break
        if ok:
            return assign, U
    return None
def tau_star_formula(a, b, x):
    p = len(a); best = None
    for i in range(p):
        for j in range(p):
            if a[i] > 0 and b[j] > 0:
                v = x[i] - min(a[i], b[i]) if i == j else (x[i] - a[i]) + (x[j] - b[j])
                best = v if best is None else min(best, v)
    return best
def tau_star_brute(a, b, x):
    # residual r: choose for each type a killing coordinate; minimal cost residual sets r_i = min over the
    # required cut levels (just below). brute force over all (i,j) choices == formula; instead enumerate
    # residual vectors with r_i in {x_i, a_i, b_i, min(a_i,b_i)} (the only relevant cut levels, infimum)
    p = len(a); best = None
    levels = [sorted(set([x[i], a[i], b[i]])) for i in range(p)]
    for r in itertools.product(*levels):
        # "just below" r_i when r_i<x_i: type kills if a_i >= r_i (limit) and r_i<x_i ... use closed version
        killa = any(a[i] >= r[i] and a[i] > 0 for i in range(p))
        killb = any(b[i] >= r[i] and b[i] > 0 for i in range(p))
        if killa and killb:
            c = sum(x[i] - r[i] for i in range(p))
            best = c if best is None else min(best, c)
    return best
def comps(n, p):
    for c in itertools.combinations(range(n + p - 1), p - 1):
        prev = -1; out = []
        for k in c + (n + p - 1,):
            out.append(k - prev - 1); prev = k
        yield out
def main():
    mode = sys.argv[1]
    p = int(sys.argv[2]); den = int(sys.argv[3])
    if mode == 'grid':
        C = [[F(v, den) for v in c] for c in comps(den, p)]
        pairs = itertools.product(C, C)
    else:
        n = int(sys.argv[4]); rng = random.Random(int(sys.argv[5]))
        def rc():
            # random sparse composition
            w = [rng.choice([0, 0, rng.randint(1, den)]) for _ in range(p)]
            if sum(w) == 0: w[rng.randrange(p)] = 1
            s = sum(w); return [F(v, s) for v in w]
        pairs = ((rc(), rc()) for _ in range(n))
    cnt = 0; bad = 0
    for a, b in pairs:
        cnt += 1
        r = counterexample(a, b)
        if r is not None:
            bad += 1
            print("COUNTEREXAMPLE a=", a, "b=", b, "assign", r[0], "U", r[1]); sys.stdout.flush()
            if bad > 5: break
    print(f"mode={mode} p={p} den={den}: pairs={cnt} counterexamples={bad}")
    # tau* formula cross-check on random x
    rng = random.Random(7); mism = 0
    for _ in range(300):
        a = [F(rng.randint(0, 4)) for _ in range(p)]; b = [F(rng.randint(0, 4)) for _ in range(p)]
        if sum(a) == 0 or sum(b) == 0: continue
        a = [v / sum(a) for v in a]; b = [v / sum(b) for v in b]
        x = [max(a[i], b[i]) + F(rng.randint(0, 8), 8) for i in range(p)]
        if tau_star_formula(a, b, x) != tau_star_brute(a, b, x):
            mism += 1; print("tau mismatch", a, b, x, tau_star_formula(a, b, x), tau_star_brute(a, b, x))
    print("tau* formula vs brute residual enumeration mismatches:", mism)
main()
