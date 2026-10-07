# Independent referee check of S1/S2 static templates (exact integers, no imports from handbound code).
# 1) Build actual E,F,G (sizes r, empty common intersection) + one outside point, requests per template,
#    responses = complement of request (worst case), verify NO 2-transversal among the 7 edges.
# 2) S2: stated conditions  <=>  exists integer (p,q,x01) making all four request sizes <= T (template-exact).
# 3) S1: continuous closed form vs integer feasibility (reports integer gaps, not claimed either way).
import itertools, sys
from fractions import Fraction as Fr

def no_two_transversal(edges, V):
    for u in V:
        for v in V:
            if all((u in e) or (v in e) for e in edges): return False
    return True

def build(r, x, y, z):
    c = itertools.count()
    mk = lambda n: [next(c) for _ in range(n)]
    X, Y, Z = mk(x), mk(y), mk(z)          # X=A&B, Y=A&C, Z=B&C
    PA, PB, PC = mk(r-x-y), mk(r-x-z), mk(r-y-z)
    out = mk(1)
    V = set(range(next(c)))
    A = set(X+Y+PA); B = set(X+Z+PB); C = set(Y+Z+PC)
    assert len(A) == len(B) == len(C) == r and not (A & B & C)
    return V, A, B, C, X, Y, Z, PA, PB, PC

def check_S1(r, x, y, z, T, x1, y1, z1):
    V, A, B, C, X, Y, Z, PA, PB, PC = build(r, x, y, z)
    X1, X2 = set(X[:x1]), set(X[x1:]); Y1, Y2 = set(Y[:y1]), set(Y[y1:]); Z1, Z2 = set(Z[:z1]), set(Z[z1:])
    R = [set(X) | set(PC) | Y2 | Z2, set(Y) | set(PB) | X2 | Z2, set(Z) | set(PA) | X2 | Y2, X1 | Y1 | Z1]
    assert all(len(Ri) <= T for Ri in R)
    edges = [A, B, C] + [V - Ri for Ri in R]
    return no_two_transversal(edges, V)

def S2_cond(r, x, y, z, T):
    P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
    return T >= r-x+z+P+Q and T >= y+z+Q and 2*T >= r+y+2*z+P+2*Q and x <= T and y <= T and T <= r

def S2_sizes(r, x, y, z, p, q, x01):
    return [x + (r-y-z-q), x01 + y + z + (r-x-y) + p + q, y + (r-x-z-p), (x-x01) + y + z + q]

def S2_exists(r, x, y, z, T):
    for p in range(r-x-z+1):
        for q in range(r-y-z+1):
            for x01 in range(x+1):
                if max(S2_sizes(r, x, y, z, p, q, x01)) <= T: return (p, q, x01)
    return None

def check_S2(r, x, y, z, T, p, q, x01):
    V, A, B, C, X, Y, Z, PA, PB, PC = build(r, x, y, z)
    PB1, PB2 = set(PB[:p]), set(PB[p:]); PC13, PC0 = set(PC[:q]), set(PC[q:])
    X01, X03 = set(X[:x01]), set(X[x01:])
    R = [set(X) | PC0, X01 | set(Y) | set(Z) | set(PA) | PB1 | PC13, set(Y) | PB2, X03 | set(Y) | set(Z) | PC13]
    assert all(len(Ri) <= T for Ri in R), [len(Ri) for Ri in R]
    edges = [A, B, C] + [V - Ri for Ri in R]
    return no_two_transversal(edges, V)

def S1_cont(r, x, y, z, T):
    S = x+y+z
    return (5*T >= 3*r+S and all(2*T >= r+w for w in (x, y, z)) and
            T >= r+x-y-z and T >= r+y-x-z and T >= r+z-x-y and
            3*T >= 2*r+x+y-z and 3*T >= 2*r+x+z-y and 3*T >= 2*r+y+z-x)

def S1_int(r, x, y, z, T):
    for x1 in range(x+1):
        for y1 in range(y+1):
            for z1 in range(z+1):
                if x1+y1+z1 <= T and y1+z1 >= r+x-T and x1+z1 >= r+y-T and x1+y1 >= r+z-T:
                    return (x1, y1, z1)
    return None

stats = dict(S1_int=0, S1_badcheck=0, S1_cont_not_int=0, S1_int_not_cont=0,
             S2_cond=0, S2_cond_not_exist=0, S2_exist_not_cond=0, S2_badcheck=0)
gaps = []
for r in range(1, int(sys.argv[1]) if len(sys.argv) > 1 else 13):
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x, y)):
                for T in range(r+1):
                    s = S1_int(r, x, y, z, T); c = S1_cont(r, x, y, z, T)
                    if s:
                        stats['S1_int'] += 1
                        if not check_S1(r, x, y, z, T, *s): stats['S1_badcheck'] += 1
                        if not c: stats['S1_int_not_cont'] += 1
                    elif c:
                        stats['S1_cont_not_int'] += 1
                        if len(gaps) < 5: gaps.append((r, x, y, z, T))
                    cond = S2_cond(r, x, y, z, T); ex = S2_exists(r, x, y, z, T)
                    if cond:
                        stats['S2_cond'] += 1
                        P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
                        x01 = min(x, T-r+x-z-P-Q)
                        if not check_S2(r, x, y, z, T, P, Q, x01): stats['S2_badcheck'] += 1
                        if not ex: stats['S2_cond_not_exist'] += 1
                    elif ex and T <= r:
                        stats['S2_exist_not_cond'] += 1
print(stats)
print('S1 continuous-feasible but integer-infeasible examples (r,x,y,z,T):', gaps)
