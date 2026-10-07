"""Independent referee checks for paper_0865 Section 7 (GT*, TC*, K4 criterion, spread lemma).
Exact/combinatorial; random end-to-end tests use brute-force 2-transversal checks.
"""
import random, itertools, sys
from itertools import combinations

def has_2transversal(edges, verts):
    verts = list(verts)
    for v in verts:
        if all(v in e for e in edges):
            return True
    for v, w in combinations(verts, 2):
        if all((v in e) or (w in e) for e in edges):
            return True
    return False

def is_fano(points, lines):
    assert len(lines) == 7 and all(len(l) == 3 for l in lines)
    for a, b in combinations(points, 2):
        if sum(1 for l in lines if a in l and b in l) != 1:
            return False
    return True

# ---------------- Lemma 7.1 brute check on the two concrete Fano planes -------------
GT_pts = ['p0', 'a', 'a2', 'b', 'b2', 'c', 'c2']
GT_lines = {'G1': {'p0', 'a', 'a2'}, 'G2': {'p0', 'b', 'b2'}, 'G3': {'p0', 'c', 'c2'},
            'M1': {'a', 'b', 'c'}, 'M2': {'a2', 'b2', 'c'}, 'M3': {'a2', 'b', 'c2'}, 'M4': {'a', 'b2', 'c2'}}
assert is_fano(GT_pts, list(GT_lines.values()))
TC_pts = ['p0', 'p1', 'q', 'r1', 'r2', 'r3', 'r4']
TC_lines = {'L': {'p0', 'p1', 'q'}, 'B1': {'p0', 'r1', 'r2'}, 'B2': {'p0', 'r3', 'r4'},
            'C1': {'p1', 'r1', 'r3'}, 'C2': {'p1', 'r2', 'r4'}, 'M1': {'q', 'r1', 'r4'}, 'M2': {'q', 'r2', 'r3'}}
assert is_fano(TC_pts, list(TC_lines.values()))
print("Fano planes: OK")

# ---------------- GT*: loads with parity choice, exhaustive over sizes ----------------
def gt_split(nA, nB, nC):
    # paper's rule: all odd classes get eps=-1 (a <= a'), etc. Check all eps choices, and paper's specific one
    best = None
    for eA in ([0] if nA % 2 == 0 else [1, -1]):
        for eB in ([0] if nB % 2 == 0 else [1, -1]):
            for eC in ([0] if nC % 2 == 0 else [1, -1]):
                N = nA + nB + nC
                loads = [(N + eA + eB + eC) / 2, (N - eA - eB + eC) / 2, (N - eA + eB - eC) / 2, (N + eA - eB - eC) / 2]
                m = max(loads)
                if best is None or m < best[0]:
                    best = (m, eA, eB, eC)
    return best

for nA in range(0, 30):
    for nB in range(0, 30):
        for nC in range(0, 30):
            N = nA + nB + nC
            m = gt_split(nA, nB, nC)[0]
            assert m <= N // 2 + 1, (nA, nB, nC, m)
            # paper's explicit choice: odd -> -1 always
            eA = -1 if nA % 2 else 0; eB = -1 if nB % 2 else 0; eC = -1 if nC % 2 else 0
            loads = [(N + eA + eB + eC) / 2, (N - eA - eB + eC) / 2, (N - eA + eB - eC) / 2, (N + eA - eB - eC) / 2]
            assert max(loads) <= N // 2 + 1, ('paper choice', nA, nB, nC, loads)
print("GT* load bound (all eps=-1 choice) OK for class sizes < 30")

# ---------------- GT*: random end-to-end ----------------
def gt_e2e(trials, rng):
    fails = 0
    for _ in range(trials):
        n = rng.randint(4, 16)
        V = list(range(n))
        outside = list(range(n, n + rng.randint(0, 5)))
        # random good triple within V, union = V
        while True:
            G = [set(v for v in V if rng.random() < 0.55) for _ in range(3)]
            if all(G) and not (G[0] & G[1] & G[2]):
                break
        U = G[0] | G[1] | G[2]
        A = sorted(U - G[0]); B = sorted(G[0] - G[1]); C = sorted(G[0] & G[1])
        lab = {}
        def split(X, p, p2):
            h = len(X) // 2  # |X_p| = floor, so eps = |X_p|-|X_p2| = -1 if odd
            rng.shuffle(X)
            for x in X[:h]: lab[x] = p
            for x in X[h:]: lab[x] = p2
        split(A, 'a', 'a2'); split(B, 'b', 'b2'); split(C, 'c', 'c2')
        allv = sorted(U) + outside
        for v in outside: lab[v] = 'p0'
        N = len(U)
        edges = [G[0], G[1], G[2]]
        maxload = 0
        for name in ['M1', 'M2', 'M3', 'M4']:
            D = {v for v in U if lab[v] in GT_lines[name]}
            maxload = max(maxload, len(D))
            # adversarial response: random subset of complement of D (nonempty)
            comp = [v for v in allv if v not in D]
            if not comp:
                comp = []
            R = set(v for v in comp if rng.random() < 0.7)
            if not R and comp:
                R = {rng.choice(comp)}
            if not R:
                R = None
            edges.append(R)
        assert maxload <= N // 2 + 1
        if any(e is None for e in edges):
            continue
        if has_2transversal(edges, allv):
            fails += 1
            print("GT* FAIL", G, edges, lab)
    return fails

