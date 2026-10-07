#!/usr/bin/env python3
"""Referee w7, claim 'paper': explicit-set end-to-end test of the constructions in
Lemmas 3.1 (L18), 3.2 (L26), 3.3 (L32), 3.4 (L31), 3.5 (S1), 3.6 (S2) and 5.2 (L41)
of paper_0865.tex, for all small integer parameters satisfying the stated hypotheses.

Independent of the paper's candidate-product bookkeeping: the final responses are
taken as the FULL complements of the requests (the worst case), and badness of the
resulting <=7 edges is decided by brute force over all point pairs (via types).
The adaptive first response H (and I in L41) ranges over ALL cell-level possibilities
allowed by the request (plus the gap restriction in L41).
Checks: every request has <= T points, and the final <=7 edges have no 2-transversal.
usage: w7_ref_paper_sets.py RMAX
"""
import sys, itertools

class U:
    def __init__(self):
        self.n = 0
    def new(self, k):
        s = list(range(self.n, self.n+k)); self.n += k; return s

def bad(edges, npts):
    # edges: list of python sets; universe 0..npts-1 plus implicit nothing else
    j = len(edges); full = (1 << j)-1
    types = set()
    for p in range(npts):
        t = 0
        for i, E in enumerate(edges):
            if p in E: t |= 1 << i
        types.add(t)
    types = list(types)
    for a in types:
        for b in types:
            if a | b == full: return False
    return True

FAIL = []
def fail(*a):
    FAIL.append(a)
    if len(FAIL) < 15: print('FAIL', a)

def triple(r, x, y, z, u, extra=0):
    X, Y, Z = u.new(x), u.new(y), u.new(z)
    PE, PF, PG = u.new(r-x-y), u.new(r-x-z), u.new(r-y-z)
    O = u.new(r+extra)
    E = set(X+Y+PE); F = set(X+Z+PF); G = set(Y+Z+PG)
    return X, Y, Z, PE, PF, PG, O, E, F, G

def finish(name, params, T, base, reqs, npts):
    for R in reqs:
        if len(R) > T: fail(name, params, 'size', len(R), T); return
    allp = set(range(npts))
    edges = list(base) + [allp - set(R) for R in reqs]
    if len(edges) > 7: fail(name, params, 'too many edges'); return
    if not bad(edges, npts): fail(name, params, 'not bad')

