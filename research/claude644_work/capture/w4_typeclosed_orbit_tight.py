"""Orbit families at the TIGHTEST capacity: for random base types, the least integer capacity X
(in units 1/D, equal parts) with tau*(orbit, X) > 3D/4; then test pairs and the all-support MILP.
Discovery only."""
import sys, random, time, json
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp, pair_bad, load_cap42
from w4_typeclosed_orbit_search import orbit, cyclic, dihedral, full, rand_type

def tightest_X(bases, group, p, D):
    lo, hi = 1, 3*D
    def ok(X):
        A = sorted(set(t for b in bases for t in orbit(b, group)))
        if any(max(a) > X for a in A): return False
        ts = tau_star(A, [X]*p)
        return ts is not None and 4*ts > 3*D
    # tau* monotone in X once all types fit
    Xmin = max(max(b) for b in bases)
    if not ok(hi): return None
    lo = Xmin
    if ok(lo): return lo
    while hi - lo > 1:
        mid = (lo + hi)//2
        if ok(mid): hi = mid
        else: lo = mid
    return hi

def run(p, grp, nt, trials, seed, D):
    rng = random.Random(seed); cap = load_cap42()
    group = {'cyc': cyclic, 'dih': dihedral, 'sym': full}[grp](p)
    st = {'tried': 0, 'pairbad': 0, 'milpbad': 0, 'none': 0, 'unknown': 0, 'fanohom': 0}
    found = []; t0 = time.time(); ntypes_hist = {}
    for tr in range(trials):
        bases = [rand_type(p, D, D, rng, sparse=True) for _ in range(nt)]
        X = tightest_X(bases, group, p, D)
        if X is None: continue
        A = sorted(set(t for b in bases for t in orbit(b, group)))
        st['tried'] += 1
        if any(all(7*a[i] <= 4*X for i in range(p)) for a in A): st['fanohom'] += 1; continue
        xf = [F(X, D)]*p; An = [tuple(F(v, D) for v in a) for a in A]
        if any(pair_bad(a, b, xf, cap) for a in An for b in An): st['pairbad'] += 1; continue
        s, assign, cells = bad_tuple_milp(An, xf, time_limit=120)
        if s == 'BAD':
            st['milpbad'] += 1; k = len(set(assign)); ntypes_hist[k] = ntypes_hist.get(k, 0) + 1
            continue
        st['none' if s == 'NONE' else 'unknown'] += 1
        found.append({'p': p, 'D': D, 'X': X, 'A': A, 'status': s, 'tau*': str(tau_star(A, [X]*p))})
        print('CANDIDATE', found[-1], flush=True)
    st['sec'] = round(time.time()-t0, 1); st['types_in_bad'] = ntypes_hist
    return st, found

if __name__ == '__main__':
    p = int(sys.argv[1]); grp = sys.argv[2]; nt = int(sys.argv[3]); trials = int(sys.argv[4])
    seed = int(sys.argv[5]); D = int(sys.argv[6])
    st, found = run(p, grp, nt, trials, seed, D)
    print(json.dumps(st))
    json.dump(found, open(f'w4_tc_tight_{p}_{grp}_{nt}_{seed}_{D}.json', 'w'))
