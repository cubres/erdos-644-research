"""Referee w7, claim core#2 (Theorem L).  Independent statement test + sharpness data.
Question: does a NON-UNIFORM family H of subsets of [n] (sizes in [smin,smax]) exist with
  (i) |E&F| <= lam for distinct E,F,  (ii) tau(H) >= T,  (iii) every <=7 edges have a 2-point transversal?
Theorem L predicts UNSAT whenever T >= 3lam+1.  Clutter WLOG (deleting a superset keeps (i)-(iii) except
it can only lower tau -- no: deleting a superset E of F keeps tau since any set hitting F hits E; keeps (i),(iii)).
(7,2) is enforced lazily: a chosen family is bad iff some <=7 of its edges are each missed by ... i.e. every
pair {x,y} (x<=y) is disjoint from some selected edge.  Found by an independent SAT (at most 7 selected).
Usage: python3 w7_ref_core2_sat.py n lam T smin smax"""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def bad_subfamily(H, n):
    m = len(H)
    S = Cadical153()
    enc = CardEnc.atmost(lits=list(range(1, m+1)), bound=7, top_id=m, encoding=EncType.seqcounter)
    for c in enc.clauses: S.add_clause(c)
    for x in range(n):
        for y in range(x, n):
            S.add_clause([j+1 for j in range(m) if x not in H[j] and y not in H[j]])
    if S.solve():
        mod = set(l for l in S.get_model() if l > 0)
        return [j for j in range(m) if (j+1) in mod]
    return None

def tau(H, n):
    for s in range(n+1):
        for T in itertools.combinations(range(n), s):
            Ts = set(T)
            if all(E & Ts for E in H): return s

def run(n, lam, T, smin, smax):
    E = [frozenset(c) for s in range(smin, smax+1) for c in itertools.combinations(range(n), s)]
    S = Cadical153()
    for i, j in itertools.combinations(range(len(E)), 2):
        if len(E[i] & E[j]) > lam or E[i] < E[j] or E[j] < E[i]:
            S.add_clause([-(i+1), -(j+1)])
    for Z in itertools.combinations(range(n), T-1):
        Zs = set(Z); S.add_clause([i+1 for i in range(len(E)) if not (E[i] & Zs)])
    # mild symmetry breaking: point 0 has max degree is not sound in general -> none
    it = 0
    while True:
        it += 1
        if not S.solve(): return 'UNSAT', it, None
        pos = set(l for l in S.get_model() if l > 0)
        idx = [i for i in range(len(E)) if (i+1) in pos]
        H = [E[i] for i in idx]
        b = bad_subfamily(H, n)
        if b is None:
            # independent verification of the witness
            assert all(len(A & B) <= lam for A, B in itertools.combinations(H, 2))
            assert tau(H, n) >= T
            for sub in itertools.combinations(range(len(H)), min(7, len(H))):
                assert any(all((x in H[j] or y in H[j]) for j in sub) for x in range(n) for y in range(x, n))
            return 'SAT', it, [sorted(h) for h in H]
        S.add_clause([-(idx[j]+1) for j in b])

if __name__ == '__main__':
    n, lam, T, smin, smax = map(int, sys.argv[1:6]); t0 = time.time()
    r = run(n, lam, T, smin, smax)
    print(f"n={n} lam={lam} T={T} sizes=[{smin},{smax}] -> {r[0]} iters={r[1]} fam={r[2]} {time.time()-t0:.1f}s", flush=True)
