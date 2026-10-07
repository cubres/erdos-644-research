# Referee w9, claim randomside#2 (Theorem 1*): deterministic core of LEMMA F, tested end to end on small instances.
# Own Fano plane (lines of PG(2,2) from the difference set {1,2,4} mod 7 -- a different labelling from the attacker's).
# (1) safe sets: union of lines != all 7 points; count by size must be 1,7,21,28,7 (64).
# (2) random lazy construction: G_1..G_7 (k-subsets of [N]) with G_j avoiding F_j = {x: sigma_<j(x) u {l_j} unsafe} and
#     |G_j & G_i| <= m. Check: F_j subset of union of pairwise intersections of earlier G's; |F_j| <= 15m; the final
#     7-tuple has NO 2-point transversal (brute force over all pairs of [N]).
# (3) MUTATION: skip the F_j avoidance -> count how often the tuple becomes 2-pierceable (test power).
import itertools, random, sys
PTS = range(7)
LINES = [frozenset(((1+i) % 7, (2+i) % 7, (4+i) % 7)) for i in range(7)]
assert all(len(LINES[a] & LINES[b]) == 1 for a in range(7) for b in range(a+1, 7))
def safe(S):
    u = set()
    for l in S: u |= LINES[l]
    return len(u) < 7
cnt = {}
for r in range(8):
    for S in itertools.combinations(range(7), r):
        if safe(S): cnt[r] = cnt.get(r, 0) + 1
print("safe sets by size:", cnt, "total", sum(cnt.values()))
assert cnt == {0: 1, 1: 7, 2: 21, 3: 28, 4: 7}
def pierceable(G, N):
    for x in range(N):
        for y in range(x, N):
            if all(x in g or y in g for g in G): return True
    return False
def construct(N, k, m, order, rng, avoid=True, tries=4000):
    G = []
    for j, lj in enumerate(order):
        sigma = {x: [order[i] for i in range(j) if x in G[i]] for x in range(N)}
        F = {x for x in range(N) if not safe(sigma[x] + [lj])}
        U = set()
        for a in range(j):
            for b in range(a+1, j): U |= (G[a] & G[b])
        assert F <= U, "F_j not inside union of pairwise intersections"
        assert len(F) <= 15*m
        pool = [x for x in range(N) if (x not in F or not avoid)]
        for _ in range(tries):
            if len(pool) < k: return None
            K = frozenset(rng.sample(pool, k))
            if all(len(K & g) <= m for g in G): break
        else:
            return None
        G.append(K)
    return G
if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    stats = {"ok": 0, "fail_construct": 0, "pierce": 0, "mut_ok": 0, "mut_pierce": 0}
    for trial in range(600):
        k = rng.randint(3, 9); N = rng.randint(3*k, 8*k); m = rng.randint(1, k-1)
        order = list(range(7)); rng.shuffle(order)
        G = construct(N, k, m, order, rng)
        if G is None: stats["fail_construct"] += 1
        else:
            if pierceable(G, N): stats["pierce"] += 1; print("COUNTEREXAMPLE", N, k, m, order, [sorted(g) for g in G])
            else: stats["ok"] += 1
        Gm = construct(N, k, m, order, rng, avoid=False)
        if Gm is not None:
            if pierceable(Gm, N): stats["mut_pierce"] += 1
            else: stats["mut_ok"] += 1
    print(stats)
