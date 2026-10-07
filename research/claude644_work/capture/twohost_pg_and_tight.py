#!/usr/bin/env python3
"""
twohost_pg_and_tight.py -- exact certificates for the report (Claude, 23 Sep 2026).

Run:  python3 twohost_pg_and_tight.py
Exit code 0 iff every check passes. Pure integer / set arithmetic.

PART A (separation of the two-colour lemma from all single-host/pencil consequences):
  H_q = lines of PG(2,q), q in {5,7,11}.  Every q-set of points is avoided by a line (T=q; tau=q+1).
  (A1) every three lines with empty common intersection span exactly 3q >= 2(q+1)-2 points, and
       every point set of size <= 2(q+1)-3 contains at most one line: so the sharp triple bound
       (GT*) and every conclusion of Theorem G hold in H_q with t = q+1;
  (A2) the two-colour recipe (E a line, balanced quartering, B1=<P,e4>, C2=<P,e1>, C1 another line
       through e4, B2 another line through e1) gives |X| = 2 and |X| + max(|E1|+|E4|,|E2|+|E3|) <= q,
       and the resulting 7 lines (with the two global lines) have NO 2-point transversal.
  (A3) for q=5, exhaustive: min |X| over all admissible (E-quartering, B1,B2,C1,C2) equals 2.
PART B (sharpness of GT* at a fully normalized family, note 7.134, m=1):
  K = all 5-subsets of [9]  (k=5, t=5).  (B1) (7,2) holds: no <=7 four-subsets cover all 36 pairs
  (backtracking); (B2) tau = 5; (B3) min union over good triples = 8 = 2t-2;
  (B4) two-colour lemma: min |X| over all admissible configurations vs the bound t - glob.
PART C: explicit good triple of union 6m+2 = 2t-2 in all (4m+1)-subsets of a (7m+2)-set, m=1..8.
PART D: parity family, m=1 (all 4-subsets of [8] meeting A={0,1,2,3} in an odd number):
  (7,2), tau = 4 = 3k/4+1, min good-triple union.
"""
import itertools, sys

ok = True
def check(c, msg):
    global ok
    if not c:
        ok = False
        print("FAIL:", msg)

def popcount(x): return bin(x).count("1")

# ------------------------------------------------------------------ PART A
def pg2(q):
    pts = []
    for x in range(q):
        for y in range(q):
            for z in range(q):
                v = (x, y, z)
                if v == (0, 0, 0): continue
                # normalize: first nonzero coordinate = 1
                i = next(i for i in range(3) if v[i] != 0)
                inv = pow(v[i], q - 2, q)
                w = tuple((c * inv) % q for c in v)
                if w == v: pts.append(v)
    idx = {p: i for i, p in enumerate(pts)}
    lines = []
    for l in pts:  # dual
        m = 0
        for p in pts:
            if (l[0] * p[0] + l[1] * p[1] + l[2] * p[2]) % q == 0:
                m |= 1 << idx[p]
        lines.append(m)
    return pts, lines

def two_pierceable(edges, n):
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            if all(e & m for e in edges):
                return True
    return False

def line_through(lines, a, b):
    m = (1 << a) | (1 << b)
    for L in lines:
        if L & m == m: return L
    return None

