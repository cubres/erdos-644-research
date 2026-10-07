# Up-box union library (templates agent, session 2).
# Types: a in R^p, sum a = 1, g^j <= a <= x for some generator j.
# tau* = min(N-1, min over blocking maps phi of sum_{i in im phi} (x_i - min_{phi(j)=i} g^j_i)).
# Templates: row classes -> generators; per-part facets sum_c coef[c]*t[c][i] <= x_i; types t[c] in U(g^sigma(c)).
import itertools
import numpy as np
from scipy.optimize import linprog

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]

def tau_star(x, gens, return_map=False):
    p = len(x); N = sum(x); best = N - 1; arg = None
    choices = [[i for i in range(p) if g[i] > 1e-15] for g in gens]
    for phi in itertools.product(*choices):
        u = {}
        for j, i in enumerate(phi):
            u[i] = min(u.get(i, 1e9), gens[j][i])
        c = sum(x[i] - u[i] for i in u)
        if c < best: best = c; arg = phi
    return (best, arg) if return_map else best

# ---- facet templates: (name, nclasses, facets(list of coef tuples)) ----
def fano_template(col):
    """col: tuple of 7 class labels (0..k-1) on Fano row labels (points). returns (k, facets)"""
    k = max(col) + 1
    fs = set()
    for j in range(7):
        c = [0.0]*k; c[col[j]] += 1; fs.add(tuple(c))
    for L in LINES:
        c = [0.0]*k
        for j in L: c[col[j]] += 0.5
        fs.add(tuple(c))
    c = [0.0]*k
    for j in range(7): c[col[j]] += 0.25
    fs.add(tuple(c))
    fs = [f for f in fs if not any(g != f and all(gg >= ff - 1e-12 for gg, ff in zip(g, f)) for g in fs)]
    return k, fs

TWO = {  # two-class functions M(s,t) = max of s*u + t*v ; class 0 = s, class 1 = t
    'V':   [(1, 1), (1.25, 0.5)],        # 5 s-rows, 2 t-rows
    'K4':  [(2/3, 1), (4/3, 0.5)],       # 4 s-rows, 3 t-rows (tetrahedral)
    'S61': [(1.2, 1)],                   # six-vs-one non-Fano: 6 s-rows, 1 t-row
    'U':   [(5/6, 1), (1, 0.75), (4/3, 0)],  # note 7.73 U(s,t)
    'Qt':  [(0, 1.5), (1, 0.75)],        # Q with t-rows on the line (= Fano)
    'F61': [(1.5, 0.25), (0, 1)],        # six s + one t Fano (3s/2+t/4)
    'NC':  [(1.5, 0), (1, 0.75), (0.5, 1)],  # noncollinear triple of t-rows
}

def template_feasible(x, gens, assign, facets, want_types=False):
    """assign: generator index for each class; facets: list of coefficient tuples over classes."""
    p = len(x); k = len(assign); nv = k*p
    A = []; b = []
    for i in range(p):
        for f in facets:
            r = np.zeros(nv)
            for c in range(k): r[c*p + i] = f[c]
            A.append(r); b.append(x[i])
    Aeq = []; beq = []
    for c in range(k):
        r = np.zeros(nv); r[c*p:(c+1)*p] = 1; Aeq.append(r); beq.append(1.0)
    bounds = []
    for c in range(k):
        g = gens[assign[c]]
        for i in range(p):
            if g[i] > x[i] + 1e-12: return (False, None) if want_types else False
            bounds.append((g[i], x[i]))
    res = linprog(np.zeros(nv), A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=bounds, method='highs')
    ok = res.status == 0
    if want_types: return ok, (res.x.reshape(k, p) if ok else None)
    return ok

def fano_colourings(m):
    """orbit reps of maps [7] -> [m] under Fano automorphisms (classes = generator labels)"""
    Ls = [frozenset(L) for L in LINES]; auts = []
    for q in itertools.permutations(range(7)):
        if all(frozenset(q[j] for j in L) in Ls for L in Ls): auts.append(q)
    seen = set(); reps = []
    for col in itertools.product(range(m), repeat=7):
        if col in seen: continue
        seen |= {tuple(col[q[j]] for j in range(7)) for q in auts}
        reps.append(col)
    return reps

def menu(m, fano=True, two=True):
    """list of (name, assign, facets)"""
    out = []
    if fano:
        for col in fano_colourings(m):
            k, fs = fano_template(tuple(range(7)))  # distinct row types per row
            out.append(('Fano' + ''.join(map(str, col)), list(col), fs))
    if two:
        for name, fs in TWO.items():
            for j1 in range(m):
                for j2 in range(m):
                    out.append((f'{name}({j1},{j2})', [j1, j2], fs))
    return out

def TABC(A, B, C):
    """template T(A,B,C): classes 0=A (4 quad rows), 1=B (2 pencil rows), 2=C (1 pencil row), equal rows."""
    fs = [(2, 1, 0), (2, 0, 1), (0, 2, 1), (4, 2, 1), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    fs = [tuple(v/ (2 if f[0] in (2,) and sum(f) == 3 else 1) for v in f) for f in fs]
    return [A, B, C], [(1, .5, 0), (1, 0, .5), (0, 1, .5), (1, .5, .25), (1, 0, 0), (0, 1, 0), (0, 0, 1)]

def find_any(x, gens, items):
    for name, assign, fs in items:
        if template_feasible(x, gens, assign, fs): return name
    return None
