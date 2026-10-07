#!/usr/bin/env python3
"""Referee w9 [dense#0]: independent exact end-to-end test of the Transfer Theorem (profile models).

For random small families H (N<=10) and random partitions pi:
  * f(u) computed EXACTLY (Fraction) by enumerating all subsets of V.
  * A = A^{(s)}(eta) = {u<=n : f((u-s)^+) >= 1-eta}.
  (i)  completeness: tau_int(A) >= tau - s p ; continuous tau*(A) >= tau - (s+1) p.
  (iii) H intersecting, eta<1/2 => A intersecting (no u,u' in A with u+u'<=n).
  (iv) E0 in H union of parts, H intersecting => no u in A vanishing on the E0 parts.
  (ii) soundness: random bad supports (cells = subsets of [7], pairwise unions != [7]) with <= s+1 cells per part,
       random rational masses; rows u^j = floor(window) must lie in A (or, for the anchored row, = e0 with the
       row's E0-window full).  Then: my own rounding, check window >= (u-s)^+, exact per-row success probability
       f(hat w) >= 1-eta, random labellings until every window has an edge, brute-force check the 7 edges are NOT
       2-pierceable.  Mutation: s+2 cells per part to show the rounding bound is sharp-ish (sensitivity).
usage: python3 w9_ref_dense0_e2e.py SEED NFAM
"""
import sys, random, itertools
from fractions import Fraction as Fr

FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]  # lines on points 0..6
# Fano cell of point p = set of line indices NOT containing p
FCELL = [frozenset(j for j,l in enumerate(FANO) if p not in l) for p in range(7)]
FULL = frozenset(range(7))

def tau_of(N, edges):
    for t in range(N+1):
        for T in itertools.combinations(range(N), t):
            S = set(T)
            if all(S & e for e in edges):
                return t
    return None

def two_pierceable(edges, N):
    for x in range(N):
        for y in range(x, N):
            if all((x in e) or (y in e) for e in edges):
                return True
    return False

def rand_bad_support(rng):
    """random family of cells (subsets of [7]) with pairwise unions != [7] (incl. self)."""
    if rng.random() < 0.5:
        return list(FCELL)
    cells = []
    tries = 0
    while len(cells) < rng.randint(3, 10) and tries < 200:
        tries += 1
        C = frozenset(j for j in range(7) if rng.random() < 0.55)
        if C == FULL or not C:
            continue
        if all((C | D) != FULL for D in cells) and C not in cells:
            cells.append(C)
    return cells