def ceil_div(a, b): return -((-a)//b)

# ---------------- L18 ----------------
def t_L18(r):
    n = 0
    for m in range(0, r//2+1):
        B = max(ceil_div(3*r+m, 4), ceil_div(2*r+2*m, 3))
        for x in range(m+1):
            for y in range(x+1):
                for z in range(y+1):
                    if y+z > r or x+y > r: continue
                    u = U(); X, Y, Z, PE, PF, PG, O, E, F, G = triple(r, x, y, z, u)
                    AF = PF[:B-x-y]
                    B0 = PG[:min(B-x, r-y-z)]
                    C = set(Z) | (set(PG)-set(B0))
                    c = len(C)
                    AE = PE[:min(B-x-c, r-x-y)]
                    if B-x-y < 0 or B-x-y > len(PF) or B-x-c < 0: fail('L18', (r,m,x,y,z), 'host'); continue
                    D1 = set(X+Y+AF); D2 = set(X+B0); D3 = set(X) | C | set(AE)
                    D4 = set(Y+Z) | (set(PE)-set(AE)) | (set(PF)-set(AF))
                    finish('L18', (r,m,x,y,z), B, [E,F,G], [D1,D2,D3,D4], u.n); n += 1
    return n

# ---------------- hypotheses ----------------
def hyp_L26(r,x,y,z,T):
    S=x+y+z
    return T>=S and T>=r-x+z and T>=r-y+z and 2*T>=2*r-2*x+y and 2*T>=2*r-2*y+x and 3*T>=r+2*x+2*y+z
def hyp_L32(r,x,y,z,T):
    S=x+y+z
    return T<=r and T>=S and 2*T>=r+2*y and 2*T>=r+2*x-y+z and 3*T>=r+2*x+y+3*z
def hyp_L31(r,x,y,z,T):
    S=x+y+z
    return (T<=r and T>=x+y and 2*T>=r+2*x and 2*T>=r+2*y and T>=r+x-y-z and T>=r-x+y-z
            and 3*T>=3*r-S and 5*T>=3*r+S and 3*T>=r+x+y+2*z and 4*T>=2*r+3*z)

def splits(n, k):
    # all (a,b,c...) not needed; helper
    pass

def H_from(cells_counts, O, r):
    """cells_counts: list of (cell_list, count). Build H with those counts and pad with O."""
    H = set()
    for cell, k in cells_counts:
        H |= set(cell[:k])
    pad = r - len(H)
    if pad < 0 or pad > len(O): return None
    H |= set(O[:pad])
    return H

# ---------------- L26 ----------------
def t_L26(r):
    n = 0
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                if x+z > r or y+z > r: continue
                for T in range(0, r+3):
                    if not hyp_L26(r,x,y,z,T): continue
                    for a in range(r-x-z+1):
                        for b in range(r-y-z+1):
                            for c in range(r-x-y+1):
                                if a+b+c > r: continue
                                u = U(); X,Y,Z,PE,PF,PG,O,E,F,G = triple(r,x,y,z,u)
                                H = H_from([(PF,a),(PG,b),(PE,c)], O, r)
                                A = set(PF[:a]); Bs = set(PG[:b]); C = set(PE[:c])
                                Bl, Al = sorted(Bs), sorted(A)
                                if b <= T-x:
                                    k1 = max(0, min(a, T-y-z-c))
                                    A1, A2 = set(Al[:k1]), set(Al[k1:])
                                    reqs = [set(X)|Bs, set(Y+Z)|C|A1, set(Y)|A2]
                                elif a <= T-y:
                                    k1 = max(0, min(b, T-x-z-c))
                                    B1, B2 = set(Bl[:k1]), set(Bl[k1:])
                                    reqs = [set(Y)|A, set(X+Z)|C|B1, set(X)|B2]
                                else:
                                    B2 = set(Bl[:T-x]); A3 = set(Al[:T-y])
                                    reqs = [set(X)|B2, set(Y)|A3, set(X+Y+Z)|C|(A-A3)|(Bs-B2)]
                                if len(set(X+Y+Z)) > T: fail('L26',(r,x,y,z,T),'first'); continue
                                finish('L26',(r,x,y,z,T,a,b,c),T,[E,F,G,H],reqs,u.n); n += 1
    return n

# ---------------- L32 ----------------
def t_L32(r):
    n = 0
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                if x+z > r or y+z > r: continue
                for T in range(0, r+1):
                    if not hyp_L32(r,x,y,z,T): continue
                    S = x+y+z
                    amax = r-x-z-(T-S)
                    if amax < 0: fail('L32',(r,x,y,z,T),'fit'); continue
                    for a in range(amax+1):
                        for b in range(r-y-z+1):
                            for c in range(r-x-y+1):
                                if a+b+c > r: continue
                                u = U(); X,Y,Z,PE,PF,PG,O,E,F,G = triple(r,x,y,z,u)
                                Pav = PF[:T-S]; Prest = PF[T-S:]
                                first = set(X+Y+Z+Pav)
                                H = H_from([(Prest,a),(PG,b),(PE,c)], O, r)
                                A = set(Prest[:a]); Bs = set(PG[:b]); C = set(PE[:c])
                                Bl = sorted(Bs)
                                if a <= T-y-z:
                                    cap = T-x-z
                                    B1, B2 = set(Bl[:cap]), set(Bl[cap:])
                                    reqs = [set(X+Z)|B1, set(X+Z)|B2, set(Y+Z)|A]
                                    Cl = sorted(C)
                                    for R in reqs:
                                        k = max(0, T-len(R)); R |= set(Cl[:k]); Cl = Cl[k:]
                                    if Cl: fail('L32',(r,x,y,z,T,a,b,c),'C leftover'); continue
                                else:
                                    BC = sorted(Bs|C); cap = T-x-z
                                    reqs = [set(X+Z)|set(BC[:cap]), set(X+Z)|set(BC[cap:]), set(Y)|A]
                                if len(first) > T: fail('L32','first'); continue
                                finish('L32',(r,x,y,z,T,a,b,c),T,[E,F,G,H],reqs,u.n); n += 1
    return n

# ---------------- L31 ----------------
def t_L31(r):
    n = 0
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                if x+z > r or y+z > r: continue
                for T in range(0, r+1):
                    if not hyp_L31(r,x,y,z,T): continue
                    z0 = min(z, T-x-y)
                    for q in range(z-z0+1):
                        for a in range(r-x-z+1):
                            for b in range(r-y-z+1):
                                for c in range(r-x-y+1):
                                    if q+a+b+c > r: continue
                                    u = U(); X,Y,Z,PE,PF,PG,O,E,F,G = triple(r,x,y,z,u)
                                    Z0 = Z[:z0]; Zr = Z[z0:]
                                    H = H_from([(Zr,q),(PF,a),(PG,b),(PE,c)], O, r)
                                    # the response must avoid X,Y,Z0 and its G-, F-traces are bounded automatically
                                    Q = set(Zr[:q]); A = set(PF[:a]); Bs = set(PG[:b]); C = set(PE[:c])
                                    V = set(Z)-Q; Dset = set(PE)-C
                                    Cl = sorted(C); Vl = sorted(V)
                                    if c <= T-z:
                                        reqs = [Q|set(X)|Bs, Q|set(Y)|A, set(Z)|C]; tag = 0
                                    else:
                                        a0 = r+x+z-2*T; b0 = r+y+z-2*T
                                        if a < a0:
                                            k2 = max(0, min(c, T-y-a-z))
                                            reqs = [Q|set(X)|Bs, set(Y)|A|set(Z)|set(Cl[:k2]), set(Z)|set(Cl[k2:])]; tag = 1
                                        elif b < b0:
                                            k2 = max(0, min(c, T-x-b-z))
                                            reqs = [Q|set(Y)|A, set(X)|Bs|set(Z)|set(Cl[:k2]), set(Z)|set(Cl[k2:])]; tag = 2
                                        else:
                                            uu = c+z-T
                                            C12 = set(Cl[:uu]); C3 = set(Cl[uu:])
                                            lo = max(0, y+a+z+uu-T); hi = min(len(V), T-q-x-b-uu)
                                            if lo > hi: fail('L31',(r,x,y,z,T,q,a,b,c),'t-interval'); continue
                                            t = lo
                                            reqs = [Q|set(X)|Bs|C12|set(Vl[:t]), Q|set(Y)|A|C12|set(Vl[t:]), set(Z)|C3]; tag = 3
                                    Dl = sorted(Dset)
                                    for R in reqs:
                                        k = max(0, T-len(R)); R |= set(Dl[:k]); Dl = Dl[k:]
                                    if Dl: fail('L31',(r,x,y,z,T,q,a,b,c,tag),'D leftover'); continue
                                    finish('L31',(r,x,y,z,T,q,a,b,c,tag),T,[E,F,G,H],reqs,u.n); n += 1
    return n

# ---------------- S1 / S2 ----------------
def t_S(r):
    n = 0
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                if x+z > r or y+z > r: continue
                for T in range(0, r+1):
                    # S1: all feasible integer splits
                    for x1 in range(x+1):
                        for y1 in range(y+1):
                            for z1 in range(z+1):
                                if not (x1+y1+z1 <= T and y1+z1 >= r+x-T and x1+z1 >= r+y-T and x1+y1 >= r+z-T): continue
                                u = U(); X,Y,Z,PE,PF,PG,O,E,F,G = triple(r,x,y,z,u)
                                X1,X2 = set(X[:x1]),set(X[x1:]); Y1,Y2 = set(Y[:y1]),set(Y[y1:]); Z1,Z2 = set(Z[:z1]),set(Z[z1:])
                                reqs = [X1|Y1|Z1, set(X+PG)|Y2|Z2, set(Y+PF)|X2|Z2, set(Z+PE)|X2|Y2]
                                finish('S1',(r,x,y,z,T,x1,y1,z1),T,[E,F,G],reqs,u.n); n += 1
                    # S2
                    P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
                    if x <= T and y <= T and T >= r-x+z+P+Q and T >= y+z+Q and 2*T >= r+y+2*z+P+2*Q:
                        u = U(); X,Y,Z,PE,PF,PG,O,E,F,G = triple(r,x,y,z,u)
                        V1, V2 = set(PF[:P]), set(PF[P:]); W13, W0 = set(PG[:Q]), set(PG[Q:])
                        U1 = T-r+x-z-P-Q; L = x+y+z+Q-T
                        lo, hi = max(0, L), min(x, U1)
                        if lo > hi: fail('S2',(r,x,y,z,T),'interval'); continue
                        for x01 in range(lo, hi+1):
                            X01, X03 = set(X[:x01]), set(X[x01:])
                            reqs = [set(X)|W0, X01|set(Y+Z+PE)|V1|W13, set(Y)|V2, X03|set(Y+Z)|W13]
                            finish('S2',(r,x,y,z,T,x01),T,[E,F,G],reqs,u.n); n += 1
    return n

# ---------------- L41 (Lemma 5.2) ----------------
def t_L41(r):
    n = 0
    half_up = (r+1)//2
    for m in range(0, r//4+1):
        for x in range(r//2+1, r+1):
            for bb in range(r//2+1, r+1):
                for y, z, a, c in itertools.product(range(m+1), repeat=4):
                    # E = X,Y,C,privE ; F = X,Z,A,privF ; G = Y,Z,B,privG ; H = A,C,B,privH
                    pe, pf, pg, ph = r-x-y-c, r-x-z-a, r-y-z-bb, r-a-c-bb
                    if min(pe, pf, pg, ph) < 0: continue
                    for T in range(0, r+1):
                        if not (T >= half_up+2*m and T >= x+m and 3*T >= 2*x+bb+half_up+2*m): continue
                        s, t = y+z, a+c
                        p = half_up - min(s, t); qq = T - half_up - max(s, t)
                        # enumerate I's cell counts: xi in X\X0, di in B\B0, private parts, gap |G cap I|,|H cap I|<=m
                        for xi in range(x-qq+1):
                            for di in range(min(bb-p, m)+1):
                                for gi in range(pg+1):
                                    if di+gi > m: continue
                                    for hi_ in range(ph+1):
                                        if di+hi_ > m: continue
                                        for ei in range(pe+1):
                                            for fi in range(pf+1):
                                                if xi+di+gi+hi_+ei+fi > r: continue
                                                u = U()
                                                X, Y, Z, A, C, B = u.new(x), u.new(y), u.new(z), u.new(a), u.new(c), u.new(bb)
                                                PE_, PF_, PG_, PH_ = u.new(pe), u.new(pf), u.new(pg), u.new(ph)
                                                O = u.new(r)
                                                E = set(X+Y+C+PE_); F = set(X+Z+A+PF_); G = set(Y+Z+B+PG_); H = set(A+C+B+PH_)
                                                B0 = B[:p]; X0 = X[:qq]
                                                req0 = set(Y+Z+A+C+B0+X0)
                                                if len(req0) != T: fail('L41', 'req0 size', len(req0), T); continue
                                                I = set(X[qq:qq+xi]) | set(B[p:p+di]) | set(PG_[:gi]) | set(PH_[:hi_]) | set(PE_[:ei]) | set(PF_[:fi])
                                                I |= set(O[:r-len(I)])
                                                BI = set(B) & I
                                                rest = [w for w in B if w not in BI]
                                                k = min(bb, T-x) - len(BI)
                                                if k < 0: fail('L41', 'B1'); continue
                                                B1 = BI | set(rest[:k])
                                                reqs = [set(X)|B1, (set(X)&I)|(set(B)-B1)]
                                                finish('L41', (r,m,x,bb,y,z,a,c,T,xi,di,gi,hi_,ei,fi), T, [E,F,G,H,I], reqs, u.n); n += 1
    return n

if __name__ == '__main__':
    RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    which = sys.argv[2].split(',') if len(sys.argv) > 2 else ['L18','L26','L32','L31','S','L41']
    for name in which:
        f = {'L18': t_L18, 'L26': t_L26, 'L32': t_L32, 'L31': t_L31, 'S': t_S, 'L41': t_L41}[name]
        tot = 0
        for r in range(1, RMAX+1):
            tot += f(r)
        print(name, 'r<=%d' % RMAX, 'instances', tot, 'failures so far', len(FAIL), flush=True)
