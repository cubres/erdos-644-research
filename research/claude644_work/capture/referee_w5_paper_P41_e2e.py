# referee_w5_paper_P41_e2e.py -- adversarial END-TO-END test of Proposition 4.1 (paper_0865.md) AS WRITTEN.
# Written from scratch by the w5 Prop-4.1 referee (no imports from author scripts).
# For integer r, T (beta r + 3 <= T <= r) and EVERY integer triple (m,y,z) in the region, it
#  * classifies the triple by the paper's if-else chain (exact Fractions on m/r, y/r, z/r),
#  * builds actual sets E,F,G with the cell sizes in the ROLE ORDER the paper uses for that case,
#  * runs the lemma's construction literally (request sizes <= budget asserted, splits asserted),
#    with an adversary answering every request by an r-set avoiding it (random greedy over Venn cells,
#    half the time taking whole cells, so traces are often extreme), and
#  * checks by brute force that the final <= 7 edges have NO transversal of size <= 2.
# Usage: python3 referee_w5_paper_P41_e2e.py rmin rmax reps seed
import sys, random
from fractions import Fraction as Fr
from math import ceil

beta = Fr(173, 200); e = 1 - beta

class World:
    def __init__(self, rng):
        self.rng = rng; self.nxt = 0; self.edges = []
    def fresh(self, n):
        s = set(range(self.nxt, self.nxt + n)); self.nxt += n; return s
    def respond(self, D, r):
        pts = set().union(*self.edges) - D if self.edges else set()
        cells = {}
        for p in pts:
            cells.setdefault(tuple(p in E for E in self.edges), []).append(p)
        keys = list(cells); self.rng.shuffle(keys)
        H = set(); mode = self.rng.random()
        for k in keys:
            c = cells[k]; self.rng.shuffle(c)
            take_n = len(c) if mode < 0.5 else self.rng.randint(0, len(c))
            for p in c[:take_n]:
                if len(H) < r: H.add(p)
        if len(H) < r: H |= self.fresh(r - len(H))
        assert len(H) == r and not (H & D)
        self.edges.append(H); return H

def triple(W, r, x, y, z):
    X, Y, Z = W.fresh(x), W.fresh(y), W.fresh(z)
    PE, PF, PG = W.fresh(r-x-y), W.fresh(r-x-z), W.fresh(r-y-z)
    E, F, G = X|Y|PE, X|Z|PF, Y|Z|PG
    W.edges += [E, F, G]
    return dict(E=E, F=F, G=G, X=X, Y=Y, Z=Z, PE=PE, PF=PF, PG=PG)

def take(S, n, rng):
    L = sorted(S); rng.shuffle(L); assert 0 <= n <= len(L), ("take", n, len(L)); return set(L[:n])

def distribute(reqs, extra, T):
    extra = sorted(extra)
    for R in reqs:
        while extra and len(R) < T: R.add(extra.pop())
    assert not extra, ("distribution failed",)

def finish(W, reqs, T, r):
    for R in reqs: assert len(R) <= T, ("request too big", len(R), T)
    for R in reqs: W.respond(set(R), r)

def has_2transversal(edges):
    full = (1 << len(edges)) - 1
    ml = list({sum(1 << i for i, E in enumerate(edges) if p in E) for p in set().union(*edges)})
    return any(ml[i] | ml[j] == full for i in range(len(ml)) for j in range(i, len(ml)))

def L31(W, r, x, y, z, rng):          # Lemma 3.1 (x>=y>=z, m=x), own budget B
    m = x; B = ceil(max(Fr(3*r+m, 4), Fr(2*r+2*m, 3)))
    t = triple(W, r, x, y, z)
    AF = take(t['PF'], B-x-y, rng); B0 = take(t['PG'], min(B-x, r-y-z), rng)
    C = t['G'] - (t['Y'] | B0); AE = take(t['PE'], min(B-x-len(C), r-x-y), rng)
    finish(W, [t['X']|t['Y']|AF, t['X']|B0, t['X']|C|AE, t['Y']|t['Z']|(t['PE']-AE)|(t['PF']-AF)], B, r)
    return B

