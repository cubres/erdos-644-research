"""Independent brute-force verification of the hand proof in K7_RESULT.md (k=7, T=6).

Pure Python, exact integers, no solver.  Points are explicit labels; edges are explicit 7-sets.
For each step of the proof we
  (1) enumerate EVERY response allowed by the rules (avoids the request; distinct from the
      existing edges; meets each existing edge in 0,1,4,5 or 6 points),
  (2) build the requests prescribed by the proof,
  (3) check |request| <= 6, that the final family has at most 7 distinct edges, and that every
      2-transversal (and 1-transversal) of the retained edges lies inside one of the requests.

Responses are enumerated as cell-count vectors: points inside one Venn cell of the existing
edges are interchangeable, so this loses nothing.  Each response is then realised as an explicit
set (taking the first points of each cell) before the checks.

Run:  python3 verify_k7.py     -> prints a line per case and 'ALL CHECKS PASSED'.
"""
import itertools

K, T = 7, 6
ALLOWED = {0, 1, 4, 5, 6}


def transversals2(edges):
    """all sets of <=2 points (from the union) meeting every edge."""
    pts = sorted(set().union(*edges))
    out = []
    for p in pts:
        if all(p in E for E in edges):
            out.append(frozenset([p]))
    for p, q in itertools.combinations(pts, 2):
        if all(p in E or q in E for E in edges):
            out.append(frozenset([p, q]))
    return out


def check_cover(edges, requests, label):
    """edges: list of explicit edges (kept family).  requests: list of explicit sets."""
    assert len(edges) + len(requests) <= 7, label + ': more than 7 edges'
    for R in requests:
        assert len(R) <= T, label + ': request too large %r' % (sorted(R),)
    for S in transversals2(edges):
        if not any(S <= R for R in requests):
            raise AssertionError(label + ': uncovered transversal %r' % (sorted(S),))
    return True


EXPLICIT = True   # True: enumerate every subset of the available points (no symmetry argument)


def responses(edges, request):
    """all explicit responses: 7-sets avoiding request, distinct from edges, traces in ALLOWED.
    EXPLICIT=True: every subset of the available points, padded with new points.
    EXPLICIT=False: one representative per Venn-cell count vector."""
    pts = sorted(set().union(*edges))
    if EXPLICIT:
        avail = [p for p in pts if p not in request]
        out = []
        for r in range(0, min(K, len(avail)) + 1):
            for chosen in itertools.combinations(avail, r):
                traces = [sum(1 for p in chosen if p in E) for E in edges]
                if all(t in ALLOWED for t in traces):
                    H = frozenset(chosen) | frozenset('n%d' % j for j in range(K - r))
                    out.append(H)
        return out
    cells = {}
    for p in pts:
        if p in request:
            continue
        m = tuple(p in E for E in edges)
        cells.setdefault(m, []).append(p)
    keys = sorted(cells)
    out = []

    def rec(i, rem, chosen):
        if i == len(keys):
            traces = [sum(1 for p in chosen if p in E) for E in edges]
            if all(t in ALLOWED for t in traces):
                new = ['n%d' % j for j in range(rem)]
                H = frozenset(chosen + new)
                assert len(H) == K
                out.append(H)
            return
        c = cells[keys[i]]
        for k in range(min(len(c), rem), -1, -1):
            rec(i + 1, rem - k, chosen + c[:k])

    rec(0, K, [])
    return out


def split(S, sizes):
    S = sorted(S)
    parts, i = [], 0
    for s in sizes:
        parts.append(frozenset(S[i:i + s])); i += s
    assert i == len(S)
    return parts


# ------------------------------------------------------------------ Step 1: M = 0
def step_M0():
    E1 = frozenset('e1 e2 e3 e4 e5 e6 e7'.split())
    E2 = frozenset('f1 f2 f3 f4 f5 f6 f7'.split())
    D = frozenset('e1 e2 e3 f1 f2 f3'.split())
    n = 0
    for G in responses([E1, E2], D):
        a, b = len(G & E1), len(G & E2)
        # with M=0 a trace of 1 is impossible; the enumeration with ALLOWED still lists it: skip
        if a == 1 or b == 1:
            continue
        n += 1
        assert (a, b) in {(0, 0), (4, 0), (0, 4)}, (a, b)
        if (a, b) == (0, 0):
            assert transversals2([E1, E2, G]) == []          # bad triple
            continue
        if b == 4:
            E1, E2 = E2, E1
            a, b = b, a
        Q = G & E1
        assert len(Q) == 4 and not (G & E2)
        reqs = [Q | S for S in split(E2, (2, 2, 2, 1))]
        check_cover([E1, E2, G], reqs, 'M0 (4,0,0)')
    print('Step 1 (M=0): %d response classes verified' % n)


