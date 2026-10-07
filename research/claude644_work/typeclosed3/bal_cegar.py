"""CEGAR for the separated regime: strategy (roles) vs BalAdv MILP adversary.
On ADVERSARY: add (1) the cheapest valid 6+1 completing request (Fano with 6 actual valid roles, 1 requested point)
and (2) the cheapest ESCAPE box of the valid roles (a box of cost < tau containing no named role: its answer is a
type the adversary has not named), both as request roles (linear in role coordinates).
usage: python3 bal_cegar.py <name> <init tags> [key=val ...]  (keys as bal_run + rounds=)
Logs to logs_caseA/cegar_<name>.log, strategy saved to strat_bal_<name>.json after each round."""
import sys, json, time, itertools
import numpy as np
from fractions import Fraction as F
from bal_adv import BalAdv, LINES, req, req_6p1, R
from bal_run import build
from tc3lib import tau_star

PEN0 = [l for l in LINES if 0 in l]


def six_plus_one(sol, maxk=3, top=5):
    x = np.array(sol['x']); tau = sol['tau']; Rl = np.array(sol['roles'])
    valid = [q is None or q == 1 for q in sol['Q']]
    groups = {}
    for j in range(len(Rl)):
        if valid[j]: groups.setdefault(tuple(np.round(Rl[j], 7)), []).append(j)
    reps = [g[0] for g in groups.values()]
    found = []; seen = set()
    for k in range(1, maxk + 1):
        for combo in itertools.combinations(reps, k):
            for pat in itertools.product(range(k), repeat=6):
                if len(set(pat)) != k: continue
                pts = [combo[p] for p in pat]           # points 1..6
                P = {q + 1: pts[q] for q in range(6)}
                ok = True
                for l in LINES:
                    if 0 in l: continue
                    if np.any(sum(Rl[P[q]] for q in l) > 2 * x + 1e-12): ok = False; break
                if not ok: continue
                u = x.copy()
                for l in PEN0:
                    o = [q for q in l if q != 0]
                    u = np.minimum(u, 2 * x - Rl[P[o[0]]] - Rl[P[o[1]]])
                u = np.minimum(u, 4 * x - sum(Rl[P[q]] for q in range(1, 7)))
                u = np.maximum(u, 0)
                cost = float((x - u).sum())
                if cost < tau:
                    key = tuple(pts)
                    if key in seen: continue
                    seen.add(key); found.append((cost, key))
    found.sort()
    return found


def escape(sol):
    """cheapest blocking map of the valid roles (exact).  Returns (cost, request role) or None if cost >= tau."""
    x = [F(v).limit_denominator(10 ** 9) for v in sol['x']]
    tau = sol['tau']
    idx = [j for j, q in enumerate(sol['Q']) if q is None or q == 1]
    Kr = [tuple(F(v).limit_denominator(10 ** 9) for v in sol['roles'][j]) for j in idx]
    cost, thr = tau_star(Kr, x, want=True)
    if float(cost) >= tau - 1e-9:
        return None
    u = []
    for i in range(3):
        if thr[i] is None:
            u.append([])
        else:
            P = [idx[k] for k, c in enumerate(Kr) if c[i] == thr[i]]
            u.append([{R(P[0], i): 1, 'c': -1e-5}])
    return float(cost), req(u, tag='escape')


def main():
    name = sys.argv[1]; tags = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    sf = 'strat_bal_%s.json' % name
    try:
        roles = json.load(open(sf)); print('resumed', sf, len(roles))
    except Exception:
        roles = build(tags)
    log = open('logs_caseA/cegar_%s.log' % name, 'a')
    def say(msg):
        print(msg, flush=True); log.write(msg + '\n'); log.flush()
    for rd in range(int(kw.get('rounds', 40))):
        t0 = time.time()
        A = BalAdv(roles, eta=float(kw.get('eta', 1e-2)), beta=float(kw.get('beta', 1e-3)), etas=float(kw.get('etas', 1e-3)),
                   xmin=float(kw.get('xmin', 0.75)), fk=int(kw.get('fk', 4)), sepmargin=float(kw.get('sepm', 0.0)))
        st, sol = A.run(verbose=False, tl=int(kw.get('tl', 3000)), maxit=400)
        say('round %d roles %d status %s (%.0fs)' % (rd, len(roles), st, time.time() - t0))
        if st != 'ADVERSARY':
            say('DONE %s' % st); json.dump(roles, open(sf, 'w')); return
        json.dump(sol, open('logs_caseA/cegar_%s_adv%d.json' % (name, rd), 'w'))
        say('  adv x=%s tau=%.4f sigma-2x/3=%s roles=%s' % (np.round(sol['x'], 4).tolist(), sol['tau'],
            np.round(np.array(sol['sigma']) - 2 * np.array(sol['x']) / 3, 4).tolist(),
            [np.round(r, 3).tolist() for r in sol['roles']]))
        existing = set(json.dumps(r, sort_keys=True) for r in roles)
        added = []
        for cost, key in six_plus_one(sol):
            role = req_6p1(list(key))
            js = json.dumps(role, sort_keys=True)
            if js not in existing:
                added.append(('6+1', cost, key, role)); break
        esc = escape(sol)
        if esc is not None:
            added.append(('escape', esc[0], None, esc[1]))
        if not added:
            say('  NO completing request and no escape box: the named roles form a family with tau* >= tau and no '
                'template of the menu -- genuine candidate'); return
        for kind, cost, key, role in added:
            roles.append(role); say('  ADD %s cost %.4f key %s' % (kind, cost, key))
        json.dump(roles, open(sf, 'w'))


if __name__ == '__main__':
    main()
