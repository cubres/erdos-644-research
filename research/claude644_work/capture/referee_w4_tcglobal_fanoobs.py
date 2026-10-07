#!/usr/bin/env python3
"""referee_w4_tcglobal_fanoobs.py -- independent referee checks for the tcglobal OBSTRUCTION
'Fano-labelled tools cannot remove the intersecting hypothesis'. Exact integer arithmetic only.
(1) own Fano plane (F_2^3 nonzero vectors); necessary conditions for a Fano-labelled tuple in a type-closed
    family (per part: row load <= cap, concurrent-triple load <= 2cap, total <= 4cap) -- these are NECESSARY for
    actual edges, which is the direction an obstruction needs.
(2) example caps (32,26), types (22,1),(5,18): Fano-free; exact actual tau; scaled check.
(3) Prop 7.55 and the sharper two-part family with parts of size (3r-1)/2 (tau = r+1 = k+1): Fano-free.
(4) brute force on an ACTUAL family: K_4^(3) disjoint-union K_4^(3) (k=3, tau=4): no Fano-labelled 7-tuple
    among all 8^7 ordered tuples (every vertex's line-set must be safe).
(5) note Lemma 7.9 family: count of assignments satisfying the exact Lemma 7.63 conditions."""
import itertools
pts = [v for v in range(1, 8)]                      # nonzero vectors of F_2^3
lines = sorted({tuple(sorted((a, b, a ^ b))) for a in pts for b in pts if a < b})
assert len(lines) == 7
# rows = lines. concurrent triples of rows = the 3 lines through a point.
conc = [[j for j, l in enumerate(lines) if p in l] for p in pts]
def safe(S):   # set of line indices; safe iff union of lines != all points
    return len(set().union(*[set(lines[j]) for j in S])) < 7 if S else True
def nec_ok(types, caps, assign):
    for i, c in enumerate(caps):
        z = [types[assign[j]][i] for j in range(7)]
        if max(z) > c or sum(z) > 4 * c: return False
        if any(sum(z[j] for j in T) > 2 * c for T in conc): return False
    return True
def fano_candidates(types, caps):
    return [a for a in itertools.product(range(len(types)), repeat=7) if nec_ok(types, caps, a)]
def tau_pattern(types, caps):
    # actual tau of the type-closed family {S : |S cap P_i| = a_i for all i} over all types a
    n = sum(caps); best = 0
    for u in itertools.product(*[range(c + 1) for c in caps]):
        if all(any(u[i] < a[i] for i in range(len(caps))) for a in types):
            best = max(best, sum(u))
    return n - best
# (2)
T, C = [(22, 1), (5, 18)], (32, 26)
print("(2) example: candidates", len(fano_candidates(T, C)), " actual tau", tau_pattern(T, C), " k", 23)
for m in (2, 3):
    Tm = [tuple(m * x for x in a) for a in T]; Cm = tuple(m * x for x in C)
    print("    scale", m, "candidates", len(fano_candidates(Tm, Cm)), "tau", tau_pattern(Tm, Cm), "k", 23 * m)
# (3)
for m in (1, 2, 3):
    r = 5 * m; T3 = [(r, 0), (0, r)]; C3 = (7 * m, 7 * m)
    print("(3) Prop7.55 r=%d candidates %d tau %d" % (r, len(fano_candidates(T3, C3)), tau_pattern(T3, C3)))
for r in (3, 5, 7, 9, 11):
    n = (3 * r - 1) // 2; T3 = [(r, 0), (0, r)]; C3 = (n, n)
    print("(3') sharper r=%d parts %d candidates %d tau %d (k=%d)" % (r, n, len(fano_candidates(T3, C3)), tau_pattern(T3, C3), r))
# (4) brute force actual family K_4^3 + K_4^3
E = [frozenset(s) for s in itertools.combinations(range(4), 3)] + [frozenset(s) for s in itertools.combinations(range(4, 8), 3)]
safeset = {S for r in range(8) for S in itertools.combinations(range(7), r) if safe(S)}
found = 0
for tup in itertools.product(range(len(E)), repeat=7):
    ok = True
    for v in range(8):
        S = tuple(j for j in range(7) if v in E[tup[j]])
        if S not in safeset: ok = False; break
    if ok: found += 1; break
def tau_actual(E, V):
    for s in range(len(V) + 1):
        for T0 in itertools.combinations(V, s):
            if all(set(T0) & e for e in E): return s
print("(4) K4^3+K4^3: Fano-labelled tuple found:", bool(found), " tau", tau_actual(E, range(8)), " k 3")
# (5)
T5, C5 = [(20, 0, 80), (0, 80, 20)], (40, 139, 99)
c5 = fano_candidates(T5, C5)
print("(5) Lemma 7.9 family: exact Lemma-7.63 feasible assignments:", len(c5))
