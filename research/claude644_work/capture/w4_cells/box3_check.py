"""Independent exact audit (standard library only) of a cells_box3.py UNSAT input.

Re-derives every clause of the CNF from the rational definitions and checks it line by line:
  cells (lattice triangles in [0,hi], homogeneous-Fano drop at lo), covering clauses at hi (cost T),
  unit clauses (pencil 3h<=2lo; QL sum(2h-lo)^+ <= R/4), pair clauses (the 42 audited two-type template
  functions at lo [note checker], GQL(e,e,f,f), mixed pencil (e,e,f)), and all Fano/parent region clauses
  (witness inequalities re-checked exactly at lo; regions recomputed).
The mathematical validity of each clause family is the Robust Box Theorem + Lemma 7.63 request lemmas
(notes_typeclosed.md).  The SAT proof is a separate check (DRAT / LRAT).
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse, json, sys
from p644_continuous_type_cells_check import audited_shapes, partner_boxes, LINES


def recon_cells(R, hi, lo):
    found = {}
    for i, j in product(range(R), repeat=2):
        for verts in (((i, j, R - i - j), (i + 1, j, R - i - j - 1), (i, j + 1, R - i - j - 1)),
                      ((i + 1, j, R - i - j - 1), (i, j + 1, R - i - j - 1), (i + 1, j + 1, R - i - j - 2))):
            if not all(all(0 <= a <= x for a, x in zip(v, hi)) for v in verts): continue
            l = tuple(min(v[h] for v in verts) for h in range(3)); h_ = tuple(max(v[h] for v in verts) for h in range(3))
            if all(7 * a <= 4 * y for a, y in zip(h_, lo)): continue
            found[l] = h_
    return found


def expected(data, shapes):
    R = data['rank']; hi = tuple(data['hi']); lo = tuple(data['lo']); T = data['threshold']
    assert R % 4 == 0 and T == 3 * R // 4 and all(0 < y <= x for x, y in zip(hi, lo))
    nodes = [(tuple(l), tuple(h)) for l, h in data['cells']]; n = len(nodes)
    exp = recon_cells(R, hi, lo)
    assert len(exp) == n and len({l for l, h in nodes}) == n and all(exp[l] == h for l, h in nodes)
    boxes = {u for u in product(*[range(x + 1) for x in hi]) if sum(u) == sum(hi) - T}
    assert boxes == {tuple(u) for u in data['boxes']} and len(boxes) == len(data['boxes'])
    for box in data['boxes']:
        yield [j + 1 for j, (l, h) in enumerate(nodes)
               if all(a <= b for a, b in zip(l, box)) and sum(min(a, b) for a, b in zip(h, box)) >= R]
    unit = []
    for j, (l, h) in enumerate(nodes):
        pen = all(3 * a <= 2 * y for a, y in zip(h, lo))
        ql = sum(max(0, 2 * a - y) for a, y in zip(h, lo)) <= R // 4
        unit.append(pen or ql)
        if unit[-1]: yield [-j - 1]
    for i, (li, hi_i) in enumerate(nodes):
        if unit[i]: continue
        pb = partner_boxes(hi_i, lo, shapes)
        for j in range(i, n):
            if unit[j]: continue
            lj, hj = nodes[j]
            b42 = any(all(a <= b for a, b in zip(hj, box)) for box in pb)
            # 42-template functions are symmetric under the swap (audited_shapes adds both orientations)
            K2 = sum(max(0, 2 * a - y, 2 * b - y) for a, b, y in zip(hi_i, hj, lo))
            K1 = sum(max(0, a + b - y) for a, b, y in zip(hi_i, hj, lo))
            g = K2 <= T and K1 <= R // 4
            m1 = all(2 * a + b <= 2 * y and b <= 2 * c for a, b, c, y in zip(hi_i, hj, li, lo))
            m2 = all(2 * b + a <= 2 * y and a <= 2 * c for a, b, c, y in zip(hi_i, hj, lj, lo))
            if b42 or g or m1 or m2: yield [-i - 1, -j - 1]
    nextvar = n; registry = {}
    for entry in data['fano_clauses']:
        bounds = [tuple(map(Q, b)) for b in entry['bounds']]; asg = entry['assignment']; q = len(bounds)
        assert len(asg) == 7 and set(asg) == set(range(q)) and all(v >= 0 for b in bounds for v in b)
        if entry['kind'] == 'fano':
            for p, cap in enumerate(lo):
                row = [bounds[j][p] for j in asg]
                assert max(row) <= cap and sum(row) <= 4 * cap
                assert all(sum(row[j] for j in line) <= 2 * cap for line in LINES)
        else:
            assert entry['kind'] == 'parents'; parents = entry['parents']
            weights = [list(map(Q, w)) for w in entry['weights']]
            assert all(0 < a < 127 for a in parents) and all(a | b != 127 for a, b in product(parents, repeat=2))
            assert len(weights) == 3
            for p, (w, cap) in enumerate(zip(weights, lo)):
                assert len(w) == len(parents) and min(w) >= 0 and sum(w) <= cap
                for row, j in enumerate(asg):
                    assert sum(v for v, m in zip(w, parents) if m >> row & 1) >= bounds[j][p]
        regions = [[j for j, (_, h) in enumerate(nodes) if all(a <= b for a, b in zip(h, bd))] for bd in bounds]
        assert regions == entry['regions']
        rv = []
        for reg in regions:
            k = tuple(reg)
            if k not in registry:
                nextvar += 1; registry[k] = nextvar
                for cell in reg: yield [-cell - 1, nextvar]
            rv.append(registry[k])
        assert rv == entry['region_variables']; yield [-v for v in rv]


def check(base, templates):
    base = Path(base); data = json.loads(base.with_suffix('.json').read_text())
    shapes = audited_shapes(Path(templates)); assert data['sat'] is False
    with base.with_suffix('.cnf').open() as cnf:
        hdr = cnf.readline().split(); assert hdr[:2] == ['p', 'cnf']; nv, nc = map(int, hdr[2:]); cnt = 0
        for e in expected(data, shapes):
            line = list(map(int, cnf.readline().split())); assert line and line[-1] == 0
            assert line[:-1] == e, ('clause mismatch', cnt, line[:10], e[:10])
            assert all(0 < abs(v) <= nv for v in e); cnt += 1
        assert cnt == nc and not cnf.read().strip()
    print('PASS: exact box3 input audit; rank', data['rank'], 'hi', data['hi'], 'lo', data['lo'], ';',
          len(data['cells']), 'triangles;', len(data['boxes']), 'covering;', len(data['fano_clauses']),
          'regions;', cnt, 'clauses')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('base')
    ap.add_argument('--templates', default='logs/astra_two_part_gap_central/templates.json')
    a = ap.parse_args(); check(a.base, a.templates)
