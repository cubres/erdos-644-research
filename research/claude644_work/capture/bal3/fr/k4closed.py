"""Closed form of the K4 template.  Per part: m_a,m_b,m_c >= 0, m_b+m_c >= t1, m_a+m_c >= t2, m_a+m_b >= t3,
m_a+m_b+m_c <= g (= x - t4).  Globally sum_i m_j,i <= L for j=a,b,c.
Test: feasibility <=> [per-part: max t <= g, sum t <= 2g] and for rho in a finite list: sum_i h_i(rho) <= L*|rho|,
h_i(rho) = min over the per-part polytope of rho.m (computed by LP here; closed forms conjectured separately)."""
import numpy as np, itertools, random
from scipy.optimize import linprog
def perpart_min(t, g, rho):
    A = [[0, -1, -1], [-1, 0, -1], [-1, -1, 0], [1, 1, 1]]; b = [-t[0], -t[1], -t[2], g]
    r = linprog(rho, A_ub=A, b_ub=b, bounds=[(0, None)]*3, method='highs')
    return r.fun if r.status == 0 else None
def full(ts, gs, L):
    # ts: list over parts of (t1,t2,t3); gs: list of g
    p = len(gs); nv = 9
    A = []; b = []
    for i in range(p):
        for (row, rhs) in [([0, -1, -1], -ts[i][0]), ([-1, 0, -1], -ts[i][1]), ([-1, -1, 0], -ts[i][2]), ([1, 1, 1], gs[i])]:
            r = np.zeros(nv); r[3*i:3*i+3] = row; A.append(r); b.append(rhs)
    for j in range(3):
        r = np.zeros(nv); r[[3*i+j for i in range(p)]] = 1; A.append(r); b.append(L)
    res = linprog(np.zeros(nv), A_ub=np.array(A), b_ub=b, bounds=[(0, None)]*nv, method='highs')
    return res.status == 0
RHOS = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1),(2,1,1),(1,2,1),(1,1,2),(3,1,1),(1,3,1),(1,1,3),(2,2,1),(2,1,2),(1,2,2)]
def crit(ts, gs, L, rhos=RHOS):
    for i in range(len(gs)):
        if max(ts[i]) > gs[i] + 1e-12 or sum(ts[i]) > 2*gs[i] + 1e-12: return False
    for rho in rhos:
        s = sum(perpart_min(ts[i], gs[i], rho) for i in range(len(gs)))
        if s > L*sum(rho) + 1e-9: return False
    return True
rng = random.Random(1); bad = 0; n = 0
for trial in range(3000):
    p = 3
    ts = [[rng.random()**2 for _ in range(3)] for _ in range(p)]
    # normalise each type (column j) to sum 1
    for j in range(3):
        s = sum(ts[i][j] for i in range(p))
        for i in range(p): ts[i][j] /= s
    gs = [max(max(ts[i]), sum(ts[i])/2) + rng.random()*0.3 for i in range(p)]
    L = rng.uniform(0.4, 0.9)
    a, c = full(ts, gs, L), crit(ts, gs, L)
    n += 1
    if a != c: bad += 1
print('mismatches', bad, 'of', n)
# which rhos are ever binding (needed)?
need = {}
for trial in range(3000):
    ts = [[rng.random()**2 for _ in range(3)] for _ in range(3)]
    for j in range(3):
        s = sum(ts[i][j] for i in range(3))
        for i in range(3): ts[i][j] /= s
    gs = [max(max(ts[i]), sum(ts[i])/2) + rng.random()*0.3 for i in range(3)]
    L = rng.uniform(0.4, 0.9)
    if full(ts, gs, L): continue
    if not crit(ts, gs, L, []): continue   # per-part infeasible
    viol = [rho for rho in RHOS if sum(perpart_min(ts[i], gs[i], rho) for i in range(3)) > L*sum(rho) + 1e-9]
    key = tuple(sorted(viol))
    for rho in viol: need[rho] = need.get(rho, 0) + 1
    if len(viol) == 1: need[('only',) + viol[0]] = need.get(('only',) + viol[0], 0) + 1
print(need)
