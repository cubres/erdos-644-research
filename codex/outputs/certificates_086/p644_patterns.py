"""Erdős #644, pattern families.

A pattern family: ground set split into parts of sizes x[0..p-1]; an r-set A is an edge iff its
intersection vector a = (|A ∩ X_0|, ..., |A ∩ X_{p-1}|) is admissible. Admissibility here:
  * box:  lo[i] <= a[i] <= hi[i]   (lo/hi may be None)
  * lin:  list of (coeffs, rhs) meaning sum_i coeffs[i]*a[i] <= rhs
  * cong: list of (i, mod, res)     meaning a[i] ≡ res (mod mod)

tau_pattern : exact transversal number via edge-free type vectors (up-set DP).
venn_milp   : does a NON-2-pierceable family of at most 7 edges exist?  Variables n[i][c] =
              number of points of part i lying in exactly the edges c ⊆ {0..6}.  A point in cell c
              covers the edges in c; the 7-tuple is 2-pierceable iff two nonempty cells c, c' have
              c ∪ c' = {0..6}.  Feasible  <=>  the family FAILS the (7,2)-property.
              With m=None and proportional data, n is continuous: a rational bad 7-tuple scales to
              an integer one, so infeasibility certifies (7,2) for every scale.
"""
import itertools, math, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

EDGES = range(7)
CELLS = [c for s in range(1, 7) for c in itertools.combinations(EDGES, s)]   # nonempty proper subsets, 126
CELL_ID = {c: i for i, c in enumerate(CELLS)}
COVER_PAIRS = [(i, j) for i, c in enumerate(CELLS) for j, d in enumerate(CELLS) if i < j and len(set(c) | set(d)) == 7]


class Pattern:
    def __init__(self, x, r, lo=None, hi=None, lin=(), cong=(), name='', boxes=None):
        self.x = list(x); self.p = len(x); self.r = r
        self.lo = list(lo) if lo else [0] * self.p
        self.hi = list(hi) if hi else [None] * self.p
        self.boxes = [tuple(b) for b in boxes] if boxes else [(tuple(self.lo), tuple(self.hi))]
        self.lo, self.hi = list(self.boxes[0][0]), list(self.boxes[0][1])
        self.lin = list(lin); self.cong = list(cong); self.name = name

    def in_box(self, a, box):
        lo, hi = box
        return all(a[i] >= lo[i] and (hi[i] is None or a[i] <= hi[i]) for i in range(self.p))

    def admissible(self, a):
        if sum(a) != self.r: return False
        if not any(self.in_box(a, b) for b in self.boxes): return False
        for i in range(self.p):
            if a[i] > self.x[i] or a[i] < 0: return False
        for coeffs, rhs in self.lin:
            if sum(c * v for c, v in zip(coeffs, a)) > rhs: return False
        for i, mod, res in self.cong:
            if a[i] % mod != res % mod: return False
        return True

    def admissible_vectors(self):
        rngs = [range(0, min(xi, self.r) + 1) for xi in self.x]
        return [a for a in itertools.product(*rngs) if self.admissible(a)]

    def scaled(self, m):
        """Proportional data given per unit; return an integer instance at scale m."""
        sb = [([int(math.ceil(v * m - 1e-9)) for v in lo], [None if v is None else int(math.floor(v * m + 1e-9)) for v in hi]) for lo, hi in self.boxes]
        return Pattern([int(round(v * m)) for v in self.x], int(round(self.r * m)),
                       lin=[(c, rhs * m) for c, rhs in self.lin], cong=self.cong, name=self.name, boxes=sb)


def tau_pattern(pat):
    """Exact tau of an integer pattern family (0 if the family is empty)."""
    adm = pat.admissible_vectors()
    if not adm: return 0
    shape = tuple(xi + 1 for xi in pat.x)
    dom = np.zeros(shape, dtype=bool)
    for a in adm: dom[tuple(a)] = True
    # propagate: u dominates some admissible a  (up-set closure)
    for i in range(pat.p):
        dom = np.logical_or.accumulate(dom, axis=i)
    idx = np.indices(shape).sum(axis=0)
    free = ~dom
    best = idx[free].max() if free.any() else -1
    return sum(pat.x) - best


