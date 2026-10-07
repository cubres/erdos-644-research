"""gen_cert3: gen_cert2 (lazy exact B&B, same certificate format) + ONE-REQUEST Fano templates 'R' (linearised).

R template  'R <sh>:<k0><k1><k2>:<lab_1>,...,<lab_m>'
  sh in {1,2,3}: P = positions of ONE requested type f:  P1 = (0,), P2 = (0,1), P3 = (0,1,3) (a triangle);
  A = sorted complement of P, carrying the named roles lab_1..lab_m (m = 7 - |P|).
  For part i the BOUNDS are, in this order: for every Fano line l (LINES order) with n_l = |l cap P| >= 1 the
  expression (2x_i - sum_{q in l cap A} c_{lab q, i}) / n_l, then (4x_i - sum_{q in A} c_{lab q, i}) / |P|.
  k_i = 'x' (u_i := x_i) or a digit (u_i := bound number k_i).
  SUCCESS (all non-strict):  (a) every A-only line: sum_{q in l} c_{lab q, i} <= 2x_i;  (b) u_i <= every bound and
  u_i <= x_i;  (c) u_i >= 0;  (d) sum_i (x_i - u_i) <= tau.  Then the box u (0 <= u <= x) has cost <= tau* and
  contains a type f (R0), and f on P + the named rows on A is a Fano tuple (Lemma 7.63).
  FAILURE disjunction: one alternative per strictly violated row of (a)-(d), plus the void alternatives of every
  request role among the labels.
usage: python3 gen_cert3.py <strategy.json> <pi0> [fk=4] [rk=4] [menu=F,V,T3,R] [maxnodes=..] [stream=1] [tag=..]"""
import sys, json, itertools, time, os
from fractions import Fraction as F
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gen_cert as G
import gen_cert2 as G2

LINES = G.LINES
SHAPES = {1: (0,), 2: (0, 1), 3: (0, 1, 3)}


def shape_data(sh):
    P = SHAPES[sh]; A = [p for p in range(7) if p not in P]
    blines = [l for l in LINES if any(p in P for p in l)]
    alines = [l for l in LINES if not any(p in P for p in l)]
    return P, A, blines, alines


_RPAT = {}


def rpattern_reps(sh, k):
    """surjections A -> range(k) modulo the stabiliser of P in the Fano group (acting on A)"""
    key = (sh, k)
    if key in _RPAT: return _RPAT[key]
    P, A, _, _ = shape_data(sh)
    stab = [a for a in G.AUT if set(a[p] for p in P) == set(P)]
    pos = {q: i for i, q in enumerate(A)}
    seen = set(); reps = []
    for pat in itertools.product(range(k), repeat=len(A)):
        if len(set(pat)) != k or pat in seen: continue
        orb = set()
        for a in stab:
            # image assignment: point a[q] gets label pat[pos[q]]
            img = [None] * len(A)
            for q in A: img[pos[a[q]]] = pat[pos[q]]
            orb.add(tuple(img))
        seen |= orb; reps.append(pat)
    _RPAT[key] = reps
    return reps


def rt_rows(S, sh, ks, labs):
    """exact failure alternatives of R <sh>:<ks>:<labs> (list of frozensets of rows), without void alternatives"""
    P, A, blines, alines = shape_data(sh)
    lab = dict(zip(A, labs))
    alts = []
    us = []
    for i in range(3):
        xi = 'x%d' % i
        bounds = []
        for l in blines:
            n = sum(1 for p in l if p in P)
            d = {xi: F(2, n)}
            for q in l:
                if q not in P: d = G.lin(d, {S.c(lab[q], i): F(-1, n)})
            bounds.append(d)
        d = {xi: F(4, len(P))}
        for q in A: d = G.lin(d, {S.c(lab[q], i): F(-1, len(P))})
        bounds.append(d)
        u = {xi: F(1)} if ks[i] == 'x' else bounds[int(ks[i])]
        us.append(u)
        for l in alines:
            d = {xi: F(-2)}
            for q in l: d = G.lin(d, {S.c(lab[q], i): 1})
            alts.append(frozenset([G.row(d, 0, True)]))
        for b in bounds + [{xi: F(1)}]:
            d = G.lin(u, G.scale(b, -1))                       # u_i - b > 0
            d = {k: v for k, v in d.items() if v != 0}
            if d: alts.append(frozenset([G.row(d, 0, True)]))
        alts.append(frozenset([G.row(G.scale(u, -1), 0, True)]))        # u_i < 0
    d = {'tau': F(-1)}
    for i in range(3): d = G.lin(d, {'x%d' % i: 1}, G.scale(us[i], -1))
    alts.append(frozenset([G.row({k: v for k, v in d.items() if v != 0}, 0, True)]))   # cost(u) > tau
    return alts


