# Referee (claim "exact and end-to-end verification"): EXHAUSTIVE adversary for the adaptive lemmas
# L26 (Lemma 2), L32, L31 at small r, plus static L18 / P0 / P4 with worst-case responses.
# First response H: every feasible vector of trace counts (points inside a cell are interchangeable,
# the prover only uses counts + sorted order).  Later responses: the COMPLEMENT of the request inside
# all points created so far (maximal responses; shrinking edges preserves "no 2-transversal", so this
# dominates every r-sized response).  Outside/fresh points are harmless (missed by E,F,G; every cell
# point is missed by one of E,F,G because E&F&G is empty).
import sys, itertools
import w4_handbound_e2e_lemmas as L
from w4_handbound_e2e import two_transversal

class ExGame:
    def __init__(s, r, T, Hspec):
        s.r = r; s.T = T; s.nxt = 0; s.edges = []; s.Hspec = Hspec; s.calls = 0; s.maxreq = 0
    def fresh(s, k):
        out = list(range(s.nxt, s.nxt + k)); s.nxt += k; return out
    def respond(s, D):
        D = set(D); assert len(D) <= s.T, ('request too big', len(D), s.T)
        s.calls += 1
        if s.calls == 1 and s.Hspec is not None:
            H = s.Hspec(s, D)
            assert len(H) <= s.r and not (H & D)
            return H | set(s.fresh(s.r - len(H)))
        return set(range(s.nxt)) - D

def Hbuilder(parts_counts):
    # parts_counts: function(g,D) -> list of (set_of_candidates, count)
    def f(g, D):
        H = set()
        for cand, k in parts_counts(g, D):
            c = sorted(set(cand) - D - H); assert k <= len(c); H |= set(c[:k])
        return H
    return f

def cellsets(g, x, y, z):
    r = g.r
    X = set(range(0, x)); Y = set(range(x, x + y)); Z = set(range(x + y, x + y + z)); o = x + y + z
    PE = set(range(o, o + r - x - y)); o += r - x - y
    PF = set(range(o, o + r - x - z)); o += r - x - z
    PG = set(range(o, o + r - y - z))
    return X, Y, Z, PE, PF, PG

def enum_H(r, x, y, z, T, name):
    # yield Hspec functions covering all trace-count vectors reachable after the first request
    # we compute the first request by running the prover up to it: emulate using cell structure
    PEn, PFn, PGn = r - x - y, r - x - z, r - y - z
    S = x + y + z
    if name == 'L26':
        # D = X|Y|Z ; H traces a in PF, b in PG, c in PE
        for a in range(PFn + 1):
            for b in range(PGn + 1):
                for c in range(PEn + 1):
                    if a + b + c <= r:
                        yield (a, b, c), (lambda a=a, b=b, c=c: (lambda g, D: _H(g, D, x, y, z, [('PF', a), ('PG', b), ('PE', c)])))
    elif name == 'L32':
        k = T - S
        if k < 0 or k > PFn: return
        for a in range(PFn - k + 1):
            for b in range(PGn + 1):
                for c in range(PEn + 1):
                    if a + b + c <= r:
                        yield (a, b, c), (lambda a=a, b=b, c=c: (lambda g, D: _H(g, D, x, y, z, [('PF', a), ('PG', b), ('PE', c)])))
    elif name == 'L31':
        z0 = min(z, T - x - y)
        if z0 < 0: return
        for q in range(z - z0 + 1):
            for a in range(PFn + 1):
                for b in range(PGn + 1):
                    for c in range(PEn + 1):
                        if q + a + b + c <= r:
                            yield (q, a, b, c), (lambda q=q, a=a, b=b, c=c: (lambda g, D: _H(g, D, x, y, z, [('Z', q), ('PF', a), ('PG', b), ('PE', c)])))

def _H(g, D, x, y, z, spec):
    X, Y, Z, PE, PF, PG = cellsets(g, x, y, z)
    d = {'X': X, 'Y': Y, 'Z': Z, 'PE': PE, 'PF': PF, 'PG': PG}
    H = set()
    for nm, k in spec:
        c = sorted(d[nm] - D); assert k <= len(c), (nm, k, len(c)); H |= set(c[:k])
    return H

def main(rmax):
    stats = {}; branch = {}
    for r in range(4, rmax + 1):
        for x in range(r + 1):
            for y in range(r + 1 - x):
                for z in range(r + 1 - max(x, y)):
                    if x + z > r or y + z > r: continue
                    for name, Tf, run in (('L26', L.T_L26, L.run_L26), ('L32', L.T_L32, L.run_L32), ('L31', L.T_L31, L.run_L31)):
                        T = Tf(r, x, y, z)
                        if T > r or T < 0: continue
                        for key, mk in enum_H(r, x, y, z, T, name):
                            g = ExGame(r, T, mk())
                            try:
                                ed = run(g, x, y, z)
                            except AssertionError as e:
                                print('ASSERT', name, r, x, y, z, T, key, e); stats[name + '_assert'] = stats.get(name + '_assert', 0) + 1; continue
                            assert len(ed) <= 7
                            tt = two_transversal(ed)
                            if tt is not None:
                                print('FAIL', name, r, x, y, z, T, key, tt); stats[name + '_FAIL'] = stats.get(name + '_FAIL', 0) + 1
                            else:
                                stats[name] = stats.get(name, 0) + 1
                            if name == 'L26':
                                a, b, c = key
                                br = 'B small' if b <= T - x else ('A small' if a <= T - y else 'both large')
                                branch[br] = branch.get(br, 0) + 1
                    # static ones: responses all complements
                    T = L.T_P0(r, x, y, z)
                    if T is not None:
                        g = ExGame(r, T, None); ed = L.run_P0(g, x, y, z)
                        if two_transversal(ed) is not None: print('FAIL P0', r, x, y, z, T); stats['P0_FAIL'] = stats.get('P0_FAIL', 0) + 1
                        else: stats['P0'] = stats.get('P0', 0) + 1
                    for T in range(0, r + 1):
                        sp = L.P4_splits(r, x, y, z, T)
                        if sp:
                            g = ExGame(r, T, None); ed = L.run_P4(g, x, y, z, *sp)
                            if two_transversal(ed) is not None: print('FAIL P4', r, x, y, z, T, sp); stats['P4_FAIL'] = stats.get('P4_FAIL', 0) + 1
                            else: stats['P4'] = stats.get('P4', 0) + 1
                            break
                    xs = sorted((x, y, z), reverse=True); M = xs[0]
                    if 2 * M <= r:
                        B = max(L.ceil(L.Fr(3 * r + M, 4)), L.ceil(L.Fr(2 * r + 2 * M, 3)))
                        if B <= r:
                            g = ExGame(r, B, None); ed = L.run_L18(g, *xs)
                            if two_transversal(ed) is not None: print('FAIL L18', r, xs, B); stats['L18_FAIL'] = stats.get('L18_FAIL', 0) + 1
                            else: stats['L18'] = stats.get('L18', 0) + 1
        print('r', r, stats, branch, flush=True)
    print('DONE', stats, branch)

if __name__ == '__main__':
    main(int(sys.argv[1]))
