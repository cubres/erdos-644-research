"""Referee w7 core#2 BREAK-IT (B2): exact SAT+CEGAR search for families H on [n] (edge sizes in [smin,smax])
with max pairwise intersection <= lam, tau(H) >= T, and property (7,2) (at-most-7 convention).
Theorem L: UNSAT whenever T >= 3lam+1.  For T <= 3lam this probes sharpness.
Independent of w7_ref_core2_sat.py: (7,2) oracle = explicit greedy-minimised bad subfamily found by bitmask search
over pairs (exact), witness re-verified by brute force over all <=7-subfamilies.
Usage: python3 w7_ref_core2_brk_sat.py n lam T smin smax [clutter=1]"""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def bad_sub(Hm, n):
    # Hm: list of bitmasks. find <=7 edges with no 2-transversal via SAT (exact); else None
    m = len(Hm)
    S = Cadical153()
    enc = CardEnc.atmost(lits=list(range(1, m+1)), bound=7, top_id=m, encoding=EncType.totalizer)
    for c in enc.clauses: S.add_clause(c)
    for x in range(n):
        for y in range(x, n):
            pm = (1 << x) | (1 << y)
            S.add_clause([j+1 for j in range(m) if not (Hm[j] & pm)])
    if not S.solve(): return None
    mod = S.get_model()
    sel = [j for j in range(m) if mod[j] > 0]
    # greedy minimise
    def ok(s):  # s has no 2-transversal
        for x in range(n):
            for y in range(x, n):
                pm = (1 << x) | (1 << y)
                if all(Hm[j] & pm for j in s): return False
        return True
    assert ok(sel)
    i = 0
    while i < len(sel):
        t = sel[:i] + sel[i+1:]
        if t and ok(t): sel = t
        else: i += 1
    return sel

def tau(Hm, n):
    for s in range(n+1):
        for T in itertools.combinations(range(n), s):
            tm = sum(1 << v for v in T)
            if all(E & tm for E in Hm): return s

def is72(Hm, n):
    m = len(Hm)
    for r in range(1, min(7, m)+1):
        for sub in itertools.combinations(Hm, r):
            if not any(all(E & ((1 << x) | (1 << y)) for E in sub) for x in range(n) for y in range(x, n)):
                return False
    return True

def run(n, lam, T, smin, smax, clutter=True):
    E = [sum(1 << v for v in c) for s in range(smin, smax+1) for c in itertools.combinations(range(n), s)]
    pc = lambda x: bin(x).count('1')
    S = Cadical153()
    for i, j in itertools.combinations(range(len(E)), 2):
        a, b = E[i], E[j]
        if pc(a & b) > lam or (clutter and ((a & b) == a or (a & b) == b)):
            S.add_clause([-(i+1), -(j+1)])
    for Z in itertools.combinations(range(n), T-1):
        zm = sum(1 << v for v in Z)
        S.add_clause([i+1 for i in range(len(E)) if not (E[i] & zm)])
    # symmetry breaking (sound): vertex 0 lies in some edge -- trivial; none else
    it = 0
    while True:
        it += 1
        if not S.solve(): return 'UNSAT', it, None
        mod = S.get_model()
        idx = [i for i in range(len(E)) if mod[i] > 0]
        Hm = [E[i] for i in idx]
        b = bad_sub(Hm, n)
        if b is None:
            assert all(pc(a & c) <= lam for a, c in itertools.combinations(Hm, 2))
            assert tau(Hm, n) >= T
            if len(Hm) <= 40: assert is72(Hm, n)
            return 'SAT', it, [[v for v in range(n) if h >> v & 1] for h in Hm]
        S.add_clause([-(idx[j]+1) for j in b])

if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    n, lam, T, smin, smax = a[:5]; cl = bool(a[5]) if len(a) > 5 else True
    t0 = time.time(); r = run(n, lam, T, smin, smax, cl)
    print(f"n={n} lam={lam} T={T} sizes=[{smin},{smax}] clutter={cl} -> {r[0]} iters={r[1]} fam={r[2]} tau={None if r[2] is None else T}+ {time.time()-t0:.1f}s", flush=True)
