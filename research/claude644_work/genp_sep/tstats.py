"""template statistics of a gen_certp certificate: internal nodes by template, Fano multiplicity patterns."""
import sys, gzip, json, collections
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
fh = gzip.open(sys.argv[1], 'rt'); hdr = json.loads(fh.readline())
nodes = {}
for line in fh:
    path, cert = json.loads(line)
    for k, (nm, ai) in enumerate(path):
        nodes[tuple(map(tuple, path[:k]))] = nm
cnt = collections.Counter(nodes.values())
pat = collections.Counter(); cls = collections.Counter(); struct = collections.Counter()
for nm, n in cnt.items():
    kind, arg = nm.split(' ', 1)
    if kind == 'F':
        labs = arg.split(','); mult = tuple(sorted(collections.Counter(labs).values(), reverse=True))
        pat[('F', mult)] += n; cls[('F', tuple(sorted(set(labs))))] += n
        # structure: for each label, its point set type (is it a line / triangle / etc.)
        sets = {}
        for q, l in enumerate(labs): sets.setdefault(l, set()).add(q)
        desc = []
        for l, S in sorted(sets.items(), key=lambda t: -len(t[1])):
            lines_in = sum(1 for L in LINES if set(L) <= S)
            desc.append('%d%s' % (len(S), 'L' * lines_in))
        struct[('F', '-'.join(desc))] += n
    elif kind == 'R':
        sh, ks, labs = arg.split(':'); labs = labs.split(',')
        mult = tuple(sorted(collections.Counter(labs).values(), reverse=True))
        pat[('R' + sh, mult)] += n; cls[('R', tuple(sorted(set(labs))))] += n
    elif kind in ('W', 'V'):
        a = arg.split(':')[-1].split(','); pat[(kind + (arg.split(':')[0] if kind == 'W' else ''), )] += n
        cls[(kind, tuple(a))] += n
    else:
        pat[(kind,)] += n
print('internal nodes', len(nodes), 'distinct templates', len(cnt))
print('multiplicity patterns:'); [print('  ', k, v) for k, v in pat.most_common(25)]
print('Fano point-set structure (size + one L per full line inside a label class):'); [print('  ', k, v) for k, v in struct.most_common(15)]
print('label sets:'); [print('  ', k, v) for k, v in cls.most_common(20)]
