"""[gen_cert3 version: + one-request Fano templates R, see r_alternatives]
INDEPENDENT std-lib checker (Fractions only) for gen_cert.py certificates.  usage: python3 -S check_gen_cert.py cert.json
Rebuilds, from the strategy spec stored in the certificate and from first principles:
 BASE: x_i + x_j >= 3/2 + pi0 (all pairs); sigma_i > 2x_i/3; sigma_i <= x_i; x_i - sigma_i > tau - 3/4;
       sum_i (x_i - sigma_i) >= tau; tau > 3/4; every role r: sum_j c_rj = 1, 0 <= c_rj <= x_j;
       minimiser role of class i: c_ri = sigma_i.
 Named disjunctions (every alternative is a conjunction of rows; 'row' = coef.v >= rhs, strict or not):
  'cls r'    : c_r0 >= sigma_0 | c_r1 >= sigma_1 | c_r2 >= sigma_2             (Lemma SEP: every type in a class)
  'val r'    : request r valid  [cost(u) <= tau]  |  request r void [cost(u) > tau],
               cost(u) = sum_i min(x_i, max(0, max_k (x_i - e_rik)))  with u_i = max(0, min(x_i, min_k e_rik));
               valid: one alternative per subset S of parts, rows  tau - sum_{S} x_i - sum_{not S}(x_i - e_{i,k_i}) >= 0
               for all k-choices;  void: one alternative per k-choice (k ranges over the exprs and 'x_i'),
               rows  sum_{S} x_i + sum_{not S}(x_i - e_{i,k_i}) - tau > 0  for all S.
  'ans r i'  : c_ri <= e_rik for all k  |  c_ri <= 0  | the void alternatives of r
               STRICT requests (spec 'strict': list of parts J): valid <=> cost < tau (strict rows), void <=>
               cost >= tau, and for i in J the first alternative is c_ri < e_rik (strict)
               (covering: a valid request has an answer in its box; R0 of notes_structure: cost <= tau* suffices)
  'F a,b,..' : Fano tuple with the listed roles on points 0..6 FAILS: some line sum > 2x_i or total > 4x_i, or a
               used request is void                                               (Lemma 7.63)
  'V a,b'    : V(a,b) (5 rows a, 2 rows b) FAILS: a_i + b_i > x_i or 5a_i/4 + b_i/2 > x_i, or a void role
  'T3 a,b,c' : L5 FAILS: a line row a_i+b_i+c_i > 2x_i, or sum_i max(a_i,b_i,c_i,(a_i+b_i+c_i)/2)/2 > tau
               (one alternative per choice of terms), or a void role                                   (L5)
Checks: path steps are alternatives of the named disjunction (matched by index into the rebuilt, deduplicated
list; a mismatch is caught because certificate rows must belong to the leaf); tree completeness (one disjunction
per internal node, all alternatives present or contradicting a BASE row); exact Motzkin certificate per leaf."""
import sys, json, itertools
from fractions import Fraction as F

if sys.argv[1].endswith('.jsonl.gz') or sys.argv[1].endswith('.jsonl'):
    # streamed format: first line = header, then one leaf [path, certificate] per line
    import gzip
    fh = gzip.open(sys.argv[1], 'rt') if sys.argv[1].endswith('.gz') else open(sys.argv[1])
    D = json.loads(fh.readline())
    D['leaves'] = (json.loads(line) for line in fh)
else:
    D = json.load(open(sys.argv[1]))
PI0 = F(D['pi0']); ROLES = D['strategy']['roles']
BYN = {r['name']: r for r in ROLES}
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
assert all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2)) and len(LINES) == 7


def row(d, rhs, strict=False):
    return (frozenset((k, F(v)) for k, v in d.items() if F(v) != 0), F(rhs), bool(strict))


def add(*ds):
    o = {}
    for d in ds:
        for k, v in d.items(): o[k] = o.get(k, F(0)) + F(v)
    return o


def c(r, j):
    return 'c%s_%d' % (r, j)


def X(i):
    return 'x%d' % i


