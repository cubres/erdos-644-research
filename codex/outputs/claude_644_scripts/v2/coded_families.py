#!/usr/bin/env python3
"""Probe f(8,7)=7 with 'coded' families: k-subsets E of [n] with |E cap X_j| = c_j (mod q_j).
tau computed exactly (every (n-T+1)-set contains an edge); (7,2) certified by set-cover SAT UNSAT."""
import itertools, sys, random
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def is72(edges, n):
    m = len(edges)
    s = Cadical153()
    for x, y in itertools.combinations(range(n), 2):
        cl = [e + 1 for e in range(m) if x not in edges[e] and y not in edges[e]]
        if not cl: s.delete(); return True, None
        s.add_clause(cl)
    enc = CardEnc.atmost(lits=list(range(1, m + 1)), bound=7, top_id=m, encoding=EncType.seqcounter)
    for c in enc.clauses: s.add_clause(c)
    if s.solve():
        mod = s.get_model(); bad = [edges[e] for e in range(m) if mod[e] > 0]; s.delete(); return False, bad
    s.delete(); return True, None

def tau_at_least(edges, n, T):
    em = [sum(1 << v for v in e) for e in edges]
    for U in itertools.combinations(range(n), n - T + 1):
        um = sum(1 << v for v in U)
        if not any((e & ~um) == 0 for e in em): return False
    return True

def tau(edges, n):
    T = 1
    while T <= n and tau_at_least(edges, n, T + 1): T += 1
    return T

def family(n, k, cons):
    out = []
    for c in itertools.combinations(range(n), k):
        s = set(c)
        if all(len(s & X) % q == r for X, q, r in cons): out.append(frozenset(c))
    return out

if __name__ == '__main__':
    k = 8
    random.seed(1)
    tried = 0
    for n in (15, 16, 17):
        # single parity / mod-3 constraint on a set X of size a
        for q in (2, 3):
            for a in range(1, n):
                X = set(range(a))
                for r in range(q):
                    H = family(n, k, [(X, q, r)])
                    if not H: continue
                    if not tau_at_least(H, n, 7): continue
                    ok, bad = is72(H, n); tried += 1
                    t = tau(H, n)
                    print(f"n={n} |X|={a} mod {q}={r}: |H|={len(H)} tau={t} (7,2)={ok}", flush=True)
                    if ok and t >= 7: print("   *** CANDIDATE f(8,7)>=7 ***", flush=True)
    print("tried", tried)
