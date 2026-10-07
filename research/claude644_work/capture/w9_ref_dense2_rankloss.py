"""Referee w9, dense#2: test the quantitative consequence behind 'rank loss <= imbalance' (integer version).
Fine type-closed set up(T) (T = generators, f_pi 0/1).  With delta = m exp(-2 lam^2/X), c = ceil(lam X/min n),
R = max_{g in T} (|g| + I(g)) + c:
   tau*_int( A_2(eta+delta)^{<=R} ) >= tau*_int( up T ) - c - m      (eta=0 here)
(tau*_int(S) = N - max{|w| : integer w <= caps, no s in S with s <= w}).  Also report the actual loss."""
import itertools, random, math, sys
from math import comb
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
fails = 0; rows = []
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 20):
    m = random.choice([2, 3]); ns = [random.randint(10, 22) for _ in range(m)]; X = sum(ns)
    e = random.randint(8, 20); N = e + X
    T = [(random.randint(0, e), tuple(random.randint(0, n) for n in ns)) for _ in range(random.randint(1, 4))]
    T.append((e, tuple(0 for _ in ns)))   # anchor
    def fpi(a, U): return any(a >= g[0] and all(U[i] >= g[1][i] for i in range(m)) for g in T)
    P = {}
    for U in itertools.product(*[range(n+1) for n in ns]):
        p = 1
        for u, n in zip(U, ns): p *= comb(n, u)
        P.setdefault(sum(U), []).append((U, p / comb(X, sum(U))))
    lam = math.sqrt(X*math.log(4*m)/2); delta = m*math.exp(-2*lam**2/X); c = math.ceil(lam*X/min(ns))
    R = max(g[0] + X*max(g[1][s]/ns[s] for s in range(m)) for g in T) + c
    # fine free max
    free_f = max((a+sum(U) for a in range(e+1) for U in itertools.product(*[range(n+1) for n in ns]) if not fpi(a, U)), default=-1)
    tf = N - free_f
    # 2-part set A_2(delta) truncated at rank R: (a,b) in set iff a+b<=R and f2>=1-delta; up-closure
    A2 = [(a, b) for a in range(e+1) for b in range(X+1)
          if a + b <= R and sum(p for U, p in P[b] if fpi(a, U)) >= 1 - delta]
    free_2 = max((a+b for a in range(e+1) for b in range(X+1) if not any(a >= s[0] and b >= s[1] for s in A2)), default=-1)
    t2 = N - free_2
    ok = t2 >= tf - c - m
    fails += not ok
    Imax = max(g[0] + X*max(g[1][s]/ns[s] for s in range(m)) - g[0] - sum(g[1]) for g in T)
    rows.append((ns, e, round(max(g[0]+sum(g[1]) for g in T)), round(R, 1), round(Imax, 1), c, tf, t2, ok))
for r in rows: print(r)
print('fails', fails)
