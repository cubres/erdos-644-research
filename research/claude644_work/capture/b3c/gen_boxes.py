from fractions import Fraction as F
import itertools, sys
w = F(sys.argv[1]); m = int(F(3,2)/w)
out = []
for a, b, c in itertools.combinations_with_replacement(range(m), 3):
    lo = [a*w, b*w, c*w]; hi = [(a+1)*w, (b+1)*w, (c+1)*w]
    if sum(hi) < F(9,4): continue
    out.append((lo, hi))
for lo, hi in out: print(','.join(map(str, lo)), ','.join(map(str, hi)))
