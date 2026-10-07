"""RESIDUAL REGIME search: parts 0=A,1=B heavy, parts>=2 light.  Every type SUPER-heavy (>2x/3) at A or B
(so no Fano tuple, Arc Lemma).  Minimise pair_margin subject to tau* >= TGT.  Negative => FP counterexample."""
import random, sys, heavylib as h, pairlib as P
seed, iters, nl, m = map(int, sys.argv[1:5]); TGT = 0.7505; rng = random.Random(seed); p = 2 + nl
def valid(x, T):
    if any(v < 0.01 for v in x): return False
    for a in T:
        if a is None or any(v < -1e-12 for v in a) or abs(sum(a)-1) > 1e-9 or any(a[i] > x[i]+1e-12 for i in range(p)): return False
        if any(7*a[i] > 4*x[i] for i in range(2, p)): return False
        sA, sB = 3*a[0] > 2*x[0], 3*a[1] > 2*x[1]
        if sA == sB: return False
        if (not sA and 7*a[0] > 4*x[0]) or (not sB and 7*a[1] > 4*x[1]): return False
    return True
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
tries = 0
if nl == 1:
    base_x = [1.2, 1.2, 0.33]; base_T = [[.82,0,.18],[0,.82,.18],[.89,.11,0],[.11,.89,0]]
else:
    base_x = [1.2, 1.2, 0.2, 0.2]; base_T = [[.82,0,.09,.09],[0,.82,.09,.09],[.89,.11,0,0],[.11,.89,0,0]]
x = list(base_x); T = [list(a) for a in base_T]
while len(T) < m:
    k = len(T) % 2; a = list(base_T[2 + k]); T.append(proj([v + rng.gauss(0, 0.01) for v in a]))
while not (valid(x, T) and h.tau_star_fast(x, T) >= TGT):
    tries += 1
    x = list(base_x); T = [list(a) for a in base_T]
    while len(T) < m:
        k = len(T) % 2; a = list(base_T[2 + k]); T.append(proj([max(0, v + rng.gauss(0, 0.01)) for v in a]))
    if tries > 1000: break
while not (valid(x, T) and h.tau_star_fast(x, T) >= TGT):
    tries += 1
    x = [rng.uniform(1.1, 1.5), rng.uniform(1.1, 1.5)] + [rng.uniform(0.05, 0.5) for _ in range(nl)]
    T = []
    for k in range(m):
        j = k % 2; a = [0.0]*p; a[j] = rng.uniform(2*x[j]/3, min(1, x[j]))
        w = [rng.random()**2 if i != j else 0 for i in range(p)]; S = sum(w)
        for i in range(p):
            if i != j: a[i] = (1-a[j])*w[i]/S
        T.append(a)
    if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
cur = P.pair_margin(x, T); step = 0.02
print("start pair margin", cur, "tau*", h.tau_star_fast(x, T), "tries", tries, flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.25:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    b = P.pair_margin(nx, nT)
    if b > cur: continue
    if h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, b
    if it % 3000 == 2999:
        print(it, "pair margin", round(cur, 5), "tau*", round(h.tau_star_fast(x, T), 4), "x", [round(v, 4) for v in x], flush=True)
        if it % 15000 == 14999: step *= 0.7
    if cur < -1e-9:
        print("RR-FP-CEX tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True); break
print("END pm", cur, "tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True)
