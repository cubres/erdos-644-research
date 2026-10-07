"""Referee w7 (nonintA): structured instances where h(E,O) < |O| (star centre E0 with many leaves sharing a core),
so the h-cost refinement of Theorem A' is exercised nontrivially (random families almost always have h = |O|).
Orientation: all disjoint pairs involving E0 point out of E0; the remaining pairs random.  Exact checks as in
w7_ref_nonintA.check.  Usage: python3 w7_ref_nonintA_struct.py TRIALS SEED"""
import random, sys
from w7_ref_nonintA import tau, disjoint_pairs, pad, hcost, build, check, rand_orient
def main():
    T, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
    tested = 0; nontriv = 0; fails = 0
    for _ in range(T):
        n = rng.randint(8, 11); k = rng.randint(3, 4)
        pts = list(range(n)); rng.shuffle(pts)
        E0 = frozenset(pts[:rng.randint(2, k)])
        rest = pts[len(E0):]
        core = rest[:rng.randint(1, k - 1)]
        others = rest[len(core):]
        leaves = list({frozenset(core + rng.sample(others, rng.randint(0, k - len(core)))) for _ in range(rng.randint(2, 5))})
        H = list({E0, *leaves, *[frozenset(rng.sample(range(n), rng.randint(2, k))) for _ in range(rng.randint(1, 5))]})
        dis = disjoint_pairs(H)
        if not dis: continue
        t = tau(H)
        i0 = H.index(E0)
        N = set(i for p in dis for i in p)
        star = pad(H, N, t)
        o = rand_orient(rng, [p for p in dis if i0 not in p])
        outs0 = [j for p in dis if i0 in p for j in p if j != i0]
        if outs0:
            o[i0] = outs0
        Hpp, cost = build(H, t, [], o, star, xmode='h')
        if not Hpp: continue
        tested += 1
        h0 = hcost([star[j] for j in outs0], t) if outs0 else 0
        if h0 < len(outs0): nontriv += 1
        r = check(H, Hpp, t, k, cost)
        if not all(r):
            fails += 1; print('FAIL', r, [sorted(e) for e in H], t, o)
    print(f'seed {seed}: tested {tested}, with h(E0)<|Out(E0)|: {nontriv}, failures {fails}')
if __name__ == '__main__':
    main()
