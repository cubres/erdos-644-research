# w5_paper_prop10_vertices.py  -- independent EXACT check of Proposition 4.1 (= handbound "Prop 10")
# AS WRITTEN IN paper_0865.tex.  Written from scratch (no imports from w4_* or referee_* scripts).
#
# Normalisation r = 1, T = beta = 173/200.  Variables v = (m, y, z) = sizes of the three pair cells,
# m >= y >= z.  Each case of the proof is a polytope (closure taken; closing only enlarges it).
# Every lemma hypothesis used in the paper is a CONVEX piecewise-linear function <= constant
# (or an affine function for the explicit S1 splits on each branch), so it holds on a polytope
# iff it holds at every vertex.  We also check every auxiliary inequality claimed in the text.
from fractions import Fraction as F
from itertools import combinations

b = F(173, 200); e = 1 - b          # e = 27/200
h = F(92, 200)                       # 23/50

def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
            - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

def vertices(cons):
    """cons: list of (a, c) meaning a . v <= c.  Returns set of vertices (exact)."""
    V = set()
    for tri in combinations(cons, 3):
        A = [list(t[0]) for t in tri]; B = [t[1] for t in tri]
        D = det3(A)
        if D == 0:
            continue
        sol = []
        for i in range(3):
            M = [row[:] for row in A]
            for j in range(3):
                M[j][i] = B[j]
            sol.append(det3(M) / D)
        if all(sum(a*x for a, x in zip(c[0], sol)) <= c[1] for c in cons):
            V.add(tuple(sol))
    return V

def le(a, c): return (tuple(F(t) for t in a), F(c))     # a.v <= c
def ge(a, c): return (tuple(-F(t) for t in a), -F(c))   # a.v >= c

# base region R of Proposition 4.1: 0 <= z <= y <= m <= 23/50, m + 2y <= 227/200
BASE = [ge((0, 0, 1), 0), ge((0, 1, -1), 0), ge((1, -1, 0), 0), le((1, 0, 0), h), le((1, 2, 0), 2 - b)]

# ---- lemma hypotheses exactly as stated in the paper (r = 1, T = beta), roles (X,Y,Z) = (x,y,z) ----
def L18(m):              # Lemma 3.1: budget max((3+m)/4,(2+2m)/3) <= beta, m <= 1/2
    return max((3 + m) / 4, (2 + 2*m) / 3) <= b and m <= F(1, 2)
def L26(x, y, z):        # Lemma 3.2
    S = x + y + z
    return max(S, 1 - x + z, 1 - y + z, 1 - x + y/2, 1 - y + x/2, (1 + 2*(x + y) + z) / 3) <= b
def L32(x, y, z):        # Lemma 3.3
    S = x + y + z
    return max(S, F(1, 2) + y, (1 + 2*x - y + z) / 2, (1 + 2*x + y + 3*z) / 3) <= b <= 1
def L31(x, y, z):        # Lemma 3.4
    S = x + y + z
    return max(x + y, F(1, 2) + x, F(1, 2) + y, 1 + x - y - z, 1 - x + y - z, 1 - S/3, (3 + S) / 5,
               (1 + x + y + 2*z) / 3, (2 + 3*z) / 4) <= b <= 1
def S2(x, y, z, T=b):    # Lemma 3.6 (hub template)
    P = max(0, 1 + y - x - z - T); Q = max(0, 1 + x - y - z - T)
    return (x <= T and y <= T and T >= 1 - x + z + P + Q and T >= y + z + Q
            and 2*T >= 1 + y + 2*z + P + 2*Q)
def S1(x, y, z, x1, y1, z1, T=b):  # Lemma 3.5 (symmetric template)
    return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1 + y1 + z1 <= T
            and y1 + z1 >= 1 + x - T and x1 + z1 >= 1 + y - T and x1 + y1 >= 1 + z - T)
def splitA(m, y, z): return ((e + y + z - m) / 2, (e + m + z - y) / 2, (e + m + y - z) / 2)
def splitB(m, y, z): return (e + y - z, e + m - z, z)

