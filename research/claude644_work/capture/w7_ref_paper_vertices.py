#!/usr/bin/env python3
"""Referee w7, claim 'paper': exact vertex enumeration of the case polytopes of
Proposition 4.1 of paper_0865.tex, written from the paper text only.

For every case polytope (closure), enumerate all vertices with Fractions and check
at each vertex every hypothesis of the lemma invoked (as stated in Section 3, at
r=1, T=beta), in the role assignment stated in the proof.  Hypotheses are concave
(>=0 form) piecewise-linear functions, so vertex checks cover the closure.
Also: random exact rational sampling of the region R, case chosen by the paper's
if-then-else chain on the OPEN/strict conditions, hypotheses checked at the point.
Mutation: beta -> beta - 1/2000 must produce a failure.
"""
from fractions import Fraction as Fr
from itertools import combinations
import random, sys

def solve3(A, b):
    # exact Cramer for 3x3
    def det(M):
        return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
    D = det(A)
    if D == 0:
        return None
    sol = []
    for j in range(3):
        M = [row[:] for row in A]
        for i in range(3):
            M[i][j] = b[i]
        sol.append(det(M)/D)
    return sol

def vertices(cons):
    """cons: list of (a,b) with a.(m,y,z) <= b, Fractions."""
    V = set()
    for tri in combinations(cons, 3):
        A = [list(c[0]) for c in tri]; b = [c[1] for c in tri]
        p = solve3(A, b)
        if p is None:
            continue
        if all(sum(ai*pi for ai, pi in zip(a, p)) <= bb for a, bb in cons):
            V.add(tuple(p))
    return sorted(V)