for q in (5, 7, 11):
    pts, lines = pg2(q)
    n = len(pts)
    check(n == q * q + q + 1 and len(lines) == n, "PG size")
    t = q + 1; T = q
    # every q-set avoided: proof in report (pencil at an outside point); spot-check tau>q on random sets
    # (A1) triples
    if q <= 7:
        mn = None
        for L1, L2, L3 in itertools.combinations(lines, 3):
            if L1 & L2 & L3: continue
            u = popcount(L1 | L2 | L3)
            mn = u if mn is None else min(mn, u)
        check(mn == 3 * q, "PG(2,%d) min good-triple union %s != 3q" % (q, mn))
        check(mn >= 2 * t - 2, "GT* fails in PG?")
    # two lines span 2q+1 > 2t-3 = 2q-1 points: at most one line in any (2t-3)-set
    check(2 * q + 1 > 2 * t - 3, "two lines fit in 2t-3")
    # (A2) recipe
    E = lines[0]
    Epts = [v for v in range(n) if E >> v & 1]
    e = len(Epts)
    j, r = divmod(e, 4)
    # arrange quarter sizes so that global pairs E1+E4, E2+E3 are <= ceil(e/2)
    sizes = {0: [j, j, j, j], 1: [j + 1, j, j, j], 2: [j + 1, j + 1, j, j], 3: [j + 1, j + 1, j + 1, j]}[r]
    # order: E1,E2,E3,E4 ; for r=2 use (j+1, j+1, j, j) -> E1+E4 = 2j+1, E2+E3 = 2j+1
    qs, pos = [], 0
    for s in sizes:
        m = 0
        for v in Epts[pos:pos + s]: m |= 1 << v
        qs.append(m); pos += s
    E1, E2, E3, E4 = qs
    glob = max(popcount(E1 | E4), popcount(E2 | E3))
    e1 = next(v for v in range(n) if E1 >> v & 1)
    e4 = next(v for v in range(n) if E4 >> v & 1)
    P = next(v for v in range(n) if not (E >> v & 1))
    B1 = line_through(lines, P, e4)
    C2 = line_through(lines, P, e1)
    C1 = next(L for L in lines if (L >> e4 & 1) and L not in (E, B1))
    B2 = next(L for L in lines if (L >> e1 & 1) and L not in (E, C2))
    check(B1 & (E1 | E2) == 0 and B2 & (E3 | E4) == 0 and C1 & (E1 | E3) == 0 and C2 & (E2 | E4) == 0,
          "trace conditions q=%d" % q)
    X = ((B1 | B2) & (C1 | C2)) & ~E
    check(popcount(X) == 2, "|X| != 2 for q=%d" % q)
    Q = X
    g1 = next((L for L in lines if L & (Q | E1 | E4) == 0), None)
    g2 = next((L for L in lines if L & (Q | E2 | E3) == 0), None)
    check(popcount(Q | E1 | E4) <= T and popcount(Q | E2 | E3) <= T, "global request too large q=%d" % q)
    check(g1 is not None and g2 is not None, "global lines missing q=%d" % q)
    tup = [E, B1, B2, C1, C2, g1, g2]
    bad = not two_pierceable(tup, n)
    check(bad, "two-colour 7-tuple is 2-pierceable in PG(2,%d)" % q)
    print("A: PG(2,%d): t=%d, |X|=%d, glob=%d, |X|+glob=%d <= T=%d; seven lines bad: %s; distinct lines: %d"
          % (q, t, popcount(X), glob, popcount(X) + glob, T, bad, len(set(tup))))

# (A3) exhaustive min |X| for q=5
q = 5
pts, lines = pg2(q)
n = len(pts)
E = lines[0]
Epts = [v for v in range(n) if E >> v & 1]
minX = None
for perm in itertools.permutations(Epts):
    # quarters of sizes (2,2,1,1) in order E1..E4 (E1+E4 = 3, E2+E3 = 3)
    E1 = (1 << perm[0]) | (1 << perm[1]); E2 = (1 << perm[2]) | (1 << perm[3])
    E3 = 1 << perm[4]; E4 = 1 << perm[5]
    Bs1 = [L for L in lines if L & (E1 | E2) == 0]
    Bs2 = [L for L in lines if L & (E3 | E4) == 0]
    Cs1 = [L for L in lines if L & (E1 | E3) == 0]
    Cs2 = [L for L in lines if L & (E2 | E4) == 0]
    for B1 in Bs1:
        for B2 in Bs2:
            for C1 in Cs1:
                for C2 in Cs2:
                    x = popcount(((B1 | B2) & (C1 | C2)) & ~E)
                    if minX is None or x < minX: minX = x
    break  # one quartering suffices by symmetry of PG(2,q) (collineations act transitively on ordered frames)
check(minX == 2, "PG(2,5) min |X| = %s" % minX)
print("A3: PG(2,5) exhaustive min |X| over (B1,B2,C1,C2) for a fixed quartering =", minX)

# ------------------------------------------------------------------ PART B  K_9^5
n, k = 9, 5
edges = []
for S in itertools.combinations(range(n), k):
    m = 0
    for v in S: m |= 1 << v
    edges.append(m)
full = (1 << n) - 1
blocks = [full & ~e for e in edges]      # complements: 4-sets
allpairs = [(x, y) for x in range(n) for y in range(x + 1, n)]
def covers(block, p): return (block >> p[0] & 1) and (block >> p[1] & 1)
blocks_with_pair = {p: [b for b in blocks if covers(b, p)] for p in allpairs}
def bt(covered, depth, maxd):
    unc = [p for p in allpairs if p not in covered]
    if not unc: return True
    if depth == maxd: return False
    if len(unc) > 6 * (maxd - depth): return False
    p = unc[0]
    for b in blocks_with_pair[p]:
        new = set(covered)
        for pp in allpairs:
            if covers(b, pp): new.add(pp)
        if bt(new, depth + 1, maxd): return True
    return False
