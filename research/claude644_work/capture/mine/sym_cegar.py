#!/usr/bin/env python3
"""Symmetry-reduced CEGAR search for k-uniform (7,2) families with tau >= T on Z_n (or another
permutation group given by generators), used to probe f(8,7) = 7 (FKW's suspicion).

Main SAT: one Boolean per G-orbit of k-subsets ("orbit chosen" = all its members are edges).
  tau >= T  <=>  every (n-T+1)-subset contains an edge: one clause per orbit of (n-T+1)-sets.
CEGAR: given a model, build the family, look for a bad 7-tuple (no 2-point transversal, points may
coincide) with a second SAT; if found, add the clause "not all these (<=7) orbits chosen".
UNSAT of the main problem => no G-invariant family with tau >= T has property (7,2).
A returned family is re-verified by an independent exhaustive (7,2) check (only feasible for small
families) or by the SAT bad-tuple search returning UNSAT (which is itself exact)."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def cyclic_gens(n):
    return [tuple((i + 1) % n for i in range(n))]

def orbit_of(s, gens, n):
    seen = {s}
    stack = [s]
    while stack:
        cur = stack.pop()
        for g in gens:
            img = frozenset(g[i] for i in cur)
            if img not in seen:
                seen.add(img)
                stack.append(img)
    return seen

def orbits(n, r, gens):
    idx = {}
    reps = []
    for c in itertools.combinations(range(n), r):
        s = frozenset(c)
        if s in idx:
            continue
        o = orbit_of(s, gens, n)
        j = len(reps)
        reps.append(sorted(o, key=sorted))
        for m in o:
            idx[m] = j
    return reps, idx

def find_bad_tuple(edges, n, max_conf=None):
    """edges: list of frozensets. Return 7 indices (with repetition allowed) forming a bad tuple, or None."""
    m = len(edges)
    var = {}
    top = [0]
    def nv():
        top[0] += 1
        return top[0]
    s = [[nv() for _ in range(m)] for _ in range(7)]
    clauses = []
    for j in range(7):
        clauses.append(s[j][:])
        enc = CardEnc.atmost(lits=s[j], bound=1, top_id=top[0], encoding=EncType.seqcounter)
        top[0] = max(top[0], enc.nv)
        clauses.extend(enc.clauses)
    # symmetry breaking: slot order by index (non-strict)
    # for each pair x<=y some slot's edge avoids both
    avoid = {}
    for x in range(n):
        for y in range(x, n):
            lits = []
            for j in range(7):
                a = nv()
                lits.append(a)
                ok = [s[j][e] for e in range(m) if x not in edges[e] and y not in edges[e]]
                clauses.append([-a] + ok)
            clauses.append(lits)
    sol = Cadical153(bootstrap_with=clauses)
    if sol.solve():
        model = set(l for l in sol.get_model() if l > 0)
        pick = []
        for j in range(7):
            for e in range(m):
                if s[j][e] in model:
                    pick.append(e)
                    break
        sol.delete()
        return pick
    sol.delete()
    return None

def two_pierceable(sets, n):
    for x in range(n):
        rest = [e for e in sets if x not in e]
        if not rest:
            return True
        c = frozenset.intersection(*rest)
        if c:
            return True
    return False

def run(n, k, T, gens=None, max_iter=100000, verbose=True):
    gens = gens or cyclic_gens(n)
    t0 = time.time()
    ek, idxk = orbits(n, k, gens)
    w = n - T + 1
    ew, _ = orbits(n, w, gens)
    if verbose:
        print(f"n={n} k={k} T={T}: {len(ek)} k-orbits, {len(ew)} {w}-orbits", flush=True)
    main = Cadical153()
    for orb in ew:
        S = orb[0]
        lits = sorted({idxk[frozenset(c)] + 1 for c in itertools.combinations(sorted(S), k)})
        main.add_clause(lits)
    it = 0
    while it < max_iter:
        it += 1
        if not main.solve():
            print(f"UNSAT after {it-1} cuts, {time.time()-t0:.1f}s: no G-invariant (7,2) family with tau>={T}", flush=True)
            return None
        model = main.get_model()
        chosen = [i for i in range(len(ek)) if model[i] > 0]
        edges = [e for i in chosen for e in ek[i]]
        bad = find_bad_tuple(edges, n)
        if bad is None:
            print(f"FOUND after {it-1} cuts, {time.time()-t0:.1f}s: {len(chosen)} orbits, {len(edges)} edges", flush=True)
            return chosen, ek, edges
        tup = [edges[e] for e in bad]
        assert not two_pierceable(tup, n), "bad-tuple SAT returned a 2-pierceable tuple"
        cut = sorted({idxk[e] + 1 for e in tup})
        main.add_clause([-l for l in cut])
        if verbose and it % 50 == 0:
            print(f"  iter {it}: {len(chosen)} orbits chosen, cut size {len(cut)}, {time.time()-t0:.1f}s", flush=True)
    print("iteration limit")
    return None

if __name__ == '__main__':
    n, k, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    res = run(n, k, T)
    if res:
        chosen, ek, edges = res
        print("orbit reps:", [sorted(ek[i][0]) for i in chosen])
