"""Lemma 4.6 (two cores): literal execution of the appendix proof. For all k <= KMAX,
0 <= T <= k, (x,y,z), 0 <= l <= u < k with the seven hypotheses: build the first request
(Y, g points of X, g of Z, then remaining points of X cup Z in the order X-then-Z or
Z-then-X (both tested), then P_F, until exactly T-y points of F), enumerate all responses
K respecting Gap(l,u) w.r.t. E,F,G (WLOG by counts; up to k outside points), build the
three bases, distribute D and W by max-flow, and check coverage literally."""
import sys
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
ONLY_MAIN_T = len(sys.argv) > 2 and sys.argv[2] == "main"


def gap_ok(size, l, u, k):
    return size == k or not (l < size <= u)


def run(k, T, x, y, z, l, u, order):
    S = x + y + z
    g = max(0, k - y - u)
    if not (g <= min(x, z) and y + 2 * g <= T and x + l <= T and z + l <= T
            and k + 2 * y <= 2 * T and 3 * k <= 4 * T and 3 * k + S <= 5 * T):
        return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    need = T - y  # points of F to request
    Xr = first(X, g); Zr = first(Z, g); need -= 2 * g
    if need < 0: return "4.6 2g > T-y"
    if order == 0:
        m = min(need, x - g); Xr |= first(X ^ Xr, m); need -= m
        m = min(need, z - g); Zr |= first(Z ^ Zr, m); need -= m
    else:
        m = min(need, z - g); Zr |= first(Z ^ Zr, m); need -= m
        m = min(need, x - g); Xr |= first(X ^ Xr, m); need -= m
    if need > k - x - z: return "4.6 first request does not fit"
    PFr = first(PF, need)
    R1 = Y | Xr | Zr | PFr
    if popcount(R1) != T: return "4.6 first request size %d != T" % popcount(R1)
    X1, Z1, PF1 = X ^ Xr, Z ^ Zr, PF ^ PFr
    n = 0
    for (p, r, a, b, c) in compositions([popcount(X1), popcount(Z1), popcount(PF1), popcount(PG), popcount(PE)]):
        o = k - p - r - a - b - c
        if o < 0 or o > k: continue
        K = first(X1, p) | first(Z1, r) | first(PF1, a) | first(PG, b) | first(PE, c) | first(O, o)
        if not (gap_ok(popcount(E & K), l, u, k) and gap_ok(popcount(F & K), l, u, k) and gap_ok(popcount(G & K), l, u, k)):
            continue
        P = X & K; R = Z & K
        if p + r > max(0, S - T): return "4.6 priority claim fails %s" % ((k, T, x, y, z, l, u, p, r, a, b, c),)
        if not (popcount(E & K) <= l and popcount(G & K) <= l):
            return "4.6 traces not forced %s" % ((k, T, x, y, z, l, u, p, r, a, b, c),)
        bases = [X | (G & K), Z | (E & K), Y | (F & K)]
        for i, bb in enumerate(bases):
            if popcount(bb) > T: return "4.6 base %d too large %s" % (i, (k, T, x, y, z, l, u, p, r, a, b, c),)
        D = PE & ~K; W = PG & ~K
        reqs = distribute(bases, [(D, [0, 1, 2]), (W, [0, 1, 2])], T)
        if reqs is None: return "4.6 distribution infeasible %s" % ((k, T, x, y, z, l, u, p, r, a, b, c),)
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok: return "4.6 COVER FAIL %s %s" % (msg, (k, T, x, y, z, l, u, p, r, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, [(D, [0, 1, 2]), (W, [0, 1, 2])], T, U.all())
        if not ok: return "4.6 COVER-ANY FAIL %s %s" % (msg, (k, T, x, y, z, l, u, p, r, a, b, c))
        n += 1
    return n


def main():
    nparam = 0; nK = 0
    for k in range(1, KMAX + 1):
        Ts = [-(-6 * k // 7)] if ONLY_MAIN_T else range(0, k + 1)
        for T in Ts:
            for x in range(0, k + 1):
                for y in range(0, k + 1 - x):
                    for z in range(0, k + 1 - max(x, y)):
                        for u in range(0, k):
                            for l in range(0, u + 1):
                                for order in (0, 1):
                                    r = run(k, T, x, y, z, l, u, order)
                                    if isinstance(r, str): print("FAIL", r); sys.exit(1)
                                    if r is not None: nparam += 1; nK += r
        print("k=%d done: params %d responses %d" % (k, nparam, nK), flush=True)
    print("ALL OK: Lemma 4.6 verified literally for k<=%d (%s): %d parameter sets (x2 orders), %d responses" % (KMAX, "T=ceil(6k/7)" if ONLY_MAIN_T else "all T", nparam, nK))


main()
