"""check_gen_certp.py -- INDEPENDENT std-lib checker (Fractions only) for SEP(h, L; pi0) certificates of gen_certp.py.
usage: python3 -S check_gen_certp.py cert.jsonl.gz [mutate=pi0:<v>|dropleaf:<k>|flipstrict:<k>]
Nothing is imported from the engine; every row is rebuilt from the statements below.

STATEMENT CERTIFIED.  Let K be a closed nonempty set of unit types over p = h + L parts (0 <= c <= x, |c| = 1) whose
heavy parts (S_i = {c in K : c_i > 2x_i/3} != {}) are exactly 0..h-1, with x_i + x_j >= 3/2 + pi0 for all heavy i != j,
and tau := tau*(K) > 3/4.  Then K has a bad 7-tuple.  (Restricted to the REGION rows printed below, if any.)
Proof by contradiction: assume no bad tuple.  The leaves show that every branch of the tree is infeasible.

BASE rows (all facts of a counterexample; proofs in notes_genp_sep.md [20:30]):
  heavy pairs: x_i + x_j >= 3/2 + pi0                                               [hypothesis]
  heavy i: s_i > 2x_i/3 (strict), x_i - s_i >= 0                                    [Lemma SEP (ii): minimiser exists]
  heavy i: x_i - s_i - tau >= -3/4  (NON-strict; only if the spec has erows=true)  [induction: SEP(h-1, L+1; pi0)]
  sum_{heavy} (x_i - s_i) - tau >= 0                                               [class box free, (iv)]
  tau > 3/4;  light l: x_l >= 0
  every role r (a type of K): sum_j c_rj = 1, c_rj >= 0, x_j - c_rj >= 0, light l: 2x_l/3 - c_rl >= 0 [definition of light]
  minimiser role of class i: c_ri = s_i                                             [(ii)]
  REGION: order -> x_0 <= .. <= x_{h-1} and x_h <= .. <= x_{p-1} [WLOG: permutations preserving the heavy set];
          xbox [i, lo, hi]; pairs [i, j, lo, hi].
DISJUNCTIONS (each named step of a path picks an alternative by INDEX in the list rebuilt here):
  'cls r'  : c_ri >= s_i for some heavy i  (pencil + disjoint classes: every type lies in a heavy class)
  'val r', 'ans r i' : requests (box u_i = max(0, min(x_i, min_k e_rik))), exactly as in check_gen_cert3_ns.py,
             with p parts; covering R0: a box of cost <= tau* holds a type.
  'F l0..l6' : the Fano tuple FAILS: some heavy part i and line with row sum > 2x_i, or some part with total > 4x_i
             (Lemma 7.63; at a light part every row is <= 2x_l/3, so line sums <= 2x_l hold automatically).
  'V a,b'  : some part with a_i + b_i > x_i or 5a_i/4 + b_i/2 > x_i.
  'W t:a,b': some part i and efficient vertex (u,v) of the VERIFIED capacity function t with u a_i + v b_i > x_i.
  'R sh:ks:labs' : ONE requested type f on P (sh 1: {0}, 2: {0,1}, 3: {0,1,3}, 4: {3,4,5,6}); see r_alternatives.
  Templates also carry the void alternatives of their request labels."""
import sys, json, itertools, gzip
from fractions import Fraction as F

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
assert all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2)) and len(LINES) == 7
assert all(sum(1 for L_ in LINES if q in L_) == 3 for q in range(7))

ARGS = dict(a.split('=', 1) for a in sys.argv[2:])
MUT = ARGS.get('mutate')
fn = sys.argv[1]
fh = gzip.open(fn, 'rt') if fn.endswith('.gz') else open(fn)
HDR = json.loads(fh.readline())
LEAVES = (json.loads(line) for line in fh)
PI0 = F(HDR['pi0'])
if MUT and MUT.startswith('pi0:'): PI0 = F(MUT[4:]); print('MUTATION: pi0 ->', PI0)
SPEC = HDR['strategy']
h = int(SPEC['h']); Lc = int(SPEC.get('L', 0)); p = h + Lc
HEAVY = list(range(h)); LIGHT = list(range(h, p))
ROLES = SPEC['roles']; BYN = {r['name']: r for r in ROLES}
assert len(BYN) == len(ROLES)
EROWS = bool(SPEC.get('erows', True))


