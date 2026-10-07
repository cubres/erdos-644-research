#!/usr/bin/env python3
"""wref8: independent exact checks of Theorem 8.4 (one-sided box families).
  (1) exact vertex enumeration of D (with and without the cut sum(theta)+x_L>=1), product-vertex test;
  (2) template T(A,B,C) feasibility (general, non-symmetrised rows) at every vertex, in two independent
      encodings: (i) Lemma 7.63 per-part inequalities, (ii) explicit Fano cell masses c[part][point];
  (3) random rational points of D and near-boundary/degenerate points;
  (4) full unmerged random families over p parts with |I|>=3, tau*>=3/4, EVERY ordered triple (A,B,C) of I.
Fractions only; LP = wref8_exactlp (witnesses re-verified, infeasibility via verified Farkas vector)."""
import itertools, random, sys
from fractions import Fraction as F
from wref8_exactlp import feasible

LINES = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
P0 = 0
PENCIL = [l for l in range(7) if P0 in LINES[l]]            # 3 lines through p
QUAD = [l for l in range(7) if P0 not in LINES[l]]           # 4 lines missing p
assert len(PENCIL) == 3 and len(QUAD) == 4

def template_rows(A, B, C):
    box = [None] * 7
    for l in QUAD: box[l] = A
    box[PENCIL[0]] = B; box[PENCIL[1]] = B; box[PENCIL[2]] = C
    return box

def build(x, theta, box, cells=False):
    """rows l=0..6 with box part box[l] (None = unconstrained). parts i with capacity x[i]."""
    p = len(x)
    var = lambda l, i: l * p + i
    nv = 7 * p + (7 * p if cells else 0)
    cvar = lambda i, q: 7 * p + i * 7 + q
    ub, eq = [], []
    lb = [F(0)] * nv
    ubv = [None] * nv
    for l in range(7):
        eq.append(({var(l, i): 1 for i in range(p)}, F(1)))
        for i in range(p): ubv[var(l, i)] = x[i]
        if box[l] is not None: lb[var(l, box[l])] = theta[box[l]]
    for i in range(p):
        if cells:
            ub.append(({cvar(i, q): 1 for q in range(7)}, x[i]))
            for l in range(7):
                d = {var(l, i): 1}
                for q in range(7):
                    if q not in LINES[l]: d[cvar(i, q)] = -1
                ub.append((d, F(0)))
        else:
            for q in range(7):
                ub.append(({var(l, i): 1 for l in range(7) if q in LINES[l]}, 2 * x[i]))
            ub.append(({var(l, i): 1 for l in range(7)}, 4 * x[i]))
    for j in range(nv):
        if ubv[j] is not None and lb[j] > ubv[j]:
            return None  # trivially infeasible bounds
    return nv, ub, eq, lb, ubv

def tmpl_feasible(x, theta, box, cells=False):
    b = build(x, theta, box, cells)
    if b is None: return 'INFEAS'
    return feasible(*b)[0]

# ---------------- (1) domain vertices ----------------
# coordinates (xA,tA,xB,tB,xC,tC,xL);  constraints as (vec, c): vec.z + c >= 0
def dom_constraints(with_h1=True):
    cons = []
    for k in range(3):
        xi, ti = 2 * k, 2 * k + 1
        v = [F(0)] * 7; v[ti] = F(1); v[xi] = F(-4, 7); cons.append((v, F(0)))   # theta >= 4x/7
        v = [F(0)] * 7; v[xi] = F(1); v[ti] = F(-1); cons.append((v, F(0)))      # theta <= x
        v = [F(0)] * 7; v[ti] = F(-1); cons.append((v, F(1)))                    # theta <= 1
    v = [F(0)] * 7; v[6] = F(1); cons.append((v, F(0)))
    v = [F(0)] * 7; v[6] = F(-1); cons.append((v, F(7, 4)))
    if with_h1:
        v = [F(0)] * 7; v[1] = v[3] = v[5] = F(1); v[6] = F(1); cons.append((v, F(-1)))
    v = [F(0)] * 7
    for k in range(3): v[2 * k] = F(1); v[2 * k + 1] = F(-1)
    v[6] = F(3, 7); cons.append((v, F(-3, 4)))
    return cons

