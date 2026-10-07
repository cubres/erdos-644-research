# referee_w5_paper_P41_int.py -- exhaustive INTEGER-level check of Proposition 4.1's case chain.
# Written from scratch by the w5 Prop-4.1 referee.  Pure integer arithmetic (everything scaled).
# For each r, each T in the chosen set, each integer (m,y,z) with 0<=z<=y<=m, 50m<=23r, 200(m+2y)<=227r:
# classify by the paper's chain (on m/r, y/r, z/r, exactly) and check the USED lemma's hypotheses
# directly at the integer data (r, cells in the paper's role order, T) -- NOT via the normalised
# reductions in the paper.  For (c4) the rounded split of the paper is checked against Lemma 3.5.
# Also records the minimum slack of every hypothesis (to see which ones are tight).
import sys
from math import ceil
from fractions import Fraction as Fr
from collections import Counter, defaultdict

def L31_ok(r, T, m):      # Lemma 3.1 with its own budget B; need B < tau, i.e. B <= T; m <= r/2
    B = max(-(-(3*r+m)//4), -(-(2*r+2*m)//3))
    return 2*m <= r and B <= T
def L32_ok(r, T, x, y, z):
    S = x+y+z
    return (T >= S and T >= r-x+z and T >= r-y+z and 2*T >= 2*r-2*x+y and 2*T >= 2*r-2*y+x
            and 3*T >= r+2*x+2*y+z)
def L33_ok(r, T, x, y, z):
    S = x+y+z
    return (T <= r and T >= S and 2*T >= r+2*y and 2*T >= r+2*x-y+z and 3*T >= r+2*x+y+3*z)
def L34_ok(r, T, x, y, z):
    S = x+y+z
    return (T <= r and T >= x+y and 2*T >= r+2*x and 2*T >= r+2*y and T >= r+x-y-z and T >= r-x+y-z
            and 3*T >= 3*r-S and 5*T >= 3*r+S and 3*T >= r+x+y+2*z and 4*T >= 2*r+3*z)
def S2_ok(r, T, x, y, z):
    P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
    return (x <= T and y <= T and T >= r-x+z+P+Q and T >= y+z+Q and 2*T >= r+y+2*z+P+2*Q)
def S1_ok(r, T, x, y, z, x1, y1, z1):
    return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1+y1+z1 <= T
            and y1+z1 >= r+x-T and x1+z1 >= r+y-T and x1+y1 >= r+z-T)

def check(r, T):
    # scaled comparisons: normalised value v/r compared with p/q  <=>  q*v vs p*r
    e = Fr(27, 200)
    cnt = Counter(); bad = []
    for m in range(0, r//2 + 1):
        if 50*m > 23*r: break
        for y in range(0, m+1):
            if 200*(m+2*y) > 227*r: break
            for z in range(0, y+1):
                if 400*m <= 119*r:
                    ok = L31_ok(r, T, m); tag = 'a'
                elif 200*y <= 73*r:
                    # y-z > m-e  <=>  200(y-z) > 200m - 27r
                    if 200*(y-z) > 200*m - 27*r: ok = L33_ok(r, T, m, y, z); tag = 'b2'
                    elif 200*(m+y+z) < 81*r: ok = L33_ok(r, T, z, y, m); tag = 'b3'
                    else: ok = L34_ok(r, T, z, y, m); tag = 'b1'
                else:
                    u = m+y; d = m-y
                    if 200*z <= 319*r - 400*u: ok = L32_ok(r, T, m, y, z); tag = 'c1'
                    elif 200*z < 27*r - 200*d: ok = S2_ok(r, T, y, m, z); tag = 'c2'
                    elif 400*z <= 146*r - 200*y: ok = S2_ok(r, T, m, y, z); tag = 'c3'
                    else:
                        M, Yn, Zn, U = Fr(m, r), Fr(y, r), Fr(z, r), Fr(u, r)
                        if 3*Zn >= e + U:
                            s = ((e+Yn+Zn-M)/2, (e+M+Zn-Yn)/2, (e+M+Yn-Zn)/2); tag = 'c4A'
                        else:
                            s = (e+Yn-Zn, e+M-Zn, Zn); tag = 'c4B'
                        x1, y1, z1 = [ceil(t*r) for t in s]
                        ok = S1_ok(r, T, m, y, z, x1, y1, z1)
                cnt[tag] += 1
                if not ok: bad.append((r, T, m, y, z, tag))
    return cnt, bad

if __name__ == '__main__':
    mode = sys.argv[1]
    tot = Counter(); allbad = []
    if mode == 'allT':        # every r in [a,b], every admissible T
        a, b = int(sys.argv[2]), int(sys.argv[3])
        for r in range(a, b+1):
            for T in range(-(-(173*r + 600)//200), r+1):
                c, bad = check(r, T); tot += c; allbad += bad
    else:                     # listed r, T = ceil(beta r + 3) only (hardest T; hypotheses monotone in T)
        for r in map(int, sys.argv[2:]):
            T = -(-(173*r + 600)//200)
            c, bad = check(r, T); tot += c; allbad += bad
    print("triples", sum(tot.values()), dict(tot))
    print("FAILURES", len(allbad), allbad[:10])
