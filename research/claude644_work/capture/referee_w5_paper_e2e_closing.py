# referee_w5_paper_e2e_closing.py  (w5 referee, independent of all earlier scripts)
# End-to-end simulation of the closing lemmas of paper_0865.tex Section 3 (L18=Lemma 3.1,
# L26=3.2, L32=3.3, L31=3.4, S1=3.5, S2=3.6), implemented directly from the paper text.
# Responses are adversarial random r-sets avoiding the request (biased to reuse existing points).
# Final check: the constructed <=7 edges have NO transversal of size <=2 (type-based exact check),
# and every request has size <= its budget.  Integer data, r-uniform.
import random, sys, itertools
from math import ceil, floor

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N_ITER = int(sys.argv[2]) if len(sys.argv) > 2 else 4000

class Uni:
    def __init__(s): s.n = 0
    def fresh(s, k):
        out = list(range(s.n, s.n + k)); s.n += k; return out

def triple(U, r, x, y, z):
    X, Y, Z = U.fresh(x), U.fresh(y), U.fresh(z)
    PE, PF, PG = U.fresh(r - x - y), U.fresh(r - x - z), U.fresh(r - y - z)
    E = set(X + Y + PE); F = set(X + Z + PF); G = set(Y + Z + PG)
    return E, F, G, X, Y, Z, PE, PF, PG

def respond(U, r, D, edges):
    """adversarial response: an r-set avoiding D; reuse many points of existing edges."""
    D = set(D)
    pool = sorted(set().union(*edges) - D)
    k = rng.randint(0, min(r, len(pool)))
    # bias: sometimes grab as many old points as possible
    if rng.random() < 0.4: k = min(r, len(pool))
    chosen = set(rng.sample(pool, k))
    chosen |= set(U.fresh(r - len(chosen)))
    assert len(chosen) == r and not (chosen & D)
    return chosen

def is_bad(edges):
    edges = list(edges)
    pts = set().union(*edges)
    full = (1 << len(edges)) - 1
    types = {}
    for p in pts:
        t = 0
        for i, e in enumerate(edges):
            if p in e: t |= 1 << i
        types[t] = types.get(t, 0) + 1
    types[0] = types.get(0, 0) + 1  # an outside point
    tl = list(types)
    for a in tl:
        if a == full: return False
        for b in tl:
            if a | b == full:
                if a != b or types[a] >= 2: return False
    return True

FAIL = []
def check(name, edges, reqs, budget, info):
    for D in reqs:
        if len(D) > budget:
            FAIL.append((name, 'size', len(D), budget, info)); return
    if not is_bad(edges):
        FAIL.append((name, 'notbad', info))

def take(lst, k):
    assert 0 <= k <= len(lst), (k, len(lst))
    return lst[:k], lst[k:]

