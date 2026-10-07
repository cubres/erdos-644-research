#!/usr/bin/env python3
"""
referee_w11_arch1_check.py  (referee w11, claim architecture#1 = Lemma G1; exact arithmetic, stdlib only)

Two sharpenings of the attacker's vacuity computation, checked exactly with the attacker's own
functions (arch/transfer_glue_check.py):

 V1 (uniform vacuity).  For EVERY k-uniform family H (k >= 1), EVERY partition pi and EVERY shift s >= 1,
     A^{<=k} is EMPTY, hence RL_pi(k) = tau*(A) >= tau(H) - (s+1)p.
     Hand proof: u in A^{<=k} needs f((u-s)^+) >= 1-eta > 0, so |(u-s)^+| >= k; but for u != 0 some
     u_i >= 1 and (u_i - s)^+ <= u_i - 1, so |(u-s)^+| <= |u| - 1 <= k-1; for u = 0 it is 0 < k.
     Checked on random k-uniform families (all of them, no (7,2) needed: the statement is about f only)
     and random partitions; a non-uniform control family (rank <= k with a small edge) shows A^{<=k} != empty
     can happen, so uniformity is what is used.

 V2 (complete family, any partition).  For K_N^(k) and any partition into p parts, RL_pi(k + s p) = 0,
     so EL_pi <= 3 s p / 4.  Hand proof: A = {u <= n : |(u-s)^+| >= k}; every v in A dominates some
     u in A with |u| <= k + sp (lower coordinates with v_i > s until sum (u_i - s)^+ = k), so A and
     A^{<=k+sp} have the same free boxes.  Checked exactly (random partitions, N <= 12).
"""
import sys, random
from itertools import combinations
from fractions import Fraction
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/arch')
from transfer_glue_check import exact_f, robust_set, tau_star_and_int, transversal_number, profiles_iter

def random_partition(rng, N, p):
    lab = [rng.randrange(p) for _ in range(N)]
    # make every part nonempty when possible
    for i in range(min(p, N)):
        lab[i] = i
    rng.shuffle(lab)
    parts = [[v for v in range(N) if lab[v] == i] for i in range(p)]
    return [P for P in parts if P]

def check_V1(trials, seed=7):
    rng = random.Random(seed)
    eta = Fraction(1, 8)
    n_uniform = 0
    for _ in range(trials):
        N = rng.randint(3, 10); k = rng.randint(1, N - 1)
        allk = list(combinations(range(N), k))
        H = [frozenset(E) for E in rng.sample(allk, rng.randint(1, min(len(allk), 12)))]
        p = rng.randint(1, 3); s = rng.randint(1, 4)
        parts = random_partition(rng, N, p)
        n = tuple(len(P) for P in parts)
        f = exact_f(H, parts)
        A = robust_set(f, n, s, eta)
        Ak = {u for u in A if sum(u) <= k}
        assert not Ak, ("V1 FAILED: k-uniform family with nonempty A^{<=k}", N, k, parts, s, sorted(Ak))
        n_uniform += 1
    print(f"[V1] {n_uniform} random k-uniform families x partitions x s>=1: A^(<=k) empty in all")
    # control: non-uniform family (rank <= k) can have A^{<=k} nonempty
    N, k = 6, 4
    H = [frozenset(E) for E in combinations(range(N), 2)] + [frozenset(E) for E in combinations(range(N), k)]  # rank 4, all pairs
    parts = [list(range(N))]
    f = exact_f(H, parts); A = robust_set(f, (N,), 1, eta)
    Ak = {u for u in A if sum(u) <= k}
    print(f"[V1 control] rank<=4 family (all pairs + all 4-sets), s=1: A^(<=4) = {sorted(Ak)} (nonempty => uniformity is used)")
    assert Ak

def check_V2(trials, seed=11):
    rng = random.Random(seed)
    eta = Fraction(1, 8)
    cnt = 0
    for _ in range(trials):
        k = rng.randint(2, 7)
        N = rng.randint(k + 1, min(12, k + 6))
        H = [frozenset(E) for E in combinations(range(N), k)]
        t = N - k + 1
        p = rng.randint(1, 3); s = rng.randint(1, 3)
        parts = random_partition(rng, N, p); p = len(parts)
        n = tuple(len(P) for P in parts)
        f = exact_f(H, parts)
        A = robust_set(f, n, s, eta)
        # A should be exactly {u : |(u-s)^+| >= k}
        A_pred = {u for u in profiles_iter(n) if sum(max(ui - s, 0) for ui in u) >= k}
        assert A == A_pred, "A formula FAILED"
        ts, ti = tau_star_and_int(A, n) if A else (0, 0)
        Ak = {u for u in A if sum(u) <= k}
        assert not Ak
        assert ts >= t - (s + 1) * p and ti >= t - s * p, "completeness FAILED"
        r = k + s * p
        Ar = {u for u in A if sum(u) <= r}
        tsr = tau_star_and_int(Ar, n)[0] if Ar else 0
        assert ts - tsr == 0, ("V2 FAILED: RL(k+sp) != 0", N, k, n, s, ts, tsr)
        cnt += 1
    print(f"[V2] {cnt} complete families K_N^(k) x random partitions: A = {{u : |(u-s)^+| >= k}}, A^(<=k) empty, RL(k+sp) = 0 in all")

if __name__ == "__main__":
    check_V1(300)
    check_V2(200)
    print("ALL REFEREE CHECKS PASSED")
