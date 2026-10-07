#!/usr/bin/env python3
"""Referee (w4, tcglobal 'Fano-labelled tools cannot remove intersecting'): independent exact checks.
(1) (32,26) types (22,1),(5,18): for EVERY 2^7 assignment of types to the 7 Fano LINES, exhibit a violated
    NECESSARY condition (per part: load<=cap; for each POINT Q, the 3 lines through Q carry <= 2*cap; total <= 4*cap).
    Necessity: a vertex with safe sigma (all lines of sigma miss some point P) lies on <=4 rows, and on <=2 of the
    three lines through any Q (0 if Q=P, else the line PQ is excluded). Pure integers, no LP, no duality shortcut.
    Also exact integer tau (=20) and continuous tau* (=18), and an explicit bad 5-tuple (non-(7,2)).
(2) Strengthening: two disjoint parts of size n < 3r/2, all r-sets in a part: brute force for r=4,n=5 that no
    Fano-labelled 7-tuple exists (indexed by lines, repetition allowed), tau = 4 = k, and a bad 6-tuple exists.
"""
import itertools
LINES = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
assert all(len(a & b) == 1 for a, b in itertools.combinations(LINES, 2))
THRU = [[j for j, l in enumerate(LINES) if q in l] for q in range(7)]
def safe(sig):  # set of line indices; safe iff some point lies on none of them
    return any(all(p not in LINES[j] for j in sig) for p in range(7))
# ---- (1)
caps = (32, 26); types = [(22, 1), (5, 18)]
viol = 0
for asg in itertools.product(range(2), repeat=7):
    found = False
    for i, c in enumerate(caps):
        loads = [types[asg[j]][i] for j in range(7)]
        if max(loads) > c or sum(loads) > 4*c or any(sum(loads[j] for j in THRU[q]) > 2*c for q in range(7)):
            found = True; break
    if not found: viol += 1
print("(1) assignments with NO violated necessary condition (must be 0):", viol)
# exact integer tau: T=(u,v) meets all (22,1)-edges iff 32-u<22 or 26-v<1; all (5,18) iff 32-u<5 or 26-v<18
def kills(u, v, a):
    return caps[0]-u < a[0] or caps[1]-v < a[1]
tau = min(u+v for u in range(33) for v in range(27) if all(kills(u, v, a) for a in types))
print("(1) exact integer tau =", tau, " k = 23  tau/k =", tau/23, "(continuous tau* = 18, ratio 18/23 =", 18/23, ")")
# explicit bad 5-tuple: X = 0..31, Y = 32..57
X = list(range(32)); Y = list(range(32, 58))
G = set(X[:22]) | {Y[0]}
Xr = X[22:]; Yr = Y[1:]          # 10 and 25 points avoiding G
Ds = []
Ycomp = [Yr[0:7], Yr[7:14], Yr[14:21], Yr[21:25] + Yr[0:3]]
Xcomp = [Xr[0:5], Xr[5:10], Xr[0:5], Xr[5:10]]
for i in range(4):
    D = (set(Xr) - set(Xcomp[i])) | (set(Yr) - set(Ycomp[i]))
    assert len(D & set(X)) == 5 and len(D & set(Y)) == 18 and not (D & G)
    Ds.append(D)
tup = [G] + Ds; V = set().union(*tup)
pierce = any(all(x in E or y in E for E in tup) for x in V for y in V)
print("(1) explicit 5-tuple G + 4 disjoint (5,18)-edges 2-pierceable?", pierce, "(must be False)")
# ---- (2)
r, n = 4, 5
A = list(range(n)); B = list(range(n, 2*n))
EA = [frozenset(c) for c in itertools.combinations(A, r)]
EB = [frozenset(c) for c in itertools.combinations(B, r)]
def part_ok(lines_in_part, edges, pts):
    # exists assignment edges -> these lines with every vertex of the part safe
    for choice in itertools.product(edges, repeat=len(lines_in_part)):
        if all(safe([lines_in_part[k] for k in range(len(lines_in_part)) if v in choice[k]]) for v in pts):
            return True
    return False
cnt = 0
for col in itertools.product(range(2), repeat=7):
    SA = [j for j in range(7) if col[j] == 0]; SB = [j for j in range(7) if col[j] == 1]
    if part_ok(SA, EA, A) and part_ok(SB, EB, B): cnt += 1
print("(2) r=4,n=5: colourings admitting a Fano-labelled tuple (must be 0):", cnt)
allE = EA + EB; Vall = A + B
def tau_of(E):
    for s in range(1, len(Vall)+1):
        for T in itertools.combinations(Vall, s):
            if all(e & set(T) for e in E): return s
print("(2) tau =", tau_of(allE), "= k =", r)
bad6 = [EA[0]] + EB   # EB = all 5 four-subsets of B, no common point
print("(2) 6-tuple 2-pierceable?", any(all(x in e or y in e for e in bad6) for x in Vall for y in Vall), "(must be False)")