def row(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))


def add(*ds):
    o = {}
    for d in ds:
        for k, v in d.items(): o[k] = o.get(k, F(0)) + F(v)
    return o


def neg(d):
    return {k: -F(v) for k, v in d.items()}


def X(i):
    return 'x%d' % i


def c(r, j):
    return 'c%s_%d' % (r, j)


# ------------------------------------------------ BASE ------------------------------------------------
BASE = set(); TAG = {}


NONSTRICT = MUT[10:] if MUT and MUT.startswith('nonstrict:') else None


def base(d, rhs, strict, tag):
    if NONSTRICT is not None and NONSTRICT in (tag, 'all') and strict:
        strict = False; print('MUTATION: BASE row', tag, 'made non-strict')
    r = row(d, rhs, strict); BASE.add(r); TAG[r] = tag


for i, j in itertools.combinations(HEAVY, 2):
    base({X(i): 1, X(j): 1}, F(3, 2) + PI0, False, 'pair')
for i in HEAVY:
    base({'s%d' % i: 1, X(i): F(-2, 3)}, 0, True, 'sigma>2x/3')
    base({X(i): 1, 's%d' % i: -1}, 0, False, 'sigma<=x')
    if EROWS: base({X(i): 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4), False, 'e-row')
base(add({'tau': -1}, *[{X(i): 1, 's%d' % i: -1} for i in HEAVY]), 0, False, 'E>=tau')
base({'tau': 1}, F(3, 4), True, 'tau>3/4')
for l in LIGHT: base({X(l): 1}, 0, False, 'x_l>=0')
REGION = []
if SPEC.get('order'):
    for grp in (HEAVY, LIGHT):
        for a, b in zip(grp, grp[1:]):
            base({X(b): 1, X(a): -1}, 0, False, 'order'); REGION.append('x%d<=x%d' % (a, b))
for i, lo, hi in SPEC.get('xbox', []):
    if lo is not None: base({X(i): 1}, F(lo), False, 'region'); REGION.append('x%d>=%s' % (i, lo))
    if hi is not None: base({X(i): -1}, -F(hi), False, 'region'); REGION.append('x%d<=%s' % (i, hi))
for i, j, lo, hi in SPEC.get('pairs', []):
    if lo is not None: base({X(i): 1, X(j): 1}, F(lo), False, 'region'); REGION.append('x%d+x%d>=%s' % (i, j, lo))
    if hi is not None: base({X(i): -1, X(j): -1}, -F(hi), False, 'region'); REGION.append('x%d+x%d<=%s' % (i, j, hi))
