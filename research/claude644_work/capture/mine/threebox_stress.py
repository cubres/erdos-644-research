import random, sys, collections
from threebox_fano import fano_lp, REPS
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
N = int(sys.argv[1])
def sample_boundary():
    while True:
        x = [rng.choice([rng.uniform(0.25, 1.3), rng.uniform(0.55, 0.9)]) for _ in range(3)]
        # push theta close to the Fano bound 4x/7 from above, and tau* just above 3/4
        th = [xi - rng.uniform(0, 3*xi/7) for xi in x]
        if sum(th) < 1 or any(t > 1 for t in th) or any(t <= 4*xi/7 for t, xi in zip(th, x)): continue
        d = sum(xi - ti for xi, ti in zip(x, th))
        if 0.75 < d < 0.78: return x, th, d
wins = collections.Counter(); fails = 0
cases = [([0.8]*3, [0.54]*3), ([0.8]*3, [0.545]*3), ([0.8]*3, [0.549]*3)]
for x, th in cases:
    w = [b for b in REPS if fano_lp(x, th, b)]
    print("C_theta", th[0], "tau*", round(sum(x)-sum(th),4), "fano assignments:", len(w), w[:3], flush=True)
for s in range(N):
    x, th, d = sample_boundary()
    w = [b for b in REPS if fano_lp(x, th, b)]
    if not w:
        fails += 1; print("NO FANO", [round(v,4) for v in x], [round(v,4) for v in th], round(d,4), flush=True)
    else:
        for b in w: wins[b] += 1
print("samples", N, "fails", fails)
print("most frequent winning assignments:", wins.most_common(8))
