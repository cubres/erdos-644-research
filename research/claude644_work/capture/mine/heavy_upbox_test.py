"""Up-box unions: generator j heavy in part j (j=0..m-1, m=p) with lower bounds on other parts.
Test: tau*>3/4 => template T(A,B,C) (some ordered triple of generators) Fano-feasible?  Also any Fano."""
import random, sys, itertools
from upbox_fano import tau_star, fano
rng = random.Random(int(sys.argv[2])); p = int(sys.argv[1]); N = int(sys.argv[3])
def template(A,B,C): return (A,A,B,A,B,C,A)
tested = fails_t = fails_any = 0
from intersecting_climb import reps
while tested < N:
    x = [rng.uniform(0.3, 1.3) for _ in range(p)]
    gens = []
    for j in range(p):
        c = [0.0]*p
        c[j] = rng.uniform(4*x[j]/7, x[j])            # heavy coordinate
        for i in range(p):
            if i != j: c[i] = rng.uniform(0, 0.35) * x[i] * (rng.random() < 0.6)   # light lower bounds
        s = sum(c)
        if s > 1: continue
        gens.append(c)
    if len(gens) < p: continue
    t = tau_star(x, gens)
    if t <= 0.75: continue
    tested += 1
    okt = any(fano(x, gens, template(*tr)) for tr in itertools.permutations(range(p), 3))
    oka = okt or any(fano(x, gens, a) for a in reps(p))
    if not okt: fails_t += 1
    if not oka:
        fails_any += 1; print("NO FANO: tau*=%.4f x=%s gens=%s" % (t, [round(v,3) for v in x], [[round(v,3) for v in c] for c in gens]), flush=True)
print(f"p={p}: tested {tested}, template fails {fails_t}, no Fano at all {fails_any}")
