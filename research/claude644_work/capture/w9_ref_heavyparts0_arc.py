"""Referee (heavyparts#0) independent check of the arc-CSP classification.
Independent Fano model: points = nonzero vectors of F_2^3 (ints 1..7), lines = {u,v,u^v}.
Rows are placed on LINES (dual form of note Lemma 7.63): per part i, pencil (3 lines through a point) sum <= 2x_i,
total <= 4x_i, row <= x_i.
Part 1: enumerate 3-colourings of lines, keep those with no monochromatic concurrent triple (arc classes),
        compute the pattern sets, the full hitting-set family over subsets of the 7 mixed patterns, and its minimal
        members, by a different algorithm (all 2^7 subsets, minimality by explicit subset test)."""
import itertools
from fractions import Fraction as Fr
PTS = list(range(1, 8))
LINES = sorted({tuple(sorted((u, v, u ^ v))) for u in PTS for v in PTS if u < v})
assert len(LINES) == 7
PENC = {p: [k for k, L in enumerate(LINES) if p in L] for p in PTS}
# arc = no 3 concurrent lines of one colour; test via ALL 3-subsets of lines with a common point
CONC3 = [c for c in itertools.combinations(range(7), 3) if set(LINES[c[0]]) & set(LINES[c[1]]) & set(LINES[c[2]])]
assert len(CONC3) == 7 and all(sorted(PENC[p]) in [list(c) for c in CONC3] for p in PTS)
MIXED = ['AAB', 'AAC', 'BBA', 'BBC', 'CCA', 'CCB', 'ABC']
def canon(ms):
    ms = sorted(ms)
    for q in MIXED:
        if sorted(q) == ms: return q
    return None
arcs = []
for col in itertools.product('ABC', repeat=7):
    if any(col[a] == col[b] == col[c] for a, b, c in CONC3): continue
    arcs.append((col, frozenset(canon([col[k] for k in PENC[p]]) for p in PTS)))
print("arc colourings:", len(arcs), "distinct pattern sets:", len({s for _, s in arcs}))
from collections import Counter
print("colour-class size profiles:", Counter(tuple(sorted(Counter(c).values())) for c, _ in arcs))
psets = {s for _, s in arcs}
hit = []
for mask in range(1 << 7):
    F = frozenset(MIXED[i] for i in range(7) if mask >> i & 1)
    if all(F & s for s in psets): hit.append(F)
minimal = [F for F in hit if not any(G < F for G in hit)]
print("minimal hitting sets:", sorted(sorted(F) for F in minimal))
expect = [{'AAB','BBA'}, {'AAC','CCA'}, {'BBC','CCB'}, {'AAB','BBC','CCA'}, {'AAC','BBA','CCB'}]
assert sorted(map(sorted, minimal)) == sorted(map(sorted, expect)), "MISMATCH with claim"
print("Part 1: classification CONFIRMED (independent model and algorithm)")
# upward-closure check: every hitting set contains a minimal one (trivial) and every superset of a minimal is hitting
for F in minimal:
    for extra in range(1 << 7):
        G = F | frozenset(MIXED[i] for i in range(7) if extra >> i & 1)
        assert all(G & s for s in psets)
print("upward closed: OK;  #hitting sets =", len(hit))

# ---------- Part 2: exact end-to-end on random 3-type families (all 3^7 line->type maps) ----------
def pencil_ok(x, rows):
    p = len(x)
    for i in range(p):
        for q in PTS:
            if sum(rows[k][i] for k in PENC[q]) > 2 * x[i]: return False
    return True
def full_ok(x, rows):
    p = len(x)
    for i in range(p):
        if any(r[i] > x[i] for r in rows): return False
        if sum(r[i] for r in rows) > 4 * x[i]: return False
    return pencil_ok(x, rows)
def forbidden(x, T, pat):
    idx = {'A': 0, 'B': 1, 'C': 2}
    rows = [T[idx[c]] for c in pat]
    return any(sum(r[i] for r in rows) > 2 * x[i] for i in range(len(x)))
def conflict(x, T):
    F = {q for q in MIXED if forbidden(x, T, q)}
    return any(set(e) <= F for e in expect), F
ALLMAPS = list(itertools.product(range(3), repeat=7))

import random, sys
def rand_type(rng, x, own, N, p):
    """integer type (sum N) super-heavy at part own: 3a_own > 2x_own, a <= x."""
    lo = (2 * x[own]) // 3 + 1; hi = min(x[own], N)
    if lo > hi: return None
    a = [0] * p; a[own] = rng.randint(lo, hi)
    rest = N - a[own]
    others = [i for i in range(p) if i != own]
    for _ in range(50):
        cuts = sorted(rng.randint(0, rest) for _ in range(len(others) - 1))
        parts = [b - c for b, c in zip(cuts + [rest], [0] + cuts)]
        if all(parts[k] <= x[others[k]] for k in range(len(others))):
            for k, i in enumerate(others): a[i] = parts[k]
            return a
    return None
def pencil_any(x, T, maps):
    for m in maps:
        if pencil_ok(x, [T[j] for j in m]): return m
    return None
def full_any(x, T, maps):
    for m in maps:
        if full_ok(x, [T[j] for j in m]): return m
    return None

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    N = 60
    stats = Counter(); tot_examples = []
    for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
        x = [rng.randint(N // 3, 2 * N) for _ in range(3)]
        T = [rand_type(rng, x, own, N, 3) for own in range(3)]
        if None in T: continue
        c, F = conflict(x, T)
        pm = pencil_any(x, T, ALLMAPS)
        fm = full_any(x, T, ALLMAPS) if pm is not None else None
        stats[(c, pm is not None, fm is not None)] += 1
        if c and pm is not None: print("VIOLATION conflict but pencil-feasible", x, T, pm); sys.exit(1)
        if (not c) and pm is None: print("VIOLATION no conflict but pencil-infeasible", x, T, sorted(F)); sys.exit(1)
        if pm is not None and fm is None and len(tot_examples) < 3: tot_examples.append((x, T, sorted(F)))
    print("Part 2 stats (conflict, pencilFeasible, fullFeasible):", dict(stats))
    print("examples where totals kill every pencil-feasible map:", tot_examples)
