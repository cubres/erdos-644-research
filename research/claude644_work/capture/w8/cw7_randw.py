import sys, random, time
from fractions import Fraction as Fr
from cw7_fixedw import run
rng = random.Random(int(sys.argv[1])); n = int(sys.argv[2]); iters = int(sys.argv[3])
t0 = time.time()
for it in range(iters):
    mode = rng.random()
    if mode < 0.3:
        w = [Fr(rng.randint(1, 50), 100) for _ in range(n)]
    elif mode < 0.6:
        w = [Fr(rng.choice([1,2,3,4,5,6]), rng.choice([4,6,8,12])) for _ in range(n)]
        w = [min(x, Fr(1,2)) for x in w]
    else:
        base = [Fr(163,500),Fr(13,50),Fr(8,125),Fr(67,200),Fr(223,500),Fr(493,1000)]
        w = base + [Fr(rng.randint(1,50),100) for _ in range(n-6)]
    E, k = run(w, 7)
    if E:
        print('FOUND', [str(x) for x in w], [''.join(str(e>>i&1) for i in range(n)) for e in E], flush=True)
        break
    if it % 20 == 0: print('it', it, round(time.time()-t0), flush=True)
print('done')
