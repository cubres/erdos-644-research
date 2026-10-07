"""EXACT certificate: every type-closed family of k RIGID types over 3 parts with tau*>3/4 has a bad tuple
T(a;b,b;c) (Fano colouring: quad a, two pencil lines b, one pencil line c; a,b,c any of the k types, equal
allowed) or V(s,t).  No other hypothesis (no class structure, no balance).  DFS over disjunctions
(blocking maps / template failures); leaves = exact rational Motzkin certificates.  usage: ktype_cert.py k"""
import sys, itertools, json, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
K = int(sys.argv[1]); P = 'ABC'
V = ['xA', 'xB', 'xC', 'tau'] + [f't{k}{P[i]}' for k in range(K) for i in range(3)]
IX = {v: i for i, v in enumerate(V)}
def tv(k, i): return f't{k}{P[i]}'
def xv(i): return 'x' + P[i]
def row(d, rhs, strict=False): return ({k: F(v) for k, v in d.items() if F(v) != 0}, F(rhs), strict)
BASE = [row({'tau': -1}, F(-3, 4), True)]
for i in range(3): BASE.append(row({xv(i): -1}, 0))
for k in range(K):
    for i in range(3): BASE += [row({tv(k, i): -1}, 0), row({tv(k, i): 1, xv(i): -1}, 0)]
    s = {tv(k, i): 1 for i in range(3)}
    BASE += [row(s, 1), row({a: -1 for a in s}, -1)]
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PEN = [l for l in LINES if 6 in l]
DISJ = []
for pi in itertools.product(range(3), repeat=K):
    used = sorted(set(pi)); alts = []
    for sel in itertools.product(*[[r for r in range(K) if pi[r] == i] for i in used]):
        d = {'tau': 1}
        for i, r in zip(used, sel): d[xv(i)] = d.get(xv(i), 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append([row(d, 0)])
    for r in range(K): alts.append([row({tv(r, pi[r]): 1}, 0)])
    DISJ.append((f'map {pi}', alts))
for a, b, c in itertools.product(range(K), repeat=3):
    typ = {l: (a if 6 not in l else None) for l in LINES}
    typ[PEN[0]] = b; typ[PEN[1]] = b; typ[PEN[2]] = c
    alts = set()
    for i in range(3):
        for q in range(7):
            d = {xv(i): F(2)}
            for l in LINES:
                if q in l: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) - 1
            alts.add(tuple(sorted(d.items())))
        d = {xv(i): F(4)}
        for l in LINES: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) - 1
        alts.add(tuple(sorted(d.items())))
    DISJ.append((f'T {a}{b}{c}', [[row(dict(d), 0, True)] for d in sorted(alts)]))
for s_, t_ in itertools.permutations(range(K), 2):
    alts = []
    for i in range(3):
        alts.append([row({xv(i): 1, tv(s_, i): -1, tv(t_, i): -1}, 0, True)])
        alts.append([row({xv(i): 1, tv(s_, i): F(-5, 4), tv(t_, i): F(-1, 2)}, 0, True)])
    DISJ.append((f'V {s_}{t_}', alts))
exec(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert/exactlib.py').read())
STATS = {'leaves': 0, 'certfail': 0, 'cex': 0}; LEAVES = []
DD = {nm: alts for nm, alts in DISJ}
def dfs(rows, path):
    t, z, du = lp(rows)
    if t <= 1e-9:
        c = exact_cert(rows); STATS['leaves'] += 1
        if c is None: STATS['certfail'] += 1; print("CERT FAIL", path, flush=True)
        else: LEAVES.append((path, c))
        return
    best = None
    for name, alts in DISJ:
        if any(all(eval_row(r, z) for r in alt) for alt in alts): continue
        feas = [ai for ai, alt in enumerate(alts) if lp(rows + alt)[0] > 1e-9]
        if best is None or len(feas) < len(best[2]): best = (name, alts, feas)
        if len(feas) <= 1: break
    if best is None:
        STATS['cex'] += 1; print("COUNTEREXAMPLE", path, {v: round(z[IX[v]], 5) for v in V}, flush=True); return
    name, alts, feas = best
    for ai, alt in enumerate(alts):
        if ai in feas: dfs(rows + alt, path + [(name, ai)])
        else:
            c = exact_cert(rows + alt); STATS['leaves'] += 1
            if c is None: STATS['certfail'] += 1; print("CERT FAIL (pruned)", flush=True)
            else: LEAVES.append((path + [(name, ai)], c))
t0 = time.time(); dfs(list(BASE), [])
print("K", K, "STATS", STATS, "time %.1f" % (time.time() - t0), flush=True)
def rows_of(p):
    Rr = list(BASE)
    for nm, ai in p: Rr = Rr + DD[nm][ai]
    return Rr
def js(r): return [{k: str(v) for k, v in r[0].items()}, str(r[1]), r[2]]
json.dump({'K': K, 'stats': STATS, 'leaves': [[[(nm, ai, [js(r) for r in DD[nm][ai]]) for nm, ai in p],
           [js(rows_of(p)[k]) + [str(l)] for k, l in c]] for p, c in LEAVES]},
          open(f'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert/ktype_leaves_{K}.json', 'w'))
