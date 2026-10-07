"""Exact check (brute force) of the ORIENTATION / PARTNER-COPY reduction on random small families.
For random H: build H'' (private padding to size max(|E|,t), copies with one point from each out-neighbour's F*),
verify: H'' intersecting; tau(H'') >= tau(H); rank bound; every H''-edge contains an H-edge."""
import random, itertools, sys

def tau(edges, ground, upto=None):
    edges = [frozenset(e) for e in edges]
    ground = sorted(ground)
    for s in range(0, len(ground)+1):
        if upto is not None and s > upto: return None
        for S in itertools.combinations(ground, s):
            S = set(S)
            if all(e & S for e in edges): return s
    return len(ground)

def has_transversal_of_size(edges, ground, s):
    for S in itertools.combinations(sorted(ground), s):
        S = set(S)
        if all(e & S for e in edges): return True
    return False

def build(H, t, orient):
    # H: list of frozensets; orient: dict idx -> list of out-neighbour idx
    n_next = [1000]
    star = {}
    N = set(i for i in orient) | set(j for i in orient for j in orient[i])
    for i in range(len(H)):
        E = set(H[i])
        if i in N:
            while len(E) < t:
                E.add(n_next[0]); n_next[0] += 1
        star[i] = frozenset(E)
    Hpp = []
    for i in range(len(H)):
        outs = orient.get(i, [])
        if not outs:
            Hpp.append(star[i]); continue
        for choice in itertools.product(*[sorted(star[j]) for j in outs]):
            Hpp.append(frozenset(star[i] | set(choice)))
    return Hpp, star

def run(trials, seed):
    random.seed(seed); bad = 0; tested = 0
    for tr in range(trials):
        n = random.randint(5, 8); k = random.randint(2, 4); m = random.randint(3, 8)
        H = list({frozenset(random.sample(range(n), random.randint(1, k))) for _ in range(m)})
        t = tau(H, range(n))
        if t > k or t == 0: continue
        dis = [(i, j) for i in range(len(H)) for j in range(i+1, len(H)) if not (H[i] & H[j])]
        orient = {}
        for (i, j) in dis:
            if random.random() < 0.5: orient.setdefault(i, []).append(j)
            else: orient.setdefault(j, []).append(i)
        for i in list(orient):
            for j in orient[i]: orient.setdefault(j, orient.get(j, []))
        d = max([len(v) for v in orient.values()] + [0])
        ncopies = 1
        Hpp, star = build(H, t, orient)
        if len(Hpp) > 4000: continue
        tested += 1
        ground = set().union(*Hpp)
        inter = all(a & b for a, b in itertools.combinations(Hpp, 2))
        rank_ok = max(len(e) for e in Hpp) <= max(k, t) + d
        sup_ok = all(any(h <= e for h in H) for e in Hpp)
        # tau(H'') >= t  <=> no transversal of size t-1
        tau_ok = not has_transversal_of_size(Hpp, ground, t-1) if t >= 1 else True
        if not (inter and rank_ok and sup_ok and tau_ok):
            bad += 1
            print('FAIL', H, t, orient, inter, rank_ok, sup_ok, tau_ok); break
    print(f'seed {seed}: tested {tested}, failures {bad}')

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]))
