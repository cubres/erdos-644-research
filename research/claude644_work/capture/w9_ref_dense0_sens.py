#!/usr/bin/env python3
"""Referee w9 [dense#0] sensitivity: (1) allow covering cell pairs -> brute force must detect 2-pierceable tuples;
(2) adversarial rounding shows s=3 is tight for Fano windows (s=2 fails)."""
import random, sys
import w9_ref_dense0_typeclosed as T
from fractions import Fraction as Fr
FULL = T.FULL
def bad_cells(rng):
    cells = [frozenset(rng.sample(range(7), rng.randint(3, 6))) for _ in range(rng.randint(4, 9))]
    cells.append(frozenset(range(7)) - cells[0]); return list(set(c for c in cells if c and c != FULL))
T.rand_cells = bad_cells
sys.argv = ['x', '7', '1500']
T.main()
# (2) adversarial rounding example: Fano, one part, row j window = 4 cells with mass a+0.99, other 3 cells absorb deficit
a = 5; m = {c: Fr(a) + Fr(99, 100) for c in range(4)}
rest = [Fr(201, 100), Fr(201, 100), Fr(202, 100)]
n = sum(m.values()) + sum(rest)
print('n =', n, '(integer:', n.denominator == 1, ')')
w = sum(m.values()); u = int(w)
floors = [int(x) for x in list(m.values()) + rest]
deficit = int(n) - sum(floors)
rounded_window = sum(floors[:4])  # deficit placed on the 3 outside cells
print('window', w, 'u=floor', u, 'rounded window', rounded_window, 'deficit', deficit, 'u-rounded =', u - rounded_window)
