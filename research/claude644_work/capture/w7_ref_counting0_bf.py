#!/usr/bin/env python3
"""w7_ref_counting0_bf.py -- referee (w7, claim counting#0) INDEPENDENT brute force of the seven-row lemma.
No shared library.  For random / structured small families H (bitmasks on V=range(n)):
  * (7,2) decided exactly: every 7-multiset of edges has a nonempty pair set Pi (pairs of DISTINCT points of V
    meeting every row) -- equivalent to (7,2) when |V|>=2.
  * ALL lex (|P7|,|Pi7|)-minimising 7-multisets are enumerated (as tuples; order irrelevant for the lemma's
    quantities because each i is treated).
  * for EVERY minimiser: (a) W_i u {u,v} transversal for all i, all uv in Pi7; (b) 7t <= sum(|W_i|+delta_i);
    (c) exact identity 4*sum|W_i| = 3*sum|F_i| + D7 and q(v) <= 7-d(v); (d) if hypothesis (every v in some W_i
    has d(v)>=4) holds then t <= 3k/4+2 (k = max edge size);  also the refined hypothesis 4q(v)<=3d(v) for all v.
  * mutation: with a NON-minimal tuple (random) or minimising |P7| only / |Pi7| only, count (a) failures to show
    the checker is sensitive.
Usage: python3 w7_ref_counting0_bf.py SEED NFAM
"""
import itertools, random, sys
from fractions import Fraction

def pairs_of(rows, n):
    out = []
    for x in range(n):
        bx = 1 << x
        for y in range(x + 1, n):
            m = bx | (1 << y)
            ok = True
            for F in rows:
                if not (F & m): ok = False; break
            if ok: out.append((x, y))
    return out

def is_transversal(X, H):
    return all(E & X for E in H)

def tau(H, n):
    for s in range(n + 1):
        for S in itertools.combinations(range(n), s):
            X = sum(1 << v for v in S)
            if is_transversal(X, H): return s
    return None

def quantities(R, n, Pi):
    Pis = set(Pi)
    W = []
    for i in range(7):
        Gi = pairs_of(R[:i] + R[i + 1:], n)
        Ai = [pr for pr in Gi if pr not in Pis]
        W.append(set(x for pr in Ai for x in pr))
    return W

def analyse(H, n, R, Pi, t, k, stats, tag):
    W = quantities(R, n, Pi)
    bad_a = 0
    for i in range(7):
        # side fact: W_i disjoint from F_i
        assert not any((R[i] >> v) & 1 for v in W[i]), ('W_i meets F_i', tag)
        for (u, v) in Pi:
            X = sum(1 << z for z in (W[i] | {u, v}))
            if not is_transversal(X, H): bad_a += 1
    if tag != 'min':
        return bad_a
    assert bad_a == 0, ('(a) FAIL', H, R)
    delta = [min(len({u, v} - W[i]) for (u, v) in Pi) for i in range(7)]
    assert 7 * t <= sum(len(W[i]) + delta[i] for i in range(7)), ('(b) FAIL', H, R)
    d = [sum((F >> v) & 1 for F in R) for v in range(n)]
    q = [sum(1 for i in range(7) if v in W[i]) for v in range(n)]
    assert all(q[v] <= 7 - d[v] for v in range(n))
    D7 = sum(4 * q[v] - 3 * d[v] for v in range(n))
    sF = sum(bin(F).count('1') for F in R)
    assert 4 * sum(len(w) for w in W) == 3 * sF + D7
    assert 28 * t <= 3 * sF + D7 + 4 * sum(delta)
    hyp = all(d[v] >= 4 for v in range(n) if q[v] > 0)
    hyp2 = all(4 * q[v] <= 3 * d[v] for v in range(n))
    if hyp: assert hyp2
    if hyp2:
        assert Fraction(t) <= Fraction(3 * k, 4) + 2, ('(d) FAIL', H, R)
        stats['hyp2'] += 1
    if hyp: stats['hyp'] += 1
    stats['min'] += 1
    stats['checks'] += 7 * len(Pi)
    return 0

def run_family(H, n, stats, rng):
    H = sorted(set(H))
    k = max(bin(E).count('1') for E in H)
    best = None; mins = []
    allkeys = []
    for F in itertools.combinations_with_replacement(range(len(H)), 7):
        R = [H[j] for j in F]
        Pi = pairs_of(R, n)
        if not Pi: return False     # not (7,2)
        P = set(x for pr in Pi for x in pr)
        key = (len(P), len(Pi))
        allkeys.append((key, F))
        if best is None or key < best: best = key; mins = [(R, Pi)]
        elif key == best: mins.append((R, Pi))
    t = tau(H, n)
    stats['fam'] += 1; stats['tmax'] = max(stats['tmax'], t)
    for (R, Pi) in mins:
        analyse(H, n, R, Pi, t, k, stats, 'min')
    # mutations
    minP = min(kk[0] for kk, F in allkeys)
    for label, cands in (('Ponly', [F for kk, F in allkeys if kk[0] == minP]),
                         ('rand', [F for kk, F in rng.sample(allkeys, min(40, len(allkeys)))])):
        for F in cands[:40]:
            R = [H[j] for j in F]; Pi = pairs_of(R, n)
            stats['mut_' + label] += analyse(H, n, R, Pi, t, k, stats, label) > 0
            stats['mut_' + label + '_n'] += 1
    return True

def rand_family(rng):
    kind = rng.random()
    if kind < 0.25:   # complete k-uniform on n < 7k/4 (+ maybe a padding edge)
        k = rng.randint(2, 4); n = rng.randint(k + 1, max(k + 1, (7 * k) // 4 - 1 + (1 if rng.random() < .3 else 0)))
        if n > 8: n = 8
        H = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)]
        if len(H) > 14: H = rng.sample(H, 14)
        return H, n
    n = rng.randint(4, 9); k = rng.randint(2, 5); m = rng.randint(3, 11)
    H = [sum(1 << v for v in rng.sample(range(n), rng.randint(1, min(k, n)))) for _ in range(m)]
    return H, n

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    NF = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rng = random.Random(seed)
    from collections import Counter
    stats = Counter(); stats['tmax'] = 0
    tries = 0
    while stats['fam'] < NF:
        tries += 1
        H, n = rand_family(rng)
        if len(set(H)) > 13: continue
        run_family(H, n, stats, rng)
    print('seed', seed, 'tries', tries, dict(stats))
    print('ALL (a)-(d) CHECKS PASS on every minimiser')
