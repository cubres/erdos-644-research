# Exact check of the weighted Chernoff bound P(X>=a) <= (e mu/a)^{a/omega}, X = sum_j B_j w_j, B_j ~ Bern(rho) indep,
# 0 <= w_j <= omega, mu >= rho sum w_j, a > mu.  Exact enumeration with Fractions.
import itertools, math, random
from fractions import Fraction
random.seed(7)
viol = 0; tests = 0; tight = 0.0
for t in range(3000):
    n = random.randint(1, 12)
    omega = Fraction(random.randint(1, 10), 10)
    w = [omega * Fraction(random.randint(0, 20), 20) for _ in range(n)]
    rho = Fraction(random.randint(1, 30), 100)
    mu = rho * sum(w)
    if mu == 0: continue
    a = mu * Fraction(random.randint(11, 60), 10)
    P = Fraction(0)
    for B in itertools.product((0, 1), repeat=n):
        if sum(b * x for b, x in zip(B, w)) >= a:
            pr = Fraction(1)
            for b in B: pr *= rho if b else 1 - rho
            P += pr
    bound = (math.e * float(mu) / float(a)) ** (float(a) / float(omega))
    tests += 1
    if float(P) > bound * (1 + 1e-12): viol += 1
    if bound > 0: tight = max(tight, float(P) / bound)
print("weighted Chernoff: tests", tests, "violations", viol, "max P/bound", tight)