for r in ROLES:
    n = r['name']
    base({c(n, j): 1 for j in range(p)}, 1, False, 'unit'); base({c(n, j): -1 for j in range(p)}, -1, False, 'unit')
    for j in range(p):
        base({c(n, j): 1}, 0, False, 'c>=0'); base({X(j): 1, c(n, j): -1}, 0, False, 'c<=x')
    for l in LIGHT:
        base({X(l): F(2, 3), c(n, l): -1}, 0, False, 'light')
    if r['kind'] == 'min':
        i = r['cls']; assert i in HEAVY
        base({c(n, i): 1, 's%d' % i: -1}, 0, False, 'min'); base({c(n, i): -1, 's%d' % i: 1}, 0, False, 'min')
    elif r['kind'] == 'dmin':
        # directional minimiser d = argmin{c_l : c in S_i} (l = dir != i; S_i closed nonempty => attained); d in S_i
        i = r['cls']; assert i in HEAVY and 0 <= r['dir'] < p and r['dir'] != i
        base({c(n, i): 1, 's%d' % i: -1}, 0, False, 'dmin-class')
    elif r['kind'] == 'lmin':
        # LEX twin t = lexmin over S_i of (c_l, c_i) (l = dir != i; S_i = {c in K: c_i >= s_i} is closed, so attained).
        # t in S_i.  FREE BOX: w_l = t_l (closed), w_i = t_i - e, w_k = s_k - e (heavy k not in {i,l}), w = x elsewhere.
        # A type c <= w in class i has c_l <= t_l, hence c_l = t_l (min) and then c_i >= t_i > w_i (lex): impossible;
        # in class k (heavy, k not in {i,l}): c_k >= s_k > w_k; in class l (if l heavy): c_l >= s_l > 2x_l/3 > t_l
        # (t is light at l).  So cost(w) = (x_l - t_l) + (x_i - t_i) + sum_k (x_k - s_k) + O(e) >= tau.
        i = r['cls']; l = r['dir']; assert i in HEAVY and 0 <= l < p and l != i
        base({c(n, i): 1, 's%d' % i: -1}, 0, False, 'lmin-class')
        base(add({X(l): 1, c(n, l): -1, X(i): 1, c(n, i): -1, 'tau': -1},
                 *[{X(k): 1, 's%d' % k: -1} for k in HEAVY if k not in (i, l)]), 0, False, 'lmin-box')
    else:
        assert r['kind'] == 'req', r


# ------------------------------------------------ requests ------------------------------------------------
def split(e):
    e = {k: F(v) for k, v in e.items()}; cc = e.pop('c', F(0)); return e, cc


def exprs(r, i):
    return [split(e) for e in r['u'][i]] + [({X(i): F(1)}, F(0))]


def void(r):
    """request r is VOID: cost(u) > tau (>= tau for a strict request); one alternative per expression choice"""
    if r['kind'] != 'req' or r.get('always_valid'): return []
    per = [exprs(r, i) for i in range(p)]
    out = []
    for ks in itertools.product(*[range(len(q)) for q in per]):
        rows = []
        for S in itertools.product([0, 1], repeat=p):
            d = {'tau': F(-1)}; cst = F(0)
            for i in range(p):
                if S[i]: d = add(d, {X(i): 1})
                else:
                    e, cc = per[i][ks[i]]
                    d = add(d, {X(i): 1}, neg(e)); cst -= cc
            rows.append(row(d, -cst, not r.get('strict')))
        out.append(frozenset(rows))
    return out


def valid(r):
    per = [exprs(r, i) for i in range(p)]
    out = []
    for S in itertools.product([0, 1], repeat=p):
        rows = []
        for ks in itertools.product(*[range(len(q)) for q in per]):
            d = {'tau': F(1)}; cst = F(0)
            for i in range(p):
                if S[i]: d = add(d, {X(i): -1})
                else:
                    e, cc = per[i][ks[i]]
                    d = add(d, {X(i): -1}, e); cst += cc
            rows.append(row(d, -cst, bool(r.get('strict'))))
        out.append(frozenset(rows))
    return out


def dedup(a):
    o = []
    for z in a:
        if z not in o: o.append(z)
    return o


def voids_of(names):
    o = []
    for n in sorted(set(names)): o += void(BYN[n])
    return o


# ------------------------------------------------ W catalogue (verified) ------------------------------------------------
_WF = {}


