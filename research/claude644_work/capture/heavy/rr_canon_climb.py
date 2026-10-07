"""RR (1 light part), non-intersecting allowed: minimise the CANONICAL pair margin = best pair template (42 fns)
among {alpha, beta, a, b} (minimisers + L-small gap-maximisers, lam* = x_L - max(alpha_L,beta_L)), subject to
tau* >= TGT.  Positive margin => a canonical 4-type argument might prove Th for 2 heavy parts + 1 light part."""
import random, sys, numpy as np, heavylib as h, pairlib as P
seed, iters, m = map(int, sys.argv[1:4]); TGT = 0.7505; rng = random.Random(seed); p = 3
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T):
    if any(v < 0.01 for v in x): return False
    for a in T:
        if a is None or any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if 7*a[2] > 4*x[2]: return False
        sA, sB = 3*a[0] > 2*x[0], 3*a[1] > 2*x[1]
        if sA == sB: return False
        if (not sA and 7*a[0] > 4*x[0]) or (not sB and 7*a[1] > 4*x[1]): return False
    return any(3*a[0] > 2*x[0] for a in T) and any(3*a[1] > 2*x[1] for a in T)
def canon(x, T):
    CA = [a for a in T if 3*a[0] > 2*x[0]]; CB = [a for a in T if 3*a[1] > 2*x[1]]
    al = min(CA, key=lambda a: a[0]); be = min(CB, key=lambda a: a[1])
    lam = x[2] - max(al[2], be[2])
    SA = [a for a in CA if a[2] <= lam + 1e-12]; SB = [b for b in CB if b[2] <= lam + 1e-12]
    S = [al, be]
    if SA: S.append(min(SA, key=lambda a: a[0]))
    if SB: S.append(min(SB, key=lambda b: b[1]))
    return S
def cm(x, T): return P.pair_margin(x, canon(x, T))
x = [1.2, 1.2, 0.33]; T = [[.82,0,.18],[0,.82,.18],[.89,.11,0],[.11,.89,0]]
while len(T) < m: T.append(proj([v + rng.gauss(0, 0.01) for v in T[2 + len(T) % 2]]))
assert valid(x, T) and h.tau_star_fast(x, T) >= TGT
cur = cm(x, T); step = 0.02
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = cm(nx, nT)
    if f > cur or h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 10000 == 9999: step *= 0.7
    if cur < -1e-9: break
print("END canon margin %.5f full pair margin %.5f tau* %.4f x %s T %s" % (cur, P.pair_margin(x, T), h.tau_star_fast(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