MODE = D['strategy'].get('mode', 'sep')
BASE = set()
if MODE == 'sep':
    # Lemma SEP: separated regime (pair sums >= 3/2 + pi0), classes disjoint, box = sigma, e_i > eta, E >= tau
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        BASE.add(row({X(i): 1, X(j): 1}, F(3, 2) + PI0))
    for i in range(3):
        BASE.add(row({'s%d' % i: 1, X(i): F(-2, 3)}, 0, True))
        BASE.add(row({X(i): 1, 's%d' % i: -1}, 0))
        BASE.add(row({X(i): 1, 's%d' % i: -1, 'tau': -1}, F(-3, 4), False))  # AUDIT FIX: Corollary C gives e_i >= eta (non-strict)
    BASE.add(row({'x0': 1, 'x1': 1, 'x2': 1, 's0': -1, 's1': -1, 's2': -1, 'tau': -1}, 0))
else:
    # case (A) of Theorem A1: box t >= sigma, cost(t) >= tau, e'_i > eta (Cor. C), x_i > 2 eta (Thm TP), pair bounds
    assert MODE == 'caseA'
    for i, j, lo, hi in D['strategy'].get('pairs', []):
        if lo is not None: BASE.add(row({X(i): 1, X(j): 1}, F(lo)))
        if hi is not None: BASE.add(row({X(i): -1, X(j): -1}, -F(hi)))
    for i in range(3):
        BASE.add(row({'s%d' % i: 1, X(i): F(-2, 3)}, 0, True))
        BASE.add(row({'t%d' % i: 1, 's%d' % i: -1}, 0))
        BASE.add(row({X(i): 1, 't%d' % i: -1}, 0))
        BASE.add(row({X(i): 1, 't%d' % i: -1, 'tau': -1}, F(-3, 4), False))  # AUDIT FIX: Corollary C gives e_i >= eta (non-strict)
        BASE.add(row({X(i): 1, 'tau': -2}, F(-3, 2), True))
    BASE.add(row({'x0': 1, 'x1': 1, 'x2': 1, 't0': -1, 't1': -1, 't2': -1, 'tau': -1}, 0))
BASE.add(row({'tau': 1}, F(3, 4), True))
# ---- REGION rows (the certificate proves the claim on this region only) ----
SPEC = D['strategy']
if SPEC.get('order'):
    BASE.add(row({'x1': 1, 'x0': -1}, 0)); BASE.add(row({'x2': 1, 'x1': -1}, 0))
for i, lo, hi in SPEC.get('xbox', []):
    if lo is not None: BASE.add(row({X(i): 1}, F(lo)))
    if hi is not None: BASE.add(row({X(i): -1}, -F(hi)))
if SPEC.get('taubox'):
    lo, hi = SPEC['taubox']
    if lo is not None: BASE.add(row({'tau': 1}, F(lo)))
    if hi is not None: BASE.add(row({'tau': -1}, -F(hi)))
if MODE == 'sep':
    for i, j, lo, hi in SPEC.get('pairs', []):
        if lo is not None: BASE.add(row({X(i): 1, X(j): 1}, F(lo)))
        if hi is not None: BASE.add(row({X(i): -1, X(j): -1}, -F(hi)))


def permuted_role(r, p, sig):
    """image of role r under the part permutation p (list: i -> p[i]) with role renaming sig (dict)"""
    def ren(k):
        if k in ('c', 'tau'): return k
        if k[0] in 'xst' and k[1:].isdigit(): return k[0] + str(p[int(k[1:])])
        assert k[0] == 'c'
        nm, j = k[1:].rsplit('_', 1)
        return 'c%s_%d' % (sig[nm], p[int(j)])
    out = {'kind': r['kind']}
    if r['kind'] == 'min': out['cls'] = p[r['cls']]
    if r['kind'] == 'blk': out['facet'] = p[r['facet']]
    if r['kind'] == 'dmin': out['cls'] = p[r['cls']]; out['dir'] = p[r['dir']]
    if r['kind'] == 'req':
        u = [None] * 3
        for i in range(3):
            u[p[i]] = sorted(json.dumps({ren(k): str(F(v)) for k, v in e.items()}, sort_keys=True) for e in r['u'][i])
        out['u'] = u; out['strict'] = sorted(p[i] for i in r.get('strict', []))
        out['lex'] = None if r.get('lex') is None else p[r['lex']]
    return out


