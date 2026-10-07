"""Static closures, checked on explicit set systems.
(a) Lemma 3.1: for all k <= KMAX, 0 <= T <= k, (a,b,c) satisfying the eleven inequalities,
    build the cells, place X,Y,Z with labels {1,2,3},{2,4},{3,4}, distribute P_E, P_F, P_G
    by max-flow with allowed sets {3,4},{2,4},{1,2,3}, and check coverage literally (for
    every allowed assignment).  Also: the eleven inequalities are exactly equivalent to
    Hall feasibility (both directions), as a sanity check of the transcription.
(b) Corollary 3.2: its hypotheses imply the eleven inequalities (integer scan).
(c) Lemma 3.3: the iff, by exhaustive search over a_i, for small M_i, L_i, t.
(d) Lemma 3.4: for all k <= KMAX, T, m >= y >= z with the four inequalities, search a_i by
    brute force and build the four requests explicitly; check coverage and sizes; also
    check that the four inequalities are equivalent to the existence of a_i (both ways).
"""
import sys, itertools
from common import *

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def hall31(k, T, a, b, c):
    return (T - a >= 0 and T - a - b >= 0 and T - a - c >= 0 and T - b - c >= 0
            and k + 2 * b <= 2 * T and k + 2 * c <= 2 * T and k + 3 * a <= 3 * T and 2 * k + b + c <= 3 * T
            and 2 * k + 2 * a + b <= 4 * T and 2 * k + 2 * a + c <= 4 * T and 3 * k + a <= 4 * T)


def check31():
    n = 0
    for k in range(1, KMAX + 1):
        for T in range(0, k + 1):
            for a in range(0, k + 1):
                for b in range(0, k + 1 - a):
                    for c in range(0, k + 1 - max(a, b)):
                        U = Universe()
                        X = U.cell("X", a); Y = U.cell("Y", b); Z = U.cell("Z", c)
                        PE = U.cell("PE", k - a - b); PF = U.cell("PF", k - a - c); PG = U.cell("PG", k - b - c)
                        E, F, G = X | Y | PE, X | Z | PF, Y | Z | PG
                        bases = [X, X | Y, X | Z, Y | Z]
                        groups = [(PE, [2, 3]), (PF, [1, 3]), (PG, [0, 1, 2])]
                        caps = [T - popcount(bb) for bb in bases]
                        feasible = all(cc >= 0 for cc in caps) and maxflow_alloc(groups, caps) is not None
                        if feasible != hall31(k, T, a, b, c):
                            print("FAIL 3.1 transcription", (k, T, a, b, c), feasible); sys.exit(1)
                        if feasible:
                            ok, msg = check_cover_any([E, F, G], bases, groups, T, U.all())
                            if not ok:
                                print("FAIL 3.1 cover", (k, T, a, b, c), msg); sys.exit(1)
                            n += 1
    print("Lemma 3.1 OK: %d parameter sets (k<=%d, all T), eleven inequalities <=> Hall feasibility, coverage for all assignments" % (n, KMAX))


def check32():
    n = 0
    for k in range(1, KMAX + 1):
        for T in range(0, k + 1):
            if 7 * T < 6 * k: continue
            for a in range(0, k + 1):
                for b in range(0, k + 1 - a):
                    for c in range(0, k + 1 - max(a, b)):
                        if 2 * a <= T and 2 * b <= 2 * T - k and 2 * c <= 2 * T - k and b + c <= 3 * T - 2 * k:
                            if not hall31(k, T, a, b, c):
                                print("FAIL 3.2", (k, T, a, b, c)); sys.exit(1)
                            n += 1
    print("Corollary 3.2 OK: %d parameter sets" % n)


def check33():
    n = 0
    R = range(0, 5)
    for M in itertools.product(R, R, R):
        for L in itertools.product(range(-2, 7), repeat=3):
            if not all(L[i] <= M[j] + M[l] for (i, j, l) in ((0, 1, 2), (1, 0, 2), (2, 0, 1))): continue
            for t in range(0, 14):
                exists = any(a[1] + a[2] >= L[0] and a[0] + a[2] >= L[1] and a[0] + a[1] >= L[2] and sum(a) <= t
                             for a in itertools.product(range(M[0] + 1), range(M[1] + 1), range(M[2] + 1)))
                bound = max(L[0], L[1], L[2], L[0] + L[1] - M[2], L[0] + L[2] - M[1], L[1] + L[2] - M[0], (L[0] + L[1] + L[2]) / 2)
                if exists != (t >= bound):
                    print("FAIL 3.3", M, L, t, exists, bound); sys.exit(1)
                n += 1
    print("Lemma 3.3 OK: %d (M,L,t) instances, iff holds" % n)


def check34():
    n = 0
    for k in range(1, KMAX + 1):
        for T in range(0, k + 1):
            for m in range(0, k + 1):
                for y in range(0, m + 1):
                    for z in range(0, y + 1):
                        if m + y > k or m + z > k or y + z > k: continue
                        S = m + y + z
                        hyp = (T >= k + m - y - z and 2 * T >= k + m and 3 * T >= 2 * k + m + y - z and 5 * T >= 3 * k + S)
                        found = None
                        for a1 in range(m + 1):
                            for a2 in range(y + 1):
                                for a3 in range(z + 1):
                                    if a2 + a3 >= k + m - T and a1 + a3 >= k + y - T and a1 + a2 >= k + z - T and a1 + a2 + a3 <= T:
                                        found = (a1, a2, a3); break
                                if found: break
                            if found: break
                        if (found is not None) != hyp:
                            print("FAIL 3.4 transcription", (k, T, m, y, z), found, hyp); sys.exit(1)
                        if not hyp: continue
                        a1, a2, a3 = found
                        U = Universe()
                        Mc = U.cell("M", m); Yc = U.cell("Y", y); Zc = U.cell("Z", z)
                        PM = U.cell("PM", k - y - z); PY = U.cell("PY", k - m - z); PZ = U.cell("PZ", k - m - y)
                        # M = E cap F, Y = E cap G, Z = F cap G; P_M = P_G etc.
                        E, F, G = Mc | Yc | PZ, Mc | Zc | PY, Yc | Zc | PM
                        M1 = first(Mc, a1); M2 = Mc ^ M1; Y1 = first(Yc, a2); Y2 = Yc ^ Y1; Z1 = first(Zc, a3); Z2 = Zc ^ Z1
                        reqs = [M1 | Y1 | Z1, Mc | PM | Y2 | Z2, Yc | PY | M2 | Z2, Zc | PZ | M2 | Y2]
                        ok, msg = check_cover([E, F, G], reqs, T, U.all())
                        if not ok:
                            print("FAIL 3.4 cover", (k, T, m, y, z), msg); sys.exit(1)
                        n += 1
    print("Lemma 3.4 OK: %d parameter sets (k<=%d, all T), four inequalities <=> existence of a_i, explicit requests cover" % (n, KMAX))


check31(); check32(); check33(); check34()
