#!/usr/bin/env python3
"""CEGAR v6 for Z_n-invariant k-uniform (7,2) families with tau>=T.
- main SAT prefers sparse families (negative phases);
- bad-tuple finder: (1) fast random Fano-partition search (window contains an edge? via bitmask lookup),
  (2) exact set-cover SAT fallback (persistent, assumptions) -- whose UNSAT certifies (7,2).
Cuts persisted to disk."""
import itertools, sys, time, random, os
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
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
def mask(s): return sum(1 << v for v in s)
def run(n, k, T, fano_samples=4000, seed=0):
    rng = random.Random(seed); t0 = time.time()
    ek, idxk = orbits(n, k); ew, _ = orbits(n, n - T + 1)
    allk = [frozenset(c) for c in itertools.combinations(range(n), k)]
    no, m = len(ek), len(allk)
    print(f"n={n} k={k} T={T}: {no} k-orbits, {len(ew)} cover-orbits, {m} k-sets", flush=True)
    avail = list(range(1, no + 1)); f = list(range(no + 1, no + m + 1)); top = no + m
    cl = [[-f[e], avail[idxk[allk[e]]]] for e in range(m)]
    for x, y in itertools.combinations(range(n), 2):
        cl.append([f[e] for e in range(m) if x not in allk[e] and y not in allk[e]])
    cl.append([f[e] for e in range(m) if 0 in allk[e]])
    enc = CardEnc.atmost(lits=f, bound=7, top_id=top, encoding=EncType.seqcounter); cl.extend(enc.clauses)
    bf = Cadical153(bootstrap_with=cl)
    main = Cadical153()
    for orb in ew:
        S = sorted(orb[0]); main.add_clause(sorted({idxk[frozenset(c)] + 1 for c in itertools.combinations(S, k)}))
    try: main.set_phases([-v for v in range(1, no + 1)])
    except Exception as e: print("set_phases unavailable:", e)
    cutf = f"f87v6_cuts_n{n}_k{k}_T{T}.txt"; ncuts = 0
    if os.path.exists(cutf):
        for line in open(cutf): main.add_clause([int(v) for v in line.split()]); ncuts += 1
    cutfh = open(cutf, 'a')
    kmask_of = {mask(e): e for e in allk}
    print(f"  built {time.time()-t0:.1f}s; loaded {ncuts} cuts", flush=True)
    it = 0; nfast = 0; nsat = 0
    while True:
        it += 1
        if not main.solve():
            print(f"UNSAT after {it-1} cuts ({nfast} fast, {nsat} sat), {time.time()-t0:.1f}s: no Z_{n}-invariant (7,2) family with tau>={T}", flush=True); return None
        model = main.get_model(); chosen = set(i for i in range(no) if model[i] > 0)
        edge_masks = [mask(e) for i in chosen for e in ek[i]]
        # fast Fano search: random partitions; window = union of classes off a line; need an edge inside each window
        bad = None
        if edge_masks:
            for _ in range(fano_samples):
                lab = [rng.randrange(7) for _ in range(n)]
                wins = []
                ok = True
                for line in LINES:
                    W = sum(1 << v for v in range(n) if lab[v] not in line)
                    e = next((em for em in edge_masks if em & ~W == 0), None)
                    if e is None: ok = False; break
                    wins.append(e)
                if ok:
                    tup = [kmask_of[e] for e in wins]
                    if not two_pierceable(tup, n): bad = tup; nfast += 1; break
        if bad is None:
            ass = [avail[i] if i in chosen else -avail[i] for i in range(no)]
            if not bf.solve(assumptions=ass):
                print(f"FOUND after {it-1} cuts, {time.time()-t0:.1f}s: {len(chosen)} orbits, {len(edge_masks)} edges", flush=True)
                return sorted(chosen), ek
            sm = set(l for l in bf.get_model() if l > 0); bad = [allk[e] for e in range(m) if f[e] in sm]; nsat += 1
            assert not two_pierceable(bad, n)
        c = sorted({-(idxk[e] + 1) for e in bad}); main.add_clause(c); cutfh.write(' '.join(map(str, c)) + '\n'); cutfh.flush()
        if it % 10 == 0: print(f"  iter {it}: chosen {len(chosen)} orbits, fast {nfast}, sat {nsat}, {time.time()-t0:.1f}s", flush=True)
if __name__ == '__main__':
    n, k, T = map(int, sys.argv[1:4]); r = run(n, k, T)
    if r: chosen, ek = r; print("orbit reps:", [sorted(ek[i][0]) for i in chosen], flush=True)
