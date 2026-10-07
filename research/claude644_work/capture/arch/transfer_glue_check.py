#!/usr/bin/env python3
"""
transfer_glue_check.py  (architecture agent, 24 Sep 2026; exact arithmetic, stdlib only)

Exact checks of three glue facts used in PROOF_ARCHITECTURE.md.

 G1 (rank shift).  For a (7,2) family H with vertex partition pi, the robust profile set
      A = A^{(s)}(eta) = { u <= n : f((u - s)^+) >= 1 - eta },
    f(u) = Pr[ a uniform random set with profile u contains an edge ],
    satisfies completeness  tau_int(A) >= tau(H) - s p  and  tau*(A) >= tau(H) - (s+1) p,
    and the transfer bound  tau(H) <= 3r/4 + RL(r) + (s+1)p  (RL(r) = tau*(A) - tau*(A^{<=r}))
    is informative only for r >= k + s p + O(1): for the complete family A^{<=k} is EMPTY.
    We compute f exactly by subset enumeration (N <= 12) and tau*, tau_int exactly.

 G3 (integer up-closure).  For a finite integer unit type set C at rank r over capacities n
    (N = sum n, p parts), U_Z(C) = { v integer : |v| = r, c <= v <= n for some c in C } satisfies
      tau*(U_Z(C)) = min( tau*(C), N - r + 1 - p )      whenever r - 1 <= N - p,
    whereas the REAL up-closure has tau* = min(tau*(C), N - r)  (Lemma U).  So an integer-only
    version of Th(p) costs an extra p in the transfer (Lemma G3 in PROOF_ARCHITECTURE.md).

 tau* of a finite integer type set T over integer capacities n (continuous sup semantics):
    a real box w is free iff floor(w) is free, so
      sup free = max over free integer m <= n of ( |m| + #{i : m_i < n_i} ),
      tau*(T) = N - sup free,   tau_int(T) = N - max over free integer m of |m|.
"""
from fractions import Fraction
from itertools import combinations, product
import random, sys

def profiles_iter(n):
    return product(*[range(ni + 1) for ni in n])

def tau_star_and_int(T, n):
    """T: set of integer tuples (types). Returns (tau*, tau_int) exactly."""
    T = list(T)
    N = sum(n); p = len(n)
    best_real = -1; best_int = -1
    for m in profiles_iter(n):
        free = True
        for t in T:
            if all(t[i] <= m[i] for i in range(p)):
                free = False; break
        if free:
            val_int = sum(m)
            val_real = val_int + sum(1 for i in range(p) if m[i] < n[i])
            best_int = max(best_int, val_int)
            best_real = max(best_real, val_real)
    if best_real < 0:   # no free box at all (T contains the zero type)
        return N, N
    return N - best_real, N - best_int

def transversal_number(H, N):
    for t in range(0, N + 1):
        for S in combinations(range(N), t):
            S = set(S)
            if all(E & S for E in H):
                return t
    return N

def is72(H):
    """every <= 7 edges have a 2-transversal (brute force; small families only)."""
    Hl = list(H)
    V = set().union(*Hl)
    for m in range(1, min(7, len(Hl)) + 1):
        for sub in combinations(Hl, m):
            ok = False
            for a in V:
                if all(a in E for E in sub):
                    ok = True; break
            if ok: continue
            for a, b in combinations(V, 2):
                if all(a in E or b in E for E in sub):
                    ok = True; break
            if not ok:
                return False
    return True

def exact_f(H, parts):
    """f(u) for all profiles u, exact Fractions, by enumerating all subsets of V."""
    N = sum(len(P) for P in parts)
    p = len(parts)
    idx = {}
    for i, P in enumerate(parts):
        for v in P: idx[v] = i
    Hl = [frozenset(E) for E in H]
    cnt_total = {}; cnt_hit = {}
    for mask in range(1 << N):
        W = frozenset(v for v in range(N) if mask >> v & 1)
        u = [0] * p
        for v in W: u[idx[v]] += 1
        u = tuple(u)
        cnt_total[u] = cnt_total.get(u, 0) + 1
        if any(E <= W for E in Hl):
            cnt_hit[u] = cnt_hit.get(u, 0) + 1
    return {u: Fraction(cnt_hit.get(u, 0), cnt_total[u]) for u in cnt_total}

def robust_set(f, n, s, eta):
    A = set()
    for u in profiles_iter(n):
        v = tuple(max(ui - s, 0) for ui in u)
        if f[v] >= 1 - eta:
            A.add(u)
    return A

