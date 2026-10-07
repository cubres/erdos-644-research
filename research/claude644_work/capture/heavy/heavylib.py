"""heavyparts agent library. Continuous type-closed model, rank 1.
Types: vectors a (len p), sum 1, 0<=a<=x.  Fano rows are indexed by the 7 LINES of PG(2,2);
per-part criterion (note Lemma 7.63, dual form): for every point q, sum of rows on lines through q <= 2x_i;
total <= 4x_i; each row <= x_i."""
import itertools
from fractions import Fraction as Fr
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PENCIL = [[l for l, L in enumerate(LINES) if q in L] for q in range(7)]   # lines through q

def fano_autos():
    L = [frozenset(l) for l in LINES]; Ls = set(L); autos = []
    for perm in itertools.permutations(range(7)):
        if all(frozenset(perm[p] for p in l) in Ls for l in L): autos.append(perm)
    return autos
AUT = fano_autos()
LIDX = {frozenset(l): i for i, l in enumerate(LINES)}
LPERMS = [[LIDX[frozenset(pp[p] for p in l)] for l in LINES] for pp in AUT]

_R = {}
def reps(m):
    """orbit representatives of maps lines->types (range m) under PSL(2,7)"""
    if m in _R: return _R[m]
    seen = set(); out = []
    for b in itertools.product(range(m), repeat=7):
        if b in seen: continue
        out.append(b)
        for lp in LPERMS:
            nb = [None]*7
            for i in range(7): nb[lp[i]] = b[i]
            seen.add(tuple(nb))
    _R[m] = out; return out

def fano_rows_ok(x, rows, tol=1e-12):
    """rows: list of 7 vectors (row on line l). exact if Fractions and tol=0."""
    p = len(x)
    for i in range(p):
        z = [r[i] for r in rows]
        if max(z) > x[i] + tol: return False
        if sum(z) > 4*x[i] + tol: return False
        for q in range(7):
            if sum(z[l] for l in PENCIL[q]) > 2*x[i] + tol: return False
    return True

def fano_assign_ok(x, T, asg, tol=1e-12):
    return fano_rows_ok(x, [T[j] for j in asg], tol)

def all_fano(x, T, tol=1e-12):
    return [a for a in reps(len(T)) if fano_assign_ok(x, T, a, tol)]

def any_fano(x, T, tol=1e-12):
    for a in reps(len(T)):
        if fano_assign_ok(x, T, a, tol): return a
    return None

def tau_star(x, T):
    """exact (if Fractions) tau* = X - max(1?, max over blocking maps of sum_i min(x_i, min_{pi(a)=i} a_i)).
    Note the residual with sum<1 is covered by blocking maps (every type is blocked somewhere)."""
    p = len(x); X = sum(x); best = None
    choices = [[i for i in range(p) if a[i] > 0] for a in T]
    for pi in itertools.product(*choices):
        caps = list(x)
        for j, i in enumerate(pi): caps[i] = min(caps[i], T[j][i])
        s = sum(caps)
        if best is None or s > best: best = s
    return X - best

def tau_star_fast(x, T):
    """tau* = X - sup{sum u : u free}; branch and bound over blocking maps with strict flags."""
    p = len(x); X = sum(x)
    order = sorted(range(len(T)), key=lambda j: -max(T[j][i]/x[i] if x[i] > 0 else 0 for i in range(p)))
    best = [None]
    def blocked(a, caps, st):
        return any(a[i] > 0 and (caps[i] < a[i] or (caps[i] == a[i] and st[i])) for i in range(p))
    def rec(k, caps, st):
        s = sum(caps)
        if best[0] is not None and s <= best[0]: return
        while k < len(order) and blocked(T[order[k]], caps, st): k += 1
        if k == len(order):
            best[0] = s; return
        a = T[order[k]]
        for i in sorted(range(p), key=lambda i: a[i]-caps[i]):
            if a[i] > 0 and a[i] <= caps[i]:
                c2 = list(caps); c2[i] = a[i]; s2 = list(st); s2[i] = True
                rec(k+1, c2, s2)
    rec(0, list(x), [False]*p)
    return X - best[0]

def heavy_parts(x, T):
    p = len(x)
    return [i for i in range(p) if any(a[i]*7 > 4*x[i] for a in T)]

def is_homog(x, a):
    return all(7*a[i] <= 4*x[i] for i in range(len(x)))

import numpy as _np
_REPARR = {}
import os as _os
def reparr(m):
    if m not in _REPARR:
        f = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), f'reps{m}.npy')
        _REPARR[m] = _np.load(f).astype(_np.int64) if _os.path.exists(f) else _np.array(reps(m), dtype=_np.int64)
    return _REPARR[m]
_PM = _np.zeros((7,7))
for _q in range(7):
    for _l in PENCIL[_q]: _PM[_q,_l] = 1.0
def fano_mask(x, T, tol=1e-12, R=None):
    """boolean array over assignment reps (or given array R of assignments) : Fano feasible"""
    T = _np.asarray(T, dtype=float); x = _np.asarray(x, dtype=float)
    if R is None: R = reparr(len(T))
    rows = T[R]                      # (N,7,p)
    pen = _np.einsum('ql,nlp->nqp', _PM, rows)   # (N,7,p)
    ok = (pen <= 2*x + tol).all(axis=(1,2)) & (rows.sum(axis=1) <= 4*x + tol).all(axis=1) & (rows <= x + tol).all(axis=(1,2))
    return ok
def any_fano_np(x, T, tol=1e-12):
    return bool(fano_mask(x, T, tol).any())

def fano_margin(x, T, R=None):
    """max over assignment reps of (min over parts/inequalities of normalised slack); >=0 iff some Fano tuple"""
    T = _np.asarray(T, dtype=float); x = _np.asarray(x, dtype=float)
    if R is None: R = reparr(len(T))
    rows = T[R]
    pen = _np.einsum('ql,nlp->nqp', _PM, rows)
    s1 = ((2*x - pen)/x).min(axis=1)        # (N,p) normalised by capacity
    s2 = (4*x - rows.sum(axis=1))/x         # (N,p)
    s3 = (x - rows).min(axis=1)
    m = _np.minimum(s1, s2/2).min(axis=1)   # row slack ignored: types always fit (a<=x)
    k = int(m.argmax()); return float(m[k]), k
