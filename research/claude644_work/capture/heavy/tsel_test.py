"""Multi-type reduced instances: is there SOME selection alpha in C_A, beta in C_B, gamma in C_C (distinct heavy
parts A,B,C) making T(A,B,C) feasible?"""
import random, sys, itertools, heavylib as h
TPL = (1,1,2,0,0,0,0)
def tsel(x, T):
    hh = len(x)
    CH = {i: [a for a in T if 7*a[i] > 4*x[i]] for i in range(hh)}
    for A, B, C in itertools.permutations(range(hh), 3):
        for al in CH[A]:
            for be in CH[B]:
                for ga in CH[C]:
                    if h.fano_rows_ok(x, [(al, be, ga)[0] if k == 0 else (al, be, ga)[k] for k in TPL]):
                        return (A, B, C, al, be, ga)
    return None
if __name__ == '__main__':
    insts = [([0.82,0.714,1.112], [[.503,.487,.01],[.507,0,.493],[.139,.169,.691],[.003,.506,.492]]),
     ([1.072,.555,.774], [[0.414, 0.128, 0.458], [0.714, 0.129, 0.156], [0.64, 0.0, 0.36], [0.268, 0.185, 0.547], [0.546, 0.439, 0.015], [0.625, 0.375, 0.0]])]
    for x, T in insts: print(tsel(x, T))
    hh, m, N, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
    tested = fails = 0
    while tested < N:
        x = [rng.uniform(0.3, 1.5) for _ in range(hh)]
        T = []
        for _ in range(m):
            w = [rng.random()**rng.choice([1,2,4,8]) for _ in range(hh)]; S = sum(w); a = [min(x[i], v/S) for i, v in enumerate(w)]
            T.append(a)
        if any(h.is_homog(x, a) for a in T) or len(h.heavy_parts(x, T)) < hh: continue
        t = h.tau_star_fast(x, T)
        if t <= 0.75: continue
        tested += 1
        if tsel(x, T) is None:
            fails += 1; print("NOSEL tau*=%.4f fano=%s x=%s T=%s" % (t, h.any_fano_np(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
    print(f"h={hh} m={m}: tested {tested}, no T-selection {fails}")
