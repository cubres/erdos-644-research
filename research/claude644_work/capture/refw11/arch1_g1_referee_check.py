#!/usr/bin/env python3
"""
refw11/arch1_g1_referee_check.py  (referee wave 11, claim architecture#1 = Lemma G1)
Exact (Fractions / integers), stdlib only.  Independent re-implementation, NOT derived from arch/transfer_glue_check.py.

Checks:
 C1  Complete family K_N^(k), N = 7k/4 - 1, ANALYTIC f (f(u) = 1 iff |u| >= k) for k = 4, 8, 12, 16, 20 and p = 1, 2, 3
     parts, shifts s in {1, 3, 14, 31}:  A^{<=k} empty, RL(k) = tau*(A), for p = 1: tau*(A) = tau - s - 1, RL(k+s) = 0,
     EL = 3s/4 exactly (large k), transfer bound at the EL-optimal r equals 3k/4 + 7s/4 + 1.
 C2  UNIVERSAL VACUITY (stronger than the claim): for EVERY k-uniform family, every partition and s >= 1,
     A^{<=k} = empty, hence RL_pi(k) = tau*(A).  Proof: |(u-s)^+| < |u| unless u = 0.  Checked on random (7,2)
     families (brute-force (7,2) test) and random partitions.
 C3  UNSHIFTED robust set A0 = {u : f(u) >= 1-eta}.  Inequalities (hand proof in the report):
        tau*(A) <= tau*(A0),   tau*(A^{<= r+sp}) >= tau*(A0^{<=r}) - (s+1)p,   tau_int(A0) >= tau(H).
     Consequently (given Th_Z(p) at rank r+sp) tau(H) <= 3r/4 + RL0_pi(r) + (7s/4+2)p for every r, with
     RL0_pi(r) := tau*(A0) - tau*(A0^{<=r}); at the extremal family RL0(k) = 0.  So the handback's rank-k sentence is
     NON-vacuous under the unshifted convention.  Checked exactly on the same random families and on K_N^(k).
 C4  EL_pi <= RL0_pi(k) + (7s/4 + 1)p  (the EL form is never worse than the unshifted rank-k form, up to O(sp)).
"""
from fractions import Fraction
from itertools import combinations, product
import random, sys

def boxes(n):
    return product(*[range(ni + 1) for ni in n])

def tau_star(T, n):
    """continuous tau* of a finite integer type set T with integer capacities n (sup semantics):
       real w is free iff floor(w) is free; sup free = max over free integer m of |m| + #{i: m_i < n_i}."""
    T = list(T); N = sum(n); p = len(n)
    if not T:
        return 0
    best = -1
    for m in boxes(n):
        if any(all(t[i] <= m[i] for i in range(p)) for t in T):
            continue
        best = max(best, sum(m) + sum(1 for i in range(p) if m[i] < n[i]))
    return N if best < 0 else N - best

def tau_int(T, n):
    T = list(T); N = sum(n); p = len(n)
    if not T:
        return 0
    best = -1
    for m in boxes(n):
        if any(all(t[i] <= m[i] for i in range(p)) for t in T):
            continue
        best = max(best, sum(m))
    return N if best < 0 else N - best

def shifted(A0, n, s):
    return {u for u in boxes(n) if tuple(max(ui - s, 0) for ui in u) in A0}

def RL(A, n, r):
    return tau_star(A, n) - tau_star({u for u in A if sum(u) <= r}, n)

def EL(A, n, k):
    N = sum(n)
    return min(Fraction(3 * (r - k), 4) + RL(A, n, r) for r in range(k, N + 1))

