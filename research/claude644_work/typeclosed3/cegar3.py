"""CEGAR driver: strategy (JSON list of roles) vs MILP adversary; on ADVERSARY add the cheapest template-completing
request (find_requests) or, failing that, the cheapest escape box of the role set.  Logs to logs/cegar_<name>.log and
saves strategy to strat_<name>.json after each round.
usage: python3 cegar3.py <name> <init tags> [eta] [order|-] [rounds]"""
import sys, json, time
import numpy as np
from roles3 import Adv, ureq, R, LINES
from run_strat import build
from find_requests import search, req_role_6plus1
from verify_adv import check, badness, rationalise
from roles3 import load_tt, req_mp
from tc3lib import tau_star


def escape_role(sol):
    """cheapest blocking box of the valid roles -> request u = thresholds (as constants relative to nothing: we
    encode it as the box (min over the roles blocked at each part) - this is role-relative: u_i = min_{r in P_i} r_i"""
    x, sg, tau, t, roles = rationalise(sol)
    valid = [q is None or q == 1 for q in sol['Q']]
    idx = [j for j in range(len(roles)) if valid[j]]
    K = [tuple(roles[j]) for j in idx]
    cost, thr = tau_star(K, x, want=True)
    u = []
    for i in range(3):
        if thr[i] is None:
            u.append([{'x%d' % i: 1}])
        else:
            P = [idx[k] for k, c in enumerate(K) if c[i] == thr[i]]
            u.append([{R(j, i): 1, 'c': -1e-4} for j in P[:1]])   # strictly below the threshold role
    return ureq(u, tag='escape', cost=float(cost))


def main():
    name = sys.argv[1]; tags = sys.argv[2]
    eta = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-2
    order = None if len(sys.argv) <= 4 or sys.argv[4] == '-' else tuple(int(c) for c in sys.argv[4])
    rounds = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    xmin = float(sys.argv[6]) if len(sys.argv) > 6 else 0.02
    tl = int(sys.argv[7]) if len(sys.argv) > 7 else 900
    sf = 'strat_%s.json' % name
    try:
        roles = json.load(open(sf)); print('resumed strategy', sf, len(roles), 'roles')
    except Exception:
        roles = build(tags.replace('A', ''))
    log = open('logs/cegar_%s.log' % name, 'a')
    tt = load_tt()
    for rd in range(rounds):
        t0 = time.time()
        A = Adv(roles, eta=eta, order=order, box=('sigma' if 'L' in tags else True), xmin=xmin, caseA=('A' in tags),
                tmpl=('F', 'V', 'TT', 'K4', 'T3'))
        st, sol = A.run(verbose=False, maxit=200, tl=tl)
        msg = 'round %d roles %d status %s (%.0fs)' % (rd, len(roles), st, time.time() - t0)
        print(msg, flush=True); log.write(msg + '\n'); log.flush()
        if st != 'ADVERSARY':
            json.dump(roles, open(sf, 'w'))
            log.write('DONE %s\n' % st); log.flush()
            return
        errs, (x, sg, tau, t, rl) = check(sol, order, verbose=False)
        valid = [q is None or q == 1 for q in sol['Q']]
        b, arg = badness(x, rl, valid, tt, tau=tau)
        json.dump(sol, open('logs/cegar_%s_adv%d.json' % (name, rd), 'w'))
        msg = '  adv x=%s tau=%.4f badness=%.5f errs=%s' % (np.round(sol['x'], 4).tolist(), sol['tau'], b, errs)
        print(msg, flush=True); log.write(msg + '\n')
        best, allf = search(sol)
        existing = set(json.dumps(r, sort_keys=True) for r in roles)
        added = None
        for cost, kind, key in allf:
            if kind == '6+1':
                pts = {q + 1: key[q] for q in range(6)}
                role = req_role_6plus1(pts)
            else:
                role = req_mp(key[0], key[1]); role['tag'] = 'MP'
            js = json.dumps(role, sort_keys=True)
            if js not in existing:
                added = (cost, kind, key, role); break
        if added is None:
            role = escape_role(sol)
            added = (role['cost'], 'escape', None, role)
        roles.append(added[3])
        json.dump(roles, open(sf, 'w'))
        msg = '  ADD %s cost %.4f key %s -> %d roles' % (added[1], added[0], added[2], len(roles))
        print(msg, flush=True); log.write(msg + '\n'); log.flush()


if __name__ == '__main__':
    main()
