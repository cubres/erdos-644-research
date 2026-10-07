#!/usr/bin/env python3
"""Exact-integer transcription check for the revised case analysis (v3).

For every rank k in a range (7..N) it enumerates every integer configuration that the
revised proof must handle and checks that the lemma named in the proof has all of
its stated hypotheses satisfied.  Standard library only.  This is a diagnostic for
transcription errors in the arithmetic; it does not verify the set constructions,
which are proved by hand in the manuscript, and it proves nothing for ranks outside
the range.

Usage: python3 -B -S check_cases.py [--max-rank N]
"""
import sys

def cdiv(a, b):  # ceil(a/b) for b>0
    return -((-a) // b)

# ---------------- exact lemma hypotheses (as stated in the manuscript) -------------
def hall(k, T, a, b, c):          # Lemma (Hall allocation), a distinguished
    return (T - a >= 0 and T - a - b >= 0 and T - a - c >= 0 and T - b - c >= 0 and
            k + 2*c <= 2*T and k + 2*b <= 2*T and k + 3*a <= 3*T and
            2*k + b + c <= 3*T and 2*k + 2*a + c <= 4*T and 2*k + 2*a + b <= 4*T and
            3*k + a <= 4*T)

def cor_hall(k, T, a, b, c):      # Corollary (Hall): hypotheses as stated, T >= 6k/7
    return (7*T >= 6*k and T <= k and 2*a <= T and 2*b <= 2*T - k and 2*c <= 2*T - k
            and b + c <= 3*T - 2*k)

def symm(k, T, x, y, z):          # Lemma (symmetric allocation); sorts internally
    m, yy, zz = sorted((x, y, z), reverse=True)
    S = x + y + z
    return (T >= k + m - yy - zz and 2*T >= k + m and 3*T >= 2*k + m + yy - zz and
            5*T >= 3*k + S)

def onecore(k, T, x, y, z):       # Lemma (one surviving cell), designated cell z
    S = x + y + z
    return (T <= k and T >= x + y and 2*T >= k + 2*x and 2*T >= k + 2*y and
            T >= k + x - y - z and T >= k - x + y - z and 3*T >= 3*k - S and
            5*T >= 3*k + S and 3*T >= k + x + y + 2*z and 4*T >= 2*k + 3*z)

def splitA(k, T, x, y, z):        # Lemma (asymmetric split A)
    S = x + y + z
    return (T <= k and T >= S and 2*T >= k + 2*y and 2*T >= k + 2*x - y + z and
            3*T >= k + 2*x + y + 3*z)

def splitB(k, T, x, y, z):        # Lemma (asymmetric split B)
    S = x + y + z
    return (T <= k and T >= S and 3*T >= k + 3*x and T >= k - x + z and
            3*T >= k + 2*x + 3*y + z)

def gap_two_traces(k, T, x, y, z, L, H):   # Lemma (two forced traces)
    assert 0 <= L <= H < k
    S = x + y + z
    p = max(0, k - x - y - H); t = max(0, k - x - z - H)
    return T <= k and S + p + t <= T and k + 3*x + p + t <= 3*T and y + z + 2*L <= T

def gap_one_core(k, T, x, y, z, L, H):     # Lemma (one core, forced traces)
    assert 0 <= L <= H < k
    S = x + y + z; Q = max(0, S - T)
    return (T <= k and x + y <= T and k - x - y <= H and k - x - z + Q <= H and
            2*x + 2*Q + k - y - z <= 2*T and y + z + 2*L <= T and
            2*k + x - y + L + Q <= 3*T)

def gap_two_cores(k, T, x, y, z, L, H):    # Lemma (two cores)
    assert 0 <= L <= H < k
    S = x + y + z; g = max(0, k - y - H)
    return (T <= k and g <= min(x, z) and y + 2*g <= T and x + L <= T and
            z + L <= T and k + 2*y <= 2*T and 3*k <= 4*T and 3*k + S <= 5*T)

def near_core(k, T, x, y, z, m):          # Lemma (near core), dichotomy <=m or >k/2
    assert 2*m <= k
    S = x + y + z; D = max(0, S - T)
    base = (T <= k and y + z <= T and m + z <= T and k + y - z <= T and
            2*k + x - 2*z <= 2*T and 2*k + x + m - z <= 3*T and x + m <= T)
    if not base:
        return False
    if S <= T and k - x + y <= T and 2*k - 2*x + z <= 2*T:
        return True
    return (k - x + y + D <= T and 2*k - 2*x + z + D <= 2*T and 2*k - z + D <= 2*T and
            3*k - x - y + D <= 3*T)

def two_large(k, T, m, x, b):             # Lemma (two large opposite cells)
    return (4*m <= k and T <= k and T >= cdiv(k, 2) + 2*m and T >= x + m and
            3*T >= 2*x + b + cdiv(k, 2) + 2*m)

# ---------------- the revised proof, branch by branch -------------------------------
def check_rank(k, stats):
    h = k // 7; s = k - 7*h; T = k - h
    assert T == cdiv(6*k, 7) and h >= 1
    A = T // 2
    B = (4*T - 2*k) // 3
    C = T - cdiv(k, 2)
    D = 2*k - T - 2*B
    L = D - 1
    U = 2*T - k - cdiv(k, 2)
    half = k // 2
    # endpoint lemma
    assert 0 <= C <= A <= B and B >= 3*h and L <= U == C - h and 4*L <= T
    assert k - B - 1 + L <= T
    # small class and medium class boundary: C = T - ceil(k/2)

    # ---- Finisher (local): M in [k-T+1, floor(T/2)], M>=y>=z, dichotomy <=M or >k/2
    for M in range(k - T + 1, A + 1):
        for y in range(0, M + 1):
            for z in range(0, y + 1):
                two_medium = (2*y > 2*T - k) and (2*z <= 2*T - k)
                if not two_medium and y + z <= 3*T - 2*k:
                    ok = cor_hall(k, T, M, y, z) and hall(k, T, M, y, z); tag = 'fin-hall'
                elif not two_medium:
                    ok = symm(k, T, M, y, z); tag = 'fin-symm'
                elif z > k - T:                        # two medium, z in (k-T, T-k/2]
                    ok = gap_two_cores(k, T, M, z, y, M, half); tag = 'fin-2cores'
                else:                                  # two medium, z <= k-T
                    ok = near_core(k, T, M, z, y, M); tag = 'fin-nearcore'
                stats[tag] = stats.get(tag, 0) + 1
                if not ok:
                    raise AssertionError((k, tag, M, y, z))
    # ---- balanced request bound in the finisher: M>=k-T+1 gives traces <= floor(k/2)
    for M in range(k - T + 1, A + 1):
        assert k - (T + M) // 2 <= half
    # ---- small maximum: M = m <= k-T  (k = 7 is Proposition 'rank seven', checked separately)
    for m in (range(0, k - T + 1) if k >= 8 else []):
        # all-small triple closes by Hall
        for y in range(0, m + 1):
            for z in range(0, y + 1):
                assert cor_hall(k, T, m, y, z) and hall(k, T, m, y, z), (k, 'small-hall', m, y, z)
                stats['small-hall'] = stats.get('small-hall', 0) + 1
        xmax = k - (T + m) // 2
        for x in range(half + 1, xmax + 1):
            # request of size x + m + z <= T must be possible (z <= m)
            assert x + 2*m <= T, (k, 'small-request', m, x)
            # branch b <= k/2: triple (E,G,H) has all cells <= m, closed by the corollary
            for z2 in range(0, m + 1):
                for b2 in range(0, m + 1):
                    assert cor_hall(k, T, m, z2, b2), (k, 'small-hall-2', m, z2, b2)
            for b in range(half + 1, k - T + x + 1):
                assert two_large(k, T, m, x, b), (k, 'two-large', m, x, b)
                stats['two-large'] = stats.get('two-large', 0) + 1
    # ---- Stage 1: q in [A+1, min(B, floor(k/2))], caps C, triple (x=q, y>=z<=C)
    for q in range(A + 1, min(B, half) + 1):
        # cap lemma hypotheses
        assert 0 <= 2*k - T - q <= 2*C and C <= k - q
        x = q
        for y in range(0, C + 1):
            for z in range(0, y + 1):
                d = y - z; v = y + z
                if d > x - h:
                    ok = splitA(k, T, x, y, z); tag = 's1-splitA'
                elif v <= 3*T - k - 2*x:
                    ok = onecore(k, T, y, z, x); tag = 's1-onecore'
                else:
                    ok = symm(k, T, x, y, z); tag = 's1-symm'
                stats[tag] = stats.get(tag, 0) + 1
                if not ok:
                    raise AssertionError((k, tag, x, y, z))
    if B >= half:
        stats['early'] = stats.get('early', 0) + 1
        return
    assert h < D <= C and 0 <= L < C < k
    assert T + B - k <= C - 1                 # Lemma (endpoints), used in the middle gap
    # ---- Stage 2: q in [D, C], caps B, traces <= B hence <= A (gap G(A,B))
    for q in range(D, C + 1):
        assert 0 <= 2*k - T - q <= 2*B and B <= k - q
        x = q
        for y in range(0, A + 1):
            for z in range(0, y + 1):
                if x + z <= k - B - 1:
                    ok = cor_hall(k, T, y, x, z) and hall(k, T, y, x, z); tag = 's2-hall'
                else:
                    ok = gap_two_cores(k, T, y, x, z, A, B); tag = 's2-2cores'
                stats[tag] = stats.get(tag, 0) + 1
                if not ok:
                    raise AssertionError((k, tag, x, y, z))
    # ---- Stage 3: q in [B+1, floor(k/2)], caps C, traces <= C hence <= L (gap G(L,C))
    J = 2*k - C + 2*half - 3*T
    assert J == (h - s) // 2
    for q in range(B + 1, half + 1):
        assert 0 <= 2*k - T - q <= 2*C and C <= k - q
        x = q
        for y in range(0, L + 1):
            for z in range(0, y + 1):
                S = x + y + z
                assert k - x + y <= T             # used in the upper gap
                if S <= T and (S <= 2*T - k or z < J):
                    ok = splitB(k, T, x, z, y); tag = 's3-splitB'
                elif S <= T:
                    ok = gap_two_traces(k, T, x, y, z, L, C); tag = 's3-2traces'
                else:
                    ok = gap_one_core(k, T, x, y, z, L, C); tag = 's3-1core'
                stats[tag] = stats.get(tag, 0) + 1
                if not ok:
                    raise AssertionError((k, tag, x, y, z))

def main():
    maxk = 84
    if '--max-rank' in sys.argv:
        maxk = int(sys.argv[sys.argv.index('--max-rank') + 1])
    stats = {}
    for k in range(7, maxk + 1):
        check_rank(k, stats)
    total = sum(v for key, v in stats.items() if key != 'early')
    print('ranks 7..%d: all %d branch checks passed' % (maxk, total))
    for key in sorted(stats):
        print('  %-14s %d' % (key, stats[key]))

if __name__ == '__main__':
    main()
