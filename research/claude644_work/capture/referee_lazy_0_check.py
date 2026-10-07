#!/usr/bin/env python3
"""Independent referee check of Lemma A (unanchored lazy protrusion Fano bound)
and Lemma A_E (anchored version).  Written from scratch; does not import the
other pencil_* scripts.

Strategy (tau-free contrapositive): run the proof's algorithm on an ARBITRARY
finite family (no (7,2) assumed).  At step j we form A_j and look for an edge of
H^(m)_U avoiding A_j.  Either
  (a) no such edge exists -> A_j is a transversal of H^(m)_U, and we assert
      |A_j| <= claimed bound  (so tau(H^(m)_U) <= bound), or
  (b) all seven edges get chosen -> we assert the 7-tuple has NO transversal of
      size <= 2 (so H fails (7,2)).
We additionally assert the intermediate counting claims |F_j| <= floor((j-1)m/2)
(Lemma A) and |F_j| <= floor((j-2)m/2) (Lemma A_E), and that every vertex ends
with a safe line set.
Edge choices are random or adversarial (greedy maximising future F sizes).
"""
import itertools, random, sys

PTS = range(7)
LINES = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]

def check_fano():
    assert len(set(LINES)) == 7
    for p, q in itertools.combinations(PTS, 2):
        assert sum(1 for l in LINES if p in l and q in l) == 1
    for l, l2 in itertools.combinations(LINES, 2):
        assert len(l & l2) == 1
    # safe-set characterisation
    for r in range(8):
        for S in itertools.combinations(range(7), r):
            cov = set().union(*[LINES[i] for i in S]) if S else set()
            safe = len(cov) < 7
            if r <= 2:
                assert safe
            if r == 3:
                conc = len(LINES[S[0]] & LINES[S[1]] & LINES[S[2]]) == 1
                assert safe == (not conc)
            if r == 4:
                missing = [p for p in PTS if all(p not in LINES[i] for i in S)]
                assert safe == (len(missing) == 1)
            if r >= 5:
                assert not safe

def covers_all(line_idx_set):
    cov = set()
    for i in line_idx_set:
        cov |= LINES[i]
    return len(cov) == 7

def two_pierceable(edges):
    V = sorted(set().union(*edges))
    for x in V:
        if all(x in G for G in edges):
            return True
    for x, y in itertools.combinations(V, 2):
        if all((x in G) or (y in G) for G in edges):
            return True
    return False

def balanced_labels(points, fano_pts, rng):
    pts = list(points); rng.shuffle(pts)
    fp = list(fano_pts); rng.shuffle(fp)
    return {x: fp[i % len(fp)] for i, x in enumerate(pts)}

def run(H, U, m, line_order, lab, anchor, rng, greedy):
    """line_order: list of 7 line indices; anchor: None or edge used as G_1."""
    Hm = [G for G in H if len(G - U) <= m]
    Lset = {i: frozenset(x for x in U if lab[x] in LINES[i]) for i in range(7)}
    chosen = []
    sig = {}  # outside vertex -> set of line indices so far
    Fsizes = []
    Asizes = []
    for j, li in enumerate(line_order, start=1):
        if j == 1 and anchor is not None:
            G = anchor
            assert not (G & Lset[li]), "anchor meets L_{l1}"
            assert G <= U
            Fsizes.append(0); Asizes.append(len(Lset[li]))
        else:
            F = frozenset(x for x, s in sig.items() if covers_all(s | {li}))
            A = Lset[li] | F
            Fsizes.append(len(F)); Asizes.append(len(A))
            pool = [G for G in Hm if not (G & A)]
            if not pool:
                return ('transversal', A, Fsizes, Asizes)
            if greedy:
                # adversarial: maximise number of outside vertices that become
                # 'loaded' (sigma size >= 2 afterwards), tie-break random
                def score(G):
                    return (sum(1 for x in G - U if len(sig.get(x, set())) >= 1), len(G - U), rng.random())
                G = max(pool, key=score)
            else:
                G = rng.choice(pool)
        chosen.append(G)
        for x in G - U:
            sig.setdefault(x, set()).add(li)
            assert not covers_all(sig[x]), "outside vertex became unsafe"
        for x in G & U:
            assert lab[x] not in LINES[li]
    return ('tuple', chosen, Fsizes, Asizes)

