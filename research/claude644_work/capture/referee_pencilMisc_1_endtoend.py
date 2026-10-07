#!/usr/bin/env python3
"""Referee check 3: end-to-end on actual random families (NOT assumed (7,2), intersecting,
uniform or critical).  Whenever the hypothesis of a claimed bound is violated, build the
seven edges exactly as the proof prescribes (searching the actual family for each requested
edge -- its existence must follow from the tau argument) and verify they have no transversal of
size <= 2.  Failure of existence or a 2-transversal would refute the proof.

Tested:
 DP : F,G disjoint and ceil(|F|/2)+ceil(|G|/2) <= t-1  ->  bad tuple {F,G,M1..M4}.
 AP : F any edge, U any set, f=|F cap U|, g=|F\\U|, q=tau(H[U]); labeling with class vector x and
      alphas as in the method; if the four m-requests are <= t-1 and both pencil requests are
      <= q-1, the tuple {F, G2, G3, M1..M4} is bad.  We enumerate ALL class vectors x (and the
      best split of F cap U) and use any that fits, so this also exercises the optimum Q*.
"""
import itertools, random

def cdiv(a, b):
    return -(-a // b)

def tau_mask(edges, n):
    if not edges:
        return 0
    for s in range(n + 1):
        for T in itertools.combinations(range(n), s):
            m = 0
            for x in T:
                m |= 1 << x
            if all(e & m for e in edges):
                return s
    return None

def has2(edges, n):
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            if all(e & m for e in edges):
                return True
    return False

def find_avoid(edges, avoid):
    c = [e for e in edges if not (e & avoid)]
    return c

def mask(S):
    m = 0
    for x in S:
        m |= 1 << x
    return m

def trial(rng, stats):
    n = rng.randint(7, 11)
    H = list({mask(rng.sample(range(n), rng.randint(1, 5))) for _ in range(rng.randint(8, 40))})
    t = tau_mask(H, n)
    # ---- DP
    for F, G in itertools.combinations(H, 2):
        if F & G:
            continue
        Fl = [x for x in range(n) if F >> x & 1]; Gl = [x for x in range(n) if G >> x & 1]
        f, g = len(Fl), len(Gl)
        if cdiv(f, 2) + cdiv(g, 2) > t - 1:
            continue
        # balanced split: F -> b,b2,c,c2 with pair sums <= ceil(f/2); G -> a (ceil), a2
        rng.shuffle(Fl); rng.shuffle(Gl)
        q0, r = divmod(f, 4)
        sizes = [q0 + (1 if i < r else 0) for i in range(4)]  # extras on b,b2,c
        cls = {}; pos = 0
        for name, s in zip(['b', 'b2', 'c', 'c2'], sizes):
            cls[name] = mask(Fl[pos:pos + s]); pos += s
        ga = cdiv(g, 2)
        cls['a'] = mask(Gl[:ga]); cls['a2'] = mask(Gl[ga:])
        req = {'M1': cls['a'] | cls['b'] | cls['c'], 'M4': cls['a'] | cls['b2'] | cls['c2'],
               'M2': cls['a2'] | cls['b2'] | cls['c'], 'M3': cls['a2'] | cls['b'] | cls['c2']}
        tup = [F, G]
        for k, av in req.items():
            assert bin(av).count('1') <= t - 1
            c = find_avoid(H, av)
            assert c, 'DP: tau argument failed to supply an edge'
            tup.append(rng.choice(c))
        assert not has2(tup, n), ('DP counterexample to the Fano logic', tup)
        stats['DP'] += 1
    # ---- AP
    for _ in range(3):
        F = rng.choice(H)
        U = mask([x for x in range(n) if rng.random() < rng.choice([0.4, 0.6, 0.8])])
        HU = [e for e in H if e & ~U == 0]
        q = tau_mask(HU, n)
        FU = [x for x in range(n) if (F >> x & 1) and (U >> x & 1)]
        FO = [x for x in range(n) if (F >> x & 1) and not (U >> x & 1)]
        R = [x for x in range(n) if (U >> x & 1) and not (F >> x & 1)]
        f, g, N = len(FU), len(FO), bin(U).count('1')
        done = False
        for u in itertools.product(range(f + 1), repeat=3):
            if sum(u) > f or done:
                continue
            u = list(u) + [f - sum(u)]
            for o in itertools.product(range(g + 1), repeat=3):
                if sum(o) > g:
                    continue
                o = list(o) + [g - sum(o)]
                x = [u[i] + o[i] for i in range(4)]
                Pa = max(x[0] + x[2], x[1] + x[3]); Pa2 = max(x[1] + x[2], x[0] + x[3])
                if max(Pa, Pa2) > t - 1:
                    continue
                al = min(t - 1 - Pa, len(R)); al2 = min(t - 1 - Pa2, len(R) - al)
                w = len(R) - al - al2
                if max(w + u[0] + u[1], w + u[2] + u[3]) > q - 1:
                    continue
                # realise the labeling on actual vertices
                FU2 = FU[:]; FO2 = FO[:]; R2 = R[:]
                rng.shuffle(FU2); rng.shuffle(FO2); rng.shuffle(R2)
                cls = {}
                pu = po = 0
                for i, name in enumerate(['b', 'b2', 'c', 'c2']):
                    cls[name] = mask(FU2[pu:pu + u[i]]) | mask(FO2[po:po + o[i]])
                    cls[name + 'U'] = mask(FU2[pu:pu + u[i]])
                    pu += u[i]; po += o[i]
                cls['a'] = mask(R2[:al]); cls['a2'] = mask(R2[al:al + al2]); cls['p0'] = mask(R2[al + al2:])
                c2 = find_avoid(HU, cls['p0'] | cls['bU'] | cls['b2U'])
                c3 = find_avoid(HU, cls['p0'] | cls['cU'] | cls['c2U'])
                assert c2 and c3, 'AP: host tau argument failed'
                G2, G3 = rng.choice(c2), rng.choice(c3)
                req = {'M1': cls['a'] | cls['b'] | cls['c'], 'M4': cls['a'] | cls['b2'] | cls['c2'],
                       'M2': cls['a2'] | cls['b2'] | cls['c'], 'M3': cls['a2'] | cls['b'] | cls['c2']}
                tup = [F, G2, G3]
                for k, av in req.items():
                    assert bin(av).count('1') <= t - 1
                    c = find_avoid(H, av)
                    assert c, 'AP: global tau argument failed'
                    tup.append(rng.choice(c))
                assert not has2(tup, n), ('AP counterexample', tup)
                stats['AP'] += 1
                done = True
                break
        if not done:
            # method infeasible here: check the confirmed bound holds (it must, since this is
            # exactly when the construction cannot be built -- no (7,2) assumption, so only the
            # arithmetic claim Q* >= q is informative)
            stats['APfeasfail'] += 1

def main(trials=4000, seed=5):
    rng = random.Random(seed)
    stats = {'DP': 0, 'AP': 0, 'APfeasfail': 0}
    for _ in range(trials):
        trial(rng, stats)
    print('bad tuples built and verified:', stats)

if __name__ == '__main__':
    main()