def run(beta, verbose=True):
    e = 1 - beta
    F = Fr
    # base region R (the paper's (R))
    R = [((0, 0, -1), F(0)), ((0, -1, 1), F(0)), ((-1, 1, 0), F(0)),
         ((1, 0, 0), F(92, 200)), ((1, 2, 0), F(227, 200))]
    # helper builders: constraint  a.(m,y,z) <= b
    def le(a, b): return (tuple(F(x) for x in a), F(b))
    def ge(a, b): return (tuple(-F(x) for x in a), -F(b))
    c_a  = [le((1,0,0), F(119,400))]
    c_b  = [ge((1,0,0), F(119,400)), le((0,1,0), F(73,200))]
    c_b2 = c_b + [ge((-1,1,-1), -e)]            # y-z >= m-e  <=> -m+y-z >= -e
    c_b3 = c_b + [le((-1,1,-1), -e), le((1,1,1), F(81,200))]
    c_b1 = c_b + [le((-1,1,-1), -e), ge((1,1,1), F(81,200))]
    c_c  = [ge((0,1,0), F(73,200))]
    # u=m+y, d=m-y
    c_c1 = c_c + [le((2,2,1), F(319,200))]      # z <= 319/200 - 2u
    c_c2 = c_c + [ge((2,2,1), F(319,200)), le((1,-1,1), e)]      # z <= e-d  <=> m-y+z <= e
    c_c3 = c_c + [ge((2,2,1), F(319,200)), ge((1,-1,1), e), le((0,F(1,2),1), F(73,200))]
    c_c4 = c_c + [ge((2,2,1), F(319,200)), ge((1,-1,1), e), ge((0,F(1,2),1), F(73,200))]
    c_c4A = c_c4 + [ge((-1,-1,3), e)]           # 3z >= e+u
    c_c4B = c_c4 + [le((-1,-1,3), e)]

    fails = []
    def chk(name, ok, pt, what):
        if not ok:
            fails.append((name, what, pt))

    def L26(x, y, z, T, r=1):
        S = x+y+z
        return {'S': T >= S, 'r-x+z': T >= r-x+z, 'r-y+z': T >= r-y+z,
                'r-x+y/2': T >= r-x+y/2, 'r-y+x/2': T >= r-y+x/2,
                '(r+2x+2y+z)/3': 3*T >= r+2*x+2*y+z}
    def L32(x, y, z, T, r=1):
        S = x+y+z
        return {'T<=r': T <= r, 'S': T >= S, 'r/2+y': T >= F(r,2)+y if isinstance(r,int) else T >= r/2+y,
                '(r+2x-y+z)/2': 2*T >= r+2*x-y+z, '(r+2x+y+3z)/3': 3*T >= r+2*x+y+3*z}
    def L31(x, y, z, T, r=1):
        S = x+y+z
        return {'T<=r': T <= r, 'x+y': T >= x+y, 'r/2+x': 2*T >= r+2*x, 'r/2+y': 2*T >= r+2*y,
                'r+x-y-z': T >= r+x-y-z, 'r-x+y-z': T >= r-x+y-z, 'r-S/3': 3*T >= 3*r-S,
                '(3r+S)/5': 5*T >= 3*r+S, '(r+x+y+2z)/3': 3*T >= r+x+y+2*z, '(2r+3z)/4': 4*T >= 2*r+3*z}
    def S2(x, y, z, T, r=1):
        P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
        return {'x<=T': x <= T, 'y<=T': y <= T, '(i)': T >= r-x+z+P+Q, '(ii)': T >= y+z+Q,
                '(iii)': 2*T >= r+y+2*z+P+2*Q}
    def S1(x, y, z, x1, y1, z1, T, r=1):
        return {'0<=x1<=x': 0 <= x1 <= x, '0<=y1<=y': 0 <= y1 <= y, '0<=z1<=z': 0 <= z1 <= z,
                'sum<=T': x1+y1+z1 <= T, 'y1+z1': y1+z1 >= r+x-T, 'x1+z1': x1+z1 >= r+y-T,
                'x1+y1': x1+y1 >= r+z-T}
    def L18norm(m):
        return {'m<=1/2': m <= F(1,2), '(2+2m)/3<=beta': (2+2*m)/3 <= beta, '(3+m)/4<=beta': (3+m)/4 <= beta}

    def check_case(name, pt):
        m, y, z = pt
        T = beta
        u, d, S = m+y, m-y, m+y+z
        if name == 'a':
            res = L18norm(m)
        elif name == 'b2':
            res = L32(m, y, z, T)
        elif name == 'b3':
            res = L32(z, y, m, T)
        elif name == 'b1':
            res = L31(z, y, m, T)
        elif name == 'c1':
            res = L26(m, y, z, T)
        elif name == 'c2':
            res = S2(y, m, z, T)
        elif name == 'c3':
            res = S2(m, y, z, T)
        elif name in ('c4A', 'c4B'):
            if name == 'c4A':
                m1 = (e+y+z-m)/2; y1 = (e+m+z-y)/2; z1 = (e+m+y-z)/2
            else:
                z1 = z; y1 = e+m-z; m1 = e+y-z
            res = S1(m, y, z, m1, y1, z1, T)
        # auxiliary claims (C) and (*) of the text, in (c)
        if name.startswith('c'):
            res.update({'(C) m<81/200': m <= F(81,200), '(C) 146<u': u >= F(146,200),
                        '(C) u<154': u <= F(154,200), '(C) d<8': d <= F(8,200),
                        '(C) 2m-y<89': 2*m-y <= F(89,200), '(C) 2m+3y<381': 2*m+3*y <= F(381,200),
                        '(C) 2m+y<235': 2*m+y <= F(235,200)})
        if name in ('c4A', 'c4B'):
            res.update({'(*) z>=e+d': z >= e+d, '(*) z>=u-119/200': z >= u-F(119,200)})
        return res

    cases = [('a', c_a), ('b1', c_b1), ('b2', c_b2), ('b3', c_b3), ('c1', c_c1), ('c2', c_c2),
             ('c3', c_c3), ('c4A', c_c4A), ('c4B', c_c4B)]
    counts = {}
    for name, cc in cases:
        V = vertices(R + cc)
        counts[name] = len(V)
        for pt in V:
            for k, ok in check_case(name, pt).items():
                chk(name, ok, pt, k)
    if verbose:
        print('vertex counts', counts)
    # random exact sampling with the strict if-then-else chain
    rnd = random.Random(7)
    nsamp = 0
    for _ in range(200000):
        den = rnd.choice([200, 400, 1000, 997, 2003, 4000])
        m = F(rnd.randint(0, 92*den//200), den)
        y = F(rnd.randint(0, int(m*den)), den)
        z = F(rnd.randint(0, int(y*den)), den)
        if m + 2*y > F(227, 200) or m > F(92,200):
            continue
        nsamp += 1
        u, d, S = m+y, m-y, m+y+z
        if m <= F(119,400): name = 'a'
        elif y <= F(73,200):
            if y-z > m-e: name = 'b2'
            elif S < F(81,200): name = 'b3'
            else: name = 'b1'
        else:
            if z <= F(319,200)-2*u: name = 'c1'
            elif z < e-d: name = 'c2'
            elif z <= (F(146,200)-y)/2: name = 'c3'
            else: name = 'c4A' if 3*z >= e+u else 'c4B'
        for k, ok in check_case(name, (m, y, z)).items():
            chk('rand-'+name, ok, (m, y, z), k)
    if verbose:
        print('random samples', nsamp)
    return fails

if __name__ == '__main__':
    beta = Fr(173, 200)
    f = run(beta)
    print('beta=173/200 failures:', len(f))
    for x in f[:20]: print('  ', x)
    fm = run(beta - Fr(1, 2000), verbose=False)
    print('mutation beta-1/2000 failures:', len(fm), 'e.g.', fm[:3])