def check_G1(H, parts, s, eta, label, trusted72=False):
    n = tuple(len(P) for P in parts); N = sum(n); p = len(n)
    k = max(len(E) for E in H)
    t = transversal_number(H, N)
    # brute-force is72 is C(|H|,7) work: infeasible for complete families; those are (7,2) by note Lemma 2.2
    # (N < 7k/4) resp. note Cor 2.3 remark (K_9^(5), covering number C(9,4,2)=8 > 7).  trusted72 documents this.
    if not trusted72:
        assert is72(H), "family is not (7,2)"
    f = exact_f(H, parts)
    A = robust_set(f, n, s, eta)
    ts, ti = tau_star_and_int(A, n)
    print(f"[{label}] N={N} n={n} k={k} tau={t} s={s} eta={eta}  |A|={len(A)}  tau*(A)={ts}  tau_int(A)={ti}")
    assert ti >= t - s * p, "completeness (integer) FAILED"
    assert ts >= t - (s + 1) * p, "completeness (continuous) FAILED"
    minr = None
    for r in range(0, N + 1):
        Ar = {u for u in A if sum(u) <= r}
        tsr, _ = tau_star_and_int(Ar, n) if Ar else (0, 0)
        RL = ts - tsr
        bound = Fraction(3 * r, 4) + RL + (s + 1) * p
        flag = "  <-- A^{<=r} empty" if not Ar else ""
        if r >= k - 1 and r <= k + s * p + 2:
            print(f"    r={r:2d}: tau*(A^<=r)={tsr}  RL(r)={RL}  3r/4+RL+(s+1)p={float(bound):.2f}{flag}")
        if Ar and (minr is None or bound < minr[1]):
            minr = (r, bound)
        assert bound >= t, f"transfer bound violated at r={r}: {bound} < tau={t} (would contradict Th(p) for p<=2!)"
    if minr is None:
        print("    A is empty (n too small for this s): bound is vacuous, completeness holds trivially")
    else:
        Ak = {u for u in A if sum(u) <= k}
        RLk = ts - (tau_star_and_int(Ak, n)[0] if Ak else 0)
        print(f"    best r = {minr[0]} (bound {float(minr[1]):.2f});  RL(k) = {RLk}  (k + s p = {k + s*p})")

def check_G3(trials, seed=1):
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        p = rng.choice([2, 3])
        n = tuple(rng.randint(1, 6) for _ in range(p))
        N = sum(n)
        r = rng.randint(1, max(1, N - p + 1))   # ensures r - 1 <= N - p
        # random finite set of unit integer types at rank r
        allunit = [u for u in profiles_iter(n) if sum(u) == r]
        if not allunit: continue
        C = set(rng.sample(allunit, rng.randint(1, min(4, len(allunit)))))
        # C need not be unit for the identity? keep unit (the transfer's G_r setting)
        UZ = {v for v in allunit if any(all(c[i] <= v[i] for i in range(p)) for c in C)}
        tC, _ = tau_star_and_int(C, n)
        tU, _ = tau_star_and_int(UZ, n)
        pred = min(tC, N - r + 1 - p)
        if tU != pred:
            bad += 1
            print("  G3 MISMATCH", n, r, sorted(C), "tau*(C)=", tC, "tau*(U_Z)=", tU, "pred=", pred)
    print(f"[G3] {trials} random finite integer unit type sets: tau*(U_Z(C)) = min(tau*(C), N-r+1-p) holds in all but {bad}")
    assert bad == 0

if __name__ == "__main__":
    random.seed(0)
    # complete families K_N^(k) with N < 7k/4 are (7,2): k=4,N=6 (tau=3); k=6,N=10 (tau=5); k=7,N=12 (tau=6)
    for (k, N, s) in [(4, 6, 1), (6, 10, 3), (7, 12, 3), (7, 12, 1)]:
        H = [frozenset(E) for E in combinations(range(N), k)]
        check_G1(H, [list(range(N))], s=s, eta=Fraction(1, 8), label=f"K_{N}^({k}), one part", trusted72=True)
    # two-part partitions of the same complete families (the inequalities hold for every s; soundness would
    # need s >= 13 for note-7.75 supports, which these tiny n cannot accommodate -- we test the rank shift only)
    for (k, N, split, s) in [(6, 10, 4, 0), (6, 10, 4, 1), (7, 12, 5, 0), (7, 12, 5, 1), (7, 12, 6, 2)]:
        H = [frozenset(E) for E in combinations(range(N), k)]
        parts = [list(range(split)), list(range(split, N))]
        check_G1(H, parts, s=s, eta=Fraction(1, 8), label=f"K_{N}^({k}), parts {split}+{N-split}", trusted72=True)
    # K_9^(5) is (7,2) with tau = 5 = k (note Cor 2.3 remark)
    H = [frozenset(E) for E in combinations(range(9), 5)]
    check_G1(H, [list(range(9))], s=3, eta=Fraction(1, 8), label="K_9^(5) (tau = k = 5)", trusted72=True)
    check_G3(400)
    print("ALL CHECKS PASSED")
