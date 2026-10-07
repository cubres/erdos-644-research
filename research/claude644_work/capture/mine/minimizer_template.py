"""Rigid finite type sets over p parts, tau*>3/4. theta_i = min a_i over i-heavy types (a_i > 4x_i/7),
a^i = the minimiser. Test: template T(A,B,C) with rows (a^A x4, a^B x2, a^C x1) Fano-feasible for some ordered
triple of heavy parts?  Compare with 'any Fano tuple from C'."""
import random, sys, itertools
from upbox_fano import tau_star, fano
from heavy_upbox_test import reps
rng = random.Random(int(sys.argv[2])); p = int(sys.argv[1]); N = int(sys.argv[3]); INTER = int(sys.argv[4])
def inter(x, T): return all(any(a[i]+b[i] > x[i]+1e-12 for i in range(len(x))) for a in T for b in T)
def rtype(x):
    while True:
        w = [rng.random()**1.5 for _ in range(p)]; s = sum(w); a = [v/s for v in w]
        if all(a[i] <= x[i] for i in range(p)): return a
tested = tmpl = anyf = 0; bad = []
while tested < N:
    x = [rng.uniform(0.3, 1.3) for _ in range(p)]
    if sum(x) < 1.75: continue
    m = rng.randint(3, 6); T = [rtype(x) for _ in range(m)]
    if INTER and not inter(x, T): continue
    if any(all(a[i] <= 4*x[i]/7 for i in range(p)) for a in T): continue   # homogeneous case excluded
    t = tau_star(x, T)
    if t <= 0.75: continue
    tested += 1
    mins = {}
    for i in range(p):
        hv = [a for a in T if a[i] > 4*x[i]/7]
        if hv: mins[i] = min(hv, key=lambda a: a[i])
    ok = False
    for A, B, C in itertools.permutations(sorted(mins), 3):
        G = [mins[A], mins[B], mins[C]]
        if fano(x, G, (0,0,1,0,1,2,0)): ok = True; break
    if ok: tmpl += 1
    af = ok or any(fano(x, T, asg) for asg in reps(len(T))) if len(T) <= 5 else ok
    if af: anyf += 1
    if not ok: bad.append((round(t,3), len(mins)))
print(f"p={p} inter={INTER}: tested {tested}; minimiser-template works {tmpl}; any Fano (m<=5) {anyf}; template-fail samples (tau*, #heavy parts): {bad[:10]}")
