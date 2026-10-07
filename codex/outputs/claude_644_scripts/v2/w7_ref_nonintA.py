"""Referee (w7, claim key nonintA): independent exact check of Theorem A (orientation / partner copies)
and Theorem A' (hybrid: block gadgets + h-cost orientation) from notes_nonint.md, plus negative controls.

Everything is exact (finite sets, SAT with exact cardinality constraints).  Written from scratch; does not import
the w5 scripts.

Usage: python3 w7_ref_nonintA.py MODE TRIALS SEED
  MODE in {A, hyb, neg_nopad, neg_shared, neg_hminus, neg_unoriented, seven2, peel}
"""
import itertools, random, sys
from pysat.solvers import Minicard

# ---------------------------------------------------------------- basic exact tools
def has_cover(edges, s):
    """exact: is there a transversal of size <= s ?  (edges: iterable of frozensets of hashable points)"""
    edges = list(edges)
    if any(len(e) == 0 for e in edges):
        return False
    if s < 0:
        return False
    pts = sorted(set().union(*edges), key=repr) if edges else []
    if not edges:
        return True
    idx = {p: i + 1 for i, p in enumerate(pts)}
    with Minicard() as S:
        for e in edges:
            S.add_clause([idx[p] for p in e])
        S.add_atmost(list(range(1, len(pts) + 1)), s)
        return S.solve()

def tau(edges):
    edges = list(edges)
    s = 0
    while not has_cover(edges, s):
        s += 1
    return s

def is_72(edges):
    """exact brute force of (7,2): every <=7 edges have a transversal of size <=2."""
    E = list(set(edges))
    pts = sorted(set().union(*E), key=repr)
    pairs = [frozenset([p]) for p in pts] + [frozenset(c) for c in itertools.combinations(pts, 2)]
    # for each pair, bitmask of edges it pierces
    masks = []
    for P in pairs:
        m = 0
        for i, e in enumerate(E):
            if e & P:
                m |= 1 << i
        masks.append(m)
    for r in range(1, min(7, len(E)) + 1):
        for sub in itertools.combinations(range(len(E)), r):
            sm = 0
            for i in sub:
                sm |= 1 << i
            if not any((m & sm) == sm for m in masks):
                return False
    return True

def disjoint_pairs(H):
    return [(i, j) for i in range(len(H)) for j in range(i + 1, len(H)) if not (H[i] & H[j])]

# ---------------------------------------------------------------- constructions
class Fresh:
    def __init__(self, tag):
        self.tag = tag; self.c = 0
    def __call__(self):
        self.c += 1
        return (self.tag, self.c)

def pad(H, N, t, shared=False):
    """E* = E padded by private new points to size max(|E|,t) for E in N (E unchanged otherwise).
    shared=True is a NEGATIVE CONTROL: all padded edges draw from one common pool of t points."""
    fr = Fresh('y'); pool = [('Y', i) for i in range(t)]
    star = {}
    for i, E in enumerate(H):
        S = set(E)
        if i in N:
            if shared:
                for p in pool:
                    if len(S) >= t: break
                    S.add(p)
            else:
                while len(S) < t:
                    S.add(fr())
        star[i] = frozenset(S)
    return star

def all_transversals_upto(sets, h):
    ground = sorted(set().union(*sets), key=repr)
    out = []
    for s in range(1, h + 1):
        for X in itertools.combinations(ground, s):
            X = frozenset(X)
            if all(X & S for S in sets):
                out.append(X)
    return out

def hcost(Ostar, t):
    """h(E,O) = max over Z (|Z|<t) of tau({F*\\Z}); Z restricted to the union WLOG (points outside are irrelevant)."""
    ground = sorted(set().union(*Ostar), key=repr)
    best = 0
    for z in range(0, t):
        for Z in itertools.combinations(ground, z):
            Z = set(Z)
            red = [S - Z for S in Ostar]
            assert all(red), 'F* inside Z: padding failed'
            best = max(best, tau(red))
    return best

