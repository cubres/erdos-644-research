"""TASK 3 sweep: MILP adversary search (bal_adv.GenAdv, case (A)) for a gen_cert-format strategy on a region, then
EXACT re-check of every adversary with gadv_verify.py (strict semantics, full menu, Fano over all assignments).
usage: python3 sweep_milp.py <strategy.json> <tag> [eta=0.01] [beta=1e-3] [etas=1e-3] [tl=1200] [fk=7]
The strategy's 'xbox' / 'order' / 'pairs' restrict the region (as in gen_cert)."""
import sys, json, subprocess, time
import numpy as np
from bal_adv import GenAdv, M


def convert(spec):
    names = [r['name'] for r in spec['roles']]
    idx = {n: k for k, n in enumerate(names)}
    def ren(e):
        out = {}
        for k, v in e.items():
            v = float(eval(str(v))) if isinstance(v, str) and '/' in v else float(v)
            if k.startswith('c') and k != 'c':
                nm, j = k[1:].rsplit('_', 1); out['r%d_%s' % (idx[nm], j)] = v
            else:
                out[k] = v
        return out
    roles = []
    for r in spec['roles']:
        if r['kind'] == 'min': roles.append({'kind': 'min', 'cls': r['cls']})
        elif r['kind'] == 'blk': roles.append({'kind': 'blk', 'facet': r['facet']})
        elif r['kind'] == 'req': roles.append({'kind': 'req', 'u': [[ren(e) for e in r['u'][i]] for i in range(3)]})
    return roles, names


def main():
    spec = json.load(open(sys.argv[1])); tag = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    roles, names = convert(spec)
    extra = []
    if spec.get('order'):
        extra += [({'x1': 1, 'x0': -1}, 0.0, None), ({'x2': 1, 'x1': -1}, 0.0, None)]
    for i, lo, hi in spec.get('xbox', []):
        extra.append(({'x%d' % i: 1}, float(eval(lo)) if lo else None, float(eval(hi)) if hi else None))
    pairs = [[i, j, float(eval(lo)) if lo else None, float(eval(hi)) if hi else None] for i, j, lo, hi in spec.get('pairs', [])]
    A = GenAdv(roles, eta=float(kw.get('eta', 1e-2)), beta=float(kw.get('beta', 1e-3)), etas=float(kw.get('etas', 1e-3)),
               xmin=0.0, fk=int(kw.get('fk', 7)), pairs=pairs or None, dt=1e-3, extra=extra)
    t0 = time.time()
    st, sol = A.run(tl=int(kw.get('tl', 1200)), maxit=300, verbose=False)
    print(tag, st, '(%.0fs)' % (time.time() - t0), flush=True)
    if sol is None: return
    X = sol
    v = {'x%d' % i: X['x'][i] for i in range(3)}
    v.update({'s%d' % i: X['sigma'][i] for i in range(3)}); v.update({'t%d' % i: X['t'][i] for i in range(3)})
    v['tau'] = X['tau']
    for k, n in enumerate(names):
        for j in range(3): v['c%s_%d' % (n, j)] = X['roles'][k][j]
    fn = 'certs/madv_%s.json' % tag
    json.dump({'path': [], 'v': v, 'beta': float(kw.get('beta', 1e-3))}, open(fn, 'w'))
    print('x', np.round(X['x'], 4).tolist(), 'tau %.4f' % X['tau'], flush=True)
    out = subprocess.run(['python3', 'gadv_verify.py', sys.argv[1], fn, '0'], capture_output=True, text=True)
    print('\n'.join(out.stdout.strip().splitlines()[-3:]), out.stderr[-300:], flush=True)


if __name__ == '__main__':
    main()
