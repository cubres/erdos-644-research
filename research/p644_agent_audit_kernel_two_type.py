#!/usr/bin/env python3
"""Small exact stress test of the identification-kernel architecture.

Uses the previously certified 42-capacity catalogue; does not replay its proof.
SAT/UNSAT below are discovery outputs. The explicit example is checked with
Fraction arithmetic. No general bound is asserted by this script.
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASK = Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
sys.path.insert(0, str(TASK / 'work/research_dependencies'))
import z3

rows = json.loads((ROOT / 'logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
ex = dict(zip(('x', 'y', 'd', 'c'), map(Q, ('11/128', '215/128', '0', '1/16'))))
slacks = []
for row in rows:
    vertices = [tuple(map(Q, v)) for v in row['vertices']]
    first = max(a * ex['d'] + b * ex['c'] for a, b in vertices)
    second = max(a * (1-ex['d']) + b * (1-ex['c']) for a, b in vertices)
    slacks.append(max(first-ex['x'], second-ex['y']))
assert min(slacks) == Q(1, 128)
assert ex['x'] > ex['c'] and ex['y'] > 1 and ex['x'] < 2*ex['c']
tau = ex['x'] + ex['y'] - 1 - ex['c']
assert tau == Q(45, 64) > Q(2, 3)

x, y, d, c = z3.Reals('x y d c')
R = z3.RealVal
t = x+y-1+d-c
base = [x > c, y > 1-d, d >= 0, d < c, c <= 1]
for row in rows:
    base.append(z3.Or(*[
        q for a, b in row['vertices'] for q in
        (R(a)*d+R(b)*c > x, R(a)*(1-d)+R(b)*(1-c) > y)
    ]))
branches = {
    'interior': [d > 0, c < 1, t < x-d, t < y-1+c],
    'd0': [d == 0, c < 1, t < y-1+c],
    'c1': [d > 0, c == 1, t < x-d],
    'both': [d == 0, c == 1],
}
results = {'example': {k: str(v) for k, v in ex.items()},
           'example_tau': str(tau), 'example_minimum_exclusion_slack': str(min(slacks)),
           'queries': {}}
for name, extra in branches.items():
    for claim, condition in [
        ('above_two_thirds', t > R('2/3')),
        ('violates_stability_above_two_thirds', z3.And(t > R('2/3'), t+(c-d)/2 > R('3/4'))),
    ]:
        solver = z3.Solver()
        solver.set(timeout=60000)
        solver.add(*(base + extra + [condition]))
        answer = solver.check()
        entry = {'result': str(answer)}
        if answer == z3.sat:
            model = solver.model()
            entry['model'] = {str(v): str(model.eval(v)) for v in (x, y, d, c, t)}
        results['queries'][name + ':' + claim] = entry
print(json.dumps(results, indent=2))
