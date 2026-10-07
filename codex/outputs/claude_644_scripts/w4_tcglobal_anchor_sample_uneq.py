#!/usr/bin/env python3
"""w4_tcglobal_anchor_sample.py -- EXPLORATORY (exact integer tests via note Lemma 7.63): sample intersecting
type-closed families with 2 or 3 types of sizes in [3r/5, r] (rank k = max size) over p parts with tau*/r > 3/4 (so NOT (7,2) by the
conjecture), and test for each type whether some Fano-downset tuple uses it as a row (= a K4/TC configuration
anchored at an edge of that type).  Reports families where some type is never a row ('anchor-free types').
Usage: seed samples ntypes nparts r"""
import random, sys, itertools
from fractions import Fraction
from w4_tcglobal_fano_exact import part_ok, tau_star, intersecting
seed, S, nt, npart, r = (int(x) for x in sys.argv[1:6]); random.seed(seed)
def rand_comp(r, caps):
    while True:
        cut = sorted(random.randint(0, r) for _ in range(npart-1))
        v = [b-a for a,b in zip([0]+cut, cut+[r])]
        if all(v[i] <= caps[i] for i in range(npart)): return v
def rows_used(types, caps):
    used = set()
    for assign in itertools.product(range(len(types)), repeat=7):
        if set(assign) <= used: continue
        if all(part_ok([types[assign[j]][i] for j in range(7)], caps[i]) for i in range(npart)):
            used |= set(assign)
            if len(used) == len(types): break
    return used
hi = 0; free = 0; nofano = 0
for _ in range(S):
    caps = [random.randint(r//4, 2*r) for _ in range(npart)]
    if sum(caps) < r: continue
    types = [rand_comp(random.randint(r*3//5, r), caps) for _ in range(nt)]
    if not intersecting(types, caps): continue
    ts = tau_star(types, caps)
    rk = max(sum(t) for t in types)
    if 4*ts <= 3*rk: continue
    hi += 1
    u = rows_used(types, caps)
    if not u: nofano += 1; print("NO Fano-downset tuple at all:", caps, types, "tau*/k", Fraction(ts, rk), flush=True)
    elif len(u) < nt:
        free += 1
        print("anchor-free type(s):", [types[i] for i in range(nt) if i not in u], "caps", caps, "types", types,
              "tau*/k", Fraction(ts, rk), flush=True)
print(f"intersecting samples with tau*/r>3/4: {hi}; with no Fano-downset tuple: {nofano}; with an anchor-free type: {free}")
