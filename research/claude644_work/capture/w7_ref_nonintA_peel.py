"""Referee w7 (nonintA): exact check of the PEELING dichotomy of notes_nonint.md checkpoint 3.
For random H and lambda: greedily delete E with h(E, D(E) n remaining) <= lambda, orienting its remaining Gamma-edges
out of E.  Verify: (1) if everything is peeled, the orientation covers every disjoint pair exactly once, every
Out(E) has h <= lambda, and the Theorem A' copy family is intersecting with tau >= tau(H) and rank <= max(k,t)+lambda;
(2) otherwise the leftover core S is nonempty and every E in S has h(E, D(E) n S) > lambda; and (3) the result
(peelable or not) does not depend on the deletion order (monotonicity of h) -- checked by a second random order.
Usage: python3 w7_ref_nonintA_peel.py TRIALS SEED
"""
import random, sys, itertools
from w7_ref_nonintA import tau, has_cover, disjoint_pairs, pad, hcost, build, rand_family

def peel(H, t, star, lam, rng):
    dis = disjoint_pairs(H)
    nb = {i: set() for i in range(len(H))}
    for i, j in dis:
        nb[i].add(j); nb[j].add(i)
    rem = set(i for p in dis for i in p)
    orient = {}
    while True:
        cand = [E for E in rem if (not (nb[E] & rem)) or hcost([star[F] for F in sorted(nb[E] & rem)], t) <= lam]
        if not cand:
            return orient, rem
        E = rng.choice(cand)
        outs = sorted(nb[E] & rem)
        if outs:
            orient[E] = outs
        rem.discard(E)

def main():
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed); stats = {'peeled': 0, 'core': 0, 'fail': 0}
    for tr in range(trials):
        n = rng.randint(5, 8); k = rng.randint(2, 4); m = rng.randint(4, 9)
        H = rand_family(rng, n, k, m)
        dis = disjoint_pairs(H)
        if not dis: continue
        t = tau(H)
        N = set(i for p in dis for i in p)
        star = pad(H, N, t)
        lam = rng.randint(1, 3)
        o1, core1 = peel(H, t, star, lam, rng)
        o2, core2 = peel(H, t, star, lam, rng)
        ok = (core1 == core2)          # the maximal fat core is order independent
        if not core1:
            stats['peeled'] += 1
            cov = sorted(tuple(sorted((a, b))) for a in o1 for b in o1[a])
            ok &= cov == sorted(dis)
            ok &= all(hcost([star[F] for F in o1[E]], t) <= lam for E in o1)
            Hpp, cost = build(H, t, [], o1, star, xmode='h')
            if Hpp is not None:
                ok &= cost <= lam
                ok &= all(a & b for a, b in itertools.combinations(Hpp, 2))
                ok &= max(len(e) for e in Hpp) <= max(k, t) + lam
                ok &= not has_cover(Hpp, t - 1)
        else:
            stats['core'] += 1
            nb = {i: set(j for j in range(len(H)) if not (H[i] & H[j])) for i in core1}
            ok &= all((nb[E] & core1) and hcost([star[F] for F in sorted(nb[E] & core1)], t) > lam for E in core1)
        if not ok:
            stats['fail'] += 1
            print('FAIL', [sorted(e) for e in H], t, lam, core1, core2)
    print('seed', seed, stats)

if __name__ == '__main__':
    main()
