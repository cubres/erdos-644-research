"""Referee w7, claim core#2 (Theorem L).  Independent checks of the proof, written from scratch.
(a) Type logic: points have membership types T subset {1..7}.  Constraints of the Theorem-L schedule:
    for each matching mu_r (r=5,6,7) of {1,2,3,4} and each pair {i,j} in mu_r: {i,j} <= T  =>  r notin T;
    and {5,6,7} not <= T.  Claim: no two allowed types cover {1..7}.  Also: each single constraint is needed.
(b) End-to-end, ADVERSARIAL: random bounded-intersection families (non-uniform) with tau >= 3lam+1.
    For random distinct G1..G4, every matching order, EVERY edge G5 avoiding I5 (repeats of G1..G4 allowed),
    EVERY g in G5, EVERY G6 avoiding I6+{g}, EVERY G7 avoiding I7+(G5&G6): the 7 edges have no 2-transversal,
    and all avoided sets have size <= 3lam.  Independent of w6_core_*.
"""
import itertools, random, sys
MATCH = [((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3))]

def allowed_types(match_rows, drop=None):
    out = []
    for m in range(128):
        T = {i+1 for i in range(7) if m >> i & 1}
        ok = True
        for ci, (mu, r) in enumerate(zip(match_rows, (5, 6, 7))):
            for (i, j) in mu:
                if drop == (ci, (i, j)): continue
                if i in T and j in T and r in T: ok = False
        if drop != 'core' and {5, 6, 7} <= T: ok = False
        if ok: out.append(frozenset(T))
    return out

def covering_pair(types):
    full = frozenset(range(1, 8))
    for A in types:
        for B in types:
            if A | B == full: return (sorted(A), sorted(B))
    return None

def part_a():
    for perm in itertools.permutations(MATCH):
        assert covering_pair(allowed_types(perm)) is None
    drops = [(ci, p) for ci in range(3) for p in MATCH[ci]] + ['core']
    for d in drops:
        cp = covering_pair(allowed_types(MATCH, d))
        assert cp is not None, d
    print("(a) type logic PASS (all 6 orders); each of the 7 constraints necessary")

def tau_at_least(H, V, t):
    # True iff no set of size <= t-1 meets all edges
    for s in range(t):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(E & Ts for E in H): return False
    return True

def has2(G, V):
    return any(all((x in E) or (y in E) for E in G) for x in V for y in V)

def e2e(H, V, lam, rnd, nquad):
    cnt = 0
    for _ in range(nquad):
        G = rnd.sample(H, 4)
        I = [set().union(*[G[a-1] & G[b-1] for (a, b) in mu]) for mu in MATCH]
        for o in itertools.permutations(range(3)):
            I5, I6, I7 = I[o[0]], I[o[1]], I[o[2]]
            assert len(I5) <= 2*lam and len(I6) <= 2*lam and len(I7) <= 2*lam
            C5 = [E for E in H if not (E & I5)]; assert C5
            for G5 in C5:
                for g in G5:
                    C6 = [E for E in H if not (E & (I6 | {g}))]; assert C6
                    for G6 in C6:
                        assert G6 != G5 and len(G5 & G6) <= lam
                        Z = I7 | (G5 & G6); assert len(Z) <= 3*lam
                        C7 = [E for E in H if not (E & Z)]; assert C7
                        for G7 in C7:
                            assert not has2(G + [G5, G6, G7], V)
                            cnt += 1
    return cnt

def part_b(nfam, seed):
    rnd = random.Random(seed); fams = 0; tot = 0; bylam = {}
    tries = 0
    while fams < nfam and tries < 200000:
        tries += 1
        lam = rnd.choice([1, 1, 2])
        n = rnd.randint(7, 11) if lam == 1 else rnd.randint(12, 15)
        V = list(range(n))
        sizes = list(range(2, 6)) if lam == 1 else list(range(3, 7))
        H = []
        for _ in range(4000):
            E = frozenset(rnd.sample(V, rnd.choice(sizes)))
            if E in H: continue
            if all(len(E & F) <= lam for F in H): H.append(E)
        if len(H) < 4 or not tau_at_least(H, V, 3*lam+1): continue
        fams += 1; bylam[lam] = bylam.get(lam, 0) + 1
        tot += e2e(H, V, lam, rnd, 3)
    print(f"(b) e2e PASS: {fams} families {bylam}, {tot} adversarial 7-tuples, all without 2-transversal")

if __name__ == '__main__':
    part_a()
    part_b(int(sys.argv[1]) if len(sys.argv) > 1 else 40, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
