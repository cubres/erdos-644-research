#!/usr/bin/env python3
"""w7_ref_counting2_noise.py -- referee w7 counting#2: test the significance example
'complete core plus private noise: D = 0'.  For core K_n^k0 with f private points per edge (and the bare core),
enumerate all six-multisets, find all lex(|P|,|Pi|) minimisers (common point => P=V), and print per-vertex
contributions c(v)=q+2[v in P]-d split into core / noise, and D."""
import itertools, sys
from collections import Counter
sys.path.insert(0,'.')
from w7_ref_counting2_brk import pairs, cov_masks, pc

def study(n, k0, f):
    core = list(itertools.combinations(range(n), k0)); H = []; nxt = n
    for S in core:
        E = sum(1 << v for v in S)
        for _ in range(f): E |= 1 << nxt; nxt += 1
        H.append(E)
    verts = list(range(nxt))
    best = None; mins = []
    for F in itertools.combinations_with_replacement(range(len(H)), 6):
        R = [H[j] for j in F]; Pi = pairs(R, verts)
        c = cov_masks(R, verts)
        if any(c[v] == 63 for v in verts): key = (len(verts), len(Pi))
        else: key = (len(set(x for pr in Pi for x in pr)), len(Pi))
        if best is None or key < best: best = key; mins = [(R, Pi)]
        elif key == best: mins.append((R, Pi))
    prof = Counter()
    for R, Pi in mins:
        Pis = set(Pi); P = set(x for pr in Pi for x in pr)
        W = []
        for i in range(6):
            W.append(set(x for pr in pairs(R[:i] + R[i+1:], verts) if pr not in Pis for x in pr))
        d = {v: sum((F >> v) & 1 for F in R) for v in verts}
        Dc = sum(sum(v in w for w in W) + 2 * (v in P) - d[v] for v in verts if v < n)
        Dn = sum(sum(v in w for w in W) + 2 * (v in P) - d[v] for v in verts if v >= n)
        U = 0
        for F in R: U |= F
        prof[(Dc, Dn, pc(U), len(set(R)), max(d.values()))] += 1
    print(f'K_{n}^{k0} noise f={f}: key {best} #min {len(mins)}  (Dcore,Dnoise,|U|,#distinct,maxdeg):count', dict(prof), flush=True)

for (n, k0) in [(5, 3), (6, 4), (7, 5), (6, 3)]:
    for f in (0, 1, 2):
        study(n, k0, f)
