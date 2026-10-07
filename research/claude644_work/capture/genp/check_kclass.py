"""INDEPENDENT std-lib checker for genp/kclass_cert.py output (Fractions only; no numpy/scipy).
Rebuilds from first principles the hypotheses (BASE) and, from each step's NAME, the disjunction it refers to:
  'gap tR_i'  : cross trace t^R_i <= 2x_i/3  OR  t^R_i >= s_i               (class gap; only heavy parts i)
  'map (pi)'  : blocking map pi (type r blocked at part pi(r)): some selection (one blocked type per used part)
                has cost sum_i (x_i - t^{r_i}_i) >= tau, OR the map is invalid (some t^r_{pi(r)} <= 0)
  'F col'     : Fano colouring col (line l -> class col[l]) FAILS: in some part i some pencil sum > 2x_i or the
                total > 4x_i (strict).  [row <= x_i is implied by t <= x in BASE]
  'V ST'      : V(S,T) fails: in some part i, s_i + t_i > x_i or 5s_i/4 + t_i/2 > x_i (strict).
Checks: (1) every path step is an alternative of the named disjunction (alternatives rebuilt here, matched as
row-SETS, index-free); (2) tree completeness: at every internal node all alternatives of the branched disjunction
are present or contradict a BASE row directly; (3) every leaf certificate is an exact Motzkin certificate
(nonnegative multipliers over rows of that leaf, stationarity, value < 0 or (= 0 with a strict row)).
usage: python3 -S check_kclass.py cert.json"""
import sys, json, itertools
from fractions import Fraction as F
fn = sys.argv[1]; D = json.load(open(fn))
h = D['h']; L = D['L']; XMIN = F(D['xmin']); p = h + L
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PEN = [[l for l, ln in enumerate(LINES) if q in ln] for q in range(7)]
assert all(len(P) == 3 for P in PEN) and all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2))
def tv(r, i): return f's{i}' if r == i else f't{r}_{i}'
def R(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))
def negs(d):   # violation of  d.z <= 0  :  -d.z < 0
    return R({k: -F(v) for k, v in d.items()}, 0, True)
BASE = set()
for i in range(p):
    BASE.add(R({f'x{i}': -1}, -XMIN)); BASE.add(R({f'x{i}': 1}, F(3, 2) if i < h else 3))
for X in range(h):
    BASE.add(R({f'x{X}': F(2, 3), f's{X}': -1}, 0, True))
    BASE.add(R({f's{X}': 1, f'x{X}': -1}, 0)); BASE.add(R({f's{X}': 1}, 1))
for r in range(h):
    s = {}
    for i in range(p):
        v = tv(r, i); s[v] = s.get(v, 0) + 1
        if r != i:
            BASE.add(R({v: -1}, 0)); BASE.add(R({v: 1, f'x{i}': -1}, 0))
            if i >= h: BASE.add(R({v: 1, f'x{i}': F(-2, 3)}, 0))
    BASE.add(R(s, 1)); BASE.add(R({k: -v for k, v in s.items()}, -1))
BASE.add(R({'tau': -1}, F(-3, 4), True))
def disj(name):
    kind, arg = name.split(' ', 1)
    if kind == 'gap':
        v = arg; r, i = v[1:].split('_'); r, i = int(r), int(i)
        assert r != i and i < h and r < h
        return [frozenset([R({v: 1, f'x{i}': F(-2, 3)}, 0)]), frozenset([R({v: -1, f's{i}': 1}, 0)])]
    if kind == 'map':
        pi = tuple(int(c) for c in arg.strip('()').split(','))
        assert len(pi) == h and all(0 <= q < p for q in pi)
        used = sorted(set(pi)); alts = []
        for sel in itertools.product(*[[r for r in range(h) if pi[r] == i] for i in used]):
            d = {'tau': F(1)}
            for i, r in zip(used, sel):
                d[f'x{i}'] = d.get(f'x{i}', 0) - 1; d[tv(r, i)] = d.get(tv(r, i), 0) + 1
            alts.append(frozenset([R(d, 0)]))
        for r in range(h):
            if pi[r] != r: alts.append(frozenset([R({tv(r, pi[r]): 1}, 0)]))
        return alts
    if kind == 'F':
        col = [int(c) for c in arg]; assert len(col) == 7 and all(0 <= c < h for c in col)
        # arc condition (no monochromatic pencil) is what makes 2 rows/class realisable; not needed for validity
        alts = []
        for i in range(p):
            for q in range(7):
                d = {f'x{i}': F(-2)}
                for l in PEN[q]: d[tv(col[l], i)] = d.get(tv(col[l], i), 0) + 1
                alts.append(frozenset([negs(d)]))
            d = {f'x{i}': F(-4)}
            for l in range(7): d[tv(col[l], i)] = d.get(tv(col[l], i), 0) + 1
            alts.append(frozenset([negs(d)]))
        return alts
    if kind == 'V':
        S, T = int(arg[0]), int(arg[1]); assert S != T
        alts = []
        for i in range(p):
            s, t, xx = tv(S, i), tv(T, i), f'x{i}'
            alts.append(frozenset([negs({s: 1, t: 1, xx: -1})]))
            alts.append(frozenset([negs({s: F(5, 4), t: F(1, 2), xx: -1})]))
        return alts
    raise ValueError(name)
def rowfromjson(r): return R({k: F(v) for k, v in r[0].items()}, F(r[1]), r[2])
def trivially_inconsistent(alt):
    for (a, b, st) in alt:
        neg = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == neg and (b + b2 < 0 or (b + b2 == 0 and (st or st2))): return True
    return False
errors = 0; tree = {}; DCACHE = {}
def getd(nm):
    if nm not in DCACHE: DCACHE[nm] = disj(nm)
    return DCACHE[nm]
for li, (path, cert) in enumerate(D['leaves']):
    rows = set(BASE); prefix = ()
    for nm, ai in path:
        alts = getd(nm)
        if not (0 <= ai < len(alts)): print("bad alt index", li, nm, ai); errors += 1; continue
        altset = alts[ai]
        tree.setdefault(prefix, {}).setdefault(nm, set()).add(altset)
        rows |= altset; prefix = prefix + ((nm, altset),)
    lam = []
    for r in cert:
        row = rowfromjson(r[:3]); l = F(r[3])
        if row not in rows: print("cert row not in leaf", li, r); errors += 1
        if l < 0: print("negative multiplier", li); errors += 1
        lam.append((row, l))
    tot = {}
    for (a, b, st), l in lam:
        for k, v in a: tot[k] = tot.get(k, 0) + l * v
    if any(v != 0 for v in tot.values()): print("stationarity fails", li); errors += 1
    val = sum(l * b for (a, b, st), l in lam); sw = sum(l for (a, b, st), l in lam if st)
    if not (val < 0 or (val == 0 and sw > 0)): print("value fails", li); errors += 1
for prefix, d in tree.items():
    if len(d) != 1: print("node branches on two disjunctions", len(prefix)); errors += 1; continue
    nm, kids = next(iter(d.items()))
    for alt in getd(nm):
        if alt not in kids and not trivially_inconsistent(alt):
            print("missing alternative at node", len(prefix), nm, sorted(alt)); errors += 1
if () not in tree and len(D['leaves']) != 1: print("empty tree"); errors += 1
names = sorted(set(nm for pth, c in D['leaves'] for nm, ai in pth))
print("file", fn, "h", h, "L", L, "xmin", XMIN, "menu", D['menu'])
print("leaves", len(D['leaves']), "internal nodes", len(tree), "distinct disjunctions used", len(names), "ERRORS", errors)