rng = random.Random(644)
print("GT* e2e fails:", gt_e2e(20000, rng))

# ---------------- TC*: random end-to-end ----------------
def tc_e2e(trials, rng):
    fails = 0; tested = 0
    for _ in range(trials):
        nE = rng.randint(1, 10); nO = rng.randint(0, 10)
        E0 = set(range(nE)); O = list(range(nE, nE + nO)); allv = list(range(nE + nO))
        def rand_edge():
            return set(v for v in allv if rng.random() < 0.5)
        # b1,b2 with b1&b2&E0 empty; c1,c2 likewise; outside arbitrary
        b1 = rand_edge(); b2 = rand_edge(); c1 = rand_edge(); c2 = rand_edge()
        for v in E0:
            if v in b1 and v in b2:
                (b1 if rng.random() < .5 else b2).discard(v)
            if v in c1 and v in c2:
                (c1 if rng.random() < .5 else c2).discard(v)
        if not (b1 and b2 and c1 and c2):
            continue
        DA = set(); DB = set()
        forcedA = E0 & ((b1 & c1) | (b2 & c2)); forcedB = E0 & ((b1 & c2) | (b2 & c1))
        assert not (forcedA & forcedB)
        for v in E0:
            if v in forcedA: DA.add(v)
            elif v in forcedB: DB.add(v)
            else: (DA if rng.random() < .5 else DB).add(v)
        TA = DA | (b1 & c1) | (b2 & c2); TB = DB | (b1 & c2) | (b2 & c1)
        cA = [v for v in allv if v not in TA]; cB = [v for v in allv if v not in TB]
        if not cA or not cB:
            continue
        g1 = set(v for v in cA if rng.random() < .7) or {rng.choice(cA)}
        g2 = set(v for v in cB if rng.random() < .7) or {rng.choice(cB)}
        edges = [E0, b1, b2, c1, c2, g1, g2]
        tested += 1
        if has_2transversal(edges, allv):
            fails += 1
            print("TC* FAIL", edges, DA, DB)
    return fails, tested

print("TC* e2e (fails, tested):", tc_e2e(40000, rng))

# TC* sensitivity: drop the D_A/D_B condition (random partition) -> should find failures
def tc_mut(trials, rng):
    found = 0
    for _ in range(trials):
        nE = rng.randint(2, 8); nO = rng.randint(0, 6)
        E0 = set(range(nE)); allv = list(range(nE + nO))
        re = lambda: set(v for v in allv if rng.random() < 0.5)
        b1, b2, c1, c2 = re(), re(), re(), re()
        for v in E0:
            if v in b1 and v in b2: b2.discard(v)
            if v in c1 and v in c2: c2.discard(v)
        if not (b1 and b2 and c1 and c2): continue
        DA = set(v for v in E0 if rng.random() < .5); DB = E0 - DA
        TA = DA | (b1 & c1) | (b2 & c2); TB = DB | (b1 & c2) | (b2 & c1)
        cA = [v for v in allv if v not in TA]; cB = [v for v in allv if v not in TB]
        if not cA or not cB: continue
        edges = [E0, b1, b2, c1, c2, set(cA), set(cB)]
        if has_2transversal(edges, allv): found += 1
    return found
print("TC* mutation (partition condition dropped) 2-transversal found in", tc_mut(5000, rng), "cases (expected > 0)")

