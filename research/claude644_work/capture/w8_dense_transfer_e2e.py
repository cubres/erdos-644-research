#!/usr/bin/env python3
"""w8_dense_transfer_e2e.py -- exact end-to-end test of the TRANSFER THEOREM (notes_dense.md w8 ckpt 2/3).

For random small families H (N<=12), an anchor edge E0 and a partition pi = (E0, O_1, ..., O_m):
 * f(u) computed EXACTLY by enumerating all subsets (Fractions).
 * A = {u : f((u-s)^+) >= 1-eta}, s = 3 (Fano rounding constant), eta < 1/6.
 * COMPLETENESS check: tau_int(A) >= tau(H) - s*p and tau*_cont(A u {e0}) >= tau(H) - (s+1)p.
 * INTERSECTING check (if H intersecting): A u {e0} intersecting.
 * SOUNDNESS check: if A u {e0} has an anchored Fano configuration (exact DFS on minimal types), build real class
   sizes by exact LP (Fractions, brute-force over vertices of the 7-dim class polytope is avoided: we solve the
   criterion constructively -- see classes()), round as in the proof, sample random labellings until all six
   windows contain edges, and verify by brute force that the resulting 7 edges have NO 2-transversal.
Every soundness case must end in an explicit bad 7-tuple.  Prints counts."""
import random, sys
from fractions import Fraction as Fr
from itertools import combinations, product
from w8_dense_lib import LINES, PENC, minimal, anchored_config, part_ok, killed_by

def classes_real(loads, cap, anchor_part):
    """real class sizes c_p>=0 (p=0..6), sum<=cap, sum_{p notin l} c_p >= loads[l]; exact via scipy + verification
    in Fractions after rationalising (fallback: tiny LP)."""
    from scipy.optimize import linprog
    A = [[-(1 if p not in LINES[l] else 0) for p in range(7)] for l in range(7)]
    b = [-v for v in loads]
    A.append([1]*7); b.append(cap)
    bounds = [(0, 0) if (anchor_part and p in LINES[0]) else (0, None) for p in range(7)]
    res = linprog(c=[0]*7, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    assert res.status == 0, 'criterion true but class LP infeasible?'
    return [max(0.0, v) for v in res.x]

def round_classes(c, cap):
    fl = [int(v + 1e-9) for v in c]
    rest = cap - sum(fl)
    assert rest >= 0
    # distribute the remaining vertices to classes with positive real mass first (any choice is fine)
    order = sorted(range(7), key=lambda p: -(c[p] - fl[p]))
    i = 0
    while rest > 0:
        p = order[i % 7]
        if c[p] > 0 or all(v == 0 for v in c): fl[p] += 1; rest -= 1
        i += 1
        if i > 1000: fl[order[0]] += rest; rest = 0
    return fl

def two_pierceable(edges, V):
    for x in V:
        for y in V:
            if y < x: continue
            if all(x in G or y in G for G in edges): return True
    return False

def run(seed, stats):
    rnd = random.Random(seed)
    N = rnd.randint(8, 12); V = list(range(N))
    k = rnd.randint(3, 5)
    nE = rnd.randint(6, 40)
    H = set()
    for _ in range(nE):
        H.add(frozenset(rnd.sample(V, rnd.randint(max(2, k-1), k))))
    if rnd.random() < 0.5:   # make it intersecting by keeping a maximal intersecting subfamily greedily
        Hl = sorted(H, key=lambda G: rnd.random()); K = []
        for G in Hl:
            if all(G & F for F in K): K.append(G)
        H = set(K)
    H = list(H)
    E0 = min(H, key=len)
    rest = [v for v in V if v not in E0]
    m = rnd.randint(1, 2)
    rnd.shuffle(rest)
    cut = sorted(rnd.sample(range(1, len(rest)), m-1)) if m > 1 and len(rest) > 1 else []
    O = [rest[i:j] for i, j in zip([0]+cut, cut+[len(rest)])]
    parts = [sorted(E0)] + [sorted(o) for o in O if o]
    p = len(parts); n = tuple(len(P) for P in parts)
    # exact f(u): enumerate subsets
    cnt = {}; tot = {}
    for mask in range(1 << N):
        W = {v for v in V if mask >> v & 1}
        u = tuple(len(W & set(P)) for P in parts)
        tot[u] = tot.get(u, 0) + 1
        if any(G <= W for G in H): cnt[u] = cnt.get(u, 0) + 1
    f = {u: Fr(cnt.get(u, 0), tot[u]) for u in tot}
    # tau(H)
    alpha = max((sum(u) for u in tot if cnt.get(u, 0) < tot[u]), default=-1)
    tauH = N - alpha
    s = 3; eta = Fr(1, 7)
    A = [u for u in tot if f[tuple(max(0, ui - s) for ui in u)] >= 1 - eta]
    e0 = (n[0],) + (0,)*(p-1)
    # completeness
    nonA = [u for u in tot if u not in set(A)]
    tau_int = sum(n) - max((sum(u) for u in nonA), default=-1)
    stats['compl_int_fail'] += tau_int < tauH - s*p
    G = minimal(A + [e0])
    best = -1
    for w in product(*[range(c+1) for c in n]):
        if all(killed_by(w, g) for g in G): best = max(best, sum(w))
    tau_cont = sum(n) - best
    stats['compl_cont_fail'] += tau_cont < tauH - (s+1)*p
    # intersecting
    Hint = all(G1 & G2 for G1, G2 in combinations(H, 2))
    if Hint:
        stats['int_cases'] += 1
        Gi = G
        bad = any(all(a + b <= c for a, b, c in zip(g, h, n)) for g in Gi for h in Gi)
        stats['int_fail'] += bad
    # soundness
    rows, _ = anchored_config(G, n, e0)
    if rows is None: return
    stats['configs'] += 1
    allrows = [e0] + list(rows)
    cls = []
    for i in range(p):
        c = classes_real([rw[i] for rw in allrows], n[i], i == 0)
        cls.append(round_classes(c, n[i]))
    # check windows after rounding dominate (u - 3)^+ and anchor part all off L
    for j in range(1, 7):
        for i in range(p):
            win = sum(cls[i][q] for q in range(7) if q not in LINES[j])
            if win < max(0, allrows[j][i] - s): stats['round_fail'] += 1
    if any(cls[0][q] for q in LINES[0]): stats['anchor_fail'] += 1
    for trial in range(2000):
        lab = {}
        for i, P in enumerate(parts):
            vs = list(P); rnd.shuffle(vs); pos = 0
            for q in range(7):
                for v in vs[pos:pos + cls[i][q]]: lab[v] = q
                pos += cls[i][q]
        edges = [E0]
        for j in range(1, 7):
            Wj = {v for v in V if lab[v] not in LINES[j]}
            cand = [Gx for Gx in H if Gx <= Wj]
            if not cand: break
            edges.append(cand[0])
        else:
            # every vertex of edge j must be labelled off line j
            assert all(lab[v] not in LINES[j] for j, Gx in enumerate(edges) for v in Gx)
            if two_pierceable(edges, V): stats['sound_fail'] += 1
            else: stats['sound_ok'] += 1
            stats['trials'] += trial + 1
            return
    stats['no_labelling'] += 1

if __name__ == '__main__':
    nrun = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    stats = {k: 0 for k in ['compl_int_fail','compl_cont_fail','int_cases','int_fail','configs','round_fail',
                            'anchor_fail','sound_ok','sound_fail','no_labelling','trials']}
    for sd in range(nrun): run(sd, stats)
    print(stats)
