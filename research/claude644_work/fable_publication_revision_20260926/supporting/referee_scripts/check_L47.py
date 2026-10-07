"""Lemma 4.7 (near core): literal execution of the appendix proof. For all k <= KMAX,
0 <= T <= k, (x,y,z), 0 <= m <= k/2 with the common hypotheses and (first alternative
and/or second alternative), build the first request, enumerate all responses K
respecting the dichotomy with threshold m w.r.t. E,F,G (by counts, WLOG; up to k outside
points), run Case 1 / Case 2 with the stated placements, distribute by max-flow with the
stated allowed sets, and check coverage literally. Under the second alternative W is
left out (as the proof says), which the coverage check then has to validate."""
import sys
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
ONLY_MAIN_T = len(sys.argv) > 2 and sys.argv[2] == "main"


def dich_ok(size, m, k):
    return size <= m or 2 * size > k


def run(k, T, x, y, z, m, alt):
    S = x + y + z
    Delta = max(0, S - T)
    common = (y + z <= T and m + z <= T and x + m <= T and k + y - z <= T
              and 2 * k + x - 2 * z <= 2 * T and 2 * k + x + m - z <= 3 * T)
    if not common: return None
    if alt == 1:
        if not (k - x + y + Delta <= T and 2 * k - 2 * x + z + Delta <= 2 * T
                and 2 * k - z + Delta <= 2 * T and 3 * k - x - y + Delta <= 3 * T):
            return None
    else:
        if not (S <= T and k - x + y <= T and 2 * k - 2 * x + z <= 2 * T):
            return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    X0 = first(X, min(x, T - y - z)); X1 = X ^ X0
    R1 = Y | Z | X0
    assert popcount(R1) <= T
    n = 0
    for (p, a, b, c) in compositions([popcount(X1), popcount(PE), popcount(PF), popcount(PG)]):
        o = k - p - a - b - c
        if o < 0 or o > k: continue
        K = first(X1, p) | first(PE, a) | first(PF, b) | first(PG, c) | first(O, o)
        if not (dich_ok(popcount(E & K), m, k) and dich_ok(popcount(F & K), m, k) and dich_ok(popcount(G & K), m, k)):
            continue
        P = X & K; Xp = X & ~P; A = K & PE; B = K & PF; C = K & G; W = PG & ~K
        if popcount(P) > Delta: return "4.7 p > Delta %s" % ((k, T, x, y, z, m, p, a, b, c),)
        if p + a <= m:
            bases = [P | Xp | Y | B, P | Z | A, P | Xp]
            groups = [(C, [0, 2])] + ([(W, [0, 1, 2])] if alt == 1 else [])
        else:
            if popcount(C) > m: return "4.7 case2 c>m %s" % ((k, T, x, y, z, m, p, a, b, c),)
            bases = [P | Y | B | Z, P | Xp | C, Z]
            groups = [(A, [0, 2])] + ([(W, [0, 1])] if alt == 1 else [])
        for i, bb in enumerate(bases):
            if popcount(bb) > T: return "4.7 base %d too large alt=%d %s" % (i, alt, (k, T, x, y, z, m, p, a, b, c),)
        reqs = distribute(bases, groups, T)
        if reqs is None: return "4.7 distribution infeasible alt=%d %s" % (alt, (k, T, x, y, z, m, p, a, b, c),)
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok: return "4.7 COVER FAIL %s alt=%d %s" % (msg, alt, (k, T, x, y, z, m, p, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, groups, T, U.all())
        if not ok: return "4.7 COVER-ANY FAIL %s alt=%d %s" % (msg, alt, (k, T, x, y, z, m, p, a, b, c))
        n += 1
    return n


def main():
    nparam = [0, 0]; nK = [0, 0]
    for k in range(1, KMAX + 1):
        Ts = [-(-6 * k // 7)] if ONLY_MAIN_T else range(0, k + 1)
        for T in Ts:
            for x in range(0, k + 1):
                for y in range(0, k + 1 - x):
                    for z in range(0, k + 1 - max(x, y)):
                        for m in range(0, k // 2 + 1):
                            for alt in (1, 2):
                                r = run(k, T, x, y, z, m, alt)
                                if isinstance(r, str): print("FAIL", r); sys.exit(1)
                                if r is not None: nparam[alt - 1] += 1; nK[alt - 1] += r
        print("k=%d done: params(alt1,alt2)=%s responses=%s" % (k, nparam, nK), flush=True)
    print("ALL OK: Lemma 4.7 verified literally for k<=%d (%s): params %s responses %s" % (KMAX, "T=ceil(6k/7)" if ONLY_MAIN_T else "all T", nparam, nK))


main()
