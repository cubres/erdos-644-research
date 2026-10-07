"""INDEPENDENT std-lib checker for ktype_cert.py output (Fractions only): rebuilds hypotheses (k rigid types,
tau>3/4, tau*>=tau via all 3^k blocking maps) and the template-failure disjunctions (T colourings via Fano
incidence + Lemma 7.63 incl. row<=x, V via max(s+t,5s/4+t/2)); checks steps, tree completeness, certificates."""
import sys, json, itertools
from fractions import Fraction as F
D = json.load(open(sys.argv[1])); K = D['K']; P = 'ABC'
def tv(k, i): return f't{k}{P[i]}'
def xv(i): return 'x' + P[i]
def R(d, rhs, strict=False): return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))
def viol(d): return R({k: -F(v) for k, v in d.items()}, 0, True)     # d.z > 0
BASE = {R({'tau': -1}, F(-3, 4), True)} | {R({xv(i): -1}, 0) for i in range(3)}
for k in range(K):
    for i in range(3): BASE |= {R({tv(k, i): -1}, 0), R({tv(k, i): 1, xv(i): -1}, 0)}
    BASE |= {R({tv(k, i): 1 for i in range(3)}, 1), R({tv(k, i): -1 for i in range(3)}, -1)}
DIS = {}
for pi in itertools.product(range(3), repeat=K):
    used = sorted(set(pi)); alts = []
    for sel in itertools.product(*[[r for r in range(K) if pi[r] == i] for i in used]):
        d = {'tau': F(1)}
        for i, r in zip(used, sel): d[xv(i)] = d.get(xv(i), 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append(frozenset([R(d, 0)]))
    for r in range(K): alts.append(frozenset([R({tv(r, pi[r]): 1}, 0)]))
    DIS[f'map {pi}'] = alts
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
for a, b, c in itertools.product(range(K), repeat=3):
    q0 = 0   # use a DIFFERENT pencil point than the generator (point 6): colourings are Fano-isomorphic
    pen = [l for l in LINES if q0 in l]; typ = {l: a for l in LINES if q0 not in l}
    typ[pen[0]] = b; typ[pen[1]] = b; typ[pen[2]] = c
    alts = set()
    for i in range(3):
        for q in range(7):
            d = {}
            for l in LINES:
                if q in l: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) + 1
            d[xv(i)] = F(-2); alts.add(frozenset([viol(d)]))
        d = {}
        for l in LINES: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) + 1
        d[xv(i)] = F(-4); alts.add(frozenset([viol(d)]))
        for l in LINES: alts.add(frozenset([viol({tv(typ[l], i): 1, xv(i): -1})]))
    DIS[f'T {a}{b}{c}'] = alts
for s_, t_ in itertools.permutations(range(K), 2):
    alts = set()
    for i in range(3):
        alts.add(frozenset([viol({tv(s_, i): 1, tv(t_, i): 1, xv(i): -1})]))
        alts.add(frozenset([viol({tv(s_, i): F(5, 4), tv(t_, i): F(1, 2), xv(i): -1})]))
    DIS[f'V {s_}{t_}'] = alts
def J(r): return R({k: F(v) for k, v in r[0].items()}, F(r[1]), r[2])
def trivial(alt):
    for (a, b, st) in alt:
        neg = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == neg and (b + b2 < 0 or (b + b2 == 0 and (st or st2))): return True
    return False
err = 0; tree = {}
for li, (path, cert) in enumerate(D['leaves']):
    rows = set(BASE); pre = ()
    for nm, ai, alt in path:
        A = frozenset(J(r) for r in alt)
        if A not in set(DIS[nm]): print("bad step", li, nm); err += 1
        tree.setdefault(pre, {}).setdefault(nm, set()).add(A); rows |= A; pre = pre + ((nm, A),)
    tot = {}; val = F(0); sw = F(0)
    for r in cert:
        row = J(r[:3]); l = F(r[3])
        if row not in rows or l < 0: print("bad cert row", li); err += 1
        for k, v in row[0]: tot[k] = tot.get(k, 0) + l * v
        val += l * row[1]; sw += l if row[2] else 0
    if any(v != 0 for v in tot.values()) or not (val < 0 or (val == 0 and sw > 0)): print("bad cert", li); err += 1
for pre, d in tree.items():
    if len(d) != 1: print("two disjunctions at node"); err += 1; continue
    nm, kids = next(iter(d.items()))
    for alt in DIS[nm]:
        if alt not in kids and not trivial(alt): print("missing alt", nm, sorted(alt)); err += 1
print("K", K, "leaves", len(D['leaves']), "nodes", len(tree), "ERRORS", err)
