#!/usr/bin/env python3
"""Referee (one-sided boxes, Thm 8.4): independent EXACT checks, Fractions only.
(1) enumerate vertices of D = Tri^3 x [0,7/4] cap {sum th + xL >= 1} cap {sum d + 3xL/7 >= 3/4}
    and test that every vertex is a product vertex (each (x,th) in {(0,0),(1,1),(7/4,1)}, xL in {0,7/4});
(2) also enumerate vertices of the relaxations without each cut, to see which constraint matters;
(3) at every vertex, build the explicit step-5 construction (rows entirely in own tight/Fano box, rows of
    empty boxes into a host) and check Lemma 7.63's per-part criterion + row sums + thresholds exactly;
(4) independently, sample exact rational points of D as convex combinations and check the combined
    construction (sanity of the convexity step with the SAME template roles)."""
import itertools, random
from fractions import Fraction as F

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]   # rows = lines
# template: quadrilateral missing point 6 = lines 0,1,3,6 -> A ; lines 2,4 (through 6) -> B ; line 5 -> C
ROLE = {0:'A',1:'A',3:'A',6:'A',2:'B',4:'B',5:'C'}
assert all(6 not in LINES[l] for l in ROLE if ROLE[l]=='A')
assert all(6 in LINES[l] for l in ROLE if ROLE[l]!='A')

def part_ok(z, x):
    """Lemma 7.63 criterion; z[l] = trace of row l (row indexed by line l). Rows are lines, so
    'lines of the row-plane' are the pencils: for each point q the three lines through q."""
    if any(v < 0 or v > x for v in z): return False
    for q in range(7):
        if sum(z[l] for l in range(7) if q in LINES[l]) > 2*x: return False
    return sum(z) <= 4*x

names = ['xA','tA','xB','tB','xC','tC','xL']
n = 7
def row(d, c):
    a = [F(0)]*n
    for k, v in d.items(): a[names.index(k)] = F(v)
    return (a, F(c))       # a.v + c >= 0
base = []
for P in 'ABC':
    xs, ts = 'x'+P, 't'+P
    base += [row({ts:1, xs:F(-4,7)},0), row({xs:1, ts:-1},0), row({ts:-1},1)]
base += [row({'xL':1},0), row({'xL':-1},F(7,4))]
cut1 = row({'tA':1,'tB':1,'tC':1,'xL':1}, -1)
cut2 = row({'xA':1,'tA':-1,'xB':1,'tB':-1,'xC':1,'tC':-1,'xL':F(3,7)}, F(-3,4))

def solve(rows):
    M = [a[:]+[-c] for a,c in rows]; r = 0
    for col in range(n):
        pr = next((i for i in range(r,len(M)) if M[i][col] != 0), None)
        if pr is None: return None
        M[r], M[pr] = M[pr], M[r]; pv = M[r][col]; M[r] = [v/pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [a-f*b for a,b in zip(M[i],M[r])]
        r += 1
    return [M[i][n] for i in range(n)]

def vertices(dom):
    vs = set()
    for S in itertools.combinations(range(len(dom)), n):
        sol = solve([dom[i] for i in S])
        if sol and all(sum(a*v for a,v in zip(d[0],sol))+d[1] >= 0 for d in dom): vs.add(tuple(sol))
    return sorted(vs)

TRI = {(F(0),F(0)),(F(1),F(1)),(F(7,4),F(1))}
def is_product(v):
    return all((v[2*i],v[2*i+1]) in TRI for i in range(3)) and v[6] in (F(0),F(7,4))

def construction(v):
    """explicit step-5 construction; returns dict part -> list of 7 traces, or None"""
    P = dict(zip(names, v))
    kind = {}
    for B in 'ABC':
        xt = (P['x'+B], P['t'+B])
        kind[B] = {(0,0):'empty',(1,1):'tight',(F(7,4),1):'fano'}[xt]
    hosts = [B for B in 'ABC' if kind[B]=='fano'] + (['L'] if P['xL']==F(7,4) else [])
    if not hosts: return None
    h = hosts[0]
    tr = {Q:[F(0)]*7 for Q in 'ABCL'}
    for l in range(7):
        B = ROLE[l]
        tgt = B if kind[B] in ('tight','fano') else h
        tr[tgt][l] = F(1)
    return tr, P

def check_construction(tr, P):
    cap = {'A':P['xA'],'B':P['xB'],'C':P['xC'],'L':P['xL']}
    th = {'A':P['tA'],'B':P['tB'],'C':P['tC']}
    for Q in 'ABCL':
        if not part_ok(tr[Q], cap[Q]): return False, 'part '+Q
    for l in range(7):
        if sum(tr[Q][l] for Q in 'ABCL') != 1: return False, 'rowsum'
        if tr[ROLE[l]][l] < th[ROLE[l]]: return False, 'threshold'
    return True, ''

if __name__ == '__main__':
    V = vertices(base + [cut1, cut2])
    print('vertices of D:', len(V), ' all product:', all(is_product(v) for v in V))
    for v in V:
        if not is_product(v): print('  NON-PRODUCT', [str(t) for t in v])
    V1 = vertices(base + [cut2]); V2 = vertices(base + [cut1])
    print('without cut1 (sum th + xL>=1):', len(V1), 'all product:', all(is_product(v) for v in V1))
    print('without cut2 (tau* cut):', len(V2), 'all product:', all(is_product(v) for v in V2),
          ' non-product examples:', [[str(t) for t in v] for v in V2 if not is_product(v)][:3])
    bad = 0; sols = {}
    for v in V:
        c = construction(v)
        if c is None: print('  NO HOST at', [str(t) for t in v]); bad += 1; continue
        ok, why = check_construction(*c)
        if not ok: print('  FAIL', why, [str(t) for t in v]); bad += 1
        sols[v] = c[0]
    print('explicit step-5 construction fails at', bad, 'vertices')
    # convex combinations: combine vertex solutions with same weights -> must be feasible (linearity)
    rng = random.Random(8); cnt = 0
    for _ in range(3000):
        k = rng.randint(2, 6); vs = rng.sample(V, k)
        w = [F(rng.randint(1, 20)) for _ in vs]; s = sum(w); w = [t/s for t in w]
        pt = [sum(wi*v[j] for wi, v in zip(w, vs)) for j in range(n)]
        tr = {Q:[sum(wi*sols[v][Q][l] for wi, v in zip(w, vs)) for l in range(7)] for Q in 'ABCL'}
        ok, why = check_construction(tr, dict(zip(names, pt)))
        if not ok: print('  COMBINATION FAIL', why); break
        cnt += 1
    print('convex-combination checks passed:', cnt)
