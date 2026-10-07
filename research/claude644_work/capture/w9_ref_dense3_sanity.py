#!/usr/bin/env python3
"""w9_ref_dense3_sanity.py -- sanity of w9_ref_dense3_lib: (1) part_ok == class-size LP (Lemma 7.63) on random
loads [scipy HiGHS as a cross-check only]; (2) tau* of simple type sets against hand values."""
import random
from fractions import Fraction as Fr
from scipy.optimize import linprog
from w9_ref_dense3_lib import *
rnd = random.Random(5); bad = 0
for _ in range(3000):
    cap = rnd.randint(3, 20)
    z = [rnd.randint(0, cap + 2) for _ in range(7)]
    A = [[-(1 if p not in LINES[l] else 0) for p in range(7)] for l in range(7)]
    res = linprog([1]*7, A_ub=A, b_ub=[-v for v in z], bounds=[(0, None)]*7, method='highs')
    lp = res.status == 0 and res.fun <= cap + 1e-9
    bad += lp != part_ok([Fr(v) for v in z], cap)
print('LP mismatches', bad)
# single type (1,1) caps (2,2): free boxes: w0<1 or w1<1 -> sup = 1+2 = 3 -> tau* = 1
print('tau* {(1,1)} caps(2,2) =', tau_star([(Fr(1), Fr(1))], (2, 2)), 'expect 1')
# anchor (3,0) + (1,2) caps (3,3): block anchor needs w0<3 ; block (1,2): w0<1 or w1<2 -> max(1+3, 3+2)=5 -> tau*=1
print('tau* =', tau_star([(Fr(3), Fr(0)), (Fr(1), Fr(2))], (3, 3)), 'expect 1')
# 1-part: types of size t, cap N: sup free = t -> tau* = N - t
print('tau* =', tau_star([(Fr(4),)], (10,)), 'expect 6')
