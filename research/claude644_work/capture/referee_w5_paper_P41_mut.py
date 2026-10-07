# referee_w5_paper_P41_mut.py -- sensitivity check for referee_w5_paper_P41_e2e.py:
# run the same case chain with a budget BELOW the claimed one (T = ceil(0.825 r)); failures are expected.
import random
from math import ceil
from fractions import Fraction as Fr
from collections import Counter
import referee_w5_paper_P41_e2e as P
rng = random.Random(5); fails = Counter(); ok = 0
for r in range(40, 61):
    T = ceil(Fr(165, 200) * r)
    for m in range(0, r // 2 + 1):
        if Fr(m, r) > Fr(23, 50): break
        for y in range(m + 1):
            if Fr(m + 2*y, r) > Fr(227, 200): break
            for z in range(y + 1):
                for _ in range(2):
                    try:
                        P.run_case(r, T, m, y, z, rng); ok += 1
                    except AssertionError as ex:
                        fails[str(ex.args[0][0] if ex.args else "?")[:30]] += 1
print("ok", ok, "fails", sum(fails.values()), fails.most_common(8))
