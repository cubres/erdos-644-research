# Referee w7 / core#1 BREAK-IT (B1): minimum four-edge overlap sum S over ACTUAL (7,2) families.
# For fixed (k,t,n): enumerate planted quadruples G1..G4 (repeats allowed) by Venn count vectors
# (15 nonempty patterns of [4]) with S = sum c_P * C(|P|,2) = s, sizes in [lo,k], up to S4 symmetry;
# CEGAR (pysat) for a family on n points, edges of size lo..k (lo = t - floor((k+4)/5), valid for every
# (7,2) family with tau >= t), containing the planted edges, tau >= t, property (7,2) (lazy: exact bad-subfamily
# DFS from lib72).  Output: smallest s for which a family exists (per n), vs stated bound
# min(t, floor(3(2t-k-2)/2)+1) and sharpened min(t, ceil(3(2t-k-1)/2)).
import itertools, sys, time
from pysat.solvers import Cadical153
sys.path.insert(0, '.')
from lib72 import find_bad_subfamily, tau as tau_exact

def popc(x): return bin(x).count('1')
PATS = [P for r in range(1, 5) for P in itertools.combinations(range(4), r)]
W = {P: len(P) * (len(P) - 1) // 2 for P in PATS}
PERMS = list(itertools.permutations(range(4)))

def canon(vec):
    best = None
    for pi in PERMS:
        v = {}
        for P, c in vec.items():
            if c: v[tuple(sorted(pi[i] for i in P))] = c
        key = tuple(v.get(P, 0) for P in PATS)
        if best is None or key < best: best = key
    return best

def venn_vectors(s, n, lo, k):
    # counts on patterns with weight>0 must sum (weighted) to s; singletons fill sizes
    heavy = [P for P in PATS if W[P] > 0]
    out = set()
    def rec(i, rem, cur):
        if i == len(heavy):
            if rem: return
            base = [sum(c for P, c in cur.items() if j in P) for j in range(4)]
            used = sum(cur.values())
            if any(b > k for b in base): return
            need = [max(0, lo - b) for b in base]
            # singletons: choose sizes from need..k-base; enumerate all (small ranges)
            rngs = [range(need[j], k - base[j] + 1) for j in range(4)]
            for sing in itertools.product(*rngs):
                if used + sum(sing) > n: continue
                v = dict(cur)
                for j in range(4):
                    if sing[j]: v[(j,)] = sing[j]
                out.add(canon(v))
            return
        P = heavy[i]
        for c in range(rem // W[P] + 1):
            if c: cur[P] = c
            rec(i + 1, rem - c * W[P], cur)
            cur.pop(P, None)
    rec(0, s, {})
    return sorted(out)

def build_edges(key):
    G = [0, 0, 0, 0]; v = 0
    for P, c in zip(PATS, key):
        for _ in range(c):
            for j in P: G[j] |= 1 << v
            v += 1
    return G, v

def cegar(n, k, t, lo, planted, maxit=20000):
    cand = [sum(1 << x for x in c) for r in range(lo, k + 1) for c in itertools.combinations(range(n), r)]
    idx = {e: i + 1 for i, e in enumerate(cand)}
    S = Cadical153()
    for e in set(planted):
        if e not in idx: return None, 0
        S.add_clause([idx[e]])
    for c in itertools.combinations(range(n), t - 1):
        m = sum(1 << x for x in c)
        S.add_clause([idx[e] for e in cand if not e & m])
    it = 0
    while S.solve():
        it += 1
        if it > maxit: return 'TIMEOUT', it
        mod = S.get_model()
        edges = [e for e in cand if mod[idx[e] - 1] > 0]
        bad = find_bad_subfamily(edges, n, 7)
        if bad is None: return edges, it
        S.add_clause([-idx[e] for e in set(bad)])
    return None, it

if __name__ == '__main__':
    k, t, n, smax = map(int, sys.argv[1:5])
    lo = max(1, t - (k + 4) // 5)
    stated = min(t, (3 * (2 * t - k - 2)) // 2 + 1)
    sharp = min(t, -((-3 * (2 * t - k - 1)) // 2))
    print(f'k={k} t={t} n={n} lo={lo} stated={stated} sharp={sharp}', flush=True)
    t0 = time.time()
    for s in range(0, smax + 1):
        vecs = venn_vectors(s, n, lo, k)
        found = None; nt = 0
        for key in vecs:
            G, used = build_edges(key)
            res, it = cegar(n, k, t, lo, G)
            if res == 'TIMEOUT': nt += 1; continue
            if res:
                tt = tau_exact(res, n)
                assert find_bad_subfamily(res, n, 7) is None and tt >= t
                found = (key, res, tt); break
        print(f' s={s}: {len(vecs)} Venn quadruples, timeouts={nt}, '
              + ('FOUND family' if found else 'none'), f'({time.time()-t0:.0f}s)', flush=True)
        if found:
            key, res, tt = found
            print('   venn', {P: c for P, c in zip(PATS, key) if c}, 'tau=', tt, '|H|=', len(res))
            print('   edges', [sorted(v for v in range(n) if e >> v & 1) for e in res])
            print('   VIOLATES stated bound' if s < stated else '   consistent with stated bound',
                  '| below sharpened' if s < sharp else '')
            break
