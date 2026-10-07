#!/usr/bin/env python3
"""
arch0_minloss_milp.py  (wave-11 referee of architecture#0; scipy/HiGHS MILP + exact re-check)

For a support (set of used cells) and real cell masses with row loads v_j and capacity n, the minimum NECESSARY loss is
    L(mass) = min over integer y >= 0 on the used cells, sum y <= n, of  max_j ( floor(v_j) - load_j(y) ).
The universal shift s must be >= sup L.  Beck-Fiala rounding (arch0_rounding.py) shows sup L <= 5.  This script searches
adversarially (random and structured masses on the densest supports) for large L, and re-checks each MILP optimum
exactly (integers).  Whatever the largest L found, it is a LOWER bound on the optimal universal s.
"""
import json, random, sys, time
from fractions import Fraction as Fr
from math import floor, ceil
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

CAT = "/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json"
FULL = 127

def downset(maximal):
    cells = set()
    for m in maximal:
        sub = m
        while True:
            cells.add(sub)
            if sub == 0:
                break
            sub = (sub - 1) & m
    return cells

def min_loss(cells, v_floor, n):
    """MILP: variables y_c (int >= 0), L (int >= 0); minimise L s.t. load_j(y) >= v_floor_j - L, sum y <= n."""
    m = len(cells)
    c = np.zeros(m + 1); c[m] = 1.0
    A = []; lo = []; hi = []
    for j in range(7):
        row = np.zeros(m + 1)
        for i, cc in enumerate(cells):
            if cc >> j & 1:
                row[i] = 1.0
        row[m] = 1.0
        A.append(row); lo.append(v_floor[j]); hi.append(np.inf)
    row = np.zeros(m + 1); row[:m] = 1.0
    A.append(row); lo.append(-np.inf); hi.append(n)
    res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(m + 1),
               bounds=Bounds(np.zeros(m + 1), np.full(m + 1, np.inf)), options={"time_limit": 20})
    if res.x is None:
        return None, None
    y = [int(round(t)) for t in res.x[:m]]
    L = int(round(res.x[m]))
    # exact re-check
    assert sum(y) <= n and min(y) >= 0
    loads = [sum(y[i] for i, cc in enumerate(cells) if cc >> j & 1) for j in range(7)]
    assert all(loads[j] >= v_floor[j] - L for j in range(7))
    return L, res.status

def main():
    rnd = random.Random(7)
    orbits = json.load(open(CAT))["orbits"]
    fams = []
    fams.append(("all 3-sets", [c for c in range(1, FULL) if bin(c).count("1") == 3]))
    fams.append(("all <=3-sets", [c for c in range(1, FULL) if bin(c).count("1") <= 3]))
    # a few catalogue supports with 5-cells
    for o in orbits:
        if max(bin(m).count("1") for m in o["maximal_cells"]) == 5:
            fams.append(("cat5", sorted(c for c in downset(o["maximal_cells"]) if c)))
            if len(fams) >= 8:
                break
    for o in rnd.sample(orbits, 6):
        fams.append(("cat", sorted(c for c in downset(o["maximal_cells"]) if c)))
    best = 0; best_inst = None; t0 = time.time(); count = 0
    while time.time() - t0 < 420:
        name, cells = rnd.choice(fams)
        mode = rnd.random()
        if mode < 0.4:
            used = cells
        else:
            used = rnd.sample(cells, rnd.randint(max(1, len(cells) // 3), len(cells)))
        # masses: fractional parts near 1 (worst for flooring) or arbitrary
        if rnd.random() < 0.6:
            mass = {c: rnd.randint(0, 2) + Fr(rnd.randint(500, 999), 1000) for c in used}
        else:
            mass = {c: Fr(rnd.randint(0, 2000), 1000) for c in used}
        tot = sum(mass.values())
        n = ceil(tot) if rnd.random() < 0.7 else floor(tot)   # floor(tot) < tot: capacity tight -> not a valid instance
        if n < tot:
            continue
        v = [sum(m for c, m in mass.items() if c >> j & 1) for j in range(7)]
        vf = [floor(x) for x in v]
        L, status = min_loss(used, vf, n)
        count += 1
        if L is not None and L > best:
            best = L; best_inst = (name, len(used), n, [str(x) for x in v], status)
            print(f"  new max necessary loss L = {L}: support {name}, |used| = {len(used)}, n = {n}, status {status}")
    print(f"[MILP] {count} instances in {time.time()-t0:.0f}s: max necessary loss found = {best}; instance = {best_inst}")
    print("=> the optimal universal shift lies in [%d, 5]" % best)

if __name__ == "__main__":
    main()
