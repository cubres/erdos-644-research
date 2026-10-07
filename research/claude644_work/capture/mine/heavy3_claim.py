"""CLAIM TEST: rigid finite type set C over p parts, no type with all fills <= 4/7, tau*(C) > 3/4, and at least
three parts host heavy types (fill > 4/7). theta_i := min a_i over i-heavy types, a^i its minimiser.
Is template T(A,B,C) with rows (a^A x4, a^B x2, a^C x1) Fano-feasible for some ordered triple?"""
import random, sys, itertools
from upbox_fano import tau_star, fano
rng = random.Random(int(sys.argv[2])); p = int(sys.argv[1]); N = int(sys.argv[3]); INTER = int(sys.argv[4])
def inter(x, T): return all(any(a[i]+b[i] > x[i]+1e-12 for i in range(len(x))) for a in T for b in T)
def rtype(x):
    while True:
        w = [rng.random()**rng.choice([1,1.5,3]) for _ in range(p)]; s = sum(w); a = [v/s for v in w]
        if all(a[i] <= x[i] for i in range(p)): return a
tested = ok_n = 0; fails = []
while tested < N:
    x = [rng.uniform(0.25, 1.4) for _ in range(p)]
    if sum(x) < 1.75: continue
    m = rng.randint(3, 8); T = [rtype(x) for _ in range(m)]
    if INTER and not inter(x, T): continue
    if any(all(a[i] <= 4*x[i]/7 for i in range(p)) for a in T): continue
    mins = {}
    for i in range(p):
        hv = [a for a in T if a[i] > 4*x[i]/7]
        if hv: mins[i] = min(hv, key=lambda a: a[i])
    if len(mins) < 3: continue
    t = tau_star(x, T)
    if t <= 0.75: continue
    tested += 1
    ok = any(fano(x, [mins[A], mins[B], mins[C]], (0,0,1,0,1,2,0)) for A, B, C in itertools.permutations(sorted(mins), 3))
    if ok: ok_n += 1
    else:
        fails.append((round(t,4), [round(v,3) for v in x], [[round(v,3) for v in a] for a in T])); print("FAIL", fails[-1], flush=True)
print(f"p={p} inter={INTER}: tested {tested} with >=3 heavy parts and tau*>3/4; minimiser template works {ok_n}; fails {len(fails)}", flush=True)