def canon(r):
    out = {'kind': r['kind']}
    if r['kind'] == 'min': out['cls'] = r['cls']
    if r['kind'] == 'blk': out['facet'] = r['facet']
    if r['kind'] == 'dmin': out['cls'] = r['cls']; out['dir'] = r['dir']
    if r['kind'] == 'req':
        out['u'] = [sorted(json.dumps({k: str(F(v)) for k, v in e.items()}, sort_keys=True) for e in r['u'][i]) for i in range(3)]
        out['strict'] = sorted(r.get('strict', []))
        out['lex'] = r.get('lex')
    return out


if SPEC.get('order'):
    # the ordering x_0 <= x_1 <= x_2 is WLOG only if hypotheses and strategy are invariant under all part permutations
    # NOTE: 'pairs' / 'xbox' / 'taubox' are REGION restrictions stated in the ordered coordinates; the certificate
    # proves the claim on that region of the ordered space (coverage of the whole space is checked separately,
    # check_cover.py).  The unrestricted hypotheses (BASE without region rows) are symmetric by construction.
    # WLOG x_0 <= x_1 <= x_2: the HYPOTHESES (closed K, tau* > 3/4, no bad tuple, and the unrestricted BASE facts) are
    # invariant under permuting the parts, so a counterexample exists iff an ordered one exists.  The strategy is only
    # a list of objects/facts derived from the (ordered) counterexample, so it need NOT be symmetric.  (The original
    # checker demanded strategy invariance; that is sufficient but not necessary.)  We report invariance for info.
    inv = True
    for p in itertools.permutations(range(3)):
        sig = {}; used = set()
        for r in ROLES:
            im = permuted_role(r, p, sig)
            cand = [q for q in ROLES if q['name'] not in used and canon(q) == im]
            if not cand: inv = False; break
            sig[r['name']] = cand[0]['name']; used.add(cand[0]['name'])
        if not inv: break
    print('ordering x0 <= x1 <= x2 used (WLOG by symmetry of the hypotheses); strategy invariant: %s' % inv)
for r in ROLES:
    n = r['name']
    BASE.add(row({c(n, j): 1 for j in range(3)}, 1)); BASE.add(row({c(n, j): -1 for j in range(3)}, -1))
    for j in range(3):
        BASE.add(row({c(n, j): 1}, 0)); BASE.add(row({X(j): 1, c(n, j): -1}, 0))
    if r['kind'] == 'min':
        i = r['cls']; BASE.add(row({c(n, i): 1, 's%d' % i: -1}, 0)); BASE.add(row({c(n, i): -1, 's%d' % i: 1}, 0))
    elif r['kind'] == 'blk':
        assert MODE == 'caseA'                      # pure facet blocker of L3: c_i = t_i, c_j < t_j
        i = r['facet']; BASE.add(row({c(n, i): 1, 't%d' % i: -1}, 0)); BASE.add(row({c(n, i): -1, 't%d' % i: 1}, 0))
        for j in range(3):
            if j != i: BASE.add(row({'t%d' % j: 1, c(n, j): -1}, 0, True))
    elif r['kind'] == 'dmin':
        # directional minimiser (separated mode): the class-k type with least c_i; it lies in S_k: c_k >= sigma_k
        assert MODE == 'sep' and r['cls'] != r['dir']
        BASE.add(row({c(n, r['cls']): 1, 's%d' % r['cls']: -1}, 0))
    else:
        assert r['kind'] == 'req'


def split(e):
    e = {k: F(v) for k, v in e.items()}; cc = e.pop('c', F(0)); return e, cc


def exprs(r, i):
    return [split(e) for e in r['u'][i]] + [({X(i): F(1)}, F(0))]


def void(r):
    if r['kind'] != 'req': return []
    per = [exprs(r, i) for i in range(3)]
    out = []
    for ks in itertools.product(*[range(len(p)) for p in per]):
        rows = []
        for S in itertools.product([0, 1], repeat=3):
            d = {'tau': F(-1)}; cst = F(0)
            for i in range(3):
                if S[i]: d = add(d, {X(i): 1})
                else:
                    e, cc = per[i][ks[i]]
                    d = add(d, {X(i): 1}, {k: -v for k, v in e.items()}); cst -= cc
            rows.append(row(d, -cst, not r.get('strict')))
        out.append(frozenset(rows))
    return out