# ------------------------------------------------------------------ small-triple static cover
def small_cover(E, F, G):
    """E∩F={p}, |E∩G|,|F∩G|<=1, E∩F∩G empty. returns the 4 requests of Lemma 2."""
    X = E & F; Y = E & G; Z = F & G
    assert len(X) == 1 and len(Y) <= 1 and len(Z) <= 1 and not (E & F & G)
    PE = E - F - G; PF = F - E - G; PG = G - E - F
    PG5 = frozenset(sorted(PG)[:5]); PGrest = PG - PG5
    f = frozenset(sorted(PF)[:1]); e = frozenset(sorted(PE)[:1])
    R1 = X | PG5
    R2 = X | Y | Z | PGrest | f | e
    R3 = Y | (PF - f)
    R4 = Z | (PE - e)
    return [R1, R2, R3, R4]


# ------------------------------------------------------------------ Lemma 3: the (4,1,z) triple
def lemma_41z(A, B, C):
    """A∩B=X (4), A∩C={y}, |B∩C|<=1, A∩B∩C empty. Returns (request D, function response->requests)."""
    X = A & B; Y = A & C; Z = B & C
    assert len(X) == 4 and len(Y) == 1 and len(Z) <= 1 and not (A & B & C)
    y = next(iter(Y))
    Ap = A - X; Bp = B - X; PC = C - A - B
    x1 = sorted(X)[0]
    bstar = next(iter(Z)) if Z else sorted(Bp)[0]
    c1 = sorted(PC)[0]
    D = frozenset([x1]) | Ap | frozenset([bstar, c1])
    assert len(D) == 6

    def final_requests(H):
        HX = H & X; HC = H & C; HB = H & Bp
        assert len(H & A) <= 1 and H & A == HX and len(H & B) <= 1 and len(HB) <= 1
        assert HC <= PC - {c1} and len(HC) in (0, 1, 4, 5)
        h = len(HC)
        if HX:                                     # case (i)
            assert not HB
            x = next(iter(HX)); Xo = X - HX
            if h <= 1:
                S1 = frozenset(sorted(C - H)[:2 - h])
                return [X | HC | S1, frozenset([x]) | (C - (H | S1))]
            if h == 4:
                xp = sorted(Xo)[0]
                return [frozenset([x, xp]) | HC, (Xo - {xp}) | HC, frozenset([x]) | (C - HC)]
            v12, v345 = split(HC, (2, 3))
            return [X | v12, frozenset([x]) | (C - v12), Xo | v345]
        else:                                      # case (ii)
            yb = frozenset([y]) | HB
            if h <= 1:
                return [X | HC, yb]
            if h == 4:
                X12, X34 = split(X, (2, 2))
                return [X12 | HC, X34 | HC, yb]
            v12, v345 = split(HC, (2, 3))
            X1, X234 = split(X, (1, 3))
            return [X | v12, X1 | yb | v345, X234 | v345]

    return D, final_requests


def run_lemma_41z(z):
    X = frozenset('x1 x2 x3 x4'.split())
    A = X | frozenset('y a1 a2'.split())
    Bp = frozenset(['z', 'b1', 'b2']) if z else frozenset(['b0', 'b1', 'b2'])
    B = X | Bp
    C = frozenset(['y'] + (['z'] if z else []) + ['c%d' % i for i in range(1, 7 - z)])
    assert len(A) == len(B) == len(C) == 7
    D, final = lemma_41z(A, B, C)
    n = 0
    seen = set()
    for H in responses([A, B, C], D):
        n += 1
        sig = (len(H & X), len(H & Bp), len(H & C))
        seen.add(sig)
        reqs = final(H)
        check_cover([A, B, C, H], reqs, 'Lemma3 z=%d H-signature %s' % (z, sig))
    print('Lemma 3 (4,1,%d): %d responses verified; (|H∩X|,|H∩B\'|,|H∩C|) signatures %s'
          % (z, n, sorted(seen)))


# ------------------------------------------------------------------ Step 2: M = 1
def step_M1():
    E = frozenset(['p'] + ['e%d' % i for i in range(1, 7)])
    F = frozenset(['p'] + ['f%d' % i for i in range(1, 7)])
    D0 = frozenset('p e1 e2 e3 f1 f2'.split())
    n = 0
    sigs = set()
    for G in responses([E, F], D0):
        n += 1
        a, b = len(G & E), len(G & F)
        sigs.add((a, b))
        assert 'p' not in G and a <= 1 and b in (0, 1, 4)
        if b <= 1:
            check_cover([E, F, G], small_cover(E, F, G), 'M1 small triple %s' % ((a, b),))
        else:
            # relabel A=F, B=G, C=E: |A∩B|=4, A∩C={p}, |B∩C|=a<=1
            A, B, C = F, G, E
            Dx, final = lemma_41z(A, B, C)
            # the closure of this triple is verified exhaustively in run_lemma_41z(a)
    print('Step 2 (M=1): %d responses to the balanced request, signatures %s' % (n, sorted(sigs)))


if __name__ == '__main__':
    import sys
    if '--cells' in sys.argv:
        EXPLICIT = False
    print('mode:', 'explicit subsets' if EXPLICIT else 'cell representatives')
    step_M0()
    step_M1()
    run_lemma_41z(1)
    run_lemma_41z(0)
    print('ALL CHECKS PASSED')
