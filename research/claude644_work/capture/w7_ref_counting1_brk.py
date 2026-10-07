# Referee w7 (BREAK-IT lens), claim counting#1.  Independent of w6_counting_lib and w7_ref_counting1_bf.
# Everything is computed from the literal definitions of note 7.91/7.92 (pairs of distinct points of V,
# rows are indexed occurrences, A_i = Pi(F minus occurrence i) \ Pi, W_i = endpoints of A_i).
# Parts:
#  A. Fano six-row support built from an actual Fano plane (not from the attacker's labels) + all fillers.
#  B. K_13^(11) (tau=3, (7,2)) with the "bowtie" tuple: an actual joint lex minimiser with a common point,
#     no degree-5 vertex, a degree-2 vertex -> formula (iii) is off by 2.  Scaled family K_n^(n-2), n>=13.
#  C. Random small (7,2) families: exhaustive joint minimisers; test literal (ii)/(iii) and corrected forms.
#  D. Random six-tuples (incl. repeated rows, singletons, outside points): literal and corrected forms.
import itertools, random, sys
from math import comb

R = range(6)
FULL = 63

def analyse(n, rows):
    """n points 0..n-1 (= V), rows = list of 6 bitmasks. Returns per-point m, d, e, q and P, Pi, W."""
    m = [sum(1 << i for i in R if not (rows[i] >> v) & 1) for v in range(n)]
    d = [6 - bin(x).count('1') for x in m]
    Pi = set(); A = [set() for _ in R]
    for u, w in itertools.combinations(range(n), 2):
        # direct definition: pair meets row i iff u in row or w in row
        miss = [i for i in R if not ((rows[i] >> u) & 1 or (rows[i] >> w) & 1)]
        if not miss: Pi.add((u, w))
        elif len(miss) == 1: A[miss[0]].add((u, w))
    P = {x for pr in Pi for x in pr}
    W = [{x for pr in A[i] for x in pr} for i in R]
    e = [int(v in P) for v in range(n)]
    q = [sum(v in W[i] for i in R) for v in range(n)]
    return m, d, e, q, P, Pi, W

def check_i(n, m, e, q):
    # (i): e(v) = [exists w!=v, m(v)&m(w)=0]; q(v) = #{i in m(v): exists w!=v, m(v)&m(w) = {i}}
    for v in range(n):
        ee = int(any(m[v] & m[w] == 0 for w in range(n) if w != v))
        qq = sum(1 for i in R if (m[v] >> i) & 1 and any(m[v] & m[w] == (1 << i) for w in range(n) if w != v))
        if ee != e[v] or qq != q[v]: return False
    return True

def formulas(n, m, d):
    """Attacker's (iii) predictions for c on degree-1/2 points (computed only from G4, G3)."""
    G4 = {m[w] for w in range(n) if d[w] == 4}; G3 = {m[w] for w in range(n) if d[w] == 3}
    pred = {}
    for v in range(n):
        sig = FULL ^ m[v]
        if d[v] == 1:
            j = sig.bit_length() - 1
            pred[v] = sum(((1 << i) | (1 << j)) in G4 for i in R if i != j) - 1
        elif d[v] == 2:
            j, l = [i for i in R if (sig >> i) & 1]
            ee = int(sig in G4)
            qq = sum(1 for i in R if i not in (j, l) and (((1 << i) | (1 << j)) in G4 or ((1 << i) | (1 << l)) in G4
                                                          or ((1 << i) | sig) in G3))
            pred[v] = qq + 2 * ee - 2
    return pred

def audit(n, rows):
    m, d, e, q, P, Pi, W = analyse(n, rows)
    c = [q[v] + 2 * e[v] - d[v] for v in range(n)]
    deg5 = any(x == 5 for x in d); deg6 = any(x == 6 for x in d)
    out = {'i': check_i(n, m, e, q)}
    # (ii) degree-5 lemma: sigma(u)=[6]\{i} => F_i u {u} subset P
    ok = True
    for u in range(n):
        if d[u] == 5:
            i = m[u].bit_length() - 1
            if not all(v in P for v in range(n) if (rows[i] >> v) & 1) or u not in P: ok = False
    out['ii_deg5'] = ok
    # "degree-0 vertex lies in W_i only through such a u"
    out['ii_deg0'] = all(q[v] == len({m[w] for w in range(n) if d[w] == 5}) for v in range(n) if d[v] == 0)
    p = len(P); minF = min(bin(r).count('1') for r in rows)
    outside0 = all(c[v] == 0 for v in range(n) if d[v] == 0)
    out['ii_pmin'] = (p > minF) or outside0              # literal clause 1
    out['ii_nodeg5'] = deg5 or outside0                  # literal clause 2 ("more generally")
    out['ii_nodeg5_fixed'] = deg5 or deg6 or outside0    # corrected clause 2
    pred = formulas(n, m, d)
    good = all(pred[v] == c[v] for v in pred)
    out['iii'] = deg5 or good
    out['iii_fixed'] = deg5 or deg6 or good
    return out, (m, d, e, q, c, P, Pi, deg5, deg6)

