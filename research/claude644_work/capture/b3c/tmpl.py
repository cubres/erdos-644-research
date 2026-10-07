"""Template inequality generators (rational) + numpy evaluators.  Variables: x0,x1,x2,g0,g1,g2, then types
t_k = (t_k0,t_k1,t_k2) at index 6+3k.  Constraint form: dict{var:Fraction}, rhs Fraction meaning sum <= rhs."""
from fractions import Fraction as F
import json, itertools
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PENCIL = [[l for l, L in enumerate(LINES) if q in L] for q in range(7)]
X = lambda i: i
G = lambda i: 3+i
T = lambda k, i: 6+3*k+i
PAIRDATA = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
PAIRF = [[(F(u), F(v)) for u, v in f['vertices']] for f in PAIRDATA['minimal_functions']]
def fano_ineqs(asg):
    """asg: tuple of 7 type indices on LINES. Lemma 7.63 parent criterion per part (rows<=x automatic)."""
    out = []
    for i in range(3):
        for q in range(7):
            d = {}
            for l in PENCIL[q]:
                d[T(asg[l], i)] = d.get(T(asg[l], i), 0) + 1
            d[X(i)] = d.get(X(i), 0) - 2
            out.append((d, F(0)))
        d = {}
        for l in range(7): d[T(asg[l], i)] = d.get(T(asg[l], i), 0) + 1
        d[X(i)] = -4
        out.append((d, F(0)))
    return dedupe(out)
def pair_ineqs(f, j, l):
    out = []
    for i in range(3):
        for u, v in PAIRF[f]:
            d = {}
            if u: d[T(j, i)] = d.get(T(j, i), 0) + u
            if v: d[T(l, i)] = d.get(T(l, i), 0) + v
            d[X(i)] = d.get(X(i), 0) - 1
            out.append((d, F(0)))
    return dedupe(out)
def dedupe(cs):
    seen = set(); out = []
    for d, r in cs:
        d = {k: v for k, v in d.items() if v != 0}
        key = (tuple(sorted(d.items())), r)
        if key in seen: continue
        seen.add(key); out.append((d, r))
    return out
