#!/usr/bin/env python3
"""w9_ref_dense1_lower.py -- referee w9, claim dense#1 (Corollary Q), LOWER-BOUND half.

Independent exact test of the step  tau*(T) >= tau(H) - 2D - 2  in the proof of Corollary Q,
generalised to an arbitrary shift s (the claim uses s=3; the proof needs only D >= s):
    A_s   = { u <= n integer : f((u - s*1)^+) >= 1 - eta }
    T     = A_s^{<= r} u {e0},  r = k + 2D,  e0 = (e, 0)
    HYP   : for every edge G with u_G + D*1 <= n :  f(u_G + (D-s)*1) >= 1 - eta
    CLAIM : H intersecting, E0 a smallest edge, HYP  ==>  tau*(T) >= tau - 2D - 2.
tau*(T) = N - max{|w| : w integer box <= n, every g in T has i with g_i>0, w_i<=g_i} (continuous sup is
attained at integer corners since all type coordinates are integers).
f computed EXACTLY (Fractions) by enumerating all subsets of V (up-closure of the edge indicator).
Mutations (to show the checker is sensitive): (M1) E0 not smallest, (M2) H not intersecting,
(M3) the sharper bound tau - 2D - 1 / tau - 2D.
Usage: python3 w9_ref_dense1_lower.py SEED NFAM
"""
import sys, random
from fractions import Fraction
from itertools import combinations
from math import comb

def upclosure(N, edges):
    top = 1 << N
    has = bytearray(top)
    for E in edges: has[E] = 1
    for i in range(N):
        b = 1 << i
        for S in range(top):
            if S & b and has[S ^ b]: has[S] = 1
    return has

def popc(x): return bin(x).count('1')

def analyse(N, e, edges, E0mask):
    has = upclosure(N, edges)
    top = 1 << N
    nO = N - e
    # f table: count edge-containing subsets per profile
    cnt = {}
    for S in range(top):
        a = popc(S & E0mask); b = popc(S & ~E0mask)
        c = cnt.setdefault((a, b), [0, 0]); c[0] += 1; c[1] += has[S]
    f = {p: Fraction(c[1], c[0]) for p, c in cnt.items()}
    alpha = max(popc(S) for S in range(top) if not has[S])
    tau = N - alpha
    return f, tau

def prof(G, E0mask): return (popc(G & E0mask), popc(G & ~E0mask))

def tau_star(T, n):
    e, x = n
    best = -1
    for w0 in range(e + 1):
        for w1 in range(x + 1):
            if w0 + w1 <= best: continue
            ok = True
            for g in T:
                if not ((g[0] > 0 and w0 <= g[0]) or (g[1] > 0 and w1 <= g[1])):
                    ok = False; break
            if ok: best = w0 + w1
    return e + x - best

