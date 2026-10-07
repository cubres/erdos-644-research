"""Referee w7 core#2 BREAK-IT (B1): exact adversarial end-to-end test of the Theorem L recipe on NON-UNIFORM
families (mixed sizes, including edges much larger than tau -- the 'rank-free' regime) with max codegree lam and
tau >= 3lam+1.  For sampled 4-tuples of DISTINCT edges, all 3! matching orders, and EVERY admissible choice of
G5 (avoids I5), g in G5, G6 (avoids I6+{g}), G7 (avoids I7 + (G5&G6)) -- up to a cap -- verify:
  sizes of avoided sets <= 3lam <= tau-1, G6 != G5, and the 7 edges have NO 2-point transversal (brute force).
Part 2 (statement test inside known (7,2) families): random subfamilies of K_n^k (n < 7k/4 verified (7,2) by brute
force for the small cases used) with pairwise intersections <= lam: record max tau/lam; must be <= 3."""
import itertools, random, sys
pc = lambda x: bin(x).count('1')
def tau(H, n):
    for s in range(n+1):
        for T in itertools.combinations(range(n), s):
            tm = sum(1 << v for v in T)
            if all(E & tm for E in H): return s
def has2(G, n):
    return any(all(E & ((1 << x) | (1 << y)) for E in G) for x in range(n) for y in range(x, n))
M = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
def e2e(H, n, lam, t, rnd, nq, cap):
    cnt = 0
    for _ in range(nq):
        G = rnd.sample(H, 4)
        I = [(G[a] & G[b]) | (G[c] & G[d]) for ((a,b),(c,d)) in M]
        for o in itertools.permutations(range(3)):
            I5, I6, I7 = (I[o[0]], I[o[1]], I[o[2]])
            assert max(pc(I5), pc(I6), pc(I7)) <= 2*lam <= t-1
            C5 = [E for E in H if not E & I5]; assert C5
            for G5 in rnd.sample(C5, min(cap, len(C5))):
                for g in [v for v in range(n) if G5 >> v & 1]:
                    Z6 = I6 | (1 << g); assert pc(Z6) <= 3*lam <= t-1
                    C6 = [E for E in H if not E & Z6]; assert C6
                    for G6 in rnd.sample(C6, min(cap, len(C6))):
                        assert G6 != G5 and pc(G5 & G6) <= lam
                        Z7 = I7 | (G5 & G6); assert pc(Z7) <= 3*lam <= t-1
                        C7 = [E for E in H if not E & Z7]; assert C7
                        for G7 in rnd.sample(C7, min(cap, len(C7))):
                            assert not has2(G + [G5, G6, G7], n); cnt += 1
    return cnt
def randfam(rnd):
    n = rnd.randint(7, 13); lam = rnd.randint(1, 2)
    cand = [sum(1 << v for v in c) for s in range(1, n+1) for c in itertools.combinations(range(n), s)
            if s <= 3 or rnd.random() < 0.02]
    rnd.shuffle(cand)
    # bias towards big edges (rank >> tau)
    cand.sort(key=lambda e: -pc(e) * rnd.random())
    H = []
    for E in cand:
        if all(pc(E & F) <= lam for F in H): H.append(E)
    return H, n, lam
if __name__ == '__main__':
    seed = int(sys.argv[1]); N = int(sys.argv[2]); rnd = random.Random(seed)
    fams = tot = 0; bigrank = 0
    while fams < N:
        H, n, lam = randfam(rnd)
        if len(H) < 4: continue
        t = tau(H, n)
        if t < 3*lam + 1: continue
        k = max(pc(E) for E in H)
        if k > 4*lam: bigrank += 1
        tot += e2e(H, n, lam, t, rnd, 20, 3); fams += 1
    print(f"PART1 PASS seed={seed}: {fams} non-uniform families with tau>=3lam+1 ({bigrank} with rank>4lam), {tot} adversarial 7-tuples, none 2-pierceable", flush=True)
    # PART 2
    best = {}
    for (n, k) in [(5,3),(6,4),(7,5),(8,5),(9,6),(10,6),(11,7),(12,7)]:
        assert n < 7*k/4
        allE = [sum(1 << v for v in c) for c in itertools.combinations(range(n), k)]
        for rep in range(200):
            lam = rnd.randint(1, k-1); rnd.shuffle(allE); H = []
            for E in allE:
                if all(pc(E & F) <= lam for F in H): H.append(E)
            if len(H) < 2: continue
            lam_act = max(pc(a & b) for a, b in itertools.combinations(H, 2))
            t = tau(H, n)
            if lam_act >= 1:
                assert t <= 3*lam_act, (n, k, H)
                r = t / lam_act
                if r > best.get((n, k), (0,))[0]: best[(n, k)] = (r, t, lam_act, len(H))
    print("PART2 PASS (subfamilies of K_n^k, n<7k/4, FKW-(7,2)): max tau/lam per (n,k):", best, flush=True)
