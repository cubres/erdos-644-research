"""Referee checks for tameness#1 (Corollary R').
(1) exact brute force of the R1 counting step: every (alpha+1)-set has an edge  =>
    #edges inside Y >= C(|Y|,k)/C(alpha+1,k)  (and >= (N/(N-k))^D), on small random families.
(2) exact (Fraction/integer) check of the ratio inequality prod_{j=a+2}^{a+1+D} j/(j-k) >= (N/(N-k))^D.
(3) log-scale evaluation of the two union bounds (q=e^{-sqrt k} as claimed; q=e^{-L}, L const, improvement).
"""
import itertools, random, math
from fractions import Fraction
from math import comb

def alpha_of(N, k, E):
    best = k - 1
    for s in range(N, k - 1, -1):
        for Y in itertools.combinations(range(N), s):
            Ys = set(Y)
            if not any(e <= Ys for e in E):
                return s
    return best

random.seed(1)
bad = 0; tests = 0
for trial in range(300):
    k = random.choice([2, 3]); N = random.randint(k + 2, 8)
    allk = [frozenset(c) for c in itertools.combinations(range(N), k)]
    E = [e for e in allk if random.random() < random.choice([0.3, 0.6, 0.9])]
    if not E: continue
    a = alpha_of(N, k, E)
    for s in range(a + 1, N + 1):
        for Y in itertools.combinations(range(N), s):
            Ys = set(Y); cnt = sum(1 for e in E if e <= Ys)
            lb = Fraction(comb(s, k), comb(a + 1, k))
            D = s - a - 1
            lb2 = Fraction(N, N - k) ** D
            tests += 1
            if cnt < lb or lb < lb2: bad += 1
print("(1) R1 counting brute force: tests", tests, "violations", bad)

bad = 0
for N in range(8, 26):
    for k in range(2, N):
        for a in range(k - 1, N):
            for D in range(0, N - a):
                lhs = Fraction(1)
                for j in range(a + 2, a + 2 + D): lhs *= Fraction(j, j - k)
                if lhs < Fraction(N, N - k) ** D: bad += 1
print("(2) product inequality exact, violations:", bad)

def union_log(k, C, p, L):
    N = C * k
    return N * math.log(p) + p * math.log(k + 1) - L * k / (2 * p)  # log of expected # bad classes
def first_k(ok):
    hi = 4
    while not ok(hi): hi *= 2
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): hi = mid
        else: lo = mid
    return hi  # (monotone for large k; coarse)
print("(3) log union bound, q=e^{-sqrt k}:")
for C in [2, 4]:
    for p in [2, 7, 64, 1000]:
        k0 = first_k(lambda k: union_log(k, C, p, math.sqrt(k)) < math.log(0.5))
        print(f"   C={C} p={p}: bound < 1/2 from k ~ {k0}")
print("    improvement q=e^{-L}, L = 2Cp ln p + 2 (+ ln-terms): loss D = C(L+ln(2N ln2)) = O(log k)")
for C in [2]:
    for p in [2, 7, 64]:
        L = 2 * C * p * math.log(p) + 2
        k0 = first_k(lambda k: union_log(k, C, p, L) < math.log(0.5))
        print(f"   C={C} p={p} L={L:.1f}: union<1/2 from k~{k0}; R1 loss ~ {C*(L+math.log(2*C*k0*math.log(2))):.1f}")
