#!/usr/bin/env python3
"""w7_ref_counting2_bf.py -- referee w7, claim counting#2 (LINE-BY-LINE lens).
Independent brute force (no shared library) of the "union-bound" form of Lemma 7.92.
Ground set V = union of H (as in note 7.91).  For every lex(|P|,|Pi|)-minimising six-multiset of edges:
  T1  W_i subset U\\F_i  holds  iff  NOT (some degree-5 vertex missing row i AND V != U)   [exact iff]
  T2  P subset U          holds  iff  NOT (common point AND V != U)
  T3  if W_i subset U: t <= |U|-|F_i|+2 ; also record whether t <= |U|-|F_i|+2 ever FAILS when W_i not in U
  T4  under the degree hypothesis (noneligible v in U: d>=3; eligible v: d>=4) and P,W_i subset U:
      sum|F_i| >= 3|U|+p  and  t <= 3k/4+3/2  (k = max edge size);  record whether hypothesis ever holds
  T5  exact identity sum|W_i| + 2p = sum|F_i| + D  (the 7.92 bookkeeping), and D computed.
Usage: python3 w7_ref_counting2_bf.py SEED NFAM
"""
import itertools, random, sys
from fractions import Fraction

def pc(x): return bin(x).count('1')

def pairs_of(rows, n):
    out = []
    for x in range(n):
        for y in range(x + 1, n):
            m = (1 << x) | (1 << y)
            if all(F & m for F in rows): out.append((x, y))
    return out

def tau(H, n):
    for s in range(n + 1):
        for S in itertools.combinations(range(n), s):
            X = sum(1 << v for v in S)
            if all(E & X for E in H): return s

def analyse(H, n, R, Pi, t, k, st):
    Vmask = 0
    for E in H: Vmask |= E
    U = 0
    for F in R: U |= F
    Pis = set(Pi)
    P = set(x for pr in Pi for x in pr)
    Pm = sum(1 << x for x in P)
    d = [sum((F >> v) & 1 for F in R) for v in range(n)]
    verts = [v for v in range(n) if (Vmask >> v) & 1]
    deg6 = any(d[v] == 6 for v in verts)
    VeqU = (U == Vmask)
    W = []
    for i in range(6):
        Ai = [pr for pr in pairs_of(R[:i] + R[i + 1:], n) if pr not in Pis]
        W.append(sum((1 << x) | (1 << y) for (x, y) in Ai))
    # T2
    PinU = (Pm & ~U) == 0
    assert PinU == (not (deg6 and not VeqU)), ('T2', R)
    st['T2'] += 1
    for i in range(6):
        assert W[i] & R[i] == 0
        deg5_i = any(d[v] == 5 and not (R[i] >> v) & 1 for v in verts)
        inU = (W[i] & ~U) == 0
        assert inU == (not (deg5_i and not VeqU)), ('T1', R, i)
        st['T1'] += 1
        delta = min(len({u, v} - set(x for x in range(n) if (W[i] >> x) & 1)) for (u, v) in Pi)
        assert t <= pc(W[i]) + delta, ('7.91', R)
        ub = pc(U) - pc(R[i]) + 2
        if inU:
            assert t <= ub, ('T3', R, i); st['T3'] += 1
        else:
            st['T3_outside'] += 1
            if t > ub: st['T3_fail_outside'] += 1
    # T5 identity
    q = [sum((W[i] >> v) & 1 for i in range(6)) for v in range(n)]
    D = sum(q[v] + 2 * ((Pm >> v) & 1) - d[v] for v in verts)
    sF = sum(pc(F) for F in R)
    assert sum(pc(w) for w in W) + 2 * len(P) == sF + D
    # T4
    hyp = all((d[v] >= 4) if (Pm >> v) & 1 else (d[v] >= 3) for v in verts if ((U | Pm) >> v) & 1)
    allW_inU = all((w & ~U) == 0 for w in W)
    if hyp and PinU and allW_inU:
        st['T4_hyp'] += 1
        assert sF >= 3 * pc(U) + len(P)
        assert len(P) >= t
        assert Fraction(t) <= Fraction(3 * k, 4) + Fraction(3, 2), ('T4', R)
        if not VeqU: st['T4_hyp_outside'] += 1
    return D

def run_family(H, n, st):
    H = sorted(set(H))
    k = max(pc(E) for E in H)
    best = None; mins = []
    for F in itertools.combinations_with_replacement(range(len(H)), 6):
        R = [H[j] for j in F]
        Pi = pairs_of(R, n)
        if not Pi: return False
        P = set(x for pr in Pi for x in pr)
        key = (len(P), len(Pi))
        if best is None or key < best: best = key; mins = [(R, Pi)]
        elif key == best: mins.append((R, Pi))
    # (7,2): every 7-multiset has a pair -- enough: every minimiser's P is a transversal is implied; check 7-sets directly
    for F in itertools.combinations_with_replacement(range(len(H)), 7):
        if not pairs_of([H[j] for j in F], n): return False
    t = tau(H, n)
    st['fam'] += 1; st['tmax'] = max(st['tmax'], t)
    for (R, Pi) in mins:
        analyse(H, n, R, Pi, t, k, st); st['min'] += 1
    return True

def rand_family(rng):
    r = rng.random()
    n = rng.randint(4, 8)
    if r < 0.3:   # sub-family of complete + a few extra (outside) edges
        k = rng.randint(2, 4); m = min(n, max(k + 1, (7 * k) // 4 - 1))
        H = [sum(1 << v for v in S) for S in itertools.combinations(range(m), k)]
        H = rng.sample(H, min(len(H), 9))
        for _ in range(rng.randint(0, 3)):
            H.append(sum(1 << v for v in rng.sample(range(n), rng.randint(1, k))))
        return H, n
    k = rng.randint(2, 5); m = rng.randint(3, 10)
    H = [sum(1 << v for v in rng.sample(range(n), rng.randint(1, min(k, n)))) for _ in range(m)]
    return H, n

if __name__ == '__main__':
    seed = int(sys.argv[1]); nf = int(sys.argv[2])
    rng = random.Random(seed)
    from collections import Counter
    st = Counter(); st['tmax'] = 0
    tries = 0
    while st['fam'] < nf:
        tries += 1
        H, n = rand_family(rng)
        run_family(H, n, st)
    print('tries', tries, dict(st))
