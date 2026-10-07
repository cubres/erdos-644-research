"""Lemma 4.8 (two large opposite cells): literal execution of the appendix proof.
For all k <= KMAX, 0 <= T <= k, m with 4m <= k, x,b > k/2, |Y|,|Z|,|A|,|C| <= m with all
private parts nonnegative and the three hypotheses: build E,F,G,H with all triple
intersections empty, the request U cup B_0 cup X_0, enumerate every response I (by
counts, WLOG; up to k outside points) respecting the dichotomy with threshold m w.r.t.
E,F,G,H, build the two final requests, and check literally that every pair of points
meeting E,F,G,H,I lies in one of them (each of size <= T)."""
import sys
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
ONLY_MAIN_T = len(sys.argv) > 2 and sys.argv[2] == "main"


def dich_ok(size, m, k):
    return size <= m or 2 * size > k


def run(k, T, m, x, b, yy, zz, aa, cc):
    ck = -(-k // 2)  # ceil(k/2)
    if not (T >= ck + 2 * m and T >= x + m and 3 * T >= 2 * x + b + ck + 2 * m):
        return None
    pE = k - x - yy - cc; pF = k - x - zz - aa; pG = k - yy - zz - b; pH = k - aa - cc - b
    if min(pE, pF, pG, pH) < 0: return None
    U = Universe()
    X = U.cell("X", x); B = U.cell("B", b); Y = U.cell("Y", yy); Z = U.cell("Z", zz); A = U.cell("A", aa); C = U.cell("C", cc)
    PE = U.cell("PE", pE); PF = U.cell("PF", pF); PG = U.cell("PG", pG); PH = U.cell("PH", pH); O = U.cell("O", k)
    E = X | Y | C | PE; F = X | Z | A | PF; G = Y | Z | B | PG; H = A | C | B | PH
    for e in (E, F, G, H): assert popcount(e) == k
    sigma = yy + zz; rho = aa + cc
    p = ck - min(sigma, rho); q = T - ck - max(sigma, rho)
    if p < 0 or q < 0 or p > b or q > x: return "4.8 p,q claims fail %s" % ((k, T, m, x, b, yy, zz, aa, cc),)
    B0 = first(B, p); X0 = first(X, q)
    R1 = Y | Z | A | C | B0 | X0
    if popcount(R1) != T: return "4.8 first request size %d != T %s" % (popcount(R1), (k, T, m, x, b, yy, zz, aa, cc))
    B1c = B ^ B0; X1c = X ^ X0
    n = 0
    for (ix, ib, ie, if_, ig, ih) in compositions([popcount(X1c), popcount(B1c), pE, pF, pG, pH]):
        o = k - ix - ib - ie - if_ - ig - ih
        if o < 0 or o > k: continue
        I = first(X1c, ix) | first(B1c, ib) | first(PE, ie) | first(PF, if_) | first(PG, ig) | first(PH, ih) | first(O, o)
        if not all(dich_ok(popcount(e & I), m, k) for e in (E, F, G, H)):
            continue
        if popcount(G & I) > m or popcount(H & I) > m:
            return "4.8 trace claim fails %s" % ((k, T, m, x, b, yy, zz, aa, cc, ix, ib, ie, if_, ig, ih),)
        BI = B & I
        n1 = min(b, T - x)
        if popcount(BI) > n1: return "4.8 B1 choice impossible %s" % ((k, T, m, x, b, yy, zz, aa, cc, ix, ib),)
        Bfull = BI | first(B & ~BI, n1 - popcount(BI))
        reqs = [X | Bfull, (X & I) | (B & ~Bfull)]
        for i, r in enumerate(reqs):
            if popcount(r) > T: return "4.8 request %d too large (%d>%d) %s" % (i, popcount(r), T, (k, T, m, x, b, yy, zz, aa, cc, ix, ib, ie, if_, ig, ih))
        ok, msg = check_cover([E, F, G, H, I], reqs, T, U.all())
        if not ok: return "4.8 COVER FAIL %s %s" % (msg, (k, T, m, x, b, yy, zz, aa, cc, ix, ib, ie, if_, ig, ih))
        n += 1
    return n


def main():
    nparam = 0; nK = 0
    for k in range(1, KMAX + 1):
        Ts = [-(-6 * k // 7)] if ONLY_MAIN_T else range(0, k + 1)
        for T in Ts:
            for m in range(0, k // 4 + 1):
                for x in range(k // 2 + 1, k + 1):
                    for b in range(k // 2 + 1, k + 1):
                        for yy in range(0, m + 1):
                            for zz in range(0, m + 1):
                                for aa in range(0, m + 1):
                                    for cc in range(0, m + 1):
                                        r = run(k, T, m, x, b, yy, zz, aa, cc)
                                        if isinstance(r, str): print("FAIL", r); sys.exit(1)
                                        if r is not None: nparam += 1; nK += r
        print("k=%d done: params %d responses %d" % (k, nparam, nK), flush=True)
    print("ALL OK: Lemma 4.8 verified literally for k<=%d (%s): %d parameter sets, %d responses" % (KMAX, "T=ceil(6k/7)" if ONLY_MAIN_T else "all T", nparam, nK))


main()
