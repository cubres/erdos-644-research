"""Robust-box cell pipeline for the three-part type-closed theorem (Claude, typeclosed run 4; rebuild of the
lost cells_box2.py).  Based on the note's p644_continuous_type_cells.py.

Rank R (R % 4 == 0), T = 3R/4.  Capacity box  lo <= x <= hi  (integer vectors, units 1/R).
  cells     : lattice triangles of the slice {sum a = R} inside [0,hi]; cells whose maxima h satisfy
              7h <= 4lo (homogeneous Fano at lo) are dropped.
  covering  : for every integer u <= hi with sum(hi-u) = T: OR of cells meeting {a <= u}.
  units     : pencil 3h <= 2lo;  quadrilateral (QL) sum (2h-lo)^+ <= R/4.
  pairs     : 42 two-type templates at lo; GQL(e,e,f,f): sum max(0,2h-lo,2h'-lo) <= T and sum (h+h'-lo)^+ <= R/4;
              mixed pencil (e,e,f): 2h_e+h_f <= 2lo and h_f <= 2 l_e (l = cell minima).
  regions   : Fano / parent multi-type witnesses at lo (note's oracles), region-variable clauses.
UNSAT => for every capacity x in [lo,hi] (units 1/R) every closed type set C with tau*_x(C) > 3/4 has a bad
tuple (Robust Box Theorem, notes_typeclosed.md).  Independent audit: box3_check.py; proof: DRAT.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import argparse, json, time
import numpy as np
from pysat.solvers import Glucose3
from p644_continuous_type_cells import expand_fano_regions


def cells(R, hi, lo):
    out = []
    for deficit in (1, 2):
        for a in range(min(R, hi[0])):
            for b in range(min(R - a, hi[1])):
                c = R - deficit - a - b
                if 0 <= c < hi[2]:
                    l = (a, b, c); h = tuple(v + 1 for v in l)
                    if any(7 * v > 4 * y for v, y in zip(h, lo)):
                        out.append((l, h))
    return out


def run(R, hi, lo, fano=True, regions=True, parents=True, tag=''):
    assert R % 4 == 0 and all(0 < y <= x for x, y in zip(hi, lo))
    T = 3 * R // 4
    root = Path('logs/astra_continuous_type_cells'); root.mkdir(parents=True, exist_ok=True)
    key = 'exp_%d_%s_lo_%s%s' % (R, '_'.join(map(str, hi)), '_'.join(map(str, lo)), tag)
    t0 = time.time(); nodes = cells(R, hi, lo); n = len(nodes)
    L = np.array([l for l, h in nodes], dtype=np.int64).reshape((-1, 3))
    U = np.array([h for l, h in nodes], dtype=np.int64).reshape((-1, 3))
    Y = np.array(lo, dtype=np.int64)
    menu = json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text())
    shapes = [[tuple(map(F, v)) for v in item['record']['vertices']] for item in menu.values()]
    import os
    if os.environ.get('FNSET') is not None: shapes=[shapes[int(i)] for i in os.environ['FNSET'].split(',') if i!='']
    clauses = []; boxes = []
    target = sum(hi) - T
    for a in range(hi[0] + 1):
        for b in range(hi[1] + 1):
            c = target - a - b
            if 0 <= c <= hi[2]:
                box = (a, b, c); boxes.append(box)
                ok = np.all(L <= box, axis=1) & (np.minimum(U, box).sum(axis=1) >= R)
                clauses.append(list(map(int, np.nonzero(ok)[0] + 1)))
    ncover = len(clauses)
    import os
    if os.environ.get('HEAVY3'):
        for p_ in range(3):
            clauses.append([int(i)+1 for i in np.nonzero(7*U[:,p_] > 4*Y[p_])[0]])
    pencil = np.all(3 * U <= 2 * Y, axis=1)
    ql = np.maximum(0, 2 * U - Y).sum(axis=1) <= R // 4
    unit = pencil | ql
    import os
    if os.environ.get('NOUNIT'): unit[:] = False
    for i in np.nonzero(unit)[0]: clauses.append([-int(i) - 1])
    nunit = int(unit.sum())
    bad = np.zeros((n, n), dtype=bool)
    for shape in shapes:
        fits = np.ones((n, n), dtype=bool)
        for u, v in shape:
            den = u.denominator * v.denominator // gcd(u.denominator, v.denominator)
            ai, bi = int(u * den), int(v * den)
            for p in range(3):
                fits &= ai * U[:, p, None] + bi * U[None, :, p] <= den * lo[p]
        bad |= fits
    bad |= bad.T
    n42 = int(np.triu(bad).sum())
    A = np.maximum(0, 2 * U - Y)
    K2 = np.maximum(A[:, None, :], A[None, :, :]).sum(axis=2)
    K1 = np.maximum(0, U[:, None, :] + U[None, :, :] - Y).sum(axis=2)
    gql = (K2 <= T) & (K1 <= R // 4)
    mp = np.all((2 * U[:, None, :] + U[None, :, :] <= 2 * Y) & (U[None, :, :] <= 2 * L[:, None, :]), axis=2)
    import os
    if not os.environ.get('NOGQL'): bad |= gql
    if not os.environ.get('NOMP'): bad |= mp | mp.T
    if os.environ.get('NOUNIT'): unit[:] = False
    npairs = 0
    for i in range(n):
        if unit[i]: continue
        for j in np.nonzero(bad[i, i:])[0] + i:
            if unit[j]: continue
            clauses.append([-i - 1, -int(j) - 1]); npairs += 1
    print('START', key, 'cells', n, 'boxes', len(boxes), 'units', nunit, 'pairs42', n42, 'pairs_total', npairs,
          'sec', round(time.time() - t0, 1), flush=True)
    fano = not os.environ.get('NOREG')
    if fano: from p644_fano_type_assignment import solve as fano_solve
    if parents: from p644_parent_type_assignment import solve as parent_solve, expand_regions as parent_expand
    fano_clauses = []; numvars = n; region_variables = {}; oracle = None; answer = None
    if os.environ.get('LEMMAE'):
        extra=int(os.environ.get('LEMMAE'))       # cost slack in lattice units (6 for unit boxes)
        tgt=sum(hi)-T-extra
        for p_ in range(3):
            light=np.nonzero(7*U[:,p_] <= 4*Y[p_])[0]
            ors=[]
            for a in range(hi[0]+1):
                for b in range(hi[1]+1):
                    c=tgt-a-b
                    if not (0<=c<=hi[2]): continue
                    v=np.array((a,b,c))
                    inside=light[np.all(U[light]<=v,axis=1)]
                    numvars+=1; ors.append(numvars)
                    for i in inside: clauses.append([-numvars,-int(i)-1])
            clauses.append(ors)
        print('LEMMAE aux vars',numvars-n,flush=True)
    with Glucose3(bootstrap_with=clauses) as solver:
        while True:
            answer = solver.solve()
            if not answer: break
            selected = [i - 1 for i in solver.get_model() if 0 < i <= n]
            assert not any(bad[i, j] for i in selected for j in selected)
            if not fano: break
            types = [nodes[i][1] for i in selected]
            w = fano_solve(types, lo, seconds=10)
            if w['status'] != 'EXACT_POSITIVE' and parents: w = parent_solve(types, lo, seconds=3)
            oracle = w['status']
            if oracle != 'EXACT_POSITIVE': break
            labels = [selected[j] for j in w['labels']]
            rec = {'labels': labels, 'kind': 'parents' if 'parents' in w else 'fano'}
            if 'parents' in w: ex = parent_expand(w, nodes, lo, labels)
            else: ex = expand_fano_regions(labels, nodes, lo)
            if ex is None: raise RuntimeError('region expansion failed')
            rec.update(ex); rv = []
            for reg in ex['regions']:
                k = tuple(reg)
                if k not in region_variables:
                    numvars += 1; region_variables[k] = numvars
                    for cell in reg:
                        imp = [-cell - 1, numvars]; clauses.append(imp); solver.add_clause(imp)
                rv.append(region_variables[k])
            rec['region_variables'] = rv; cl = [-v for v in rv]
            fano_clauses.append(rec); clauses.append(cl); solver.add_clause(cl)
            if len(fano_clauses) % 25 == 0:
                print('REGIONS', len(fano_clauses), 'sec', round(time.time() - t0, 1), flush=True)
    if not answer:
        with (root / (key + '.cnf')).open('w') as out:
            out.write('p cnf %d %d\n' % (numvars, len(clauses)))
            for c in clauses: out.write(' '.join(map(str, c)) + ' 0\n')
    rep = {'rank': R, 'hi': list(hi), 'lo': list(lo), 'threshold': T, 'cells': nodes, 'boxes': boxes,
           'ncover': ncover, 'nunit': nunit, 'npairs': npairs, 'sat': bool(answer),
           'selected': [nodes[i] for i in selected] if answer else [], 'fano_clauses': fano_clauses,
           'oracle_status': oracle, 'elapsed': time.time() - t0}
    (root / (key + '.json')).write_text(json.dumps(rep))
    print('FINISHED', 'SAT_RELAXATION' if answer else 'UNSAT_AUDIT_PENDING', 'regions', len(fano_clauses),
          'sec', round(rep['elapsed'], 1), 'key', key, flush=True)
    return rep


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('rank', type=int); ap.add_argument('hi', nargs=3, type=int)
    ap.add_argument('--lo', nargs=3, type=int); ap.add_argument('--tag', default='')
    a = ap.parse_args(); lo = a.lo if a.lo else a.hi
    run(a.rank, tuple(a.hi), tuple(lo), tag=a.tag)
