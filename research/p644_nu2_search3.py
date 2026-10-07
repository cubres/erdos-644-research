"""ν=2 budget 12/16: beam search over WHOLE-CELL requests (unions of current Venn cells), optionally
plus all outside parts of earlier probes.  Heuristic = number of realisable piercing patterns
(maximised by the adversary).  Legality (max avoided mass <= 12) checked by check_budget on wins,
and estimated during the search from the adversary's returned configuration (cells with mass
above `mass_cap` in the returned configuration are not offered)."""
import sys, time, itertools, json
import p644_strategy2 as S2
from p644_strategy import Aff, mass, Script, inpick, both, notin, contains
from p644_nu2_tree import R, T, A12

def cell_pred(side, S, placed):
    S = frozenset(S); pl = frozenset(placed)
    if side == 0: return lambda E, L, p: (1 not in E) and (2 not in E) and ((E & pl) == S)
    return lambda E, L, p: (side in E) and ((E & pl) == S)
def union_pred(preds): return lambda E, L, p: any(q(E, L, p) for q in preds)
def xprev_pred(placed):
    pl = frozenset(placed); return lambda E, L, p: (1 not in E) and (2 not in E) and bool(E & pl)
def make_script(steps, J, nox=False):
    hyps = [(A12, 0, 0, (1, 2))]
    if nox: hyps.append((mass(lambda E, L, p: (1 not in E) and (2 not in E)), 0, 0, ()))
    return Script(J, R, T, steps, intersecting=False, hyps=hyps)

def cells_from(out, placed):
    """Nonempty cells (side, pattern) with masses from the adversary's configuration."""
    acc = {}
    for (E, L), m in out['atoms'].items():
        E = frozenset(E); side = 1 if 1 in E else (2 if 2 in E else 0)
        key = (side, E & frozenset(placed)); acc[key] = acc.get(key, 0.0) + m
    return acc

def menu(out, placed, max_cells=3, mass_cap=12.0):
    cells = cells_from(out, placed)
    items = [(k, m) for k, m in cells.items() if k[0] in (1, 2) and m <= mass_cap]
    reqs = []
    for k in range(1, max_cells + 1):
        for combo in itertools.combinations(items, k):
            tot = sum(m for _, m in combo)
            if tot > mass_cap + 1e-9: continue
            sides = {c[0][0] for c in combo}
            if sides != {1, 2}: continue            # must touch both A1 and A2 (else A1 or A2 answers)
            reqs.append(tuple(c[0] for c in combo))
    return reqs

def extend(steps, J, req, placed, avoidX):
    j = J + 1; st = dict(steps)
    avoid = [union_pred([cell_pred(s, S, placed) for (s, S) in req])]
    if avoidX: avoid.append(xprev_pred(placed))
    st[j] = {'avoid': avoid}
    return st, j

def search(beam=8, maxJ=9, tl=300, nox=False, avoidX=True, log=None, first=(6, 6), max_cells=3):
    t0 = time.time()
    st0 = {3: {'picks': [('S1', contains(1), first[0]), ('S2', contains(2), first[1])], 'avoid': ['S1', 'S2']}}
    o0 = S2.solve(make_script(st0, 3, nox), time_limit=tl, want=True, continuous=True, objective='pierce')
    frontier = [(o0['obj'], (st0, 3), o0, [])]
    for depth in range(4, maxJ + 1):
        nxt = []; tried = 0; seen = set()
        for _, (steps, J), out, path in frontier:
            placed = list(range(3, J + 1))
            for req in menu(out, placed, max_cells=max_cells):
                key = (json.dumps(path), req)
                if key in seen: continue
                seen.add(key)
                st, j = extend(steps, J, req, placed, avoidX); sc = make_script(st, j, nox); tried += 1
                o = S2.solve(sc, time_limit=tl, want=True, continuous=True, objective='pierce')
                desc = path + [[(s, sorted(S)) for (s, S) in req]]
                if o['status'].startswith('PROVER'):
                    rep = S2.check_budget(sc, time_limit=tl, continuous=True)
                    legal = all(v is None or v <= T + 1e-6 for v in rep.values())
                    msg = json.dumps({'WIN': True, 'J': j, 'legal': legal, 'budget': rep, 'path': desc})
                    print(msg, flush=True)
                    if log: log.write(msg + '\n'); log.flush()
                    if legal: return st, j
                    continue
                if not o['status'].startswith('ADVERSARY'): continue
                nxt.append((o['obj'], (st, j), o, desc))
        nxt.sort(key=lambda t: t[0])
        frontier = nxt[:beam]
        summary = f"depth {depth}: tried {tried}, best pierce-counts {[round(t[0], 1) for t in frontier]} [{time.time()-t0:.0f}s]"
        print(summary, flush=True)
        if log:
            log.write(summary + '\n')
            for sc_, _, _, desc in frontier: log.write('   ' + json.dumps(desc) + f' -> {sc_:.1f}\n')
            log.flush()
        if not frontier: break
    return None

if __name__ == '__main__':
    beam = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    maxJ = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    nox = 'nox' in sys.argv[3:]
    with open(f'logs/nu2_search3_{"nox" if nox else "x"}.log', 'a') as lg:
        res = search(beam=beam, maxJ=maxJ, nox=nox, log=lg)
        print('RESULT:', 'found' if res else 'none', flush=True)
