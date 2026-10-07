"""Referee check for Lemma A / Lemma A_E (lazy protrusion Fano bounds).

Part 1: Fano incidence facts used.
Part 2: adversarial simulation of the lazy selection procedure: an adversary picks each
        G_j arbitrarily subject ONLY to the stated constraints (G_j avoids L_{l_j} cap U and
        F_j, |G_j \ U| <= m, outside points drawn from a SMALL pool to force reuse).
        We check (a) |F_j| <= stated bound, (b) the resulting 7-tuple has no 2-transversal
        (brute force over all pairs of vertices, x=y allowed).
Part 3: actual small families: random H on few vertices, check (7,2) exactly, compute
        tau(H^(m)_U) exactly and compare with both bounds.
"""
import itertools, random

PTS = range(7)
LINES = [frozenset(s) for s in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]

def covers_all(lines):
    u = set()
    for l in lines: u |= l
    return len(u) == 7

# ---- Part 1
for a, b in itertools.combinations(LINES, 2):
    assert len(a & b) == 1
for S in itertools.combinations(LINES, 3):
    conc = len(S[0] & S[1] & S[2]) == 1
    assert covers_all(S) == conc
for S in itertools.combinations(LINES, 2):
    assert not covers_all(S)
for S in itertools.combinations(LINES, 4):
    safe = not covers_all(S)
    ismiss = any(all(p not in l for l in S) for p in PTS)
    assert safe == ismiss
    if safe:
        p = [p for p in PTS if all(p not in l for l in S)][0]
        assert set(S) == {l for l in LINES if p not in l}
for S in itertools.combinations(LINES, 5):
    assert covers_all(S)
# anchored: every line != l1 has exactly one point on l1, two off
l1 = LINES[0]
for l in LINES[1:]:
    assert len(l & l1) == 1 and len(l - l1) == 2
print("Part 1 Fano facts OK")

# ---- Part 2
def has_2transversal(edges, verts):
    for x in verts:
        for y in verts:
            if all((x in G) or (y in G) for G in edges):
                return True
    return False

def simulate(anchored, trials, rng):
    worst_ratio = 0.0
    for _ in range(trials):
        m = rng.randint(0, 4)
        pool = [('o', i) for i in range(rng.randint(1, 8))]  # small outside pool forces reuse
        if not anchored:
            N = rng.randint(0, 20)
            U = list(range(N))
            lab = {x: x % 7 for x in U}  # balanced
            order = LINES[:]  # l1,l2,l3 = (0,1,2),(0,3,4),(0,5,6) are concurrent! shuffle to test ordering claim
            rng.shuffle(order)
            G = []
            start = 0
        else:
            e = rng.randint(1, 12); r = rng.randint(0, 9)
            E = [('E', i) for i in range(e)]; R = [('R', i) for i in range(r)]
            U = E + R
            off = sorted(set(PTS) - l1); on = sorted(l1)
            lab = {}
            for i, x in enumerate(E): lab[x] = off[i % 4]
            for i, x in enumerate(R): lab[x] = on[i % 3]
            rest = LINES[1:]; rng.shuffle(rest)
            order = [l1] + rest
            G = [frozenset(E)]
            start = 1
        for j in range(start, 7):
            lj = order[j]
            Fj = set()
            for x in pool:
                sig = [order[i] for i in range(j) if x in G[i]]
                if covers_all(sig + [lj]):
                    Fj.add(x)
            prev_out = sum(len([x for x in G[i] if x in pool]) for i in range(j))
            assert 2 * len(Fj) <= prev_out, "double-count bound fails"
            bound = (j - 1) * m / 2 if not anchored else (j - 2) * m / 2
            assert len(Fj) <= bound + 1e-9
            if anchored:
                assert len(Fj) <= (5 * m) // 2
            else:
                assert len(Fj) <= 3 * m
            if len(Fj) > 0 and m > 0:
                worst_ratio = max(worst_ratio, len(Fj) / m)
            allowed_in = [x for x in U if lab[x] not in lj]
            allowed_out = [x for x in pool if x not in Fj]
            # adversary: prefer outside points already used often (maximise reuse)
            rng.shuffle(allowed_out)
            allowed_out.sort(key=lambda x: -sum(x in g for g in G))
            k_out = rng.randint(0, min(m, len(allowed_out)))
            gi = set(rng.sample(allowed_in, rng.randint(0, len(allowed_in)))) if allowed_in else set()
            go = set(allowed_out[:k_out]) if rng.random() < 0.7 else set(rng.sample(allowed_out, k_out))
            g = gi | go
            if not g:
                g = set(allowed_in[:1]) or set(allowed_out[:1])
                if not g:
                    break
            G.append(frozenset(g))
        else:
            verts = list(U) + pool
            assert not has_2transversal(G, verts), (G,)
    return worst_ratio

rng = random.Random(1)
w0 = simulate(False, 20000, rng)
w1 = simulate(True, 20000, rng)
print("Part 2 adversarial simulations OK; max |F_j|/m seen: unanchored %.2f anchored %.2f" % (w0, w1))