def build(H, t, blocks, orient, star, xmode='one', hdelta=0):
    """Hybrid construction.  blocks: list of sets of indices (each gets a gadget: all r-subsets of a (2r-1)-set,
    r = tau(block)).  orient: dict i -> list of out-neighbours.  xmode 'one': X = one point from each F* (Theorem A);
    'h': X ranges over all transversals of {F*} of size <= h(E,O)+hdelta (Theorem A').
    Returns (Hpp, cost) where cost = max_E (sum of gadget ranks + |X|max)."""
    gad = []
    for b, B in enumerate(blocks):
        r = tau([H[i] for i in B])
        W = [('w', b, j) for j in range(2 * r - 1)]
        gad.append([frozenset(c) for c in itertools.combinations(W, r)])
    Hpp = []; cost = 0
    for i in range(len(H)):
        myg = [gad[b] for b, B in enumerate(blocks) if i in B]
        outs = orient.get(i, [])
        if outs:
            Ostar = [star[j] for j in outs]
            if xmode == 'one':
                Xs = [frozenset(c) for c in itertools.product(*[sorted(S, key=repr) for S in Ostar])]
                xc = len(outs)
            else:
                from math import comb
                if sum(comb(len(set().union(*Ostar)), s_) for s_ in range(1, len(outs) + 1)) > 30000:
                    return None, None   # skip instances too large to enumerate exactly
                h0 = hcost(Ostar, t)
                if hdelta and h0 + hdelta < 1:
                    h = h0  # negative control only lowers h when the result is still >= 1
                else:
                    h = h0 + hdelta
                Xs = all_transversals_upto(Ostar, max(h, 0))
                xc = max(h, 0)
        else:
            Xs = [frozenset()]; xc = 0
        cost = max(cost, sum(len(g[0]) for g in myg) + xc)
        for combo in itertools.product(*myg):
            base = star[i].union(*combo) if combo else star[i]
            for X in Xs:
                Hpp.append(frozenset(base | X))
        if len(Hpp) > 2500:
            return None, None
    return list(set(Hpp)), cost

# ---------------------------------------------------------------- random instances
def rand_family(rng, n, k, m):
    H = list({frozenset(rng.sample(range(n), rng.randint(1, k))) for _ in range(m)})
    return H

def rand_orient(rng, dis):
    o = {}
    for (i, j) in dis:
        if rng.random() < 0.5: o.setdefault(i, []).append(j)
        else: o.setdefault(j, []).append(i)
    return o

def check(H, Hpp, t, k, cost):
    inter = all(a & b for a, b in itertools.combinations(Hpp, 2))
    sup = all(any(h <= e for h in H) for e in Hpp)
    rank = max(len(e) for e in Hpp) <= max(k, t) + cost
    notau = not has_cover(Hpp, t - 1)
    return inter, sup, rank, notau

def main():
    mode, trials, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    tested = 0; fails = {}
    for tr in range(trials):
        n = rng.randint(5, 9); k = rng.randint(2, 4); m = rng.randint(3, 9)
        H = rand_family(rng, n, k, m)
        if mode == 'seven2':
            # real (7,2) families with at least one disjoint pair
            if not disjoint_pairs(H) or not is_72(H):
                continue
        t = tau(H)
        dis = disjoint_pairs(H)
        if not dis:
            continue
        N = set(i for p in dis for i in p)
        star = pad(H, N, t, shared=(mode == 'neg_shared'))
        if mode == 'neg_nopad':
            star = {i: H[i] for i in range(len(H))}
        blocks = []; orient = {}
        if mode in ('hyb',):
            # random blocks covering a random subset of the disjoint pairs; rest oriented, h-cost X
            cand = list(N); rng.shuffle(cand)
            for _ in range(rng.randint(1, 2)):
                B = set(rng.sample(cand, min(len(cand), rng.randint(2, 4))))
                blocks.append(B)
            rest = [(i, j) for (i, j) in dis if not any(i in B and j in B for B in blocks)]
            orient = rand_orient(rng, rest)
            Hpp, cost = build(H, t, blocks, orient, star, xmode='h')
        elif mode == 'neg_hminus':
            orient = rand_orient(rng, dis)
            Hpp, cost = build(H, t, [], orient, star, xmode='h', hdelta=-1)
        elif mode == 'neg_unoriented':
            orient = rand_orient(rng, dis[1:])  # drop one disjoint pair
            Hpp, cost = build(H, t, [], orient, star, xmode='one')
        else:
            orient = rand_orient(rng, dis)
            Hpp, cost = build(H, t, [], orient, star, xmode='one')
        if not Hpp:
            continue
        tested += 1
        res = check(H, Hpp, t, k, cost)
        if mode == 'seven2' and len(Hpp) <= 16:
            res = res + (is_72(Hpp),)
        if not all(res):
            key = tuple(res)
            fails[key] = fails.get(key, 0) + 1
            if fails[key] == 1:
                print('FAIL', res, 't=', t, 'H=', [sorted(e) for e in H], 'orient=', orient, 'blocks=', blocks)
    print(f'mode={mode} seed={seed} tested={tested} failure-patterns={fails}')

if __name__ == '__main__':
    main()
