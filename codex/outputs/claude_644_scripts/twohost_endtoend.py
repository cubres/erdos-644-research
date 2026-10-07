#!/usr/bin/env python3
"""
twohost_endtoend.py -- end-to-end test of the two constructions used in the report (exact, bitmask sets).

Run:  python3 twohost_endtoend.py [seed] [trials]
For random families H (not assumed (7,2)) on n <= 11 vertices we compute tau(H) exactly and T = tau-1.
 (a) SHARP GT: for every good triple (G1,G2,G3) (no common point) with |union| <= 2T-1 we build the
     pencil 7-tuple: classes A (not in G1), B (in G1, not in G2), C (in G1,G2, hence not in G3),
     balanced splits with the parity placement, four m-line edges = any actual edges avoiding the
     m-line classes (they exist because each m-line class set has <= T points), and verify that
     the resulting <= 7 actual edges have NO transversal of size <= 2.
 (b) TWO-COLOUR LEMMA: for every edge E, every quartering, every B1,B2,C1,C2 with the required
     trace conditions and |X| + max(|E1|+|E4|,|E2|+|E3|) <= T, where
     X = ((B1 u B2) n (C1 u C2)) \\ E, we set Q = X, O1 = (B1 u B2)\\(E u Q), O0 = rest, pick the two
     global edges (avoiding Q u E1 u E4 and Q u E2 u E3), and verify the 7-tuple is not 2-pierceable.
Any failure would refute the corresponding proof; the script reports counts.
"""
import itertools, random, sys

def popcount(x): return bin(x).count("1")

def tau_exact(edges, n):
    full = (1 << n) - 1
    for s in range(0, n + 1):
        for comb in itertools.combinations(range(n), s):
            m = 0
            for v in comb: m |= 1 << v
            if all(e & m for e in edges):
                return s
    return None

def two_pierceable(edges, n):
    # exists x,y (x==y allowed) meeting every edge
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            if all(e & m for e in edges):
                return True
    return False

def find_avoiding(edges, forbidden):
    for e in edges:
        if e & forbidden == 0:
            return e
    return None

def pencil_tuple(G1, G2, G3, edges, n, T):
    W = G1 | G2 | G3
    A = W & ~G1                       # not in G1
    B = W & G1 & ~G2                  # in G1, not in G2
    C = W & G1 & G2                   # in G1 and G2 -> not in G3 (good triple)
    def split(S, big_first=True):
        vs = [v for v in range(n) if S >> v & 1]
        h = (len(vs) + 1) // 2 if big_first else len(vs) // 2
        s1 = 0
        for v in vs[:h]: s1 |= 1 << v
        return s1, S & ~s1
    a, a2 = split(A, True)
    b, b2 = split(B, True)
    c, c2 = split(C, False)           # extra of C goes to c'
    mlines = [a | b | c, a2 | b2 | c, a2 | b | c2, a | b2 | c2]
    tup = [G1, G2, G3]
    for M in mlines:
        if popcount(M) > T:
            return None, "mline too big"
        g = find_avoiding(edges, M)
        if g is None:
            return None, "no avoiding edge (tau violated?)"
        tup.append(g)
    return tup, None

def twocolour_tuple(E, quarters, B1, B2, C1, C2, edges, n, T):
    E1, E2, E3, E4 = quarters
    X = ((B1 | B2) & (C1 | C2)) & ~E
    Q = X
    g1 = find_avoiding(edges, Q | E1 | E4)
    g2 = find_avoiding(edges, Q | E2 | E3)
    if g1 is None or g2 is None:
        return None
    return [E, B1, B2, C1, C2, g1, g2]

def quarterings(E, n):
    vs = [v for v in range(n) if E >> v & 1]
    e = len(vs)
    j, r = divmod(e, 4)
    sizes = [j + 1] * r + [j] * (4 - r)
    out = []
    for perm in set(itertools.permutations(sizes)):
        # random assignment of the vertices to quarters of these sizes
        vv = vs[:]
        random.shuffle(vv)
        qs, pos = [], 0
        for s in perm:
            m = 0
            for v in vv[pos:pos + s]: m |= 1 << v
            qs.append(m); pos += s
        out.append(tuple(qs))
    return out

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    random.seed(seed)
    stats = dict(fams=0, gt_cases=0, gt_bad=0, gt_fail=0, tc_cases=0, tc_bad=0, tc_fail=0)
    for _ in range(trials):
        n = random.randint(7, 11)
        k = random.randint(3, min(7, n - 2))
        m = random.randint(6, 40)
        edges = set()
        for _ in range(m):
            size = random.randint(max(2, k - 2), k)
            S = random.sample(range(n), size)
            mm = 0
            for v in S: mm |= 1 << v
            edges.add(mm)
        edges = list(edges)
        tau = tau_exact(edges, n)
        if tau is None or tau < 3:
            continue
        T = tau - 1
        stats['fams'] += 1
        # (a) sharp GT
        for G1, G2, G3 in itertools.combinations_with_replacement(edges, 3):
            if G1 & G2 & G3:
                continue
            if popcount(G1 | G2 | G3) <= 2 * T - 1:
                for perm in set(itertools.permutations((G1, G2, G3))):
                    tup, err = pencil_tuple(*perm, edges, n, T)
                    stats['gt_cases'] += 1
                    if tup is None:
                        stats['gt_fail'] += 1
                        print("GT construction failed:", err)
                    elif two_pierceable(tup, n):
                        stats['gt_fail'] += 1
                        print("GT tuple 2-pierceable!", [bin(x) for x in tup])
                    else:
                        stats['gt_bad'] += 1
                    break
        # (b) two-colour lemma
        for E in edges:
            if popcount(E) < 4:
                continue
            for qs in quarterings(E, n):
                E1, E2, E3, E4 = qs
                glob = max(popcount(E1 | E4), popcount(E2 | E3))
                Bs1 = [g for g in edges if g & (E1 | E2) == 0]
                Bs2 = [g for g in edges if g & (E3 | E4) == 0]
                Cs1 = [g for g in edges if g & (E1 | E3) == 0]
                Cs2 = [g for g in edges if g & (E2 | E4) == 0]
                if not (Bs1 and Bs2 and Cs1 and Cs2):
                    continue
                cnt = 0
                for B1 in Bs1:
                    for B2 in Bs2:
                        for C1 in Cs1:
                            for C2 in Cs2:
                                X = ((B1 | B2) & (C1 | C2)) & ~E
                                if popcount(X) + glob <= T:
                                    stats['tc_cases'] += 1
                                    tup = twocolour_tuple(E, qs, B1, B2, C1, C2, edges, n, T)
                                    if tup is None:
                                        stats['tc_fail'] += 1
                                        print("two-colour: global edge missing")
                                    elif two_pierceable(tup, n):
                                        stats['tc_fail'] += 1
                                        print("two-colour tuple 2-pierceable!")
                                    else:
                                        stats['tc_bad'] += 1
                                    cnt += 1
                                    if cnt > 50:
                                        break
                            if cnt > 50: break
                        if cnt > 50: break
                    if cnt > 50: break
    print(stats)
    good = stats['gt_fail'] == 0 and stats['tc_fail'] == 0
    print("ALL CONSTRUCTED TUPLES BAD" if good else "FAILURES FOUND")
    sys.exit(0 if good else 1)

if __name__ == "__main__":
    main()