# ---------------- K4 criterion ----------------
K4E = [frozenset(p) for p in combinations(range(4), 2)]
# dictionary: line for G_ab contains r_c, r_d with {c,d} = complement
matchings = [{frozenset({0, 1}), frozenset({2, 3})}, {frozenset({0, 2}), frozenset({1, 3})}, {frozenset({0, 3}), frozenset({1, 2})}]
triangles = [{frozenset(p) for p in combinations([x for x in range(4) if x != a], 2)} for a in range(4)]
# Build explicit Fano with L={s0,s1,s2}, r0..r3: use TC plane: L={p0,p1,q}; r1..r4
rmap = {0: 'r1', 1: 'r2', 2: 'r3', 3: 'r4'}
line_of_pair = {}
for name, l in TC_lines.items():
    if name == 'L': continue
    rs = sorted(k for k, v in rmap.items() if v in l)
    assert len(rs) == 2
    ab = frozenset(set(range(4)) - set(rs))
    line_of_pair[ab] = name
assert len(line_of_pair) == 6
ok = True
for mask in range(64):
    sig = {K4E[i] for i in range(6) if mask >> i & 1}
    # labelable in the actual Fano plane: some point not on any line of sig (L excluded since v not in E0)
    used = set().union(*[TC_lines[line_of_pair[e]] for e in sig]) if sig else set()
    lab_fano = len(used) < 7
    has_tri = any(t <= sig for t in triangles)
    lab_dict = any(not (sig & m) for m in matchings) or any(not (sig & t) for t in triangles)
    if lab_fano != (not has_tri) or lab_fano != lab_dict:
        ok = False; print("K4 mismatch", sig)
print("K4 criterion outside-vertex dictionary (64 types):", "OK" if ok else "FAIL")
# inside E0: v in E_a labelled r_a: lines through r_a other than L carry G with index avoiding a
for a in range(4):
    lines_through = [n for n, l in TC_lines.items() if rmap[a] in l]
    assert 'L' not in lines_through and len(lines_through) == 3
    idx = [ab for ab, n in line_of_pair.items() if n in lines_through]
    assert all(a not in ab for ab in idx) and len(idx) == 3
print("K4 criterion E0-vertex labelling: OK")

# ---------------- Spread lemma: T_A subset D_A u W, T_B subset D_B u W on random instances ----------------
def spread_check(trials, rng):
    bad = 0
    for _ in range(trials):
        nE = rng.randint(4, 12); nO = rng.randint(0, 10)
        allv = list(range(nE + nO)); E0 = set(range(nE))
        part = {v: rng.randrange(4) for v in E0}
        Ei = [set(v for v in E0 if part[v] == i) for i in range(4)]
        out = set(allv) - E0
        rs = lambda S: set(v for v in S if rng.random() < .5)
        b1 = rs(Ei[2] | Ei[3] | out); b2 = rs(Ei[0] | Ei[1] | out)
        c1 = rs(Ei[1] | Ei[3] | out); c2 = rs(Ei[0] | Ei[2] | out)
        DA = Ei[0] | Ei[3]; DB = Ei[1] | Ei[2]
        # TC* hypotheses
        assert not (b1 & b2 & E0) and not (c1 & c2 & E0)
        assert E0 & ((b1 & c1) | (b2 & c2)) <= DA and E0 & ((b1 & c2) | (b2 & c1)) <= DB
        W = ((b1 | b2) & (c1 | c2)) - E0
        TA = DA | (b1 & c1) | (b2 & c2); TB = DB | (b1 & c2) | (b2 & c1)
        if not (TA <= DA | W and TB <= DB | W): bad += 1
    return bad
print("Spread containment failures:", spread_check(20000, rng))

# ---------------- K_9^(5) has (7,2): no 7 four-subsets of [9] cover all pairs ----------------
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
blocks = list(combinations(range(9), 4))
var = {b: i + 1 for i, b in enumerate(blocks)}
cnf = []
for p in combinations(range(9), 2):
    cnf.append([var[b] for b in blocks if p[0] in b and p[1] in b])
card = CardEnc.atmost(lits=list(var.values()), bound=7, top_id=len(blocks), encoding=EncType.seqcounter)
with Minisat22(bootstrap_with=cnf + card.clauses) as s:
    sat7 = s.solve()
card8 = CardEnc.atmost(lits=list(var.values()), bound=8, top_id=len(blocks), encoding=EncType.seqcounter)
with Minisat22(bootstrap_with=cnf + card8.clauses) as s:
    sat8 = s.solve()
print("K_9^(5): 7 complements cover all pairs?", sat7, "(False => (7,2)); 8 suffice?", sat8)
# tau(K_9^(5)) = 9-5+1 = 5; triple
T = [{1, 2, 3, 4, 5}, {1, 2, 6, 7, 8}, {3, 4, 6, 7, 8}]
print("sharpness triple: common =", T[0] & T[1] & T[2], "union size =", len(T[0] | T[1] | T[2]))
