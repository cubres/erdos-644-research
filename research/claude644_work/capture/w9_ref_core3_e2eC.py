"""w9 referee [core#3] part C: random SUBFAMILIES of verified (7,2) families with larger tau (subfamilies of (7,2)
families are (7,2)), plus mixed families {x} u K_n^k.  Same checks as part B (L+, L++, necessity, eps side condition).
Bases: K_6^4 (t=3), K_8^5 (t=4), K_9^5 (t=5), parity k=4 on 8 points (t=4), K_12^7? (checked by SAT first)."""
import random, sys, itertools, json
from w9_ref_core3_lib import *
from w9_ref_core3_e2eB import check
import os
LIGHT = os.environ.get("LIGHT") == "1"
def K(n, k, off=0): return [sum(1 << (v+off) for v in S) for S in itertools.combinations(range(n), k)]
def bases():
    out = [("K6^4", 6, K(6,4)), ("K8^5", 8, K(8,5)), ("K9^5", 9, K(9,5)), ("K7^4", 7, K(7,4)), ("K11^6", 11, K(11,6)),
           ("K10^6", 10, K(10,6))]
    if LIGHT: out = [o for o in out if o[0] not in ("K9^5", "K11^6", "K10^6", "x+K8^7")]
    A = 0b1111
    out.append(("parity4", 8, [E for E in K(8,4) if popc(E & A) % 2 == 1]))
    # singleton + 7-wise intersecting complete family: {x} u K_n^k on other points, n < 7k/6
    out.append(("x+K6^5", 7, [1] + K(6,5,1)))
    out.append(("x+K8^7", 9, [1] + K(8,7,1)))
    good = []
    for name, n, H in out:
        ok = is72(H, n); print(name, "n", n, "|H|", len(H), "(7,2):", ok, "tau:", tau(H, n) if ok else "-", flush=True)
        if ok: good.append((name, n, H))
    return good
def main(trials, seed):
    rnd = random.Random(seed); stats = {'fams': 0, 't': {}, 'nec': {}, 'eps': []}
    bs = bases()
    for name, n, H in bs: check(name, H, n, stats)
    for it in range(trials):
        name, n, H = rnd.choice(bs)
        p = rnd.choice([0.3, 0.5, 0.7, 0.85, 0.95])
        S = [E for E in H if rnd.random() < p]
        if not S: continue
        check(f"{name} sub p={p} i{it}", S, n, stats)
    print("part C PASS seed", seed, "families", stats['fams'], "tau distribution", stats['t'])
    print("necessity witnesses (inequality violated, other four hold):")
    for k, v in stats['nec'].items(): print("  ", k, v[:6])
    print("eps side-condition counterexamples (name,n,t,d,beta,|H|):", len(stats['eps']), stats['eps'][:10])
    json.dump({'nec': stats['nec'], 'eps': stats['eps']}, open(f"w9_ref_core3_e2eC_s{seed}.json", "w"))
if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
