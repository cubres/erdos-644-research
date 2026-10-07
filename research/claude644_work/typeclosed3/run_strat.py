"""Driver: python3 run_strat.py <tags> [eta] [order|-] [byx 0/1] [menu]
tags (roles, in order): m = 3 class minimisers; b = 3 window blockers; e = 'empty part i' requests (3);
v = vertex requests (3); c = corners of the minimisers at their class (3); k = corners of the blockers at their
facet class (3); p = mixed-pencil requests MP(b,c) for all ordered pairs of the roles present so far (n(n-1)).
"""
import sys, json, itertools, time
import numpy as np
from roles3 import *


def build(tags):
    roles = []
    for tg in tags:
        if tg in 'mA': roles += [{'kind': 'min', 'cls': i} for i in range(3)] if tg == 'm' else []
        elif tg in 'bL': roles += [{'kind': 'blk', 'facet': i} for i in range(3)]   # b: H-box, L: Lemma L3 box
        elif tg == 'e': roles += [req_empty(i) for i in range(3)]
        elif tg == 'v': roles += [req_vertex(i) for i in range(3)]
        elif tg == 'c':
            km = [k for k, r in enumerate(roles) if r['kind'] == 'min']
            roles += [req_corner(k, roles[k]['cls']) for k in km]
        elif tg == 'k':
            kb = [k for k, r in enumerate(roles) if r['kind'] == 'blk']
            roles += [req_corner(k, roles[k]['facet']) for k in kb]
        elif tg == 'x':   # lexicographic-box blockers as extremal request answers (order 0,1,2)
            roles += lexbox_roles_at(len(roles), (0, 1, 2))
        elif tg == 'y':   # same, all six orders
            for od in itertools.permutations(range(3)):
                roles += lexbox_roles_at(len(roles), od)
        elif tg == 'w':   # lexicographic box above sigma (Lemma L3 + lex), order 0,1,2
            roles += lexbox_sigma_roles_at(len(roles), (0, 1, 2))
        elif tg == 'z':   # same, all six orders
            for od in itertools.permutations(range(3)):
                roles += lexbox_sigma_roles_at(len(roles), od)
        elif tg == 'h':   # half-box lexicographic blockers: for each part i (tiny candidate) and order (j,k) of the others:
            # b = argmin c_j over {c_i <= x_i/2, c_k <= 4x_k/7};  a = argmin c_k over {c_i <= x_i/2, c_j <= b_j}
            for i in range(3):
                for j, k in itertools.permutations([l for l in range(3) if l != i]):
                    kb = len(roles)
                    ub = [None] * 3; ub[i] = [{'x%d' % i: 0.5}]; ub[j] = [{'x%d' % j: 1}]; ub[k] = [{'x%d' % k: 4 / 7}]
                    rb = xreq(ub, [j], tag='half%d_%d%d_b' % (i, j, k))
                    rb['extra'] = [({R(kb, j): 1, 'x%d' % j: -4 / 7, 'q%d' % kb: M}, M, None)]
                    ua = [None] * 3; ua[i] = [{'x%d' % i: 0.5}]; ua[j] = [{R(kb, j): 1, 'q%d' % kb: -M, 'c': M}]; ua[k] = [{'x%d' % k: 1}]
                    ra = xreq(ua, [k], tag='half%d_%d%d_a' % (i, j, k))
                    ra['extra'] = [({R(kb + 1, k): 1, 'x%d' % k: -4 / 7, 'q%d' % (kb + 1): M}, M, None)]
                    roles += [rb, ra]
        elif tg == 'p':   # MP requests (incl. pencils a == b) among the first 6 roles
            n = min(6, len(roles))
            roles += [req_mp(a, b) for a in range(n) for b in range(n)]
        else: raise ValueError(tg)
    return roles


if __name__ == '__main__':
    name = sys.argv[1]
    eta = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-2
    order = None
    if len(sys.argv) > 3 and sys.argv[3] != '-':
        order = tuple(int(c) for c in sys.argv[3])
    byx = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
    menu = tuple(sys.argv[5].split(',')) if len(sys.argv) > 5 and sys.argv[5] != '-' else ('F', 'V', 'TT', 'K4', 'T3')
    xmin = float(sys.argv[6]) if len(sys.argv) > 6 else 0.02
    roles = build(name)
    print('roles', len(roles), 'xmin', xmin, flush=True)
    A = Adv(roles, eta=eta, order=order, byx=byx, tmpl=menu, box=('sigma' if 'L' in name else True), xmin=xmin,
            caseA=('A' in name))
    name = name.replace('A', 'a')
    tl = int(sys.argv[7]) if len(sys.argv) > 7 else 600
    if len(sys.argv) > 8:
        A.eta2 = float(sys.argv[8]); print('eta2', A.eta2)
    st, sol = A.run(tl=tl)
    print(name, eta, order, byx, menu, st)
    if sol:
        print(json.dumps(sol))
        fn = 'adv_%s_%s_%s_%d%s%s.json' % (name, eta, ''.join(map(str, order)) if order else 'any', int(byx), '' if xmin == 0.02 else '_x%g' % xmin, '' if A.eta2 == 1e-4 else '_s%g' % A.eta2)
        json.dump(sol, open(fn, 'w'))
        print('saved', fn)