def trace_tau(pat, e):
    """Min transversal size inside an edge with intersection vector e (traces): min |T|, T <= e,
    such that x - T is edge-free... i.e. every edge meets T.  Computed by brute force over t <= e."""
    adm = pat.admissible_vectors()
    shape = tuple(xi + 1 for xi in pat.x)
    dom = np.zeros(shape, dtype=bool)
    for a in adm: dom[tuple(a)] = True
    for i in range(pat.p): dom = np.logical_or.accumulate(dom, axis=i)
    best = None
    for t in itertools.product(*[range(ei + 1) for ei in e]):
        u = tuple(xi - ti for xi, ti in zip(pat.x, t))
        if not dom[u]:  # x - t is edge-free  => t is a transversal
            s = sum(t)
            if best is None or s < best: best = s
    return best


FANO_LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
FANO_CELLS = [CELL_ID[tuple(sorted(set(EDGES) - set(L)))] for L in FANO_LINES]


def venn_milp(pat, m=None, want_solution=False, forced_cells=None, time_limit=120,
              intersecting=None, symbreak=True, extra_options=None):
    """Search for a non-2-pierceable family of <=7 edges of the pattern family.
    m=None: continuous n (pattern data are per-unit proportions).  m=int: integer n, data scaled.
    Returns (status, info) with status in {'FAILS' (bad tuple found), 'HAS' (proved none), 'UNKNOWN'}.
    intersecting: if True (auto: total size < 2r) a point in >=5 edges is impossible in a bad tuple
    (the other <=2 edges meet), so cells with |c|>=5 are zeroed.  symbreak: edges sorted by |A∩X_0|."""
    P = pat if m is None else pat.scaled(m)
    p, r, nc = P.p, P.r, len(CELLS)
    tot = sum(P.x)
    if intersecting is None: intersecting = tot < 2 * r
    nN = p * nc; nZ = nc
    congs = list(P.cong); nQ = 7 * len(congs)
    nB = len(P.boxes); nBox = 7 * nB if nB > 1 else 0
    nvar = nN + nZ + nQ + nBox
    integrality = np.zeros(nvar)
    if m is not None: integrality[:nN] = 1
    integrality[nN:nN + nZ] = 1; integrality[nN + nZ:] = 1
    BIG = float(sum(P.x)) + 1.0
    lb = np.zeros(nvar); ub = np.full(nvar, np.inf); ub[nN:nN + nZ] = 1
    if nBox: ub[nN + nZ + nQ:] = 1
    for c in range(nc):
        if forced_cells is not None and c not in forced_cells: ub[nN + c] = 0
        if intersecting and len(CELLS[c]) >= 5: ub[nN + c] = 0
        if ub[nN + c] == 0:
            for i in range(p): ub[i * nc + c] = 0
    rows, lbs, ubs = [], [], []
    def add(coefs, lo, hi):
        row = np.zeros(nvar)
        for j, v in coefs: row[j] += v
        rows.append(row); lbs.append(lo); ubs.append(hi)
    for c in range(nc):
        add([(i * nc + c, 1.0) for i in range(p)] + [(nN + c, -float(tot))], -np.inf, 0)
    for (c, d) in COVER_PAIRS:
        if ub[nN + c] > 0 and ub[nN + d] > 0: add([(nN + c, 1.0), (nN + d, 1.0)], -np.inf, 1)
    for i in range(p):
        add([(i * nc + c, 1.0) for c in range(nc)], -np.inf, P.x[i])
    aji_coefs = {}
    for j in EDGES:
        cells_j = [c for c in range(nc) if j in CELLS[c]]
        add([(i * nc + c, 1.0) for i in range(p) for c in cells_j], r, r)
        for i in range(p):
            aji = [(i * nc + c, 1.0) for c in cells_j]; aji_coefs[(j, i)] = aji
            if nB == 1:
                lo = P.lo[i]; hi = P.hi[i] if P.hi[i] is not None else np.inf
                add(aji, lo, hi)
        if nB > 1:
            bvars = [nN + nZ + nQ + j * nB + b for b in range(nB)]
            add([(v, 1.0) for v in bvars], 1, 1)
            for b, (lo, hi) in enumerate(P.boxes):
                for i in range(p):
                    # a_ji >= lo_i - BIG*(1-b) ;  a_ji <= hi_i + BIG*(1-b)
                    add(aji_coefs[(j, i)] + [(bvars[b], -BIG)], lo[i] - BIG, np.inf)
                    if hi[i] is not None: add(aji_coefs[(j, i)] + [(bvars[b], BIG)], -np.inf, hi[i] + BIG)
        for coeffs, rhs in P.lin:
            add([(i * nc + c, coeffs[i]) for i in range(p) for c in cells_j if coeffs[i] != 0], -np.inf, rhs)
        for qi, (i, mod, res) in enumerate(congs):
            add([(i * nc + c, 1.0) for c in cells_j] + [(nN + nZ + j * len(congs) + qi, -float(mod))], res, res)
    if symbreak and p >= 2:
        for j in range(6):   # a_{j,0} <= a_{j+1,0}
            add(aji_coefs[(j, 0)] + [(v, -w) for v, w in aji_coefs[(j + 1, 0)]], -np.inf, 0)
    A = np.array(rows); cons = LinearConstraint(A, np.array(lbs), np.array(ubs))
    res = milp(c=np.zeros(nvar), constraints=cons, integrality=integrality, bounds=Bounds(lb, ub),
               options=dict({'time_limit': time_limit, 'disp': False}, **(extra_options or {})))
    if res.status == 0 and res.x is not None: status = 'FAILS'
    elif res.status == 2: status = 'HAS'
    else: status = 'UNKNOWN'
    info = {'scipy_status': res.status, 'message': res.message}
    if status == 'FAILS' and want_solution:
        xsol = res.x
        info['cells'] = [(CELLS[c], [round(float(xsol[i * nc + c]), 4) for i in range(p)]) for c in range(nc)
                         if xsol[nN + c] > 0.5 and sum(xsol[i * nc + c] for i in range(p)) > 1e-7]
    return status, info


