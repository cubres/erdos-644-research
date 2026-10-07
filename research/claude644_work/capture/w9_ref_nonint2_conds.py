"""Referee w9 [nonint#2] -- exact checks of the arithmetic of Prop C (fattened 7.97).
(A) literal conditions (0),(1),(2) admit degenerate parameters with c<=delta, where H has nu>=3 (NOT (7,2)).
(B) exact family k=140n,s=98n-1,c=119n-1,delta=7n: every condition, independent of sympy (Fractions; each
    condition is a polynomial of degree<=2 in n: check p(1)>0, and p nondecreasing on [1,inf) via leading
    coefficient >=0 and p'(1)>=0).
(C) continuous optimum of s/k over c (k=1) as a function of delta/k, vs (5-2delta)/7 (NUMERICAL grid, exact Fractions
    at grid points); locate the threshold where (5-2d)/7 stops being attained.
(D) exact integer best-s tables (literal conditions + c>5 delta), compare with Prop B bound 7s<=5k-2delta+24."""
from fractions import Fraction as Fr
import itertools

def conds(k, s, c, d, strict_note=False):
    """Literal statement: (0),(1),(2) plus the implicit set-size constraints 0<=c, 2c<=k+s, c<=k."""
    if not (0 <= c and 2*c <= k+s and c <= k and s >= 0 and d >= 0): return False
    if not 4*s < 3*k: return False
    for a in range(1, 7):
        x = c - a*d
        if not ((x > s and (5-a)*s < 2*k + x) or ((6-a)*s < k + 2*x)): return False
    for a in range(1, 7):
        for b in range(1, 7-a):
            if not (4*(c-a*d)*(c-b*d) > (7-a-b)*s*s): return False
    return True

# (A) degenerate instances
print('(A) literal-condition instances with c<=delta (each has three pairwise disjoint edges):')
cnt = 0
for k in range(1, 40):
    for s in range(0, k):
        for c in range(0, k+1):
            for d in range(1, k):
                if c <= d and conds(k, s, c, d):
                    cnt += 1
                    if cnt <= 8:
                        # explicit three disjoint edges: core edge avoiding C1 u C2 is not needed; take
                        # K1 row = U1 minus (C1 plus d-c other points), K2 row likewise, core row = any k-subset of U.
                        # K1 row is inside D1 u X1 (outside U): size k+d-c-(d-c) = k. Disjoint from U, from U2.
                        print(f'  k={k} s={s} c={c} delta={d}: K1-row=D1uX1 minus (d-c) pts, K2-row likewise, core row in U -> nu>=3')
print('  total such (k<40):', cnt)
# is c>5d implied once c>=d+1 ?
bad = [(k,s,c,d) for k in range(1,40) for s in range(k) for c in range(k+1) for d in range(1,k)
       if c >= d+1 and conds(k,s,c,d) and not c > 5*d]
print('  instances with c>=d+1, conditions hold, but c<=5d:', len(bad))
bad2 = [(k,s,c,d) for k in range(1,40) for s in range(k) for c in range(k+1) for d in range(1,k)
       if conds(k,s,c,d) and not 5*d < k]
print('  instances where conditions hold but 5d>=k:', len(bad2), bad2[:5])

# (B) exact family
print('(B) exact family k=140n, s=98n-1, c=119n-1, d=7n')
def poly(f):
    # f: function of n returning Fraction; recover degree<=2 polynomial by interpolation at n=0,1,2 and verify at 3,4
    v = [Fr(f(Fr(n))) for n in range(5)]
    C0 = v[0]; A = (v[2]-2*v[1]+v[0])/2; B = v[1]-v[0]-A
    for n in range(5): assert A*n*n+B*n+C0 == v[n], 'degree>2'
    return A, B, C0
def pos_n_ge_1(f):
    A, B, C0 = poly(f)
    return (A+B+C0 > 0) and A >= 0 and (2*A+B >= 0)
