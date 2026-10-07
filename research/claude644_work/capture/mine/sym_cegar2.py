#!/usr/bin/env python3
"""Incremental symmetry-reduced CEGAR for k-uniform (7,2) families with tau >= T, invariant under Z_n.
Main SAT over orbit variables; one persistent 'bad-tuple' SAT over all k-subsets with slot selectors,
restricted to the current family by assumptions on orbit-availability literals.
Soundness: every cut is a genuine bad 7-tuple of orbit members (re-checked exhaustively);
a FOUND family is certified (7,2) by the UNSAT answer of the complete bad-tuple SAT."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def orbits(n, r, shift_only=True):
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

class BadFinder:
    def __init__(self, n, k, allk, idxk, norb):
        self.n = n; self.allk = allk
        top = [0]
        def nv():
            top[0] += 1; return top[0]
        self.avail = [nv() for _ in range(norb)]
        m = len(allk)
        self.s = [[nv() for _ in range(m)] for _ in range(7)]
        cl = []
        for j in range(7):
            cl.append(self.s[j][:])
            enc = CardEnc.atmost(lits=self.s[j], bound=1, top_id=top[0], encoding=EncType.seqcounter)
            top[0] = max(top[0], enc.nv); cl.extend(enc.clauses)
            for e in range(m):
                cl.append([-self.s[j][e], self.avail[idxk[allk[e]]]])
        # symmetry: slot 0 edge contains point 0
        cl.append([self.s[0][e] for e in range(m) if 0 in allk[e]])
        for x in range(n):
            for y in range(x, n):
                lits = []
                for j in range(7):
                    a = nv(); lits.append(a)
                    cl.append([-a] + [self.s[j][e] for e in range(m) if x not in allk[e] and y not in allk[e]])
                cl.append(lits)
        self.sol = Cadical153(bootstrap_with=cl)
    def find(self, chosen_set):
        ass = [self.avail[i] if i in chosen_set else -self.avail[i] for i in range(len(self.avail))]
        if not self.sol.solve(assumptions=ass): return None
        model = set(l for l in self.sol.get_model() if l > 0)
        pick = []
        for j in range(7):
            for e, v in enumerate(self.s[j]):
                if v in model: pick.append(self.allk[e]); break
        return pick

def run(n, k, T, max_iter=200000, prefer_all=False):
    t0 = time.time()
    ek, idxk = orbits(n, k)
    w = n - T + 1
    ew, _ = orbits(n, w)
    allk = [frozenset(c) for c in itertools.combinations(range(n), k)]
    print(f"n={n} k={k} T={T}: {len(ek)} k-orbits, {len(ew)} {w}-orbits, {len(allk)} k-sets", flush=True)
    bf = BadFinder(n, k, allk, idxk, len(ek))
    print(f"  bad-finder built {time.time()-t0:.1f}s", flush=True)
    main = Cadical153()
    for orb in ew:
        S = sorted(orb[0])
        main.add_clause(sorted({idxk[frozenset(c)] + 1 for c in itertools.combinations(S, k)}))
    it = 0
    while it < max_iter:
        it += 1
        if not main.solve():
            print(f"UNSAT after {it-1} cuts, {time.time()-t0:.1f}s: no Z_{n}-invariant (7,2) family with tau>={T}", flush=True)
            return None
        model = main.get_model()
        chosen = set(i for i in range(len(ek)) if model[i] > 0)
        bad = bf.find(chosen)
        if bad is None:
            print(f"FOUND after {it-1} cuts, {time.time()-t0:.1f}s: {len(chosen)} orbits", flush=True)
            return sorted(chosen), ek
        assert not two_pierceable(bad, n)
        cut = sorted({idxk[e] + 1 for e in bad})
        main.add_clause([-l for l in cut])
        if it % 200 == 0:
            print(f"  iter {it}: chosen {len(chosen)}, cut {len(cut)}, {time.time()-t0:.1f}s", flush=True)
    print("iteration limit"); return None

if __name__ == '__main__':
    n, k, T = map(int, sys.argv[1:4])
    r = run(n, k, T)
    if r:
        chosen, ek = r
        print("orbit reps:", [sorted(ek[i][0]) for i in chosen], flush=True)
