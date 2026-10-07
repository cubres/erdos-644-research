# referee_w5_paper_prop_int.py (w5 referee, independent): integer-level check of Proposition 4.1 of
# paper_0865.tex.  For integer r and the smallest allowed T = ceil(beta r + 3) (lemma hypotheses are
# monotone in T, shown in Lemma 3.7; T<=r checked), enumerate integer (m,y,z) with
# 0<=z<=y<=m<=23r/50, m+2y<=227r/200, follow the paper's case chain (decisions on normalised
# values, exact Fractions), and check the INTEGER hypotheses of the lemma used, as stated in
# Section 3, with the paper's role assignment.  (a): Lemma 3.1 budget B <= T.  (c4): rounded splits.
import sys, random
from fractions import Fraction as Fr

b = Fr(173, 200); e = 1 - b
def cdiv(a, d): return -((-a) // d)

def hyp_L26(r, x, y, z, T):
    S = x + y + z
    return (T >= S and T >= r - x + z and T >= r - y + z and 2*T >= 2*r - 2*x + y
            and 2*T >= 2*r - 2*y + x and 3*T >= r + 2*x + 2*y + z)
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
def hyp_S1(r, x, y, z, T, x1, y1, z1):
    return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1 + y1 + z1 <= T
            and y1 + z1 >= r + x - T and x1 + z1 >= r + y - T and x1 + y1 >= r + z - T)

def ceilfr(q): return -((-q.numerator) // q.denominator)

def check(r, m, y, z, T):
    M, Y, Z = Fr(m, r), Fr(y, r), Fr(z, r)
    if M <= Fr(119, 400):
        B = max(cdiv(3*r + m, 4), cdiv(2*r + 2*m, 3))
        return 'a', (2*m <= r and B <= T)
    if Y <= Fr(73, 200):
        S = M + Y + Z
        if Y - Z > M - e: return 'b2', hyp_L32(r, m, y, z, T)
        if S < Fr(81, 200): return 'b3', hyp_L32(r, z, y, m, T)
        return 'b1', hyp_L31(r, z, y, m, T)
    u = M + Y; d = M - Y
    if Z <= Fr(319, 200) - 2*u: return 'c1', hyp_L26(r, m, y, z, T)
    if Z < e - d: return 'c2', hyp_S2(r, y, m, z, T)
    if Z <= (Fr(146, 200) - Y) / 2: return 'c3', hyp_S2(r, m, y, z, T)
    if 3*Z >= e + u:
        m1 = (e + Y + Z - M) / 2; y1 = (e + M + Z - Y) / 2; z1 = (e + M + Y - Z) / 2; tag = 'c4A'
    else:
        z1 = Z; y1 = e + M - Z; m1 = e + Y - Z; tag = 'c4B'
    hm, hy, hz = ceilfr(m1 * r), ceilfr(y1 * r), ceilfr(z1 * r)
    return tag, hyp_S1(r, m, y, z, T, hm, hy, hz)

def run_r(r, stride=1):
    T = cdiv(173*r + 600, 200)
    assert T <= r
    mmax = (23*r) // 50; lim = (227*r) // 200
    fails = []; cnt = {}
    for m in range(0, mmax + 1, stride):
        for y in range(0, min(m, (lim - m) // 2) + 1):
            for z in range(0, y + 1):
                tag, ok = check(r, m, y, z, T)
                cnt[tag] = cnt.get(tag, 0) + 1
                if not ok: fails.append((r, m, y, z, T, tag))
    return cnt, fails

if __name__ == '__main__':
    tot = 0
    for r in [int(a) for a in sys.argv[1:]] or [100, 137, 200, 231, 333, 400, 401, 577]:
        cnt, fails = run_r(r)
        tot += len(fails)
        print(r, sum(cnt.values()), cnt, 'FAIL', len(fails), fails[:5])
    # random large r, boundary-biased
    rng = random.Random(5); rf = 0; n = 0
    for _ in range(300000):
        r = rng.randint(1000, 10**6)
        T = cdiv(173*r + 600, 200)
        mmax = (23*r)//50; lim = (227*r)//200
        m = rng.choice([rng.randint(0, mmax), mmax, mmax - rng.randint(0, 3), (119*r)//400 + rng.randint(-2, 2),
                        (81*r)//200 + rng.randint(-2, 2)])
        m = max(0, min(mmax, m))
        ymax = min(m, (lim - m)//2)
        if ymax < 0: continue
        y = rng.choice([rng.randint(0, ymax), ymax, max(0, ymax - rng.randint(0, 3)), min(ymax, (73*r)//200 + rng.randint(-2, 2))])
        y = max(0, min(ymax, y))
        z = rng.choice([rng.randint(0, y), y, 0, max(0, y - rng.randint(0, 3))])
        tag, ok = check(r, m, y, z, T); n += 1
        if not ok: rf += 1; print('RANDFAIL', r, m, y, z, tag)
    print('random', n, 'fails', rf)
    print('TOTAL exhaustive fails', tot)
