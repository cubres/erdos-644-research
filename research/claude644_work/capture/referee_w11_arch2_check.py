#!/usr/bin/env python3
"""
referee_w11_arch2_check.py  (wave-11 referee of claim architecture#2 = N2.0; exact Fractions, stdlib only)

Check 1 (direction (iii), scaling step).  For small integer data (n, r, Gen) let G_r be the unit up-closure
   and H_m the type-closed family at scale m (all subsets of parts of sizes m n_i with profile in m G_r).
   Brute force:  tau(H_m) = mN - max{|w| : w integer <= mn, no u in T_m with u <= w},
   T_m = {u integer : |u| = mr, m g <= u <= m n for some g in Gen}.   Claim: tau(H_m) >= m tau*(G_r).
   tau*(G_r) = N - max(sup free(Gen), r)  (Lemma U; sup free of the finite set Gen by corner enumeration,
   independently re-implemented here).  Sanity: tau(H_m) <= m tau*(G_r) + p (integrality).

Check 2 (direction (ii), the constant).  For the complete family K_N^(k) (type-closed, p = 1) the robust set
   A = {u : (u-s)^+ >= k} = {u >= k+s} has A^{<=k} EMPTY, so RL(k) = tau*(A) and the transfer bound
   3k/4 + RL(k) + (s+1) is vacuous; the first r with RL(r) = 0 is r = k+s, giving 3k/4 + 3s/4 + s + 1.
   Two-part type-closed example with a full-support type: RL(r) = 0 first at r = k + s p.

Check 3 (referee's replacement rounding for the deterministic case).  In one part, real masses m_C >= 0 on the
   parent cells C of any bad support (complements = intersecting antichain on [7]) with row windows
   W_j = sum_{C ni j} m_C >= t_j (integers).  Exact vertex reduction: while more than 7 cells carry mass, move
   along a kernel vector of the 7 x |support| window matrix (sign chosen so the total does not increase) until a
   coordinate hits 0; windows are unchanged.  Then ceil the <= 7 remaining masses: windows >= t_j and total
   < original total + 7, i.e. <= n_i + 6 when the original total is <= n_i (integer).  So 6 spare vertices per
   part suffice, for EVERY support (no per-window cell count enters).
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import random

# ---------------------------------------------------------------- generic helpers
def dominated(t, w):
    return all(t[i] <= w[i] for i in range(len(w)))

def sup_free_finite(T, x):
    """sup{|w| : 0 <= w <= x, no t in T with t <= w}, finite T, exact (corner enumeration)."""
    p = len(x)
    choices = []
    for i in range(p):
        vals = {("cap", Fr(x[i]))}
        for t in T:
            if 0 < t[i] <= x[i]:
                vals.add(("typ", Fr(t[i])))
        choices.append(sorted(vals))
    best = None
    for combo in product(*choices):
        ok = True
        for t in T:
            dom = True
            for i in range(p):
                kind, c = combo[i]
                if kind == "cap":
                    if not t[i] <= c: dom = False; break
                else:
                    if not t[i] < c: dom = False; break
            if dom: ok = False; break
        if ok:
            s = sum(c for _, c in combo)
            if best is None or s > best: best = s
    return Fr(0) if best is None else best

# ---------------------------------------------------------------- check 1
def check1(trials=150, seed=11):
    rng = random.Random(seed)
    tested = 0
    for _ in range(trials):
        p = rng.choice([2, 3])
        n = tuple(rng.randint(1, 4) for _ in range(p)); N = sum(n)
        r = rng.randint(1, N)
        cands = [g for g in product(*[range(ni + 1) for ni in n]) if sum(g) <= r]
        Gen = rng.sample(cands, rng.randint(1, min(3, len(cands))))
        tau_star = N - max(sup_free_finite(Gen, n), Fr(r))          # Lemma U (N >= r here)
        for m in (1, 2, 3):
            mn = tuple(m * ni for ni in n)
            Tm = [u for u in product(*[range(v + 1) for v in mn]) if sum(u) == m * r
                  and any(dominated(tuple(m * gi for gi in g), u) for g in Gen)]
            best = -1
            for w in product(*[range(v + 1) for v in mn]):
                if not any(dominated(u, w) for u in Tm):
                    best = max(best, sum(w))
            tau_Hm = m * N - best if best >= 0 else m * N
            assert tau_Hm >= m * tau_star, (n, r, Gen, m, tau_Hm, tau_star)
            assert tau_Hm <= m * tau_star + p, (n, r, Gen, m, tau_Hm, tau_star)
            tested += 1
    print(f"[check1] (iii) scaling: tau(H_m) >= m tau*(G_r) (and <= m tau* + p) in all {tested} instances")

# ---------------------------------------------------------------- check 2
def tau_star_int_set(T, n):
    """continuous tau* of a finite integer type set over integer caps (sup semantics)."""
    N = sum(n); p = len(n); best = -1
    for mm in product(*[range(ni + 1) for ni in n]):
        if not any(dominated(t, mm) for t in T):
            best = max(best, sum(mm) + sum(1 for i in range(p) if mm[i] < n[i]))
    return N if best < 0 else N - best

def check2():
    # complete family K_N^(k), p = 1, s = 14 (Milner shift): f(u) = 1 iff u >= k
    for (k, N, s) in [(8, 13, 3), (12, 24, 4), (16, 27, 3)]:
        n = (N,); tau = N - k + 1
        A = [(u,) for u in range(N + 1) if max(u - s, 0) >= k]
        first_zero = None
        for r in range(0, N + 1):
            Ar = [u for u in A if u[0] <= r]
            RL = tau_star_int_set(A, n) - (tau_star_int_set(Ar, n) if Ar else 0)
            if Ar and RL == 0 and first_zero is None: first_zero = r
        Ak = [u for u in A if u[0] <= k]
        print(f"[check2] K_{N}^({k}): tau={tau}, s={s}: A^(<=k) empty? {not Ak};  first r with RL(r)=0: {first_zero} = k+s? {first_zero == k + s if first_zero else 'A empty (N<k+s)'}")
    # two-part type-closed family with one full-support type t = (a,b): generators of A are t + s*1, rank k + 2s
    k, s = 6, 2
    n = (8, 8); N = 16
    T = [(3, 3)]
    A = [u for u in product(range(9), range(9)) if dominated(T[0], (max(u[0]-s, 0), max(u[1]-s, 0)))]
    tA = tau_star_int_set(A, n)
    first_zero = None
    for r in range(0, N + 1):
        Ar = [u for u in A if sum(u) <= r]
        if Ar and tA - tau_star_int_set(Ar, n) == 0 and first_zero is None: first_zero = r
    print(f"[check2] two-part, T={T}, s={s}: first r with RL(r)=0 is {first_zero} = k + s p = {k + s*2}")

# ---------------------------------------------------------------- check 3
def random_bad_support(rng):
    """random antichain of cells in [7] with pairwise unions != [7] (complements: intersecting antichain)."""
    cells = []
    subs = [frozenset(c) for sz in range(1, 7) for c in combinations(range(7), sz)]
    rng.shuffle(subs)
    for c in subs:
        if all((c | d) != frozenset(range(7)) and not (c < d) and not (d < c) and c != d for d in cells):
            cells.append(c)
        if len(cells) >= rng.randint(8, 35): break
    return cells

def kernel_vector(rows, S):
    """exact nonzero vector d (len |S|) with W_S d = 0, W the 7 x |S| 0/1 window matrix; None if injective."""
    # gaussian elimination on the 7 x |S| matrix over Fractions
    M = [[Fr(1 if j in S[c] else 0) for c in range(len(S))] for j in range(7)]
    ncol = len(S); pivots = []; rrow = 0
    for col in range(ncol):
        piv = None
        for i in range(rrow, 7):
            if M[i][col] != 0: piv = i; break
        if piv is None: continue
        M[rrow], M[piv] = M[piv], M[rrow]
        pv = M[rrow][col]; M[rrow] = [v / pv for v in M[rrow]]
        for i in range(7):
            if i != rrow and M[i][col] != 0:
                f = M[i][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rrow])]
        pivots.append(col); rrow += 1
        if rrow == 7: break
    free = [c for c in range(ncol) if c not in pivots]
    if not free: return None
    fc = free[0]; d = [Fr(0)] * ncol; d[fc] = Fr(1)
    for i, pc in enumerate(pivots):
        d[pc] = -M[i][fc]
    return d

def check3(trials=400, seed=7):
    rng = random.Random(seed)
    worst_inc = Fr(0); maxsupp = 0
    for it in range(trials):
        cells = random_bad_support(rng) if it > 0 else [frozenset(c) for c in combinations(range(7), 3)]  # 35 parent cells
        mass = {c: Fr(rng.randint(0, 40), rng.randint(1, 7)) for c in cells}
        total0 = sum(mass.values())
        win = lambda ms, j: sum(v for c, v in ms.items() if j in c)
        t = [int(win(mass, j)) for j in range(7)]     # integer targets <= windows (floor)
        ms = dict(mass)
        while True:
            S = [c for c in ms if ms[c] > 0]
            if len(S) <= 7: break
            d = kernel_vector(None, S)
            assert d is not None
            if sum(d) > 0: d = [-v for v in d]
            if all(v >= 0 for v in d):          # then sum(d) <= 0 forces d = 0: impossible
                raise AssertionError("kernel vector nonneg")
            lam = min(ms[S[c]] / (-d[c]) for c in range(len(S)) if d[c] < 0)
            for c in range(len(S)): ms[S[c]] += lam * d[c]
            assert all(v >= 0 for v in ms.values())
            for j in range(7): assert win(ms, j) == win(mass, j)
        assert sum(ms.values()) <= total0
        rounded = {c: (v.numerator + v.denominator - 1) // v.denominator for c, v in ms.items()}
        for j in range(7): assert win(rounded, j) >= t[j]
        inc = sum(rounded.values()) - total0
        assert inc < 7
        worst_inc = max(worst_inc, inc); maxsupp = max(maxsupp, len(cells))
    print(f"[check3] LP-vertex rounding on {trials} random bad supports (up to {maxsupp} parent cells): "
          f"<= 7 cells after reduction, windows >= targets, total increase < 7 (worst {float(worst_inc):.3f})")

if __name__ == "__main__":
    check1(); check2(); check3()
    print("ALL CHECKS PASSED")
