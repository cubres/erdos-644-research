import random, itertools, sys
from threebox_fano import fano_lp, REPS
rng = random.Random(int(sys.argv[1]))
def valid(x, th):
    return all(0 < xi for xi in x) and all(4*xi/7 < ti <= xi and ti <= 1 for xi, ti in zip(x, th)) and sum(th) >= 1
def tau(x, th): return sum(xi - ti for xi, ti in zip(x, th))
def fano(x, th): return any(fano_lp(x, th, b) for b in REPS)
best = (0, None)
for restart in range(int(sys.argv[2])):
    while True:
        x = [rng.uniform(0.2, 1.4) for _ in range(3)]
        th = [xi - rng.uniform(0, 3*xi/7) for xi in x]
        if valid(x, th) and not fano(x, th): break
    cur = tau(x, th); step = 0.05
    for it in range(250):
        nx = [xi + rng.gauss(0, step) for xi in x]; nth = [ti + rng.gauss(0, step) for ti in th]
        if not valid(nx, nth): continue
        nt = tau(nx, nth)
        if nt > cur and not fano(nx, nth):
            x, th, cur = nx, nth, nt
        if it % 80 == 79: step *= 0.5
    if cur > best[0]: best = (cur, x, th)
    print(f"restart {restart}: Fano-free tau* {cur:.4f} x={[round(v,4) for v in x]} th={[round(v,4) for v in th]}", flush=True)
print("BEST", best)