def check_72(pat, m=None, time_limit=120, **kw):
    """Fano prefilter (LP with only the 7 Fano-complement cells) then full MILP."""
    st, info = venn_milp(pat, m=m, forced_cells=set(FANO_CELLS), time_limit=30, **kw)
    if st == 'FAILS': return 'FAILS', dict(info, via='fano')
    st2, info2 = venn_milp(pat, m=m, time_limit=time_limit, **kw)
    return st2, dict(info2, via='full')


# ---------- convenience constructors ----------
def complete(N, r):
    return Pattern([N], r, name=f'K_{N}^({r})')

def parity(m):
    """FKW 1999: 4m-subsets of a (7m+1)-set with odd intersection with a fixed 4m-set."""
    return Pattern([4 * m, 3 * m + 1], 4 * m, cong=[(0, 2, 1)], name=f'FKW-odd m={m}')

def two_part(xi, zeta, alpha, beta, rho=1.0):
    """Proportional: |X|=xi, |Z|=zeta, edges of size rho with |A∩X| in [alpha, beta] (units of m)."""
    return Pattern([xi, zeta], rho, lo=[alpha, 0], hi=[beta, None], name=f'2part xi={xi} zeta={zeta} a∈[{alpha},{beta}]')

def two_part_tau_ratio(xi, zeta, alpha, beta):
    """tau/r for the proportional 2-part family, closed form (edge size 1)."""
    free = max(min(alpha, xi) + zeta if alpha > 0 else -1, xi + (1 - beta) if beta < 1 else -1, 1.0)
    free = min(free, xi + zeta)
    return xi + zeta - free