def rt_eval(R, names, x, tau, rk, tol=1e-9, top=None):
    """numeric search: best (most robust) R templates over valid roles R (dict name -> vec).
    returns list of (margin, name) with margin <= tol, sorted (at most `top` if given, else the best one)."""
    out = []
    for sh in (1, 2, 3):
        P, A, blines, alines = shape_data(sh)
        nb = len(blines)
        for k in range(1, min(rk, len(A), len(names)) + 1):
            combos = list(itertools.combinations(names, k))
            Rc = np.array([[R[n] for n in cb] for cb in combos])           # (C,k,3)
            for pat in rpattern_reps(sh, k):
                Z = Rc[:, list(pat), :]                                       # (C,|A|,3) rows on A in order
                pos = {q: j for j, q in enumerate(A)}
                mg = np.full(len(combos), -np.inf)
                for l in alines:
                    s_ = Z[:, pos[l[0]]] + Z[:, pos[l[1]]] + Z[:, pos[l[2]]]
                    mg = np.maximum(mg, np.max(s_ - 2 * x, axis=1))
                B = []
                for l in blines:
                    n = sum(1 for p in l if p in P)
                    s_ = sum(Z[:, pos[q]] for q in l if q not in P)
                    B.append((2 * x - s_) / n)
                B.append((4 * x - Z.sum(1)) / len(P))
                B.append(np.broadcast_to(x, B[0].shape))                     # index nb+1 = 'x'
                B = np.stack(B, 0)                                           # (nb+2, C, 3)
                kk = np.argmin(B, axis=0)                                    # (C,3)
                u = np.min(B, axis=0)
                mg = np.maximum(mg, np.max(-u, axis=1))
                mg = np.maximum(mg, (x - u).sum(1) - tau)
                order = np.argsort(mg)
                for j in order[: (top or 1)]:
                    if mg[j] > tol: break
                    ks = ''.join('x' if kk[j, i] == nb + 1 else str(int(kk[j, i])) for i in range(3))
                    out.append((float(mg[j]), 'R %d:%s:%s' % (sh, ks, ','.join(combos[j][p] for p in pat))))
    out.sort()
    return out


TTFILE = '/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_two_part_gap_central/templates.json'
_TT = None


def load_tt():
    """the 42 two-type capacity functions: key -> list of efficient vertices (u, v) (Fractions); M_t(a,b) =
    max (u a + v b).  (Soundness of each record is re-verified by check_gen_cert3.py.)"""
    global _TT
    if _TT is None:
        d = json.load(open(TTFILE))
        _TT = {k: [(F(u), F(v)) for u, v in d[k]['record']['vertices']] for k in sorted(d, key=int)}
    return _TT


def w_rows(S, t, a, b):
    """failure alternatives of W t:a,b (two-type tuple of function t with rows a (colour 0) and b (colour 1)):
    some part i and efficient vertex (u,v) with u a_i + v b_i > x_i"""
    alts = []
    for i in range(3):
        for u, v in load_tt()[t]:
            alts.append(frozenset([G.row(G.lin({S.c(a, i): u}, {S.c(b, i): v}, {'x%d' % i: -1}), 0, True)]))
    return alts