def fam_tau(n, H):
    for s in range(0, n + 1):
        for T in itertools.combinations(range(n), s):
            b = sum(1 << x for x in T)
            if all(E & b for E in H): return s
def is72(n, H):
    pairs = [(1 << u) | (1 << w) for u, w in itertools.combinations(range(n), 2)]
    for S in itertools.combinations(H, min(7, len(H))):
        if not any(all(E & pb for E in S) for pb in pairs): return False
    return True

def joint_minimisers(n, H):
    best = None; out = []
    for T in itertools.combinations_with_replacement(range(len(H)), 6):
        rows = [H[i] for i in T]
        _, _, _, _, P, Pi, _ = analyse(n, rows)
        key = (len(P), len(Pi))
        if best is None or key < best: best, out = key, [T]
        elif key == best: out.append(T)
    return best, out

if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'ABC'
    if 'A' in part:
        # Fano plane on points 0..6; lines; drop line L0; rows = complements of the other six lines on 7 classes (size 2)
        lines = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
        L0, rest = lines[0], lines[1:]
        cls = {}; n = 0
        for pt in range(7):
            cls[pt] = [n, n + 1]; n += 2
        base_n = n
        rows = [0] * 6
        for i, L in enumerate(rest):
            for pt in range(7):
                if pt not in L:
                    for v in cls[pt]: rows[i] |= 1 << v
        mb, db, eb, qb, *_ = analyse(base_n, rows)
        cb = [qb[v] + 2 * eb[v] - db[v] for v in range(base_n)]
        print('A: pure Fano support degrees/elig/q/c per class:',
              [(pt, db[cls[pt][0]], eb[cls[pt][0]], qb[cls[pt][0]], cb[cls[pt][0]]) for pt in range(7)])
        G4 = sorted({tuple(i + 1 for i in R if (mb[v] >> i) & 1) for v in range(base_n) if db[v] == 4})
        G3 = sorted({tuple(i + 1 for i in R if (mb[v] >> i) & 1) for v in range(base_n) if db[v] == 3})
        print('A: G4 =', G4, ' G3 =', G3)
        # add every degree-1 and degree-2 filler type (one point each) and one outside point
        fillers = {}
        for j in R:
            fillers[('f1', j)] = n; rows[j] |= 1 << n; n += 1
        for j, l in itertools.combinations(R, 2):
            fillers[('f2', j, l)] = n; rows[j] |= 1 << n; rows[l] |= 1 << n; n += 1
        z = n; n += 1
        out, (m, d, e, q, c, P, Pi, deg5, deg6) = audit(n, rows)
        print('A: audit', out, 'deg5', deg5, 'deg6', deg6)
        print('A: Fano classes unchanged by fillers:', all(c[v] == cb[v] for v in range(base_n)))
        match = {frozenset(x - 1 for x in g) for g in G4}
        for key, v in fillers.items():
            tag = ''
            if key[0] == 'f2': tag = 'matching' if frozenset(key[1:]) in match else 'nonmatch'
            print('   filler', key, tag, 'd e q c =', d[v], e[v], q[v], c[v])
        print('   outside z: c =', c[z])
    if 'B' in part:
        # K_n^(n-2): edges = complements of 2-sets.  n>=13 => 6 complements cover <=12 < n points => every
        # six-tuple has a common point => P = V for every tuple; |Pi| = C(n,2) - #distinct complement pairs >= C(n,2)-6.
        for n in (13, 14, 16):
            k = n - 2
            # bowtie complements: c-a1, c-a2, a1-a2, c-b1, c-b2, b1-b2 on points c=0,a1=1,a2=2,b1=3,b2=4
            comps = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)]
            rows = [((1 << n) - 1) ^ ((1 << a) | (1 << b)) for a, b in comps]
            out, (m, d, e, q, c, P, Pi, deg5, deg6) = audit(n, rows)
            key = (len(P), len(Pi)); lower = (n, comb(n, 2) - 6)
            # tau of K_n^(n-2) is 3; (7,2): a pair misses an edge iff it equals its complement pair, so any pair
            # other than the <=7 complements pierces 7 edges (C(n,2) > 7).
            print(f'B: K_{n}^({k}) tau=3, bowtie tuple key={key}, universal lower bound={lower}, minimiser={key == lower}')
            print('   degrees', d[:5], 'deg5', deg5, 'deg6', deg6, 'audit', out)
            pred = formulas(n, m, d)
            for v in pred: print(f'   point {v}: d={d[v]} e={e[v]} q={q[v]} actual c={c[v]}  formula (iii) c={pred[v]}')
        # sanity on tau and (7,2) for n=13 via brute force over pairs/triples (edges as complements)
        n = 13; H = [((1 << n) - 1) ^ ((1 << a) | (1 << b)) for a, b in itertools.combinations(range(n), 2)]
        t2 = any(all(E & ((1 << u) | (1 << w)) for E in H) for u, w in itertools.combinations(range(n), 2))
        print('B: K_13^11 has a 2-cover?', t2, '; 3-cover {0,1,2} works?', all(E & 7 for E in H))
        rnd = random.Random(5); bad = 0
        for _ in range(20000):
            S = rnd.sample(H, 7)
            if not any(all(E & ((1 << u) | (1 << w)) for E in S) for u, w in itertools.combinations(range(n), 2)): bad += 1
        print('B: random 7-subsets without 2-transversal:', bad)
    if 'C' in part:
        seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        trials = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        rnd = random.Random(seed)
        stats = {}; fams = 0; mins = 0; examples = []
        for tr in range(trials):
            n = rnd.randint(5, 9)
            mode = rnd.random()
            if mode < 0.4:   # 6-wise intersecting flavour: complements of small sets (+ a few extra)
                s = rnd.randint(1, 2)
                H = set()
                for _ in range(rnd.randint(4, 9)):
                    B = rnd.sample(range(n), s); H.add(((1 << n) - 1) ^ sum(1 << b for b in B))
            else:
                H = set()
                for _ in range(rnd.randint(4, 10)):
                    sz = rnd.randint(2, max(2, n - 2)); H.add(sum(1 << b for b in rnd.sample(range(n), sz)))
            H = sorted(H)
            if len(H) > 11 or not is72(n, H): continue
            V = 0
            for E in H: V |= E
            if V != (1 << n) - 1: continue
            t = fam_tau(n, H)
            fams += 1
            best, outs = joint_minimisers(n, H)
            for T in outs:
                rows = [H[i] for i in T]
                out, info = audit(n, rows); mins += 1
                for kk, vv in out.items():
                    stats.setdefault(kk, [0, 0]); stats[kk][0] += 1; stats[kk][1] += (not vv)
                    if not vv and kk in ('ii_nodeg5', 'iii') and t >= 2 and len(examples) < 6:
                        examples.append((kk, t, n, [bin(r) for r in rows], info[1], info[4]))
        print(f'C seed {seed}: families {fams}, joint minimisers audited {mins}')
        for kk, (tot, fail) in stats.items(): print(f'   {kk}: {fail} failures / {tot}')
        for ex in examples: print('   example', ex)
    if 'D' in part:
        seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        rnd = random.Random(seed); stats = {}
        for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 20000):
            n = rnd.randint(2, 11)
            rows = []
            for i in R:
                if i and rnd.random() < 0.15: rows.append(rows[rnd.randrange(i)]); continue
                sz = rnd.randint(1, n); rows.append(sum(1 << b for b in rnd.sample(range(n), sz)))
            if rnd.random() < 0.2:
                x = rnd.randrange(n); rows = [r | (1 << x) for r in rows]
            out, info = audit(n, rows)
            for kk, vv in out.items():
                stats.setdefault(kk, [0, 0]); stats[kk][0] += 1; stats[kk][1] += (not vv)
        print(f'D seed {seed}:')
        for kk, (tot, fail) in stats.items(): print(f'   {kk}: {fail} failures / {tot}')
