"""Exact standard-library classification of the Fano capacity dual polytope.

Every vertex has seven independent tight constraints among the fourteen
defining inequalities. All 3432 possible bases are solved over the rationals.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]


def solve(rows, rhs):
    a = [[F(v) for v in row] + [F(b)] for row,b in zip(rows,rhs)]
    for col in range(7):
        pivot = next((j for j in range(col,7) if a[j][col]), None)
        if pivot is None:
            return None
        a[col],a[pivot] = a[pivot],a[col]
        scale = a[col][col]
        a[col] = [v/scale for v in a[col]]
        for j in range(7):
            if j != col and a[j][col]:
                scale = a[j][col]
                a[j] = [u-scale*v for u,v in zip(a[j],a[col])]
    return tuple(row[-1] for row in a)


def check():
    assert all(len(set(a)&set(b)) == 1 for a,b in combinations(LINES,2))
    assert len({tuple(sorted(q)) for line in LINES for q in combinations(line,2)}) == 21
    rows = [tuple(int(j not in line) for j in range(7)) for line in LINES]
    rows += [tuple(-int(i==j) for j in range(7)) for i in range(7)]
    rhs = [1]*7+[0]*7
    vertices = set()
    stats = {'bases':0,'singular':0,'infeasible_bases':0,'feasible_bases':0}
    for inds in combinations(range(14),7):
        stats['bases'] += 1
        point = solve([rows[i] for i in inds],[rhs[i] for i in inds])
        if point is None:
            stats['singular'] += 1
        elif any(sum(a*b for a,b in zip(row,point)) > bound for row,bound in zip(rows,rhs)):
            stats['infeasible_bases'] += 1
        else:
            stats['feasible_bases'] += 1
            vertices.add(point)
    expected = {(F(0),)*7,(F(1,4),)*7}
    expected.update(tuple(F(i==j) for j in range(7)) for i in range(7))
    expected.update(tuple(F(1,2) if j in line else F(0) for j in range(7)) for line in LINES)
    assert stats['bases'] == 3432 and vertices == expected and len(vertices) == 16
    stats['vertices'] = [[str(v) for v in q] for q in sorted(vertices)]
    print('PASS: all 3432 rational bases; exactly 16 Fano dual vertices.', flush=True)
    return stats


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--report')
    args = parser.parse_args()
    result = check()
    if args.report:
        Path(args.report).write_text(json.dumps(result,indent=2))
