#!/usr/bin/env python3
"""
arch0_rounding.py  (wave-11 referee of architecture#0 / Lemma G2; exact Fractions, stdlib only)

Part A.  The proof text of G2 says "window >= ceil(v_j) - 14".  Explicit instance where this intermediate inequality is
         FALSE (loss < 15 only gives window >= floor(v_j) - 14); the final inequality window >= u_j - 14 (u_j integer
         <= v_j) survives.
Part B.  Random exact test of the flooring step on random antichains of cells drawn from the downsets of random Astra
         catalogue orbits (arbitrary supports): after reassignment to maximal used cells and flooring, every window
         is >= floor(load) - 14, and the observed worst loss is recorded.
Part C.  IMPROVEMENT: Beck-Fiala-type iterative rounding.  Each cell C != [7] lies in |C| <= 6 rows.  Keep the total
         mass constraint always active and a row constraint active while it has >= 7 fractional cells; move along a
         null-space direction until a variable becomes an integer.  #active < #fractional always holds (proof in
         notes_referee_w11.md), so the process terminates with integer masses, the SAME total, cells only from the
         original support (no reassignment needed), and every row load > original load - 6, i.e. >= floor(v_j) - 5:
         UNIVERSAL shift s = 5.  Exact random test over catalogue supports.
"""
import json, random, sys
from fractions import Fraction as Fr
from itertools import combinations
from math import floor, ceil

CAT = "/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json"
FULL = 127

def downset(maximal):
    cells = set()
    for m in maximal:
        sub = m
        while True:
            cells.add(sub)
            if sub == 0:
                break
            sub = (sub - 1) & m
    return cells

def maximal_of(cells):
    return [c for c in cells if not any(d != c and (d & c) == c for d in cells)]

def loads(mass):
    return [sum(m for c, m in mass.items() if c >> j & 1) for j in range(7)]

# ---------------------------------------------------------------- Part A
def part_a():
    # support: all 3-subsets of [7] (a valid bad support: two 3-sets never cover [7]); 15 cells per window
    cells = [c for c in range(1, FULL) if bin(c).count("1") == 3]
    assert all((a | b) != FULL for a in cells for b in cells)
    v = Fr(29, 2)                                   # each window load 14.5
    mass = {c: v / 15 for c in cells}               # 35 cells, each 29/30
    ld = loads(mass)
    assert all(x == v for x in ld)
    fl = {c: floor(m) for c, m in mass.items()}
    win = loads(fl)
    print(f"[A] all-3-sets support, every cell mass 29/30, every window load v = 29/2: after flooring every window = "
          f"{win[0]}; ceil(v)-14 = {ceil(v)-14} (claimed bound VIOLATED), floor(v)-14 = {floor(v)-14} (holds); "
          f"with u = floor(v) = 14 the transfer's requirement window >= u - 14 = 0 holds.")

# ---------------------------------------------------------------- Part B
def part_b(rnd, orbits, trials=4000):
    worst = 0
    for _ in range(trials):
        o = rnd.choice(orbits)
        ds = [c for c in downset(o["maximal_cells"]) if c != 0]
        used = rnd.sample(ds, rnd.randint(1, len(ds)))
        # arbitrary rational masses
        mass = {c: Fr(rnd.randint(0, 3000), rnd.choice([7, 11, 13, 100, 1000])) for c in used}
        n = ceil(sum(mass.values())) + rnd.randint(0, 3)
        v = loads(mass)
        # reassignment to maximal used cells
        mx = maximal_of(used)
        mass2 = {c: Fr(0) for c in mx}
        for c, m in mass.items():
            parent = next(d for d in mx if (d & c) == c)
            mass2[parent] += m
        assert all((a | b) != FULL for a in mx for b in mx)
        v2 = loads(mass2)
        assert all(v2[j] >= v[j] for j in range(7))
        assert sum(mass2.values()) == sum(mass.values()) <= n
        fl = {c: floor(m) for c, m in mass2.items()}
        win = loads(fl)
        for j in range(7):
            k = sum(1 for c in mx if c >> j & 1)
            assert k <= 15, k
            assert win[j] >= floor(v2[j]) - 14 and win[j] >= floor(v[j]) - 14
            worst = max(worst, floor(v[j]) - win[j])
    print(f"[B] {trials} random supports/antichains/masses: reassignment + flooring always gives window >= floor(v)-14; "
          f"worst observed floor(v) - window = {worst}")

# ---------------------------------------------------------------- Part C: iterative rounding
def nullspace_vector(rows, ncols):
    """rows: list of lists of Fractions (constraints over the fractional variables). Return a nonzero rational z with
    rows . z = 0, or None if the rows have full column rank."""
    M = [r[:] for r in rows]
    pivcols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivcols.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in pivcols]
    if not free:
        return None
    f0 = free[0]
    z = [Fr(0)] * ncols
    z[f0] = Fr(1)
    for i, pc in enumerate(pivcols):
        z[pc] = -M[i][f0]
    return z

