"""ν=2 budget 12/16: beam search with a structural heuristic (number of realisable piercing patterns,
maximised by the adversary) and an optional NO-X restriction (all probe edges inside A1 ∪ A2)."""
import sys, time, itertools, json
import p644_strategy2 as S2
from p644_strategy import Aff, mass, Script, inpick, both, notin, contains
from p644_nu2_tree import R, T, A12
NOX = (mass(lambda E, L, p: (1 not in E) and (2 not in E)), 0, 0, ())

def cls_pred(side, S, placed):
    S = frozenset(S); pl = frozenset(placed)
    return lambda E, L, p: (side in E) and ((E & pl) == S)
def union_pred(preds): return lambda E, L, p: any(q(E, L, p) for q in preds)
def make_script(steps, J, nox):
    hyps = [(A12, 0, 0, (1, 2))] + ([NOX] if nox else [])
    return Script(J, R, T, steps, intersecting=False, hyps=hyps)

def menu(J):
    """hosts: single classes, pairs of classes, or all; sigma in {4,6,8}."""
    placed = list(range(3, J + 1))
    classes = [frozenset(S) for k in range(len(placed) + 1) for S in itertools.combinations(placed, k)]
    hosts = [(c,) for c in classes] + [(a, b) for a, b in itertools.combinations(classes, 2)] + [tuple(classes)]
    if len(classes) > 8: hosts = [(c,) for c in classes] + [tuple(classes)]   # keep it small at depth
    out = []
    for h1 in hosts:
        for h2 in hosts:
            for sig in (4, 6, 8):
                out.append((h1, h2, sig))
    return out, placed

def extend(steps, J, h1, h2, sig, placed):
    j = J + 1; st = dict(steps)
    p1 = union_pred([cls_pred(1, S, placed) for S in h1]); p2 = union_pred([cls_pred(2, S, placed) for S in h2])
    st[j] = {'picks': [(f'P{j}a', p1, sig), (f'P{j}b', p2, T - sig)], 'avoid': [f'P{j}a', f'P{j}b']}
    return st, j

def search(beam=6, maxJ=9, tl=300, nox=True, log=None, first=(6, 6)):
    t0 = time.time()
    st0 = {3: {'picks': [('S1', contains(1), first[0]), ('S2', contains(2), first[1])], 'avoid': ['S1', 'S2']}}
    frontier = [(None, (st0, 3), [])]
    for depth in range(4, maxJ + 1):
        nxt = []; tried = 0
        for _, (steps, J), path in frontier:
            items, placed = menu(J)
            for (h1, h2, sig) in items:
                st, j = extend(steps, J, h1, h2, sig, placed); sc = make_script(st, j, nox); tried += 1
                o = S2.solve(sc, time_limit=tl, continuous=True, objective='pierce')
                desc = path + [(tuple(sorted(map(tuple, h1))), tuple(sorted(map(tuple, h2))), sig)]
                if o['status'].startswith('PROVER'):
                    rep = S2.check_budget(sc, time_limit=tl, continuous=True)
                    legal = all(v is None or v <= T + 1e-6 for v in rep.values())
                    msg = json.dumps({'WIN': True, 'J': j, 'legal': legal, 'budget': rep, 'nox': nox, 'path': [str(d) for d in desc]})
                    print(msg, flush=True)
                    if log: log.write(msg + '\n'); log.flush()
                    if legal: return st, j
                    continue
                if not o['status'].startswith('ADVERSARY'): continue
                nxt.append((o['obj'], (st, j), desc))
        nxt.sort(key=lambda t: t[0])
        frontier = nxt[:beam]
        summary = f"depth {depth}: tried {tried}, best pierce-counts {[round(t[0], 1) for t in frontier]} [{time.time()-t0:.0f}s]"
        print(summary, flush=True)
        if log: log.write(summary + '\n'); log.flush()
        if log:
            for sc_, (st, j), desc in frontier: log.write('   ' + json.dumps([str(d) for d in desc]) + f' -> {sc_:.1f}\n')
            log.flush()
        if not frontier: break
    return None

if __name__ == '__main__':
    beam = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    maxJ = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    nox = (sys.argv[3] != 'x') if len(sys.argv) > 3 else True
    with open(f'logs/nu2_search2_{"nox" if nox else "x"}.log', 'a') as lg:
        res = search(beam=beam, maxJ=maxJ, nox=nox, log=lg)
        print('RESULT:', 'found' if res else 'none', flush=True)
