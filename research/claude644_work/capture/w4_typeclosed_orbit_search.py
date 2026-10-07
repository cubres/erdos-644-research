"""Random search for counterexamples among ORBIT families: A = orbit(s) of one or two base types under
a group acting on p equal parts (cyclic Z_p or dihedral or full S_p).  Discovery only.
For each sample: exact tau* (rational, denominators 1/Dg); if tau* > 3/4 run the all-support MILP.
"""
import sys, random, itertools, time, json
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp, single_bad, pair_bad, load_cap42

def orbit(a, group):
    return sorted(set(tuple(a[g[i]] for i in range(len(a))) for g in group))

def cyclic(p): return [[(i + s) % p for i in range(p)] for s in range(p)]
def dihedral(p): return cyclic(p) + [[(s - i) % p for i in range(p)] for s in range(p)]
def full(p): return [list(g) for g in itertools.permutations(range(p))]

def rand_type(p, D, X, rng, sparse):
    # random composition of D into p parts with caps X, optionally with forced zeros
    while True:
        k = rng.randint(1, p) if sparse else p
        supp = rng.sample(range(p), k)
        w = [rng.random() ** rng.choice([1, 2, 3]) for _ in supp]
        s = sum(w); a = [0]*p
        for i, wi in zip(supp, w): a[i] = int(round(D * wi / s))
        diff = D - sum(a)
        a[supp[0]] += diff
        if all(0 <= a[i] <= X for i in range(p)): return tuple(a)

def run(p, grp, ntypes, trials, seed, D=60, milp_limit=60):
    rng = random.Random(seed); cap = load_cap42()
    group = {'cyc': cyclic, 'dih': dihedral, 'sym': full}[grp](p)
    found = []; stats = {'tried': 0, 'tau_ok': 0, 'pairbad': 0, 'milpbad': 0, 'none': 0, 'unknown': 0}
    t0 = time.time()
    for tr in range(trials):
        X = rng.randint(D // p + 1, D)        # capacity in units of 1/D
        if p * X < 7 * D / 4: continue
        base = [rand_type(p, D, X, rng, sparse=True) for _ in range(ntypes)]
        A = sorted(set(t for b in base for t in orbit(b, group)))
        A = [a for a in A if not all(7*a[i] <= 4*X for i in range(p))]
        if not A: continue
        stats['tried'] += 1
        ts = tau_star(A, [X]*p)
        if ts is None or 4*ts <= 3*D: continue
        stats['tau_ok'] += 1
        xf = [F(X, D)]*p; An = [tuple(F(v, D) for v in a) for a in A]
        if any(pair_bad(a, b, xf, cap) for a in An for b in An):
            stats['pairbad'] += 1; continue
        st, assign, cells = bad_tuple_milp(An, xf, time_limit=milp_limit)
        if st == 'BAD': stats['milpbad'] += 1; continue
        stats['none' if st == 'NONE' else 'unknown'] += 1
        found.append({'p': p, 'D': D, 'X': X, 'A': A, 'tau*': str(ts), 'status': st})
        print('CANDIDATE', found[-1], flush=True)
    stats['sec'] = round(time.time() - t0, 1)
    return stats, found

if __name__ == '__main__':
    p = int(sys.argv[1]); grp = sys.argv[2]; nt = int(sys.argv[3]); trials = int(sys.argv[4])
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    D = int(sys.argv[6]) if len(sys.argv) > 6 else 60
    stats, found = run(p, grp, nt, trials, seed, D)
    print(json.dumps(stats))
    json.dump(found, open(f'w4_tc_orbit_{p}_{grp}_{nt}_{seed}.json', 'w'))
