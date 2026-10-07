"""INDEPENDENT std-lib checker for three_type_cert.py output (python3 -S safe; Fractions only).
Rebuilds the hypotheses and the template-failure disjunctions from first principles (Fano incidence +
note Lemma 7.63 for T colourings; V capacity function max(s+t, 5s/4+t/2); blocking maps), then checks
(1) every path step is an alternative of the named disjunction, (2) the branching tree is complete
(alternatives not branched on must contradict a base row directly), (3) every leaf certificate is an
exact Motzkin certificate over rows of that leaf."""
import sys, json, itertools
from fractions import Fraction as F
fn = sys.argv[1]; D = json.load(open(fn)); XMIN = F(D['xmin']); BAL = D['bal']
P = 'ABC'
def tv(r, i): return ('s' + P[i]) if r == i else ('abc'[r] + P[i])
def R(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))
def neg_strict(d):   # violation of  d.z <= 0  :  -d.z < 0
    return R({k: -F(v) for k, v in d.items()}, 0, True)
BASE = set()
for i in range(3):
    X = P[i]
    BASE |= {R({'x' + X: -1}, -XMIN), R({'x' + X: 1}, F(3, 2)), R({'x' + X: F(2, 3), 's' + X: -1}, 0),
             R({'s' + X: 1, 'x' + X: -1}, 0), R({'s' + X: 1}, 1)}
for r in range(3):
    s = {}
    for i in range(3):
        v = tv(r, i); s[v] = 1
        if r != i: BASE |= {R({v: -1}, 0), R({v: 1, 'x' + P[i]: -1}, 0)}
    BASE |= {R(s, 1), R({k: -1 for k in s}, -1)}
BASE.add(R({'tau': -1}, F(-3, 4), True))
if BAL:
    for i, j in itertools.combinations(range(3), 2):
        BASE.add(R({'x' + P[i]: 1, 's' + P[i]: -1, 'x' + P[j]: 1, 's' + P[j]: -1}, F(3, 4)))
DIS = {}
for r in range(3):
    for i in range(3):
        if r != i:
            v = tv(r, i)
            DIS[f'cls {v}'] = [frozenset([R({v: 1, 'x' + P[i]: F(-2, 3)}, 0)]), frozenset([R({v: -1, 's' + P[i]: 1}, 0)])]
for pi in itertools.product(range(3), repeat=3):
    used = sorted(set(pi)); alts = []
    for sel in itertools.product(*[[r for r in range(3) if pi[r] == i] for i in used]):
        d = {'tau': F(1)}
        for i, r in zip(used, sel):
            d['x' + P[i]] = d.get('x' + P[i], 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
        alts.append(frozenset([R(d, 0)]))
    for r in range(3):
        if pi[r] != r: alts.append(frozenset([R({tv(r, pi[r]): 1}, 0)]))
    DIS[f'map {pi}'] = alts
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
for X, Y, Z in itertools.permutations(range(3)):
    q0 = 6; pen = [l for l in LINES if q0 in l]; typ = {}
    for l in LINES:
        if q0 not in l: typ[l] = X
    typ[pen[0]] = Y; typ[pen[1]] = Y; typ[pen[2]] = Z
    alts = set()
    for i in range(3):
        xi = 'x' + P[i]
        for q in range(7):     # Lemma 7.63: sum over the 3 lines through q <= 2 x_i
            d = {xi: F(-2)}
            for l in LINES:
                if q in l: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) + 1
            alts.add(frozenset([neg_strict(d)]))
        d = {xi: F(-4)}
        for l in LINES: d[tv(typ[l], i)] = d.get(tv(typ[l], i), 0) + 1
        alts.add(frozenset([neg_strict(d)]))
        for l in LINES: alts.add(frozenset([neg_strict({tv(typ[l], i): 1, xi: -1})]))
    DIS[f'T {P[X]}{P[Y]}{P[Z]}'] = list(alts)
for S, T in itertools.permutations(range(3), 2):
    alts = []
    for i in range(3):
        s, t, xi = tv(S, i), tv(T, i), 'x' + P[i]
        alts.append(frozenset([neg_strict({s: 1, t: 1, xi: -1})]))
        alts.append(frozenset([neg_strict({s: F(5, 4), t: F(1, 2), xi: -1})]))
    DIS[f'V {P[S]}{P[T]}'] = alts
def rowfromjson(r): return R({k: F(v) for k, v in r[0].items()}, F(r[1]), r[2])
def trivially_inconsistent(alt):
    for (a, b, st) in alt:
        neg = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == neg and (b + b2 < 0 or (b + b2 == 0 and (st or st2))): return True
    return False
errors = 0; tree = {}
for li, (path, cert) in enumerate(D['leaves']):
    rows = set(BASE); prefix = ()
    for nm, ai, alt in path:
        altset = frozenset(rowfromjson(r) for r in alt)
        if altset not in set(DIS[nm]): print("step not an alternative", li, nm); errors += 1
        tree.setdefault(prefix, {}).setdefault(nm, set()).add(altset)
        rows |= altset; prefix = prefix + ((nm, altset),)
    lam = []
    for r in cert:
        row = rowfromjson(r[:3]); l = F(r[3])
        if row not in rows: print("cert row not in leaf", li); errors += 1
        if l < 0: print("negative multiplier", li); errors += 1
        lam.append((row, l))
    tot = {}
    for (a, b, st), l in lam:
        for k, v in a: tot[k] = tot.get(k, 0) + l * v
    if any(v != 0 for v in tot.values()): print("stationarity fails", li); errors += 1
    val = sum(l * b for (a, b, st), l in lam); sw = sum(l for (a, b, st), l in lam if st)
    if not (val < 0 or (val == 0 and sw > 0)): print("value fails", li); errors += 1
# completeness
for prefix, d in tree.items():
    if len(d) != 1: print("node branches on two disjunctions", prefix); errors += 1; continue
    nm, kids = next(iter(d.items()))
    for alt in DIS[nm]:
        if alt not in kids and not trivially_inconsistent(alt):
            print("missing alternative at node", len(prefix), nm, alt); errors += 1
if () not in tree: print("empty tree"); errors += 1
print("leaves", len(D['leaves']), "internal nodes", len(tree), "ERRORS", errors)