# ---- auxiliary inequalities asserted in the text (each must be >= 0 on the case polytope) ----
AUX = {
 'a':  [lambda m, y, z: F(119, 400) - m],
 'b2': [lambda m, y, z: F(146, 200) - (2*m - y + z),             # (1+2m-y+z)/2 <= beta
        lambda m, y, z: F(173, 200) - (m + y + z),
        lambda m, y, z: F(319, 200) - (2*m + y + 3*z)],
 'b3': [lambda m, y, z: F(146, 200) - (2*z - y + m),
        lambda m, y, z: F(319, 200) - (2*z + y + 3*m)],
 'b1': [lambda m, y, z: F(319, 200) - (z + y + 2*m),              # condition 8, tight at m = 23/50
        lambda m, y, z: F(265, 200) - (m + y + z),
        lambda m, y, z: (y + m - z) - e],
 'c':  [lambda m, y, z: F(81, 200) - m,                            # m < 81/200 (closure)
        lambda m, y, z: F(8, 200) - (m - y),
        lambda m, y, z: F(89, 200) - (2*m - y),                    # used in c3 and c4
        lambda m, y, z: F(381, 200) - (2*m + 3*y),                 # used in c2 and c4
        lambda m, y, z: F(235, 200) - (2*m + y)],                  # used in c2
 'c1': [lambda m, y, z: (y - e) - z,                               # 1-y+z <= beta
        lambda m, y, z: (m - y/2) - e, lambda m, y, z: (y - m/2) - e],
 'c2': [lambda m, y, z: (F(319, 200) - 2*(m + y)) - (F(81, 200) - y),   # 319/200-2u >= 81/200-y
        lambda m, y, z: (F(319, 200) - 2*(m + y)) - (y - F(65, 200)),   # 319/200-2u >= y-65/200
        lambda m, y, z: (e + (m - y) - z),                         # P > 0 (closure: >= 0)
        lambda m, y, z: (e - (m - y) - z)],                        # Q > 0 (closure: >= 0)
 'c4': [lambda m, y, z: z - (e + (m - y)),                         # z >= 27/200 + d
        lambda m, y, z: z - ((m + y) - F(119, 200))],              # z >= u - 119/200
}

def region(extra): return BASE + extra
Y73 = ge((0, 1, 0), F(73, 200))
NOT_C1 = ge((2, 2, 1), F(319, 200)); NOT_C2 = ge((-1, 1, -1), -e)   # z >= e - d  <=>  -m+y-z >= -e
cases = {
 'a':   (region([le((1, 0, 0), F(119, 400))]), lambda m, y, z: L18(m)),
 'b2':  (region([ge((1, 0, 0), F(119, 400)), le((0, 1, 0), F(73, 200)), ge((-1, 1, -1), -e)]),
         lambda m, y, z: L32(m, y, z)),
 'b3':  (region([ge((1, 0, 0), F(119, 400)), le((0, 1, 0), F(73, 200)), le((-1, 1, -1), -e),
                 le((1, 1, 1), F(81, 200))]), lambda m, y, z: L32(z, y, m)),
 'b1':  (region([ge((1, 0, 0), F(119, 400)), le((0, 1, 0), F(73, 200)), le((-1, 1, -1), -e),
                 ge((1, 1, 1), F(81, 200))]), lambda m, y, z: L31(z, y, m)),
 'c1':  (region([Y73, le((2, 2, 1), F(319, 200))]), lambda m, y, z: L26(m, y, z)),
 'c2':  (region([Y73, NOT_C1, le((-1, 1, -1), -e)]), lambda m, y, z: S2(y, m, z)),
 'c3':  (region([Y73, NOT_C1, NOT_C2, le((0, 1, 2), F(146, 200))]), lambda m, y, z: S2(m, y, z)),
 'c4A': (region([Y73, NOT_C1, NOT_C2, ge((0, 1, 2), F(146, 200)), ge((-1, -1, 3), e)]),
         lambda m, y, z: S1(m, y, z, *splitA(m, y, z))),
 'c4B': (region([Y73, NOT_C1, NOT_C2, ge((0, 1, 2), F(146, 200)), le((-1, -1, 3), e)]),
         lambda m, y, z: S1(m, y, z, *splitB(m, y, z))),
}
ok_all = True
for name, (cons, test) in cases.items():
    V = vertices(cons)
    bad = [v for v in V if not test(*v)]
    auxkeys = [name] + (['c'] if name.startswith('c') else []) + (['c4'] if name.startswith('c4') else [])
    auxbad = [(k, i, v) for k in auxkeys if k in AUX for i, f in enumerate(AUX[k]) for v in V if f(*v) < 0]
    print(f"{name:4s} vertices={len(V):3d} lemma-failures={len(bad)} aux-failures={len(auxbad)}")
    if bad or auxbad:
        ok_all = False
        print('   ', [tuple(map(str, v)) for v in bad][:3], [(k, i, tuple(map(str, v))) for k, i, v in auxbad][:3])
    assert len(V) > 0, name   # every case region is nonempty

# Exhaustiveness is by construction of the if-chain; double-check on an exact rational grid.
import random
random.seed(2026); miss = 0; N = 0
for _ in range(100000):
    m = h * F(random.randint(0, 10**6), 10**6); y = m * F(random.randint(0, 10**6), 10**6)
    z = y * F(random.randint(0, 10**6), 10**6)
    if m + 2*y > 2 - b: continue
    N += 1
    if not any(all(sum(a*x for a, x in zip(c[0], (m, y, z))) <= c[1] for c in cons) for cons, _ in cases.values()):
        miss += 1
print('random exact points', N, 'outside every case polytope:', miss)
print('ALL PASS' if ok_all and miss == 0 else 'FAILURE')
