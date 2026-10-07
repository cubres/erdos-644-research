"""EXACT re-check (Fractions) of a gen_cert/gen_cert2 adversary point: rationalise the LP point (the margin beta is
~1e-3, far above the rounding), then check (1) every BASE row of the strategy (strict rows strictly), (2) every role
disjunction has a true alternative, (3) EVERY template of the menu (Fano with ALL assignments of the valid roles,
V for all ordered pairs, T3 for all multisets) FAILS, i.e. has a true failure alternative.  Prints the exact minimum
margin.  usage: python3 gadv_verify.py <strategy.json> <gadv.json> [pi0]"""
import sys, json, itertools
from fractions import Fraction as F
import gen_cert as G

spec = json.load(open(sys.argv[1])); d = json.load(open(sys.argv[2]))
pi0 = F(sys.argv[3]) if len(sys.argv) > 3 else F(0)
S = G.Strategy(spec, pi0, lazy=True)
v = {k: F(val).limit_denominator(10 ** 7) for k, val in d['v'].items()}
# restore exact equalities: unit mass of each role on its largest coordinate; minimiser / blocker coordinates
for r in S.roles:
    n = r['name']; fixed = None
    if r['kind'] == 'min': fixed = r['cls']; v[S.c(n, fixed)] = v['s%d' % fixed]
    if r['kind'] == 'blk': fixed = r['facet']; v[S.c(n, fixed)] = v['t%d' % fixed]
    j = max((i for i in range(3) if i != fixed), key=lambda i: v[S.c(n, i)])
    v[S.c(n, j)] = 1 - sum(v[S.c(n, i)] for i in range(3) if i != j)


def val(row):
    co, rhs, st = row
    return sum(c * v[k] for k, c in co) - rhs


def holds(alt):
    return all((val(r) > 0) if r[2] else (val(r) >= 0) for r in alt)


def margin(alt):
    return min(val(r) for r in alt) if alt else F(1)


bad = []
mb = min(val(r) for r in S.BASE)
for r in S.BASE:
    if (r[2] and not val(r) > 0) or (not r[2] and not val(r) >= 0): bad.append(('BASE', sorted(r[0]), float(val(r))))
for nm, alts in S.D.items():
    if not any(holds(a) for a in alts): bad.append((nm, 'no true alternative'))
# validity of requests (exact)
valid = {}
for r in S.roles:
    if r['kind'] != 'req': valid[r['name']] = True; continue
    valid[r['name']] = not any(holds(a) for a in S.void_alts(r))
names = [n for n in S.names if valid[n]]
worst = None
def tcheck(nm, alts):
    global worst
    m = max(margin(a) for a in alts)
    if m <= 0: bad.append((nm, 'template SUCCEEDS', float(m)))
    if worst is None or m < worst[0]: worst = (m, nm)
# Fano over ALL assignments of the valid roles to the 7 points: exact branch and bound (bal_verify.fano_best)
from bal_verify import fano_best
xs = [v['x0'], v['x1'], v['x2']]
vecs = []; vnames = []
for n in names:
    c = [v[S.c(n, j)] for j in range(3)]
    if c not in vecs: vecs.append(c); vnames.append(n)
fb, fa = fano_best(vecs, xs)
print('Fano: min over ALL assignments of the max violation = %.6g at %s' % (float(fb), [vnames[i] for i in fa]))
if fb <= 0: bad.append(('Fano succeeds', [vnames[i] for i in fa]))
if worst is None or fb < worst[0]: worst = (fb, 'F ' + ','.join(vnames[i] for i in fa))
for a in names:
    for b in names:
        if a != b: tcheck('V %s,%s' % (a, b), S.v_fail(a, b))
for t in itertools.combinations_with_replacement(names, 3):
    tcheck('T3 ' + ','.join(t), S.t3_fail(list(t)))
print('valid requests:', [n for n in S.names if S.byname[n]['kind'] == 'req' and valid[n]])
print('min BASE slack %.6g; weakest template margin %.6g at %s' % (float(mb), float(worst[0]), worst[1]))
print('EXACT ADVERSARY CONFIRMED' if not bad else 'NOT CONFIRMED: %s' % bad[:5])
