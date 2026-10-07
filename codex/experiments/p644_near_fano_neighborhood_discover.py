"""Numerical discovery only; exact support checking is separate."""
from itertools import combinations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

parser = argparse.ArgumentParser()
parser.add_argument('--margin', type=float, default=0.001)
args = parser.parse_args()

lines = [frozenset(t) for t in combinations(range(7), 3)
         if (t[0] + 1) ^ (t[1] + 1) ^ (t[2] + 1) == 0]
types = [(line, 33) for line in lines]
types += [(line | {h}, 1) for line in lines
          for h in set(range(7)) - line]
masks = [sum(1 << (j - 2) for j in range(2, 7) if j not in typ)
         for typ, _ in types]
weights = np.array([w for _, w in types], dtype=float)
n = len(types)
neighbors = [{j for j, t in enumerate(masks) if s | t == 31}
             for s in masks]
eligible = {i for i in range(n) if neighbors[i]}
p5 = sum(weights[i] for i in eligible)
p = 111
print('p5', p5, 'threshold', p5 - p, flush=True)
rows, lower, upper = [], [], []


def add(row, lo, hi):
    rows.append(row)
    lower.append(lo)
    upper.append(hi)


add({n + i: 1 for i in eligible}, p5 - p + args.margin, np.inf)
for i in range(n):
    add({n + i: 1, i: -weights[i]}, -np.inf, 0)
    add({2 * n + i: 1, n + i: -1}, 0, np.inf)
    for j in neighbors[i]:
        add({2 * n + j: 1, i: -weights[j]}, 0, np.inf)
matrix = lil_matrix((len(rows), 3 * n))
for r, row in enumerate(rows):
    for j, value in row.items():
        matrix[r, j] = value
bounds_upper = np.r_[np.array([int(i in eligible) for i in range(n)]),
                     weights, weights]
result = milp(np.r_[np.zeros(2 * n), np.ones(n)],
              integrality=np.r_[np.ones(n), np.zeros(2 * n)],
              bounds=Bounds(np.zeros(3 * n), bounds_upper),
              constraints=LinearConstraint(matrix.tocsr(), lower, upper),
              options={'time_limit': 30})
print(result.message, 'objective', result.fun, 'gap', result.get('mip_gap'), flush=True)
out = {'message': result.message, 'objective': result.fun,
       'gap': result.get('mip_gap'), 'p5': p5, 'threshold': p5 - p,
       'types': [sorted(t) for t, _ in types], 'weights': weights.tolist()}
if result.x is not None:
    out['selected'] = result.x[n:2*n].tolist()
    out['cover'] = result.x[2*n:].tolist()
    print('selected', [(i, sorted(types[i][0]), v)
                       for i, v in enumerate(out['selected']) if v > 1e-7])
suffix = '_equal' if args.margin == 0 else ''
Path('outputs/agent_near_fano_neighborhood' + suffix + '_discovery.json').write_text(json.dumps(out, indent=2))
