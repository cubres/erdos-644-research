#!/usr/bin/env python3
"""Exact Fourier-Motzkin projection of the three-box universal Fano template (symmetric Q-rows) onto the
parameters (xA,xB,xC,tA,tB,tC), then exact LP check (Fractions via scipy only for discovery; final
verification of each projected inequality over the domain by exact vertex enumeration is separate).
Per-part inequalities = note Lemma 7.63 (pencil sums <= 2x, total <= 4x, rows <= x)."""
from fractions import Fraction as F
import itertools
V = ['al','be','ga','de','qB','qC']
P = ['xA','xB','xC','tA','tB','tC']
def C(v, p, c=0):
    # represents sum v[var]*var <= sum p[par]*par + c
    return ({k: F(x) for k, x in v.items() if x}, {k: F(x) for k, x in p.items() if x}, F(c))
cons = [
 # part A
 C({'al':2,'be':1},{'xA':4,'tA':-4}), C({'al':1},{'xA':2,'tA':-2}), C({'be':1},{'xA':2,'tA':-2}),
 C({'al':2,'be':1},{'xA':2}), C({'al':1},{'xA':1}), C({'be':1},{'xA':1}),
 # part B
 C({'ga':1},{'xB':2,'tB':-2}), C({'qB':2},{'xB':2,'tB':-1}), C({'qB':2,'ga':1},{'xB':2}),
 C({'qB':4,'ga':1},{'xB':4,'tB':-2}), C({'qB':1},{'xB':1}), C({'ga':1},{'xB':1}),
 # part C
 C({'de':2},{'xC':2,'tC':-1}), C({'qC':2},{'xC':2,'tC':-1}), C({'de':1,'qC':2},{'xC':2}),
 C({'qC':4,'de':2},{'xC':4,'tC':-1}), C({'qC':1},{'xC':1}), C({'de':1},{'xC':1}),
 # rows
 C({'qB':-1,'qC':-1},{'tA':1},-1), C({'al':-1,'de':-1},{'tB':1},-1), C({'be':-1,'ga':-1},{'tC':1},-1),
] + [C({v:-1},{}) for v in V]

def combine(c1, c2, var):
    a, b = c1[0][var], c2[0][var]   # a>0, b<0
    lam1, lam2 = -b, a
    v = {}; p = {}
    for k in set(c1[0]) | set(c2[0]):
        val = lam1*c1[0].get(k,0) + lam2*c2[0].get(k,0)
        if val: v[k] = val
    for k in set(c1[1]) | set(c2[1]):
        val = lam1*c1[1].get(k,0) + lam2*c2[1].get(k,0)
        if val: p[k] = val
    const = lam1*c1[2] + lam2*c2[2]
    # normalise
    return (v, p, const)

def key(c):
    v, p, k = c
    allc = list(v.values()) + list(p.values()) + [k]
    m = max(abs(x) for x in allc if x) if any(allc) else 1
    return (tuple(sorted((a, b/m) for a, b in v.items())), tuple(sorted((a, b/m) for a, b in p.items())), k/m)

cur = cons
for var in V:
    pos = [c for c in cur if c[0].get(var, 0) > 0]
    neg = [c for c in cur if c[0].get(var, 0) < 0]
    zero = [c for c in cur if c[0].get(var, 0) == 0]
    new = zero + [combine(a, b, var) for a in pos for b in neg]
    seen = {}; 
    for c in new: seen.setdefault(key(c), c)
    cur = list(seen.values())
    print(f"eliminated {var}: {len(cur)} constraints", flush=True)
# now all constraints are 0 <= sum p + c, i.e. -(sum p) - c <= 0 ; keep as (p, const): need sum p*par + const >= 0
proj = [(c[1], c[2]) for c in cur]
import pickle; pickle.dump(proj, open('threebox_proj.pkl','wb'))
print("projected inequalities:", len(proj))
