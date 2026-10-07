"""Hill-climb (simulated annealing) over base types of orbit families at the tightest capacity,
maximising the bad-tuple margin lambda* (min capacity scaling admitting a bad tuple).
lambda* > 1 at tau* > 3/4 would be a counterexample candidate (then verify exactly).
Discovery only.  usage: p grp nbase iters seed D"""
import sys, random, time, json, math
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_margin
from w4_typeclosed_orbit_search import orbit, cyclic, dihedral, full
from w4_typeclosed_orbit_tight import tightest_X

def evaluate(bases, group, p, D):
    X = tightest_X(bases, group, p, D)
    if X is None: return None
    A = sorted(set(t for b in bases for t in orbit(b, group)))
    if any(all(7*a[i] <= 4*X for i in range(p)) for a in A): return (0.0, X, A, None)
    xf = [F(X, D)]*p; An = [tuple(F(v, D) for v in a) for a in A]
    r = bad_tuple_margin(An, xf, time_limit=60)
    if r[0] is None: return None
    return (r[0], X, A, r[1])

def mutate(b, rng, D):
    b = list(b); p = len(b)
    for _ in range(rng.randint(1, 3)):
        i, j = rng.sample(range(p), 2)
        k = rng.randint(1, max(1, D//10))
        k = min(k, b[i])
        b[i] -= k; b[j] += k
    return tuple(b)

def run(p, grp, nb, iters, seed, D):
    rng = random.Random(seed)
    group = {'cyc': cyclic, 'dih': dihedral, 'sym': full}[grp](p)
    def rnd():
        w = [rng.random()**2 if rng.random() < 0.7 else 0 for _ in range(p)]
        if sum(w) == 0: w[0] = 1
        a = [int(D*v/sum(w)) for v in w]; a[w.index(max(w))] += D - sum(a); return tuple(a)
    cur = [rnd() for _ in range(nb)]
    ev = evaluate(cur, group, p, D)
    while ev is None:
        cur = [rnd() for _ in range(nb)]; ev = evaluate(cur, group, p, D)
    best = (ev[0], cur, ev); T0 = 0.05; t0 = time.time()
    for it in range(iters):
        cand = list(cur); k = rng.randrange(nb); cand[k] = mutate(cand[k], rng, D)
        e2 = evaluate(cand, group, p, D)
        if e2 is None: continue
        T = T0*(1 - it/iters) + 1e-4
        if e2[0] >= ev[0] or rng.random() < math.exp((e2[0]-ev[0])/T):
            cur, ev = cand, e2
            if ev[0] > best[0]:
                best = (ev[0], list(cur), ev)
                print(f'it {it} lambda*={ev[0]:.4f} X={ev[1]} bases={cur} assign={ev[3]} ({time.time()-t0:.0f}s)', flush=True)
    return best

if __name__ == '__main__':
    p, grp, nb, iters, seed, D = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    b = run(p, grp, nb, iters, seed, D)
    print('BEST', b[0], b[1], 'X', b[2][1])
