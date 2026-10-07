"""Type-closed k-uniform families over p parts: exact tau and exact (7,2) test via the complete
bad-support catalogue (715 S7-orbits, logs/astra_full_support_catalog.json).
Family: H_T = {k-sets E : profile(E) in T}. T given by a predicate on integer profiles OR (for
parity-check / code families) by values c_i in F_2^r per part and a target a.
(7,2) test: for each support (maximal cells M_1..M_m), ILP: y[i][j]>=0 int, sum_j y[i][j] = n_i;
window w^l_i = sum_{j: l in M_j} y[i][j];  row l needs u^l <= w^l with u^l in T.
A vertex whose cell is M_j may be left out of some rows (u^l <= w^l), so down-closure is automatic."""
import json, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
CAT = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json'))
SUPPORTS = [row['maximal_cells'] for row in CAT['orbits']]
FANO_IDX = None
for idx, cells in enumerate(SUPPORTS):
    if len(cells) == 7 and all(bin(c).count('1') == 4 for c in cells):
        FANO_IDX = idx; break

def order_supports():
    o = list(range(len(SUPPORTS)))
    if FANO_IDX is not None: o.remove(FANO_IDX); o = [FANO_IDX] + o
    return o

def code_ilp(n, c, a, k, cells, time_limit=60):
    """feasibility ILP for a code family: parts sizes n, part values c[i] (tuple of bits), target a."""
    p = len(n); r = len(a); m = len(cells)
    # variable layout: y (p*m), u (7*p), z (7*r)
    ny = p*m; nu = 7*p; nz = 7*r; nv = ny+nu+nz
    Y = lambda i,j: i*m+j; U = lambda l,i: ny+l*p+i; Z = lambda l,b: ny+nu+l*r+b
    rows=[]; lo=[]; hi=[]
    for i in range(p):
        row=np.zeros(nv); row[[Y(i,j) for j in range(m)]]=1; rows.append(row); lo.append(n[i]); hi.append(n[i])
    for l in range(7):
        for i in range(p):  # u^l_i - sum_{j: l in M_j} y_ij <= 0
            row=np.zeros(nv); row[U(l,i)]=1
            for j in range(m):
                if cells[j]>>l & 1: row[Y(i,j)]=-1
            rows.append(row); lo.append(-np.inf); hi.append(0)
        row=np.zeros(nv); row[[U(l,i) for i in range(p)]]=1; rows.append(row); lo.append(k); hi.append(k)
        for b in range(r):
            row=np.zeros(nv)
            for i in range(p):
                if c[i][b]: row[U(l,i)]=1
            row[Z(l,b)]=-2; rows.append(row); lo.append(a[b]); hi.append(a[b])
    A=np.array(rows)
    ub=np.full(nv, np.inf); lb=np.zeros(nv)
    for i in range(p):
        for j in range(m): ub[Y(i,j)]=n[i]
        for l in range(7): ub[U(l,i)]=n[i]
    for l in range(7):
        for b in range(r): lb[Z(l,b)]=-np.inf
    res=milp(c=np.zeros(nv), constraints=LinearConstraint(A,lo,hi), integrality=np.ones(nv),
             bounds=Bounds(lb,ub), options={'time_limit':time_limit,'disp':False})
    if res.status==0: 
        y=[[int(round(res.x[Y(i,j)])) for j in range(m)] for i in range(p)]
        return True, y
    if res.status==2: return False, None   # infeasible
    return None, res.message

def is72_code(n, c, a, k, verbose=False):
    for idx in order_supports():
        ok, y = code_ilp(n, c, a, k, SUPPORTS[idx])
        if ok is None: return None, (idx, y)
        if ok: return False, (idx, SUPPORTS[idx], y)
    return True, None

def dominates_type(w, c, a, k):
    """does profile w dominate some u with |u|=k and sum u_i c_i = a (mod 2)?"""
    p=len(w); r=len(a)
    if sum(w) < k: return False
    supp=[i for i in range(p) if w[i]>0]
    for mask in range(1<<len(supp)):
        J=[supp[t] for t in range(len(supp)) if mask>>t&1]
        if (len(J)-k)%2: continue
        s=[0]*r
        for i in J:
            for b in range(r): s[b]^=c[i][b]
        if tuple(s)!=tuple(a): continue
        mx=0
        for i in range(p):
            if i in J: mx += w[i] if w[i]%2==1 else w[i]-1
            else: mx += w[i] if w[i]%2==0 else w[i]-1
        if len(J) <= k <= mx: return True
    return False

def tau_code(n, c, a, k):
    """tau = N - alpha, alpha = max |w| over edge-free profiles."""
    N=sum(n); best=-1
    for w in itertools.product(*[range(x+1) for x in n]):
        s=sum(w)
        if s>best and not dominates_type(w,c,a,k): best=s
    return N-best
