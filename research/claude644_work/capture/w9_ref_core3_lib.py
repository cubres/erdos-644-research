"""w9 referee [core#3] library: independent (bitmask) implementations. No imports from attacker scripts."""
import itertools
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
def popc(x): return bin(x).count('1')
def min_transversal(F, n):
    """exact minimum transversal (bitmask) of family F (list of nonzero masks) on vertices 0..n-1"""
    if not F: return 0
    for s in range(0, n+1):
        for T in itertools.combinations(range(n), s):
            m = 0
            for v in T: m |= 1 << v
            if all(E & m for E in F): return m
    raise ValueError("empty edge?")
def _can(F, b):
    if not F: return True
    if b == 0: return False
    E = min(F, key=popc)
    x = E
    while x:
        v = x & -x; x ^= v
        if _can([G for G in F if not (G & v)], b-1): return True
    return False
def tau(F, n):
    """exact tau by iterative-deepening branching on a smallest unhit edge"""
    F = list(set(F)); b = 0
    while not _can(F, b): b += 1
    return b
def tau_brute(F, n): return popc(min_transversal(F, n))
def bad_tuple(H, n, force=None):
    """return a list of <=7 edges of H with no transversal of size <=2, or None.  force: index that must be used."""
    m = len(H)
    covers = [1 << i for i in range(n)] + [(1 << i) | (1 << j) for i in range(n) for j in range(i+1, n)]
    cls = []
    for c in covers:
        cl = [e+1 for e in range(m) if not (H[e] & c)]
        if not cl: return None
        cls.append(cl)
    top = m
    card = CardEnc.atmost(lits=list(range(1, m+1)), bound=7, top_id=top, encoding=EncType.seqcounter)
    with Minisat22(bootstrap_with=cls + card.clauses) as s:
        ok = s.solve(assumptions=[force+1] if force is not None else [])
        if not ok: return None
        mod = set(l for l in s.get_model() if 0 < l <= m)
        T = [H[e-1] for e in sorted(mod)]
    # independent brute verification
    assert len(T) <= 7
    for c in covers: assert any(not (E & c) for E in T)
    return T
def is72(H, n): return bad_tuple(H, n) is None
def lpp_data(H, n, lam):
    """dict E -> tau(N_lam[E]),  N_lam[E] = {F : |E&F| > lam}"""
    return {E: tau([F for F in H if popc(E & F) > lam], n) for E in H}
def five(t, lam, delta, beta):
    return [3*delta <= t-1, 2*delta+beta <= t-1, 2*lam+beta <= t-1, 2*lam+delta <= t-1, 3*lam <= t-1]