K = lambda n: 140*n; S = lambda n: 98*n-1; Cc = lambda n: 119*n-1; D = lambda n: 7*n
checks = {}
checks['(0) 3k-4s>0'] = lambda n: 3*K(n)-4*S(n)
checks['U0=k+s-2c >=0 (as >-1)'] = lambda n: K(n)+S(n)-2*Cc(n)+1
checks['|Di|=k-c>0'] = lambda n: K(n)-Cc(n)
checks['tau: s-(2d+1)>=0 (as >-1)'] = lambda n: S(n)-2*D(n)-1+1
checks['tau: c-(d+1)>=0'] = lambda n: Cc(n)-D(n)
checks['Gamma: c-d-s>0'] = lambda n: Cc(n)-D(n)-S(n)
checks['c-5d>0 (needed in case 2)'] = lambda n: Cc(n)-5*D(n)
ok = all(pos_n_ge_1(f) for f in checks.values())
for nm, f in checks.items(): print('  ', nm, pos_n_ge_1(f))
for a in range(1, 7):
    b1 = pos_n_ge_1(lambda n: Cc(n)-a*D(n)-S(n)) and pos_n_ge_1(lambda n: 2*K(n)+Cc(n)-a*D(n)-(5-a)*S(n))
    b2 = pos_n_ge_1(lambda n: K(n)+2*(Cc(n)-a*D(n))-(6-a)*S(n))
    print(f'   (1) a={a}: branch1={b1} branch2={b2}'); ok &= (b1 or b2)
for a in range(1, 7):
    for b in range(1, 7-a):
        r = pos_n_ge_1(lambda n: 4*(Cc(n)-a*D(n))*(Cc(n)-b*D(n))-(7-a-b)*S(n)**2); ok &= r
        if not r: print('   (2) FAIL', a, b)
print('  all exact-family conditions hold for every n>=1:', ok)
print('  margin in (1) a=1 branch1 second part: 2k+c-d-4s =', [2*K(n)+Cc(n)-D(n)-4*S(n) for n in (1,2,3)])

# (C) continuous optimum
print('(C) continuous: max s (k=1) over c, grid; compare (5-2d)/7')
def cont_ok(s, c, d):
    if not (2*c <= 1+s and 4*s < 3): return False
    for a in range(1, 7):
        x = c-a*d
        if not ((x > s and (5-a)*s < 2+x) or ((6-a)*s < 1+2*x)): return False
    for a in range(1, 7):
        for b in range(1, 7-a):
            if not (4*(c-a*d)*(c-b*d) > (7-a-b)*s*s): return False
    return True
N = 400
for dd in [0, Fr(2,100), Fr(4,100), Fr(5,100), Fr(55,1000), Fr(58,1000), Fr(6,100), Fr(65,1000), Fr(7,100), Fr(71,1000), Fr(72,1000), Fr(75,1000), Fr(8,100), Fr(1,10)]:
    target = (5-2*dd)/7
    best = None
    # s slightly below target: test s = target - eps for eps in 1/N^2 grid, c on grid near (1+s)/2
    for epsi in [Fr(1,10**4), Fr(1,10**3), Fr(1,10**2), Fr(3,10**2), Fr(5,10**2)]:
        s = target - epsi
        found = False
        for ci in range(0, 2*N+1):
            c = (1+s)/2 * Fr(ci, 2*N)
            if cont_ok(s, c, dd): found = True; break
        if found: best = epsi; break
    print(f'   d={float(dd):.3f}: (5-2d)/7={float(target):.4f}; feasible at target-eps with eps={best}')

# (D) integer tables, literal + c>5d (i.e. the corrected statement), vs Prop B
print('(D) integer best s (corrected conditions) vs Prop B ceiling (5k-2d+24)/7')
for k in [70, 140, 280, 700]:
    row = []
    for d in [0, k//70, k//35, k//20, k//16, k//14]:
        bs = None
        for s in range(3*k//4, -1, -1):
            if any(conds(k, s, c, d) and c > 5*d and c >= d+1 and s >= 2*d+1 for c in range(k+1)):
                bs = s; break
        row.append((d, bs, None if bs is None else round((bs+1)/k, 4), Fr(5*k-2*d+24, 7) >= bs if bs is not None else None))
    print('  k=%d' % k, row)