def valid(r):
    per = [exprs(r, i) for i in range(3)]
    out = []
    for S in itertools.product([0, 1], repeat=3):
        rows = []
        for ks in itertools.product(*[range(len(p)) for p in per]):
            d = {'tau': F(1)}; cst = F(0)
            for i in range(3):
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


def alternatives(name):
    kind, arg = name.split(' ', 1)
    if kind == 'gap':                    # F3 dichotomy: c_i <= 2x_i/3 or c_i >= sigma_i
        assert MODE == 'caseA'
        n, i = arg.split(' '); i = int(i); assert n in BYN
        return [frozenset([row({X(i): F(2, 3), c(n, i): -1}, 0)]), frozenset([row({c(n, i): 1, 's%d' % i: -1}, 0)])]
    if kind == 'sh':                     # F2: every type is super-heavy somewhere
        assert MODE == 'caseA' and arg in BYN
        return [frozenset([row({c(arg, i): 1, 's%d' % i: -1}, 0)]) for i in range(3)]
    if kind == 'bk':                     # case (A): every type is blocked by t
        assert MODE == 'caseA' and arg in BYN
        return [frozenset([row({c(arg, i): 1, 't%d' % i: -1}, 0)]) for i in range(3)]
    if kind == 'lex':
        # EXTREMAL answer: the answer of request r minimises c_l over the types in r's box (K closed: attained).  If
        # c_l > 0 the box {w_l < c_l, w_j <= u_j} is free, so (x_l - c_l) + sum_{j != l} cost_j(u) >= tau*, where
        # cost_j(u) = min(x_j, max_k (x_j - e_jk)) = max over expression choices of min over S ... (see valid()).
        r = BYN[arg]; l = r['lex']; assert not r.get('strict')
        others = [j for j in range(3) if j != l]
        per = {j: exprs(r, j) for j in others}
        out = []
        for ks in itertools.product(*[range(len(per[j])) for j in others]):
            rows = []
            for S in itertools.product([0, 1], repeat=len(others)):
                d = {X(l): F(1), c(arg, l): F(-1), 'tau': F(-1)}; cst = F(0)
                for jj, j in enumerate(others):
                    if S[jj]: d = add(d, {X(j): 1})
                    else:
                        e, cc = per[j][ks[jj]]
                        d = add(d, {X(j): 1}, {k: -v for k, v in e.items()}); cst -= cc
                rows.append(row(d, -cst))
            out.append(frozenset(rows))
        return out + [frozenset([row({c(arg, l): -1}, 0)])] + void(r)
    if kind == 'cls':
        assert MODE == 'sep'
        return [frozenset([row({c(arg, i): 1, 's%d' % i: -1}, 0)]) for i in range(3)]
    if kind == 'val':
        r = BYN[arg]; assert r['kind'] == 'req'
        return valid(r) + void(r)
    if kind == 'ans':
        n, i = arg.split(' '); i = int(i); r = BYN[n]
        rows = []
        for e, cc in [split(e) for e in r['u'][i]]:
            # STRICT request (r['strict'] = parts J): if cost(u) < tau then some type c <= u has c_j < u_j for every
            # j in J with u_j > 0 (apply the covering to u - eps*1_J); hence c_j < e_jk for all k, or c_j <= 0.
            rows.append(row(add(e, {c(n, i): -1}), -cc, i in r.get('strict', [])))
        return [frozenset(rows), frozenset([row({c(n, i): -1}, 0)])] + void(r)
    if kind == 'R':
        return r_alternatives(arg)
    if kind == 'W':
        # two-type tuple of capacity function t (rows a on the colour-0 rows of its support, b on the colour-1 rows):
        # FAILS iff some part i and efficient vertex (u,v) of the verified function has u a_i + v b_i > x_i.
        t, ab = arg.split(':'); a, b = ab.split(','); assert a in BYN and b in BYN
        verts = w_function(t)
        alts = []
        for i in range(3):
            for u, v in verts:
                alts.append(frozenset([row(add({c(a, i): u}, {c(b, i): v}, {X(i): -1}), 0, True)]))
        return dedup(alts + voids_of([a, b]))
    if kind == 'dm':
        # d = argmin{c_i : c in S_k} (S_k = {c_k >= sigma_k}, closed, nonempty).  Any type r: r not in S_k (r_k < sigma_k,
        # by the dichotomy c_k <= 2x_k/3 < sigma_k or c_k >= sigma_k) or r_i >= d_i.
        dn, rn = arg.split(' '); d = BYN[dn]; assert d['kind'] == 'dmin' and rn in BYN and rn != dn
        k, i = d['cls'], d['dir']
        return [frozenset([row({'s%d' % k: 1, c(rn, k): -1}, 0, True)]), frozenset([row({c(rn, i): 1, c(dn, i): -1}, 0)])]
    if kind == 'dfree':
        # if d_i > 0 the box {c_i < d_i, c_j < sigma_j} (j the third part) holds no type: class i needs c_i >= sigma_i
        # > 2x_i/3 > d_i (d is light at i), class j needs c_j >= sigma_j, class k needs c_i >= d_i.  So its cost
        # (x_i - d_i) + (x_j - sigma_j) >= tau*.
        d = BYN[arg]; assert d['kind'] == 'dmin'
        k, i = d['cls'], d['dir']; j = 3 - k - i
        return [frozenset([row({c(arg, i): -1}, 0)]),
                frozenset([row({X(i): 1, c(arg, i): -1, X(j): 1, 's%d' % j: -1, 'tau': -1}, 0)])]
    labs = arg.split(',')
    for l in labs: assert l in BYN
    alts = []
    if kind == 'F':
        assert len(labs) == 7
        for i in range(3):
            for L in LINES:
                d = {X(i): F(-2)}
                for q in L: d = add(d, {c(labs[q], i): 1})
                alts.append(frozenset([row(d, 0, True)]))
            d = {X(i): F(-4)}
            for q in range(7): d = add(d, {c(labs[q], i): 1})
            alts.append(frozenset([row(d, 0, True)]))
    elif kind == 'V':
        a, b = labs; assert a != b
        for i in range(3):
            alts.append(frozenset([row({c(a, i): 1, c(b, i): 1, X(i): -1}, 0, True)]))
            alts.append(frozenset([row({c(a, i): F(5, 4), c(b, i): F(1, 2), X(i): -1}, 0, True)]))
    elif kind == 'T3':
        assert len(labs) == 3
        for i in range(3):
            d = {X(i): F(-2)}
            for q in labs: d = add(d, {c(q, i): 1})
            alts.append(frozenset([row(d, 0, True)]))
        per = []
        for i in range(3):
            ts = []
            for q in labs:
                t = {c(q, i): F(1, 2)}
                if t not in ts: ts.append(t)
            h = {}
            for q in labs: h = add(h, {c(q, i): F(1, 4)})
            if h not in ts: ts.append(h)
            per.append(ts)
        for ch in itertools.product(*per):
            alts.append(frozenset([row(add({'tau': F(-1)}, *ch), 0, True)]))
    else:
        raise ValueError(name)
    return dedup(alts + voids_of(labs))


