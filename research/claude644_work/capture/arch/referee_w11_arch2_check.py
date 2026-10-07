#!/usr/bin/env python3
"""
referee_w11_arch2_check.py  (wave-11 referee, claim architecture#2 = N2.0, 24 Sep 2026; exact, stdlib only)

Claim N2.0: Th_Z(p) <=> 644 for p-part type-closed families.
  Th_Z(p): for integers r, n in Z_{>0}^p, finite integer Gen (0 <= g <= n, |g| <= r),
           G_r = {v real : |v| = r, g <= v <= n for some g in Gen},  tau*(G_r) > 3r/4  =>  continuous bad 7-tuple.

Part A  (direction <=, the scaling step).  H_m := all subsets of a ground set with parts of sizes m n_i whose profile
        lies in T_m := Z^p cap m G_r (uniform, rank m r, type-closed).  Claimed: w integer free for H_m => w/m free for
        G_r, hence tau(H_m) >= m tau*(G_r).  We enumerate T_m and all integer boxes w <= m n EXPLICITLY (no use of the
        claimed lemma) and test both statements for m = 1, 2, 3; we also record the gap tau(H_m) - m tau*(G_r), which
        must lie in [0, p] (integer-vs-real slop), and check that the gap is < p+1 always.
        tau*(G_r) is computed by two independent routes: (a) Lemma U's identity min(tau*(Gen), N - r) with tau*(Gen)
        by the integer-corner formula (attacker's tau_star_and_int, re-implemented), and (b) directly from the
        real free region of G_r via the characterisation 'w free for G_r iff |w| < r or no g <= w' proved here from
        scratch (raise g inside w), taking the sup over real boxes by corner enumeration.  (a) and (b) must agree.

Part B  (direction =>, the constant).  For a type-closed family with type set T and its natural partition, f is 0/1
        and f(u) = 1 iff some t in T has t <= u.  The transfer's robust set is A = {u <= n : (u - s)^+ in up(T)} and the
        bound is tau <= min_r [3r/4 + RL(r)] + (s+1)p, RL(r) = tau*(A) - tau*(A^{<=r}).  The claim states the result as
        tau <= 3k/4 + 15p (= 3k/4 + (s+1)p with s = 14).  We compute the best transfer bound exactly for complete
        families K_N^(k) (p = 1, s in {1,2,3,14}) and for two-part uniform type-closed families (p = 2, s in {1,2}),
        and compare with 3k/4 + (s+1)p and with 3k/4 + 3sp/4 + (s+1)p.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import random, sys

# ---------------------------------------------------------------- tau* of a finite integer type set (sup semantics)
def boxes(n):
    return product(*[range(ni + 1) for ni in n])

def dominated(t, w):
    return all(t[i] <= w[i] for i in range(len(w)))

def tau_star_int_set(T, n):
    """tau*(T) for a finite integer set T at integer capacities n, sup semantics.  A real w is free iff floor(w) is
    free (types integer), and w_i may approach m_i + 1 when m_i < n_i.  Returns (tau*, tau_int)."""
    T = list(T); N = sum(n); p = len(n)
    best_real = None; best_int = None
    for m in boxes(n):
        if any(dominated(t, m) for t in T):
            continue
        vi = sum(m); vr = vi + sum(1 for i in range(p) if m[i] < n[i])
        best_int = vi if best_int is None else max(best_int, vi)
        best_real = vr if best_real is None else max(best_real, vr)
    if best_real is None:
        return Fr(N), Fr(N)
    return Fr(N - best_real), Fr(N - best_int)

# ---------------------------------------------------------------- Part A
def free_for_Gr_real(w, Gen, r):
    """w real box (0 <= w <= n).  There is v in G_r with v <= w  iff  |w| >= r and some g in Gen has g <= w
    (raise coordinates of g inside w to total r; conversely v <= w gives |w| >= r and g <= v <= w)."""
    return (sum(w) < r) or not any(dominated(g, w) for g in Gen)

def sup_free_Gr_direct(Gen, n, r):
    """sup{|w| : w real, 0<=w<=n, free for G_r} by corner enumeration: the free region is
    {|w| < r} u {w : for all g some coord w_i < g_i}.  Its sup is max(r [if N >= r], sup free(Gen)); we do NOT use
    that: we enumerate candidate corners w with w_i in {n_i} u {g_i^- : g in Gen} plus the hyperplane |w| = r^-."""
    p = len(n); N = sum(n)
    best = Fr(0)
    # corners of the second region (strictly below some type coordinate)
    choices = []
    for i in range(p):
        vals = {("cap", n[i])}
        for g in Gen:
            if 0 < g[i] <= n[i]:
                vals.add(("typ", g[i]))
        choices.append(sorted(vals))
    for combo in product(*choices):
        ok = True
        for g in Gen:
            dom = True
            for i in range(p):
                kind, c = combo[i]
                if kind == "cap":
                    if not g[i] <= c: dom = False; break
                else:
                    if not g[i] < c: dom = False; break
            if dom: ok = False; break
        if ok:
            best = max(best, Fr(sum(c for _, c in combo)))
    # the first region {|w| < r}: sup = min(r, N) (as a sup, not attained if r <= N)
    best = max(best, Fr(min(r, N)))
    return best

def check_partA(trials=60, seed=11):
    rng = random.Random(seed)
    tested = 0; maxgap = 0
    for _ in range(trials):
        p = rng.choice([1, 2, 3])
        n = tuple(rng.randint(1, 4 if p == 3 else 6) for _ in range(p))
        N = sum(n)
        r = rng.randint(1, N)
        cands = [g for g in boxes(n) if sum(g) <= r]
        Gen = rng.sample(cands, min(len(cands), rng.randint(1, 3)))
        tG, _ = tau_star_int_set(Gen, n)
        tGr_a = min(tG, Fr(N - r))                       # Lemma U identity
        tGr_b = Fr(N) - sup_free_Gr_direct(Gen, n, r)   # direct
        assert tGr_a == tGr_b, ("Lemma U identity mismatch", n, r, Gen, tGr_a, tGr_b)
        for m in (1, 2, 3):
            mn = tuple(m * ni for ni in n)
            if max(mn) > 12 and p == 3: continue
            Tm = [u for u in boxes(mn) if sum(u) == m * r and any(all(m * g[i] <= u[i] for i in range(p)) for g in Gen)]
            best = -1
            for w in boxes(mn):
                if any(dominated(u, w) for u in Tm):
                    continue
                # claimed implication: w/m is free for G_r
                wm = tuple(Fr(wi, m) for wi in w)
                assert free_for_Gr_real(wm, Gen, r), ("free-box implication FAILED", n, r, Gen, m, w)
                best = max(best, sum(w))
            tauHm = m * N - best if best >= 0 else m * N
            assert Fr(tauHm) >= m * tGr_a, ("tau(H_m) >= m tau*(G_r) FAILED", n, r, Gen, m, tauHm, tGr_a)
            gap = Fr(tauHm) - m * tGr_a
            assert gap <= p, ("gap > p", n, r, Gen, m, tauHm, tGr_a)
            maxgap = max(maxgap, gap)
            tested += 1
    print(f"[A] {tested} (instance, m) pairs, p<=3, m<=3: Lemma U identity (two routes) agrees; "
          f"'w free for H_m => w/m free for G_r' holds; tau(H_m) >= m tau*(G_r) holds; max gap tau(H_m)-m tau*(G_r) = {maxgap} (<= p)")

# ---------------------------------------------------------------- Part B
def transfer_bound_typeclosed(T, n, k, s):
    """T finite integer type set (rank <= k) at capacities n; deterministic f; returns
    (tau_int(T) [= tau(H)], tau*(A), best bound over r >= k, bound at r = k, bound at r = k + sp, r_best)."""
    p = len(n); N = sum(n)
    Tl = list(T)
    tauH = tau_star_int_set(Tl, n)[1]        # tau of the type-closed family = tau_int(T)
    A = []
    for u in boxes(n):
        v = tuple(max(ui - s, 0) for ui in u)
        if any(dominated(t, v) for t in Tl):
            A.append(u)
    tsA = tau_star_int_set(A, n)[0] if A else Fr(0)
    best = None; at_k = None; at_ksp = None
    for r in range(0, N + 1):
        Ar = [u for u in A if sum(u) <= r]
        tsr = tau_star_int_set(Ar, n)[0] if Ar else Fr(0)
        RL = tsA - tsr
        b = Fr(3 * r, 4) + RL + (s + 1) * p
        if r == k: at_k = b
        if r == k + s * p: at_ksp = b
        if r >= k and (best is None or b < best[1]): best = (r, b)   # EL form: minimise over r >= k
    return tauH, tsA, best, at_k, at_ksp

def check_partB():
    print("[B] complete families K_N^(k), p = 1 (type set {k}); transfer bound with deterministic f:")
    for (k, N, s) in [(8, 13, 1), (12, 20, 2), (16, 27, 3), (20, 34, 3), (40, 69, 14), (48, 83, 14), (60, 104, 14)]:
        tauH, tsA, best, at_k, at_ksp = transfer_bound_typeclosed([(k,)], (N,), k, s)
        claimed = Fr(3 * k, 4) + (s + 1)
        predicted = Fr(3 * k, 4) + min(tsA, Fr(3 * s, 4)) + (s + 1)
        print(f"   k={k:2d} N={N:3d} s={s:2d}: tau={tauH} (=3k/4+{tauH - Fr(3*k,4)}), tau*(A)={tsA}, bound at r=k: {float(at_k):.2f} "
              f"(RL(k)=tau*(A): vacuous), at r=k+s: {float(at_ksp):.2f}, BEST over r: {float(best[1]):.2f} at r={best[0]}; "
              f"claim's 3k/4+(s+1)p = {float(claimed):.2f}; 3k/4+min(tau*(A),3s/4)+(s+1) = {float(predicted):.2f}")
        assert best[1] == predicted
        assert best[1] >= tauH
        if tsA > Fr(3 * s, 4):
            assert best[1] > claimed, "transfer gave the claimed (s+1)p constant?!"
            assert best[1] == Fr(3 * k, 4) + Fr(7 * s, 4) + 1
    print("   => the transfer's best bound for a uniform type-closed family is 3k/4 + 3sp/4 + (s+1)p = 3k/4 + (7s/4+1)p,")
    print("      i.e. 3k/4 + 25.5p at s = 14, NOT 3k/4 + 15p; the r = k instance is vacuous (A^{<=k} empty).")
    print("[B'] two-part uniform type-closed families (p = 2), several type sets, s in {1,2}: best bound minus 3k/4")
    rng = random.Random(5)
    worst_excess = Fr(0)
    for trial in range(12):
        n = (rng.randint(5, 8), rng.randint(5, 8)); N = sum(n)
        k = rng.randint(4, min(N - 1, 9))
        unit = [u for u in boxes(n) if sum(u) == k]
        T = rng.sample(unit, rng.randint(1, min(4, len(unit))))
        for s in (1, 2):
            tauH, tsA, best, at_k, at_ksp = transfer_bound_typeclosed(T, n, k, s)
            excess = best[1] - Fr(3 * k, 4)
            worst_excess = max(worst_excess, excess - (s + 1) * 2)
            print(f"   n={n} k={k} T={sorted(T)} s={s}: tau={tauH}, tau*(A)={tsA}, best bound = 3k/4 + {float(excess):.2f} at r={best[0]} "
                  f"(claimed constant (s+1)p = {(s+1)*2}; RL(k) = {float(at_k - Fr(3*k,4) - (s+1)*2):.2f})")
            assert best[1] >= tauH
    print(f"   => max over these instances of [best transfer constant - (s+1)p] = {float(worst_excess):.2f} > 0: the (s+1)p form is not what the transfer yields.")

if __name__ == "__main__":
    check_partA()
    check_partB()
    print("REFEREE CHECKS DONE")
