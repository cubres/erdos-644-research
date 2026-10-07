"""summarise a search tree: node kinds, depth, templates used, request vectors"""
import sys, json, collections
D = json.load(open(sys.argv[1])); C = collections.Counter(); depth = [0]; tm = collections.Counter(); reqs = collections.Counter()
def walk(n, d):
    k = n['k']; C[k] += 1; depth[0] = max(depth[0], d)
    if k in ('TMPL', 'FACET'): tm[json.dumps(n['t'])[:60]] += 1
    if k == 'REQ': reqs[json.dumps(n['w'])] += 1
    for kid in n.get('kids', []):
        walk(kid[1] if isinstance(kid, list) else kid, d + 1)
walk(D['tree'], 0)
print('box', D['box'], 'nodes', dict(C), 'depth', depth[0])
print('templates:'); [print('  ', v, k) for k, v in tm.most_common(12)]
print('requests:'); [print('  ', v, k) for k, v in reqs.most_common(12)]