def w_eval(R, names, x, tol=1e-9, top=1):
    TT = load_tt(); out = []
    if len(names) < 2: return out
    K = np.array([R[n] for n in names])
    for t, verts in TT.items():
        U = np.array([[float(u), float(v)] for u, v in verts])
        val = U[:, 0][:, None, None, None] * K[None, :, None, :] + U[:, 1][:, None, None, None] * K[None, None, :, :] - x
        m = val.max(axis=(0, 3)); np.fill_diagonal(m, np.inf)
        idx = np.argsort(m, axis=None)[:top]
        for f in idx:
            ia, ib = divmod(int(f), len(names))
            if m[ia, ib] <= tol: out.append((float(m[ia, ib]), 'W %s:%s,%s' % (t, names[ia], names[ib])))
    out.sort()
    return out


class Strategy3(G.Strategy):
    """+ role kind 'dmin' (separated mode): {"name":..,"kind":"dmin","cls":k,"dir":i}: the class-k type with the least
    c_i (exists: S_k closed, nonempty).  BASE: c_k >= sigma_k.  Disjunctions:
      'dm <d> <r>'  (every role r != d):  r_k < sigma_k (r not in S_k)  |  r_i >= d_i        [minimality]
      'dfree <d>'  :  d_i <= 0  |  (x_i - d_i) + (x_j - sigma_j) >= tau   [box c_i < d_i, c_j < sigma_j is free]"""
    def base(s):
        B = G.Strategy.base(s)
        for r in s.roles:
            if r['kind'] == 'dmin':
                assert s.mode == 'sep'
                k = r['cls']
                B.append(G.row({s.c(r['name'], k): 1, 's%d' % k: -1}, 0))
        return B

    def build_disj(s):
        G.Strategy.build_disj(s)
        D = s.D
        for d in s.roles:
            if d['kind'] != 'dmin': continue
            dn = d['name']; k = d['cls']; i = d['dir']; j = 3 - k - i
            D.pop('cls %s' % dn, None)                      # its class is known
            for r in s.roles:
                rn = r['name']
                if rn == dn: continue
                D['dm %s %s' % (dn, rn)] = [frozenset([G.row({'s%d' % k: 1, s.c(rn, k): -1}, 0, True)]),
                                            frozenset([G.row({s.c(rn, i): 1, s.c(dn, i): -1}, 0)])]
            D['dfree %s' % dn] = [frozenset([G.row({s.c(dn, i): -1}, 0)]),
                                  frozenset([G.row({'x%d' % i: 1, s.c(dn, i): -1, 'x%d' % j: 1, 's%d' % j: -1, 'tau': -1}, 0)])]