def w_function(t):
    """capacity function t of the two-type catalogue, VERIFIED from first principles (same audit as
    check_gen_cert3_ns.py): cells pairwise non-covering; every LP certificate a feasible primal/dual pair with equal
    values; listed efficient vertices = certified upper-right hull.  M_t(a,b) = max over efficient (u,v) of ua + vb is
    the least total cell mass loading the colour-0 rows by a and the colour-1 rows by b; M_t(a_i,b_i) <= x_i in every
    part gives a bad 7-tuple (same cell family in every part)."""
    if t in _WF: return _WF[t]
    if 'TT' not in _WF:
        _WF['TT'] = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'))
    rec = _WF['TT'][t]; parents = rec['parents']; r = rec['record']; colour = r['colour']
    assert all(0 < m < 127 for m in parents)
    assert all((m1 | m2) != 127 for m1 in parents for m2 in parents)
    certs = {}; vld = {(F(0), F(0))}
    for ce in r['lp_certificates']:
        d = tuple(map(F, ce['direction'])); assert sum(d) == 1 and min(d) >= 0
        y = list(map(F, ce['primal'])); w = list(map(F, ce['dual']))
        assert len(y) == len(parents) and len(w) == 7 and min(y + w) >= 0
        dem = [d[colour >> j & 1] for j in range(7)]
        assert all(sum(y[k] for k, m in enumerate(parents) if m >> j & 1) >= dem[j] for j in range(7))
        assert all(sum(w[j] for j in range(7) if m >> j & 1) <= 1 for m in parents)
        val = sum(y); assert val == sum(a * b for a, b in zip(w, dem)) == F(ce['value'])
        pt = (sum(w[j] for j in range(7) if not colour >> j & 1), sum(w[j] for j in range(7) if colour >> j & 1))
        vld.add(pt); vld.add((pt[0], F(0))); vld.add((F(0), pt[1]))
        certs[d] = val
    pts = [tuple(map(F, q)) for q in r['all_vertices']]
    assert all(q in vld for q in pts)
    eff = sorted(v for v in pts if not any(v != q and v[0] <= q[0] and v[1] <= q[1] for q in pts))
    assert eff == [tuple(map(F, q)) for q in r['vertices']]
    assert certs[(F(1), F(0))] == eff[-1][0] and certs[(F(0), F(1))] == eff[0][1]
    for lft, rgt in zip(eff, eff[1:]):
        a_ = lft[1] - rgt[1]; b_ = rgt[0] - lft[0]; assert a_ > 0 and b_ > 0
        dd = (a_ / (a_ + b_), b_ / (a_ + b_)); assert dd in certs and certs[dd] == (a_ * lft[0] + b_ * lft[1]) / (a_ + b_)
    _WF[t] = eff
    return eff


# ------------------------------------------------ R (one-request Fano) ------------------------------------------------
def r_alternatives(arg):
    """'R sh:ks:labs'.  P = positions of one requested type f; the named rows labs sit on A = [7] \\ P (increasing).
    Per part i:  heavy i: bounds B_i = [ (2x_i - sum_{q in l, q in A} c_{lab q,i}) / |l n P|  for each line l meeting P
    (LINES order) ] + [ (4x_i - sum_{q in A} c_{lab q,i}) / |P| ];  u_i = x_i (ks[i] = 'x') or B_i[int(ks[i])].
    light l: tb = (4x_l - sum_{q in A} c_{lab q,l}) / |P|;  u_l = x_l (ks = 'x') or tb (ks = '0').
    SUCCESS rows: heavy i: every A-only line sum <= 2x_i, u_i <= each bound, u_i <= x_i, u_i >= 0;
    light l: 'x': 2x_l/3 <= tb;  '0': 0 <= u_l <= x_l;   and  sum_i (x_i - u_i) <= tau.
    Then 0 <= u <= x, cost(u) <= tau*, so (R0) some f in K has f <= u, and f on P + labs on A is a Fano tuple:
    heavy i: a line l meeting P has sum = (A-part) + |l n P| f_i <= 2x_i since f_i <= u_i <= B_i[l]; total similarly;
    A-only lines by the rows.  Light l: all line sums <= 2x_l (every type, f included, is <= 2x_l/3 at a light part);
    total = sum_A + |P| f_l <= 4x_l because f_l <= 2x_l/3 <= tb ('x') or f_l <= u_l = tb ('0').  Rows <= x: f <= u <= x.
    Lemma 7.63 => bad tuple.  FAILURE = one strictly violated success row (or a void request label)."""
    sh, ks, labs = arg.split(':'); labs = labs.split(',')
    P = {'1': (0,), '2': (0, 1), '3': (0, 1, 3), '4': (3, 4, 5, 6)}[sh]
    A = [q for q in range(7) if q not in P]
    assert len(labs) == len(A) and len(ks) == p and all(l in BYN for l in labs)
    lab = {q: labs[k] for k, q in enumerate(A)}
    nP = len(P)
    alts = []; U = []
    for i in range(p):
        tot = add({X(i): F(4, nP)}, *[{c(lab[q], i): F(-1, nP)} for q in A])
        if i in HEAVY:
            bounds = []
            for L_ in LINES:
                m = len([q for q in L_ if q in P])
                if m == 0: continue
                bounds.append(add({X(i): F(2, m)}, *[{c(lab[q], i): F(-1, m)} for q in L_ if q not in P]))
            bounds.append(tot)
            if ks[i] == 'x': u = {X(i): F(1)}
            else:
                assert ks[i].isdigit() and int(ks[i]) < len(bounds); u = bounds[int(ks[i])]
            for L_ in LINES:
                if any(q in P for q in L_): continue
                alts.append(frozenset([row(add({X(i): F(-2)}, *[{c(lab[q], i): 1} for q in L_]), 0, True)]))
            for b in bounds + [{X(i): F(1)}]:
                d = {k: v for k, v in add(u, neg(b)).items() if v != 0}
                if d: alts.append(frozenset([row(d, 0, True)]))
            alts.append(frozenset([row(neg(u), 0, True)]))
        else:
            if ks[i] == 'x':
                u = {X(i): F(1)}
                alts.append(frozenset([row(add({X(i): F(2, 3)}, neg(tot)), 0, True)]))
            else:
                assert ks[i] == '0'; u = tot
                alts.append(frozenset([row(add(u, {X(i): F(-1)}), 0, True)]))
                alts.append(frozenset([row(neg(u), 0, True)]))
        U.append(u)
    d = add({'tau': F(-1)}, *[add({X(i): F(1)}, neg(U[i])) for i in range(p)])
    alts.append(frozenset([row(d, 0, True)]))
    return dedup(alts + voids_of(labs))


