# w5_paper_constants.py -- exact integer check of every numerical inequality used in Sections 5-6 of
# paper_0865.tex (main theorem chain: Step 1, Lemma 5.1 (= note 7.27), Lemma 5.3 (= note 7.50)),
# for every r in [R0, R1].  Pure integer / Fraction arithmetic.  Worst cases are taken over the
# integer ranges of the free parameters as described in the comments (monotone expressions).
import sys
from fractions import Fraction as F
from math import ceil, floor

def cdiv(a, b): return -((-a) // b)          # ceil(a/b) for integers, b>0

R0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
R1 = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
fails = []
def chk(cond, tag, r):
    if not cond: fails.append((tag, r))

for r in range(R0, R1 + 1):
    cb = cdiv(173 * r, 200)                    # ceil(beta r)
    K = cb + 10
    h0 = (23 * r) // 50                         # floor(h r)
    lmin = cdiv(43 * r, 200)                    # smallest integer >= l r
    lmax = lmin - 1                             # largest integer < l r
    # ---------------- main theorem, Step 1 ----------------
    chk(K <= r, 'K<=r', r)
    chk(200 * (K) >= 173 * r + 600, 'K>=beta r+3', r)          # Prop hypothesis beta r + 3 <= T
    # y,z <= r - floor((K+m)/2) for m >= lmin; worst m = lmin
    ymax = r - (K + lmin) // 2
    chk(ymax < h0, 'step1 y<=h0-1', r)
    chk(200 * ymax <= 92 * r - 900, 'step1 y<=hr-4.5', r)
    # m + 2y <= 2r - K + 1 <= 227 r/200 - 9
    chk(200 * (2 * r - K + 1) <= 227 * r - 1800, 'step1 m+2y', r)
    # ---------------- Lemma 5.1 (gap extension to r/2) ----------------
    T = cb + 4
    xs = range(cdiv(23 * r, 50), r // 2 + 1)
    # balanced first request of size cb: y <= r - floor((cb + x)/2) < h r  (worst x = ceil(hr))
    x0 = cdiv(23 * r, 50)
    chk(50 * (r - (cb + x0) // 2) < 23 * r, 'L51 y<hr', r)
    # Case S <= T : core bound C <= T
    chk(r - h0 + lmax <= T, 'L51 r-h0+y', r)
    chk(2 * r - x0 - 2 * h0 <= T, 'L51 2r-x-2h0', r)
    chk(T <= r, 'L51 T<=r', r)
    # first two final requests: x + ceil(b/2) <= T with b <= r - T + x + p + t, worst y = z = 0
    for x in xs:
        p = max(0, r - x - h0)
        b = r - T + x + 2 * p
        chk(x + cdiv(b, 2) <= T, 'L51 case1 x+ceil(b/2)', r)
    chk(4 * lmax <= T, 'L51 third request', r)
    # Case S > T
    xm = r // 2
    chk(xm + lmax < T, 'L51 case2 x+y<T', r)
    chk(50 * (r - T + lmax) < 23 * r, 'L51 case2 traces <hr', r)
    # x + q + ceil(b/2), q <= x+y+z-T, b <= r-y-z; increasing in x and in s=y+z (coefficient 1/2)
    s = 2 * lmax
    chk(xm + (xm + s - T) + cdiv(r - s, 2) <= T, 'L51 case2 first two', r)
    chk(4 * lmax <= T, 'L51 case2 third', r)
    chk(2 * r + 2 * xm + 2 * lmax - T <= 3 * T, 'L51 case2 total', r)
    # ---------------- Lemma 5.3 (conditional finish), beta = 173/200 ----------------
    chk(T <= r, 'L53 T<=r', r)
    mmax = (119 * r) // 400
    B18 = max(cdiv(3 * r + mmax, 4), cdiv(2 * r + 2 * mmax, 3))
    chk(B18 <= cb, 'L18 budget at 119/400', r)
    mm = r - T                                   # m <= r - T
    chk(4 * mm <= r, 'L53 m<=r/4', r)
    # x <= r - (T+m)/2 + 1/2  =>  x + 2m <= (5r - 4T + 1)/2 < T  (worst m = r - T)
    chk(5 * r - 4 * T + 1 < 2 * T, 'L53 core<T', r)
    chk(cdiv(r, 2) + 2 * mm <= T, 'L41 cond1', r)
    chk(3 * r - 2 * T + 1 <= 2 * T, 'L41 cond2 (x+m <= 3r/2-T+1/2 <= T)', r)
    chk(9 * r + mm - 5 * T + 4 <= 6 * T, 'L41 cond3', r)
    chk(43 * 400 <= 119 * 200, 'l <= (3beta-2)/2', r)

print('checked r in', (R0, R1), 'failures:', len(fails), fails[:10])
print('ALL PASS' if not fails else 'FAILURE')
