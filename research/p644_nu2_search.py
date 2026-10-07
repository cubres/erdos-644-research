"""ν=2, budget T = 12 (r = 16): CEGAR-style beam search for a prover script.

State = script prefix (edges 1 = A1, 2 = A2 disjoint; 3.. = requests).  A request avoids two picks
P1 ⊆ host1 (⊆ A1-classes), P2 ⊆ host2 (⊆ A2-classes) with |P1| + |P2| = T, optionally plus the
outside parts (X-classes) of earlier edges.  Classes = atoms grouped by (side, membership pattern
in the placed request edges).  Candidates are generated from the adversary's surviving
configuration: the (class, class) combinations carrying the most "covering pair" mass.
"""
import sys, time, itertools, json, random
import p644_strategy2 as S2
from p644_strategy import Aff, mass, Script, inpick, both, notin, contains
from p644_nu2_tree import R, T, A12

def side_of(E):
    return 1 if 1 in E else (2 if 2 in E else 0)

def cls_pred(side, S, placed):
    """atoms on `side` whose membership among placed request edges equals S (frozenset)."""
    S = frozenset(S); pl = frozenset(placed)
    if side == 0:
        return lambda E, L, p: (1 not in E) and (2 not in E) and ((E & pl) == S)
    return lambda E, L, p: (side in E) and ((E & pl) == S)

def union_pred(preds):
    return lambda E, L, p: any(q(E, L, p) for q in preds)

def xprev_pred(placed):
    pl = frozenset(placed)
    return lambda E, L, p: (1 not in E) and (2 not in E) and bool(E & pl)

def make_script(steps, J):
    return Script(J, R, T, steps, intersecting=False, hyps=[(A12, 0, 0, (1, 2))])

def surviving(out, J):
    """Mass of covering pairs of the placed family: pairs of atoms (u,v) with E_u ∪ E_v ⊇ [J]
    (J <= 7), or min over 7-subsets F ⊆ [J] of the pair mass covering F.  Also returns the
    aggregated (class_u, class_v) table for the minimising F."""
    atoms = [(frozenset(E), frozenset(L), m) for (E, L), m in out['atoms'].items()]
    fams = [frozenset(range(1, J + 1))] if J <= 7 else [frozenset(F) for F in itertools.combinations(range(1, J + 1), 7)]
    best = None
    for F in fams:
        tot = 0.0; table = {}
        for i, (Eu, Lu, mu) in enumerate(atoms):
            for (Ev, Lv, mv) in atoms[i:]:
                if (Eu | Ev) >= F:
                    w = mu * mv; tot += w
                    key = ((side_of(Eu), Eu - {1, 2}), (side_of(Ev), Ev - {1, 2}))
                    table[key] = table.get(key, 0.0) + w
        if best is None or tot < best[0]: best = (tot, F, table)
    return best

def candidates(prefix_steps, J, table, placed, k=6):
    """Requests targeting the heaviest surviving (class, class) combos."""
    cands = []
    seen = set()
    items = sorted(table.items(), key=lambda kv: -kv[1])[:k]
    for ((s_u, S_u), (s_v, S_v)), w in items:
        hosts1 = []; hosts2 = []; hostsX = []
        for (s, S) in ((s_u, S_u), (s_v, S_v)):
            if s == 1: hosts1.append(S)
            elif s == 2: hosts2.append(S)
            else: hostsX.append(S)
        # request shapes: (host1 union, host2 union) with sizes (sig, T - sig); if a side is missing use "all"
        h1 = union_pred([cls_pred(1, S, placed) for S in hosts1]) if hosts1 else (lambda E, L, p: 1 in E)
        h2 = union_pred([cls_pred(2, S, placed) for S in hosts2]) if hosts2 else (lambda E, L, p: 2 in E)
        for sig in (4, 6, 8):
            for avoidX in (False, True):
                key = (tuple(sorted(map(tuple, hosts1))), tuple(sorted(map(tuple, hosts2))), sig, avoidX)
                if key in seen: continue
                seen.add(key)
                cands.append((key, h1, h2, sig, avoidX, hostsX))
    return cands

def extend(steps, J, h1, h2, sig, avoidX, hostsX, placed):
    j = J + 1
    st = dict(steps)
    picks = [(f'P{j}a', h1, sig), (f'P{j}b', h2, T - sig)]
    avoid = [f'P{j}a', f'P{j}b']
    if avoidX: avoid.append(xprev_pred(placed))
    for S in hostsX: avoid.append(cls_pred(0, S, placed))
    st[j] = {'picks': picks, 'avoid': avoid}
    return st, j

def search(beam=4, maxJ=9, tl=600, log=None, seed=0):
    random.seed(seed)
    root = ({}, 2)
    out = S2.solve(make_script(*root), time_limit=tl, want=True, continuous=True)
    frontier = [(0.0, root, out)]
    t0 = time.time()
    for depth in range(3, maxJ + 1):
        nxt = []
        for score, (steps, J), out in frontier:
            placed = [e for e in range(3, J + 1)]
            tot, F, table = surviving(out, J) if J >= 3 else (256.0, None, {((1, frozenset()), (2, frozenset())): 256.0})
            cands = candidates(steps, J, table, placed)
            for key, h1, h2, sig, avoidX, hostsX in cands:
                st, j = extend(steps, J, h1, h2, sig, avoidX, hostsX, placed)
                sc = make_script(st, j)
                o = S2.solve(sc, time_limit=tl, want=True, continuous=True)
                if o['status'].startswith('PROVER'):
                    rep = S2.check_budget(sc, time_limit=tl, continuous=True)
                    legal = all(v is None or v <= T + 1e-6 for v in rep.values())
                    msg = json.dumps({'WIN': True, 'J': j, 'legal': legal, 'budget': rep, 'path': [str(k) for k in st_keys(st)]})
                    print(msg, flush=True)
                    if log: log.write(msg + '\n'); log.flush()
                    if legal: return st, j
                    continue
                if not o['status'].startswith('ADVERSARY'): continue
                s_tot, _, _ = surviving(o, j)
                nxt.append((s_tot, (st, j), o))
                line = f"  depth {j} cand {key}: surviving {s_tot:.2f} [{time.time()-t0:.0f}s]"
                if log: log.write(line + '\n'); log.flush()
        nxt.sort(key=lambda t: t[0])
        frontier = nxt[:beam]
        summary = f"depth {depth}: {len(nxt)} candidates, best surviving {[round(t[0], 2) for t in frontier]} [{time.time()-t0:.0f}s]"
        print(summary, flush=True)
        if log: log.write(summary + '\n'); log.flush()
        if not frontier: break
    return None

def st_keys(st):
    out = []
    for j in sorted(st):
        out.append((j, [(n, s if not isinstance(s, Aff) else 'aff') for (n, h, s) in st[j].get('picks', [])], len(st[j].get('avoid', []))))
    return out

if __name__ == '__main__':
    beam = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    maxJ = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    with open('logs/nu2_search.log', 'a') as lg:
        res = search(beam=beam, maxJ=maxJ, log=lg)
        print('RESULT:', 'found' if res else 'none', flush=True)
