# mutation test: run the e2e chain with T slightly BELOW the claimed threshold; failures expected
import random, sys
from math import ceil
from fractions import Fraction as Fr
import referee_w5_paper_e2e as P
rng = random.Random(5); from collections import Counter
fails = Counter(); ok = 0
for r in range(40, 61):
    T = ceil(Fr(165,200)*r)
    for m in range(0, r//2+1):
        if Fr(m, r) > Fr(23, 50): break
        for y in range(m+1):
            if Fr(m+2*y, r) > Fr(227, 200): break
            for z in range(y+1):
                for _ in range(2):
                    try: P.run_case(r, T, m, y, z, rng); ok += 1
                    except AssertionError as ex: fails[str(ex.args[0])[:40]] += 1
print("ok", ok, "fails", sum(fails.values()), fails.most_common(6))
