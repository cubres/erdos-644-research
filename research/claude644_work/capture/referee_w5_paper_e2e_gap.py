# referee_w5_paper_e2e_gap.py (w5 referee, independent): end-to-end simulation of Lemma 5.1
# (gap extension), Lemma 5.3 (conditional finish, with Lemmas 3.1 and 5.2) of paper_0865.tex at
# r >= 1000, implemented from the paper text on actual sets.  The adversary answers every request
# with an r-set avoiding it; it is constrained ONLY by the gap facts that the proof invokes
# (an intersection the proof bounds by <= h r (5.1) or <= r/2 (5.3) must then lie below l r, resp.
# be <= m).  All other intersection sizes are free (more adversarial than a real family).
# Final check: the <=7 constructed edges have no transversal of size <= 2; all requests <= budget.
import random, sys
from fractions import Fraction as Fr

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
NIT = int(sys.argv[2]) if len(sys.argv) > 2 else 300
beta = Fr(173, 200); h = Fr(23, 50); ell = Fr(43, 200)
def cdiv(a, d): return -((-a) // d)
def ceilfr(q): return -((-q.numerator) // q.denominator)

class Uni:
    def __init__(s): s.n = 0
    def fresh(s, k):
        out = set(range(s.n, s.n + k)); s.n += k; return out

def is_bad(edges):
    pts = set().union(*edges); full = (1 << len(edges)) - 1; types = {}
    for p in pts:
        t = 0
        for i, e in enumerate(edges):
            if p in e: t |= 1 << i
        types[t] = types.get(t, 0) + 1
    types[0] = types.get(0, 0) + 1
    tl = list(types)
    for a in tl:
        if a == full: return False
        for b in tl:
            if a | b == full and (a != b or types[a] >= 2): return False
    return True

def respond(U, r, D, quotas):
    """r-set avoiding D.  quotas: list of (pool_set, lo, hi) -> take k in [lo,hi] points of pool\\D
    (pools disjoint, processed in order; already-chosen points count).  Rest: random old pts / fresh."""
    D = set(D); ch = set()
    for pool, lo, hi in quotas:
        avail = sorted((pool - D) - ch)
        have = len(ch & pool)
        hi2 = min(hi - have, len(avail), r - len(ch)); lo2 = max(0, lo - have)
        if hi2 < lo2: return None
        k = rng.choice([lo2, hi2, rng.randint(lo2, hi2)])
        ch |= set(rng.sample(avail, k))
    ch |= U.fresh(r - len(ch))
    assert len(ch) == r and not (ch & D)
    return ch

FAIL = []; STATS = {}
def stat(k): STATS[k] = STATS.get(k, 0) + 1

def final(tag, edges, reqs, budget, U, r, info):
    for R in reqs:
        if len(R) > budget: FAIL.append((tag, 'size', len(R), budget, info)); return
    resp = [U.fresh(0) | respond(U, r, R, [(set().union(*edges), 0, r)]) for R in reqs]
    allE = edges + resp
    if len(allE) > 7: FAIL.append((tag, '>7', info)); return
    if not is_bad(allE): FAIL.append((tag, 'notbad', info))
    stat(tag)

def take(s, k):
    s = sorted(s); assert 0 <= k <= len(s), (k, len(s)); return set(s[:k]), set(s[k:])

# ---------- Lemma 3.1 on actual sets (good triple, all pair intersections <= m <= r/2) ----------
def L18_actual(E, F, G, r, m, budget_T, U, tag):
    import itertools
    best = None
    for (a, b_, c) in itertools.permutations([E, F, G]):
        key = (len(a & b_), len(a & c))
        if best is None or key > best[0]: best = (key, (a, b_, c))
    E, F, G = best[1]
    X, Y, Z = E & F, E & G, F & G
    assert not (E & F & G) and len(X) >= len(Y) >= len(Z) and max(len(X), len(Y), len(Z)) <= m <= r / 2
    PE, PF, PG = E - F - G, F - E - G, G - E - F
    x, y, z = len(X), len(Y), len(Z)
    B = max(cdiv(3*r + m, 4), cdiv(2*r + 2*m, 3))
    if B > budget_T: FAIL.append((tag, 'L18 budget', B, budget_T)); return
    AF, _ = take(PF, B - x - y)
    B0, restG = take(PG, min(B - x, r - y - z))
    C = Z | restG
    AE, restE = take(PE, min(B - x - len(C), r - x - y))
    reqs = [X | Y | AF, X | B0, X | C | AE, Y | Z | restE | (PF - AF)]
    final(tag, [E, F, G], reqs, B, U, r, (r, m, x, y, z))

# ---------------- Lemma 5.1 ----------------
def lemma51(r):
    U = Uni(); cb = cdiv(173*r, 200); T = cb + 4; h0 = (23*r)//50
    lr_below = cdiv(43*r, 200) - 1          # largest integer < l r
    x = rng.randint(cdiv(23*r, 50), r//2)
    X = U.fresh(x); E = X | U.fresh(r - x); F = X | U.fresh(r - x)
    # balanced request, T0 = ceil(beta r)
    e1 = (cb + x)//2; g1 = cb + x - e1
    Ep = X | set(sorted(E - X)[:e1 - x]); Gp = X | set(sorted(F - X)[:g1 - x])
    assert len(Ep | Gp) == cb
    G = respond(U, r, Ep | Gp, [(E - X, 0, lr_below), (F - X, 0, lr_below)])
    Y, Z = E & G, F & G; y, z = len(Y), len(Z); S = x + y + z
    assert max(y, z) < Fr(43*r, 200) and not (E & F & G)
    PE, PF, PG = E - F - G, F - E - G, G - E - F
    if S <= T:
        p = max(0, r - x - y - h0); t = max(0, r - x - z - h0)
        P1, _ = take(PE, p); P2, _ = take(PF, t)
        core = X | Y | Z | P1 | P2
        if len(core) > T: FAIL.append(('5.1a', 'core', r, x, y, z)); return
        W, _ = take(PG, T - len(core)); D = core | W
        # gap: E n H (<= h0) and F n H must be < l r; G n H free
        H = respond(U, r, D, [(PE, 0, lr_below), (PF, 0, lr_below), (PG, 0, r)])
        Bs = G & H; Bl = sorted(Bs); half = cdiv(len(Bl), 2)
        B1, B2 = set(Bl[:half]), set(Bl[half:])
        reqs = [X | B1, X | B2, Y | Z | (E & H) | (F & H)]
        final('5.1 S<=T', [E, F, G, H], [D] + reqs, T, U, r, (r, x, y, z))
    else:
        Z0, _ = take(Z, T - x - y); D = X | Y | Z0
        assert len(D) == T
        # gap: c = |E n H| < l r, q + a = |F n H| < l r; G n H free (B any size)
        H = respond(U, r, D, [(Z - Z0, 0, lr_below), (PF, 0, lr_below), (PE, 0, lr_below), (PG, 0, r)])
        Q = Z & H; A = (F & H) - Q; Bs = (G & H) - Q; C = E & H
        Bl = sorted(Bs); half = cdiv(len(Bl), 2)
        R1, R2, R3 = X | Q | set(Bl[:half]), X | Q | set(Bl[half:]), Y | Z | A | C
        reqs = [R1, R2, R3]
        for R in reqs:
            if len(R) > T: FAIL.append(('5.1b', 'pre', len(R), T, r, x, y, z)); return
        Dl = sorted(E - X - Y - C)
        for R in reqs:
            while Dl and len(R) < T: R.add(Dl.pop())
        if Dl: FAIL.append(('5.1b', 'dist', r, x, y, z)); return
        final('5.1 S>T', [E, F, G, H], [D] + reqs, T, U, r, (r, x, y, z))

# ---------------- Lemma 5.2 on actual sets ----------------
def lemma52(E, F, G, H, r, m, T, U, tag):
    X, B = E & F, G & H; Y, Z, A, C = E & G, F & G, F & H, E & H
    x, b = len(X), len(B)
    s, t = len(Y) + len(Z), len(A) + len(C)
    half_up = cdiv(r, 2)
    p = half_up - min(s, t); q = T - half_up - max(s, t)
    B0, _ = take(B, p); X0, _ = take(X, q)
    Dreq = Y | Z | A | C | B0 | X0
    assert len(Dreq) == T
    # gap facts used: |G n I|, |H n I| <= m (they are <= floor(r/2)); E, F free
    I = respond(U, r, Dreq, [(G - Y - Z - B0, 0, m), (H - A - C - B0, 0, m), (E | F, 0, r)])
    if I is None: FAIL.append((tag, 'I none')); return
    if len(G & I) > m or len(H & I) > m: FAIL.append((tag, 'gapI')); return
    BI = B & I
    B1 = set(BI) | set(sorted(B - BI)[:min(b, T - x) - len(BI)])
    assert len(B1) == min(b, T - x)
    reqs = [X | B1, (X & I) | (B - B1)]
    final(tag, [E, F, G, H, I], [Dreq] + reqs, T, U, r, (r, m, x, b))

# ---------------- Lemma 5.3 ----------------
def lemma53(r):
    U = Uni(); cb = cdiv(173*r, 200); T = cb + 4
    mcap = (119*r)//400
    m = rng.choice([rng.randint(0, mcap), mcap, rng.randint(0, r - T), r - T, max(0, r - T - 1)])
    Y = U.fresh(m); E = Y | U.fresh(r - m); G = Y | U.fresh(r - m)
    e1 = (T + m)//2; g1 = T + m - e1
    Ep = Y | set(sorted(E - Y)[:e1 - m]); Gp = Y | set(sorted(G - Y)[:g1 - m])
    assert len(Ep | Gp) == T
    # F: |E n F|, |G n F| each <= m or > r/2 (adversary picks which)
    availE = r - e1; availG = r - g1
    modeE = rng.random() < 0.5 and availE > r//2
    modeG = (not modeE) and rng.random() < 0.5 and availG > r//2
    qE = (r//2 + 1, availE) if modeE else (0, m)
    qG = (r//2 + 1, availG) if modeG else (0, m)
    F = respond(U, r, Ep | Gp, [(E - Ep, qE[0], qE[1]), (G - Gp, qG[0], qG[1])])
    if F is None: return
    ef, gf = len(E & F), len(G & F)
    if ef <= r/2 and gf <= r/2:
        L18_actual(E, F, G, r, m, T, U, '5.3 L18(EFG)'); return
    if gf > r/2: E, G = G, E
    X = E & F; Z = F & G; x, z = len(X), len(Z)
    assert x > r/2 and z <= m and len(E & G) == m
    PE, PF, PG = E - F - G, F - E - G, G - E - F
    k = T - x - m - z
    if not (0 < k <= len(PG)): FAIL.append(('5.3', 'pad', r, m, x, z)); return
    pad, _ = take(PG, k); D = X | Y | Z | pad
    assert len(D) == T
    rest = PG - pad
    mode = rng.random() < 0.5 and len(rest) > r//2
    qB = (r//2 + 1, len(rest)) if mode else (0, m)
    H = respond(U, r, D, [(PE, 0, m), (PF, 0, m), (rest, qB[0], qB[1])])
    if H is None: return
    b = len(G & H)
    if b <= r/2:
        L18_actual(E, G, H, r, m, T, U, '5.3 L18(EGH)'); return
    lemma52(E, F, G, H, r, m, T, U, '5.3 L41')

for it in range(NIT):
    r = rng.choice([1000, 1001, 1003, 1199, rng.randint(1000, 2500)])
    lemma51(r)
    for _ in range(3): lemma53(r)
print('STATS', STATS)
print('FAILURES', len(FAIL), FAIL[:10])