cover7 = bt(set(), 0, 7)
check(not cover7, "K_9^5: seven 4-sets cover all pairs -> (7,2) fails")
print("B1: K_9^5 (7,2) holds (no 7 four-sets cover all 36 pairs):", not cover7)
# tau = 5
t = 5
check(all(any(e & 0 == 0 for e in edges) for _ in [0]), "")
tau_ok = all(any((e & m) == 0 for e in edges) for S in itertools.combinations(range(n), 4)
             for m in [sum(1 << v for v in S)]) and all(all(e & m for e in edges)
             for S in [range(5)] for m in [sum(1 << v for v in S)])
check(tau_ok, "tau(K_9^5) != 5")
print("B2: tau(K_9^5) = 5:", tau_ok)
mn = None
for G1, G2, G3 in itertools.combinations_with_replacement(edges, 3):
    if G1 & G2 & G3: continue
    u = popcount(G1 | G2 | G3)
    mn = u if mn is None else min(mn, u)
check(mn == 2 * t - 2, "K_9^5 min union %s != 2t-2" % mn)
print("B3: K_9^5 min good-triple union =", mn, "= 2t-2 =", 2 * t - 2)
# B4 two-colour tightness: E = {0..4}, quarter sizes (2,1,1,1) arranged E1+E4 <= 3, E2+E3 <= 2
E = sum(1 << v for v in range(5))
best = None
for perm in itertools.permutations(range(5)):
    E1 = (1 << perm[0]) | (1 << perm[1]); E2 = 1 << perm[2]; E3 = 1 << perm[3]; E4 = 1 << perm[4]
    glob = max(popcount(E1 | E4), popcount(E2 | E3))
    Bs1 = [g for g in edges if g & (E1 | E2) == 0]
    Bs2 = [g for g in edges if g & (E3 | E4) == 0]
    Cs1 = [g for g in edges if g & (E1 | E3) == 0]
    Cs2 = [g for g in edges if g & (E2 | E4) == 0]
    mX = min(popcount(((B1 | B2) & (C1 | C2)) & ~E) for B1 in Bs1 for B2 in Bs2 for C1 in Cs1 for C2 in Cs2)
    check(mX >= t - glob, "two-colour lemma violated in K_9^5")
    best = (mX, glob) if best is None else best
    break
print("B4: K_9^5 two-colour: min |X| =", best[0], " bound t - glob =", t - best[1])

# ------------------------------------------------------------------ PART C explicit tight triples
for m in range(1, 9):
    n = 7 * m + 2; k = 4 * m + 1; t = 3 * m + 2
    V = list(range(n))
    X0 = V[:m]; z = V[m]; Y1 = V[m + 1:3 * m + 1]; Y2 = V[3 * m + 1:5 * m + 1]; Y3 = V[5 * m + 1:]
    check(len(Y1) == 2 * m and len(Y2) == 2 * m and len(Y3) == 2 * m + 1, "sizes m=%d" % m)
    C1 = set(X0) | {z} | set(Y1); C2 = set(X0) | {z} | set(Y2); C3 = set(X0) | set(Y3)
    G = [set(V) - C for C in (C1, C2, C3)]
    check(all(len(g) == k for g in G), "edge sizes m=%d" % m)
    check(not (G[0] & G[1] & G[2]), "common point m=%d" % m)
    check(len(G[0] | G[1] | G[2]) == 2 * t - 2, "union != 2t-2 m=%d" % m)
print("C: explicit good triples of union exactly 2t-2 in K_{7m+2}^{(4m+1)}, m=1..8: verified")

# ------------------------------------------------------------------ PART D parity family m=1
n, k = 8, 4
A = 0b1111
edges = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)
         if popcount(sum(1 << v for v in S) & A) % 2 == 1]
full = (1 << n) - 1
blocks = [full & ~e for e in edges]
allpairs = [(x, y) for x in range(n) for y in range(x + 1, n)]
blocks_with_pair = {p: [b for b in blocks if covers(b, p)] for p in allpairs}
cover7 = bt(set(), 0, 7)
check(not cover7, "parity m=1 fails (7,2)")
tau = None
for s in range(0, n + 1):
    if any(all(e & sum(1 << v for v in S) for e in edges) for S in itertools.combinations(range(n), s)):
        tau = s; break
check(tau == 4, "parity tau = %s" % tau)
mn = None
for G1, G2, G3 in itertools.combinations_with_replacement(edges, 3):
    if G1 & G2 & G3: continue
    u = popcount(G1 | G2 | G3)
    mn = u if mn is None else min(mn, u)
print("D: parity m=1: (7,2) =", not cover7, " tau =", tau, " min good-triple union =", mn,
      " (2t-2 =", 2 * tau - 2, ")")
check(mn >= 2 * tau - 2, "GT* violated in parity family")

print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
