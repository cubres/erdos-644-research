#!/usr/bin/env python3
"""w7_ref_counting2_brk.py -- referee w7, claim counting#2, BREAK-IT lens.
Independent fast evaluator (coverage bitmasks), no shared library.
Families: random subfamilies of near-extremal complete K_n^k (tau up to 5) plus a few extra edges that
use OUTSIDE vertices (so V != U is possible), plus private-noise paddings.  (7,2) checked exactly
over all 7-multisets.  For EVERY lex(|P|,|Pi|) minimising six-multiset:
  L1 literal claim hypothesis: no degree-5 vertex, no degree-6 vertex, noneligible v in U d>=3, eligible d>=4
     => W_i subset U\\F_i for all i, P subset U, S>=3|U|+p, t<=|U|-|F_i|+2 all i, t<=3k/4+3/2  (exact Fractions)
  L2 7.92 literal hypothesis (all of V): t<=3k/4+3/2 and W_i,P subset U
  L3 claim's union bound t<=|U|-|F_i|+2 whenever only 'no degree 5' holds (common point allowed)
  L4 counterexample hunt: minimisers where degree-5 exists, V!=U, and t > |U|-|F_i|+2 for some i
Usage: python3 w7_ref_counting2_brk.py SEED NFAM"""
import itertools, random, sys
from fractions import Fraction
from collections import Counter

def pc(x): return bin(x).count('1')

def cov_masks(rows, verts):
    c = {}
    for v in verts:
        m = 0
        for j, F in enumerate(rows):
            if (F >> v) & 1: m |= 1 << j
        c[v] = m
    return c

def pairs(rows, verts):
    full = (1 << len(rows)) - 1
    c = cov_masks(rows, verts)
    out = []
    for a in range(len(verts)):
        x = verts[a]; cx = c[x]
        for b in range(a + 1, len(verts)):
            y = verts[b]
            if cx | c[y] == full: out.append((x, y))
    return out

def is72(H, verts):
    # every 7-multiset has a 2-point transversal; multisets reduce to sets of size <=7
    m = len(H)
    for r in range(1, min(7, m) + 1):
        for S in itertools.combinations(H, r):
            if not pairs(list(S), verts): return False
    return True

def tau(H, verts):
    for s in range(len(verts) + 1):
        for S in itertools.combinations(verts, s):
            X = sum(1 << v for v in S)
            if all(E & X for E in H): return s

def analyse(H, verts, R, Pi, t, k, st):
    Vm = sum(1 << v for v in verts)
    U = 0
    for F in R: U |= F
    P = 0
    for (x, y) in Pi: P |= (1 << x) | (1 << y)
    p = pc(P)
    Pis = set(Pi)
    d = {v: sum((F >> v) & 1 for F in R) for v in verts}
    W = []
    for i in range(6):
        w = 0
        for pr in pairs(R[:i] + R[i + 1:], verts):
            if pr not in Pis: w |= (1 << pr[0]) | (1 << pr[1])
        W.append(w)
    has5 = any(d[v] == 5 for v in verts); has6 = any(d[v] == 6 for v in verts)
    VeqU = (U == Vm)
    S = sum(pc(F) for F in R)
    ub = [pc(U) - pc(R[i]) + 2 for i in range(6)]
    # sanity: 7.91 part 1 bound
    Wsets = [set(v for v in verts if (w >> v) & 1) for w in W]
    for i in range(6):
        delta = min(len({u, v} - Wsets[i]) for (u, v) in Pi)
        assert t <= pc(W[i]) + delta, ('7.91', R)
    hypU = all((d[v] >= 4) if (P >> v) & 1 else (d[v] >= 3) for v in verts if (U >> v) & 1)
    hypV = all((d[v] >= 4) if (P >> v) & 1 else (d[v] >= 3) for v in verts)
    if not has5 and not has6 and hypU:
        st['L1_hyp'] += 1
        if not VeqU: st['L1_hyp_outside'] += 1
        if t >= 3: st['L1_hyp_t3'] += 1
        if t >= 3 and not VeqU: st['L1_hyp_t3_outside'] += 1
        assert all((w & ~U) == 0 and (w & R[i]) == 0 for i, w in enumerate(W)), ('L1 W', R)
        assert (P & ~U) == 0, ('L1 P', R)
        assert S >= 3 * pc(U) + p, ('L1 S', R)
        assert p >= t
        assert all(t <= b for b in ub), ('L1 ub', R)
        assert Fraction(t) <= Fraction(3 * k, 4) + Fraction(3, 2), ('L1 final', R, t, k)
        st['L1_maxslack_min'] = min(st.get('L1_maxslack_min', 99), Fraction(3 * k, 4) + Fraction(3, 2) - t)
    if hypV:
        st['L2_hyp'] += 1
        assert VeqU
        assert Fraction(t) <= Fraction(3 * k, 4) + Fraction(3, 2), ('L2', R)
    if not has5:
        st['L3'] += 1
        assert all(t <= b for b in ub), ('L3', R)
    if has5 and not VeqU:
        st['L4_cases'] += 1
        if any(t > b for b in ub):
            st['L4_unionbound_fails'] += 1
            if 'L4_example' not in st:
                st['L4_example'] = (t, pc(U), [pc(F) for F in R], [sorted(v for v in verts if (F >> v) & 1) for F in R])

