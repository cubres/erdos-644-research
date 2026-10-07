"""Experiment 2: Zykov symmetrisation process.
H -> repeatedly: pick admissible Zykov move (tau >= t0, (7,2)) between different
exchangeability classes; apply; then class-saturate (add whole orbits of k-sets
under the product of the symmetric groups of the current classes while (7,2)).
Report final class structure."""
import random, sys, itertools, collections
from deep_symm_lib import *

def orbit(E, cls, n):
    # all sets with same intersection sizes with each class
    parts = []
    for c in cls:
        a = sum((E >> x) & 1 for x in c)
        parts.append([mask(s) for s in itertools.combinations(c, a)])
    out = []
    for combo in itertools.product(*parts):
        m = 0
        for s in combo: m |= s
        out.append(m)
    return out

def class_saturate(H, n, k, rng):
    S = set(H)
    cls = exch_classes(list(S), n)
    cand = [mask(c) for c in itertools.combinations(range(n), k)]
    rng.shuffle(cand)
    changed = True
    while changed:
        changed = False
        for E in cand:
            if E in S: continue
            orb = orbit(E, cls, n)
            new = [F for F in orb if F not in S]
            T = list(S) + new
            if is72(T, n):
                S |= set(new); changed = True
        cls2 = exch_classes(list(S), n)
        if cls2 != cls:
            cls = cls2; changed = True
    return list(S)

def process(H, n, k, t0, rng, verbose=True):
    steps = 0
    while True:
        cls = exch_classes(H, n)
        rep = {x: i for i, c in enumerate(cls) for x in c}
        moves = []
        for u in range(n):
            for v in range(n):
                if u == v or rep[u] == rep[v]: continue
                Z = zykov(H, u, v)
                if is72(Z, n) and tau(Z, n) >= t0:
                    moves.append((u, v, Z))
        if not moves:
            return H, cls, steps
        u, v, Z = rng.choice(moves)
        H = class_saturate(Z, n, k, rng)
        steps += 1
        if verbose:
            print(f"  step {steps}: clone {u}<-{v}; |H|={len(H)} tau={tau(H,n)} classes={[len(c) for c in exch_classes(H,n)]}", flush=True)

if __name__ == '__main__':
    n, k, trials, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    tally = collections.Counter()
    for tr in range(trials):
        H = saturate_uniform(n, k, rng)
        t0 = tau(H, n)
        cls0 = exch_classes(H, n)
        print(f"trial {tr}: start |H|={len(H)} tau={t0} classes={[len(c) for c in cls0]}")
        Hf, clsf, steps = process(H, n, k, t0, rng)
        tf = tau(Hf, n)
        print(f"   final: |H|={len(Hf)} tau={tf} classes={[len(c) for c in clsf]} steps={steps}")
        tally[tuple(len(c) for c in clsf)] += 1
    print("TALLY", dict(tally))
