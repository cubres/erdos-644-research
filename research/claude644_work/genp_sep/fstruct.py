"""canonical point-structure of the Fano templates branched in a certificate (by multiplicity pattern)."""
import sys, gzip, json, collections, itertools
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
LS = [set(l) for l in LINES]
fh = gzip.open(sys.argv[1], 'rt'); fh.readline()
nodes = {}
for line in fh:
    path, cert = json.loads(line)
    for k, (nm, ai) in enumerate(path): nodes[tuple(map(tuple, path[:k]))] = nm
cnt = collections.Counter(n for n in nodes.values() if n.startswith('F '))
def desc(labs):
    pos = collections.defaultdict(set)
    for q, l in enumerate(labs): pos[l].add(q)
    order = sorted(pos, key=lambda l: (-len(pos[l]), l))
    name = {l: 'ABCDEFG'[k] for k, l in enumerate(order)}
    A = pos[order[0]]
    out = []
    if len(A) == 4:                       # quadrangle: complementary line
        ell = set(range(7)) - A
        out.append('A=quad; line{%s}' % ''.join(sorted(name[labs[q]] for q in ell)))
    elif len(A) == 3:
        if any(A == L for L in LS):
            out.append('A=line; rest{%s}' % ''.join(sorted(name[labs[q]] for q in set(range(7)) - A)))
        else:
            ell = [L for L in LS if not (L & A)][0]; q7 = (set(range(7)) - A - ell).pop()
            out.append('A=triangle; opp.line{%s}; 7th %s' % (''.join(sorted(name[labs[q]] for q in ell)), name[labs[q7]]))
    else:
        # all classes <= 2 points: list the lines spanned by each pair
        ks = [l for l in order if len(pos[l]) == 2]
        thirds = []
        for l in ks:
            a, b = sorted(pos[l]); L = next(L for L in LS if a in L and b in L); c = (L - {a, b}).pop()
            thirds.append('%s%s' % (name[l], name[labs[c]]))
        out.append('pairs; third-points ' + ','.join(thirds))
    return out[0]
agg = collections.Counter()
for nm, n in cnt.items():
    labs = nm[2:].split(','); m = tuple(sorted(collections.Counter(labs).values(), reverse=True))
    agg[(m, desc(labs))] += n
for (m, d), n in sorted(agg.items(), key=lambda t: -t[1]): print(n, m, d)
