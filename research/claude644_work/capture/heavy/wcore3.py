"""W-core + third type: alpha=(1-s,0,s) [A], gamma=(s2,0,1-s2) [C], beta=(b,1-b,0) [B]. Random search for
simple-heavy, tau*>3/4, Fano-free."""
import random, sys, heavylib as h, pairlib as P
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); best = (-1,)
for t in range(N):
    xA, xB, xC = rng.uniform(0.6, 1.5), rng.uniform(0.3, 1.5), rng.uniform(0.6, 1.5)
    s, s2, b = rng.uniform(0, 0.5), rng.uniform(0, 0.5), rng.uniform(0, 0.6)
    x = [xA, xB, xC]; T = [[1-s, 0, s], [b, 1-b, 0], [s2, 0, 1-s2]]
    if any(a[i] > x[i] for a in T for i in range(3)): continue
    if [[i for i in range(3) if 7*a[i] > 4*x[i]] for a in T] != [[0], [1], [2]]: continue
    tau = h.tau_star(x, T)
    if tau <= best[0]: continue
    if h.any_fano_np(x, T): continue
    best = (tau, x, T); print("Fano-free", round(tau, 4), [round(v, 4) for v in x], [[round(v, 4) for v in a] for a in T], "pm", round(P.pair_margin(x, T), 4), flush=True)
print("BEST", best)
