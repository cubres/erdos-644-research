"""Bounded positive-witness discovery; failure is not an infeasibility proof."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np

b = 100
a = 33 * b
lines = [frozenset(t) for t in combinations(range(7), 3)
         if (t[0] + 1) ^ (t[1] + 1) ^ (t[2] + 1) == 0]
types = [(line, line, None, a) for line in lines]
types += [(line | {h}, line, h, b) for line in lines
          for h in sorted(set(range(7)) - line)]
x_line = frozenset((0, 1, 2))
old_masks, weights, labels = [], [], []
for i, (typ, line, extra, weight) in enumerate(types):
    mask = 127 ^ sum(1 << j for j in typ)
    old_masks.append(mask)
    weights.append(weight - int(extra is None and line == x_line))
    labels.append({'type': sorted(typ), 'line': sorted(line), 'extra': extra, 'source': i})
old_masks += [(127 ^ sum(1 << j for j in x_line)) | 1, 0]
weights += [1, b]
labels += [{'x': True}, {'outside': 'Y'}]
n = len(weights)
w = np.array(weights, dtype=np.int64)
old_masks = np.array(old_masks, dtype=np.int64)
pair_weights = w[:, None] * w[None, :]
pair_weights[np.diag_indices(n)] = w * (w - 1)
is_A = [0 not in line for typ, line, extra, weight in types] + [False, False]
A_defects = [i for i, (_, line, extra, _) in enumerate(types) if 0 not in line and extra is not None]
allowed_specs = [(frozenset((0, 1, 2)), 3), (frozenset((0, 3, 4)), 5), (frozenset((0, 5, 6)), 1)]
allowed = [i for i, (_, line, extra, _) in enumerate(types) if (line, extra) in allowed_specs]
assert len(allowed) == 3 and len(A_defects) == 16
p, Q = 111 * b, 3669 * b * b
base_g = np.array(is_A, dtype=bool)
base_g[allowed] = True
base_g[-1] = True
graphs = []
for keep in combinations(range(7), 5):
    mask = sum(1 << j for j in keep)
    adj = ((old_masks[:, None] | old_masks[None, :]) & mask) == mask
    graphs.append((keep, adj))


def potential(adj):
    # Each present cell has positive weight; a self-adjacency can only
    # witness another point when that cell has at least two points.
    aa = adj.copy()
    for i in range(n):
        if weights[i] == 1:
            aa[i, i] = False
    pp = int(w[np.any(aa, axis=1)].sum())
    qq = int(np.sum(pair_weights * adj) // 2)
    return pp, qq


found = []
for count, removed in enumerate(combinations(A_defects, 8), 1):
    g = base_g.copy()
    g[list(removed)] = False
    assert int(w[g].sum()) == 144 * b
    touch = g[:, None] | g[None, :]
    vals = [potential(adj & touch) for _, adj in graphs]
    if all(pp >= p and (pp > p or qq >= Q) for pp, qq in vals):
        found.append({'removed': list(removed), 'selected': [i for i in range(n) if g[i]],
                      'minimum_replacement_endpoint': min(pp for pp, qq in vals),
                      'minimum_replacement_pair_count': min(qq for pp, qq in vals)})
        if len(found) >= 8:
            break
out = {'b': b, 'a': a, 'k': 144*b+1, 'p': p, 'Q': Q,
       'allowed': allowed, 'labels': labels, 'old_masks': old_masks.tolist(),
       'weights': weights, 'tried': count, 'found': found}
Path('outputs/agent_near_fano_first_response_discovery.json').write_text(json.dumps(out, indent=2))
print(json.dumps({'tried': count, 'found': found}, indent=2))