def gen(rng, m, anchored):
    N = rng.randint(0, 9)
    W = rng.randint(0, 12)
    U = frozenset(range(N))
    out = list(range(N, N + W))
    H = set()
    nE = rng.randint(5, 60)
    for _ in range(nE):
        a = rng.randint(0, N) if N else 0
        inside = rng.sample(range(N), a) if N else []
        b = rng.randint(0, min(W, m + rng.randint(0, 2)))
        outs = rng.sample(out, b) if W else []
        G = frozenset(inside) | frozenset(outs)
        if G:
            H.add(G)
    H = list(H)
    return N, U, out, H

def main(trials=40000, seed=1):
    rng = random.Random(seed)
    check_fano()
    stats = {'A_tuple': 0, 'A_trans': 0, 'AE_tuple': 0, 'AE_trans': 0, 'AE_skip': 0}
    maxF = {}
    for tr in range(trials):
        m = rng.randint(0, 3)
        greedy = rng.random() < 0.5
        # ---- Lemma A ----
        N, U, out, H = gen(rng, m, False)
        if H:
            lab = balanced_labels(U, PTS, rng)
            order = list(range(7)); rng.shuffle(order)   # no non-concurrency imposed
            bound = N - 4 * (N // 7) + 3 * m
            res = run(H, U, m, order, lab, None, rng, greedy)
            for j, f in enumerate(res[2], start=1):
                assert f <= ((j - 1) * m) // 2, (j, f, m)
                maxF[(m, j)] = max(maxF.get((m, j), 0), f)
            if res[0] == 'transversal':
                A = res[1]
                assert len(A) <= bound, (len(A), bound)
                assert all(G & A for G in H if len(G - U) <= m)
                stats['A_trans'] += 1
            else:
                assert not two_pierceable(res[1]), "Lemma A tuple is 2-pierceable!"
                stats['A_tuple'] += 1
        # ---- Lemma A_E ----
        N, U0, out, H = gen(rng, m, True)
        inside_edges = [G for G in H if G <= U0]
        if not inside_edges:
            stats['AE_skip'] += 1
            continue
        E = rng.choice(inside_edges)
        R = frozenset(x for x in U0 if x not in E and rng.random() < 0.8)
        U = E | R
        l1 = rng.randrange(7)
        off = [p for p in PTS if p not in LINES[l1]]
        lab = {}
        lab.update(balanced_labels(E, off, rng))
        lab.update(balanced_labels(R, sorted(LINES[l1]), rng))
        others = [i for i in range(7) if i != l1]; rng.shuffle(others)
        order = [l1] + others
        e, r = len(E), len(R)
        bound = 2 * (-(-e // 4)) + (-(-r // 3)) + (5 * m) // 2
        # claimed incidence: every other line has |L_l cap U| <= 2ceil(e/4)+ceil(r/3)
        for i in others:
            Li = [x for x in U if lab[x] in LINES[i]]
            assert len(Li) <= 2 * (-(-e // 4)) + (-(-r // 3))
        res = run(H, U, m, order, lab, E, rng, greedy)
        for j, f in enumerate(res[2], start=1):
            assert f <= max(0, ((j - 2) * m) // 2), (j, f, m)
        if res[0] == 'transversal':
            A = res[1]
            assert len(A) <= bound, (len(A), bound)
            stats['AE_trans'] += 1
        else:
            assert not two_pierceable(res[1]), "Lemma A_E tuple is 2-pierceable!"
            stats['AE_tuple'] += 1
    print(stats)
    print('max |F_j| observed (m,j)->', {k: v for k, v in sorted(maxF.items()) if v})

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40000)
