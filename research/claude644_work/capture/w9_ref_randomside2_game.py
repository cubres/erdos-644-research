# Referee w9, claim randomside#2: independent spot checks of the Game Theorem V(n) >= psi(n-3/4).
# (1) Near corner: rebuild the cert_near2 strategy y(d) = a + d(b0 + kappa/ln(1/d) b1) from its published data with MY
#     OWN quad-correction solver (exact Fractions, Gaussian elimination) and MY OWN step-entropy evaluator (mpmath, 80
#     digits), and evaluate min_j e_j(y(d)) - psi(1+d) at d = 0.03 .. 1e-80.  Also check feasibility (y>=0, line sums 1,
#     total 7/4+d, only safe cells).
# (2) Proportional greedy (hand proof n >= 4.75): simulate the continuous greedy on Venn cells for every line order whose
#     first three lines are non-concurrent, n in a grid of [4.75, 200]; check min_j a_j >= n - 3/4.
import itertools
from fractions import Fraction as F
from mpmath import mp, mpf, log
mp.dps = 80
LINES = [frozenset(((i) % 7, (i+1) % 7, (i+3) % 7)) for i in range(7)]   # attacker's labelling (data refer to it)
def safe(S):
    u = set()
    for l in S: u |= LINES[l]
    return len(u) < 7
SAFE = [tuple(S) for r in range(8) for S in itertools.combinations(range(7), r) if safe(S)]
QUADS = [S for S in SAFE if len(S) == 4]
T6 = [(0,1,3),(0,2,5),(2,3,4),(1,4,5)]; T5 = [(1,2,3),(0,3,4),(0,2,6),(1,4,6)]
T4 = [(0,3,6),(0,3,5),(0,1,2),(2,3,6),(2,3,5),(0,2,4),(1,5,6)]
T3 = [(1,3,6),(0,1,6),(1,3,5),(1,2,5),(0,5,6),(1,2,4),(0,1,4),(0,4,5),(2,4,6),(2,5,6)]
for S in T6+T5+T4+T3: assert S in SAFE, S
xi0 = {S: F(0) for S in SAFE}; eta = {S: F(0) for S in SAFE}
for S in T6+T5: xi0[S] = F(1,4)
for S in T4: xi0[S] = F(1,7)
for S in T3: xi0[S] = F(1,10)
for S in T6: eta[S] = F(1,4)
for S in T4: eta[S] = F(-1,7)
kappa = F(1,5)
def solve(A, b):   # exact Gaussian elimination, square nonsingular
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [M[r][i] - f*M[c][i] for i in range(n+1)]
    return [M[i][n] / M[i][i] for i in range(n)]
A = [[F(1) if l in Q else F(0) for Q in QUADS] for l in range(7)]
def fill(v):
    w = dict(v)
    rhs = [-sum(v[S] for S in SAFE if l in S and len(S) < 4) for l in range(7)]
    q = solve(A, rhs)
    for Q, x in zip(QUADS, q): w[Q] = x
    return w
b0 = fill(xi0); b1 = fill(eta)
a = {S: (F(1,4) if len(S) == 4 else F(0)) for S in SAFE}
def y_of(d):
    L = -log(d); u = 1/L
    return {S: mpf(a[S].numerator)/a[S].denominator + d*(mpf(b0[S].numerator)/b0[S].denominator
             + mpf(kappa.numerator)/kappa.denominator*u*mpf(b1[S].numerator)/b1[S].denominator) for S in SAFE}
def xl(x): return x*log(x) if x > 0 else mpf(0)
def step_ents(y, order):
    out = []
    for j, lj in enumerate(order):
        prev = set(order[:j]); G = {}
        for S in SAFE:
            key = frozenset(set(S) & prev); z, w = G.get(key, (mpf(0), mpf(0)))
            G[key] = (z + y[S], w + (y[S] if lj in S else 0))
        out.append(sum(xl(z) - xl(w) - xl(z-w) for z, w in G.values()))
    return out
def psi(x): return xl(x) - xl(x-1)
print("(1) near-corner strategy of cert_near2, independent evaluation")
worst = None
ds = [mpf('0.03'), mpf('0.02'), mpf('0.01'), mpf('0.005')] + [mpf(10)**(-e) for e in range(3, 81, 3)]
for d in ds:
    y = y_of(d)
    assert min(y.values()) >= 0, ("negative cell", d)
    for l in range(7): assert abs(sum(y[S] for S in SAFE if l in S) - 1) < mpf(10)**-70
    assert abs(sum(y.values()) - (mpf(7)/4 + d)) < mpf(10)**-70
    e = step_ents(y, list(range(7)))
    g = (min(e) - psi(1+d)) / d
    worst = g if worst is None else min(worst, g)
    print(f"  d={mp.nstr(d,3):>8}: min_j e_j - psi(1+d) = d * {mp.nstr(g,6)}   (binding step {e.index(min(e))})")
print("  worst normalised margin:", mp.nstr(worst, 6))
print("(2) proportional greedy")
def greedy(n, order):
    cells = {frozenset(): mpf(n)}; amin = None
    for lj in order:
        allowed = {T: z for T, z in cells.items() if safe(tuple(T | {lj}))}
        aj = sum(allowed.values()); amin = aj if amin is None else min(amin, aj)
        new = {}
        for T, z in cells.items():
            if T in allowed:
                new[T | {lj}] = new.get(T | {lj}, 0) + z/aj
                new[T] = new.get(T, 0) + z - z/aj
            else: new[T] = new.get(T, 0) + z
        cells = new
    assert all(safe(tuple(T)) for T, z in cells.items() if z > 0)
    return amin
worst2 = None; nord = 0
for order in itertools.permutations(range(7)):
    l1, l2, l3 = order[:3]
    if LINES[l1] & LINES[l2] & LINES[l3]: continue     # concurrent first three: skip (proof uses a triangle)
    nord += 1
    if nord % 97: continue                               # sample of orders
    for n in [4.75, 4.8, 5, 6, 8, 12, 20, 50, 200]:
        g = greedy(n, order) - (mpf(n) - mpf(3)/4)
        worst2 = g if worst2 is None else min(worst2, g)
print(f"  sampled orders (of {nord} triangle-first): min_j a_j - (n-3/4) over grid = {mp.nstr(worst2,6)}")