def solve_eq(rows):
    n = 7
    M = [list(a) + [-c] for a, c in rows]
    r = 0
    for col in range(n):
        pr = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if pr is None: return None
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return [M[i][n] for i in range(n)]

def vertices(cons):
    vs = set()
    for S in itertools.combinations(range(len(cons)), 7):
        s = solve_eq([cons[i] for i in S])
        if s is None: continue
        if all(sum(a * z for a, z in zip(v, s)) + c >= 0 for v, c in cons): vs.add(tuple(s))
    return sorted(vs)

TRI = [(F(0), F(0)), (F(1), F(1)), (F(7, 4), F(1))]
PRODUCT = set()
for a in TRI:
    for b in TRI:
        for c in TRI:
            for xl in (F(0), F(7, 4)):
                PRODUCT.add((a[0], a[1], b[0], b[1], c[0], c[1], xl))

def in_D(z, with_h1=True):
    return all(sum(a * w for a, w in zip(v, z)) + c >= 0 for v, c in dom_constraints(with_h1))

def merged_instance(z):
    x = [z[0], z[2], z[4], z[6]]
    th = [z[1], z[3], z[5], F(0)]
    return x, th

def host_rule_witness(z):
    """Step-5 hand rule: tight/Fano boxes keep their own rows; empty-box rows go to one host."""
    x, th = merged_instance(z)
    kind = []
    for k in range(3):
        kind.append({(F(0), F(0)): 'E', (F(1), F(1)): 'T', (F(7, 4), F(1)): 'F'}[(x[k], th[k])])
    hosts = [k for k in range(3) if kind[k] == 'F'] + ([3] if x[3] == F(7, 4) else [])
    if not hosts: return None
    h = hosts[0]
    box = template_rows(0, 1, 2)
    pt = [[F(0)] * 4 for _ in range(7)]
    for l in range(7):
        k = box[l]
        pt[l][k if kind[k] != 'E' else h] = F(1)
    # verify Lemma 7.63 criterion
    for i in range(4):
        for l in range(7):
            if pt[l][i] > x[i]: return False
        for q in range(7):
            if sum(pt[l][i] for l in range(7) if q in LINES[l]) > 2 * x[i]: return False
        if sum(pt[l][i] for l in range(7)) > 4 * x[i]: return False
    for l in range(7):
        if pt[l][box[l]] < th[box[l]]: return False
    return True

def part1():
    for h1 in (True, False):
        vs = vertices(dom_constraints(h1))
        nonprod = [v for v in vs if v not in PRODUCT]
        print(f'[1] D (with H1={h1}): {len(vs)} vertices; non-product: {len(nonprod)}')
    prodD = [v for v in PRODUCT if in_D(v)]
    print(f'[1] product vertices lying in D: {len(prodD)} (of {len(PRODUCT)})')
    return vertices(dom_constraints(True))

def part2(vs):
    bad = 0
    for z in vs:
        x, th = merged_instance(z)
        box = template_rows(0, 1, 2)
        r1 = tmpl_feasible(x, th, box, cells=False)
        r2 = tmpl_feasible(x, th, box, cells=True)
        hw = host_rule_witness(z)
        if r1 != 'FEAS' or r2 != 'FEAS' or hw is not True:
            bad += 1; print('   vertex problem', [str(t) for t in z], r1, r2, hw)
    print(f'[2] vertices: {len(vs)} checked, problems {bad}')

def rand_frac(rng, lo, hi, den=None):
    den = den or rng.choice([7, 8, 12, 20, 28, 35, 56, 97, 101, 1000])
    a = int(lo * den); b = int(hi * den)
    return F(rng.randint(a, b), den) if b >= a else F(lo)