_WF = {}


def w_function(t):
    """Load capacity function t from the two-type catalogue and VERIFY it from first principles (std lib, Fractions):
    the support cells ('parents', 7-bit masks) are pairwise non-covering (no union of two cells, nor a single cell, is
    all of [7]); every LP certificate (direction d, cell masses y, row weights w) is a feasible primal/dual pair of
    min sum y s.t. every row j is covered >= d[colour_j], with equal values; the dual points are points of the
    projected dual polytope; the listed efficient vertices are the upper-right hull and every facet direction of it is
    certified.  Hence M_t(a,b) := max over efficient (u,v) of u a + v b is EXACTLY the least total cell mass that
    loads the colour-0 rows by a and the colour-1 rows by b, and M_t(a_i,b_i) <= x_i in every part gives cells with
    part totals <= x_i, pairwise non-covering, loading 5-or-so copies... i.e. a bad 7-tuple on the rows a, b."""
    if t in _WF: return _WF[t]
    if 'TT' not in _WF:
        _WF['TT'] = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'))
    rec = _WF['TT'][t]; parents = rec['parents']; r = rec['record']; colour = r['colour']
    assert all(0 < m < 127 for m in parents)
    assert all((m1 | m2) != 127 for m1 in parents for m2 in parents)
    certs = {}; valid = {(F(0), F(0))}
    for ce in r['lp_certificates']:
        d = tuple(map(F, ce['direction'])); assert sum(d) == 1 and min(d) >= 0
        y = list(map(F, ce['primal'])); w = list(map(F, ce['dual']))
        assert len(y) == len(parents) and len(w) == 7 and min(y + w) >= 0
        dem = [d[colour >> j & 1] for j in range(7)]
        assert all(sum(y[k] for k, m in enumerate(parents) if m >> j & 1) >= dem[j] for j in range(7))
        assert all(sum(w[j] for j in range(7) if m >> j & 1) <= 1 for m in parents)
        val = sum(y); assert val == sum(p * q for p, q in zip(w, dem)) == F(ce['value'])
        pt = (sum(w[j] for j in range(7) if not colour >> j & 1), sum(w[j] for j in range(7) if colour >> j & 1))
        valid.add(pt); valid.add((pt[0], F(0))); valid.add((F(0), pt[1]))
        certs[d] = val
    pts = [tuple(map(F, p)) for p in r['all_vertices']]
    assert all(p in valid for p in pts)
    eff = sorted(v for v in pts if not any(v != q and v[0] <= q[0] and v[1] <= q[1] for q in pts))
    assert eff == [tuple(map(F, p)) for p in r['vertices']]
    assert certs[(F(1), F(0))] == eff[-1][0] and certs[(F(0), F(1))] == eff[0][1]
    for lft, rgt in zip(eff, eff[1:]):
        a_ = lft[1] - rgt[1]; b_ = rgt[0] - lft[0]; assert a_ > 0 and b_ > 0
        dd = (a_ / (a_ + b_), b_ / (a_ + b_)); assert dd in certs and certs[dd] == (a_ * lft[0] + b_ * lft[1]) / (a_ + b_)
    _WF[t] = eff
    return eff