class Engine3(G2.Engine2):
    def __init__(s, S):
        G2.Engine2.__init__(s, S)
        s.isrole = np.array([True for nm in s.names])
    def cert(s, rows):
        """exact Motzkin certificate: first try to rationalise the float dual (fast), else gen_cert's exact path."""
        A, b, st = s.mat(rows)
        m = len(rows)
        from scipy.optimize import linprog
        res = linprog(-(b + st), A_ub=-b[None, :], b_ub=[0.0], A_eq=np.vstack([A.T, np.ones((1, m))]),
                      b_eq=np.concatenate([np.zeros(s.nv), [1.0]]), bounds=[(0, None)] * m, method='highs-ds')
        if res.status == 0 and -res.fun > 1e-12:
            lam = res.x
            for den in (60, 1000, 10 ** 5):
                sup = [r for r in range(m) if lam[r] > 1e-9]
                ls = [F(float(lam[r])).limit_denominator(den) for r in sup]
                rowsS = [rows[r] for r in sup]
                if all(l >= 0 for l in ls) and G.verify(rowsS, ls):
                    s.fastc = getattr(s, 'fastc', 0) + 1
                    return [(rowsS[k], ls[k]) for k in range(len(rowsS)) if ls[k] != 0]
        return G2.Engine2.cert(s, rows)

    def best_template(s, v, tol=1e-9):
        best = G2.Engine2.best_template(s, v, tol)
        if 'R' in s.S.menu:
            S = s.S
            x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]; tau = v[S.VI['tau']]
            valid = [nm for nm in S.names if not s.is_void(nm, v)]
            R = {nm: v[s.rv[nm]] for nm in valid}
            r = rt_eval(R, valid, x, tau, getattr(s, 'rk', 4), tol)
            if r and (best is None or r[0][0] < best[0]): best = r[0]
        if 'W' in s.S.menu:
            S = s.S
            x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]
            valid = [nm for nm in S.names if not s.is_void(nm, v)]
            R = {nm: v[s.rv[nm]] for nm in valid}
            r = w_eval(R, valid, x, tol)
            if r and (best is None or r[0][0] < best[0]): best = r[0]
        return best

    def top_templates(s, v, k=4, tol=1e-9):
        out = G2.Engine2.top_templates(s, v, k, tol)
        if 'R' in s.S.menu:
            S = s.S
            x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]; tau = v[S.VI['tau']]
            valid = [nm for nm in S.names if not s.is_void(nm, v)]
            R = {nm: v[s.rv[nm]] for nm in valid}
            r = rt_eval(R, valid, x, tau, getattr(s, 'rk', 4), tol, top=2)
            out = out + [nm for _, nm in r[:k]]
        if 'W' in s.S.menu:
            S = s.S
            x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]
            valid = [nm for nm in S.names if not s.is_void(nm, v)]
            R = {nm: v[s.rv[nm]] for nm in valid}
            r = w_eval(R, valid, x, tol)
            out = out + [nm for _, nm in r[:2]]
        return out

    def disj(s, nm):
        if nm.startswith('W '):
            if nm not in s.cache:
                t, ab = nm[2:].split(':'); a, b = ab.split(',')
                s.cache[nm] = G.dedup(w_rows(s.S, t, a, b) + s.S.tmpl_void([a, b]))
            return s.cache[nm]
        if nm.startswith('R '):
            if nm not in s.cache:
                sh, ks, labs = nm[2:].split(':'); labs = labs.split(',')
                s.cache[nm] = G.dedup(rt_rows(s.S, int(sh), ks, labs) + s.S.tmpl_void(labs))
            return s.cache[nm]
        return G2.Engine2.disj(s, nm)


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2])
    kw = dict(a.split('=') for a in sys.argv[3:])
    menu = tuple(kw.get('menu', 'F,V,T3,R,W').split(','))
    S = Strategy3(spec, pi0, fk=int(kw.get('fk', 4)), menu=menu, lazy=True)
    E = Engine3(S); E.heur = kw.get('heur', 'robust'); E.strong = int(kw.get('strong', 0)); E.rk = int(kw.get('rk', 4))
    base = kw.get('tag', sys.argv[1].split('/')[-1].replace('.json', ''))
    tagp = str(pi0).replace('/', '_')
    outdir = kw.get('outdir', os.path.join(HERE, 'certs'))
    os.makedirs(outdir, exist_ok=True)
    stream_fn = None
    if kw.get('stream', '1') == '1':
        import gzip
        stream_fn = os.path.join(outdir, 'gcert3_%s_%s.jsonl.gz' % (base, tagp))
        E.stream = gzip.open(stream_fn + '.part', 'wt')
        E.stream.write(json.dumps({'pi0': str(pi0), 'strategy': spec, 'fk': S.fk, 'rk': E.rk, 'menu': list(S.menu),
                                   'format': 'jsonl-v1'}) + '\n')
    print('strategy', base, 'roles', S.names, 'pi0', pi0, 'menu', menu, 'fk', S.fk, 'rk', E.rk, flush=True)
    t0 = time.time()
    st, a, b = E.run(maxnodes=int(kw.get('maxnodes', 10 ** 7)))
    print(st, '(%.0fs)' % (time.time() - t0), flush=True)
    if stream_fn is not None: E.stream.close()
    if st == 'CERTIFIED':
        if stream_fn is not None:
            os.rename(stream_fn + '.part', stream_fn)
            print('leaves', getattr(E, 'nleaves', 0), 'nodes', b, '->', stream_fn)
    elif st == 'ADVERSARY':
        beta, v = b
        print('path', a)
        print('beta %.6g' % beta, {k: round(float(x), 5) for k, x in zip(S.VARS, v)})
        json.dump({'path': a, 'v': dict(zip(S.VARS, map(float, v))), 'beta': beta},
                  open(os.path.join(outdir, 'gadv3_%s_%s.json' % (base, tagp)), 'w'))
    else:
        print(a)
