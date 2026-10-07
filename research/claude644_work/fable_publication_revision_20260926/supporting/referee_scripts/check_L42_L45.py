"""Lemmas 4.2, 4.3 (asymmetric splits, no gap) and 4.4, 4.5 (gap lemmas): literal
execution of the appendix proofs on explicit set systems. Enumerates all k <= KMAX,
0 <= T <= k, all (x,y,z), for 4.4/4.5 all 0 <= l <= u < k; responses K are enumerated by
intersection counts with sub-cells (WLOG), including up to k outside points; for the gap
lemmas only responses satisfying Gap(l,u) w.r.t. E,F,G are adversarially allowed."""
import sys
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
WHICH = sys.argv[2] if len(sys.argv) > 2 else "all"


def gap_ok(size, l, u, k):
    # Gap(l,u): no two distinct edges meet in l+1..u points. size==k means same edge.
    return size == k or not (l < size <= u)


def ceil2(n):
    return -(-n // 2)


def run42(k, T, x, y, z):
    S = x + y + z
    if not (T >= S and 2 * T >= k + 2 * y and 2 * T >= k + 2 * x - y + z and 3 * T >= k + 2 * x + y + 3 * z):
        return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    PF0 = first(PF, T - S); PF1 = PF ^ PF0
    R1 = X | Y | Z | PF0
    assert popcount(R1) == T
    n = 0
    for (a, b, c) in compositions([popcount(PF1), popcount(PG), popcount(PE)]):
        o = k - a - b - c
        if o < 0 or o > k: continue
        K = first(PF1, a) | first(PG, b) | first(PE, c) | first(O, o)
        A = F & K; B = G & K; C = E & K
        if a <= T - y - z:
            if b > 2 * (T - x - z): return "4.2 split bound fails %s" % ((k, T, x, y, z, a, b, c),)
            B1 = first(B, min(b, T - x - z)); B2 = B ^ B1
            bases = [X | Z | B1, X | Z | B2, Y | Z | A]
            groups = [(C, [0, 1, 2])]
        else:
            BC = B | C
            if b + c > 2 * (T - x - z): return "4.2 case2 bound fails %s" % ((k, T, x, y, z, a, b, c),)
            P1 = first(BC, ceil2(b + c)); P2 = BC ^ P1
            bases = [X | Z | P1, X | Z | P2, Y | A]
            groups = []
        for bb in bases:
            if popcount(bb) > T: return "4.2 base too large %s" % ((k, T, x, y, z, a, b, c),)
        reqs = distribute(bases, groups, T) if groups else bases
        if reqs is None: return "4.2 distribution infeasible %s" % ((k, T, x, y, z, a, b, c),)
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok: return "4.2 COVER FAIL %s %s" % (msg, (k, T, x, y, z, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, groups, T, U.all())
        if not ok: return "4.2 COVER-ANY FAIL %s %s" % (msg, (k, T, x, y, z, a, b, c))
        n += 1
    return n


def run43(k, T, x, y, z):
    S = x + y + z
    if not (T >= S and 3 * T >= k + 3 * x and T >= k - x + z and 3 * T >= k + 2 * x + 3 * y + z):
        return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    p = max(0, k - 2 * (T - x) - y - z)
    if p > k - y - z: return "4.3 p does not fit %s" % ((k, T, x, y, z),)
    PG0 = first(PG, p); PG1 = PG ^ PG0
    R1 = X | Y | Z | PG0
    if popcount(R1) > T: return "4.3 first request too large %s" % ((k, T, x, y, z),)
    n = 0
    for (a, b, c) in compositions([popcount(PF), popcount(PG1), popcount(PE)]):
        o = k - a - b - c
        if o < 0 or o > k: continue
        K = first(PF, a) | first(PG1, b) | first(PE, c) | first(O, o)
        A = F & K; B = G & K; C = E & K
        if b > k + y + z - T:
            if b > 2 * (T - x): return "4.3 case1 split fails %s" % ((k, T, x, y, z, a, b, c),)
            B1 = first(B, min(b, T - x)); B2 = B ^ B1
            bases = [X | B1, X | B2, Y | Z | A | C]; groups = []
        else:
            if b > 2 * (T - x - y): return "4.3 case2 split fails %s" % ((k, T, x, y, z, a, b, c),)
            B1 = first(B, min(b, T - x - y)); B2 = B ^ B1
            bases = [X | Y | B1, X | Y | B2, Y | Z | C]; groups = [(A, [0, 1, 2])]
        for bb in bases:
            if popcount(bb) > T: return "4.3 base too large %s" % ((k, T, x, y, z, a, b, c),)
        reqs = distribute(bases, groups, T) if groups else bases
        if reqs is None: return "4.3 distribution infeasible %s" % ((k, T, x, y, z, a, b, c),)
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok: return "4.3 COVER FAIL %s %s" % (msg, (k, T, x, y, z, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, groups, T, U.all())
        if not ok: return "4.3 COVER-ANY FAIL %s %s" % (msg, (k, T, x, y, z, a, b, c))
        n += 1
    return n


def run44(k, T, x, y, z, l, u):
    S = x + y + z
    p = max(0, k - x - y - u); t = max(0, k - x - z - u)
    if not (S + p + t <= T and k + 3 * x + p + t <= 3 * T and y + z + 2 * l <= T):
        return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    if p > k - x - y or t > k - x - z or T - S - p - t > k - y - z or T - S - p - t < 0:
        return "4.4 first request does not fit %s" % ((k, T, x, y, z, l, u),)
    PE0 = first(PE, p); PF0 = first(PF, t); PG0 = first(PG, T - S - p - t)
    R1 = X | Y | Z | PE0 | PF0 | PG0
    assert popcount(R1) == T
    PE1, PF1, PG1 = PE ^ PE0, PF ^ PF0, PG ^ PG0
    n = 0
    for (a, b, c) in compositions([popcount(PF1), popcount(PG1), popcount(PE1)]):
        o = k - a - b - c
        if o < 0 or o > k: continue
        K = first(PF1, a) | first(PG1, b) | first(PE1, c) | first(O, o)
        # adversary must respect Gap(l,u)
        if not (gap_ok(popcount(E & K), l, u, k) and gap_ok(popcount(F & K), l, u, k) and gap_ok(popcount(G & K), l, u, k)):
            continue
        A = F & K; B = G & K; C = E & K
        if not (popcount(C) <= l and popcount(A) <= l):
            return "4.4 trace not forced small %s" % ((k, T, x, y, z, l, u, a, b, c),)
        half = ceil2(k - T + x + p + t)
        if b > 2 * half: return "4.4 B split fails %s" % ((k, T, x, y, z, l, u, a, b, c),)
        B1 = first(B, min(b, half)); B2 = B ^ B1
        bases = [X | B1, X | B2, Y | Z | A | C]
        for bb in bases:
            if popcount(bb) > T: return "4.4 base too large %s" % ((k, T, x, y, z, l, u, a, b, c),)
        ok, msg = check_cover([E, F, G, K], bases, T, U.all())
        if not ok: return "4.4 COVER FAIL %s %s" % (msg, (k, T, x, y, z, l, u, a, b, c))
        n += 1
    return n


def run45(k, T, x, y, z, l, u):
    S = x + y + z
    Q = max(0, S - T)
    if not (x + y <= T and k - x - y <= u and k - x - z + Q <= u and 2 * x + 2 * Q + k - y - z <= 2 * T
            and y + z + 2 * l <= T and 2 * k + x - y + l + Q <= 3 * T):
        return None
    U = Universe()
    X = U.cell("X", x); Y = U.cell("Y", y); Z = U.cell("Z", z)
    PE = U.cell("PE", k - x - y); PF = U.cell("PF", k - x - z); PG = U.cell("PG", k - y - z); O = U.cell("O", k)
    E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
    Z0 = first(Z, min(z, T - x - y)); Z1 = Z ^ Z0
    R1 = X | Y | Z0
    assert popcount(R1) <= T
    n = 0
    for (p, a, b, c) in compositions([popcount(Z1), popcount(PF), popcount(PG), popcount(PE)]):
        o = k - p - a - b - c
        if o < 0 or o > k: continue
        K = first(Z1, p) | first(PF, a) | first(PG, b) | first(PE, c) | first(O, o)
        if not (gap_ok(popcount(E & K), l, u, k) and gap_ok(popcount(F & K), l, u, k) and gap_ok(popcount(G & K), l, u, k)):
            continue
        P = Z & K; A = (F & K) & ~P; B = (G & K) & ~P; C = E & K
        if not (popcount(C) <= l and popcount(A | P) <= l):
            return "4.5 trace not forced small %s" % ((k, T, x, y, z, l, u, p, a, b, c),)
        B1 = first(B, ceil2(b)); B2 = B ^ B1
        bases = [X | P | B1, X | P | B2, Y | Z | A | C]
        for bb in bases:
            if popcount(bb) > T: return "4.5 base too large %s" % ((k, T, x, y, z, l, u, p, a, b, c),)
        D = E & ~(X | Y | C)
        reqs = distribute(bases, [(D, [0, 1, 2])], T)
        if reqs is None: return "4.5 distribution infeasible %s" % ((k, T, x, y, z, l, u, p, a, b, c),)
        ok, msg = check_cover([E, F, G, K], reqs, T, U.all())
        if not ok: return "4.5 COVER FAIL %s %s" % (msg, (k, T, x, y, z, l, u, p, a, b, c))
        ok, msg = check_cover_any([E, F, G, K], bases, [(D, [0, 1, 2])], T, U.all())
        if not ok: return "4.5 COVER-ANY FAIL %s %s" % (msg, (k, T, x, y, z, l, u, p, a, b, c))
        n += 1
    return n


def main():
    stats = {"4.2": [0, 0], "4.3": [0, 0], "4.4": [0, 0], "4.5": [0, 0]}
    for k in range(1, KMAX + 1):
        for T in range(0, k + 1):
            for x in range(0, k + 1):
                for y in range(0, k + 1 - x):
                    for z in range(0, k + 1 - max(x, y)):
                        if WHICH in ("all", "4.2"):
                            r = run42(k, T, x, y, z)
                            if isinstance(r, str): print("FAIL", r); sys.exit(1)
                            if r is not None: stats["4.2"][0] += 1; stats["4.2"][1] += r
                        if WHICH in ("all", "4.3"):
                            r = run43(k, T, x, y, z)
                            if isinstance(r, str): print("FAIL", r); sys.exit(1)
                            if r is not None: stats["4.3"][0] += 1; stats["4.3"][1] += r
                        if WHICH in ("all", "4.4", "4.5"):
                            for u in range(0, k):
                                for l in range(0, u + 1):
                                    if WHICH in ("all", "4.4"):
                                        r = run44(k, T, x, y, z, l, u)
                                        if isinstance(r, str): print("FAIL", r); sys.exit(1)
                                        if r is not None: stats["4.4"][0] += 1; stats["4.4"][1] += r
                                    if WHICH in ("all", "4.5"):
                                        r = run45(k, T, x, y, z, l, u)
                                        if isinstance(r, str): print("FAIL", r); sys.exit(1)
                                        if r is not None: stats["4.5"][0] += 1; stats["4.5"][1] += r
        print("k=%d done: %s" % (k, stats), flush=True)
    print("ALL OK for k<=%d, all 0<=T<=k: (parameter sets, responses) = %s" % (KMAX, stats))


main()
