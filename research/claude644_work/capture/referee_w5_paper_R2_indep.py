# Independent referee check (w5 paper, referee R2) of Proposition 4.1 of paper_0865.tex.
# Written from the paper's LEMMA STATEMENTS only (Section 3), not from its derived inequalities.
# For integers r, T (beta r + 3 <= T <= r) and every integer triple m>=y>=z>=0 with
# m <= 23r/50, m+2y <= 227r/200, the case chain of Prop 4.1 (on normalised values, exact Fractions)
# is evaluated and the hypotheses of the lemma used are tested at the INTEGER level (r,T), with the
# role assignment of the paper. Case (a) uses Lemma 3.1 with its own budget B. Case (c4) uses
# Lemma 3.5 with ceil-rounded splits. Exact arithmetic throughout.
import sys, random
from fractions import Fraction as Fr
from math import ceil, floor

beta = Fr(173, 200); e = 1 - beta

def L31(r, T, m):   # all three cells <= m <= r/2, tau > B
    B = ceil(max(Fr(3*r + m, 4), Fr(2*r + 2*m, 3)))
    return 2*m <= r and B <= T

def L32(r, T, x, y, z):
    S = x + y + z
    return all([T >= S, T >= r - x + z, T >= r - y + z, 2*T >= 2*r - 2*x + y,
                2*T >= 2*r - 2*y + x, 3*T >= r + 2*x + 2*y + z])

def L33(r, T, x, y, z):
    S = x + y + z
    return all([T <= r, T >= S, 2*T >= r + 2*y, 2*T >= r + 2*x - y + z, 3*T >= r + 2*x + y + 3*z])

def L34(r, T, x, y, z):
    S = x + y + z
    return all([T <= r, T >= x + y, 2*T >= r + 2*x, 2*T >= r + 2*y, T >= r + x - y - z,
                T >= r - x + y - z, 3*T >= 3*r - S, 5*T >= 3*r + S, 3*T >= r + x + y + 2*z,
                4*T >= 2*r + 3*z])

def L35(r, T, x, y, z, x1, y1, z1):
    return all([0 <= x1 <= x, 0 <= y1 <= y, 0 <= z1 <= z, x1 + y1 + z1 <= T,
                y1 + z1 >= r + x - T, x1 + z1 >= r + y - T, x1 + y1 >= r + z - T])

def L36(r, T, x, y, z):
    P = max(0, r + y - x - z - T); Q = max(0, r + x - y - z - T)
    return all([x <= T, y <= T, T >= r - x + z + P + Q, T >= y + z + Q, 2*T >= r + y + 2*z + P + 2*Q])

def check(r, T, M, Y, Z):
    m, y, z = Fr(M, r), Fr(Y, r), Fr(Z, r)
    if m <= Fr(119, 400):
        return 'a', L31(r, T, M)
    if y <= Fr(73, 200):
        S = m + y + z
        if y - z > m - e: return 'b2', L33(r, T, M, Y, Z)
        if S < Fr(81, 200): return 'b3', L33(r, T, Z, Y, M)
        return 'b1', L34(r, T, Z, Y, M)
    u = m + y; d = m - y
    if z <= Fr(319, 200) - 2*u: return 'c1', L32(r, T, M, Y, Z)
    if z < e - d: return 'c2', L36(r, T, Y, M, Z)
    if z <= (Fr(146, 200) - y) / 2: return 'c3', L36(r, T, M, Y, Z)
    if 3*z >= e + u:
        m1 = (e + y + z - m) / 2; y1 = (e + m + z - y) / 2; z1 = (e + m + y - z) / 2; tag = 'c4A'
    else:
        z1 = z; y1 = e + m - z; m1 = e + y - z; tag = 'c4B'
    return tag, L35(r, T, M, Y, Z, ceil(m1 * r), ceil(y1 * r), ceil(z1 * r))

def run(r, T, sample=None):
    assert beta * r + 3 <= T <= r
    cnt = {}; bad = []
    it = 0
    for M in range(0, (23 * r) // 50 + 1):
        for Y in range(0, M + 1):
            if 200 * (M + 2 * Y) > 227 * r: break
            for Z in range(0, Y + 1):
                if sample and random.random() > sample: continue
                tag, ok = check(r, T, M, Y, Z)
                cnt[tag] = cnt.get(tag, 0) + 1
                if not ok: bad.append((tag, M, Y, Z))
    return cnt, bad

if __name__ == '__main__':
    random.seed(1)
    for r in [int(a) for a in sys.argv[1:]] or [200, 333, 401]:
        for T in sorted({ceil(beta * r + 3), r}):
            if not (beta * r + 3 <= T <= r): continue
            cnt, bad = run(r, T)
            print(r, T, 'total', sum(cnt.values()), dict(sorted(cnt.items())), 'FAIL', len(bad), bad[:5])
            # mutation: budget one less than required must fail somewhere (sensitivity)
    # mutation test: shrink beta-margin
    r = 401; T = ceil(beta * r + 3) - 4
    cnt, bad = run(r, T)
    print('mutation r=401 T=', T, 'FAIL', len(bad), 'by case', {t: sum(1 for b in bad if b[0] == t) for t in cnt})
