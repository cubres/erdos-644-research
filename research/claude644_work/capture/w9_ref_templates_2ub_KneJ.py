# Referee w9, templates#1: explicit instance realising the proof's rare branch K != J (then necessarily L = I),
# and a hand check that the branch 'i = J != K with L != I' is VACUOUS (K != J forces L = I).
from fractions import Fraction as F
from w9_ref_templates_2ub import tau_756, analyse, check_tuple
x = [F(143,100), F(69,100), F(86,100)]; g = [F(96,100), F(0), F(0)]; h = [F(0), F(40,100), F(58,100)]
print('tau*', tau_756(x, [g, h]))
I, J = 0, 1
a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
Ks = [i for i in range(3) if 2 * x[i] < 3 * b[i]]; Ls = [i for i in range(3) if 2 * x[i] < 3 * a[i]]
print('a', a, 'b', b, 'K set', Ks, 'L set', Ls, {k: check_tuple(k, x, a, b) for k in ('Qb', 'Qa', 'V')})
print('analyse all heavy pairs:', analyse(x, g, h))