# ---------------- C1: complete family, analytic f ----------------
def C1():
    print("== C1: complete family K_N^(k), N = 7k/4 - 1, analytic f ==")
    fails = 0
    for k in [4, 8, 12, 16, 20]:
        N = 7 * k // 4 - 1
        tau = N - k + 1                      # = 3k/4
        assert tau == 3 * k // 4
        for p in [1, 2, 3]:
            if p == 1: n = (N,)
            elif p == 2: n = (N // 2, N - N // 2)
            else: n = (N // 3, N // 3, N - 2 * (N // 3))
            if p == 3 and k > 12: continue    # box enumeration cost
            if p == 2 and k > 16: continue
            A0 = {u for u in boxes(n) if sum(u) >= k}          # f(u) = 1 iff |u| >= k, eta irrelevant
            for s in [1, 3, 14, 31]:
                A = shifted(A0, n, s)
                Ak = {u for u in A if sum(u) <= k}
                tsA = tau_star(A, n)
                rlk = RL(A, n, k) if A else 0
                ok = (len(Ak) == 0) and (rlk == tsA)
                if not A:
                    print(f"  k={k} p={p} n={n} s={s}: A EMPTY (s too large for N={N}); vacuity trivially holds")
                    continue
                msg = f"  k={k} p={p} n={n} s={s}: |A|={len(A)} A^<=k empty={len(Ak)==0} tau*(A)={tsA} RL(k)={rlk} tau={tau}"
                if p == 1:
                    e = EL(A, n, k)
                    rlks = RL(A, n, k + s)
                    bound_opt = Fraction(3 * k, 4) + e + (s + 1)
                    # exact value: EL = min(3s/4, tau*(A)) = min(3s/4, tau-s-1); the claim asserts only EL <= 3s/4
                    e_exp = min(Fraction(3 * s, 4), Fraction(tau - s - 1))
                    ok = ok and (tsA == tau - s - 1) and (rlks == 0) and (e == e_exp) and (e <= Fraction(3 * s, 4)) \
                         and (bound_opt == Fraction(3 * k, 4) + e_exp + s + 1)
                    msg += f" | tau-s-1={tau-s-1} RL(k+s)={rlks} EL={e} (=min(3s/4,tau-s-1)={e_exp}) bound@EL={bound_opt}"
                else:
                    e = EL(A, n, k)
                    # completeness (refereed (i)); EL bound must be >= tau (sanity, Th(p) true for p<=2 by note 7.75 [C])
                    ok = ok and (tsA >= tau - (s + 1) * p) and (Fraction(3 * k, 4) + e + (s + 1) * p >= tau)
                    msg += f" | EL={e} (3sp/4={Fraction(3*s*p,4)}) tau-(s+1)p={tau-(s+1)*p}"
                print(msg + ("" if ok else "   <<< FAIL"))
                fails += (not ok)
    print(f"C1 failures: {fails}")
    return fails

# ---------------- random (7,2) families ----------------
def is72(H, V):
    Hl = list(H)
    for m in range(1, min(7, len(Hl)) + 1):
        for sub in combinations(Hl, m):
            if any(all(a in E for E in sub) for a in V): continue
            if any(all(a in E or b in E for E in sub) for a, b in combinations(V, 2)): continue
            return False
    return True

def transversal(H, N):
    for t in range(N + 1):
        for S in combinations(range(N), t):
            S = set(S)
            if all(E & S for E in H): return t
    return N

def exact_f(H, parts, N):
    p = len(parts); idx = {}
    for i, P in enumerate(parts):
        for v in P: idx[v] = i
    tot = {}; hit = {}
    for mask in range(1 << N):
        W = frozenset(v for v in range(N) if mask >> v & 1)
        u = [0] * p
        for v in W: u[idx[v]] += 1
        u = tuple(u)
        tot[u] = tot.get(u, 0) + 1
        if any(E <= W for E in H): hit[u] = hit.get(u, 0) + 1
    return {u: Fraction(hit.get(u, 0), tot[u]) for u in tot}

def random_72_family(rng, N, k, want_uniform=True):
    V = list(range(N))
    allk = [frozenset(E) for E in combinations(V, k)]
    while True:
        m = rng.randint(3, min(12, len(allk)))
        H = rng.sample(allk, m)
        if not want_uniform:
            # add a few smaller edges (rank <= k)
            small = [frozenset(E) for E in combinations(V, k - 2)] if k >= 3 else []
            H = H + rng.sample(small, rng.randint(0, 2))
        if is72(H, V): return H

def random_partition(rng, N, p):
    lab = [rng.randrange(p) for _ in range(N)]
    parts = [[v for v in range(N) if lab[v] == i] for i in range(p)]
    return [P for P in parts if P]

def C2_C3_C4(trials=60, seed=11):
    print("== C2/C3/C4: random (7,2) families, random partitions ==")
    rng = random.Random(seed)
    f2 = f3 = f4 = 0; nonuniform_nonempty = 0; cnt = 0
    for t in range(trials):
        N = rng.choice([6, 7, 8, 9]); k = rng.choice([3, 4]) if N <= 8 else 4
        uniform = (t % 4 != 3)
        H = random_72_family(rng, N, k, want_uniform=uniform)
        p = rng.choice([1, 2, 3])
        parts = random_partition(rng, N, p); p = len(parts)
        n = tuple(len(P) for P in parts)
        eta = Fraction(1, 8)
        f = exact_f(H, parts, N)
        A0 = {u for u in f if f[u] >= 1 - eta}
        tau = transversal(H, N)
        kk = max(len(E) for E in H)
        for s in [1, 2, 3]:
            A = shifted(A0, n, s)
            cnt += 1
            # C2: shifted A^{<=k} empty for k-uniform (every partition, every s >= 1)
            Ak = {u for u in A if sum(u) <= kk}
            if uniform and Ak:
                f2 += 1; print("  C2 FAIL", H, parts, s, Ak)
            if (not uniform) and Ak:
                nonuniform_nonempty += 1
            # C3: tau*(A) <= tau*(A0); tau*(A^{<=r+sp}) >= tau*(A0^{<=r}) - (s+1)p; tau_int(A0) >= tau
            if tau_star(A, n) > tau_star(A0, n):
                f3 += 1; print("  C3a FAIL tau*(A) > tau*(A0)", H, parts, s)
            if tau_int(A0, n) < tau:
                f3 += 1; print("  C3c FAIL tau_int(A0) < tau", H, parts)
            for r in range(0, N + 1):
                lhs = tau_star({u for u in A if sum(u) <= r + s * p}, n)
                rhs = tau_star({u for u in A0 if sum(u) <= r}, n) - (s + 1) * p
                if lhs < rhs:
                    f3 += 1; print("  C3b FAIL", H, parts, s, r, lhs, rhs)
            # C4: EL <= RL0(k) + (7s/4+1)p
            if A:
                e = EL(A, n, kk)
                rl0 = RL(A0, n, kk) if A0 else 0
                if e > rl0 + Fraction(7 * s, 4) * p + p:
                    f4 += 1; print("  C4 FAIL", H, parts, s, e, rl0)
    print(f"  {cnt} (family, partition, s) instances; C2 failures {f2}; non-uniform instances with A^<=k nonempty: "
          f"{nonuniform_nonempty} (expected > 0: vacuity is a k-UNIFORM phenomenon); C3 failures {f3}; C4 failures {f4}")
    return f2 + f3 + f4

# ---------------- C3 on the complete family: unshifted rank-k loss is 0 ----------------
def C3_complete():
    print("== C3 at K_N^(k): unshifted RL0(k) ==")
    fails = 0
    for k in [4, 8, 12]:
        N = 7 * k // 4 - 1; tau = N - k + 1
        for p, n in [(1, (N,)), (2, (N // 2, N - N // 2))]:
            A0 = {u for u in boxes(n) if sum(u) >= k}
            rl0 = RL(A0, n, k)
            ts0 = tau_star(A0, n); ti0 = tau_int(A0, n)
            ok = (rl0 == 0) and (ti0 == tau) and (ts0 >= tau - p)
            print(f"  k={k} p={p} n={n}: tau={tau} tau_int(A0)={ti0} tau*(A0)={ts0} RL0(k)={rl0}" + ("" if ok else "  <<< FAIL"))
            fails += (not ok)
    return fails

if __name__ == "__main__":
    F = C1() + C3_complete() + C2_C3_C4()
    print("TOTAL FAILURES:", F)
    print("ALL REFEREE CHECKS PASSED" if F == 0 else "SOME CHECKS FAILED")
