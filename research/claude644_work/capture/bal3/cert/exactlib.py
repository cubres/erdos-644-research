def eval_row(r, z):
    val = sum(float(c) * z[IX[k]] for k, c in r[0].items())
    return val < float(r[1]) - 1e-9 if r[2] else val <= float(r[1]) + 1e-9
def lp(rows):
    """max t s.t. strict rows: a.z + t <= b ; nonstrict a.z <= b ; t <= 1. returns (t*, z, duals)"""
    n = len(V); M = len(rows)
    A = np.zeros((M + 1, n + 1)); b = np.zeros(M + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, IX[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[M, n] = 1.0; b[M] = 1.0
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * (n + 1), method='highs')
    if res.status == 2: return -np.inf, None, None
    return -res.fun, res.x, -res.ineqlin.marginals
def exact_cert(rows):
    """exact Motzkin certificate: lam>=0 over rows, sum lam*a = 0, sum lam*b < 0 or (=0 and strict weight>0)"""
    t, z, du = lp(rows)
    if t > 1e-9: return None
    if du is None:
        # phase-1 infeasible even without strictness: find Farkas via LP on nonstrict relaxation with t fixed
        rows2 = [(c, r, False) for c, r, s in rows]
        return exact_cert_nonstrict(rows2)
    M = len(rows)
    supp = [k for k in range(M) if du[k] > 1e-11]
    return solve_exact(rows, supp, du)
def exact_cert_nonstrict(rows):
    # Farkas: min 0 s.t. ... use linprog on dual: find lam>=0, lam A = 0, lam b = -1
    n = len(V); M = len(rows)
    Aeq = np.zeros((n + 1, M)); beq = np.zeros(n + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): Aeq[IX[v], k] = float(c)
        Aeq[n, k] = float(rhs)
    beq[n] = -1.0
    res = linprog(np.ones(M), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method='highs')
    if res.status != 0: return None
    supp = [k for k in range(M) if res.x[k] > 1e-11]
    return solve_exact(rows, supp, res.x, nonstrict=True)
def solve_exact(rows, supp, du, nonstrict=False):
    import sympy as sp
    n = len(V)
    lam = sp.symbols('l0:%d' % len(supp))
    eqs = []
    for j, v in enumerate(V):
        eqs.append(sum(sp.Rational(rows[k][0].get(v, 0)) * lam[q] for q, k in enumerate(supp)))
    # normalisation
    if nonstrict:
        eqs.append(sum(sp.Rational(rows[k][1]) * lam[q] for q, k in enumerate(supp)) + 1)
    else:
        eqs.append(sum((1 if rows[k][2] else 0) * lam[q] for q, k in enumerate(supp)) - 1)
    sol = sp.linsolve(eqs, lam)
    if not sol: return None
    sol = list(sol)[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    if free:
        guess = {lam[q]: sp.Rational(F(du[k]).limit_denominator(10**8)) for q, k in enumerate(supp)}
        sol = [e.subs({f: guess[f] for f in free}) for e in sol]
    L = [F(str(v)) for v in sol]
    if any(v < 0 for v in L): return None
    # exact verification
    for v in V:
        if sum(l * rows[k][0].get(v, 0) for l, k in zip(L, supp)) != 0: return None
    val = sum(l * rows[k][1] for l, k in zip(L, supp))
    sw = sum(l for l, k in zip(L, supp) if rows[k][2])
    if val < 0 or (val == 0 and sw > 0):
        return [(k, l) for k, l in zip(supp, L)]
    return None