def r_alternatives(arg):
    """ONE-REQUEST Fano template 'R sh:ks:labs' FAILS.  Statement: P = positions of one requested type f
    (sh 1 -> {0}, 2 -> {0,1}, 3 -> {0,1,3}); A = the other points in increasing order, carrying the named roles labs.
    For part i, the bounds on f_i are (2x_i - sum of the A-rows of line l)/|l cap P| for each line l meeting P (in
    LINES order), then (4x_i - sum of all A-rows)/|P|; u_i = x_i (ks[i] = 'x') or the bound number ks[i].
    SUCCESS = (a) A-only lines <= 2x_i, (b) u_i <= each bound and u_i <= x_i, (c) u_i >= 0, (d) sum_i (x_i - u_i)
    <= tau.  Then the box u has cost <= tau*, contains a type f (R0: closed K), and f on P with the named rows on A
    satisfies Lemma 7.63 (lines through P: A-sum + |l cap P| f_i <= 2x_i by (b); total by (b); A-only lines by (a)).
    FAILURE = one strictly violated row of (a)-(d), or a used request is void."""
    sh, ks, labs = arg.split(':'); labs = labs.split(',')
    P = {'1': (0,), '2': (0, 1), '3': (0, 1, 3)}[sh]
    A = [q for q in range(7) if q not in P]
    assert len(labs) == len(A) and len(ks) == 3
    for l in labs: assert l in BYN
    lab = {q: labs[k] for k, q in enumerate(A)}
    alts = []; U = []
    for i in range(3):
        bounds = []
        for L in LINES:
            n = len([q for q in L if q in P])
            if n == 0: continue
            d = {X(i): F(2, n)}
            for q in L:
                if q not in P: d = add(d, {c(lab[q], i): F(-1, n)})
            bounds.append(d)
        d = {X(i): F(4, len(P))}
        for q in A: d = add(d, {c(lab[q], i): F(-1, len(P))})
        bounds.append(d)
        u = {X(i): F(1)} if ks[i] == 'x' else bounds[int(ks[i])]
        U.append(u)
        for L in LINES:                                       # (a) A-only lines
            if any(q in P for q in L): continue
            d = {X(i): F(-2)}
            for q in L: d = add(d, {c(lab[q], i): 1})
            alts.append(frozenset([row(d, 0, True)]))
        for b in bounds + [{X(i): F(1)}]:                     # (b) u_i - b > 0
            d = add(u, {k: -v for k, v in b.items()})
            d = {k: v for k, v in d.items() if v != 0}
            if d: alts.append(frozenset([row(d, 0, True)]))
        alts.append(frozenset([row({k: -v for k, v in u.items()}, 0, True)]))     # (c) u_i < 0
    d = {'tau': F(-1)}
    for i in range(3): d = add(d, {X(i): 1}, {k: -v for k, v in U[i].items()})
    alts.append(frozenset([row({k: v for k, v in d.items() if v != 0}, 0, True)]))  # (d) cost(u) > tau
    return dedup(alts + voids_of(labs))


