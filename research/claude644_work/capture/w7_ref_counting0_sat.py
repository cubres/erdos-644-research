#!/usr/bin/env python3
"""w7_ref_counting0_sat.py n b -- exact SAT (pysat): can 7 blocks of size b on n points cover every pair except the
single pair {0,1} (which no block contains)?  SAT <=> K_n^(n-b) has a 7-tuple with (|P7|,|Pi7|)=(2,1)."""
import sys, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
n, b = int(sys.argv[1]), int(sys.argv[2])
pool = IDPool(); cl = []
x = lambda v, j: pool.id(('x', v, j)); c = lambda u, v, j: pool.id(('c', u, v, j))
for j in range(7):
    cl += CardEnc.equals([x(v, j) for v in range(n)], bound=b, vpool=pool, encoding=EncType.seqcounter).clauses
for u, v in itertools.combinations(range(n), 2):
    if (u, v) == (0, 1):
        for j in range(7): cl.append([-x(0, j), -x(1, j)])
        continue
    for j in range(7):
        cl += [[-c(u, v, j), x(u, j)], [-c(u, v, j), x(v, j)]]
    cl.append([c(u, v, j) for j in range(7)])
s = Cadical153(bootstrap_with=cl); r = s.solve()
print('n', n, 'b', b, '(2,1) achievable:', r)
if r:
    m = set(l for l in s.get_model() if l > 0)
    blocks = [sorted(v for v in range(n) if x(v, j) in m) for j in range(7)]
    print(blocks)
    # exact recheck
    unc = [(u, v) for u, v in itertools.combinations(range(n), 2) if not any(u in B and v in B for B in blocks)]
    print('uncovered pairs', unc)
