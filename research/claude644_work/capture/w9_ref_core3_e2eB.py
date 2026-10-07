"""w9 referee [core#3] part B: ACTUAL (7,2) families (greedy maximal random (7,2) families + structured ones).
For every lam, delta: assert L++ conclusion (not all five inequalities) and L+ conclusion.
Also collect: (i) counterexamples to the 'in particular' line WITHOUT its side condition 3floor(eps t)<=t-1
(lam=delta=d, 3d>=t, beta < t-2d, eps=d/t); (ii) for each of the five inequalities, (7,2) families satisfying the
other four (=> that inequality cannot be dropped from L++)."""
import random, sys, itertools, json
from w9_ref_core3_lib import *
def greedy72(n, lo, hi, rnd, cap=None):
    cands = [sum(1 << v for v in S) for s in range(lo, hi+1) for S in itertools.combinations(range(n), s)]
    rnd.shuffle(cands); H = []
    for E in cands:
        if cap and len(H) >= cap: break
        if bad_tuple(H + [E], n, force=len(H)) is None: H.append(E)
    return H
def structured():
    out = []
    for n, k in [(5,3),(6,4),(9,5),(8,5)]:
        out.append((f"K_{n}^{k}", n, [sum(1<<v for v in S) for S in itertools.combinations(range(n), k)]))
    A = 0b1111  # parity family k=4: 4-sets of [8] with odd intersection with {0,1,2,3}
    out.append(("parity k=4", 8, [sum(1<<v for v in S) for S in itertools.combinations(range(8), 4) if popc(sum(1<<v for v in S) & A) % 2 == 1]))
    return out
NAMES = ["3d<=t-1", "2d+b<=t-1", "2l+b<=t-1", "2l+d<=t-1", "3l<=t-1"]
def check(name, H, n, stats):
    assert is72(H, n), name
    t = tau(H, n); stats['fams'] += 1; stats['t'][t] = stats['t'].get(t, 0) + 1
    for lam in range(0, 5):
        tn = lpp_data(H, n, lam); dmax = max(tn.values())
        if 3*lam <= t-1: assert 3*dmax >= t or 2*lam + dmax >= t, ("L+ FAIL", name, lam)
        for delta in range(0, 7):
            B = [E for E in H if tn[E] > delta]; beta = tau(B, n)
            f = five(t, lam, delta, beta)
            assert not all(f), ("L++ FAIL", name, lam, delta)
            if sum(f) == 4:
                i = f.index(False)
                if NAMES[i] not in stats['nec']: stats['nec'][NAMES[i]] = (name, n, t, lam, delta, beta, [bin(E) for E in H][:60])
            if lam == delta and 3*lam >= t and 2*lam < t and beta < t - 2*lam:
                stats['eps'].append((name, n, t, lam, beta, len(H)))
def main(trials, seed):
    rnd = random.Random(seed)
    stats = {'fams': 0, 't': {}, 'nec': {}, 'eps': []}
    if seed == 0:
        for name, n, H in structured(): check(name, H, n, stats)
    for it in range(trials):
        n = rnd.randint(6, 10); lo = rnd.randint(1, 4); hi = rnd.randint(lo, min(lo+2, n-2))
        H = greedy72(n, lo, hi, rnd, cap=rnd.choice([None, 30, 60]))
        check(f"greedy s{seed} i{it} n{n} [{lo},{hi}]", H, n, stats)
    print("part B PASS seed", seed, "families", stats['fams'], "tau distribution", stats['t'])
    print("necessity witnesses (inequality violated, other four hold):")
    for k, v in stats['nec'].items(): print("  ", k, v[:6])
    print("eps side-condition counterexamples (name,n,t,d,beta,|H|):", len(stats['eps']), stats['eps'][:10])
    json.dump({'nec': stats['nec'], 'eps': stats['eps']}, open(f"w9_ref_core3_e2eB_s{seed}.json", "w"))
if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
