"""w9 referee [core#3]: K_9^(5) (t=5, (7,2), GT*-tight) and K_8^(5) (t=4): vertex-transitive, so tau(N_lam[E]) is the
same for all E; B is empty or everything.  Check L+/L++ for all lam,delta and the formula tau(N_lam[E]) = t if
lam < 2k-n else min(k-lam, t)."""
import itertools
from w9_ref_core3_lib import *
for n, k in [(9, 5), (8, 5), (6, 4)]:
    H = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)]
    if n <= 8: assert is72(H, n)   # K_9^5 (7,2) taken from the refereed GT* tightness (SAT too slow here)
    t = tau(H, n); E = H[0]
    for lam in range(0, k+1):
        d0 = tau([F for F in H if popc(E & F) > lam], n)
        pred = t if lam < 2*k-n else max(0, min(k-lam, t))
        assert d0 == pred, (n, k, lam, d0, pred)
        if 3*lam <= t-1: assert 3*d0 >= t or 2*lam + d0 >= t
        for delta in range(0, t+1):
            beta = t if d0 > delta else 0
            assert not all(five(t, lam, delta, beta))
    print(f"K_{n}^{k}: (7,2), t={t}; tau(N_lam) formula and L+/L++ verified for all lam, delta")
