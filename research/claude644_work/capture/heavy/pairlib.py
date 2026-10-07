"""42-function two-type catalogue (note 7.71; tmpl/lib2.py data): bad tuple with two types a,b exists iff for
some function k: max over vertices (u,v) of u*a_i+v*b_i <= x_i in every part i."""
import json
D = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
from fractions import Fraction as _F
FUNCS = [[(float(_F(u)), float(_F(v))) for u, v in f['vertices']] for f in D['minimal_functions']]
def pair_ok(x, a, b, tol=1e-12):
    for k, V in enumerate(FUNCS):
        if all(max(u*a[i]+v*b[i] for u, v in V) <= x[i] + tol for i in range(len(x))): return k
    return None
def any_pair(x, T, tol=1e-12):
    for j, a in enumerate(T):
        for l, b in enumerate(T):
            if l < j: continue
            k = pair_ok(x, a, b, tol)
            if k is not None: return (j, l, k)
            k = pair_ok(x, b, a, tol)
            if k is not None: return (l, j, k)
    return None

import numpy as _np
_FV = [_np.array(V) for V in FUNCS]
def pair_margin(x, T):
    """max over ordered pairs and functions of min over parts of (x_i - M(a_i,b_i)); >=0 iff some pair template"""
    x = _np.asarray(x, dtype=float); T = _np.asarray(T, dtype=float); m = len(T)
    best = -1e9
    for V in _FV:
        # M[j,l,i] = max_v u*T[j,i]+v*T[l,i]
        M = (V[:,0][:,None,None,None]*T[None,:,None,:] + V[:,1][:,None,None,None]*T[None,None,:,:]).max(axis=0)
        mm = ((x[None,None,:] - M)/x[None,None,:]).min(axis=2).max()
        if mm > best: best = mm
    return float(best)
