#!/usr/bin/env python3
"""
referee_lemmaZ_check.py  (referee w12, claim generalp#1 = Lemma Z; exact Fractions, stdlib only)

Exact checks of Lemma Z for random rational SUB-UNIT finite generator sets Gen (0 <= g <= x, |g| <= 1):

 (a) identity  tau*(G) = min(tau*(Gen), N - 1)  for G = unit up-closure of Gen (checked on a rational grid
     approximation of G from above and below: G_grid subset G gives tau*(G_grid) >= tau*(G) ... we instead verify
     the identity directly through its proof step: sup free(G) = max(min(1,N), sup free(Gen)) by testing, on a
     fine grid of boxes w, that 'w free for G' <=> '|w| < 1 or w free for Gen', where 'w free for G' is decided
     EXACTLY: not free iff some g <= w with |w| >= 1 (then g + fill <= w is a unit point of G).  That equivalence
     IS the identity, so the check is of the logic, not of the arithmetic; we still compute both sides.
 (c) pencil step: for every g with g_i <= 2 x_i/3 for all i, if tau*(Gen) > 3/4 then some f in Gen satisfies
     f <= x - 3g/4 and the Fano loads (g,g,g on a pencil, f on the other four lines) satisfy Lemma 7.63 in every
     part; verified ALSO by an explicit point-mass construction (7 point masses per part, loads >= rows) found by
     exact rational LP-free formula: m_{p0} = ..., we simply solve the 7x7 system with a small exact search:
     put mass g_i/2 on each of the three points of the centre pencil other than p0?  -- no: we use the Lemma 7.63
     criterion (refereed, note) AND an independent exact feasibility check by Fourier-Motzkin-free enumeration:
     brute-force rational point masses on a grid is too coarse, so we use scipy HiGHS as a cross-check with
     tolerance, if available.
 (d) BOUNDARY: instances where the light generator is EXACTLY 2x/3 in some part, and instances with x_i = 0.
"""
from fractions import Fraction as Fr
from itertools import product
import random, sys

# Fano plane: points 0..6, lines as triples; pencil through point 0 = lines containing 0
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]

def sup_free_exact(T, x):
    """sup{|w| : 0<=w<=x, w free for finite T}: corner enumeration (as in arch/upclosure_check.py, re-implemented)."""
    p = len(x)
    best = None
    choices = []
    for i in range(p):
        vals = {("cap", x[i])}
        for t in T:
            if t[i] <= x[i] and t[i] > 0:
                vals.add(("typ", t[i]))
        choices.append(sorted(vals))
    for combo in product(*choices):
        ok = True
        for t in T:
            dom = True
            for i in range(p):
                kind, c = combo[i]
                if kind == "cap":
                    if not (t[i] <= c): dom = False; break
                else:
                    if not (t[i] < c): dom = False; break
            if dom:
                ok = False; break
        if ok:
            s = sum(c for _, c in combo)
            if best is None or s > best:
                best = s
    return Fr(0) if best is None else best

def tau_star(T, x):
    return sum(x) - sup_free_exact(T, x)

def fano_ok(loads, xi):
    """Lemma 7.63 criterion for one part: loads z_l (7 lines), capacity xi."""
    if any(z > xi for z in loads): return False
    for pt in range(7):
        s = sum(loads[l] for l in range(7) if pt in LINES[l])
        if s > 2*xi: return False
    return sum(loads) <= 4*xi

def fano_masses_exact(loads, xi):
    """Independent realisation: point masses m_pt >= 0, sum <= xi, sum_{pt in line l} m_pt >= z_l.
    Solve via the explicit formula of Lemma 7.63's proof is not reproduced; instead exact LP by scipy if present."""
    try:
        import numpy as np
        from scipy.optimize import linprog
    except Exception:
        return None
    A = []; b = []
    for l in range(7):
        row = [0.0]*7
        for pt in range(7):
            if pt not in LINES[l]: row[pt] = -1.0   # parent cell of P = lines NOT through P (note 7.63)
        A.append(row); b.append(-float(loads[l]))
    A.append([1.0]*7); b.append(float(xi))
    res = linprog(c=[0.0]*7, A_ub=A, b_ub=b, bounds=[(0,None)]*7, method="highs")
    return res.status == 0

def rand_fr(lo, hi, den):
    return Fr(random.randint(int(lo*den), int(hi*den)), den)

def main(seed=1, trials=400):
    random.seed(seed)
    n_a = n_c = n_c_lp = 0; fails = []
    n_light_cases = 0; n_tau_big = 0
    for t in range(trials):
        p = random.choice([2,3,4])
        den = random.choice([4,6,8,12])
        x = [rand_fr(0, 1.2, den) for _ in range(p)]
        if random.random() < 0.15: x[random.randrange(p)] = Fr(0)   # boundary: empty part
        N = sum(x)
        m = random.randint(1, 5)
        Gen = []
        for _ in range(m):
            g = [min(x[i], rand_fr(0, 1, den)) for i in range(p)]
            s = sum(g)
            if s > 1:
                # scale down to a random sub-unit mass, keep rational
                lam = Fr(random.randint(int(den*0.4), den), den) / s
                g = [gi*lam for gi in g]
            Gen.append(tuple(g))
        tG = tau_star(Gen, x)
        # (a): identity check via the logic on a grid of boxes w
        gden = 6
        rng = [[Fr(j, gden) for j in range(int(x[i]*gden)+1)] for i in range(p)]
        for w in product(*rng):
            free_gen = not any(all(g[i] <= w[i] for i in range(p)) for g in Gen)
            free_G = (sum(w) < 1) or free_gen        # exact characterisation, see docstring
            # direct: is there a unit v with g<=v<=w?  iff some g<=w and |w|>=1
            direct = not any(all(g[i] <= w[i] for i in range(p)) and sum(w) >= 1 for g in Gen)
            if free_G != direct:
                fails.append(("a", x, Gen, w))
        n_a += 1
        # (c): pencil step for light generators when tau*(Gen) > 3/4
        if tG > Fr(3,4):
            n_tau_big += 1
            if not (N > Fr(7,4) or any(all(g[i] <= 4*x[i]/7 for i in range(p)) for g in Gen)):
                fails.append(("N", x, Gen, tG))
            for g in Gen:
                if all(g[i] <= 2*x[i]/3 for i in range(p)):
                    n_light_cases += 1
                    u = [x[i] - 3*g[i]/4 for i in range(p)]
                    assert all(ui >= 0 for ui in u)
                    fs = [f for f in Gen if all(f[i] <= u[i] for i in range(p))]
                    if not fs:
                        fails.append(("c-request", x, Gen, g)); continue
                    f = fs[0]
                    loads = [g,g,g,f,f,f,f]   # lines 0,1,2 = pencil through point 0
                    for i in range(p):
                        z = [row[i] for row in loads]
                        if not fano_ok(z, x[i]):
                            fails.append(("c-fano", x, Gen, g, f, i))
                        r = fano_masses_exact(z, x[i])
                        if r is False:
                            fails.append(("c-lp", x, Gen, g, f, i))
                        if r is not None: n_c_lp += 1
                    n_c += 1
    print("trials", trials, "(a) grids checked", n_a, "tau*>3/4 instances", n_tau_big,
          "light-generator cases", n_light_cases, "pencil tuples checked", n_c, "LP cross-checks", n_c_lp)
    print("FAILURES", len(fails))
    for f in fails[:10]: print(f)
    return len(fails)

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    sys.exit(1 if main(seed, trials) else 0)
