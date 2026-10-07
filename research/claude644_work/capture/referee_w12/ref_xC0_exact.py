"""REFEREE (w12): EXACT rational boundary counterexample to Theorem 3T as stated with 'x >= 0' (x_C = 0).
All hypotheses of the statement hold, tau*({alpha,beta,gamma}) > 3/4, yet all six T(X;Y,Y;Z) and all six
V(s,t) (both argument orders) fail.  Cause: with s_C = 0 the identity map / pair maps / Lemma 0's map are
invalid (they would retain u_C = s_C - eps < 0), so tau* is not bounded by e_A+e_B+e_C there."""
from fractions import Fraction as F
import itertools, math
x = (F(93, 100), F(122, 100), F(0))
alpha = (F(924, 1000), F(76, 1000), F(0))
beta = (F(131, 1000), F(869, 1000), F(0))
gamma = (F(53, 100), F(47, 100), F(0))
types = [alpha, beta, gamma]
s = [alpha[0], beta[1], gamma[2]]
e = [x[i] - s[i] for i in range(3)]
print('x =', x, ' s =', s, ' e =', e)
# hypotheses
for i in range(3):
    assert 2 * x[i] / 3 <= s[i] <= min(1, x[i]), i
    for r in range(3):
        assert 0 <= types[r][i] <= x[i]
        if r != i: assert types[r][i] <= 2 * x[i] / 3 or types[r][i] >= s[i], (r, i)
    assert sum(types[i]) == 1
for i, j in itertools.combinations(range(3), 2): assert e[i] + e[j] <= F(3, 4)
print('hypotheses (x>=0 version) OK; balance sums:', [e[i] + e[j] for i, j in itertools.combinations(range(3), 2)])
def tau_star(x, types):
    best = None
    for sigma in itertools.product(range(3), repeat=3):
        u = list(x); ok = True
        for i in range(3):
            ts = [t[i] for t, sg in zip(types, sigma) if sg == i]
            if ts:
                m = min(ts)
                if m <= 0: ok = False; break     # cannot retain u_i < 0
                u[i] = m
        if ok:
            c = sum(x) - sum(u)
            if best is None or c < best: best = c
    return best
ts = tau_star(x, types); print('tau* =', ts, float(ts), ' > 3/4:', ts > F(3, 4))
def T_ok(a, b, c):
    return all(2*a[i]+b[i] <= 2*x[i] and 2*a[i]+c[i] <= 2*x[i] and 2*b[i]+c[i] <= 2*x[i] and 4*a[i]+2*b[i]+c[i] <= 4*x[i] for i in range(3))
def V_ok(s_, t_):
    return all(s_[i]+t_[i] <= x[i] and 5*s_[i]/4 + t_[i]/2 <= x[i] for i in range(3))
names = 'ABC'
anyok = False
for X, Y, Z in itertools.permutations(range(3)):
    ok = T_ok(types[X], types[Y], types[Z]); anyok |= ok
    print(f'T({names[X]};{names[Y]},{names[Y]};{names[Z]}) feasible:', ok)
for S, T_ in itertools.permutations(range(3), 2):
    ok = V_ok(types[S], types[T_]); anyok |= ok
    print(f'V({names[S]},{names[T_]}) (5s/4+t/2 convention) feasible:', ok)
print('SOME TEMPLATE FEASIBLE:', anyok, '  => counterexample to the x>=0 statement:', (not anyok) and ts > F(3, 4))
# the same configuration with x_C = eps > 0, s_C = eps (types renormalised) has tau* <= e_A+e_B+eps
eps = F(1, 1000)
x2 = (x[0], x[1], eps)
def renorm(t, sc):
    r = (t[0] * (1 - sc), t[1] * (1 - sc), sc); assert sum(r) == 1; return r
types2 = [renorm(alpha, eps / 2), renorm(beta, eps / 2), (gamma[0] * (1 - eps), gamma[1] * (1 - eps), eps)]
print('perturbed x_C = 1/1000: tau* =', float(tau_star(x2, types2)), '(identity map now valid: <= e_A+e_B+e_C =', float(e[0] + e[1] + eps), ')')
