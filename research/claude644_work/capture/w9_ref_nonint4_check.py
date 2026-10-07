#!/usr/bin/env python3
"""Referee w9, claim nonint#4 (Staircase lemma for bi-cliques). Independent exact checks.

Setup: U1, U2 disjoint, |Ui| = k + d_i, K_i = C(U_i, k); W = w extra outside points.
(7,2) convention of the note: every subfamily of AT MOST seven edges is 2-pierceable.

(A) K1 u K2 is (7,2)  <=>  5 d1 < k and 5 d2 < k        (SAT, all rows explicit)
(B) For a single extra edge G (only its type (g1,g2,gw) matters by symmetry),
    exact:  K1 u K2 u {G} has a bad <=7-subfamily containing G   (SAT)
    vs staircase predicate  S(G): exists a,b>=1, a+b=6, g1 <= a d1 and g2 <= b d2.
    Claim (necessity): exact-good => not S(G).  Referee sharpening: when 5d_i<k they are EQUIVALENT.
(C) maximal fatness d1=d2=d, 5d=k-1: every G not in K1 u K2 (|G|<=k, G nonempty) violates staircase;
    bad 7-tuple from the proof's choice a=max(1,ceil(g1/d)) built explicitly and brute-force checked.
(D) tau(K1 u K2) = d1+d2+2 (brute force on small cases).
"""
import itertools, math, sys
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def setup(k, d1, d2, w):
    U1 = list(range(0, k + d1))
    U2 = list(range(k + d1, 2 * k + d1 + d2))
    W = list(range(2 * k + d1 + d2, 2 * k + d1 + d2 + w))
    rows = [frozenset(c) for c in itertools.combinations(U1, k)] + \
           [frozenset(c) for c in itertools.combinations(U2, k)]
    return U1, U2, W, rows


def bad_exists(ground, rows, forced=None, maxrows=7):
    """SAT: exist <= maxrows edges (forced edge included) with no 2-point transversal.
    Returns a witness list or None."""
    pool = IDPool()
    x = [pool.id(('x', i)) for i in range(len(rows))]
    clauses = []
    m = maxrows - (1 if forced is not None else 0)
    pts = list(ground)
    for i in range(len(pts)):
        for j in range(i, len(pts)):
            p, q = pts[i], pts[j]
            if forced is not None and p not in forced and q not in forced:
                continue  # forced edge already avoids pair -> pair fails
            cl = [x[r] for r, R in enumerate(rows) if p not in R and q not in R]
            if not cl:
                return None  # this pair pierces every possible choice -> no bad subfamily
            clauses.append(cl)
    if forced is None:
        clauses.append(list(x))  # nonempty
    card = CardEnc.atmost(lits=x, bound=m, vpool=pool, encoding=EncType.seqcounter)
    with Solver(name='cadical153', bootstrap_with=clauses + card.clauses) as s:
        if s.solve():
            mod = set(l for l in s.get_model() if l > 0)
            return [rows[r] for r in range(len(rows)) if x[r] in mod]
    return None


def two_pierceable(edges, ground):
    for p in ground:
        for q in ground:
            if all(p in E or q in E for E in edges):
                return True
    return False


def staircase_violated(g1, g2, d1, d2):
    return any(g1 <= a * d1 and g2 <= (6 - a) * d2 for a in range(1, 6))


def make_G(U1, U2, W, g1, g2, gw):
    return frozenset(U1[:g1] + U2[:g2] + W[:gw])


def check_A(cases):
    out = []
    for (k, d1, d2) in cases:
        U1, U2, W, rows = setup(k, d1, d2, 0)
        wit = bad_exists(U1 + U2, rows)
        is72 = wit is None
        pred = (5 * d1 < k and 5 * d2 < k)
        if wit is not None:
            assert len(wit) <= 7 and not two_pierceable(wit, U1 + U2)
        out.append((k, d1, d2, is72, pred, is72 == pred))
    return out


def check_B(k, d1, d2, w):
    U1, U2, W, rows = setup(k, d1, d2, w)
    ground = U1 + U2 + W
    rowset = set(rows)
    fails, n, agree = [], 0, 0
    for g1 in range(0, min(k, k + d1) + 1):
        for g2 in range(0, k - g1 + 1):
            for gw in range(0, min(w, k - g1 - g2) + 1):
                if g1 + g2 + gw == 0:
                    continue
                G = make_G(U1, U2, W, g1, g2, gw)
                if G in rowset:
                    continue
                n += 1
                wit = bad_exists(ground, rows, forced=G)
                exact_bad = wit is not None
                if exact_bad:
                    assert not two_pierceable(wit + [G], ground)
                pred_bad = staircase_violated(g1, g2, d1, d2)
                # necessity claim: staircase violated => exact bad
                if pred_bad and not exact_bad:
                    fails.append(('NECESSITY', g1, g2, gw))
                if pred_bad == exact_bad:
                    agree += 1
                else:
                    fails.append(('NOT_EQUIV', g1, g2, gw, exact_bad, pred_bad))
    return n, agree, fails


