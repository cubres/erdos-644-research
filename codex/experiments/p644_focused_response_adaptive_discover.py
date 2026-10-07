"""One adaptive second-request discovery against the focused concrete G.

The five-row core is W3,W4,W5,W6,G and has no common point. The support
gates impose no minimum positive mass. Numerical failures are not proofs.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix


def focused_cells():
    cells = []
    lines = [frozenset(t) for t in combinations(range(7), 3)
             if (t[0]+1) ^ (t[1]+1) ^ (t[2]+1) == 0]
    for L in lines:
        types = ([(L, F(37), 'A'+''.join(map(str, L)))] if 0 not in L else
                 [(L, F(33), 'B'+''.join(map(str, L)))] + [
                     (L | {h}, F(1), 'd'+''.join(map(str, L))+str(h))
                     for h in sorted(set(range(7))-L)])
        for omitted, w, name in types:
            old = sum(1 << (r-1) for r in range(1, 7) if r not in omitted)
            pieces = [(w, name.startswith('A'))]
            if name == 'd0564':
                pieces = [(w, True)]
            if name == 'd0563':
                pieces = [(F(1, 2), True), (F(1, 2), False)]
            if name == 'A245':
                pieces = [(F(67, 2), True), (F(7, 2), False)]
            for j, (weight, g) in enumerate(pieces):
                cells.append({'name': name+':'+str(j), 'weight': weight,
                              'mask': old | (int(g) << 6)})
    assert sum(c['weight'] for c in cells if c['mask'] & 64) == 146
    return cells


def main():
    core = [2, 3, 4, 5, 6]
    agg = defaultdict(F)
    for c in focused_cells():
        mask = sum(1 << j for j, r in enumerate(core) if c['mask'] & (1 << r))
        agg[mask] += c['weight']
    assert 31 not in agg
    cw = [(s, w) for s, w in sorted(agg.items()) if any(s | t == 31 for t in agg)]
    n = len(cw); nq = 2*n; nv = 4*nq
    x = lambda i, q: 2*i+q
    z = lambda i, q: nq+2*i+q
    active = lambda i, q: 2*nq+2*i+q
    u = lambda i, q: 3*nq+2*i+q
    lb = np.zeros(nv); ub = np.ones(nv); integrality = np.zeros(nv)
    integrality[nq:3*nq] = 1
    for i, (s, w) in enumerate(cw):
        for q in range(2):
            ub[x(i,q)] = ub[u(i,q)] = float(w)
    rr=[]; cc=[]; vv=[]; lo=[]; hi=[]
    def add(co, low=-np.inf, high=np.inf):
        row = len(lo)
        for k, v in co.items():
            rr.append(row); cc.append(k); vv.append(v)
        lo.append(low); hi.append(high)
    for i, (s, w) in enumerate(cw):
        add({x(i,0):1, x(i,1):1}, float(w), float(w))
        for q in range(2):
            add({x(i,q):1, z(i,q):-float(w)}, high=0)
            add({u(i,q):1, x(i,q):-1, active(i,q):-float(w)}, low=-float(w))
            for j, (t, ww) in enumerate(cw):
                if s | t != 31:
                    continue
                for r in range(2):
                    if q & r == 0:
                        add({active(i,q):1, z(j,r):-1}, low=0)
    add({x(i,1):1 for i in range(n)}, high=109.5)
    objective = np.zeros(nv)
    for i in range(n):
        for q in range(2):
            objective[u(i,q)] = 1
    matrix = coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
    res = milp(objective, integrality=integrality, bounds=Bounds(lb,ub),
               constraints=LinearConstraint(matrix,lo,hi),
               options={'time_limit':20,'mip_rel_gap':1e-9})
    out={'core_zero_based':core,'budget':109.5,'status':int(res.status),
         'message':res.message,'objective':None if res.fun is None else float(res.fun),
         'dual_bound':float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None}
    if res.x is not None:
        out['allocation']=[{'mask':s,'mass':str(w),
                            'outside_D':float(res.x[x(i,0)]),
                            'inside_D':float(res.x[x(i,1)])}
                           for i,(s,w) in enumerate(cw)]
    Path('outputs/agent_focused_response_adaptive_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
