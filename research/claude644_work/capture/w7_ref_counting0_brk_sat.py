#!/usr/bin/env python3
"""w7_ref_counting0_brk_sat.py -- referee w7 BREAK-IT, claim counting#0, complete family K_n^(k) via SAT (pysat).
Vars x[v][i] = (v in row i), every row exactly k vertices (edges of K_n^k; repetitions allowed).
Phase 1: minimise |P7| then |Pi7| (incremental cardinality bounds).  Phase 2: is there a lex-minimiser in which
every vertex of some W_i has degree >= 4 (hypothesis of (d))?  Every model is re-verified in pure python.
Usage: n k"""
import sys, itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
FULL = 127
n, k = int(sys.argv[1]), int(sys.argv[2])
pool = IDPool()
X = lambda v, i: pool.id(('x', v, i))
cls = []
for i in range(7):
    cls += CardEnc.equals([X(v, i) for v in range(n)], bound=k, vpool=pool, encoding=EncType.seqcounter).clauses
prs = list(itertools.combinations(range(n), 2))
C = lambda u, v, i: pool.id(('c', u, v, i))
Y = lambda u, v: pool.id(('y', u, v))
Yi = lambda u, v, i: pool.id(('yi', u, v, i))
A = lambda u, v, i: pool.id(('a', u, v, i))
for (u, v) in prs:
    for i in range(7):
        c = C(u, v, i); cls += [[-c, X(u, i), X(v, i)], [c, -X(u, i)], [c, -X(v, i)]]
    y = Y(u, v); cls += [[-y, C(u, v, i)] for i in range(7)] + [[y] + [-C(u, v, i) for i in range(7)]]
    for i in range(7):
        yi = Yi(u, v, i); oth = [j for j in range(7) if j != i]
        cls += [[-yi, C(u, v, j)] for j in oth] + [[yi] + [-C(u, v, j) for j in oth]]
        a = A(u, v, i); cls += [[-a, yi], [-a, -Y(u, v)], [a, -yi, Y(u, v)]]
Pv = lambda v: pool.id(('p', v))
Wv = lambda v, i: pool.id(('w', v, i))
for v in range(n):
    ys = [Y(min(u, v), max(u, v)) for u in range(n) if u != v]
    cls += [[-Pv(v)] + ys] + [[Pv(v), -y] for y in ys]
    for i in range(7):
        As = [A(min(u, v), max(u, v), i) for u in range(n) if u != v]
        cls += [[-Wv(v, i)] + As] + [[Wv(v, i), -a] for a in As]
# symmetry breaking: vertex 0 in P (P nonempty); nothing else (keep it simple and sound)
S = Solver(name='cadical153', bootstrap_with=cls)
def model_sig(m):
    ms = set(l for l in m if l > 0)
    return [sum(1 << i for i in range(7) if X(v, i) in ms) for v in range(n)]
def verify(sg):
    pairs = [(x, y) for x, y in prs if sg[x] | sg[y] == FULL]; Ps = set(pairs)
    P = set(z for pr in pairs for z in pr)
    W = []
    for i in range(7):
        m = FULL & ~(1 << i)
        W.append(set(z for (x, y) in prs if (sg[x] | sg[y]) & m == m and (x, y) not in Ps for z in (x, y)))
    d = [bin(s).count('1') for s in sg]; q = [sum(v in W[i] for i in range(7)) for v in range(n)]
    hyp = all(d[v] >= 4 for v in range(n) if q[v] > 0)
    return len(P), len(pairs), d, q, [len(w) for w in W], hyp
def with_bound(lits, B, extra=[]):
    enc = CardEnc.atmost(lits, bound=B, vpool=pool, encoding=EncType.seqcounter)
    s2 = Solver(name='cadical153', bootstrap_with=cls + enc.clauses + extra)
    ok = s2.solve(); m = s2.get_model() if ok else None; s2.delete(); return ok, m
Plits = [Pv(v) for v in range(n)]; Ylits = [Y(u, v) for (u, v) in prs]
assert S.solve(); sg = model_sig(S.get_model()); cur = verify(sg); print('initial', cur[:2], flush=True)
# minimise |P|
B = cur[0]
while True:
    ok, m = with_bound(Plits, B - 1)
    if not ok: break
    sg = model_sig(m); cur = verify(sg); B = cur[0]; print(' |P| ->', cur[:2], flush=True)
minP = B
eqP = CardEnc.equals(Plits, bound=minP, vpool=pool, encoding=EncType.seqcounter).clauses
B2 = cur[1] if cur[0] == minP else len(prs)
while True:
    ok, m = with_bound(Ylits, B2 - 1, eqP)
    if not ok: break
    sg = model_sig(m); cur = verify(sg); B2 = cur[1]; print(' |Pi| ->', cur[:2], flush=True)
minPi = B2
print(f'K_{n}^{k}: tau={n-k+1} lexmin=({minP},{minPi})  bound(d)={3*k/4+2}', flush=True)
# phase 2: hypothesis of (d) among minimisers
eqY = CardEnc.equals(Ylits, bound=minPi, vpool=pool, encoding=EncType.seqcounter).clauses
hypcl = []
for v in range(n):
    for T in itertools.combinations(range(7), 4):
        for j in range(7):
            hypcl.append([-Wv(v, j)] + [X(v, i) for i in T])
s3 = Solver(name='cadical153', bootstrap_with=cls + eqP + eqY + hypcl)
ok = s3.solve()
if ok:
    sg = model_sig(s3.get_model()); r = verify(sg)
    assert r[0] == minP and r[1] == minPi and r[5]
    print('  phase2: a lex-minimiser SATISFYING hyp(d) exists:', [format(s, '07b') for s in sg], 'd', r[2], 'q', r[3], '|W|', r[4])
else:
    print('  phase2: NO lex-minimiser satisfies hyp(d) (UNSAT)')
# also: sample a minimiser for description
s4 = Solver(name='cadical153', bootstrap_with=cls + eqP + eqY); s4.solve(); sg = model_sig(s4.get_model()); r = verify(sg)
print('  sample minimiser:', [format(s, '07b') for s in sg], 'd', r[2], 'q', r[3], '|W|', r[4], 'hyp', r[5])
