# exact library for two-part two-type template analysis
import json, itertools
from fractions import Fraction as F
D = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tmpl/astra_support_capacity_minimal.json'))
FUNCS = [[(F(u),F(v)) for u,v in f['vertices']] for f in D['minimal_functions']]
def M(k, s, t):
    return max(u*s+v*t for u,v in FUNCS[k])
def feasible(k, x, y, al, be):
    return M(k, al, be) <= x and M(k, 1-al, 1-be) <= y

def solve(A, b):
    # exact gaussian elimination, square system; return None if singular
    n = len(A)
    Mx = [list(map(F,A[i]))+[F(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c,n) if Mx[r][c]!=0), None)
        if p is None: return None
        Mx[c],Mx[p] = Mx[p],Mx[c]
        for r in range(n):
            if r!=c and Mx[r][c]!=0:
                f = Mx[r][c]/Mx[c][c]
                Mx[r] = [Mx[r][j]-f*Mx[c][j] for j in range(n+1)]
    return [Mx[i][n]/Mx[i][i] for i in range(n)]

def vertices(cons, dim):
    # cons: list of (coef list, const) meaning coef.z + const >= 0
    V = set()
    for S in itertools.combinations(range(len(cons)), dim):
        A = [cons[i][0] for i in S]; b = [-cons[i][1] for i in S]
        z = solve(A, b)
        if z is None: continue
        if all(sum(F(c)*zz for c,zz in zip(co,z))+F(k) >= 0 for co,k in cons):
            V.add(tuple(z))
    return sorted(V)
