# Referee (w4 handbound): independent INTEGER check of Proposition 10.
# For integer r, T = ceil(173r/200)+3 (the smallest T allowed), and every integer triple
# z<=y<=m<=23r/50, m+2y<=227r/200, apply the proof's case rule (thresholds scaled by r, exact)
# and verify the INTEGER hypotheses of the invoked lemma exactly as the lemmas state them
# (Lemma 1 with its ceiling; Lemma 5 with the continuous splits rounded UP to integers).
# Written independently of w4_handbound_*.py.
import sys
from fractions import Fraction as Fr
from math import ceil, floor

def run(r, full=True, stride=1):
    B = Fr(173, 200)
    T = ceil(B * r) + 3
    assert T <= r
    R = Fr(r)
    c27, c73, c81, c119_400 = Fr(27, 200) * R, Fr(73, 200) * R, Fr(81, 200) * R, Fr(119, 400) * R
    c146, c319 = Fr(146, 200) * R, Fr(319, 200) * R
    def L1(m):  # Lemma 1: needs ceil(max(...)) <= T (then < tau), m <= r/2
        return 2 * m <= r and ceil(max(Fr(3 * r + m, 4), Fr(2 * r + 2 * m, 3))) <= T
    def L2(x, y, z):
        S = x + y + z
        return T <= r and all(v <= T for v in [S, r - x + z, r - y + z, Fr(2 * r - 2 * x + y, 2),
                                                Fr(2 * r - 2 * y + x, 2), Fr(r + 2 * x + 2 * y + z, 3)])
    def L3(x, y, z):
        S = x + y + z
        return T <= r and all(v <= T for v in [S, Fr(r + 2 * y, 2), Fr(r + 2 * x - y + z, 2),
                                                Fr(r + 2 * x + y + 3 * z, 3)])
    def L4(x, y, z):
        S = x + y + z
        return T <= r and all(v <= T for v in [x + y, Fr(r + 2 * x, 2), Fr(r + 2 * y, 2), r + x - y - z,
                                                r - x + y - z, r - Fr(S, 3), Fr(3 * r + S, 5),
                                                Fr(r + x + y + 2 * z, 3), Fr(2 * r + 3 * z, 4)])
    def L6(x, y, z):
        P = max(0, r + y - x - z - T); Q = max(0, r + x - y - z - T)
        return (x <= T and y <= T and T <= r and T >= r - x + z + P + Q and T >= y + z + Q
                and 2 * T >= r + y + 2 * z + P + 2 * Q)
    def L5(cells, splits):
        # cells (x,y,z); integer splits; conditions of Lemma 5
        x, y, z = cells; x1, y1, z1 = splits
        return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1 + y1 + z1 <= T
                and y1 + z1 >= r + x - T and x1 + z1 >= r + y - T and x1 + y1 >= r + z - T)
    cnt = {}; bad = []
    mmax = floor(Fr(23, 50) * R)
    for m in range(0, mmax + 1, 1 if full else stride):
        ymax = min(m, floor((Fr(227, 200) * R - m) / 2))
        if m <= c119_400:
            ok = L1(m); cnt['a'] = cnt.get('a', 0) + 1
            if not ok: bad.append(('a', m))
            continue
        for y in range(0, ymax + 1):
            for z in range(0, y + 1):
                S = m + y + z
                if False:
                    c, ok = 'a', L1(m)
                elif y <= c73:
                    if y - z > m - c27:
                        c, ok = 'b2', L3(m, y, z)
                    elif S < c81:
                        c, ok = 'b3', L3(z, y, m)
                    else:
                        c, ok = 'b1', L4(z, y, m)
                else:
                    u = m + y; d = m - y
                    if z <= c319 - 2 * u:
                        c, ok = 'c1', L2(m, y, z)
                    elif z < c27 - d:
                        c, ok = 'c2', L6(y, m, z)
                    elif z <= (c146 - y) / 2:
                        c, ok = 'c3', L6(m, y, z)
                    else:
                        if 3 * z >= c27 + u:
                            m1 = (c27 + y + z - m) / 2; y1 = (c27 + m + z - y) / 2; z1 = (c27 + m + y - z) / 2
                        else:
                            z1 = Fr(z); y1 = c27 + m - z; m1 = c27 + y - z
                        c, ok = 'c4', L5((m, y, z), (ceil(m1), ceil(y1), ceil(z1)))
                cnt[c] = cnt.get(c, 0) + 1
                if not ok:
                    bad.append((c, m, y, z))
    return T, cnt, bad

if __name__ == '__main__':
    for r in [int(a) for a in sys.argv[1:]]:
        T, cnt, bad = run(r)
        print('r', r, 'T', T, cnt, 'FAIL', len(bad), bad[:8])
