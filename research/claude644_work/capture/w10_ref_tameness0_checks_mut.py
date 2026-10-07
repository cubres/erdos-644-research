# Referee checks for tameness#0 (Theorem R, sparsification). Exact arithmetic (Fractions) where it matters.
# 1. R1 double-counting bound on random small families (every (alpha+1)-subset of Y has an edge).
# 2. [t4'] per-edge weight bound P(E subset W) <= exp(-min(k ln2/2, s k/(4m))) and the [t4] bound exp(-s k/N).
# 3. Shift-monotonicity lemma (referee fix): RL^{(s+d)}(r+d p) <= RL^{(s)}(r) + d p, exact f by enumeration.
# 4. Counterexample to R2(a) as literally stated (singleton partition, s=0).
# 5. Corollary arithmetic: c(eps), allowed ln p, eps below which only p=1 is allowed at fixed s.
import itertools, math, random, sys
from fractions import Fraction
from math import comb

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

def alpha(N, H):
    best = 0
    for r in range(N, -1, -1):
        for S in itertools.combinations(range(N), r):
            s = set(S)
            if not any(E <= s for E in H):
                return r
    return 0

# ---------- 1. R1 counting ----------
bad1 = 0; tests1 = 0
for trial in range(300):
    N = random.randint(5, 9); k = random.randint(2, min(4, N - 1))
    allk = [frozenset(c) for c in itertools.combinations(range(N), k)]
    H = [E for E in allk if random.random() < random.choice([0.3, 0.6, 0.9])]
    if not H: continue
    a = alpha(N, H)
    for D in range(0, N - a):
        for Y in itertools.combinations(range(N), a + 1 + D):
            y = set(Y); cnt = sum(1 for E in H if E <= y)
            lb = Fraction(comb(len(Y), k), comb(a + 1, k)) if a + 1 >= k else None
            tests1 += 1
            if lb is not None and cnt < lb: bad1 += 1
            # product form lower bound (N/(N-k))^D
            if a + 1 >= k and Fraction(cnt) < Fraction(N, N - k) ** D: bad1 += 1
print("R1 counting: tests", tests1, "violations", bad1)

# ---------- 2. weight bound ----------
def wexact(ns, vs, es):
    w = Fraction(1)
    for n, v, e in zip(ns, vs, es):
        w *= Fraction(comb(v, e), comb(n, e))
    return w
bad2 = 0; bad2b = 0; tests2 = 0; worst = 0.0
for trial in range(20000):
    p = random.randint(1, 4)
    ns = [random.randint(1, 30) for _ in range(p)]
    s = random.randint(0, 12)
    vs = [random.randint(0, max(n - s, 0)) for n in ns]
    k = random.randint(1, 40)
    # random e with e_i <= v_i summing to k
    cap = sum(vs)
    if cap < k: continue
    es = [0] * p; rem = k
    idx = list(range(p))
    while rem:
        i = random.choice(idx)
        if es[i] < vs[i]: es[i] += 1; rem -= 1
    m = sum(vs); N = sum(ns)
    if m < k: continue
    w = wexact(ns, vs, es)
    tests2 += 1
    b = math.exp(-min(k * math.log(2) / 2, s * k / (4 * m)))
    if float(w) > b * (1 + 1e-12): bad2 += 1
    b2 = math.exp(-s * k / N)
    if float(w) > b2 * (1 + 1e-12): bad2b += 1
print("weight bound [t4']: tests", tests2, "violations", bad2, "; [t4] exp(-sk/N):", bad2b)

# ---------- 3. shift monotonicity ----------
def profiles(ns):
    return itertools.product(*[range(n + 1) for n in ns])

def f_exact(parts, H, v):
    # probability a uniform set with |W cap P_i| = v_i contains an edge of H
    choices = [list(itertools.combinations(P, vi)) for P, vi in zip(parts, v)]
    tot = 0; hit = 0
    for pick in itertools.product(*choices):
        W = set().union(*[set(c) for c in pick]) if pick else set()
        tot += 1
        if any(E <= W for E in H): hit += 1
    return Fraction(hit, tot)

def robust(parts, H, s, eta, fcache):
    ns = [len(P) for P in parts]
    A = []
    for u in profiles(ns):
        v = tuple(max(x - s, 0) for x in u)
        if v not in fcache: fcache[v] = f_exact(parts, H, v)
        if fcache[v] >= 1 - eta: A.append(u)
    return A

def tau_int(ns, G):
    # integer tau*: N - max{|w| : w integer in box, no g in G with g <= w}
    N = sum(ns); best = -1
    for w in profiles(ns):
        if not any(all(g[i] <= w[i] for i in range(len(ns))) for g in G):
            best = max(best, sum(w))
    return N - best if best >= 0 else N + 1  # N+1 if even 0 is not free (never happens here)

bad3 = 0; tests3 = 0
eta = Fraction(1, 8)
for trial in range(60):
    N = random.randint(6, 8); k = random.randint(2, 3)
    allk = [frozenset(c) for c in itertools.combinations(range(N), k)]
    H = [E for E in allk if random.random() < random.choice([0.2, 0.5, 0.8])]
    if not H: continue
    perm = list(range(N)); random.shuffle(perm)
    p = random.randint(1, 3)
    cuts = sorted(random.sample(range(1, N), p - 1))
    parts = [perm[a:b] for a, b in zip([0] + cuts, cuts + [N])]
    ns = [len(P) for P in parts]
    fc = {}
    for s in range(0, 3):
        As = robust(parts, H, s, eta, fc)
        for d in range(1, 3):
            Asd = robust(parts, H, s + d, eta, fc)
            tA, tAd = tau_int(ns, As), tau_int(ns, Asd)
            for r in range(0, N + 1):
                RL = tA - tau_int(ns, [u for u in As if sum(u) <= r])
                r2 = r
                RL2 = tAd - tau_int(ns, [u for u in Asd if sum(u) <= r2])
                tests3 += 1
                if RL2 > RL: bad3 += 1; pass
print("shift monotonicity RL^{(s+d)}(r+dp) <= RL^{(s)}(r)+dp: tests", tests3, "violations", bad3)

# ---------- 4. R2(a) literal counterexample ----------
N, k = 7, 3
H = [frozenset(c) for c in itertools.combinations(range(N), k)][:5]
parts = [[i] for i in range(N)]
A0 = robust(parts, H, 0, eta, {})
small = [u for u in A0 if sum(u) <= k]
print("R2(a) singleton partition, s=0: members of A of size k:", len(small), "(= #edges", len(H), ")")

# ---------- 5. corollary arithmetic ----------
def psi(x): return x * math.log(x) - (x - 1) * math.log(x - 1)
C = 1.75
for s in (13, 63):
    for eps in (0.1, 0.01, 1e-3, 1e-6, 1e-8, 1e-10):
        g = 2 * eps / 3
        c = 2 * psi(1 + g)
        lnp = (3 / 7) * math.exp(s / (4 * (1 + g))) * c / C
        print(f"s={s} eps={eps:g}: c={c:.3e} (approx {(4*eps/3)*math.log(3*math.e/(2*eps)):.3e}), max ln p={lnp:.3e}, p>=2 allowed: {lnp > math.log(2)}")