def check_C(k):
    assert (k - 1) % 5 == 0
    d = (k - 1) // 5
    w = 3
    U1, U2, W, rows = setup(k, d, d, w)
    ground = U1 + U2 + W
    rowset = set(rows)
    n = 0
    bad = []
    for g1 in range(0, k + 1):
        for g2 in range(0, k - g1 + 1):
            for gw in range(0, min(w, k - g1 - g2) + 1):
                if g1 + g2 + gw == 0:
                    continue
                G = make_G(U1, U2, W, g1, g2, gw)
                if G in rowset:
                    continue
                n += 1
                if d == 0:
                    a = 1
                else:
                    a = max(1, -(-g1 // d))
                b = 6 - a
                if not (1 <= a <= 5 and g1 <= a * d and g2 <= b * d):
                    bad.append(('proof_choice_invalid', g1, g2, gw, a))
                    continue
                # explicit rows: holes covering G n U1 / G n U2 (distinct when d>=1)
                GU1 = [p for p in U1 if p in G]
                GU2 = [p for p in U2 if p in G]
                def holes(GU, U, cnt, dd):
                    rest = [p for p in U if p not in GU]
                    seq = GU + rest
                    H = []
                    for i in range(cnt):
                        h = seq[i * dd:(i + 1) * dd] if dd > 0 else []
                        if len(h) < dd:  # pad from the rest (keeps coverage), make distinct
                            h = (h + [p for p in rest if p not in h])[:dd]
                        H.append(frozenset(h))
                    # ensure distinct holes (when d>=1 and enough subsets)
                    if dd > 0:
                        seen = set(); out = []
                        extra = itertools.combinations(U, dd)
                        for h in H:
                            while h in seen:
                                h = frozenset(next(extra))
                            seen.add(h); out.append(h)
                        H = out
                    return H
                h1 = holes(GU1, U1, a, d)
                h2 = holes(GU2, U2, b, d)
                assert set(GU1) <= set().union(*h1) if GU1 else True
                assert set(GU2) <= set().union(*h2) if GU2 else True
                tup = [frozenset(U1) - h for h in h1] + [frozenset(U2) - h for h in h2] + [G]
                if two_pierceable(tup, ground):
                    bad.append(('tuple_pierceable', g1, g2, gw))
    return d, n, bad


def tau_brute(rows, ground, cap):
    for t in range(0, cap + 1):
        for T in itertools.combinations(ground, t):
            Ts = set(T)
            if all(R & Ts for R in rows):
                return t
    return None


if __name__ == '__main__':
    print('(A) K1 u K2 is (7,2) iff 5d1<k and 5d2<k')
    casesA = [(k, d1, d2) for k in range(1, 12) for d1 in range(0, 4) for d2 in range(0, d1 + 1)
              if math.comb(k + d1, k) + math.comb(k + d2, k) <= 400]
    resA = check_A(casesA)
    badA = [r for r in resA if not r[5]]
    print('  cases', len(resA), 'mismatches', badA)
    sys.stdout.flush()

    print('(B) single extra edge: staircase predicate vs exact SAT')
    casesB = [(k, d1, d2, w) for (k, d1, d2) in [(1, 0, 0), (2, 0, 0), (5, 0, 0), (6, 1, 0), (6, 1, 1), (7, 1, 1),
                                                   (8, 1, 0), (9, 1, 1), (10, 1, 1), (11, 2, 1), (11, 2, 2),
                                                   (12, 2, 1), (12, 2, 2)] for w in (2,)]
    for (k, d1, d2, w) in casesB:
        n, agree, fails = check_B(k, d1, d2, w)
        print(f'  k={k} d=({d1},{d2}) w={w}: types {n}, agree {agree}, fails {fails[:6]}')
        sys.stdout.flush()

    print('(C) maximal fatness 5d=k-1: proof tuple explicit + brute-force check')
    for k in (1, 6, 11, 16, 21):
        d, n, bad = check_C(k)
        print(f'  k={k} d={d}: other-edge types {n}, failures {bad[:6]}')
        sys.stdout.flush()

    print('(D) tau(K1 u K2) = d1+d2+2')
    for (k, d1, d2) in [(1, 0, 0), (3, 0, 0), (4, 1, 0), (5, 1, 1), (6, 1, 1), (4, 2, 1), (5, 2, 2)]:
        U1, U2, W, rows = setup(k, d1, d2, 0)
        t = tau_brute(rows, U1 + U2, d1 + d2 + 3)
        print(f'  k={k} d=({d1},{d2}): tau={t}, claim {d1 + d2 + 2}, ok={t == d1 + d2 + 2}')
