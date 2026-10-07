"""Driver for bal_adv.py.  usage: python3 bal_run.py <tags> <name> [key=value ...]
tags: m = 3 minimisers; v = 3 vertex requests; p = pencil requests on the minimisers; P = pencil requests on all roles
so far; M = MP requests among the minimisers (ordered pairs incl. b==c); d = discard-route requests on ordered pairs
of the minimisers (and m^i, m^i); o = the three Corollary-C monochromatic window roles; f<k> = k free roles.
keys: eta, beta, etas, xmin, xmax, fk, tl, maxit, strat=<json file of extra roles>"""
import sys, json, time
from bal_adv import *


def build(tags):
    roles = []
    i = 0
    while i < len(tags):
        tg = tags[i]
        if tg == 'm': roles += mins()
        elif tg == 'v': roles += [req_vertex(j) for j in range(3)]
        elif tg == 'p': roles += [req_pencil(k) for k in range(3)]
        elif tg == 'P':
            n = len(roles); roles += [req_pencil(k) for k in range(n)]
        elif tg == 'M': roles += [req_mp(b, c) for b in range(3) for c in range(3)]
        elif tg == 'd': roles += [req_discard(a, c) for a in range(3) for c in range(a, 3)]
        elif tg == 'o': roles += [{'kind': 'mono', 'cls': j} for j in range(3)]
        elif tg == 'b': roles += [{'kind': 'blk', 'facet': j} for j in range(3)]
        elif tg == 'e': roles += [req([[{'c': 0.0}] if jj == j else [] for jj in range(3)], tag='empty%d' % j) for j in range(3)]
        elif tg == 'f':
            k = int(tags[i + 1]); i += 1; roles += [{'kind': 'free'} for _ in range(k)]
        else: raise ValueError(tg)
        i += 1
    return roles


if __name__ == '__main__':
    tags = sys.argv[1]; name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    roles = build(tags)
    if 'strat' in kw:
        roles += json.load(open(kw['strat']))
    if kw.get('mode') == 'gen':
        pairs = json.loads(kw['pairs']) if 'pairs' in kw else None
        A = GenAdv(roles, eta=float(kw.get('eta', 1e-2)), beta=float(kw.get('beta', 1e-3)), etas=float(kw.get('etas', 1e-3)),
                   xmin=float(kw.get('xmin', 0.02)), xmax=float(kw.get('xmax', 1.5)), fk=int(kw.get('fk', 4)), pairs=pairs,
                   dt=float(kw.get('dt', 1e-3)))
    else:
      A = BalAdv(roles, eta=float(kw.get('eta', 1e-2)), beta=float(kw.get('beta', 1e-3)), etas=float(kw.get('etas', 1e-3)),
               xmin=float(kw.get('xmin', 0.75)), xmax=float(kw.get('xmax', 1.5)), fk=int(kw.get('fk', 4)),
               sep=bool(int(kw.get('sep', 1))), sepmargin=float(kw.get('sepm', 0.0)),
               menu=tuple(kw.get('menu', 'F,TT,T3,K4').split(',')))
    print('roles', len(roles), kw, flush=True)
    st, sol = A.run(tl=int(kw.get('tl', 600)), maxit=int(kw.get('maxit', 300)))
    print(name, st, flush=True)
    if sol:
        fn = 'badv_%s.json' % name
        json.dump(sol, open(fn, 'w')); print('saved', fn)
