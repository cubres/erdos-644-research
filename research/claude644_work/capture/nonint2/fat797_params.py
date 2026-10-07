"""Exact integer check of the sufficient conditions (0),(1),(2) of the fattened-7.97 lemma; list best s."""
import sys
from fractions import Fraction as F
def ok(k, s, c, d):
    if not (0 <= 2*c - (k+s) <= 0 or 2*c <= k+s): return False
    if 2*c > k+s or c > k or c < d+1 or s+1 < 2*d+2: return False
    if not 4*s < 3*k: return False
    for a in range(1, 7):
        x = c - a*d
        if not ((x > s and (5-a)*s < 2*k + x) or ((6-a)*s < k + 2*x)): return False
    for a in range(1, 7):
        for b in range(1, 7-a):
            j = 7-a-b
            if not ((c-a*d) >= 1 and (c-b*d) >= 1 and 4*(c-a*d)*(c-b*d) > j*s*s): return False
    # need X,Y nonempty when all rows cluster: a*d < k+d
    return True
def best(k, d):
    bs = None
    for s in range(k):
        for c in range(k+1):
            if ok(k, s, c, d):
                if bs is None or s > bs[0]: bs = (s, c)
    return bs
if __name__ == '__main__':
    for k in [14, 21, 28, 35, 42, 56, 70, 140, 700]:
        row = []
        for d in range(0, max(1, k//12)+1):
            b = best(k, d)
            if b: row.append((d, b[0]+1, round((b[0]+1)/k, 3), b[1]))
        print(k, row[:12])
