"""Referee w9, claim dense#2 (averaging proposition).  Exact tests with Fractions.
For random small families H on N<=12 vertices and partitions pi=(E0,O_1..O_m) (m=2,3):
 T1 identity   f_2(a,b) == sum_U P(U) f_pi(a,U)   (U multivariate hypergeometric)
 T2 Hoeffding  P(U_s < u_s) <= exp(-2 lam^2/b) whenever b*n_s/X >= u_s+lam   (exact hypergeometric tail)
 T3 proposition: (a,u) in A_pi(eta), b>=X max_s (u_s+lam)/n_s, b<=X  =>  f_2(a,b) >= 1-eta-m exp(-2lam^2/b)
 T4 converse (referee's addition): f_2(a,b)>=1-eta => f_pi(a,v)>=1-eta-m exp(-2lam^2/b),
    v_s=min(n_s, ceil(b n_s/X + lam))
 T5 rank identity  a+X h(g) == |g| + sum_s n_s (h-y_s)
 T6 tau* comparison (integer): tau*_int(A_pi) <= tau*_int(A_2)   (averaging: a free 2-part profile has a free
    fine profile of the same size)
No sympy/LP used."""
import itertools, random, math, sys
from fractions import Fraction as F
from math import comb

def profiles_stats(N, edges, parts):
    # contains-edge counts per profile
    idx = {}
    for pi_, P in enumerate(parts):
        for v in P: idx[v] = pi_
    cnt = {}; tot = {}
    emasks = [sum(1 << v for v in E) for E in edges]
    for S in range(1 << N):
        prof = [0]*len(parts)
        for v in range(N):
            if S >> v & 1: prof[idx[v]] += 1
        prof = tuple(prof)
        tot[prof] = tot.get(prof, 0) + 1
        if any(S & em == em for em in emasks):
            cnt[prof] = cnt.get(prof, 0) + 1
    return {p: F(cnt.get(p, 0), tot[p]) for p in tot}

def hyper(b, ns):
    X = sum(ns); out = {}
    for U in itertools.product(*[range(n+1) for n in ns]):
        if sum(U) != b: continue
        p = F(1, comb(X, b))
        for u, n in zip(U, ns): p *= comb(n, u)
        out[U] = p
    return out

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
fails = {k: 0 for k in 'T1 T2 T3 T4 T5 T6'.split()}; checks = {k: 0 for k in fails}
worst_slack = None
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 60):
    N = random.randint(8, 12); m = random.choice([2, 3])
    e = random.randint(2, 4)
    verts = list(range(N)); random.shuffle(verts)
    E0 = verts[:e]; rest = verts[e:]
    cuts = sorted(random.sample(range(1, len(rest)), m-1))
    Os = [rest[i:j] for i, j in zip([0]+cuts, cuts+[len(rest)])]
    ns = [len(o) for o in Os]; X = sum(ns)
    k = random.randint(3, 6)
    nE = random.randint(3, 25)
    edges = [E0] + [random.sample(range(N), random.randint(2, k)) for _ in range(nE)]
    fpi = profiles_stats(N, edges, [E0] + Os)
    f2 = profiles_stats(N, edges, [E0, sum(Os, [])])
    H = {b: hyper(b, ns) for b in range(X+1)}
    # T1
    for (a, b), val in f2.items():
        s = sum(p * fpi[(a,)+U] for U, p in H[b].items())
        checks['T1'] += 1
        if s != val: fails['T1'] += 1
    # T2 exact tail vs Hoeffding
    for b in range(1, X+1):
        for s_ in range(m):
            for u in range(ns[s_]+1):
                lam = F(b*ns[s_], X) - u
                if lam <= 0: continue
                tail = sum(p for U, p in H[b].items() if U[s_] < u)
                checks['T2'] += 1
                if float(tail) > math.exp(-2*float(lam)**2/b) + 1e-12: fails['T2'] += 1
    # T3, T4
    for eta in [F(0), F(1,10), F(1,6), F(1,3)]:
        for (a, *u), val in fpi.items():
            if val < 1 - eta: continue
            for lam in [F(1,2), F(1), F(3,2), F(2), F(3)]:
                need = max(F(X*(u[s_]+lam), ns[s_]) for s_ in range(m))
                for b in range(max(1, math.ceil(need)), X+1):
                    checks['T3'] += 1
                    bound = 1 - float(eta) - m*math.exp(-2*float(lam)**2/b)
                    if float(f2[(a, b)]) < bound - 1e-12: fails['T3'] += 1
        for (a, b), val in f2.items():
            if val < 1 - eta or b == 0: continue
            for lam in [F(1,2), F(1), F(2), F(3)]:
                v = tuple(min(ns[s_], math.ceil(F(b*ns[s_], X) + lam)) for s_ in range(m))
                checks['T4'] += 1
                if float(fpi[(a,)+v]) < 1 - float(eta) - m*math.exp(-2*float(lam)**2/b) - 1e-12:
                    fails['T4'] += 1
        # T6 integer tau*
        free_pi = max((a+sum(u) for (a, *u), v in fpi.items() if v < 1-eta), default=-1)
        free_2 = max((a+b for (a, b), v in f2.items() if v < 1-eta), default=-1)
        checks['T6'] += 1
        if free_pi < free_2: fails['T6'] += 1
    # T5
    for (a, *u) in fpi:
        ys = [F(u[s_], ns[s_]) for s_ in range(m)]; h = max(ys)
        checks['T5'] += 1
        if a + X*h != a + sum(u) + sum(ns[s_]*(h-ys[s_]) for s_ in range(m)): fails['T5'] += 1
print('checks', checks); print('fails', fails)