def main():
    seed = int(sys.argv[1]); nfam = int(sys.argv[2])
    rng = random.Random(seed)
    stats = dict(fam=0, compl=0, compl_fail=0, inter=0, inter_fail=0, anch=0, anch_fail=0,
                 sound_prem=0, sound_fail=0, round_fail=0, prob_fail=0, anch_sound=0, mut_prem=0, mut_round_viol=0,
                 realised=0, notfound=0)
    for fi in range(nfam):
        N = rng.randint(7, 12)
        # dense-ish random family so that A is nonempty at small profiles
        mode = rng.random()
        edges = set()
        if mode < 0.3:
            # intersecting & dense: all sets of size 3..4 meeting a fixed 3-set K in >= 2 points
            K = set(rng.sample(range(N), 3))
            for sz in (3, 4):
                for E in itertools.combinations(range(N), sz):
                    if len(K & set(E)) >= 2 and rng.random() < 0.9:
                        edges.add(frozenset(E))
        elif mode < 0.65:
            ksz = rng.choice([2, 2, 2, 3, 3, 4])
            for E in itertools.combinations(range(N), ksz):
                if rng.random() < rng.choice([0.5, 0.8, 0.95, 1.0]):
                    edges.add(frozenset(E))
        else:
            for _ in range(rng.randint(4, 40)):
                edges.add(frozenset(rng.sample(range(N), rng.randint(2, min(5, N-1)))))
        edges = [e for e in edges]
        if not edges:
            continue
        # optionally make intersecting: keep a star-free intersecting subfamily greedily
        if rng.random() < 0.4:
            rng.shuffle(edges)
            keep = []
            for e in edges:
                if all(e & g for g in keep):
                    keep.append(e)
            edges = keep
        H = edges
        stats['fam'] += 1
        tau = tau_of(N, H)
        intersecting = all(a & b for a in H for b in H)
        # partition: optionally E0 as union of parts
        anchored = intersecting and rng.random() < 0.6
        V = list(range(N)); rng.shuffle(V)
        if anchored:
            E0 = rng.choice(H)
            rest = [v for v in V if v not in E0]
            e0l = [v for v in V if v in E0]
            parts = []
            # E0 split into 1 or 2 parts, rest into 1 or 2 parts
            for block in (e0l, rest):
                if not block:
                    continue
                if len(block) >= 2 and rng.random() < 0.4:
                    c = rng.randint(1, len(block)-1)
                    parts += [block[:c], block[c:]]
                else:
                    parts.append(block)
            e0parts = [i for i, P in enumerate(parts) if set(P) <= E0]
        else:
            p = rng.randint(1, 3)
            cuts = sorted(rng.sample(range(1, N), p-1))
            parts = [V[a:b] for a, b in zip([0]+cuts, cuts+[N])]
            e0parts = []
        p = len(parts)
        n = tuple(len(P) for P in parts)
        pid = {}
        for i, P in enumerate(parts):
            for v in P:
                pid[v] = i
        # exact f
        cnt = {}; hit = {}
        for mask in range(1 << N):
            S = frozenset(v for v in range(N) if mask >> v & 1)
            prof = [0]*p
            for v in S:
                prof[pid[v]] += 1
            prof = tuple(prof)
            cnt[prof] = cnt.get(prof, 0) + 1
            if any(e <= S for e in H):
                hit[prof] = hit.get(prof, 0) + 1
        f = {u: Fr(hit.get(u, 0), cnt[u]) for u in cnt}
        eta = rng.choice([Fr(1, 8), Fr(1, 10), Fr(1, 50), Fr(0), Fr(1, 7) - Fr(1, 1000)])
        s = rng.choice([0, 0, 1, 1, 2, 3])
        profs = list(itertools.product(*[range(x+1) for x in n]))
        def sh(u, k=s):
            return tuple(max(0, a-k) for a in u)
        A = set(u for u in profs if f[sh(u)] >= 1 - eta)
        # (i) completeness
        stats['compl'] += 1
        nonA = [u for u in profs if u not in A]
        Ntot = sum(n)
        tau_int = Ntot - max(sum(u) for u in nonA) if nonA else Ntot
        supfree = max(sum(min(a+1, x) for a, x in zip(u, n)) for u in nonA) if nonA else 0
        tau_cont = Ntot - supfree
        if not (tau_int >= tau - s*p and tau_cont >= tau - (s+1)*p and tau_cont <= tau_int):
            stats['compl_fail'] += 1
            print('COMPL FAIL', N, H, parts, s, eta, tau, tau_int, tau_cont)
        # (iii) intersecting
        if intersecting:
            stats['inter'] += 1
            bad = [(u, w) for u in A for w in A if all(a+b <= x for a, b, x in zip(u, w, n))]
            if bad:
                stats['inter_fail'] += 1
                print('INTER FAIL', bad[:2])
        if anchored:
            stats['anch'] += 1
            if any(all(u[i] == 0 for i in e0parts) for u in A):
                stats['anch_fail'] += 1
                print('ANCH FAIL')
        e0 = tuple(n[i] if i in e0parts else 0 for i in range(p))
        # (ii) soundness trials
        for trial in range(60):
            mutate = (trial % 4 == 3)
            cells = rand_bad_support(rng)
            use_anchor = anchored and cells == list(FCELL) and rng.random() < 0.7
            Lrow = rng.randrange(7)
            percells = []
            for i in range(p):
                allowed = list(range(len(cells)))
                if use_anchor and i in e0parts:
                    # only Fano points off line Lrow: their cells contain Lrow
                    allowed = [c for c in allowed if Lrow in cells[c]]
                cap = s + 1 + (1 if mutate else 0)
                k = rng.randint(1, min(cap, len(allowed)))
                percells.append(rng.sample(allowed, k))
            # random rational masses summing to n_i
            mass = []
            for i in range(p):
                ws = [Fr(rng.randint(1, 40), rng.randint(1, 7)) for _ in percells[i]]
                tot = sum(ws)
                mass.append({c: ws[j]*n[i]/tot for j, c in enumerate(percells[i])})
            win = [[sum((m for c, m in mass[i].items() if j in cells[c]), Fr(0)) for i in range(p)] for j in range(7)]
            rows = [tuple(int(w) for w in win[j]) for j in range(7)]  # floor of nonneg Fraction
            anchor_rows = set()
            ok = True
            for j in range(7):
                if rows[j] in A:
                    continue
                if use_anchor and j == Lrow and all(rows[j][i] >= e0[i] for i in e0parts):
                    anchor_rows.add(j)
                    continue
                ok = False; break
            if not ok:
                continue
            if mutate:
                stats['mut_prem'] += 1
            else:
                stats['sound_prem'] += 1
                if anchor_rows:
                    stats['anch_sound'] += 1
            # my rounding: floor + deficit to support cells
            mh = []
            for i in range(p):
                d = {c: int(m) for c, m in mass[i].items()}
                deficit = n[i] - sum(d.values())
                cs = list(d)
                for _ in range(deficit):
                    d[rng.choice(cs)] += 1
                mh.append(d)
            hw = [tuple(sum(v for c, v in mh[i].items() if j in cells[c]) for i in range(p)) for j in range(7)]
            viol = any(hw[j][i] < rows[j][i] - s for j in range(7) for i in range(p) if j not in anchor_rows)
            aviol = any(hw[j][i] < n[i] for j in anchor_rows for i in e0parts)
            if mutate:
                if viol:
                    stats['mut_round_viol'] += 1
                continue
            if viol or aviol:
                stats['round_fail'] += 1
                print('ROUND FAIL', rows, hw, s)
                continue
            if any(f[hw[j]] < 1 - eta for j in range(7) if j not in anchor_rows):
                stats['prob_fail'] += 1
                print('PROB FAIL')
                continue
            # realise: random labellings
            found = False
            for att in range(20000):
                lab = {}
                for i in range(p):
                    pts = list(parts[i]); rng.shuffle(pts)
                    pos = 0
                    for c, k in mh[i].items():
                        for v in pts[pos:pos+k]:
                            lab[v] = c
                        pos += k
                Ws = [frozenset(v for v in range(N) if j in cells[lab[v]]) for j in range(7)]
                G = []
                for j in range(7):
                    cand = [e for e in H if e <= Ws[j]]
                    if not cand:
                        break
                    G.append(cand[0])
                if len(G) == 7:
                    found = True
                    break
            if not found:
                stats['notfound'] += 1
                print('NOT FOUND (union bound says prob >= 1-7eta)', eta)
                continue
            stats['realised'] += 1
            if two_pierceable(G, N):
                stats['sound_fail'] += 1
                print('SOUND FAIL', G)
    print('seed', seed, stats)

if __name__ == '__main__':
    main()