# ---------------- Lemma 3.1 (L18) ----------------
def L18(r, x, y, z, m):
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    B = ceil(max((3*r + m)/4, (2*r + 2*m)/3))  # exact enough: use fractions below
    from fractions import Fraction as Fr
    B = max(-((-(3*r+m))//4), -((-(2*r+2*m))//3))
    # paper assumes x>=y>=z after relabelling; we relabel explicitly
    cells = sorted([(x, 'X'), (y, 'Y'), (z, 'Z')], reverse=True)
    # rebuild triple with sorted sizes (relabelling = permuting edges)
    xs, ys, zs = cells[0][0], cells[1][0], cells[2][0]
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, xs, ys, zs)
    AF, _ = take(PF, B - xs - ys)
    B0, restG = take(PG, min(B - xs, r - ys - zs))
    C = Z + restG
    AE, restE = take(PE, min(B - xs - len(C), r - xs - ys))
    D1 = set(X + Y + AF); D2 = set(X + B0); D3 = set(X + C + AE)
    D4 = set(Y + Z + restE + [p for p in PF if p not in set(AF)])
    base = [E, F, G]
    resp = [respond(U, r, D, base) for D in (D1, D2, D3, D4)]
    check('L18', base + resp, [D1, D2, D3, D4], B, (r, x, y, z, m))

# ---------------- Lemma 3.2 (L26) ----------------
def L26(r, x, y, z, T):
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    base = [E, F, G]
    D0 = set(X + Y + Z); H = respond(U, r, D0, base)
    if len(D0) > T: FAIL.append(('L26', 'D0', r, x, y, z, T)); return
    A = sorted(F & H); Bs = sorted(G & H); C = sorted(E & H)
    a, b, c = len(A), len(Bs), len(C)
    if b <= T - x:
        cap1 = T - y - z - c
        A1, A2 = A[:max(0, min(a, cap1))], A[max(0, min(a, cap1)):]
        reqs = [set(X + Bs), set(Y + Z + C + A1), set(Y + A2)]
    elif a <= T - y:
        cap1 = T - x - z - c
        B1, B2 = Bs[:max(0, min(b, cap1))], Bs[max(0, min(b, cap1)):]
        reqs = [set(Y + A), set(X + Z + C + B1), set(X + B2)]
    else:
        B2, Brest = Bs[:T - x], Bs[T - x:]
        A3, Arest = A[:T - y], A[T - y:]
        reqs = [set(X + B2), set(Y + A3), set(X + Y + Z + C + Arest + Brest)]
    resp = [respond(U, r, D, base + [H]) for D in reqs]
    check('L26', base + [H] + resp, reqs, T, (r, x, y, z, T, a, b, c))

def distribute(reqs, D, T):
    D = list(D)
    for R in reqs:
        while D and len(R) < T: R.add(D.pop())
    return not D

# ---------------- Lemma 3.3 (L32) ----------------
def L32(r, x, y, z, T):
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    base = [E, F, G]
    S = x + y + z
    pad, _ = take(PF, T - S)
    D0 = set(X + Y + Z + pad); H = respond(U, r, D0, base)
    A = sorted(F & H); Bs = sorted(G & H); C = sorted(E & H)
    a, b, c = len(A), len(Bs), len(C)
    if a <= T - y - z:
        k = T - x - z
        B1, B2 = Bs[:k], Bs[k:]
        reqs = [set(X + Z + B1), set(X + Z + B2), set(Y + Z + A)]
        if not distribute(reqs, C, T): FAIL.append(('L32', 'dist', r, x, y, z, T)); return
    else:
        k = T - x - z; BC = Bs + C
        reqs = [set(X + Z + BC[:k]), set(X + Z + BC[k:]), set(Y + A)]
    resp = [respond(U, r, D, base + [H]) for D in reqs]
    check('L32', base + [H] + resp, [D0] + reqs, T, (r, x, y, z, T, a, b, c))

# ---------------- Lemma 3.4 (L31) ----------------
def L31(r, x, y, z, T):
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    base = [E, F, G]
    Z0 = Z[:min(z, T - x - y)]
    D0 = set(X + Y + Z0); H = respond(U, r, D0, base)
    Hs = H
    Q = sorted(set(Z) & Hs); A = sorted((F & Hs) - set(Q)); Bs = sorted((G & Hs) - set(Q))
    C = sorted(E & Hs); V = [p for p in Z if p not in set(Q)]
    Dset = [p for p in E if p not in set(X) | set(Y) | set(C)]
    q, a, b, c, v = len(Q), len(A), len(Bs), len(C), len(V)
    a0 = r + x + z - 2*T; b0 = r + y + z - 2*T
    if c <= T - z:
        reqs = [set(Q + X + Bs), set(Q + Y + A), set(Z + C)]; case = 0
    elif a < a0:
        k = T - y - a - z
        reqs = [set(Q + X + Bs), set(Y + A + Z + C[:k]), set(Z + C[k:])]; case = 1
    elif b < b0:
        k = T - x - b - z
        reqs = [set(Q + Y + A), set(X + Bs + Z + C[:k]), set(Z + C[k:])]; case = 2
    else:
        u = c + z - T
        C12, C3 = C[:u], C[u:]
        lo = max(0, y + a + z + u - T); hi = min(v, T - q - x - b - u)
        if lo > hi: FAIL.append(('L31', 'interval', r, x, y, z, T, q, a, b, c)); return
        t = rng.randint(lo, hi)
        reqs = [set(Q + X + Bs + C12 + V[:t]), set(Q + Y + A + C12 + V[t:]), set(Z + C3)]; case = 3
    for R in reqs:
        if len(R) > T: FAIL.append(('L31', 'pre', case, r, x, y, z, T, q, a, b, c)); return
    if not distribute(reqs, Dset, T): FAIL.append(('L31', 'dist', case, r, x, y, z, T)); return
    resp = [respond(U, r, D, base + [H]) for D in reqs]
    check('L31', base + [H] + resp, [D0] + reqs, T, (case, r, x, y, z, T, q, a, b, c))

# ---------------- Lemma 3.5 (S1) ----------------
def S1(r, x, y, z, T, x1, y1, z1):
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    base = [E, F, G]
    X1, X2 = X[:x1], X[x1:]; Y1, Y2 = Y[:y1], Y[y1:]; Z1, Z2 = Z[:z1], Z[z1:]
    reqs = [set(X1 + Y1 + Z1), set(X + PG + Y2 + Z2), set(Y + PF + X2 + Z2), set(Z + PE + X2 + Y2)]
    resp = [respond(U, r, D, base) for D in reqs]
    check('S1', base + resp, reqs, T, (r, x, y, z, T, x1, y1, z1))

# ---------------- Lemma 3.6 (S2) ----------------
def S2(r, x, y, z, T):
    P = max(0, r + y - x - z - T); Q = max(0, r + x - y - z - T)
    U = Uni(); E, F, G, X, Y, Z, PE, PF, PG = triple(U, r, x, y, z)
    base = [E, F, G]
    V1, V2 = PF[:P], PF[P:]; W13, W0 = PG[:Q], PG[Q:]
    U1 = T - r + x - z - P - Q; L = x + y + z + Q - T
    lo, hi = max(0, L), min(x, U1)
    if lo > hi: FAIL.append(('S2', 'interval', r, x, y, z, T)); return
    x01 = rng.randint(lo, hi)
    X01, X03 = X[:x01], X[x01:]
    reqs = [set(X + W0), set(X01 + Y + Z + PE + V1 + W13), set(Y + V2), set(X03 + Y + Z + W13)]
    resp = [respond(U, r, D, base) for D in reqs]
    check('S2', base + resp, reqs, T, (r, x, y, z, T, x01))

# hypotheses (integer, as stated in the paper)
def hyp_L26(r, x, y, z, T):
    S = x + y + z
    return 2*T >= 0 and T >= S and T >= r - x + z and T >= r - y + z and 2*T >= 2*r - 2*x + y \
        and 2*T >= 2*r - 2*y + x and 3*T >= r + 2*x + 2*y + z
def hyp_L32(r, x, y, z, T):
    S = x + y + z
    return T <= r and T >= S and 2*T >= r + 2*y and 2*T >= r + 2*x - y + z and 3*T >= r + 2*x + y + 3*z
def hyp_L31(r, x, y, z, T):
    S = x + y + z
    return (T <= r and T >= x + y and 2*T >= r + 2*x and 2*T >= r + 2*y and T >= r + x - y - z
            and T >= r - x + y - z and 3*T >= 3*r - S and 5*T >= 3*r + S and 3*T >= r + x + y + 2*z
            and 4*T >= 2*r + 3*z)
def hyp_S2(r, x, y, z, T):
    P = max(0, r + y - x - z - T); Q = max(0, r + x - y - z - T)
    return x <= T and y <= T and T >= r - x + z + P + Q and T >= y + z + Q and 2*T >= r + y + 2*z + P + 2*Q

cnt = {}
for it in range(N_ITER):
    r = rng.randint(4, 36)
    # random triple sizes with pair sums <= r
    while True:
        x, y, z = rng.randint(0, r), rng.randint(0, r), rng.randint(0, r)
        if x + y <= r and x + z <= r and y + z <= r: break
    T = rng.randint(1, r)
    if hyp_L26(r, x, y, z, T): L26(r, x, y, z, T); cnt['L26'] = cnt.get('L26', 0) + 1
    if hyp_L32(r, x, y, z, T): L32(r, x, y, z, T); cnt['L32'] = cnt.get('L32', 0) + 1
    if hyp_L31(r, x, y, z, T):
        for _ in range(3): L31(r, x, y, z, T)
        cnt['L31'] = cnt.get('L31', 0) + 1
    if hyp_S2(r, x, y, z, T): S2(r, x, y, z, T); cnt['S2'] = cnt.get('S2', 0) + 1
    m = max(x, y, z)
    if 2*m <= r: L18(r, x, y, z, m); cnt['L18'] = cnt.get('L18', 0) + 1
    # S1: random splits satisfying the hypotheses
    for _ in range(5):
        x1, y1, z1 = rng.randint(0, x), rng.randint(0, y), rng.randint(0, z)
        if x1 + y1 + z1 <= T and y1 + z1 >= r + x - T and x1 + z1 >= r + y - T and x1 + y1 >= r + z - T:
            S1(r, x, y, z, T, x1, y1, z1); cnt['S1'] = cnt.get('S1', 0) + 1
            break
print('instances', cnt)
print('FAILURES', len(FAIL), FAIL[:10])
