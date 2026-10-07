"""Lemma 4.1 (one surviving cell): literal execution of the appendix proof on explicit
set systems. For every k <= KMAX, every 0 <= T <= k and every (x,y,z) with nonnegative
cells satisfying the nine hypotheses, build E,F,G, the first request, enumerate every
response K (by its intersection counts with the sub-cells, which is WLOG by symmetry;
K may also use up to k points outside E cup F cup G), run the construction of the
proof literally (Case 0/1/2/3), distribute D by max-flow, and check that every pair of
points meeting E,F,G,K lies in some request of size <= T."""
import sys
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
ONLY_MAIN_T = len(sys.argv) > 2 and sys.argv[2] == "main"
THETA_LOW = not (len(sys.argv) > 3 and sys.argv[3] == "hi")


def hyps(k, T, x, y, z):
    S = x + y + z
    return (T >= x + y and 2 * T >= k + 2 * x and 2 * T >= k + 2 * y
            and T >= k + x - y - z and T >= k - x + y - z
            and 3 * T >= 3 * k - S and 5 * T >= 3 * k + S
            and 3 * T >= k + x + y + 2 * z and 4 * T >= 2 * k + 3 * z)


def run(k, T, x, y, z):
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z)
    O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    Z0 = first(Z, min(z, T - x - y)); Z1 = Z ^ Z0
    R1 = X | Y | Z0
    assert popcount(R1) <= T
    cases = [0, 0, 0, 0]
    for (q, a, b, c) in compositions([popcount(Z1), popcount(PF), popcount(PG), popcount(PE)]):
        o = k - q - a - b - c
        if o < 0 or o > k:
            continue
        K = first(Z1, q) | first(PF, a) | first(PG, b) | first(PE, c) | first(O, o)
        assert popcount(K) == k and K & R1 == 0
        Q = Z & K; A = (F & K) & ~Q; B = (G & K) & ~Q; C = E & K
        V = Z & ~Q; D = E & ~(X | Y | C)
        S = x + y + z
        assert q <= max(0, S - T)
        if c <= T - z:
            cases[0] += 1
            bases = [Q | X | B, Q | Y | A, Z | C]
        else:
            a0 = k + x + z - 2 * T; b0 = k + y + z - 2 * T
            if a < a0:
                cases[1] += 1
                # proof: split C = C2 + C3 with |C2| <= T-y-a-z, |C3| <= T-z
                if not (y + a + z < T):
                    return "Case1 claim y+a+z<T fails k=%d T=%d xyz=%d,%d,%d K=%s" % (k, T, x, y, z, (q, a, b, c))
                n3 = min(c, T - z); C3 = first(C, n3); C2 = C ^ C3
                if popcount(C2) > T - y - a - z:
                    return "Case1 split fails k=%d T=%d xyz=%d,%d,%d K=%s" % (k, T, x, y, z, (q, a, b, c))
                bases = [Q | X | B, Y | A | Z | C2, Z | C3]
            elif b < b0:
                cases[2] += 1
                if not (x + b + z < T):
                    return "Case2 claim x+b+z<T fails k=%d T=%d xyz=%d,%d,%d K=%s" % (k, T, x, y, z, (q, a, b, c))
                n3 = min(c, T - z); C3 = first(C, n3); C2 = C ^ C3
                if popcount(C2) > T - x - b - z:
                    return "Case2 split fails k=%d T=%d xyz=%d,%d,%d K=%s" % (k, T, x, y, z, (q, a, b, c))
                bases = [Q | Y | A, X | B | Z | C2, Z | C3]
            else:
                cases[3] += 1
                u = c + z - T
                if not (0 < u <= c):
                    return "Case3 u out of range"
                C12 = first(C, u); C3 = C ^ C12
                v = popcount(V)
                lo = max(0, y + a + z + u - T); hi = min(v, T - q - x - b - u)
                if lo > hi:
                    return "Case3 theta does not exist k=%d T=%d xyz=%d,%d,%d K=%s lo=%d hi=%d" % (k, T, x, y, z, (q, a, b, c), lo, hi)
                theta = lo if THETA_LOW else hi
                V13 = first(V, theta); V23 = V ^ V13
                bases = [Q | X | B | C12 | V13, Q | Y | A | C12 | V23, Z | C3]
        for i, bb in enumerate(bases):
            if popcount(bb) > T:
                return "base %d too large (%d>%d) k=%d T=%d xyz=%d,%d,%d K=%s" % (i, popcount(bb), T, k, T, x, y, z, (q, a, b, c))
        reqs = distribute(bases, [(D, [0, 1, 2])], T)
        if reqs is None:
            return "distribution of D infeasible k=%d T=%d xyz=%d,%d,%d K=%s" % (k, T, x, y, z, (q, a, b, c))
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok:
            return "COVER FAIL %s k=%d T=%d xyz=%d,%d,%d K=%s" % (msg, k, T, x, y, z, (q, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, [(D, [0, 1, 2])], T, U.all())
        if not ok:
            return "COVER-ANY FAIL %s k=%d T=%d xyz=%d,%d,%d K=%s" % (msg, k, T, x, y, z, (q, a, b, c))
    return cases


def main():
    nparam = 0; nK = 0; casetot = [0, 0, 0, 0]
    for k in range(1, KMAX + 1):
        Ts = [-(-6 * k // 7)] if ONLY_MAIN_T else range(0, k + 1)
        for T in Ts:
            for x in range(0, k + 1):
                for y in range(0, k + 1 - x):
                    for z in range(0, k + 1 - max(x, y)):
                        if not hyps(k, T, x, y, z):
                            continue
                        res = run(k, T, x, y, z)
                        if isinstance(res, str):
                            print("FAIL:", res); sys.exit(1)
                        nparam += 1; nK += sum(res)
                        for i in range(4): casetot[i] += res[i]
        print("k=%d done; params so far %d, responses so far %d, cases %s" % (k, nparam, nK, casetot), flush=True)
    print("ALL OK: Lemma 4.1 verified literally for k<=%d (%s), %d parameter sets, %d responses" % (KMAX, "T=ceil(6k/7) only" if ONLY_MAIN_T else "all 0<=T<=k", nparam, nK))


main()
