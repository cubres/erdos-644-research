"""EXACT symbolic check (sympy, rational polynomials in n) that the parametric family
k=140n, s=98n-1, c=119n-1, delta=7n satisfies every sufficient condition of Prop C for ALL integers n>=1.
Each condition is 'poly(n) > 0'; we verify poly has nonnegative-after-shift form: poly(n+1) has all
coefficients >= 0 with positive constant term (so poly(m) > 0 for every integer m >= 1)."""
import sympy as sp
n, m = sp.symbols('n m', integer=True, positive=True)
k, s, c, d = 140*n, 98*n-1, 119*n-1, 7*n
conds = []
conds.append(('case0 3k-4s', 3*k-4*s))
conds.append(('Gamma: c-d-s', c-d-s))
conds.append(('fit: k+s-2c >= 0', k+s-2*c+1))   # >=0  <=> +1 >0
conds.append(('tau: s+1-(2d+2) >= 0', s+1-2*d-2+1))
for a in range(1, 7):
    x = c-a*d
    b1 = [x-s, 2*k+x-(5-a)*s]        # bracket 1 (both >0)
    b2 = [k+2*x-(6-a)*s]             # bracket 2
    conds.append((f'case1 a={a}', (b1, b2)))
for a in range(1, 7):
    for b in range(1, 7-a):
        j = 7-a-b
        conds.append((f'case2 a={a} b={b}', 4*(c-a*d)*(c-b*d) - j*s*s))
def pos_all(p):
    q = sp.Poly(sp.expand(p.subs(n, m+1)), m)   # n = m+1, m >= 0
    co = q.all_coeffs()
    return all(cf >= 0 for cf in co) and co[-1] > 0
ok = True
for name, p in conds:
    if isinstance(p, tuple):
        b1, b2 = p
        r = all(pos_all(x) for x in b1) or all(pos_all(x) for x in b2)
    else:
        r = pos_all(p)
    print(name, 'OK' if r else 'FAIL'); ok &= r
print('ALL CONDITIONS HOLD FOR EVERY n>=1' if ok else 'SOME CONDITION FAILS')
