#!/usr/bin/env python3
"""w8_dense_rounding_check.py -- the Fano rounding step of the transfer theorem: if integer loads satisfy the
Lemma 7.63 criterion in a part of capacity n (anchor part: anchor load n on line L), then integer class sizes
c^ >= floor(c) with sum = n exist (E0: classes on L zero) and every window >= load - 3.  Random adversarial test."""
import random
from w8_dense_transfer_e2e import classes_real, round_classes
from w8_dense_lib import LINES, part_ok
rnd = random.Random(7); bad = 0; tested = 0
for it in range(20000):
    n = rnd.randint(1, 60); anchor = rnd.random() < 0.4
    loads = [rnd.randint(0, n) for _ in range(7)]
    if anchor: loads[0] = n
    if not part_ok(loads, n): continue
    tested += 1
    c = classes_real(loads, n, anchor)
    ch = round_classes(c, n)
    if sum(ch) != n or min(ch) < 0: bad += 1; continue
    if anchor and any(ch[q] for q in LINES[0]): bad += 1; continue
    for l in range(7):
        if sum(ch[q] for q in range(7) if q not in LINES[l]) < loads[l] - 3: bad += 1; break
print('tested', tested, 'failures', bad)
