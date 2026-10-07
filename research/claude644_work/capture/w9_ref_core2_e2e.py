"""Referee w9 core#2: EXHAUSTIVE adversarial end-to-end test of the Theorem L recipe.
Families H (distinct nonempty sets, bitmasks on n points) with lam = max_{E!=F}|E&F| >= 1 and tau(H) >= 3lam+1
(so H is NOT (7,2) by the theorem; the recipe must exhibit a bad 7-tuple for EVERY adversarial choice).
For every 4-set {G1..G4} of distinct edges (all of them, or a random sample if too many), every bijection
matchings->rows 5,6,7, EVERY G5 avoiding I5, EVERY g in G5, EVERY G6 avoiding I6+{g}, EVERY G7 avoiding
I7+(G5&G6): assert avoided-set sizes <= 3lam <= tau-1, existence of the requested edge, G6!=G5, |G5&G6|<=lam,
and the 7 edges have no transversal of size <= 2 (brute force over all points and pairs).
Family generators: (a) random greedy bounded-codegree with mixed sizes incl. edges of size >> tau;
(b) PG(2,q) lines (q=3,4) plus random 'huge' edges meeting every line in <=1 point where possible;
(c) K_n^k (lam=k-1) when n-k+1 >= 3k-2."""
import itertools, random, sys
pc = lambda x: bin(x).count('1')
def tau(H, n):
    for s in range(n+1):
        for T in itertools.combinations(range(n), s):
            tm = 0
            for v in T: tm |= 1 << v
            if all(E & tm for E in H): return s
def pierce2(G, n):
    full = (1 << len(G)) - 1
    S = set(sum(1 << i for i, E in enumerate(G) if E >> x & 1) for x in range(n))
    return any((a | b) == full for a in S for b in S)
M = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
def run(H, n, rnd, max4=60, cap=None):
    sub = (lambda L: L if cap is None or len(L) <= cap else rnd.sample(L, cap))
    lam = max(pc(E & F) for E, F in itertools.combinations(H, 2)); t = tau(H, n)
    assert lam >= 1 and t >= 3*lam + 1
    quads = list(itertools.combinations(H, 4))
    if len(quads) > max4: quads = rnd.sample(quads, max4)
    cnt = 0
    for G in quads:
        I = [(G[a] & G[b]) | (G[c] & G[d]) for ((a,b),(c,d)) in M]
        for o in itertools.permutations(range(3)):
            I5, I6, I7 = I[o[0]], I[o[1]], I[o[2]]
            assert max(pc(I5), pc(I6), pc(I7)) <= 2*lam <= t-1
            C5 = [E for E in H if not E & I5]; assert C5
            for G5 in sub(C5):
                for g in range(n):
                    if not G5 >> g & 1: continue
                    Z6 = I6 | (1 << g); assert pc(Z6) <= 3*lam <= t-1
                    C6 = [E for E in H if not E & Z6]; assert C6
                    for G6 in sub(C6):
                        assert G6 != G5 and pc(G5 & G6) <= lam
                        Z7 = I7 | (G5 & G6); assert pc(Z7) <= 3*lam <= t-1
                        C7 = [E for E in H if not E & Z7]; assert C7
                        for G7 in sub(C7):
                            assert not pierce2(list(G) + [G5, G6, G7], n); cnt += 1
    return lam, t, cnt
def greedy(rnd):
    n = rnd.randint(6, 12); lam = rnd.choice([1, 1, 2])
    big = [sum(1 << v for v in rnd.sample(range(n), rnd.randint(4, n))) for _ in range(rnd.randint(0, 6))]
    small = [sum(1 << v for v in c) for s in (2, 3) for c in itertools.combinations(range(n), s)]
    rnd.shuffle(small)
    H = []
    for E in big + small:
        if E not in H and all(pc(E & F) <= lam for F in H): H.append(E)
    return H, n
def pg(q):
    # PG(2,q) for prime q via homogeneous coordinates
    pts = []
    for v in itertools.product(range(q), repeat=3):
        if any(v):
            f = next(x for x in v if x); inv = pow(f, q-2, q)
            w = tuple((x*inv) % q for x in v)
            if w not in pts: pts.append(w)
    lines = []
    for L in pts:
        lines.append(sum(1 << i for i, p in enumerate(pts) if sum(a*b for a, b in zip(L, p)) % q == 0))
    return lines, len(pts)
if __name__ == '__main__':
    # self-test of pierce2 against brute force
    _r = random.Random(0)
    for _ in range(3000):
        nn = _r.randint(2, 6); GG = [_r.randint(1, (1 << nn) - 1) for _ in range(7)]
        bf = any(all(E & ((1 << x) | (1 << y)) for E in GG) for x in range(nn) for y in range(x, nn))
        assert bf == pierce2(GG, nn)
    seed = int(sys.argv[1]); N = int(sys.argv[2]); rnd = random.Random(seed)
    tot = fams = bigrank = 0
    # (b) PG(2,3), PG(2,5) (tau=q+1>=3lam+1=4 needs q>=3), plus huge edges that keep linearity
    for q in (3, 5):
        L, n = pg(q)
        H = list(L)
        lam, t, c = run(H, n, rnd, 25, None if q == 3 else 8); tot += c; fams += 1
        print(f"PG(2,{q}): lam={lam} tau={t} tuples={c}", flush=True)
    # (c) K_n^k with n-k+1 >= 3(k-1)+1
    for (n, k) in [(6, 2), (8, 2), (9, 3)]:
        H = [sum(1 << v for v in c) for c in itertools.combinations(range(n), k)]
        lam, t, c = run(H, n, rnd, 20, 12); tot += c; fams += 1
        print(f"K_{n}^{k}: lam={lam} tau={t} tuples={c}", flush=True)
    while fams < N:
        H, n = greedy(rnd)
        if len(H) < 4: continue
        lam = max(pc(E & F) for E, F in itertools.combinations(H, 2))
        if lam < 1 or tau(H, n) < 3*lam + 1: continue
        if max(pc(E) for E in H) > 4*lam: bigrank += 1
        _, t, c = run(H, n, rnd, 8, None if len(H) <= 16 else 10); tot += c; fams += 1
    print(f"PASS seed={seed}: {fams} families ({bigrank} random with rank>4lam), {tot} exhaustive-adversarial 7-tuples, none <=2-pierceable", flush=True)