def alternatives(name):
    kind, arg = name.split(' ', 1)
    if kind == 'dm':
        # d = argmin{c_l : c in S_i}.  A type r is either outside S_i -- then r_i <= 2x_i/3 < s_i (classes: c_i > 2x_i/3
        # iff c in S_i, and s_i > 2x_i/3) -- or in S_i, and then r_l >= d_l by minimality.
        dn, rn = arg.split(' '); d = BYN[dn]; assert d['kind'] == 'dmin' and rn in BYN and rn != dn
        i, l = d['cls'], d['dir']
        return [frozenset([row({'s%d' % i: 1, c(rn, i): -1}, 0, True)]), frozenset([row({c(rn, l): 1, c(dn, l): -1}, 0)])]
    if kind == 'dfree':
        # if d_l > 0, the box w_l = d_l - e, w_k = s_k - e (heavy k not in {i,l}), w = x elsewhere is FREE: a class-i type
        # has c_l >= d_l; a class-k type c_k >= s_k; if l is heavy, a class-l type has c_l >= s_l > 2x_l/3 > d_l (d is
        # light at l, being in S_i).  So cost = (x_l - d_l) + sum_{k} (x_k - s_k) + O(e) >= tau.
        d = BYN[arg]; assert d['kind'] == 'dmin'
        i, l = d['cls'], d['dir']
        cost = add({X(l): 1, c(arg, l): -1, 'tau': -1}, *[{X(k): 1, 's%d' % k: -1} for k in HEAVY if k not in (i, l)])
        return [frozenset([row({c(arg, l): -1}, 0)]), frozenset([row(cost, 0)])]
    if kind == 'lm':
        # t = lexmin_{S_i} (c_l, c_i).  A type r: r not in S_i (then r_i <= 2x_i/3 < s_i), or (r_l, r_i) >=_lex (t_l, t_i),
        # i.e. r_l > t_l, or r_l = t_l and r_i >= t_i (the last alternative is stated with r_l >= t_l: weaker, sound).
        tn, rn = arg.split(' '); t = BYN[tn]; assert t['kind'] == 'lmin' and rn in BYN and rn != tn
        i, l = t['cls'], t['dir']
        return [frozenset([row({'s%d' % i: 1, c(rn, i): -1}, 0, True)]),
                frozenset([row({c(rn, l): 1, c(tn, l): -1}, 0, True)]),
                frozenset([row({c(rn, l): 1, c(tn, l): -1}, 0), row({c(rn, i): 1, c(tn, i): -1}, 0)])]
    if kind == 'lfree':
        # t_l = min{c_l : c in S_i}; if t_l > 0 the box w_l = t_l - e, w_k = s_k - e (heavy k not in {i,l}) is free
        # (same argument as dfree): (x_l - t_l) + sum_k (x_k - s_k) >= tau.
        t = BYN[arg]; assert t['kind'] == 'lmin'
        i, l = t['cls'], t['dir']
        cost = add({X(l): 1, c(arg, l): -1, 'tau': -1}, *[{X(k): 1, 's%d' % k: -1} for k in HEAVY if k not in (i, l)])
        return [frozenset([row({c(arg, l): -1}, 0)]), frozenset([row(cost, 0)])]
    if kind == 'cls':
        assert arg in BYN and BYN[arg]['kind'] not in ('min', 'dmin', 'lmin')
        return [frozenset([row({c(arg, i): 1, 's%d' % i: -1}, 0)]) for i in HEAVY]
    if kind == 'val':
        r = BYN[arg]; assert r['kind'] == 'req'
        return valid(r) + void(r)
    if kind == 'ans':
        n, i = arg.split(' '); i = int(i); r = BYN[n]; assert r['kind'] == 'req' and 0 <= i < p
        rows = [row(add(e, {c(n, i): -1}), -cc, i in r.get('strict', [])) for e, cc in [split(e) for e in r['u'][i]]]
        return [frozenset(rows), frozenset([row({c(n, i): -1}, 0)])] + void(r)
    if kind == 'R':
        return r_alternatives(arg)
    if kind == 'W':
        t, ab = arg.split(':'); a, b = ab.split(','); assert a in BYN and b in BYN
        verts = w_function(t)
        alts = []
        for i in range(p):
            for u, v in verts:
                alts.append(frozenset([row(add({c(a, i): u}, {c(b, i): v}, {X(i): -1}), 0, True)]))
        return dedup(alts + voids_of([a, b]))
    labs = arg.split(',')
    assert all(l in BYN for l in labs)
    alts = []
    if kind == 'F':
        assert len(labs) == 7
        for i in range(p):
            if i in HEAVY:
                for L_ in LINES:
                    alts.append(frozenset([row(add({X(i): F(-2)}, *[{c(labs[q], i): 1} for q in L_]), 0, True)]))
            alts.append(frozenset([row(add({X(i): F(-4)}, *[{c(labs[q], i): 1} for q in range(7)]), 0, True)]))
    elif kind == 'V':
        a, b = labs; assert a != b
        for i in range(p):
            alts.append(frozenset([row({c(a, i): 1, c(b, i): 1, X(i): -1}, 0, True)]))
            alts.append(frozenset([row({c(a, i): F(5, 4), c(b, i): F(1, 2), X(i): -1}, 0, True)]))
    else:
        raise ValueError(name)
    return dedup(alts + voids_of(labs))


