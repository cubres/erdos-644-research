#!/usr/bin/env python3
"""
threehost_check.py -- exact check of the anchored Fano THREE-HOST lemma (Claude, 23 Sep 2026).

Statement checked.  H has (7,2); E in H; E = E1 u E2 u E3 u E4 (quarters); pairings
   pi_x = {E1uE2, E3uE4},  pi_y = {E1uE3, E2uE4},  pi_z = {E1uE4, E2uE3}.
For EVERY partition V \\ E = Vx u Vy u Vz there are w in {x,y,z} and S in pi_w such that every edge
disjoint from V_w meets S.   (No hypothesis on tau is needed.)

Part 1: exhaustive over all 3-partitions of V\\E, all edges E and one random quartering per E, for
        (7,2) families = random subfamilies of K_N^(k) with 7*C(N-k,2) < C(N,2) (then (7,2) holds by
        counting: seven complements cannot cover all pairs), and for K_9^(5).
Part 2: contrapositive on random families (no (7,2) assumed): whenever a partition has an edge
        avoiding V_w u S for all six (w,S), the seven edges E, G_{w,S} are verified NOT 2-pierceable.
Run: python3 threehost_check.py [seed]
"""
import itertools, random, sys
from math import comb

def popcount(x): return bin(x).count("1")

def two_pierceable(edges, n):
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            if all(e & m for e in edges):
                return True
    return False

def quartering(E, n):
    vs = [v for v in range(n) if E >> v & 1]
    random.shuffle(vs)
    e = len(vs); j, r = divmod(e, 4)
    sizes = [j + 1] * r + [j] * (4 - r)
    qs, pos = [], 0
    for s in sizes:
        m = 0
        for v in vs[pos:pos + s]: m |= 1 << v
        qs.append(m); pos += s
    return qs

def pairings(qs):
    E1, E2, E3, E4 = qs
    return {'x': (E1 | E2, E3 | E4), 'y': (E1 | E3, E2 | E4), 'z': (E1 | E4, E2 | E3)}

def partitions3(rest):
    vs = [v for v in range(64) if rest >> v & 1]
    for colors in itertools.product(range(3), repeat=len(vs)):
        parts = [0, 0, 0]
        for v, c in zip(vs, colors): parts[c] |= 1 << v
        yield {'x': parts[0], 'y': parts[1], 'z': parts[2]}

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    random.seed(seed)
    ok = True
    # ---------------- Part 1
    fams = []
    for (N, k) in [(8, 5), (8, 6), (9, 6), (9, 7), (7, 5), (10, 7), (10, 8)]:
        assert 7 * comb(N - k, 2) < comb(N, 2), (N, k)
        allk = [sum(1 << v for v in S) for S in itertools.combinations(range(N), k)]
        for _ in range(6):
            sub = random.sample(allk, random.randint(3, min(len(allk), 25)))
            fams.append((N, sub))
    # K_9^5 (7,2) certified in twohost_pg_and_tight.py
    fams.append((9, [sum(1 << v for v in S) for S in itertools.combinations(range(9), 5)]))
    checked = 0
    for n, H in fams:
        full = (1 << n) - 1
        for E in H:
            if popcount(E) < 4: continue
            qs = quartering(E, n)
            pw = pairings(qs)
            for part in partitions3(full & ~E):
                found = False
                for w in 'xyz':
                    rest_edges = [G for G in H if G & part[w] == 0]
                    for S in pw[w]:
                        if all(G & S for G in rest_edges):
                            found = True; break
                    if found: break
                checked += 1
                if not found:
                    ok = False
                    print("THREE-HOST LEMMA FAILS", n, bin(E), part)
    print("Part 1: three-host lemma verified on", checked, "(family, edge, partition) instances; ok =", ok)
    # ---------------- Part 2
    bad_ok, built = 0, 0
    for _ in range(400):
        n = random.randint(7, 10)
        k = random.randint(4, n - 2)
        H = list({sum(1 << v for v in random.sample(range(n), random.randint(max(2, k - 2), k)))
                  for _ in range(random.randint(8, 30))})
        full = (1 << n) - 1
        for E in H:
            if popcount(E) < 4: continue
            qs = quartering(E, n)
            pw = pairings(qs)
            for part in partitions3(full & ~E):
                chosen = []
                for w in 'xyz':
                    for S in pw[w]:
                        g = next((G for G in H if G & (part[w] | S) == 0), None)
                        chosen.append(g)
                if all(g is not None for g in chosen):
                    built += 1
                    tup = [E] + chosen
                    if two_pierceable(tup, n):
                        ok = False
                        print("CONSTRUCTED 7-TUPLE IS 2-PIERCEABLE", n, [bin(x) for x in tup])
                    else:
                        bad_ok += 1
                    break
    print("Part 2: built", built, "seven-tuples from satisfied partitions; not 2-pierceable:", bad_ok)
    print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
