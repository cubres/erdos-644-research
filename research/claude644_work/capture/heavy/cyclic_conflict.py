"""Search one-type-per-class super-heavy families (3 parts) whose Fano-freeness comes from a CYCLIC conflict
{AAB,BBC,CCA} (not a mutual one); report tau* and the pair margin."""
import random, sys, itertools, heavylib as h, pairlib as P
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); best = (-1,); cnt = 0
def forb(x, a, b):   # pattern (a,a,b) forbidden somewhere?
    return any(2*a[i] + b[i] > 2*x[i] + 1e-12 for i in range(3))
for t in range(N):
    x = [rng.uniform(0.6, 1.5) for _ in range(3)]
    T = []
    for j in range(3):
        a = [0.0]*3; a[j] = rng.uniform(2*x[j]/3, min(1, x[j]))
        u = rng.random(); o = [i for i in range(3) if i != j]
        a[o[0]] = (1 - a[j])*u; a[o[1]] = (1 - a[j])*(1-u)
        T.append(a)
    if any(a[i] > x[i] for a in T for i in range(3)): continue
    if [[i for i in range(3) if 3*a[i] > 2*x[i]] for a in T] != [[0],[1],[2]]: continue
    A, B, C = T
    mutual = (forb(x,A,B) and forb(x,B,A)) or (forb(x,A,C) and forb(x,C,A)) or (forb(x,B,C) and forb(x,C,B))
    cyc = (forb(x,A,B) and forb(x,B,C) and forb(x,C,A)) or (forb(x,A,C) and forb(x,B,A) and forb(x,C,B))
    if mutual or not cyc: continue
    cnt += 1
    tau = h.tau_star(x, T)
    if tau > best[0]:
        best = (tau, x, T); print("cyclic-conflict: tau* %.4f fano %s pair margin %.4f x %s T %s" % (tau, h.any_fano_np(x, T), P.pair_margin(x, T), [round(v,3) for v in x], [[round(v,3) for v in a] for a in T]), flush=True)
print("found", cnt, "BEST", best[0])