def contradicts_base(alt):
    for (a, b, st) in alt:
        neg = frozenset((k, -v) for k, v in a)
        for (a2, b2, st2) in BASE:
            if a2 == neg and (b + b2 > 0 or (b + b2 == 0 and (st or st2))): return True
    return False


def fromjson(r):
    return (frozenset((k, F(v)) for k, v in r[0].items() if F(v) != 0), F(r[1]), bool(r[2]))


errors = 0; tree = {}; ALT = {}; nleaves = 0; USED = set(); DEMOTED = [0]
for li, (path, cert) in enumerate(D['leaves']):
    nleaves += 1; USED.update(nm for nm, ai in path)
    rows = set(BASE); prefix = ()
    for nm, ai in path:
        if nm not in ALT: ALT[nm] = alternatives(nm)
        al = ALT[nm]
        if not 0 <= ai < len(al): print('bad index', li, nm, ai); errors += 1; continue
        tree.setdefault(prefix, {}).setdefault(nm, set()).add(ai)       # children recorded by alternative INDEX
        rows |= al[ai]; prefix = prefix + ((nm, ai),)
    tot = {}; val = F(0); sw = F(0)
    for r in cert:
        rr = fromjson(r[:3]); l = F(r[3])
        if rr not in rows and rr[2] and (rr[0], rr[1], False) in rows:
            rr = (rr[0], rr[1], False); DEMOTED[0] += 1        # AUDIT FIX: cited strict, only non-strict is proved
        if rr not in rows: print('certificate row not in leaf', li); errors += 1
        if l < 0: print('negative multiplier', li); errors += 1
        for k, v in rr[0]: tot[k] = tot.get(k, 0) + l * v
        val += l * rr[1]
        if rr[2]: sw += l
    if any(v != 0 for v in tot.values()): print('stationarity fails', li); errors += 1
    if not (val > 0 or (val == 0 and sw > 0)): print('value fails', li); errors += 1
for prefix, d in tree.items():
    if len(d) != 1: print('node branches on two disjunctions'); errors += 1; continue
    nm, kids = next(iter(d.items()))
    for ai, alt in enumerate(ALT[nm]):
        if ai not in kids and not contradicts_base(alt):
            print('missing alternative at depth', len(prefix), nm); errors += 1
if () not in tree and nleaves != 1: print('empty tree'); errors += 1
used = sorted(USED)
print('pi0', PI0, 'roles', [r['name'] for r in ROLES], 'leaves', nleaves, 'internal nodes', len(tree))
print('REGION: order=%s pairs=%s xbox=%s taubox=%s' % (bool(SPEC.get('order')), SPEC.get('pairs', []), SPEC.get('xbox', []), SPEC.get('taubox')))
print('disjunctions used', len(used), sorted(set(u.split(' ')[0] for u in used)))
print('demoted strict e-rows', DEMOTED[0]); print('ERRORS', errors, '=> CERTIFICATE VALID' if errors == 0 else '=> INVALID')
