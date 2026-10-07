#!/usr/bin/env python3
"""w7_ref_denseTwoPart_E4.py -- brute-force test of the probabilistic PROFILE MODEL (E4) of notes_dense.md ckpt 2.
Small random families H on N vertices, random partitions into p parts.
 f(a) = Pr[uniform W with |W cap P_i| = a_i contains an edge]  (exact Fractions, full enumeration).
 (i) completeness: tau*(A(eta)) = N - max{|u| : f(u) < 1-eta} >= tau(H) for eta in {0,1/10,1/7,1/6,1/2,9/10};
     equality at eta=0.
 (ii) soundness: for every Fano class-profile assignment c_p (p = Fano point, per part) with all 7 row windows
     W_j = union of classes p not on line j having f(W_j) > 6/7, H must fail (7,2) (brute force over <=7 edges).
     Anchored: E0 := an edge that is a union of parts, classes on the anchor line vanish on E0, other 6 windows f>5/6.
Usage: seed trials N"""
import sys, random, itertools
from fractions import Fraction as Fr
from w7_ref_denseTwoPart_lib import LINES, L
seed, trials, N = map(int, sys.argv[1:4]); random.seed(seed)

def tau(H, N):
    for s in range(N + 1):
        for T in itertools.combinations(range(N), s):
            T = set(T)
            if all(T & E for E in H): return s

def has72(H, N):
    Hl = list(H)
    for s in range(1, min(7, len(Hl)) + 1):
        for sub in itertools.combinations(Hl, s):
            ok = False
            for u in range(N):
                for v in range(u, N):
                    if all(u in E or v in E for E in sub): ok = True; break
                if ok: break
            if not ok: return False
    return True

def compositions(n, k):
    if k == 1: yield (n,); return
    for i in range(n + 1):
        for rest in compositions(n - i, k - 1): yield (i,) + rest

stats = dict(H=0, compl_fail=0, eq_fail=0, sound_premise=0, sound_fail=0, anch_premise=0, anch_fail=0)
for _ in range(trials):
    m = random.randint(3, 14)
    H = list({frozenset(random.sample(range(N), random.randint(2, 3 if m > 9 else 4))) for _ in range(m)})
    # remove non-minimal duplicates are harmless
    t = tau(H, N); stats['H'] += 1
    p = random.choice([1, 2, 2, 3])
    perm = list(range(N)); random.shuffle(perm)
    cuts = sorted(random.sample(range(1, N), p - 1)); parts = []; prev = 0
    for c in cuts + [N]: parts.append(perm[prev:c]); prev = c
    # optionally make E0 = an edge a part (anchored test)
    anchored = random.random() < 0.5
    if anchored:
        E0 = random.choice(H); rest = [v for v in range(N) if v not in E0]
        random.shuffle(rest)
        q = random.randint(1, 2) if len(rest) >= 2 else 1
        cuts = sorted(random.sample(range(1, len(rest)), q - 1)) if len(rest) > 1 else []
        parts = [sorted(E0)]; prev = 0
        for c in cuts + [len(rest)]:
            if rest[prev:c]: parts.append(rest[prev:c])
            prev = c
    p = len(parts); sizes = [len(P) for P in parts]
    f = {}
    for prof in itertools.product(*[range(s + 1) for s in sizes]):
        tot = 0; good = 0
        for choice in itertools.product(*[itertools.combinations(parts[i], prof[i]) for i in range(p)]):
            W = set().union(*[set(c) for c in choice]); tot += 1
            if any(E <= W for E in H): good += 1
        f[prof] = Fr(good, tot)
    for eta in (Fr(0), Fr(1, 10), Fr(1, 7), Fr(1, 6), Fr(1, 2), Fr(9, 10)):
        notA = [sum(u) for u, v in f.items() if v < 1 - eta]
        ts = N - (max(notA) if notA else -1) if notA else None
        if ts is not None and ts < t: stats['compl_fail'] += 1; print('COMPLETENESS FAIL', H, parts, eta, ts, t)
        if eta == 0 and ts != t: stats['eq_fail'] += 1; print('EQUALITY FAIL eta=0', H, parts, ts, t)
    is72 = None
    for comp in itertools.product(*[list(compositions(s, 7)) for s in sizes]):
        # comp[i][pt] = size of Fano class pt in part i
        wins = [tuple(sum(comp[i][pt] for pt in range(7) if pt not in LINES[j]) for i in range(p)) for j in range(7)]
        if anchored:
            if any(comp[0][pt] for pt in LINES[L]): continue
            if not all(f[wins[j]] > Fr(5, 6) for j in range(7) if j != L): continue
            stats['anch_premise'] += 1
        else:
            if not all(f[w] > Fr(6, 7) for w in wins): continue
            stats['sound_premise'] += 1
        # the proof's conclusion: some assignment of vertices to classes (with these sizes) makes every window
        # (for anchored: the 6 non-anchor windows; the anchor window contains E0) contain an edge
        found = False
        def rec(i, assign):
            global found
            if found: return
            if i == p:
                cls = {}
                for part_assign in assign:
                    for v, pt in part_assign: cls[v] = pt
                if all(any(E <= {v for v in cls if cls[v] not in LINES[j]} for E in H) for j in range(7)):
                    found = True
                return
            labels = [pt for pt in range(7) for _ in range(comp[i][pt])]
            for perm_l in set(itertools.permutations(labels)):
                rec(i + 1, assign + [list(zip(parts[i], perm_l))])
                if found: return
        rec(0, [])
        if not found:
            stats['assign_fail'] = stats.get('assign_fail', 0) + 1; print('NO GOOD ASSIGNMENT', anchored, H, parts, comp, flush=True)
        if is72 is None and len(H) <= 10: is72 = has72(H, N)
        if is72:
            k = 'anch_fail' if anchored else 'sound_fail'; stats[k] += 1; print('SOUNDNESS FAIL', anchored, H, parts, comp)
        break
print(stats)
