#!/usr/bin/env python3
"""w4_tcglobal_tcstar_e2e.py -- end-to-end checks on random families (no (7,2) assumed). Exact set arithmetic.
 (a) TC*: E0 in H; b1,b2 with b1nb2nE0 empty; c1,c2 with c1nc2nE0 empty; any split E0 = D_A u D_B with
     E0n((b1nc1)u(b2nc2)) in D_A, E0n((b1nc2)u(b2nc1)) in D_B.  If neither
     T_A = D_A u (b1nc1) u (b2nc2) nor T_B = D_B u (b1nc2) u (b2nc1) is a transversal, pick g1 avoiding T_A,
     g2 avoiding T_B and verify {E0,b1,b2,c1,c2,g1,g2} has no 2-point transversal.
 (b) K4 criterion: quartering + six edges G_Q (trace inside half Q) with no outside vertex in the three edges
     of a triangle (halves missing a common quarter) => the 7 edges have no 2-point transversal.
Usage: python3 w4_tcglobal_tcstar_e2e.py seed trials"""
import itertools, random, sys
def pc(x): return bin(x).count('1')
def two_pierce(edges, n):
    for x in range(n):
        for y in range(x, n):
            m = (1<<x)|(1<<y)
            if all(e & m for e in edges): return True
    return False
def is_transversal(T, H): return all(G & T for G in H)
seed, trials = int(sys.argv[1]), int(sys.argv[2])
random.seed(seed)
cntA = cntB = fails = 0
for tr in range(trials):
    n = random.randint(7, 12)
    H = list(set(sum(1<<v for v in random.sample(range(n), random.randint(2, min(n-1,6)))) for _ in range(random.randint(6, 30))))
    E0 = random.choice(H)
    ev = [v for v in range(n) if E0>>v&1]
    if len(ev) < 2: continue
    others = H
    # (a)
    for _ in range(20):
        b1, b2, c1, c2 = (random.choice(others) for _ in range(4))
        if b1 & b2 & E0 or c1 & c2 & E0: continue
        A_need = E0 & ((b1&c1)|(b2&c2)); B_need = E0 & ((b1&c2)|(b2&c1))
        assert not (A_need & B_need)
        free = [v for v in ev if not ((A_need|B_need)>>v&1)]
        DA = A_need
        for v in free:
            if random.random() < 0.5: DA |= 1<<v
        DB = E0 & ~DA
        TA = DA | (b1&c1) | (b2&c2); TB = DB | (b1&c2) | (b2&c1)
        if is_transversal(TA, H) or is_transversal(TB, H): continue
        g1 = next(G for G in H if not G & TA); g2 = next(G for G in H if not G & TB)
        cntA += 1
        if two_pierce([E0,b1,b2,c1,c2,g1,g2], n): fails += 1; print("TC* FAIL", tr)
    # (b)
    if len(ev) >= 4:
        random.shuffle(ev)
        cuts = sorted(random.sample(range(1, len(ev)), 3))
        Q = [sum(1<<v for v in ev[a:b]) for a,b in zip([0]+cuts, cuts+[len(ev)])]
        halves = {(a,b): Q[a]|Q[b] for a,b in itertools.combinations(range(4),2)}
        cand = {h: [G for G in H if not (G & E0 & ~halves[h])] for h in halves}
        if all(cand[h] for h in halves):
            for _ in range(20):
                pick = {h: random.choice(cand[h]) for h in halves}
                badpt = False
                for T in itertools.combinations(range(4),3):
                    hs = list(itertools.combinations(T,2))
                    if pick[hs[0]] & pick[hs[1]] & pick[hs[2]] & ~E0: badpt = True
                if badpt: continue
                cntB += 1
                if two_pierce([E0]+list(pick.values()), n): fails += 1; print("K4 FAIL", tr)
print("TC* constructions:", cntA, " K4 constructions:", cntB, " failures:", fails)
sys.exit(1 if fails else 0)