def enum_two_part(D, tl=60, min_ratio=None, log=None):
    """Enumerate proportional 2-part patterns on the grid 1/D; keep tau/r >= 3/4 + 1/D; check (7,2)."""
    if min_ratio is None: min_ratio = 0.75 + 1.0 / D
    m = 2 * D; survivors = []; tested = 0
    grid = [i / D for i in range(0, 2 * D + 1)]
    for xi in grid:
        if xi <= 0: continue
        for zeta in grid:
            if xi + zeta <= 1: continue
            for ia in range(0, D + 1):
                for ib in range(ia, D + 1):
                    alpha, beta = ia / D, ib / D
                    if alpha > xi: continue
                    P = two_part(xi, zeta, alpha, beta)
                    Pm = P.scaled(m); tau = tau_pattern(Pm)
                    if tau < min_ratio * m - 1e-9: continue
                    tested += 1
                    st, info = check_72(P, m=None, time_limit=tl)
                    line = f"xi={xi} zeta={zeta} a in [{alpha},{beta}] tau/r={tau/m:.4f}: {st} via {info.get('via')}"
                    if log: log.write(line + '\n'); log.flush()
                    if st != 'FAILS': survivors.append((xi, zeta, alpha, beta, tau / m, st)); print('  SURVIVOR', line, flush=True)
    print(f"enum2 D={D}: tested {tested} patterns with tau/r >= {min_ratio:.3f}; survivors (HAS or UNKNOWN): {len(survivors)}", flush=True)
    return survivors


def three_part(x, boxes):
    return Pattern(list(x), 1.0, boxes=boxes, name=f'3part x={x} boxes={boxes}')

def enum_three_part(D, tl=60, min_ratio=0.77, log=None, max_size=2.0):
    m = 2 * D; survivors = []; tested = 0; t0 = time.time()
    grid = [i / D for i in range(1, int(max_size * D) + 1)]
    ivals = [(a / D, b / D) for a in range(0, D + 1) for b in range(a, D + 1)]
    for x1 in grid:
        for x2 in grid:
            if x2 > x1: continue
            for x3 in grid:
                if x3 > x2 or x1 + x2 + x3 <= 1: continue
                for (a1, b1) in ivals:
                    if a1 > x1: continue
                    for (a2, b2) in ivals:
                        if a2 > x2: continue
                        P = Pattern([x1, x2, x3], 1.0, boxes=[((a1, a2, 0.0), (b1, b2, None))], name=f'3part')
                        tau = tau_pattern(P.scaled(m))
                        if tau < min_ratio * m - 1e-9: continue
                        tested += 1
                        st, info = check_72(P, m=None, time_limit=tl)
                        line = f"x=({x1},{x2},{x3}) a1 in [{a1},{b1}] a2 in [{a2},{b2}] tau/r={tau/m:.4f}: {st} via {info.get('via')}"
                        if log: log.write(line + '\n'); log.flush()
                        if st != 'FAILS': survivors.append(line); print('  SURVIVOR', line, flush=True)
        print(f"  x1={x1} done: tested {tested}, survivors {len(survivors)} [{time.time()-t0:.0f}s]", flush=True)
    print(f"enum3 D={D}: tested {tested}; survivors: {len(survivors)}", flush=True)
    return survivors

