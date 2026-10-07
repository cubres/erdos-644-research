"""INDEPENDENT std-lib checker (Fractions only; no numpy/scipy/sympy) for sep_cert.py certificates.
Rebuilds from first principles:
 BASE (hypotheses of CLAIM SEP(pi0)): x_i + x_j >= 3/2 + pi0; sigma_i > 2x_i/3; sigma_i <= x_i;
   x_i - sigma_i > tau - 3/4; m^i_i = sigma_i; sum_j m^i_j = 1; 0 <= m^i_j <= x_j; sum_i (x_i - sigma_i) >= tau;
   tau > 3/4.
 The FAILURE alternatives of each named template (a template fails iff one of its feasibility rows is violated
   strictly):  'F <7 labels>' Fano (Lemma 7.63): per part i, 7 line rows  sum_line m^{lab}_i <= 2x_i and the total
   row sum_7 m^{lab}_i <= 4x_i;  'V ab': per part i, a_i + b_i <= x_i and 5a_i/4 + b_i/2 <= x_i;
   'T3 abc': per part the line row a_i+b_i+c_i <= 2x_i, and the cost row sum_i max(a_i,b_i,c_i,(a_i+b_i+c_i)/2)/2
   <= tau whose failure is the disjunction over one term per part of  sum terms/2 > tau.
Checks: (1) each path step names a template and an alternative index; alternatives are matched as ROW SETS;
(2) tree completeness: at every internal node exactly one template is branched and every alternative is a child
(or directly contradicts a BASE row); (3) every leaf carries an exact Motzkin certificate over rows of the leaf:
lam >= 0, sum lam*coef = 0, sum lam*rhs > 0 or (= 0 and positive weight on a strict row).
usage: python3 -S check_sep_cert.py cert.json"""
import sys, json, itertools
from fractions import Fraction as F

D = json.load(open(sys.argv[1]))
PI0 = F(D['pi0'])
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
assert all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2))


def row(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))


def m(i, j):
    return 'm%d_%d' % (i, j)


BASE = set()
for i, j in [(0, 1), (0, 2), (1, 2)]:
    BASE.add(row({'x%d' % i: 1, 'x%d' % j: 1}, F(3, 2) + PI0))
for i in range(3):
    BASE.add(row({'s%d' % i: 1, 'x%d' % i: F(-2, 3)}, 0, True))
    BASE.add(row({'x%d' % i: 1, 's%d' % i: -1}, 0))
    BASE.add(row({'x%d' % i: 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4), True))
    BASE.add(row({m(i, i): 1, 's%d' % i: -1}, 0)); BASE.add(row({m(i, i): -1, 's%d' % i: 1}, 0))
    BASE.add(row({m(i, j): 1 for j in range(3)}, 1)); BASE.add(row({m(i, j): -1 for j in range(3)}, -1))
    for j in range(3):
        BASE.add(row({m(i, j): 1}, 0)); BASE.add(row({'x%d' % j: 1, m(i, j): -1}, 0))
BASE.add(row({'x0': 1, 'x1': 1, 'x2': 1, 's0': -1, 's1': -1, 's2': -1, 'tau': -1}, 0))
BASE.add(row({'tau': 1}, F(3, 4), True))


def fail(d):
    """violation of  d.z <= 0  written as  d.z > 0"""
    return row(d, 0, True)


def alternatives(name):
    kind, arg = name.split(' ', 1)
    out = []
    if kind == 'F':
        lab = [int(c) for c in arg]; assert len(lab) == 7 and set(lab) <= {0, 1, 2}
        for i in range(3):
            for l in LINES:
                d = {'x%d' % i: -2}
                for q in l: d[m(lab[q], i)] = d.get(m(lab[q], i), 0) + 1
                out.append(frozenset([fail(d)]))
            d = {'x%d' % i: -4}
            for q in range(7): d[m(lab[q], i)] = d.get(m(lab[q], i), 0) + 1
            out.append(frozenset([fail(d)]))
    elif kind == 'V':
        a, b = int(arg[0]), int(arg[1]); assert a != b and len(arg) == 2
        for i in range(3):
            out.append(frozenset([fail({m(a, i): 1, m(b, i): 1, 'x%d' % i: -1})]))
            out.append(frozenset([fail({m(a, i): F(5, 4), m(b, i): F(1, 2), 'x%d' % i: -1})]))
    elif kind == 'T3':
        a, b, c = [int(ch) for ch in arg]
        for i in range(3):
            d = {'x%d' % i: -2}
            for q in (a, b, c): d[m(q, i)] = d.get(m(q, i), 0) + 1
            out.append(frozenset([fail(d)]))
        per = []
        for i in range(3):
            ts = []
            for q in (a, b, c):
                t = {m(q, i): F(1, 2)}
                if t not in ts: ts.append(t)
            h = {}
            for q in (a, b, c): h[m(q, i)] = h.get(m(q, i), 0) + F(1, 4)
            if h not in ts: ts.append(h)
            per.append(ts)
        for ch in itertools.product(*per):
            d = {'tau': -1}
            for t in ch:
                for k, v in t.items(): d[k] = d.get(k, 0) + v
            out.append(frozenset([fail(d)]))
    else:
        raise ValueError(name)
    ded = []                      # identical alternatives are merged (first occurrence order)
    for a in out:
        if a not in ded: ded.append(a)
    return ded


def contradicts_base(alt):
    for (a, b, st) in alt:
        neg = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == neg and (b + b2 > 0 or (b + b2 == 0 and (st or st2))):
                return True
    return False


def fromjson(r):
    return (frozenset((k, F(v)) for k, v in r[0].items() if F(v) != 0), F(r[1]), bool(r[2]))


errors = 0; tree = {}; ALT = {}
for li, (path, cert) in enumerate(D['leaves']):
    rows = set(BASE); prefix = ()
    for nm, ai in path:
        if nm not in ALT: ALT[nm] = alternatives(nm)
        alts = ALT[nm]
        if not 0 <= ai < len(alts):
            print('bad alternative index', li, nm, ai); errors += 1; continue
        tree.setdefault(prefix, {}).setdefault(nm, set()).add(alts[ai])
        rows |= alts[ai]; prefix = prefix + ((nm, alts[ai]),)
    tot = {}; val = F(0); sw = F(0)
    for r in cert:
        rr = fromjson(r[:3]); l = F(r[3])
        if rr not in rows: print('certificate row not in leaf', li, r[:3]); errors += 1
        if l < 0: print('negative multiplier', li); errors += 1
        for k, v in rr[0]: tot[k] = tot.get(k, 0) + l * v
        val += l * rr[1]
        if rr[2]: sw += l
    if any(v != 0 for v in tot.values()): print('stationarity fails at leaf', li); errors += 1
    if not (val > 0 or (val == 0 and sw > 0)): print('value condition fails at leaf', li); errors += 1
for prefix, d in tree.items():
    if len(d) != 1: print('node branches on two templates'); errors += 1; continue
    nm, kids = next(iter(d.items()))
    for alt in ALT[nm]:
        if alt not in kids and not contradicts_base(alt):
            print('missing alternative at depth', len(prefix), nm); errors += 1
if () not in tree and len(D['leaves']) != 1:
    print('empty tree'); errors += 1
used = sorted(set(nm for p, c in D['leaves'] for nm, a in p))
print('pi0', PI0, 'leaves', len(D['leaves']), 'internal nodes', len(tree), 'templates used', used)
print('ERRORS', errors, '=> CERTIFICATE VALID' if errors == 0 else '=> INVALID')
