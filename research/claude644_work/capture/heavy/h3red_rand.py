"""H3-REDUCED test: types on h heavy parts, sum<=1 (light mass discarded), each type heavy somewhere,
every part hosts a heavy type, tau*_H > 3/4 (H-maps)  ==> Fano tuple?  random + reports failures."""
import random, sys, heavylib as h
h_, m, N, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
tested = fails = 0
while tested < N:
    x = [rng.uniform(0.3, 1.5) for _ in range(h_)]
    T = []
    for _ in range(m):
        s = rng.uniform(0.6, 1.0)
        w = [rng.random()**rng.choice([1,2,4]) for _ in range(h_)]; S = sum(w); a = [s*v/S for v in w]
        a = [min(a[i], x[i]) for i in range(h_)]
        T.append(a)
    if any(h.is_homog(x, a) for a in T): continue
    if len(h.heavy_parts(x, T)) < h_: continue
    t = h.tau_star_fast(x, T)
    if t <= 0.75: continue
    tested += 1
    if not h.any_fano_np(x, T):
        fails += 1; print("FAIL tau*=%.4f x=%s T=%s" % (t, [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
print(f"h={h_} m={m}: tested {tested}, Fano-free {fails}")
