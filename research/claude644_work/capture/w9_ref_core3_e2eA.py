"""w9 referee [core#3] part A: ARBITRARY random families (no (7,2) assumed).  Whenever the hypotheses of L+ (resp. the
five inequalities of L++) hold, an independent SAT search must find a bad <=7-subfamily (i.e. H is not (7,2)).
This tests the STATEMENT (contrapositive), independent of the attacker's recipe."""
import random, sys
from w9_ref_core3_lib import *
def main(trials, seed):
    rnd = random.Random(seed); hitP = hitPP = 0; fams = 0; byl = {}
    for _ in range(trials):
        n = rnd.randint(5, 9); lo = rnd.randint(1, 4); hi = rnd.randint(lo, min(n-1, lo+2))
        m = rnd.randint(4, 22)
        H = list(set(sum(1 << v for v in rnd.sample(range(n), rnd.randint(lo, hi))) for _ in range(m)))
        t = tau(H, n); fams += 1
        notseven = None
        for lam in range(0, 4):
            tn = lpp_data(H, n, lam)
            dmax = max(tn.values())
            # L+
            if 3*lam <= t-1 and 3*dmax <= t-1 and 2*lam + dmax <= t-1:
                if notseven is None: notseven = bad_tuple(H, n) is not None
                assert notseven, ("L+ FAIL", n, H, lam)
                hitP += 1
            for delta in range(0, 5):
                B = [E for E in H if tn[E] > delta]
                beta = tau(B, n)
                if all(five(t, lam, delta, beta)):
                    if notseven is None: notseven = bad_tuple(H, n) is not None
                    assert notseven, ("L++ FAIL", n, H, lam, delta)
                    hitPP += 1; byl[lam] = byl.get(lam,0)+1
    print(f"part A PASS seed={seed}: {fams} families, L+ hyp hits {hitP}, L++ hyp hits {hitPP}; all non-(7,2); L++ hits by lam {byl}")
if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
