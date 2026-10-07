"""Exact brute-force check of the REFINED (h-cost) partner-copy reduction on random small families.
h(E,O) = max_{Z subset V*, |Z|<t} tau({F* \\ Z : F in O}); copies E* u X for all transversals X of {F*} with |X|<=h(E).
Checks: intersecting, every copy contains an H-edge, rank <= max(k,t)+max h, no transversal of size t-1."""
import random, itertools, sys
from w5_nonint_orient_check import tau, has_transversal_of_size

def min_transversals(sets, ground, maxsize):
    out = []
    for s in range(1, maxsize+1):
        for X in itertools.combinations(sorted(ground), s):
            X = set(X)
            if all(S & X for S in sets): out.append(frozenset(X))
    return out

def run(trials, seed):
    random.seed(seed); tested = 0
    for tr in range(trials):
        n = random.randint(5, 7); k = random.randint(2, 3); m = random.randint(3, 7)
        H = list({frozenset(random.sample(range(n), random.randint(1, k))) for _ in range(m)})
        t = tau(H, range(n))
        if t > k or t == 0: continue
        dis = [(i, j) for i in range(len(H)) for j in range(i+1, len(H)) if not (H[i] & H[j])]
        if not dis: continue
        orient = {}
        for (i, j) in dis:
            if random.random() < 0.5: orient.setdefault(i, []).append(j)
            else: orient.setdefault(j, []).append(i)
        N = set(i for e in dis for i in e)
        nxt = 100; star = {}
        for i in range(len(H)):
            E = set(H[i])
            if i in N:
                while len(E) < t: E.add(nxt); nxt += 1
            star[i] = frozenset(E)
        Vstar = set(range(n)) | set(p for s in star.values() for p in s)
        Hpp = []; hmax = 0
        for i in range(len(H)):
            outs = orient.get(i, [])
            if not outs: Hpp.append(star[i]); continue
            O = [star[j] for j in outs]
            ground = set().union(*O)
            h = 0
            for zs in range(0, t):
                for Z in itertools.combinations(sorted(ground), zs):
                    Z = set(Z)
                    tr_ = tau([S - Z for S in O], ground - Z)
                    h = max(h, tr_)
            hmax = max(hmax, h)
            for X in min_transversals(O, ground, h):
                Hpp.append(star[i] | X)
        if len(Hpp) > 3000: continue
        tested += 1
        G = set().union(*Hpp)
        ok = (all(a & b for a, b in itertools.combinations(Hpp, 2)) and
              max(len(e) for e in Hpp) <= max(k, t) + hmax and
              all(any(h_ <= e for h_ in H) for e in Hpp) and
              not has_transversal_of_size(Hpp, G, t-1))
        if not ok:
            print('FAIL', H, t, orient); return
    print(f'seed {seed}: tested {tested}, failures 0')

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]))
