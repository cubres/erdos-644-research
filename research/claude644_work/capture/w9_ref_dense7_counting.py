"""Referee check for dense#7 (counting lemma):
 tau(H)=t, min edge size k', ground set V with |V|=N  =>
   |H| >= C(N,t-1)/C(N-k',t-1) = C(N,k')/C(N-t+1,k') >= (N/(N-t+1))^k'.
Exact (Fractions / integers). Tests: random hypergraphs (no (7,2) needed), (7,2)-filtered ones,
complete families (tightness), identity checks, asymptotic rate in the dense regime.
"""
import itertools, random, math
from fractions import Fraction
from math import comb

def tau(N, edges):
    masks = [sum(1<<v for v in e) for e in edges]
    for s in range(N+1):
        for T in itertools.combinations(range(N), s):
            m = sum(1<<v for v in T)
            if all(m & e for e in masks):
                return s
    return None

def is72(N, edges):
    masks = [sum(1<<v for v in e) for e in edges]
    ok2 = [ (1<<x)|(1<<y) for x in range(N) for y in range(x,N)]
    # every <=7 edges have a 2-transversal: suffices to check 7-multisets -> check all 7-subsets (and smaller if <7 edges)
    E = list(set(masks))
    r = min(7, len(E))
    for sub in itertools.combinations(E, r):
        if not any(all(p & g for g in sub) for p in ok2):
            return False
    return True

def bound(N, t, kp):
    return Fraction(comb(N, t-1), comb(N-kp, t-1))

fails = 0; checks = 0; tight = 0; n72 = 0
rng = random.Random(20260924)
for trial in range(4000):
    N = rng.randint(3, 10)
    kmax = rng.randint(1, N)
    m = rng.randint(1, 25)
    edges = set()
    for _ in range(m):
        s = rng.randint(1, kmax)
        edges.add(tuple(sorted(rng.sample(range(N), s))))
    edges = list(edges)
    t = tau(N, edges)
    kp = min(len(e) for e in edges)
    # side conditions implied by tau=t
    assert N - (t-1) >= kp and t >= 1
    b = bound(N, t, kp)
    # identity C(N,t-1)/C(N-k',t-1) == C(N,k')/C(N-t+1,k')
    assert b == Fraction(comb(N, kp), comb(N-t+1, kp))
    b2 = Fraction(N, N-t+1)**kp
    checks += 1
    if not (len(edges) >= b >= b2):
        fails += 1; print("FAIL", N, t, kp, len(edges), b, b2, edges)
    if len(edges) == b: tight += 1
    if trial % 8 == 0 and len(edges) <= 14 and is72(N, edges):
        n72 += 1
print(f"random: {checks} checks, {fails} failures, {tight} tight, {n72} were (7,2)")

# (7,2)-only sample: complete k-uniform families on n points (known (7,2) iff n <= ~7k/4 region; just test lemma)
for k in range(1, 7):
    for n in range(k, k+7):
        edges = list(itertools.combinations(range(n), k))
        if len(edges) > 300: continue
        t = n - k + 1
        b = bound(n, t, k)
        assert b == len(edges), (n, k)   # EXACT equality for complete families
print("complete families K_n^k: bound is attained with equality (N=k+t-1)")

# asymptotic rate in the dense regime: (1/k) ln bound for N=c k, t=3k/4, k'=t (intersecting NF) and k'=k
for c in [Fraction(7,4), 2, 3, 5, 10]:
    for k in [400, 4000]:
        N = int(c*k); t = 3*k//4
        for kp in [t, k, t - (k+4)//5]:
            if N-kp < t-1: continue
            lb = math.lgamma(N+1)-math.lgamma(t)-math.lgamma(N-t+2) - (math.lgamma(N-kp+1)-math.lgamma(t)-math.lgamma(N-kp-t+2))
            print(f"c={float(c):5.2f} k={k:5d} k'={kp:5d}: ln(bound)/k = {lb/k:.4f}   k' ln(N/(N-t+1))/k = {kp*math.log(N/(N-t+1))/k:.4f}")