def run_family(H, st):
    H = sorted(set(H))
    Vm = 0
    for E in H: Vm |= E
    verts = [v for v in range(Vm.bit_length()) if (Vm >> v) & 1]
    if len(verts) < 2 or len(H) > 22: return False
    if not is72(H, verts): return False
    k = max(pc(E) for E in H)
    best = None; mins = []
    for F in itertools.combinations_with_replacement(range(len(H)), 6):
        R = [H[j] for j in F]
        Pi = pairs(R, verts)
        # common point convention: P = V
        full = 63
        c = cov_masks(R, verts)
        if any(c[v] == full for v in verts):
            key = (len(verts), len(Pi))
        else:
            P = set(x for pr in Pi for x in pr); key = (len(P), len(Pi))
        if best is None or key < best: best = key; mins = [(R, Pi)]
        elif key == best: mins.append((R, Pi))
    t = tau(H, verts)
    st['fam'] += 1; st['t%d' % t] += 1
    for (R, Pi) in mins:
        analyse(H, verts, R, Pi, t, k, st); st['min'] += 1
    return True

def gen(rng):
    n, k = rng.choice([(5, 3), (6, 4), (7, 5), (6, 3), (8, 5), (9, 6)])
    core = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)]
    H = rng.sample(core, min(len(core), rng.randint(6, 13)))
    mode = rng.random()
    nxt = n
    if mode < 0.4:   # extra edges using outside vertices
        for _ in range(rng.randint(1, 3)):
            sz = rng.randint(1, k)
            inside = rng.sample(range(n), max(0, sz - rng.randint(1, 2)))
            E = sum(1 << v for v in inside)
            for _ in range(sz - len(inside)):
                E |= 1 << rng.randint(n, n + 2)
            H.append(E)
    elif mode < 0.7:  # private noise on some edges (rank grows)
        H2 = []
        for E in H:
            if rng.random() < 0.5:
                E |= 1 << nxt; nxt += 1
            H2.append(E)
        H = H2
    else:            # delete a vertex from some edges (non-uniform)
        H = [E & ~(1 << rng.randrange(n)) if rng.random() < 0.3 else E for E in H]
        H = [E for E in H if E]
    return H

if __name__ == '__main__':
    seed = int(sys.argv[1]); nf = int(sys.argv[2])
    rng = random.Random(seed)
    st = Counter(); tries = 0
    while st['fam'] < nf:
        tries += 1
        run_family(gen(rng), st)
        if st['fam'] % 50 == 0 and st['fam']:
            pass
    print('seed', seed, 'tries', tries, dict(st), flush=True)
