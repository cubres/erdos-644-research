"""Referee (wave 9) for core#7 'Lemma T (lazy tetrahedral dual pencil)'.
Independent of w6_core_lemmaT_logic.py.  Exact (integer/bitmask) arithmetic only.

Claim: G1..G4 edges, G1&G2&G3&G4 = empty, U_A = G1|..|G4,
  I5=(G1&G2)|(G3&G4), I6=(G1&G3)|(G2&G4), I7=(G1&G4)|(G2&G3);
  G5 avoids I5, G6 avoids I6, G7 avoids I7 | (G5&G6&U_A)  ==>  G1..G7 have no transversal of size <= 2.

Parts:
 (a) type-level check derived directly from the set hypotheses (per point: which rows contain it),
     all 6 assignments of matchings to rows 5,6,7; compare maximal allowed types with note Lemma 7.70 parent cells.
 (b) mutation tests: drop each hypothesis -> explicit counterexample (actual sets with a 2-transversal).
 (c) random actual set systems satisfying the hypotheses (ground sizes 4..12): brute-force 2-transversal check.
 (d) end-to-end consistency on (7,2) families: in K_9^(5) (tau=5) and K_12^(7) (all 7-subsets of 12 points,
     tau=6, (7,2)?) Lemma T must never be applicable with avoidance sets of size <= tau-1.
"""
import itertools, random

ROWS = 7
A = [0, 1, 2, 3]
MATCH = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]

def type_ok(T, order, core_rule=True, empty_common=True, pair_rules=(True, True, True)):
    """T: frozenset of rows containing a point.  order[j] = matching index assigned to row 4+j.
    Return True iff a point with type T is consistent with the hypotheses."""
    inA = [i for i in A if i in T]
    if empty_common and len(inA) == 4:
        return False
    for j in range(3):
        if not pair_rules[j]:
            continue
        in_I = any(a in T and b in T for (a, b) in MATCH[order[j]])
        if in_I and (4 + j) in T:          # G_{5+j} avoids I_{5+j}
            return False
    if core_rule and inA and {4, 5, 6} <= T:  # G7 avoids G5&G6&U_A
        return False
    return True

def all_types():
    for m in range(1 << ROWS):
        yield frozenset(i for i in range(ROWS) if m >> i & 1)

FULL = frozenset(range(ROWS))

def covering_pair(order, **kw):
    ok = [T for T in all_types() if type_ok(T, order, **kw)]
    for S in ok:
        for T in ok:
            if S | T == FULL:
                return S, T
    return None

def part_a():
    for order in itertools.permutations(range(3)):
        assert covering_pair(order) is None, order
        ok = [T for T in all_types() if type_ok(T, order)]
        maximal = {T for T in ok if not any(T < S for S in ok)}
        # note Lemma 7.70 parent cells: A-triples; B; e u (B \ {b}) with e in matching of b
        rowof = {order[j]: 4 + j for j in range(3)}
        parents = {frozenset(set(A) - {a}) for a in A} | {frozenset({4, 5, 6})}
        for mi in range(3):
            for e in MATCH[mi]:
                parents.add(frozenset(set(e) | ({4, 5, 6} - {rowof[mi]})))
        assert maximal == parents, (order, maximal ^ parents)
        assert len(parents) == 11
    print("(a) PASS: no covering pair for all 6 orders; maximal allowed types == note 7.70's 11 parent cells")

def realize(S, T):
    """Two points p (type S), q (type T): rows as sets over {0,1}; {p,q} is a 2-transversal iff S|T=FULL."""
    G = [set() for _ in range(ROWS)]
    for r in S: G[r].add(0)
    for r in T: G[r].add(1)
    return G

def has_2transversal(G, ground):
    pts = sorted(ground)
    for x in pts:
        for y in pts:
            if all((x in g) or (y in g) for g in G):
                return True
    return False

def check_hyp(G, order, core_rule=True, empty_common=True, pair_rules=(True, True, True)):
    UA = G[0] | G[1] | G[2] | G[3]
    if empty_common and (G[0] & G[1] & G[2] & G[3]):
        return False
    for j in range(3):
        if not pair_rules[j]:
            continue
        (a, b), (c, d) = MATCH[order[j]]
        I = (G[a] & G[b]) | (G[c] & G[d])
        if G[4 + j] & I:
            return False
    if core_rule and (G[6] & (G[4] & G[5] & UA)):
        return False
    return True