def contradicts_base(alt):
    for (a, b, st) in alt:
        ng = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == ng and (b + b2 > 0 or (b + b2 == 0 and (st or st2))): return True
    return False


def fromjson(r):
    return (frozenset((k, F(v)) for k, v in r[0].items() if F(v) != 0), F(r[1]), bool(r[2]))


DROP = int(MUT[9:]) if MUT and MUT.startswith('dropleaf:') else None
FLIP = int(MUT[11:]) if MUT and MUT.startswith('flipstrict:') else None
LAM = int(MUT[4:]) if MUT and MUT.startswith('lam:') else None
ALTNS = MUT == 'altnonstrict'   # every non-BASE (template/role) row read as non-strict
errors = 0; tree = {}; ALT = {}; nleaves = 0; USE = {}; NODEKIND = {}; DEMOTED = [0]; FLIPPED = []
for li, (path, cert) in enumerate(LEAVES):
    if DROP is not None and li == DROP: print('MUTATION: leaf', li, 'dropped'); continue
    nleaves += 1
    rows = set(BASE); prefix = ()
    for nm, ai in path:
        if nm not in ALT: ALT[nm] = alternatives(nm)
        al = ALT[nm]
        if not 0 <= ai < len(al): print('bad index', li, nm, ai); errors += 1; break
        tree.setdefault(prefix, {}).setdefault(nm, set()).add(ai)
        rows |= al[ai]; prefix = prefix + ((nm, ai),)
    if ALTNS: rows = set((a, b, st_ and (a, b, st_) in BASE) for (a, b, st_) in rows)
    tot = {}; val = F(0); sw = F(0); tags = set()
    for k, r in enumerate(cert):
        rr = fromjson(r[:3]); l = F(r[3])
        if LAM is not None and li == LAM and k == 0: l = 2 * l; print('MUTATION: multiplier of leaf', li, 'row 0 doubled')
        if ALTNS: rr = (rr[0], rr[1], rr[2] and rr in BASE)
        if FLIP is not None and li == FLIP and rr[2] and not FLIPPED:
            rr = (rr[0], rr[1], False); FLIPPED.append(k); print('MUTATION: first strict row of leaf', li, '(row %d) made non-strict' % k)
        if rr not in rows and rr[2] and (rr[0], rr[1], False) in rows:
            rr = (rr[0], rr[1], False); DEMOTED[0] += 1          # cited strict, only the non-strict row is proved
        if rr not in rows: print('certificate row not in leaf', li); errors += 1
        if l < 0: print('negative multiplier', li); errors += 1
        if l > 0 and rr in TAG: tags.add(TAG[rr])
        for kk, v in rr[0]: tot[kk] = tot.get(kk, 0) + l * v
        val += l * rr[1]
        if rr[2]: sw += l
    for t in tags: USE[t] = USE.get(t, 0) + 1
    if any(v != 0 for v in tot.values()): print('stationarity fails', li); errors += 1
    if not (val > 0 or (val == 0 and sw > 0)): print('value fails', li); errors += 1
