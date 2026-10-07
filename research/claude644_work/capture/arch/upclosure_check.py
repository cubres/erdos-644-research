#!/usr/bin/env python3
"""
upclosure_check.py  (architecture agent, 24 Sep 2026; exact Fractions, stdlib only)

Exact checks for two glue facts of PROOF_ARCHITECTURE.md.

 G4 (real up-closure at unit rank).  Let C be a finite set of unit types (|c| = 1, 0 <= c <= x) over p parts with
    rational capacities x, N = |x|.  U(C) := { v : |v| = 1, v <= x, v >= c for some c in C }.  Then
        tau*(U(C)) = min( tau*(C), N - 1 ).
    (Proof in the architecture file: w is free for U(C) iff |w| < 1 or w is free for C; so
     sup free(U(C)) = max(sup free(C), 1) and tau* = N - that.)  Bad tuples of U(C) trim to bad tuples of C.
    Here tau* uses the sup semantics of note 7.76: tau*(T) = N - sup{|w| : 0 <= w <= x, no t in T with t <= w}.
    For a finite T the sup is computed exactly: free boxes are unions of boxes with corners at type coordinates,
    so sup free = max over "corner" boxes w with w_i in {x_i} u {t_i - 0 : t in T} of |w| where a coordinate
    "t_i - 0" contributes t_i (the sup is not attained).  We compute it exactly by that corner enumeration and
    cross-check with a fine rational grid lower bound.

 A4 (non-inheritance).  Structural hypotheses (light / heavy / super-heavy) of a generator set are NOT inherited
    by its up-closure at rank r: A = {(5,5,0)} over n = (10,10,3), r = 14: A is light everywhere (5 <= 4*10/7?
    no: 5 <= 5.71 yes; 0 <= 12/7), but G_r contains (9,5,0), (5,9,0), (5,6,3), which are super-heavy (> 2n_i/3)
    in parts 1, 2 and 3 respectively.  So Theorems L+/H2 apply to G_r only if G_r itself meets their hypotheses.
"""
from fractions import Fraction as Fr
from itertools import product
import random

def is_free(w, T):
    return not any(all(t[i] <= w[i] for i in range(len(w))) for t in T)

def sup_free_exact(T, x):
    """sup{|w| : 0<=w<=x, w free for T} for finite T. The free region is a finite union of half-open boxes; its
    sup of |w| is attained (as a sup) at a corner w whose coordinate i is either x_i or (t_i)^- for some t in T.
    We enumerate corner candidates: for each i choose c_i in {x_i} u {t_i : t in T, t_i <= x_i}; the candidate
    box is w = c but with 'strictly below' semantics at type coordinates.  A candidate is realisable iff the box
    w' = (c_i - eps for chosen type coordinates, x_i otherwise) is free for small eps: i.e. no t in T with
    t_i <= c_i - eps (type coords) and t_i <= x_i (cap coords), i.e. no t with t_i < c_i on type coords."""
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
        # free for small eps?
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
    if best is None:
        # even the zero box is not free: T contains the zero type
        return Fr(0)
    return best

def sup_free_grid(T, x, denom):
    best = Fr(0)
    rngs = [[Fr(j, denom) for j in range(int(x[i] * denom) + 1)] for i in range(len(x))]
    for w in product(*rngs):
        if is_free(w, T):
            best = max(best, sum(w))
    return best

def tau_star(T, x):
    return sum(x) - sup_free_exact(T, x)

def upclosure_unit(C, x, denom=12):
    """finite rational approximation of U(C): all unit v on the grid 1/denom with v>=c for some c in C, v<=x."""
    p = len(x)
    rngs = [[Fr(j, denom) for j in range(int(x[i] * denom) + 1)] for i in range(p)]
    U = set()
    for v in product(*rngs):
        if sum(v) == 1 and any(all(c[i] <= v[i] for i in range(p)) for c in C):
            U.add(v)
    return U

def check_G4(trials=300, seed=3):
    rng = random.Random(seed)
    fails = 0; tested = 0
    for _ in range(trials):
        p = rng.choice([2, 3])
        denom = 6
        x = tuple(Fr(rng.randint(2, 10), denom) for _ in range(p))
        if sum(x) < 1: continue
        # random finite set of unit types on the grid 1/denom
        cands = [v for v in product(*[[Fr(j, denom) for j in range(int(x[i]*denom)+1)] for i in range(p)]) if sum(v) == 1]
        if not cands: continue
        C = rng.sample(cands, min(len(cands), rng.randint(1, 4)))
        # U(C) restricted to the same grid is EXACTLY the grid part of U(C); tau* of the true (continuous) U(C)
        # equals tau* of its grid version only if the sup-free corners are on the grid -- they are, since the
        # relevant thresholds are type coordinates (grid) and capacities (grid).  We therefore also compare to the
        # formula min(tau*(C), N-1) which is the claimed exact value.
        U = upclosure_unit(C, x, denom)
        tC = tau_star(C, x); tU = tau_star(sorted(U), x)
        N = sum(x)
        pred = min(tC, N - 1)
        tested += 1
        if tU != pred:
            fails += 1
            print("  G4 MISMATCH", x, C, "tau*(C)=", tC, "tau*(U)=", tU, "pred=", pred)
    print(f"[G4] {tested} random finite unit type sets (p=2,3, grid 1/6): tau*(U(C)) = min(tau*(C), N-1) failed {fails} times")
    assert fails == 0

def check_supfree_exact(trials=200, seed=5):
    rng = random.Random(seed)
    for _ in range(trials):
        p = rng.choice([1, 2, 3]); denom = 4
        x = tuple(Fr(rng.randint(1, 8), denom) for _ in range(p))
        cands = [v for v in product(*[[Fr(j, denom) for j in range(int(x[i]*denom)+1)] for i in range(p)])]
        T = rng.sample(cands, min(len(cands), rng.randint(1, 5)))
        s_exact = sup_free_exact(T, x)
        s_grid = sup_free_grid(T, x, 8)   # grid at 1/8 is a lower bound of the sup, within p/8 of it
        assert s_grid <= s_exact and s_exact - s_grid <= Fr(p, 8), (x, T, s_exact, s_grid)
    print(f"[sup-free] corner enumeration agrees with fine-grid lower bounds ({trials} random instances)")

def check_A4():
    n = (10, 10, 3); r = 14
    A = [(5, 5, 0)]
    def light(t): return all(t[i] <= Fr(4*n[i], 7) for i in range(3))
    def superheavy_parts(t): return [i for i in range(3) if t[i] > Fr(2*n[i], 3)]
    assert light(A[0])
    Gr = [v for v in product(*[range(ni+1) for ni in n]) if sum(v) == r and all(A[0][i] <= v[i] for i in range(3))]
    sh = {}
    for v in Gr:
        for i in superheavy_parts(v):
            sh.setdefault(i, v)
    assert set(sh) == {0, 1, 2}, sh
    print(f"[A4] A={A} light everywhere over n={n}; G_{r} (|G_r|={len(Gr)}) has super-heavy types in every part: "
          f"{sh[0]}, {sh[1]}, {sh[2]}  -> hypotheses of L+/H2 are not inherited by the up-closure")

if __name__ == "__main__":
    check_supfree_exact()
    check_G4()
    check_A4()
    print("ALL CHECKS PASSED")