def enum_union(D, tl=60, min_ratio=0.77, log=None):
    """2 parts, admissible |A∩X| in [a1,b1] ∪ [a2,b2]."""
    m = 2 * D; survivors = []; tested = 0; t0 = time.time()
    grid = [i / D for i in range(1, 2 * D + 1)]
    ivals = [(a / D, b / D) for a in range(0, D + 1) for b in range(a, D + 1)]
    for xi in grid:
        for zeta in grid:
            if xi + zeta <= 1: continue
            for i1, (a1, b1) in enumerate(ivals):
                for (a2, b2) in ivals[i1 + 1:]:
                    if b1 >= a2 - 1e-12: continue   # disjoint, ordered
                    P = Pattern([xi, zeta], 1.0, boxes=[((a1, 0.0), (b1, None)), ((a2, 0.0), (b2, None))], name='union')
                    tau = tau_pattern(P.scaled(m))
                    if tau < min_ratio * m - 1e-9: continue
                    tested += 1
                    st, info = check_72(P, m=None, time_limit=tl)
                    line = f"xi={xi} zeta={zeta} a in [{a1},{b1}]∪[{a2},{b2}] tau/r={tau/m:.4f}: {st} via {info.get('via')}"
                    if log: log.write(line + '\n'); log.flush()
                    if st != 'FAILS': survivors.append(line); print('  SURVIVOR', line, flush=True)
    print(f"enumU D={D}: tested {tested}; survivors: {len(survivors)}", flush=True)
    return survivors


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if mode == 'enum3':
        D = int(sys.argv[2]); tl = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        mr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.77
        with open(f'logs/enum3_D{D}.log', 'a') as lg: enum_three_part(D, tl=tl, min_ratio=mr, log=lg)
        sys.exit(0)
    if mode == 'enumU':
        D = int(sys.argv[2]); tl = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        mr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.77
        with open(f'logs/enumU_D{D}.log', 'a') as lg: enum_union(D, tl=tl, min_ratio=mr, log=lg)
        sys.exit(0)
    TL = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    if mode == 'parity':
        m = int(sys.argv[2]); P = parity(m); t0 = time.time()
        st, info = venn_milp(P, m=1, want_solution=True, time_limit=TL)
        print(f"parity m={m} r={4*m} |S|={7*m+1}: tau={tau_pattern(P)} {st} scipy_status={info['scipy_status']} msg={info['message']} [{time.time()-t0:.0f}s]", flush=True)
        if st == 'FAILS': print('  cells:', info.get('cells'))
        sys.exit(0)
    if mode == 'enum2':
        D = int(sys.argv[2]); tl = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        mr = float(sys.argv[4]) if len(sys.argv) > 4 else None
        with open(f'logs/enum2_D{D}.log', 'a') as lg: enum_two_part(D, tl=tl, min_ratio=mr, log=lg)
        sys.exit(0)
    # ---- mandatory cross-checks ----
    t0 = time.time()
    print("== complete hypergraphs (feasible <=> fails (7,2)) ==")
    for r in (8, 12):
        for N in (math.ceil(7 * r / 4) - 1, math.ceil(7 * r / 4), math.ceil(7 * r / 4) + 1):
            st, _ = venn_milp(complete(N, r), m=1)
            print(f"  r={r} N={N}: {st}   tau={tau_pattern(complete(N, r))}   expected {'FAILS' if N >= 7*r/4 else 'HAS'}")
    print("== FKW parity family, tau=3m+1, (7,2) known for m>=4, fails at m=2 ==")
    for m in (2, 3, 4, 5, 6):
        P = parity(m); st, info = venn_milp(P, m=1, want_solution=True, time_limit=TL)
        print(f"  m={m} r={4*m} |S|={7*m+1}: tau={tau_pattern(P)}  {st} ({info['message'][:40]})  [{time.time()-t0:.1f}s]", flush=True)
        if st == 'FAILS' and 'cells' in info:
            print("     bad 7-tuple cells (edges containing cell, counts per part):", info['cells'][:12])
    print("== tau cross-check vs p644_restricted.tau_restricted ==")
    try:
        from p644_restricted import tau_restricted
        for (nS, x, r, R) in [(15, 8, 8, {1, 3, 5, 7}), (13, 5, 8, {2, 3, 4}), (14, 6, 8, {0, 1, 2})]:
            P = Pattern([x, nS - x], r, name='chk')
            P.admissible = (lambda a, R=R, r=r, x=x, nS=nS: sum(a) == r and a[0] in R and a[0] <= x and a[1] <= nS - x)
            print(f"  |S|={nS} |X|={x} r={r} R={sorted(R)}: tau_pattern={tau_pattern(P)} tau_restricted={tau_restricted(nS, x, r, R)}")
    except Exception as e:
        print("  (cross-check skipped:", e, ")")