def gen_family(rng, N, mode):
    """returns (edges as masks, E0mask, e, k)."""
    e = rng.randint(2, max(2, N // 2))
    E0 = rng.sample(range(N), e); E0mask = sum(1 << v for v in E0)
    kmax = rng.randint(e, min(N - 1, e + 4))
    edges = [E0mask]
    others = [v for v in range(N) if v not in E0]
    if mode == 'dense':
        # N < 2e: every set of size >= e meets every other -> intersecting; E0 is a smallest edge
        e = rng.randint((N + 2) // 2, N - 2)
        E0 = rng.sample(range(N), e); E0mask = sum(1 << v for v in E0)
        kmax = rng.randint(e, min(N - 1, e + 2))
        p = rng.choice([1.0, 0.97, 0.9, 0.75])
        edges = [E0mask]
        for sz in range(e, kmax + 1):
            for S in combinations(range(N), sz):
                if rng.random() < p: edges.append(sum(1 << v for v in S))
        edges = list(set(edges)); k = max(popc(E) for E in edges)
        return edges, E0mask, e, k
    if mode == 'typeclosed':
        # pick a few 2-part types (a,b), a>=1, e<=a+b<=kmax; include ALL sets of those profiles if pairwise intersecting
        types = set()
        for _ in range(rng.randint(1, 3)):
            a = rng.randint(1, e); b = rng.randint(max(0, e - a), min(len(others), kmax - a)) if kmax - a >= max(0, e - a) else None
            if b is None: continue
            types.add((a, b))
        types = [t for t in types if all(t[0] + u[0] > e or t[1] + u[1] > N - e for u in types)]
        for (a, b) in types:
            for A in combinations(E0, a):
                for B in combinations(others, b):
                    edges.append(sum(1 << v for v in A + B))
        # optionally delete a random fraction (quasirandom-like), keep E0
        if rng.random() < 0.5:
            p = rng.choice([0.9, 0.7, 0.5])
            edges = [edges[0]] + [E for E in edges[1:] if rng.random() < p]
    else:
        tries = rng.randint(5, 60)
        for _ in range(tries):
            sz = rng.randint(e, kmax)
            S = rng.sample(range(N), sz); m = sum(1 << v for v in S)
            if mode == 'nonint' or all(m & E for E in edges):
                edges.append(m)
    edges = list(set(edges))
    k = max(popc(E) for E in edges)
    return edges, E0mask, e, k

def run(seed, nfam):
    rng = random.Random(seed)
    stats = dict(tested=0, hyp=0, fail=0, m1_fail=0, m1_hyp=0, m2_fail=0, m2_hyp=0, sharp1=0, sharp0=0, nontriv=0)
    for it in range(nfam):
        mode = rng.choice(['typeclosed', 'random', 'dense', 'dense', 'dense'])
        N = rng.randint(9, 13) if mode == 'dense' else rng.randint(6, 12)
        edges, E0mask, e, k = gen_family(rng, N, mode)
        # sanity on hypotheses
        inter = all(E & F for E, F in combinations(edges, 2))
        smallest = min(popc(E) for E in edges) == e
        f, tau = analyse(N, e, edges, E0mask)
        n = (e, N - e)
        for s in (0, 1, 3):
            for D in sorted({s, s + 1, s + 2}):
                for eta in (Fraction(0), Fraction(1, 7), Fraction(1, 2)):
                    hyp = True
                    for G in edges:
                        u = prof(G, E0mask)
                        if u[0] + D <= n[0] and u[1] + D <= n[1]:
                            if f[(u[0] + D - s, u[1] + D - s)] < 1 - eta: hyp = False; break
                    stats['tested'] += 1
                    if not hyp: continue
                    r = k + 2 * D
                    A = [(a, b) for a in range(n[0] + 1) for b in range(n[1] + 1)
                         if a + b <= r and f[(max(0, a - s), max(0, b - s))] >= 1 - eta]
                    T = A + [(e, 0)]
                    ts = tau_star(T, n)
                    ok = ts >= tau - 2 * D - 2
                    if tau - 2 * D - 2 > 0 and inter and smallest: stats['nontriv'] += 1
                    if inter and smallest:
                        stats['hyp'] += 1
                        if not ok:
                            stats['fail'] += 1
                            print('FAIL', seed, it, N, e, k, s, D, eta, tau, ts, [bin(E) for E in edges][:6])
                        if ts < tau - 2 * D - 1: pass
                        if ts >= tau - 2 * D - 1: stats['sharp1'] += 1
                        if ts >= tau - 2 * D: stats['sharp0'] += 1
                    elif inter and not smallest:
                        stats['m1_hyp'] += 1; stats['m1_fail'] += (not ok)
                    elif not inter:
                        stats['m2_hyp'] += 1; stats['m2_fail'] += (not ok)
        # mutation M1 explicitly: re-anchor at a NON-smallest edge if one exists
    return stats

def run_mut(seed, nfam):
    """M1/M2 explicit: choose E0 = a larger edge than the minimum (M1), or add an edge disjoint from another (M2)."""
    rng = random.Random(seed + 1000)
    res = dict(m1=0, m1_fail=0, m2=0, m2_fail=0)
    for it in range(nfam):
        N = rng.randint(6, 11)
        # M1: small edge Z of size 2 meeting E0, E0 bigger; intersecting family
        e = rng.randint(3, N - 3)
        E0 = list(range(e)); E0mask = (1 << e) - 1
        edges = [E0mask]
        # all sets of size >= e+? containing vertex 0 -> intersecting
        z = rng.randint(1, e - 1)
        Z = [0] + rng.sample(range(e, N), 1); edges.append(sum(1 << v for v in Z))  # small edge through 0
        for _ in range(rng.randint(3, 30)):
            sz = rng.randint(2, min(N - 1, e + 2))
            S = [0] + rng.sample(range(1, N), sz - 1); edges.append(sum(1 << v for v in S))
        edges = list(set(edges)); k = max(popc(E) for E in edges)
        f, tau = analyse(N, e, edges, E0mask); n = (e, N - e)
        for s, D in ((0, 0), (0, 1)):
            eta = Fraction(0)
            hyp = all(f[(u[0] + D - s, u[1] + D - s)] >= 1 for u in (prof(G, E0mask) for G in edges)
                      if u[0] + D <= n[0] and u[1] + D <= n[1])
            if not hyp: continue
            r = k + 2 * D
            A = [(a, b) for a in range(n[0] + 1) for b in range(n[1] + 1)
                 if a + b <= r and f[(max(0, a - s), max(0, b - s))] >= 1]
            ts = tau_star(A + [(e, 0)], n)
            res['m1'] += 1; res['m1_fail'] += ts < tau - 2 * D - 2
    return res

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    nfam = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    print('main', run(seed, nfam))
    print('mut', run_mut(seed, nfam))