def L32(W, r, T, x, y, z, rng):       # Lemma 3.2
    t = triple(W, r, x, y, z); X, Y, Z = t['X'], t['Y'], t['Z']
    assert len(X|Y|Z) <= T
    H = W.respond(X|Y|Z, r)
    A, B, C = t['F'] & H, t['G'] & H, t['E'] & H; a, b, c = len(A), len(B), len(C)
    if b <= T - x:
        A1 = take(A, min(a, T-y-z-c), rng); reqs = [X|B, Y|Z|C|A1, Y|(A-A1)]
    elif a <= T - y:
        B1 = take(B, min(b, T-x-z-c), rng); reqs = [Y|A, X|Z|C|B1, X|(B-B1)]
    else:
        B2 = take(B, T-x, rng); A3 = take(A, T-y, rng)
        reqs = [X|B2, Y|A3, X|Y|Z|C|(A-A3)|(B-B2)]
    finish(W, reqs, T, r)

def L33(W, r, T, x, y, z, rng):       # Lemma 3.3
    t = triple(W, r, x, y, z); X, Y, Z = t['X'], t['Y'], t['Z']; S = x+y+z
    H = W.respond(X|Y|Z|take(t['PF'], T-S, rng), r)
    A, B, C = t['F'] & H, t['G'] & H, t['E'] & H
    if len(A) <= T - y - z:
        B1 = take(B, min(len(B), T-x-z), rng)
        reqs = [X|Z|B1, X|Z|(B-B1), Y|Z|A]
        for R in reqs: assert len(R) <= T
        distribute(reqs, C, T)
    else:
        BC = B | C; p1 = take(BC, min(len(BC), T-x-z), rng)
        reqs = [X|Z|p1, X|Z|(BC-p1), Y|A]
    finish(W, reqs, T, r)

def L34(W, r, T, x, y, z, rng):       # Lemma 3.4
    t = triple(W, r, x, y, z); X, Y, Z, E = t['X'], t['Y'], t['Z'], t['E']
    H = W.respond(X|Y|take(Z, min(z, T-x-y), rng), r)
    Q = Z & H; A = (t['F'] & H) - Q; B = (t['G'] & H) - Q; C = E & H
    V = Z - Q; D = E - (X|Y|C)
    q, a, b, c, v = len(Q), len(A), len(B), len(C), len(V)
    if c <= T - z:
        reqs = [Q|X|B, Q|Y|A, Z|C]
    else:
        a0 = r+x+z-2*T; b0 = r+y+z-2*T
        if a < a0:
            C2 = take(C, min(c, T-y-a-z), rng); assert len(C - C2) <= T - z
            reqs = [Q|X|B, Y|A|Z|C2, Z|(C-C2)]
        elif b < b0:
            C2 = take(C, min(c, T-x-b-z), rng); assert len(C - C2) <= T - z
            reqs = [Q|Y|A, X|B|Z|C2, Z|(C-C2)]
        else:
            u = c + z - T; assert 0 < u <= c
            C12 = take(C, u, rng)
            lo = max(0, y+a+z+u-T); hi = min(v, T-q-x-b-u)
            assert lo <= hi, ("empty t interval", lo, hi)
            V13 = take(V, rng.randint(lo, hi), rng)
            reqs = [Q|X|B|C12|V13, Q|Y|A|C12|(V-V13), Z|(C-C12)]
    for R in reqs: assert len(R) <= T
    distribute(reqs, D, T)
    finish(W, reqs, T, r)

