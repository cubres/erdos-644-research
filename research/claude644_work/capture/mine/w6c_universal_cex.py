#!/usr/bin/env python3
"""w6c_universal_cex.py -- exact check: the counting target  sum_i|W_i| + 2t <= 6k + o(k)  (equivalently the
gap-sensitive target D <= 2(p-t) + o(k) for full rows) FAILS for general (7,2) families at a joint minimiser.
Family H = six rows F_1..F_6 on classes X_j (sigma={j}, size m) and Y_ab (missing {a,b}, size 1), all 15 pairs.
Checks by brute force on vertices: (7,2) (every multiset of <=7 rows = subset of the six), tau(H)=2, the full
tuple is a lex (|P|,|Pi|) minimiser (every 6-tuple uses a subset of the rows, whose pair set contains Pi),
p, |Pi|, W_i, sum|W_i|+2t versus 6k."""
import itertools, sys
m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
verts = []   # sigma of each vertex
for j in range(6):
    verts += [frozenset([j])] * m
for a, b in itertools.combinations(range(6), 2):
    verts.append(frozenset(range(6)) - {a, b})
n = len(verts)
rows = [set(v for v in range(n) if i in verts[v]) for i in range(6)]
k = max(len(F) for F in rows)
def Pi_of(R):
    return [pr for pr in itertools.combinations(range(n), 2) if all(pr[0] in F or pr[1] in F for F in R)]
Pi = Pi_of(rows); P = set(x for pr in Pi for x in pr)
# tau(H)=2: no common point, and a piercing pair exists
common = set.intersection(*rows)
assert not common and Pi
# lex minimiser: any 6-tuple over these rows uses a subset S of rows; Pi(S) contains Pi(all)
for r in range(1, 7):
    for S in itertools.combinations(range(6), r):
        PS = Pi_of([rows[i] for i in S]); assert set(Pi) <= set(PS)
W = []
for i in range(6):
    Gi = Pi_of(rows[:i] + rows[i+1:]); Ai = set(Gi) - set(Pi)
    W.append(len(set(x for pr in Ai for x in pr)))
t = 2
print('m', m, 'n', n, 'k', k, 'rows', [len(F) for F in rows], 'p', len(P), '|Pi|', len(Pi), 'W', W)
print('sum|W|+2t =', sum(W) + 2 * t, '  6k =', 6 * k, '  excess =', sum(W) + 2 * t - 6 * k)
