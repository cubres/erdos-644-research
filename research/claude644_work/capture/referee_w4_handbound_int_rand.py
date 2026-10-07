# Referee: random large-r sampling (r up to 1e6, boundary-biased) of the integer Prop 10 check.
# Reuses the dispatch/lemma tests of referee_w4_handbound_int.py on chosen points.
import random, sys
from fractions import Fraction as Fr
from math import floor
random.seed(5)
src = open('referee_w4_handbound_int.py').read()
src = src.replace("    for m in range(0, mmax + 1, 1 if full else stride):", "    for m in PTS_M:")
src = src.replace("        for y in range(0, ymax + 1):\n            for z in range(0, y + 1):", "        for (y, z) in PTS_YZ[m]:\n            if True:")
src = src.replace("def run(r, full=True, stride=1):", "def run(r, PTS_M, PTS_YZ, full=True, stride=1):")
ns = {}; exec(src.split("if __name__")[0], ns)
tot = nb = 0
for it in range(3000):
    r = random.choice([random.randint(1000, 10**6), random.randint(1000, 5000)])
    mmax = floor(Fr(23, 50) * r); pts = {}
    for _ in range(50):
        m = random.choice([mmax, mmax - random.randint(0, 3), random.randint(floor(Fr(119, 400) * r) - 2, mmax)])
        ymax = min(m, floor((Fr(227, 200) * r - m) / 2))
        y = random.choice([ymax, ymax - random.randint(0, 3), random.randint(0, ymax), floor(Fr(73, 200) * r) + random.randint(-2, 2)])
        y = max(0, min(y, ymax))
        z = random.choice([random.randint(0, y), y, 0, max(0, y - random.randint(0, 3))])
        pts.setdefault(m, []).append((y, z))
    T, cnt, bad = ns['run'](r, sorted(pts), pts)
    tot += sum(cnt.values()); nb += len(bad)
    if bad: print(r, bad[:3]); break
print('points', tot, 'fails', nb)