for prefix, d in tree.items():
    if len(d) != 1: print('node branches on two disjunctions'); errors += 1; continue
    nm, kids = next(iter(d.items()))
    NODEKIND[nm] = NODEKIND.get(nm, 0) + 1
    for ai, alt in enumerate(ALT[nm]):
        if ai not in kids and not contradicts_base(alt):
            print('missing alternative at depth', len(prefix), nm); errors += 1
if () not in tree and nleaves != 1: print('empty tree'); errors += 1
# ---- statistics ----
st = {}
for nm, cnt in NODEKIND.items():
    kind, arg = nm.split(' ', 1)
    if kind == 'F': key = 'F(%d labels)' % len(set(arg.split(',')))
    elif kind == 'R':
        sh, ks, labs = arg.split(':'); key = 'R%s(%d labels)' % (sh, len(set(labs.split(','))))
    elif kind == 'W': key = 'W#%s' % arg.split(':')[0]
    else: key = kind
    st[key] = st.get(key, 0) + cnt
print('h %d L %d p %d pi0 %s erows %s roles %s leaves %d internal nodes %d' % (h, Lc, p, PI0, EROWS, [r['name'] for r in ROLES], nleaves, len(tree)))
print('REGION:', REGION if REGION else 'none (all x)')
print('branched templates (internal nodes by kind):', dict(sorted(st.items())))
print('distinct branched templates:', len(NODEKIND))
print('BASE fact usage (number of leaves whose certificate uses it):', dict(sorted(USE.items())))
print('demoted strict rows', DEMOTED[0])
print('ERRORS', errors, '=> CERTIFICATE VALID' if errors == 0 else '=> INVALID')
