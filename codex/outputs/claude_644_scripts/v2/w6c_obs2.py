#!/usr/bin/env python3
"""w6c_obs2.py -- OBS2 (general single-exchange criterion) at the lex (|P|,|Pi|) potential, class-level X.
X is a transversal if replacing F_i by any G avoiding X gives a lex-smaller potential:
  Gamma_i = pairs covering rows != i;  after removal of E(Gamma_i[X]) the remaining graph R has
  (|V(R)|, |E(R)|) < (p, |Pi|) lexicographically.  (Pi' is a subgraph of R, so the new potential is <= that.)
Search over X = union of whole classes (plus optional partial class) -- upper bound on min |X|."""
import itertools
from w6c_static import near_fano
from w6_counting_lib import analyse

def gamma_types(conf, i, r=6):
    full = frozenset(range(r)); tgt = full - {i}
    keys = [s for s in conf if conf[s] > 0]
    E = []
    for a in range(len(keys)):
        for b in range(a, len(keys)):
            s, s2 = keys[a], keys[b]
            if (s | s2) >= tgt:
                if a == b and conf[s] < 2: continue
                E.append((s, s2))
    return keys, E

def remaining(conf, E, xcnt):
    """xcnt: dict type->number of its vertices in X. Returns (|V(R)|, |E(R)|) exactly."""
    nE = 0
    # edges fully inside X
    tot = 0; inside = 0
    for (s, s2) in E:
        if s == s2:
            tot += conf[s] * (conf[s] - 1) // 2; inside += xcnt.get(s, 0) * (xcnt.get(s, 0) - 1) // 2
        else:
            tot += conf[s] * conf[s2]; inside += xcnt.get(s, 0) * xcnt.get(s2, 0)
    # vertices of R: v outside X with a neighbour; v in X with a neighbour outside X
    nbr = {}
    for (s, s2) in E:
        nbr.setdefault(s, set()).add(s2); nbr.setdefault(s2, set()).add(s)
    V = 0
    for s, ns in nbr.items():
        out_s = conf[s] - xcnt.get(s, 0)
        # vertex outside X of type s: has neighbour (any vertex of a neighbour type other than itself)
        if out_s > 0:
            has = any((s2 != s and conf[s2] > 0) or (s2 == s and conf[s] >= 2) for s2 in ns)
            if has: V += out_s
        inx = xcnt.get(s, 0)
        if inx > 0:
            # neighbour outside X
            has = any((conf[s2] - xcnt.get(s2, 0)) > (0 if s2 != s else 0) for s2 in ns if s2 != s) or \
                  (s in ns and conf[s] - xcnt.get(s, 0) > 0)
            if has: V += inx
    return V, tot - inside

def search(conf, i, p, Q, maxcls=None):
    keys, E = gamma_types(conf, i)
    verts = sorted(set([s for e in E for s in e]), key=lambda s: -conf[s])
    best = None
    n = len(verts)
    for m in range(1 << n):
        xc = {verts[j]: conf[verts[j]] for j in range(n) if m >> j & 1}
        size = sum(xc.values())
        if best is not None and size >= best[0]: continue
        V, Ecount = remaining(conf, E, xc)
        if (V, Ecount) < (p, Q):
            best = (size, [''.join(str(z + 1) for z in sorted(s)) for s in xc])
    return best, n

if __name__ == '__main__':
    for (a, b) in [(0, 2), (1, 2), (4, 1)]:
        conf = near_fano(a, b)
        A = analyse({('x', s): c for s, c in conf.items()}, 6)
        print('a=%d b=%d k=%d p=%d Q=%d W=%s' % (a, b, max(A['rows']), A['P'], A['Q'], A['W']))
        for i in range(1):
            best, n = search(conf, i, A['P'], A['Q'])
            print('  row', i, 'classes in Gamma', n, 'best class-union OBS2 transversal', best)
