"""adversarial climb against a strategy margin (strat.<name>) in the balanced regime. usage: seed iters m name"""
import random, sys, json, b3lib as B, strat, gen
seed, iters, m, name = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
TGT = 0.7505; rng = random.Random(seed); F = getattr(strat, name)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T):
    if not all(v > 0.005 for v in x): return False
    if not all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(3)) for a in T): return False
    r = B.regime(x, T)
    if r is None: return False
    S, sig, e = r
    return all(e[i]+e[j] <= 0.75 for i in range(3) for j in range(i+1, 3))
x, T = gen.rand_inst(rng, m); tau = B.tau_star(x, T); cur = F(x, T, tau); step = 0.03
print("start", round(cur, 4), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.25:
        i = rng.randrange(3); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    nt = B.tau_star(nx, nT)
    if nt < TGT: continue
    f = F(nx, nT, nt)
    if f > cur: continue
    x, T, cur = nx, nT, f
    if it % 3000 == 2999: step *= 0.7
    if cur < -1e-9: break
r = B.regime(x, T)
print("END %s marg %.5f tau* %.5f e %s" % (name, cur, B.tau_star(x, T), [round(v, 4) for v in r[2]]), flush=True)
print(json.dumps({'x': x, 'T': T, 'obj': cur}), flush=True)
