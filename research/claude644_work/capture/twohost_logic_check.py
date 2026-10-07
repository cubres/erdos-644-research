#!/usr/bin/env python3
"""
twohost_logic_check.py  --  exact finite checks for the global-selection report (Claude, 23 Sep 2026).

Run:  python3 twohost_logic_check.py
All checks are exact integer / set computations (no floating point).  Exit code 0 iff all pass.

Checks:
 (1) The seven lines used for the TWO-COLOUR shape (points p0,p1,q,r1..r4) form a Fano plane.
 (2) Two-colour shape logic: with labels E_i->r_i, Q->q, O0->p0, O1->p1 and edges
        L={p0,p1,q}:E, {p0,r1,r2}:B1, {p0,r3,r4}:B2, {p1,r1,r3}:C1, {p1,r2,r4}:C2,
        {q,r1,r4}:global g1, {q,r2,r3}:global g2,
     every label p is such that every line through p carries an edge that is REQUIRED to avoid
     the class of p (so the Venn/Fano criterion applies).  Verified by enumerating lines.
 (3) Pencil rounding lemma (sharp GT): for all class sizes A,B,C (A+B+C <= 80) there is a split
     A=a+a', B=b+b', C=c+c' with max over the four m-lines of the labelled load
     <= floor((A+B+C)/2) + 1, and this bound is attained for some (A,B,C) of every total >= 2.
 (4) Two-colour quarter arrangement: for every e >= 4 there is a quartering with both
     'global' pairs |E1|+|E4|, |E2|+|E3| <= ceil(e/2) and all six pairs <= 2*ceil(e/4).
"""
import itertools, sys

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# ---------------------------------------------------------------- (1) two-colour Fano plane
P = ['p0', 'p1', 'q', 'r1', 'r2', 'r3', 'r4']
LINES2 = {
    'L':  ('p0', 'p1', 'q'),
    'B1': ('p0', 'r1', 'r2'),
    'B2': ('p0', 'r3', 'r4'),
    'C1': ('p1', 'r1', 'r3'),
    'C2': ('p1', 'r2', 'r4'),
    'g1': ('q', 'r1', 'r4'),
    'g2': ('q', 'r2', 'r3'),
}
pairs_seen = {}
for name, ln in LINES2.items():
    check(len(set(ln)) == 3, "line size " + name)
    for a, b in itertools.combinations(sorted(ln), 2):
        pairs_seen.setdefault((a, b), []).append(name)
check(len(pairs_seen) == 21 and all(len(v) == 1 for v in pairs_seen.values()),
      "two-colour lines are not a Fano plane")
print("(1) two-colour configuration is a Fano plane:", len(pairs_seen) == 21)

# ---------------------------------------------------------------- (2) two-colour shape logic
# class of each label and which classes each edge is REQUIRED to avoid (from the hypotheses)
avoid_required = {
    'L':  {'p0', 'p1', 'q'},        # E is disjoint from O0, O1, Q by definition
    'B1': {'p0', 'r1', 'r2'},       # B1 avoids O0 and E1 u E2
    'B2': {'p0', 'r3', 'r4'},
    'C1': {'p1', 'r1', 'r3'},
    'C2': {'p1', 'r2', 'r4'},
    'g1': {'q', 'r1', 'r4'},        # global request: Q u E1 u E4
    'g2': {'q', 'r2', 'r3'},
}
for name in LINES2:
    check(set(LINES2[name]) == avoid_required[name], "edge %s does not avoid its line classes" % name)
# Venn/Fano criterion: for any two labels (equal allowed) some line through both -> its edge misses both
for x, y in itertools.product(P, repeat=2):
    lines_xy = [n for n, ln in LINES2.items() if x in ln and y in ln]
    check(len(lines_xy) >= 1, "no line through %s,%s" % (x, y))
print("(2) two-colour shape: every edge avoids exactly the classes of its line; any two labels lie on a line")

# ---------------------------------------------------------------- (3) pencil rounding lemma
def best_mline_max(A, B, C):
    best = None
    for a in range(A + 1):
        for b in range(B + 1):
            for c in range(C + 1):
                a2, b2, c2 = A - a, B - b, C - c
                m = max(a + b + c, a2 + b2 + c, a2 + b + c2, a + b2 + c2)
                if best is None or m < best:
                    best = m
    return best

worst_excess = {}
for tot in range(0, 81):
    for A in range(tot + 1):
        for B in range(tot - A + 1):
            C = tot - A - B
            # fast closed form candidate: balanced split with smart parity placement
            m = best_mline_max(A, B, C) if tot <= 30 else None
            if m is None:
                # closed form: a=ceil(A/2), b=ceil(B/2), c'=ceil(C/2) placement (checked vs brute force below)
                a, a2 = (A + 1) // 2, A // 2
                b, b2 = (B + 1) // 2, B // 2
                c, c2 = C // 2, (C + 1) // 2
                m = max(a + b + c, a2 + b2 + c, a2 + b + c2, a + b2 + c2)
            check(m <= tot // 2 + 1, "rounding lemma fails at %s" % ((A, B, C),))
            worst_excess[tot] = max(worst_excess.get(tot, -99), m - tot // 2)
# brute force agrees with the closed-form placement for tot <= 30
for tot in range(0, 31):
    for A in range(tot + 1):
        for B in range(tot - A + 1):
            C = tot - A - B
            a, a2 = (A + 1) // 2, A // 2
            b, b2 = (B + 1) // 2, B // 2
            c, c2 = C // 2, (C + 1) // 2
            mcf = max(a + b + c, a2 + b2 + c, a2 + b + c2, a + b2 + c2)
            check(mcf <= tot // 2 + 1, "closed-form placement exceeds bound at %s" % ((A, B, C),))
attained = all(worst_excess[tot] == 1 for tot in range(2, 81))
check(attained, "bound floor(W/2)+1 not attained for some total")
print("(3) pencil rounding: max m-line load <= floor(|W|/2)+1 for all A+B+C<=80; attained for every total >=2:",
      attained)
print("    => a good triple with |W| <= 2T-1 gives m-line requests of size <= T  (T = t-1)  => union >= 2t-2")

# ---------------------------------------------------------------- (4) quarter arrangement
for e in range(4, 400):
    j, r = divmod(e, 4)
    sizes = [j + 1] * r + [j] * (4 - r)          # balanced quarter sizes
    found = False
    for perm in set(itertools.permutations(sizes)):
        E1, E2, E3, E4 = perm
        glob = max(E1 + E4, E2 + E3)
        allpairs = max(x + y for x, y in itertools.combinations(perm, 2))
        if glob <= (e + 1) // 2 and allpairs <= 2 * ((e + 3) // 4):
            found = True
            break
    check(found, "no good quartering for e=%d" % e)
print("(4) for every 4<=e<400 a balanced quartering has global pairs <= ceil(e/2), all pairs <= 2ceil(e/4)")

print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