def iterative_round(mass, n, threshold=7):
    """mass: dict cell -> Fraction >= 0 (cells distinct, != FULL), sum <= n (integer).  Returns integer dict with the
    same cells (some may become 0), total exactly n (the empty cell 0 absorbs the slack), every row load
    > original - (threshold - 1)."""
    x = dict(mass)
    x[0] = n - sum(mass.values())           # empty cell carries the slack; total is now exactly n
    assert x[0] >= 0
    steps = 0
    while True:
        F = [c for c in x if x[c].denominator != 1]
        if not F:
            break
        assert len(F) >= 2, "a single fractional variable is impossible (total is an integer)"
        active = [FULL + 1]                                   # the total constraint, always active
        for j in range(7):
            if sum(1 for c in F if c >> j & 1) >= threshold:
                active.append(j)
        assert len(active) < len(F), ("#active >= #fractional", len(active), len(F))
        rows = []
        for a in active:
            if a == FULL + 1:
                rows.append([Fr(1)] * len(F))
            else:
                rows.append([Fr(1) if c >> a & 1 else Fr(0) for c in F])
        z = nullspace_vector(rows, len(F))
        assert z is not None
        # step to the first integer hit
        t = None
        for c, zc in zip(F, z):
            if zc > 0:
                cand = (ceil(x[c]) - x[c]) / zc
            elif zc < 0:
                cand = (x[c] - floor(x[c])) / (-zc)
            else:
                continue
            if t is None or cand < t:
                t = cand
        assert t is not None and t > 0
        for c, zc in zip(F, z):
            x[c] += t * zc
            assert x[c] >= 0
        steps += 1
    return x, steps

def part_c(rnd, orbits, trials=1500):
    worst = 0
    max_steps = 0
    for _ in range(trials):
        o = rnd.choice(orbits)
        ds = [c for c in downset(o["maximal_cells"]) if c != 0]
        used = rnd.sample(ds, rnd.randint(1, len(ds)))
        mass = {c: Fr(rnd.randint(0, 3000), rnd.choice([7, 11, 13, 100, 1000])) for c in used}
        n = ceil(sum(mass.values())) + rnd.randint(0, 3)
        v = loads(mass)
        y, steps = iterative_round(mass, n)
        max_steps = max(max_steps, steps)
        assert all(val.denominator == 1 and val >= 0 for val in y.values())
        assert sum(y.values()) == n
        assert set(y) == set(used) | {0}                     # no new cells
        w = loads(y)
        for j in range(7):
            assert w[j] > v[j] - 6, (w[j], v[j])
            assert w[j] >= floor(v[j]) - 5
            worst = max(worst, floor(v[j]) - w[j])
    print(f"[C] {trials} random supports/masses: Beck-Fiala rounding (threshold 7) gives integer masses on the SAME cells, "
          f"total = n, every window > v - 6 (>= floor(v) - 5); worst observed floor(v) - window = {worst}; "
          f"max steps = {max_steps}")

def part_c_adversarial(rnd, trials=300):
    """Adversarial masses: all fractional parts near 1 on dense supports (all 3-sets; all <=3-sets; catalogue orbit
    with 5-cells), to push the loss up."""
    worst = 0
    fams = []
    fams.append([c for c in range(1, FULL) if bin(c).count("1") == 3])
    fams.append([c for c in range(1, FULL) if bin(c).count("1") <= 3])
    fams.append([c for c in range(1, FULL) if bin(c).count("1") <= 2] + [c for c in range(1, FULL) if bin(c).count("1") == 3 and c & 1])
    for _ in range(trials):
        used = rnd.choice(fams)
        used = rnd.sample(used, rnd.randint(max(1, len(used) // 2), len(used)))
        mass = {c: rnd.randint(0, 5) + Fr(rnd.randint(900, 999), 1000) for c in used}
        n = ceil(sum(mass.values()))
        v = loads(mass)
        y, _ = iterative_round(mass, n)
        w = loads(y)
        for j in range(7):
            assert w[j] > v[j] - 6
            worst = max(worst, floor(v[j]) - w[j])
    print(f"[C-adv] {trials} adversarial instances (fractional parts >= 0.9): worst observed floor(v) - window = {worst}")

def main():
    rnd = random.Random(20260924)
    orbits = json.load(open(CAT))["orbits"]
    part_a()
    part_b(rnd, orbits)
    part_c(rnd, orbits)
    part_c_adversarial(rnd)
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
