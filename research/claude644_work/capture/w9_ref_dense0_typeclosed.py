#!/usr/bin/env python3
"""Referee w9 [dense#0]: soundness/rounding of the Transfer Theorem at larger scale (type-closed H, f in {0,1}).

H = all sets whose profile w.r.t. pi equals an admissible type g in G (plus optionally an anchor E0 = union of the
first parts, anchor type e0).  Then f(u)=1 iff u >= some g, and A^{(s)} = {u : (u-s)^+ >= some g}.
Random bad supports (Fano cells, or random pairwise-non-covering cells), <= s+1 cells per part, random rational
masses; premise: every row's floor(window) lies in A (anchored row: E0-parts full).  Then the claim's rounding
(floor + distribute deficit inside the support) must give windows >= (u-s)^+ (=> contains an edge), anchored row
window contains E0; a random labelling realises explicit edges which must NOT be 2-pierceable (brute force).
Mutation: s+2 cells per part -> count rounding violations (sensitivity of the s bound).
usage: python3 w9_ref_dense0_typeclosed.py SEED TRIALS
"""
import sys, random
from fractions import Fraction as Fr

FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
FCELL = [frozenset(j for j,l in enumerate(FANO) if p not in l) for p in range(7)]
FULL = frozenset(range(7))

def rand_cells(rng):
    if rng.random() < 0.5:
        return list(FCELL)
    cells = []
    target = rng.randint(4, 16)
    for _ in range(400):
        if len(cells) >= target: break
        C = frozenset(j for j in range(7) if rng.random() < rng.choice([0.45, 0.55, 0.65]))
        if not C or C == FULL or C in cells: continue
        if all((C | D) != FULL for D in cells):
            cells.append(C)
    return cells

def dom(u, g):
    return all(a >= b for a, b in zip(u, g))

def main():
    seed, trials = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = dict(inst=0, prem=0, anch_prem=0, round_fail=0, edge_fail=0, anchor_fail=0, pierce_fail=0,
              mut_prem=0, mut_viol=0)
    for _ in range(trials):
        p = rng.choice([1, 2, 2, 3])
        anchored = rng.random() < 0.5 and p >= 2
        n = [rng.randint(5, 22) for _ in range(p)]
        e0parts = [0] if anchored else []
        G = []
        for _ in range(rng.randint(1, 5)):
            G.append(tuple(rng.randint(0, max(0, x*3//7)) for x in n))
        G = [g for g in G if sum(g) > 0]
        if not G: continue
        e0 = tuple(n[i] if i in e0parts else 0 for i in range(p))
        s = rng.choice([3, 3, 6, 13])
        A = lambda u: any(dom(tuple(max(0, a-s) for a in u), g) for g in G)
        st['inst'] += 1
        parts = []; off = 0
        for x in n:
            parts.append(list(range(off, off+x))); off += x
        N = off
        for _t in range(20):
            mutate = (_t % 5 == 4)
            cells = rand_cells(rng)
            Lrow = rng.randrange(7)
            use_anchor = anchored and cells == list(FCELL)
            percells = []
            for i in range(p):
                allowed = list(range(len(cells)))
                if use_anchor and i in e0parts:
                    allowed = [c for c in allowed if Lrow in cells[c]]
                cap = s + 1 + (1 if mutate else 0)
                k = rng.randint(max(1, min(cap, len(allowed)) - 2), min(cap, len(allowed)))
                percells.append(rng.sample(allowed, k))
            mass = []
            for i in range(p):
                if rng.random() < 0.5 and len(percells[i]) >= 2:
                    # adversarial fractional parts close to 1 (worst case for flooring)
                    q = len(percells[i]); fr = Fr(rng.randint(90, 99), 100)
                    base = (n[i] - q*fr) / q
                    if base < 0:
                        ws = None
                    else:
                        ws = [base + fr]*q  # equal masses, frac part of each ~ fr if base integer-ish
                        b0 = int(base); ws = [Fr(b0) + fr]*(q-1)
                        last = n[i] - sum(ws)
                        if last < 0: ws = None
                        else: ws.append(last)
                    if ws is not None:
                        mass.append({c: ws[j] for j, c in enumerate(percells[i])}); continue
                ws = [Fr(rng.randint(1, 60), rng.randint(1, 9)) for _ in percells[i]]
                tot = sum(ws)
                mass.append({c: ws[j]*n[i]/tot for j, c in enumerate(percells[i])})
            win = [[sum((m for c, m in mass[i].items() if j in cells[c]), Fr(0)) for i in range(p)] for j in range(7)]
            rows = [tuple(int(w) for w in win[j]) for j in range(7)]
            arow = set()
            ok = True
            for j in range(7):
                if A(rows[j]): continue
                if use_anchor and j == Lrow and all(rows[j][i] >= n[i] for i in e0parts):
                    arow.add(j); continue
                ok = False; break
            if not ok: continue
            if mutate: st['mut_prem'] += 1
            else:
                st['prem'] += 1
                if arow: st['anch_prem'] += 1
            mh = []
            for i in range(p):
                d = {c: int(m) for c, m in mass[i].items()}
                cs = list(d)
                for _ in range(n[i] - sum(d.values())):
                    d[rng.choice(cs)] += 1
                mh.append(d)
            hw = [tuple(sum(v for c, v in mh[i].items() if j in cells[c]) for i in range(p)) for j in range(7)]
            viol = any(hw[j][i] < rows[j][i] - s for j in range(7) if j not in arow for i in range(p))
            if mutate:
                st['mut_viol'] += bool(viol); continue
            if viol:
                st['round_fail'] += 1; print('ROUND FAIL', s, rows, hw); continue
            if any(hw[j][i] < n[i] for j in arow for i in e0parts):
                st['anchor_fail'] += 1; print('ANCHOR FAIL'); continue
            # realise with a random labelling (f in {0,1}: any labelling works)
            lab = {}
            for i in range(p):
                pts = parts[i][:]; rng.shuffle(pts); pos = 0
                for c, k in mh[i].items():
                    for v in pts[pos:pos+k]: lab[v] = c
                    pos += k
            edges = []
            for j in range(7):
                W = [v for v in range(N) if j in cells[lab[v]]]
                if j in arow:
                    E = set(v for i in e0parts for v in parts[i])
                    if not E <= set(W):
                        st['anchor_fail'] += 1; E = None
                else:
                    prof = tuple(sum(1 for v in W if v in set(parts[i])) for i in range(p))
                    gs = [g for g in G if dom(prof, g)]
                    if not gs:
                        st['edge_fail'] += 1; print('EDGE FAIL', prof, rows[j], s); E = None
                    else:
                        g = rng.choice(gs); E = set()
                        for i in range(p):
                            Wi = [v for v in W if v in set(parts[i])]
                            E |= set(rng.sample(Wi, g[i]))
                if E is None: break
                edges.append(E)
            if len(edges) < 7: continue
            pierce = any(all((x in E) or (y in E) for E in edges) for x in range(N) for y in range(x, N))
            if pierce:
                st['pierce_fail'] += 1; print('PIERCE FAIL', cells)
    print('seed', seed, st)

if __name__ == '__main__':
    main()
