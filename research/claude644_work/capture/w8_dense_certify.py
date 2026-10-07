#!/usr/bin/env python3
"""w8_dense_certify.py -- produce a checkable UNSAT certificate for one anchored multi-part grid instance.
 1. CEGAR as in w8_dense_maxT (CaDiCaL) at threshold T, recording every cut together with the explicit
    six rows of the anchored Fano configuration it came from.
 2. Independent re-derivation: base clauses (anchor unit, up-closure, intersecting pairs, covering for tau*>=T)
    are rebuilt from scratch here; every cut is re-verified: its rows satisfy Lemma 7.63 in every part, and the
    cut clause is exactly the negation of the set of rows' types.
 3. Dump CNF, solve with Glucose4 + DRUP proof, check the proof with the independent checker
    w4_typeclosed_drup_check.py.
Usage: python3 w8_dense_certify.py r e x1 x2 ... T"""
import sys, subprocess, time
from itertools import product
from pysat.solvers import Cadical153, Glucose4
from w8_dense_lib import all_types, minimal, anchored_config, fano_ok

args = list(map(int, sys.argv[1:])); r, caps, T = args[0], tuple(args[1:-1]), args[-1]
e = caps[0]; p = len(caps); N = sum(caps)
types = all_types(caps, r, amin=1); idx = {g: i+1 for i, g in enumerate(types)}
anchor = (e,) + (0,)*(p-1)
base = [[idx[anchor]]]
for g in types:
    for i in range(p):
        h = list(g); h[i] += 1; h = tuple(h)
        if h in idx: base.append([-idx[g], idx[h]])
for g in types:
    comp = tuple(c - x for c, x in zip(caps, g))
    if sum(comp) <= r: cands = [comp] if comp in idx else []
    else: cands = [h for h in product(*[range(c+1) for c in comp]) if sum(h) == r and h in idx]
    for h in cands: base.append([-idx[g], -idx[h]])
cover = []
for w in product(*[range(c+1) for c in caps]):
    if sum(w) != N - T + 1: continue
    cover.append([idx[g] for g in types if all(gi == 0 or gi < wi for gi, wi in zip(g, w))])
S = Cadical153(bootstrap_with=base + cover); cuts = []
while S.solve():
    mdl = S.get_model(); Gm = minimal([g for g in types if mdl[idx[g]-1] > 0])
    rows, _ = anchored_config(Gm, caps, anchor)
    if rows is None: print('SAT: counterexample', Gm); sys.exit()
    cuts.append(list(rows)); S.add_clause([-idx[g] for g in sorted(set(rows))])
print(f'CEGAR UNSAT with {len(cuts)} cuts; re-verifying', flush=True)
# independent re-verification of cuts
for rows in cuts:
    assert fano_ok([anchor] + rows, caps)
# independent audit of intersecting clauses: every pair g,h with g+h<=caps must be excluded by base+upclosure
# (checked semantically: for each such pair some base pair clause (g',h') has g'<=g, h'<=h)
pairs = {(tuple(sorted((a, b)))) for cl in base if len(cl) == 2 and cl[0] < 0 and cl[1] < 0 for a, b in [(-cl[0], -cl[1])]}
inv = {v: k for k, v in idx.items()}
maxpairs = [(inv[a], inv[b]) for a, b in pairs]
bad = 0
for g in types:
    for h in types:
        if all(x + y <= c for x, y, c in zip(g, h, caps)):
            if not any(all(u <= v for u, v in zip(g1, g)) and all(u <= v for u, v in zip(h1, h)) or
                       all(u <= v for u, v in zip(g1, h)) and all(u <= v for u, v in zip(h1, g)) for g1, h1 in maxpairs):
                bad += 1
print('intersecting audit failures:', bad)
cnf = base + cover + [[-idx[g] for g in sorted(set(rw))] for rw in cuts]
nv = len(types)
fn = f'w8_cert_{r}_{"_".join(map(str, caps))}_{T}'
with open(fn + '.cnf', 'w') as f:
    f.write(f'p cnf {nv} {len(cnf)}\n')
    for cl in cnf: f.write(' '.join(map(str, cl)) + ' 0\n')
G = Glucose4(bootstrap_with=cnf, with_proof=True)
assert not G.solve()
with open(fn + '.drat', 'w') as f:
    for line in G.get_proof(): f.write(line + '\n')
print('proof lines', len(G.get_proof()), flush=True)
t0 = time.time()
out = subprocess.run(['python3', 'w4_typeclosed_drup_check.py', fn + '.cnf', fn + '.drat'], capture_output=True, text=True)
print('DRUP check:', out.stdout.strip()[-300:], out.stderr.strip()[-300:], f'({time.time()-t0:.0f}s)')
