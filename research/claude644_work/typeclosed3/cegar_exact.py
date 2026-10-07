"""CEGAR with the exact lazy engine (gen_cert2): search for a strict adversary (bounded node budget); if found, add the
ESCAPE-BOX request of its valid roles (the cheapest box containing none of them; strict thresholds at the threshold
roles' coordinates) and repeat.  The escape box is valid at the adversary (its cost = tau*(roles) < tau), so the new
answer is a genuinely forced new type.  When the search budget is exhausted without adversary, run the full
certification separately (gen_cert2 on the saved strategy).
usage: python3 cegar_exact.py <start strategy.json> <name> [pi0=0] [rounds=30] [budget=20000] [fk=7]"""
import sys, json, time
from fractions import Fraction as F
import numpy as np
import gen_cert as G
import gen_cert2 as G2
from tc3lib import tau_star


def escape_request(S, v, valid_names, tag):
    x = [F(v[S.VI['x%d' % i]]).limit_denominator(10 ** 9) for i in range(3)]
    R = {n: tuple(F(v[S.VI[S.c(n, j)]]).limit_denominator(10 ** 9) for j in range(3)) for n in valid_names}
    K = list(set(R.values()))
    cost, thr = tau_star(K, x, want=True)
    u = [[], [], []]; strict = []
    for i in range(3):
        if thr[i] is None: continue
        owner = next(n for n in valid_names if R[n][i] == thr[i])
        u[i] = [{S.c(owner, i): 1}]; strict.append(i)
    return {'name': tag, 'kind': 'req', 'u': u, 'strict': strict}, float(cost)


def main():
    spec = json.load(open(sys.argv[1])); name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    pi0 = F(kw.get('pi0', '0')); budget = int(kw.get('budget', 20000)); fk = int(kw.get('fk', 7))
    log = open('logs_caseA/cx_%s.log' % name, 'a')
    def say(m):
        print(m, flush=True); log.write(m + '\n'); log.flush()
    for rd in range(int(kw.get('rounds', 30))):
        S = G.Strategy(spec, pi0, fk=fk, lazy=True); E = G2.Engine2(S)
        t0 = time.time()
        st, a, b = E.run(maxnodes=budget, verbose=False)
        say('round %d roles %d: %s (%.0fs)' % (rd, len(S.names), st, time.time() - t0))
        json.dump(spec, open('strategies/cx_%s.json' % name, 'w'))
        if st != 'ADVERSARY':
            say('STOP: %s -- strategy saved to strategies/cx_%s.json' % (st, name)); return
        beta, v = b
        valid = [n for n in S.names if not E.is_void(n, v)]
        say('  adversary beta %.5f x=%s tau=%.4f' % (beta, [round(float(v[S.VI['x%d' % i]]), 4) for i in range(3)], v[S.VI['tau']]))
        role, cost = escape_request(S, v, valid, 'X%d' % rd)
        if cost >= v[S.VI['tau']] - 1e-12:
            say('  NO escape box (tau*(roles) = %.4f >= tau): the named roles are a family with tau* >= tau' % cost); return
        say('  ADD escape %s cost %.4f u=%s' % (role['name'], cost, role['u']))
        spec = dict(spec); spec['roles'] = spec['roles'] + [role]


if __name__ == '__main__':
    main()
