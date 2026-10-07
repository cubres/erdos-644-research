"""EXACT certificate for Lemma Q (dual pencil / quadrilateral lemma).  Pure integer/set arithmetic.

LEMMA Q.  H a family of nonempty sets, rank <= k, tau(H) = t.  G1..G4 in H (not nec. distinct).
For a perfect matching mu = {ij, kl} of {1,2,3,4} put I(mu) = (Gi & Gj) | (Gk & Gl).  Let
(mu5, mu6, mu7) be the three perfect matchings in any order, I_j = I(mu_j).  If
      |I5|, |I6|, |I7| <= t-1   and   |I6| + |I7| <= 2t - k - 2,
then H contains seven edges with no transversal of size <= 2.
Construction: G5 avoids I5; Y = any min(|G5\\I6|, t-1-|I6|) points of G5\\I6; G6 avoids I6 u Y;
G7 avoids I7 u (G5 & G6)  (|G5&G6| <= max(0,k-t+1+|I6|)).

PART 1 (logic, exhaustive): the set of vertex types forced by the construction,
   Allowed = { T subset [7] : for each pair {i,j} subset T&[4], row 4+m(ij) notin T;  {4,5} subset T => 6 notin T }
(rows 0..3 = G1..G4, rows 4,5,6 = G5,G6,G7, m(ij) = index of the matching containing ij), has no two
members (equal allowed) whose union is [7].  Checked for all 6 orders of the matchings.
Also: removing any one of the constraint families creates a covering pair (all constraints needed).
PART 2 (end-to-end): random small families; whenever the numerical hypotheses hold for some 4-tuple and
order, the seven edges are constructed explicitly inside H by the recipe and checked to have no 2-transversal.
"""
import itertools, random, sys

MATCH = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]

def allowed_types(order, drop=None):
    # order: permutation of range(3); row 4+j serves matching MATCH[order[j]]
    rowof = {}
    for j, mi in enumerate(order):
        for pr in MATCH[mi]:
            rowof[frozenset(pr)] = 4 + j
    out = []
    for T in range(128):
        S = [i for i in range(4) if T >> i & 1]
        ok = True
        for i, j in itertools.combinations(S, 2):
            r = rowof[frozenset((i, j))]
            if drop == ('pair', r):
                continue
            if T >> r & 1: ok = False
        if drop != 'G7' and (T >> 4 & 1) and (T >> 5 & 1) and (T >> 6 & 1): ok = False
        if ok: out.append(T)
    return out

def part1():
    for order in itertools.permutations(range(3)):
        A = allowed_types(order)
        for T1 in A:
            for T2 in A:
                assert T1 | T2 != 127, (order, T1, T2)
        # necessity of each constraint family
        for drop in [('pair', 4), ('pair', 5), ('pair', 6), 'G7']:
            A2 = allowed_types(order, drop)
            assert any(T1 | T2 == 127 for T1 in A2 for T2 in A2), (order, drop)
    print("PART 1 PASS: allowed-type system is pairwise non-covering for all 6 orders; every constraint needed")

# ---------------- PART 2 ----------------
def tau_exact(H, V):
    for s in range(0, len(V)+1):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(E & Ts for E in H): return s
    return None

def has_2transversal(G, V):
    for x in V:
        for y in V:
            if y < x: continue
            if all((x in g) or (y in g) for g in G): return True
    return False

def avoid(H, Z):
    for E in H:
        if not (E & Z): return E
    return None

def part2(trials=4000, seed=1):
    rnd = random.Random(seed)
    hits = 0; fams = 0
    for _ in range(trials):
        n = rnd.randint(5, 10)
        V = list(range(n))
        m = rnd.randint(4, 14)
        H = []
        k = rnd.randint(2, max(2, n-2))
        for _ in range(m):
            s = rnd.randint(1, k)
            H.append(frozenset(rnd.sample(V, s)))
        H = list(set(H))
        k = max(len(E) for E in H)
        t = tau_exact(H, V)
        fams += 1
        for quad in itertools.product(range(len(H)), repeat=4):
            if rnd.random() > 0.05: continue
            G = [H[i] for i in quad]
            I = [set().union(*[G[a] & G[b] for (a, b) in M]) for M in MATCH]
            for order in itertools.permutations(range(3)):
                I5, I6, I7 = I[order[0]], I[order[1]], I[order[2]]
                if not (len(I5) <= t-1 and len(I6) <= t-1 and len(I7) <= t-1 and len(I6)+len(I7) <= 2*t-k-2):
                    continue
                G5 = avoid(H, I5); assert G5 is not None
                pool = sorted(G5 - I6)
                Y = set(pool[:min(len(pool), t-1-len(I6))])
                G6 = avoid(H, I6 | Y); assert G6 is not None
                assert len(G5 & G6) <= max(0, k - t + 1 + len(I6))
                Z7 = I7 | (G5 & G6)
                assert len(Z7) <= t-1
                G7 = avoid(H, Z7); assert G7 is not None
                seven = G + [G5, G6, G7]
                assert not has_2transversal(seven, V), (H, quad, order)
                hits += 1
    print(f"PART 2 PASS: {fams} random families, {hits} (4-tuple, order) instances meeting the hypotheses;"
          f" every constructed 7-tuple lies in H and has no 2-transversal")

if __name__ == '__main__':
    part1()
    part2(int(sys.argv[1]) if len(sys.argv) > 1 else 4000)

# ---------------- PART 3: structured families with t <= k ----------------
def pg2(q):
    pts = []
    for a in range(q):
        for b in range(q): pts.append((a, b, 1))
    for a in range(q): pts.append((a, 1, 0))
    pts.append((1, 0, 0))
    lines = []
    for l in pts:
        lines.append(frozenset(i for i, P in enumerate(pts) if sum(x*y for x, y in zip(l, P)) % q == 0))
    return lines, list(range(len(pts)))

def run_family(H, V, t, k, name, sample=None, seed=3):
    rnd = random.Random(seed); hits = 0; tested = 0
    quads = itertools.product(range(len(H)), repeat=4)
    for quad in quads:
        if sample and rnd.random() > sample: continue
        G = [H[i] for i in quad]
        I = [set().union(*[G[a] & G[b] for (a, b) in M]) for M in MATCH]
        for order in itertools.permutations(range(3)):
            I5, I6, I7 = I[order[0]], I[order[1]], I[order[2]]
            if not (len(I5) <= t-1 and len(I6) <= t-1 and len(I7) <= t-1 and len(I6)+len(I7) <= 2*t-k-2):
                continue
            G5 = avoid(H, I5); pool = sorted(G5 - I6)
            Y = set(pool[:min(len(pool), t-1-len(I6))])
            G6 = avoid(H, I6 | Y)
            assert len(G5 & G6) <= max(0, k - t + 1 + len(I6))
            G7 = avoid(H, I7 | (G5 & G6)); assert G7 is not None
            assert not has_2transversal(G + [G5, G6, G7], V)
            hits += 1
            if hits >= 3000: break
        if hits >= 3000: break
    print(f"PART 3 {name}: t={t} k={k}: {hits} instances meeting hypotheses, all 7-tuples bad")

if __name__ == '__main__':
    for q in (5, 7):
        L, V = pg2(q)
        run_family(L, V, q+1, q+1, f"PG(2,{q})", sample=0.02)
    for n, k in ((9, 4), (10, 5), (12, 5), (14, 6)):
        V = list(range(n)); H = [frozenset(c) for c in itertools.combinations(V, k)]
        run_family(H, V, n-k+1, k, f"K_{n}^({k})", sample=0.0005)
