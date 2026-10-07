# referee_w5_paper_P41_vert.py -- exact vertex check (w5 Prop-4.1 referee, written from scratch).
# At r=1, T=beta, each lemma hypothesis is g(m,y,z) >= 0 with g CONCAVE piecewise linear
# (linear minus max(0,linear) terms), so its minimum over a polytope is attained at a vertex.
# For S1 the paper's split is affine on each sub-branch, so the requirements are affine there.
# We compute the lemma hypotheses DIRECTLY from the lemma statements (with the paper's role order),
# not from the paper's reduced inequalities, on the closure of every case polytope.
from fractions import Fraction as F
from itertools import combinations

b = F(173, 200); e = 1 - b

def solve3(A, B):
    import copy
    M = [A[i][:] + [B[i]] for i in range(3)]
    for c in range(3):
        p = next((i for i in range(c, 3) if M[i][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        for i in range(3):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [M[i][j] - f*M[c][j] for j in range(4)]
    return tuple(M[i][3] / M[i][i] for i in range(3))

def verts(cons):   # cons: (a,c) with a.v <= c
    V = set()
    for tri in combinations(cons, 3):
        s = solve3([list(t[0]) for t in tri], [t[1] for t in tri])
        if s is None: continue
        if all(sum(a*x for a, x in zip(c[0], s)) <= c[1] for c in cons): V.add(s)
    return V
def le(a, c): return (tuple(F(t) for t in a), F(c))
def ge(a, c): return (tuple(-F(t) for t in a), -F(c))

# variables (m,y,z)
BASE = [ge((0,0,1),0), ge((0,1,-1),0), ge((1,-1,0),0), le((1,0,0),F(23,50)), le((1,2,0),F(227,200))]
NOT_A = [ge((1,0,0),F(119,400))]
B_ = NOT_A + [le((0,1,0),F(73,200))]
C_ = [ge((0,1,0),F(73,200))]
# y - z - m + e >= 0
b2 = B_ + [ge((-1,1,-1), -e)]
b3 = B_ + [le((-1,1,-1), -e), le((1,1,1),F(81,200))]
b1 = B_ + [le((-1,1,-1), -e), ge((1,1,1),F(81,200))]
# z <= 319/200 - 2(m+y)   <=>  2m+2y+z <= 319/200
c1 = C_ + [le((2,2,1),F(319,200))]
NC1 = C_ + [ge((2,2,1),F(319,200))]
# z <= e - d  <=> m - y + z <= e
c2 = NC1 + [le((1,-1,1), e)]
NC2 = NC1 + [ge((1,-1,1), e)]
# z <= (146/200 - y)/2  <=> y + 2z <= 146/200
c3 = NC2 + [le((0,1,2), F(146,200))]
c4 = NC2 + [ge((0,1,2), F(146,200))]
# 3z >= e + m + y  <=> -m - y + 3z >= e
c4A = c4 + [ge((-1,-1,3), e)]
c4B = c4 + [le((-1,-1,3), e)]

def L32(x, y, z, T=b):
    S = x+y+z
    return min(T-S, T-(1-x+z), T-(1-y+z), T-(1-x+y/2), T-(1-y+x/2), T-(1+2*x+2*y+z)/3)
def L33(x, y, z, T=b):
    S = x+y+z
    return min(1-T, T-S, T-(F(1,2)+y), T-(1+2*x-y+z)/2, T-(1+2*x+y+3*z)/3)
def L34(x, y, z, T=b):
    S = x+y+z
    return min(1-T, T-(x+y), T-(F(1,2)+x), T-(F(1,2)+y), T-(1+x-y-z), T-(1-x+y-z), T-(1-S/3),
               T-(3+S)/5, T-(1+x+y+2*z)/3, T-(2+3*z)/4)
def S2(x, y, z, T=b):
    P = max(0, 1+y-x-z-T); Q = max(0, 1+x-y-z-T)
    return min(T-x, T-y, T-(1-x+z+P+Q), T-(y+z+Q), 2*T-(1+y+2*z+P+2*Q))
def S1(x, y, z, x1, y1, z1, T=b):
    return min(x1, x-x1, y1, y-y1, z1, z-z1, T-(x1+y1+z1), y1+z1-(1+x-T), x1+z1-(1+y-T), x1+y1-(1+z-T))
def splitA(m, y, z): return ((e+y+z-m)/2, (e+m+z-y)/2, (e+m+y-z)/2)
def splitB(m, y, z): return (e+y-z, e+m-z, z)

cases = {
 'b2': (b2, lambda m,y,z: L33(m,y,z)),
 'b3': (b3, lambda m,y,z: L33(z,y,m)),
 'b1': (b1, lambda m,y,z: L34(z,y,m)),
 'c1': (c1, lambda m,y,z: L32(m,y,z)),
 'c2': (c2, lambda m,y,z: S2(y,m,z)),
 'c3': (c3, lambda m,y,z: S2(m,y,z)),
 'c4A': (c4A, lambda m,y,z: S1(m,y,z,*splitA(m,y,z))),
 'c4B': (c4B, lambda m,y,z: S1(m,y,z,*splitB(m,y,z))),
}
allok = True
for name, (cons, g) in cases.items():
    V = verts(BASE + cons)
    worst = min((g(*v), v) for v in V) if V else None
    ok = worst is not None and worst[0] >= 0
    allok &= ok
    print(name, "vertices", len(V), "min slack", worst[0] if worst else None, "at", tuple(map(str, worst[1])) if worst else None, "OK" if ok else "FAIL")
# (a): Lemma 3.1 at m=119/400: max((3+m)/4,(2+2m)/3) <= beta
ma = F(119, 400); print('a', max((3+ma)/4, (2+2*ma)/3) <= b, (2+2*ma)/3 == b)
# mutation: same polytopes, beta lowered by 1/1000 -> expect some FAIL
bm = b - F(1, 1000); fails = []
for name, (cons, g) in cases.items():
    V = verts(BASE + cons)
    import inspect
fl = []
fl.append(('c1', min(L32(m,y,z,bm) for (m,y,z) in verts(BASE+c1))))
fl.append(('b1', min(L34(z,y,m,bm) for (m,y,z) in verts(BASE+b1))))
fl.append(('c3', min(S2(m,y,z,bm) for (m,y,z) in verts(BASE+c3))))
print("mutation beta-1/1000 min slacks:", [(n, str(s)) for n, s in fl])
print("ALL OK" if allok else "SOME FAIL")
