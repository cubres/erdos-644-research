"""Start from a Fano-free high-tau* family (H3s-cex or W+light) and minimise the (normalised) pair margin while
keeping Fano-freeness (fano margin < 0) and tau* >= TGT.  pair margin < 0 => FP counterexample candidate."""
import random, sys, heavylib as h, pairlib as P
seed, iters, start, extra = map(int, sys.argv[1:5]); TGT = 0.7505; rng = random.Random(seed)
if start == 0:
    x = [0.861, 1.44, 0.741]; T = [[.664, 0, .336], [.019, .981, 0], [.424, 0, .576]]
elif start == 1:
    x = [1.2, 1.2, 0.33]; T = [[.82,0,.18],[0,.82,.18],[.89,.11,0],[.11,.89,0]]
else:
    x = [0.861, 1.44, 0.741, 0.3]; T = [[.664, 0, .336, 0], [.019, .981, 0, 0], [.424, 0, .576, 0]]
p = len(x)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
for _ in range(extra):
    for _ in range(10000):
        a = proj([rng.random()**3 for _ in range(p)])
        if all(a[i] <= x[i] for i in range(p)) and h.fano_margin(x, T + [a])[0] < 0 and h.tau_star(x, T + [a]) >= TGT:
            T = T + [a]; break
m = len(T)
def valid(x, T): return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(p)) for a in T)
cur = P.pair_margin(x, T); step = 0.02
print("start pm", cur, "fm", h.fano_margin(x, T)[0], "tau*", h.tau_star(x, T), "m", m, flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    b = P.pair_margin(nx, nT)
    if b > cur: continue
    if h.fano_margin(nx, nT)[0] >= 0 or h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, b
    if it % 10000 == 9999: step *= 0.7
    if cur < -1e-9:
        print("FP-CEX", h.tau_star_fast(x, T), x, T, flush=True); break
print("END pm %.5f fm %.5f tau* %.4f x %s T %s" % (cur, h.fano_margin(x, T)[0], h.tau_star_fast(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