def S1(W, r, T, x, y, z, x1, y1, z1, rng):   # Lemma 3.5
    assert 0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z
    t = triple(W, r, x, y, z); X, Y, Z = t['X'], t['Y'], t['Z']
    X1, Y1, Z1 = take(X, x1, rng), take(Y, y1, rng), take(Z, z1, rng)
    X2, Y2, Z2 = X - X1, Y - Y1, Z - Z1
    finish(W, [X1|Y1|Z1, X|t['PG']|Y2|Z2, Y|t['PF']|X2|Z2, Z|t['PE']|X2|Y2], T, r)

def S2(W, r, T, x, y, z, rng):        # Lemma 3.6
    P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
    t = triple(W, r, x, y, z); X, Y, Z = t['X'], t['Y'], t['Z']
    V1 = take(t['PF'], P, rng); W13 = take(t['PG'], Q, rng)
    U1 = T - r + x - z - P - Q; L = x + y + z + Q - T
    lo, hi = max(0, L), min(x, U1); assert lo <= hi, ("S2 empty", lo, hi)
    X01 = take(X, rng.randint(lo, hi), rng)
    finish(W, [X|(t['PG']-W13), X01|Y|Z|t['PE']|V1|W13, Y|(t['PF']-V1), (X-X01)|Y|Z|W13], T, r)

def run_case(r, T, m, y, z, rng):
    W = World(rng)
    M, Yn, Zn = Fr(m, r), Fr(y, r), Fr(z, r)
    if M <= Fr(119, 400):
        B = L31(W, r, m, y, z, rng); assert B <= T; tag = 'a'
    elif Yn <= Fr(73, 200):
        Sn = M + Yn + Zn
        if Yn - Zn > M - e: L33(W, r, T, m, y, z, rng); tag = 'b2'
        elif Sn < Fr(81, 200): L33(W, r, T, z, y, m, rng); tag = 'b3'
        else: L34(W, r, T, z, y, m, rng); tag = 'b1'
    else:
        u = M + Yn; d = M - Yn
        if Zn <= Fr(319, 200) - 2*u: L32(W, r, T, m, y, z, rng); tag = 'c1'
        elif Zn < e - d: S2(W, r, T, y, m, z, rng); tag = 'c2'
        elif Zn <= (Fr(146, 200) - Yn) / 2: S2(W, r, T, m, y, z, rng); tag = 'c3'
        else:
            if 3*Zn >= e + u:
                m1, y1, z1 = (e+Yn+Zn-M)/2, (e+M+Zn-Yn)/2, (e+M+Yn-Zn)/2; tag = 'c4A'
            else:
                z1, y1, m1 = Zn, e+M-Zn, e+Yn-Zn; tag = 'c4B'
            hm, hy, hz = ceil(m1*r), ceil(y1*r), ceil(z1*r)
            assert (hm+hy+hz <= T and hy+hz >= r+m-T and hm+hz >= r+y-T and hm+hy >= r+z-T), (tag,)
            S1(W, r, T, m, y, z, hm, hy, hz, rng)
    assert len(W.edges) <= 7 and not (W.edges[0] & W.edges[1] & W.edges[2])
    if has_2transversal(W.edges):
        raise AssertionError(("2-transversal", r, T, m, y, z, tag))
    return tag

def sweep(rs, reps, rng, Tfun):
    from collections import Counter
    cnt = Counter()
    for r in rs:
        for T in Tfun(r, rng):
            for m in range(0, r // 2 + 1):
                if Fr(m, r) > Fr(23, 50): break
                for y in range(0, m + 1):
                    if Fr(m + 2*y, r) > Fr(227, 200): break
                    for z in range(0, y + 1):
                        for _ in range(reps):
                            cnt[run_case(r, T, m, y, z, rng)] += 1
    return cnt

def Tclaimed(r, rng):
    Tmin = ceil(beta * r + 3)
    return [] if Tmin > r else sorted({Tmin, r, rng.randint(Tmin, r)})

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[4]))
    cnt = sweep(range(int(sys.argv[1]), int(sys.argv[2]) + 1), int(sys.argv[3]), rng, Tclaimed)
    print("PASS", sum(cnt.values()), "runs", dict(cnt))
