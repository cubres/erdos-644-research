"""Referee w9, claim core#5: W(x,s) two-part two-type family.
Parts P,Q of capacity x (rank normalised to 1); types a=(s,1-s), b=(1-s,s).
Independent exact checks (Fractions unless stated):
 A. tau*: note Thm 7.71 formula vs attacker's min(x-s,2x-2+2s); discrete blow-up tau by enumeration.
 B. Fano: all 128 line->type assignments; per-part min mass by (i) own LP (HiGHS, float) and (ii) note Lemma 7.63
    closed form; hand certificate = monochromatic concurrent triple; threshold F(s)=min_A max_parts M = 3(1-s)/2.
 C. GT* (continuum good-triple unions), degree-4 rule, nu<=2, over whole claimed parameter region.
 D. Tetrahedral support (note Lemma 7.70): explicit INTEGER bad 7-tuple in the discrete blow-up, brute-force
    verified to have no 2-transversal.
 E. Which of the note's 42 certified two-type functions kill W (is tetrahedral the only one?).
"""
import itertools
from fractions import Fraction as F
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LINES = [frozenset(l) for l in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
# sanity: Fano
assert all(len(LINES[i] & LINES[j]) == 1 for i in range(7) for j in range(i+1, 7))

def types(s):
    return {'a': (s, 1-s), 'b': (1-s, s)}

# ---------------- A. tau* ----------------
def tau_star_thm771(x, s):
    a, b = types(s)['a'], types(s)['b']
    X = (x, x); best = None
    for i in range(2):
        if a[i] <= 0: continue
        for j in range(2):
            if b[j] <= 0: continue
            v = X[i] - min(a[i], b[i]) if i == j else X[i]-a[i]+X[j]-b[j]
            best = v if best is None else min(best, v)
    return best

def tau_discrete(n, aP, aQ):
    # edges: all sets with (aP,aQ) or (aQ,aP) points in (P,Q), parts of size n.
    best = None
    for tP in range(n+1):
        for tQ in range(n+1):
            ok = all((tP > n-u) or (tQ > n-v) for (u, v) in ((aP, aQ), (aQ, aP)))
            if ok and (best is None or tP+tQ < best): best = tP+tQ
    return best

# ---------------- B. Fano ----------------
def lp_min_mass(loads):
    # labels p (Fano points); a vertex labelled p may lie in rows l with p notin l.
    M = [[0 if p in LINES[l] else 1 for p in range(7)] for l in range(7)]
    r = linprog([1]*7, A_ub=[[-v for v in row] for row in M], b_ub=[-float(v) for v in loads],
                bounds=(0, None), method='highs')
    return r.fun

CONC = [frozenset(l for l in range(7) if p in LINES[l]) for p in range(7)]   # rows concurrent at p

def lemma763(loads):
    # note Lemma 7.63 in the dual indexing: row-'lines' = concurrent triples of lines.
    return max(max(loads), max(sum(loads[l] for l in C) for C in CONC)/2, sum(loads)/4)

from functools import lru_cache
@lru_cache(maxsize=None)
def fano_min_capacity(s):
    """min over assignments of the capacity x needed (max over the 2 parts)."""
    T = types(s); best = None; arg = None
    for asg in itertools.product('ab', repeat=7):
        need = max(lemma763([T[asg[l]][i] for l in range(7)]) for i in range(2))
        if best is None or need < best: best, arg = need, asg
    return best, arg

def check_B():
    # (1) every 2-colouring of lines has a monochromatic concurrent triple
    for asg in itertools.product('ab', repeat=7):
        assert any(len({asg[l] for l in C}) == 1 for C in CONC), asg
    print("B1 every a/b assignment of the 7 lines has a monochromatic concurrent triple: OK (128)")
    # (2) LP vs Lemma 7.63 closed form on random rational loads
    import random; random.seed(5); mx = 0
    for _ in range(3000):
        loads = [F(random.randint(0, 40), 40) for _ in range(7)]
        mx = max(mx, abs(lp_min_mass(loads) - float(lemma763(loads))))
    print(f"B2 own LP vs Lemma 7.63 closed form, 3000 random load vectors: max |diff| = {mx:.2e}")
    # (3) threshold F(s) = 3(1-s)/2 on s-grid in [0,2/5]
    bad = []
    for num in range(0, 161):
        s = F(num, 400)
        Fs, arg = fano_min_capacity(s)
        if Fs != F(3, 2)*(1-s): bad.append((s, Fs))
    print(f"B3 Fano threshold F(s) == 3(1-s)/2 for s=0..2/5 step 1/400: {'OK' if not bad else bad[:5]}")
    # (4) beyond 2/5 (documentation)
    for s in (F(2,5), F(9,20), F(1,2)):
        print(f"    s={s}: F(s)={fano_min_capacity(s)[0]}, 3(1-s)/2={F(3,2)*(1-s)}")
    # (5) the sample points: Fano-free by exact margin
    for (x, s) in [(F(5,4),F(3,20)),(F(5,4),F(4,25)),(F(32,25),F(7,50)),(F(257,200),F(71,500))]:
        Fs = fano_min_capacity(s)[0]
        # LP cross-check for every assignment at this point
        T = types(s); lpmin = min(max(lp_min_mass([float(T[asg[l]][i]) for l in range(7)]) for i in range(2))
                                   for asg in itertools.product('ab', repeat=7))
        print(f"B5 x={x} s={s}: Fano needs capacity {Fs} (LP {lpmin:.6f}) > x={x}: {Fs > x}")

# ---------------- C. local rules ----------------
def gt_star_min_union(x, s):
    T = list(types(s).values()); best = None
    for tr in itertools.combinations_with_replacement(T, 3):
        U = 0; feas = True
        for i in range(2):
            v = [t[i] for t in tr]; u = max(max(v), sum(v)/2)
            if u > x: feas = False; break
            U += u
        if feas and (best is None or U < best): best = U
    return best

def d4_exists(x, s):
    a, b = types(s)['a'], types(s)['b']
    return [ka for ka in range(8) if all(ka*a[i]+(7-ka)*b[i] <= 3*x for i in range(2))]

def nu3_exists(x, s):
    T = list(types(s).values())
    return any(all(sum(t[i] for t in tr) <= x for i in range(2))
               for tr in itertools.combinations_with_replacement(T, 3))

def tetra_ok(x, s):
    a, b = types(s)['a'], types(s)['b']
    M = lambda u, v: max(F(2,3)*u+v, F(4,3)*u+v/2)
    return all(M(a[i], b[i]) <= x for i in range(2))

def check_C():
    pts = [(F(5,4),F(3,20)),(F(5,4),F(4,25)),(F(32,25),F(7,50)),(F(257,200),F(71,500))]
    for (x, s) in pts:
        ts = tau_star_thm771(x, s)
        assert ts == min(x-s, 2*x-2+2*s)
        mu = gt_star_min_union(x, s)
        print(f"C x={x} s={s}: tau*={ts} ({float(ts):.4f}); GT* min good-triple union {mu} vs 2tau*={2*ts}: "
              f"{mu > 2*ts}; D4 multisets {d4_exists(x,s)}; 3 disjoint: {nu3_exists(x,s)}; tetra kills: {tetra_ok(x,s)}; "
              f"Fano-free: {fano_min_capacity(s)[0] > x}")
    # whole region R = {9/8<x<9/7, 11/8-x < s < 1-2x/3}: dense rational grid (all conditions are linear/PL)
    fails = {'tau>3/4': 0, 'GT*': 0, 'D4': 0, 'nu': 0, 'tetra': 0, 'fano': 0, 'formula': 0}; cnt = 0
    for i in range(1, 60):
        x = F(9,8) + (F(9,7)-F(9,8))*F(i, 60)
        lo, hi = F(11,8)-x, 1-F(2,3)*x
        for j in range(1, 40):
            s = lo + (hi-lo)*F(j, 40); cnt += 1
            ts = tau_star_thm771(x, s)
            if ts != 2*x-2+2*s: fails['formula'] += 1
            if not ts > F(3,4): fails['tau>3/4'] += 1
            if not gt_star_min_union(x, s) > 2*ts: fails['GT*'] += 1
            if d4_exists(x, s): fails['D4'] += 1
            if nu3_exists(x, s): fails['nu'] += 1
            if not tetra_ok(x, s): fails['tetra'] += 1
            if not fano_min_capacity(s)[0] > x: fails['fano'] += 1
    print(f"C region grid ({cnt} rational points of the open triangle): failures {fails}")
    # beyond x>=9/7: D4 region vs Fano-free region disjoint (sup of the W-family under GT*+D4+nu+noFano is 6/7)
    over = 0
    for i in range(0, 80):
        x = F(9,7) + F(i, 160)
        for j in range(1, 80):
            s = F(j, 160)
            if 1-s > x or s > x: continue
            if not d4_exists(x, s) and not nu3_exists(x, s) and fano_min_capacity(s)[0] > x:
                over = max(over, tau_star_thm771(x, s))
    print(f"C x>=9/7 (s-grid 1/160): max tau* over Fano-free & D4-free & nu<=2 W-points = {over} ({float(over):.4f}) < 6/7: {over < F(6,7)}")
    # tetra region vs tau*>3/4
    ex = [(F(23,20), s) for s in (F(1,5), F(19,100), F(21,100))]
    for (x, s) in ex:
        print(f"    tetra/tau*: x={x} s={s}: tau*={tau_star_thm771(x,s)} tetra={tetra_ok(x,s)} (tetra needs s>=(8-6x)/5={(8-6*x)/5})")

# ---------------- D. explicit discrete tetrahedral bad tuple ----------------
def tetra_cells():
    A = [0, 1, 2, 3]; B = [4, 5, 6]
    matchings = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
    cells = [frozenset(set(A)-{q}) for q in A] + [frozenset(B)]
    for bi, mt in enumerate(matchings):
        for e in mt:
            cells.append(frozenset(set(e) | (set(B)-{B[bi]})))
    return cells

def explicit_tuple(k, x, s):
    n = int(x*k); aP = int(s*k); aQ = k - aP
    assert F(n) == x*k and F(aP) == s*k
    cells = tetra_cells(); C = len(cells)
    loads = {0: [aP]*4 + [aQ]*3, 1: [aQ]*4 + [aP]*3}     # rows 0-3 type a, rows 4-6 type b
    rows_pts = [[] for _ in range(7)]; nxt = 0; parts_pts = {}
    for part in (0, 1):
        A_ = np.array([[1 if r in c else 0 for c in cells] for r in range(7)])
        res = milp(c=np.ones(C), constraints=[LinearConstraint(A_, lb=loads[part], ub=np.inf),
                                                LinearConstraint(np.ones((1, C)), lb=0, ub=n)],
                   integrality=np.ones(C), bounds=Bounds(0, n))
        if res.status != 0: return None
        mass = [int(round(v)) for v in res.x]
        pts = list(range(nxt, nxt+n)); nxt += n; parts_pts[part] = set(pts)
        it = iter(pts); cell_pts = [[next(it) for _ in range(m)] for m in mass]
        for r in range(7):
            cand = [p for ci, c in enumerate(cells) if r in c for p in cell_pts[ci]]
            assert len(cand) >= loads[part][r]
            rows_pts[r] += cand[:loads[part][r]]
    edges = [frozenset(r) for r in rows_pts]
    for r, E in enumerate(edges):
        tp = (len(E & parts_pts[0]), len(E & parts_pts[1]))
        assert tp == ((aP, aQ) if r < 4 else (aQ, aP)), tp
    V = sorted(parts_pts[0] | parts_pts[1])
    pierce = [(u, v) for i, u in enumerate(V) for v in V[i:] if all(u in E or v in E for E in edges)]
    return n, aP, edges, pierce

def check_D():
    for (k, x, s) in [(20, F(5,4), F(3,20)), (40, F(5,4), F(3,20)), (100, F(32,25), F(7,50)), (50, F(32,25), F(7,50))]:
        out = explicit_tuple(k, x, s)
        if out is None:
            print(f"D k={k} x={x} s={s}: no integer tetrahedral realization at this scale"); continue
        n, aP, edges, pierce = out
        t = tau_discrete(n, aP, k-aP)
        print(f"D k={k} x={x} s={s}: parts {n}+{n}, types ({aP},{k-aP})/({k-aP},{aP}); discrete tau={t} "
              f"(tau/k={t/k:.3f}); explicit 4a+3b tetrahedral 7-tuple, distinct edges={len(set(edges))}, "
              f"2-transversals of the 7 edges: {len(pierce)}")

# ---------------- E. which certified two-type functions kill W ----------------
CAPJSON = ('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/outputs/'
           'two_type_capacity_certificate/logs/astra_support_capacity_minimal.json')   # read-only source

def support_maximal(hexmask):
    m = int(hexmask, 16)
    sets = [S for S in range(128) if (m >> (127 - S)) & 1]   # bit order: MSB = subset 0 (validated: downset, non-covering)
    ss = set(sets); assert all(T in ss for S in sets for T in range(128) if T & S == T) and all((S | T) != 127 for S in sets for T in sets)
    return sorted([S for S in sets if not any(S != T and (S & T) == S for T in sets)], key=lambda S: (-bin(S).count('1'), S))

def is_fano_support(maxs):
    if len(maxs) != 7 or any(bin(S).count('1') != 4 for S in maxs): return False
    comps = [127 ^ S for S in maxs]     # should be the 7 lines of a Fano plane
    return all(bin(comps[i] & comps[j]).count('1') == 1 for i in range(7) for j in range(i+1, 7))

def check_E():
    import json, ast
    d = json.load(open(CAPJSON))
    fns = d['minimal_functions']
    if isinstance(fns, str): fns = ast.literal_eval(fns)
    print(f"E loaded {len(fns)} minimal certified two-type functions (note Thm 7.69)")
    for (x, s) in [(F(5,4),F(3,20)),(F(257,200),F(71,500)),(F(32,25),F(7,50))]:
        a, b = types(s)['a'], types(s)['b']
        kills = []
        for i, f in enumerate(fns):
            V = [(F(u), F(v)) for u, v in f['vertices']]
            for (p, q, lab) in ((a, b, 'M(a,b)'), (b, a, 'M(b,a)')):
                if all(max(u*p[j]+v*q[j] for u, v in V) <= x for j in range(2)):
                    maxs = support_maximal(f['witness'][0])
                    kills.append((i, lab, [(str(u), str(v)) for u, v in V], len(maxs), is_fano_support(maxs),
                                  bin(f['witness'][1]).count('1')))
        print(f"E x={x} s={s}: {len(kills)} (function,orientation) pairs realise a bad tuple:")
        fnids = sorted({kk[0] for kk in kills})
        print(f"     functions: {fnids}; any Fano support among them: {any(kk[4] for kk in kills)}")
        for kk in kills:
            if kk[1] == 'M(a,b)': print(f"     fn#{kk[0]} vertices {kk[2]}; support {kk[3]} maximal cells, Fano={kk[4]}")
    # Fano-support functions present in the list (sanity: they must all FAIL on W)
    nf = sum(1 for f in fns if is_fano_support(support_maximal(f['witness'][0])))
    print(f"E sanity: {nf} of the 42 minimal functions have a Fano-downset witness support")

# ---------------- F. the elementary 'link' rule L_m (m edges, no common point, + 1 edge disjoint from their union) ----
def link_kills(x, s, mmax=6):
    """smallest m<=mmax such that m type-u edges with empty common intersection plus one type-w edge disjoint from
    their union fit (continuum); u,w in {a,b} (u=w allowed). Returns (m,u,w) or None."""
    T = types(s)
    for m in range(2, mmax+1):
        for u in 'ab':
            for w in 'ab':
                if all(F(m, m-1)*T[u][i] + T[w][i] <= x and T[u][i] <= x for i in range(2)):
                    return (m, u, w)
    return None

def explicit_link_tuple(k, x, s, m):
    n = int(x*k); aP = int(s*k); aQ = k - aP
    # m a-edges in P (size aP) and Q (size aQ), every point in exactly <= m-1 of them: cyclic construction on
    # N_i = ceil(m*load/(m-1)) points: edge j = all points except a block of the cyclic order.
    edges = [set() for _ in range(m)]; used = {}
    base = 0
    for part, load in ((0, aP), (1, aQ)):
        N = -(-m*load // (m-1)); pts = list(range(base, base+N))
        # each point omitted by >=1 edge: edge j omits points p with p % m == j, then trim to load
        for j in range(m):
            cand = [p for idx, p in enumerate(pts) if idx % m != j]
            assert len(cand) >= load, (N, load, m)
            edges[j] |= set(cand[:load])
        used[part] = (base, base+N); base += n
    # b-edge: (aQ, aP) points in (P,Q) outside the union
    freeP = [p for p in range(0, n) if not any(p in E for E in edges)]
    freeQ = [p for p in range(n, 2*n) if not any(p in E for E in edges)]
    if len(freeP) < aQ or len(freeQ) < aP: return None
    Fb = set(freeP[:aQ]) | set(freeQ[:aP])
    fam = [frozenset(E) for E in edges] + [frozenset(Fb)]
    for j, E in enumerate(fam):
        tp = (sum(1 for p in E if p < n), sum(1 for p in E if p >= n))
        assert tp == ((aP, aQ) if j < m else (aQ, aP)), tp
    assert not frozenset.intersection(*fam[:m])
    V = list(range(2*n))
    pierce = sum(1 for i, u in enumerate(V) for v in V[i:] if all(u in E or v in E for E in fam))
    return n, fam, pierce

def check_F():
    for (x, s) in [(F(5,4),F(3,20)),(F(5,4),F(4,25)),(F(32,25),F(7,50)),(F(257,200),F(71,500))]:
        print(f"F x={x} s={s}: link rule L_m kills with (m,u,w) = {link_kills(x, s)}")
    for (k, x, s, m) in [(20, F(5,4), F(3,20), 5), (100, F(32,25), F(7,50), 5), (40, F(5,4), F(3,20), 5)]:
        out = explicit_link_tuple(k, x, s, m)
        if out is None: print(f"F k={k}: rounding prevents explicit tuple"); continue
        n, fam, pierce = out
        print(f"F k={k} x={x} s={s}: explicit {m} a-edges (no common point) + 1 disjoint b-edge, parts {n}+{n}: "
              f"{len(fam)} edges, 2-transversals: {pierce}  => W not even ({m+1},2)")
    # sup of tau* over W-points surviving Fano + D4 + nu + L6 (grid, exact)
    best = (F(0), None)
    for i in range(0, 721):
        x = F(1) + F(i, 1440)
        for j in range(0, 721):
            s = F(j, 1440)
            if 1-s > x or s > x: continue
            if fano_min_capacity(s)[0] <= x or d4_exists(x, s) or nu3_exists(x, s) or link_kills(x, s): continue
            ts = tau_star_thm771(x, s)
            if ts > best[0]: best = (ts, (x, s))
    print(f"F sup tau* over W-points free of Fano, D4, nu>=3 and L_m (m<=6), grid 1/1440: {best[0]} = {float(best[0]):.5f} "
          f"at (x,s)={best[1]}; predicted sup 10/13 = {10/13:.5f} at (15/13, 3/13) (not attained)")
    # which W-points with tau*>3/4 survive L6 as well: region x in (9/8, 15/13)
    x0, s0 = F(15,13), F(3,13)
    print(f"    at (15/13,3/13): tau*={tau_star_thm771(x0,s0)}, Fano cap {fano_min_capacity(s0)[0]} vs x, L6 slack Q: "
          f"{F(6,5)*(1-s0)+s0 - x0}")

if __name__ == '__main__':
    import sys as _s
    if 'E' in _s.argv: check_E()
    elif 'F' in _s.argv: check_F()
    else: check_B(); check_C(); check_D(); check_E(); check_F()
