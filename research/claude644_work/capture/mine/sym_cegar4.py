#!/usr/bin/env python3
"""Z_n-invariant CEGAR for k-uniform (7,2) families with tau >= T (probe of f(8,7)=7).
Bad-subfamily finder = set-cover SAT (as p644_sat.py): choose <= 7 edges of the current family so that
every pair {x,y} (x != y) is avoided by some chosen edge; one persistent solver, family given by
assumptions on orbit literals; rotation symmetry: some chosen edge contains 0.
FOUND => the finder's UNSAT certifies (7,2) for the whole invariant family."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def orbits(n, r):
    idx, reps = {}, []
    for c in itertools.combinations(range(n), r):
        s = frozenset(c)
        if s in idx: continue
        o, cur = [], s
        for _ in range(n):
            if cur not in o: o.append(cur)
            cur = frozenset((i + 1) % n for i in cur)
        j = len(reps); reps.append(o)
        for m in o: idx[m] = j
    return reps, idx

def two_pierceable(sets, n):
    for x in range(n):
        rest = [e for e in sets if x not in e]
        if not rest or frozenset.intersection(*rest): return True
    return False

def run(n, k, T, max_iter=10**6, log_every=500):
    t0 = time.time()
    ek, idxk = orbits(n, k)
    w = n - T + 1
    ew, _ = orbits(n, w)
    allk = [frozenset(c) for c in itertools.combinations(range(n), k)]
    no = len(ek); m = len(allk)
    print(f"n={n} k={k} T={T}: {no} k-orbits, {len(ew)} {w}-orbits, {m} k-sets", flush=True)
    avail = list(range(1, no + 1)); f = list(range(no + 1, no + m + 1)); top = no + m
    cl = [[-f[e], avail[idxk[allk[e]]]] for e in range(m)]
    for x, y in itertools.combinations(range(n), 2):
        cl.append([f[e] for e in range(m) if x not in allk[e] and y not in allk[e]])
    cl.append([f[e] for e in range(m) if 0 in allk[e]])
    enc = CardEnc.atmost(lits=f, bound=7, top_id=top, encoding=EncType.seqcounter)
    cl.extend(enc.clauses)
    bf = Cadical153(bootstrap_with=cl)
    main = Cadical153()
    for orb in ew:
        S = sorted(orb[0])
        main.add_clause(sorted({idxk[frozenset(c)] + 1 for c in itertools.combinations(S, k)}))
    print(f"  built {time.time()-t0:.1f}s", flush=True)
    it = 0
    while it < max_iter:
        it += 1
        if not main.solve():
            print(f"UNSAT after {it-1} cuts, {time.time()-t0:.1f}s: no Z_{n}-invariant (7,2) family with tau>={T}", flush=True)
            return None
        model = main.get_model()
        chosen = set(i for i in range(no) if model[i] > 0)
        ass = [avail[i] if i in chosen else -avail[i] for i in range(no)]
        if not bf.solve(assumptions=ass):
            print(f"FOUND after {it-1} cuts, {time.time()-t0:.1f}s: {len(chosen)} orbits", flush=True)
            return sorted(chosen), ek
        sm = set(l for l in bf.get_model() if l > 0)
        bad = [allk[e] for e in range(m) if f[e] in sm]
        assert not two_pierceable(bad, n)
        main.add_clause(sorted({-(idxk[e] + 1) for e in bad}))
        if it % log_every == 0:
            print(f"  iter {it}: chosen {len(chosen)}, bad size {len(bad)}, {time.time()-t0:.1f}s", flush=True)
    print("iteration limit"); return None

if __name__ == '__main__':
    n, k, T = map(int, sys.argv[1:4])
    r = run(n, k, T)
    if r:
        chosen, ek = r
        print("orbit reps:", [sorted(ek[i][0]) for i in chosen], flush=True)