def part3(N, seed):
    rng = random.Random(seed)
    cnt = 0; fails = 0; mismatch = 0
    while cnt < N:
        z = []
        for k in range(3):
            mode = rng.random()
            if mode < 0.15:
                xk = F(0); tk = F(0)
            else:
                xk = rand_frac(rng, 0, 7 / 4)
                lo = F(4, 7) * xk; hi = min(xk, F(1))
                if lo > hi: continue_flag = True; xk = hi = F(7, 4); lo = F(1)
                r = rng.random()
                if r < 0.2: tk = lo                      # theta = 4x/7 (boundary)
                elif r < 0.3: tk = lo + F(1, 10 ** 6) if lo + F(1, 10 ** 6) <= hi else hi
                elif r < 0.4: tk = hi
                else: tk = lo + (hi - lo) * rand_frac(rng, 0, 1)
            z += [xk, tk]
        r = rng.random()
        if r < 0.2: xl = F(7, 4)
        elif r < 0.3: xl = F(7, 4) - F(1, 10 ** 6)
        elif r < 0.4: xl = F(0)
        else: xl = rand_frac(rng, 0, 7 / 4)
        z.append(xl)
        if not in_D(z): continue
        cnt += 1
        x, th = merged_instance(z)
        box = template_rows(0, 1, 2)
        r1 = tmpl_feasible(x, th, box)
        if cnt <= N // 4:
            r2 = tmpl_feasible(x, th, box, cells=True)
            if r2 != r1: mismatch += 1; print('   encodings disagree', [str(t) for t in z], r1, r2)
        if r1 != 'FEAS':
            fails += 1; print('   TEMPLATE FAILS in D', [str(t) for t in z])
    print(f'[3] random points of D: {N}, template infeasible: {fails}, encoding mismatches: {mismatch}')

def tau_star(x, th, I):
    """one-sided boxes; th are effective thresholds; I nonempty boxes."""
    X = sum(x)
    s = sum(th[i] for i in I) + sum(x[j] for j in range(len(x)) if j not in I)
    return X - max(F(1), s)

def part4(N, seed, pmin=3, pmax=6, plow=0.15):
    rng = random.Random(seed)
    stats = dict(inst=0, hom=0, nonhom=0, triples=0, fail=0)
    while stats['inst'] < N:
        p = rng.randint(pmin, pmax)
        x = [rand_frac(rng, 0.02, 1.8) for _ in range(p)]
        if rng.random() < 0.2: x[rng.randrange(p)] = F(1, 1000)             # tiny part
        k = rng.randint(3, p)
        I = sorted(rng.sample(range(p), k))
        th_raw = [F(0)] * p
        for i in I:
            lo = F(4, 7) * x[i]
            hi = min(x[i], F(1))
            if rng.random() < plow: th_raw[i] = rand_frac(rng, 0, float(lo))  # includes low / homogeneous
            else: th_raw[i] = lo + (hi - lo) * rand_frac(rng, 0, 1) if hi >= lo else hi
        X = sum(x)
        th = [max(th_raw[i], 1 - X + x[i]) if i in I else F(0) for i in range(p)]
        I = [i for i in I if th[i] <= min(x[i], F(1))]
        if len(I) < 3: continue
        ts = tau_star(x, th, I)
        if ts < F(3, 4): continue
        stats['inst'] += 1
        hom = any(th[i] <= F(4, 7) * x[i] for i in I) or sum(th[i] for i in I) + sum(x[j] for j in range(p) if j not in I) < 1
        if hom:
            stats['hom'] += 1
            # step 1: exhibit a <= 4x/7 in C and check homogeneous Fano (7 equal rows) exactly
            box = [None] * 7
            iwit = next((i for i in I if th[i] <= F(4, 7) * x[i]), None)
            box = [iwit] * 7
            xs = [F(4, 7) * xi for xi in x]
            r = feasible(*build(x, th, box)) if iwit is not None else feasible(*build(x, th, [None] * 7))
            if r[0] != 'FEAS': stats['fail'] += 1; print('   HOMOGENEOUS FAILS', x, th, I)
            continue
        stats['nonhom'] += 1
        for A, B, C in itertools.permutations(I, 3):
            stats['triples'] += 1
            r = tmpl_feasible(x, th, template_rows(A, B, C))
            if r != 'FEAS':
                stats['fail'] += 1
                print('   TEMPLATE FAILS', [str(v) for v in x], [str(v) for v in th], I, (A, B, C), 'tau*', ts)
    print('[4]', stats)

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'vert':
        vs = part1(); part2(vs)
    elif what == 'rand':
        part3(int(sys.argv[2]), int(sys.argv[3]))
    elif what == 'full':
        part4(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv)>4 else 3,
              int(sys.argv[5]) if len(sys.argv)>5 else 6, float(sys.argv[6]) if len(sys.argv)>6 else 0.15)
