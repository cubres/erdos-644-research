# Theorem R+ (notes_tameanchored [a2]): numerical table of the partition-free non-robustness radius eps(c).
# Condition:  (1-eta) ((1+eps)/eps)^s (c - phi(eps)) > n ln 2 ,   phi(eps) = eps ln(e(1+eps)/eps),
# compared with Theorem R's fixed-partition radius gamma(c): psi(1+gamma) = c (Markov, exact exponent) and
# the value used in Theorem R (psi(1+gamma) = c/2).  psi(x) = x ln x - (x-1) ln(x-1).
# Also the tau loss C c k of Lemma R1 (C = N/k = n) versus the guaranteed rank loss (3/4) eps k.
import math
def psi(x): return x*math.log(x) - (x-1)*math.log(x-1)
def phi(e): return e*math.log(math.e*(1+e)/e)
def solve_inc(fun, target, lo, hi):
    for _ in range(200):
        mid = (lo+hi)/2
        if fun(mid) < target: lo = mid
        else: hi = mid
    return lo
def eps_max(c, n, s=3, eta=1/7):
    # largest eps with (1-eta)((1+eps)/eps)^s (c - phi(eps)) > n ln 2 ; LHS decreasing in eps on (0, eps0) where phi(eps0)=c
    eps0 = solve_inc(phi, c, 1e-12, 1.0)
    def g(e):  # sign of (1-eta)((1+e)/e)^s (c-phi(e)) - n ln2, computed in log space
        d = c - phi(e)
        if d <= 0: return -1.0
        return math.log(1-eta) + s*math.log((1+e)/e) + math.log(d) - math.log(n*math.log(2))
    lo, hi = 1e-12, eps0
    if g(lo) <= 0: return 0.0
    for _ in range(200):
        mid = (lo+hi)/2
        if g(mid) > 0: lo = mid
        else: hi = mid
    return lo
print(f"{'c':>7} {'n':>5} {'s':>2} {'eps(c) R+':>10} {'gamma:psi=c':>12} {'gamma:psi=c/2':>13} {'eps/gamma':>9} {'tau loss n*c':>12} {'3eps/4':>8}")
for n in (1.75, 2.0, 2.6, 4.0):
    for c in (0.001, 0.003, 0.01, 0.03, 0.1, 0.2):
        for s in (1, 3, 31):
            e = eps_max(c, n, s)
            g1 = solve_inc(lambda x: psi(1+x), c, 1e-12, 1.0)
            g2 = solve_inc(lambda x: psi(1+x), c/2, 1e-12, 1.0)
            print(f"{c:7.3f} {n:5.2f} {s:2d} {e:10.5f} {g1:12.5f} {g2:13.5f} {e/g1:9.3f} {n*c:12.4f} {0.75*e:8.4f}")
