"""OTP-3: three parts, three types, type j heavy EXACTLY at part j (sum 1 or <=1).  Minimise the Fano margin
(row slack ignored) subject to tau* >= TGT.  Negative => Fano-free OTP-3 counterexample."""
import random, sys, heavylib as h
seed, iters, SUM1 = map(int, sys.argv[1:4]); TGT = 0.7505; rng = random.Random(seed); p = 3
def valid(x, T):
    if any(v < 0.005 for v in x): return False
    for j, a in enumerate(T):
        if any(v < -1e-12 for v in a) or sum(a) > 1 + 1e-9 or (SUM1 and sum(a) < 1 - 1e-9) or any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if [i for i in range(p) if 7*a[i] > 4*x[i]] != [j]: return False
    return True
def fix(a):
    a = [max(0.0, v) for v in a]; s = sum(a)
    return [v/s for v in a] if (SUM1 or s > 1) and s > 0 else a
while True:
    x = [rng.uniform(0.2, 1.5) for _ in range(p)]
    T = []
    for j in range(p):
        a = [0.0]*p; a[j] = rng.uniform(4*x[j]/7, min(1, x[j])); rest = (1 - a[j]) if SUM1 else rng.uniform(0, 1 - a[j])
        w = [rng.random() if i != j else 0 for i in range(p)]; S = sum(w)
        for i in range(p):
            if i != j: a[i] = rest*w[i]/S
        T.append(a)
    if valid(x, T) and h.tau_star(x, T) >= TGT: break
cur = h.fano_margin(x, T)[0]; step = 0.03
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(p); nT[j] = fix([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = h.fano_margin(nx, nT)[0]
    if f > cur or h.tau_star(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 20000 == 19999: step *= 0.6
    if cur < -1e-9: break
print("END fm %.5f tau* %.4f x %s T %s" % (cur, h.tau_star(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
