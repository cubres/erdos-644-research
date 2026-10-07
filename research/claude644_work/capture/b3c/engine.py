"""Discovery engine (float LPs; exact certificates produced separately by certify.py).
Region: list of constraints (dict,rhs) meaning a.z <= rhs, and equalities (dict,rhs) a.z == rhs."""
import sys, itertools, json, time
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
from tmpl import *
from heavylib import reparr, _PM
FT = F
def nv(nt): return 6+3*nt
def tomat(cons, n):
    A = np.zeros((len(cons), n)); b = np.zeros(len(cons))
    for r, (d, rhs) in enumerate(cons):
        for k, v in d.items(): A[r, k] = float(v)
        b[r] = float(rhs)
    return A, b
def lp(c, A, b, Ae, be, n):
    res = linprog(c, A_ub=A if len(A) else None, b_ub=b if len(A) else None, A_eq=Ae if len(Ae) else None,
                  b_eq=be if len(Ae) else None, bounds=[(None, None)]*n, method='highs')
    return res
# ---------------- base hypotheses ----------------
def base_constraints(balanced=True):
    C = []; E = []
    h = F(1, 1)
    for i in range(3):
        C.append(({X(i): -1}, F(0)))                  # x_i >= 0
        C.append(({X(i): 1}, F(3, 2)))                # x_i <= 3/2
        C.append(({X(i): F(2, 3), G(i): -1}, F(0)))   # g_i >= 2x_i/3
        C.append(({G(i): 1, X(i): -1}, F(0)))         # g_i <= x_i
        C.append(({G(i): 1}, F(1)))                   # g_i <= 1
    C.append(({X(0): -1, X(1): -1, X(2): -1, G(0): 1, G(1): 1, G(2): 1}, F(-3, 4)))   # E >= 3/4
    if balanced:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            C.append(({X(i): 1, X(j): 1, G(i): -1, G(j): -1}, F(3, 4)))
    return C, E
def type_constraints(k):
    C = []; E = [({T(k, 0): 1, T(k, 1): 1, T(k, 2): 1}, F(1))]
    for i in range(3):
        C.append(({T(k, i): -1}, F(0)))
        C.append(({T(k, i): 1, X(i): -1}, F(0)))
    return C, E
def pattern_constraints(k, pat):
    C = []
    for i in range(3):
        if pat[i]: C.append(({T(k, i): -1, G(i): 1}, F(0)))            # t_i >= g_i
        else: C.append(({T(k, i): 1, X(i): F(-2, 3)}, F(0)))           # t_i <= 2x_i/3
    return C
PATS = [p for p in itertools.product([0, 1], repeat=3) if any(p)]
def request_constraints(k, w):
    """w: list of 3 dicts (linear forms incl. const key 'c'); t_i <= x_i - w_i"""
    C = []
    for i in range(3):
        d = {T(k, i): F(1), X(i): F(-1)}
        const = F(0)
        for kk, v in w[i].items():
            if kk == 'c': const += v
            else: d[kk] = d.get(kk, 0) + v
        C.append((d, -const))
    return C
# ---------------- numeric template evaluation ----------------
def decode(z, nt):
    x = z[0:3]; g = z[3:6]; Tt = z[6:6+3*nt].reshape(nt, 3); return x, g, Tt
def fano_candidates(Z, nt, tol=1e-9):
    """Z: (m, n) sample points. returns list of assignment tuples feasible at all points, sorted by min margin."""
    R = reparr(nt)
    marg = None
    for z in Z:
        x, g, Tt = decode(z, nt)
        rows = Tt[R]; pen = np.einsum('ql,nlp->nqp', _PM, rows)
        s1 = (2*x - pen).min(axis=1); s2 = (4*x - rows.sum(axis=1))
        m = np.minimum(s1, s2).min(axis=1)
        marg = m if marg is None else np.minimum(marg, m)
    idx = np.argsort(-marg)
    return [(tuple(int(v) for v in R[i]), float(marg[i])) for i in idx if marg[i] >= -tol], marg, R
_PV = [np.array([[float(u), float(v)] for u, v in f]) for f in PAIRF]
def pair_candidates(Z, nt, tol=1e-9):
    out = []
    for f, V in enumerate(_PV):
        for j in range(nt):
            for l in range(nt):
                if j == l: continue
                mm = 9.0
                for z in Z:
                    x, g, Tt = decode(z, nt)
                    load = (V[:, 0][:, None]*Tt[j][None, :] + V[:, 1][:, None]*Tt[l][None, :]).max(axis=0)
                    mm = min(mm, float((x - load).min()))
                if mm >= -tol: out.append(((f, j, l), mm))
    out.sort(key=lambda t: -t[1]); return out
def template_ineqs(tp):
    kind, data = tp
    return fano_ineqs(data) if kind == 'F' else pair_ineqs(*data)
