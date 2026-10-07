import sys, random
from fractions import Fraction as Fr
import fp_cegar as F, heavylib as h, pairlib as P
seed, N, count = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); p = int(sys.argv[4]) if len(sys.argv) > 4 else 3
rng = random.Random(seed)
fixed = [[Fr(5,4),Fr(5,4),Fr(1,3)], [Fr(6,5),Fr(6,5),Fr(33,100)], [Fr(9,10)]*3, [Fr(1),Fr(1),Fr(1,2)], [Fr(7,10),Fr(4,5),Fr(6,5)], [Fr(31,50)]*3, [Fr(2,3)]*3, [Fr(3,4)]*3]
xs = fixed if p == 3 else []
while len(xs) < count:
    x = [Fr(rng.randint(10, 150), 100) for _ in range(p)]
    if sum(x) > Fr(7,4) + Fr(1,20): xs.append(x)
for x in xs[:count]:
    sel = F.run(x, N, Fr(1,1000), maxit=4000, log=lambda s: print(s, flush=True))
    if isinstance(sel, list):
        print("  TYPES", [[str(v) for v in a] for a in sel], flush=True)
        print("  exact tau*", h.tau_star_fast(x, sel), "fano", F.fano_find(x, sel), "pair", P.any_pair([float(v) for v in x], [[float(v) for v in a] for a in sel]), flush=True)
