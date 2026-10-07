"""Bounded low-c second-response discovery model, not a proof certificate.

Seed: six pure coordinate rows; row7 avoids the two small cells and has
trace <=1/8+c on each half-sized cell. Row8 is an actual disjoint partner.
Row9 avoids the whole 101 cell and every row7 point outside the old union.
The Q-minimum consequence z>=3c/(1+c) is imposed for c>=.2164.
No claim of completeness for the whole global Q program is made.
"""
import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt')
from p644_strategy2 import Script, build, mass, cellin, contains


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c', type=float, default=.24)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    c = args.c
    base = frozenset(range(1, 7))
    cell_edges = {
        'A': (1, 3, 5), 'B': (1, 4, 6),
        'C': (2, 3, 5), 'D': (2, 3, 6),
        'E': (2, 4, 5), 'F': (2, 4, 6),
    }
    sizes = dict(A=.5, B=.5, C=c, D=.5-c, E=.5-c, F=c)
    predicates = {name: cellin(base, *edges) for name, edges in cell_edges.items()}
    hyps = []
    for subset_size in range(1, 7):
        for subset in itertools.combinations(range(1, 7), subset_size):
            val = next((sizes[name] for name, edges in cell_edges.items()
                        if subset == edges), 0.)
            hyps.append((mass(cellin(base, *subset)), val, val, base))
    for name in ['A', 'B']:
        pred = predicates[name]
        hyps.append((mass(lambda E, L, p, pred=pred: 7 in E and pred(E,L,p)),
                     0, .125+c, frozenset(range(1,8))))
    hyps.append((mass(contains(7,8)), 0, 0, frozenset(range(1,9))))
    hyps.append((mass(lambda E,L,p: 7 in E and bool(E & base)),
                 3*c/(1+c), np.inf, frozenset(range(1,8))))
    outside_g = lambda E,L,p: 7 in E and not (E & base)
    steps = {7: {'avoid': [predicates['C'], predicates['F']]},
             9: {'avoid': [outside_g, predicates['D']]}}
    script = Script(9, 1, .75, steps, intersecting=False, hyps=hyps)
    model = build(script, continuous=True)
    result = milp(model['c'], integrality=model['integrality'],
                  bounds=Bounds(model['lb'], model['ub']),
                  constraints=LinearConstraint(model['A'], model['lbs'], model['ubs']),
                  options={'time_limit': args.seconds})
    out = {'status': result.status, 'message': result.message, 'c': c,
           'scope': 'Discovery only: Q constraints are inspected after solving, not all imposed.',
           'atoms': []}
    if result.x is not None:
        atoms = [(set(E), float(result.x[i])) for i, (E,L) in enumerate(model['atoms'])
                 if result.x[i] > 1e-8]
        out['atoms'] = [{'edges': sorted(E), 'mass': w} for E,w in atoms]
        oldpairs = [{1,2}, {3,4}, {5,6}]
        qs = []
        for retained in itertools.combinations(oldpairs, 2):
            rows = retained[0] | retained[1] | {7,8}
            qs.append(sum(x*y for i,(E,x) in enumerate(atoms)
                          for F,y in atoms[i+1:] if rows <= (E|F)))
        out['three_replacement_Q'] = qs
        out['Q_constraints_hold'] = min(qs) >= c-1e-7
        out['outside_G'] = sum(w for E,w in atoms if 7 in E and not E&base)
    Path(args.output).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='atoms'}, indent=2))


if __name__ == '__main__':
    main()
