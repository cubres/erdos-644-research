#!/usr/bin/env python3
"""Exact integer threshold for the anchored pencil lemma (Lemma D) and the
unanchored pencil lemma (Lemma C), plus an exhaustive test on actual families.

Fano plane: pencil point p0; pencil lines l1={p0,a,a'}, l2={p0,b,b'},
l3={p0,c,c'}; m-lines are the four transversals (a,b,c),(a',b',c),(a',b,c'),
(a,b',c') (one point from each pencil line, even parity).

Lemma D data: anchor E (size e) is split into classes e_b,e_b',e_c,e_c'
(labels off l1); R = U \\ E (size r) is split into w (at p0), r_a, r_a'.
Conditions for a bad 7-tuple (given tau(H)=t, q=tau(H[U])):
   m-lines:  r_a + e_b + e_c <= t-1,  r_a' + e_b' + e_c <= t-1,
             r_a' + e_b + e_c' <= t-1, r_a + e_b' + e_c' <= t-1
   host l2:  w + e_b + e_b' <= q-1,   host l3: w + e_c + e_c' <= q-1.
So (7,2) forces q <= h_D(e,r,t) := min over splits of w + max(e_b+e_b', e_c+e_c').

Lemma C data: U (size N) split into w at p0 and u_x at the six other points.
   m-lines: u_a+u_b+u_c <= t-1 etc.;  pencil lines: w+u_a+u_a' <= q-1 etc.
So (7,2) forces q <= h_C(N,t).
"""
import itertools, sys
from functools import lru_cache

def h_D(e, r, t):
    best = None
    # enumerate E splits (e_b,e_b',e_c,e_c') near-balanced is enough but do all small ones
    for eb in range(e + 1):
        for ebp in range(e - eb + 1):
            for ec in range(e - eb - ebp + 1):
                ecp = e - eb - ebp - ec
                # r_a limited by lines (a,b,c) and (a,b',c'); r_a' by (a',b',c),(a',b,c')
                ra_max = min(t - 1 - eb - ec, t - 1 - ebp - ecp)
                rap_max = min(t - 1 - ebp - ec, t - 1 - eb - ecp)
                if ra_max < 0 or rap_max < 0:
                    continue
                w = max(0, r - ra_max - rap_max)
                val = w + max(eb + ebp, ec + ecp)
                if best is None or val < best:
                    best = val
    return best  # None means no feasible split (e.g. anchor too large)

def h_C(N, t):
    best = None
    pts = ['a', 'ap', 'b', 'bp', 'c', 'cp']
    # with symmetric optimum: all six classes equal u, w = N - 6u (w>=0) ; also allow unequal
    for u in range(0, t):
        if 3 * u > t - 1:
            break
        w = N - 6 * u
        if w < 0:
            # distribute N over six points as evenly as possible
            base, extra = divmod(N, 6)
            # worst m-line = 3 largest possible... check feasibility
            sizes = [base + 1] * extra + [base] * (6 - extra)
            # arrange: a,ap,b,bp,c,cp ; try all permutations for feasibility
            ok_val = None
            for perm in set(itertools.permutations(sizes)):
                a, ap, b, bp, c, cp = perm
                if max(a + b + c, ap + bp + c, ap + b + cp, a + bp + cp) <= t - 1:
                    v = max(a + ap, b + bp, c + cp)
                    ok_val = v if ok_val is None else min(ok_val, v)
            if ok_val is not None:
                best = ok_val if best is None else min(best, ok_val)
            continue
        val = w + 2 * u
        best = val if best is None else min(best, val)
    return best

def main():
    print("Lemma D threshold h_D(e, r=t-1, t) versus 3e/2 - t (critical host):")
    for t in range(6, 31, 3):
        for e in (t - 1, t, (4 * t) // 3, (4 * t) // 3 + 2):
            if e < 1:
                continue
            h = h_D(e, t - 1, t)
            print(f"  t={t:3d} e={e:3d}: h_D={h}   3e/2-t={1.5*e-t:6.1f}   ceil(e/2)={(e+1)//2}")
    print()
    print("Maximum of h_D(e,r,t) - max(ceil(e/2), r + 3e/2 - 2t) over a grid:")
    worst = -99
    for t in range(4, 26):
        for e in range(2, 2 * t - 1):
            for r in range(0, 3 * t):
                h = h_D(e, r, t)
                if h is None:
                    continue
                ref = max((e + 1) // 2, r + 1.5 * e - 2 * t)
                worst = max(worst, h - ref)
    print("  worst excess =", worst)
    worstC = -99
    for t in range(4, 26):
        for N in range(1, 4 * t):
            h = h_C(N, t)
            if h is None:
                continue
            ref = max(N / 3, N - 4 * (t - 1) / 3)
            worstC = max(worstC, h - ref)
    print("Lemma C: worst excess of h_C(N,t) over max(N/3, N-4(t-1)/3) =", worstC)

if __name__ == "__main__":
    main()
