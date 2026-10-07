# w9_ref_tc2_literal_a.py -- referee [typeclosed#2]: statement (a) read literally lacks the hypotheses
# "tau*>3/4 and NO type is 4/7-light in every part" (homogeneous Fano already dealt with).  Instance:
from fractions import Fraction as F
from w9_ref_tc2_lib import *
x = (F(1, 5), F(7, 5), F(7, 5))
a = (F(0), F(1, 20), F(19, 20)); b = (F(0), F(19, 20), F(1, 20)); ell = (F(1, 10), F(9, 20), F(9, 20))
C = [a, b, ell]
print("tau*(C) =", tau_star(C, x), " tau*({a,b}) =", tau_star([a, b], x))
print("Q_b(b pencil, a quad):", Qb_ok(b, a, x), " Q_a:", Qb_ok(a, b, x))
print("ell <= 4x/7 everywhere:", all(ell[i] <= F(4, 7) * x[i] for i in range(3)),
      " homogeneous Fano (7 rows ell) valid:", fano_ok([ell] * 7, x))
print("ell super-heavy somewhere:", any(ell[i] > F(2, 3) * x[i] for i in range(3)))
print("V(a,b):", V_ok(a, b, x))