def part_b():
    order = (0, 1, 2)
    muts = {
        'no core rule (G7 avoids only I7)': dict(core_rule=False),
        'no empty-common-intersection': dict(empty_common=False),
        'G5 need not avoid I5': dict(pair_rules=(False, True, True)),
        'G6 need not avoid I6': dict(pair_rules=(True, False, True)),
        'G7 need not avoid I7': dict(pair_rules=(True, True, False)),
    }
    for name, kw in muts.items():
        cp = covering_pair(order, **kw)
        assert cp is not None, name
        S, T = cp
        G = realize(S, T)
        assert all(G)  # nonempty edges
        assert check_hyp(G, order, **kw) and not check_hyp(G, order)
        assert has_2transversal(G, {0, 1})
        print(f"(b) mutation '{name}': counterexample types {sorted(x+1 for x in S)} + {sorted(x+1 for x in T)}")
    # 'core rule restricted to U_A' is genuinely weaker than Lemma Q's G5&G6: witness where B-core lies outside U_A
    G = [set() for _ in range(ROWS)]
    # point 0 in G5,G6,G7 only (outside U_A); give A-rows other points
    for r in (4, 5, 6): G[r].add(0)
    G[0] |= {1, 2}; G[1] |= {1, 3}; G[2] |= {2, 3, 4}; G[3] |= {4, 5}
    assert check_hyp(G, order) and not has_2transversal(G, set(range(6)))
    print("(b) B-core outside U_A allowed (G5&G6&G7 = {0} not in U_A): hypotheses hold, no 2-transversal")

def part_c(trials=200000, seed=7):
    rnd = random.Random(seed)
    n_ok = 0
    for _ in range(trials):
        n = rnd.randint(4, 12)
        order = rnd.choice(list(itertools.permutations(range(3))))
        p = rnd.uniform(0.2, 0.8)
        G = [{v for v in range(n) if rnd.random() < p} for _ in range(4)]
        common = G[0] & G[1] & G[2] & G[3]
        for v in common:
            G[rnd.randrange(4)].discard(v)
        UA = G[0] | G[1] | G[2] | G[3]
        I = []
        for j in range(3):
            (a, b), (c, d) = MATCH[order[j]]
            I.append((G[a] & G[b]) | (G[c] & G[d]))
        q = rnd.uniform(0.3, 0.95)
        G5 = {v for v in range(n) if v not in I[0] and rnd.random() < q}
        G6 = {v for v in range(n) if v not in I[1] and rnd.random() < q}
        forb = I[2] | (G5 & G6 & UA)
        G7 = {v for v in range(n) if v not in forb and rnd.random() < q}
        GG = G + [G5, G6, G7]
        if not all(GG):
            continue
        assert check_hyp(GG, order)
        assert not has_2transversal(GG, set(range(n))), (GG, order)
        n_ok += 1
    print(f"(c) PASS: {n_ok} random actual 7-edge systems satisfying the hypotheses, none 2-pierceable")

def tau(edges, n):
    for s in range(n + 1):
        for S in itertools.combinations(range(n), s):
            Sset = set(S)
            if all(e & Sset for e in edges):
                return s

def part_d(n, k, samples, seed=1):
    rnd = random.Random(seed)
    edges = [frozenset(c) for c in itertools.combinations(range(n), k)]
    t = n - k + 1  # complete k-uniform on n points
    applicable = 0
    tried = 0
    for _ in range(samples):
        G = rnd.sample(edges, 4)
        if G[0] & G[1] & G[2] & G[3]:
            continue
        UA = G[0] | G[1] | G[2] | G[3]
        for order in itertools.permutations(range(3)):
            I = []
            for j in range(3):
                (a, b), (c, d) = MATCH[order[j]]
                I.append((G[a] & G[b]) | (G[c] & G[d]))
            if len(I[0]) > t - 1 or len(I[1]) > t - 1:
                continue
            c5 = [e for e in edges if not (e & I[0])]
            c6 = [e for e in edges if not (e & I[1])]
            for G5 in c5:
                for G6 in c6:
                    tried += 1
                    forb = I[2] | (G5 & G6 & UA)
                    if len(forb) <= n - k:  # some k-set avoids forb
                        applicable += 1
    return t, tried, applicable

if __name__ == '__main__':
    part_a()
    part_b()
    part_c()
    for (n, k, s) in [(9, 5, 3000), (7, 4, 3000), (12, 7, 8)]:
        t, tried, app = part_d(n, k, s)
        print(f"(d) K_{n}^({k}) tau={t}: {tried} (quad,order,G5,G6) choices, Lemma T applicable in {app}")

def part_e():
    """Unified Q/T statement: G5 avoids I5, G6 avoids I6, G7 avoids I7|(G5&G6&U_A), and
    EITHER G1&G2&G3&G4 = empty OR G5&G6&G7 subset U_A.  Second branch: types {1,2,3,4} allowed (with no B-row forced
    by the pair rules), types disjoint from A containing {5,6,7} forbidden.  Lemma Q is a special case."""
    for order in itertools.permutations(range(3)):
        ok = [T for T in all_types() if type_ok(T, order, empty_common=False)
              and not (not (T & set(A)) and {4, 5, 6} <= T)]
        assert frozenset(A) in ok
        assert not any(S | T == FULL for S in ok for T in ok), order
    print("(e) PASS: unified statement (empty 4-wise intersection OR B-core inside U_A) is sound for all orders")

if __name__ == '__main__':
    part_e()
