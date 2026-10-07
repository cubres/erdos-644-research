"""CEGAR with gen_cert3 (menu F,V,T3,R): search a strict adversary (node budget); if found add the ESCAPE-BOX request
of its valid roles (cheapest free box of the role family, strict at the threshold roles' coordinates; valid at the
adversary since its cost tau*(roles) < tau), repeat.  usage: python3 cegar3.py <start.json> <name> [pi0=0]
[rounds=30] [budget=20000] [fk=7] [rk=4]"""
import sys, json, time, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import gen_cert as G
from gen_cert3 import Engine3
from cegar_exact import escape_request


def main():
    spec = json.load(open(sys.argv[1])); name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    pi0 = F(kw.get('pi0', '0')); budget = int(kw.get('budget', 20000)); fk = int(kw.get('fk', 7)); rk = int(kw.get('rk', 4))
    log = open(os.path.join(HERE, 'cx3_%s.log' % name), 'a')
    def say(m):
        print(m, flush=True); log.write(m + '\n'); log.flush()
    for rd in range(int(kw.get('rounds', 30))):
        S = G.Strategy(spec, pi0, fk=fk, menu=('F', 'V', 'T3', 'R'), lazy=True); E = Engine3(S); E.rk = rk
        t0 = time.time()
        st, a, b = E.run(maxnodes=budget, verbose=False)
        say('round %d roles %d: %s (%.0fs)' % (rd, len(S.names), st, time.time() - t0))
        json.dump(spec, open(os.path.join(HERE, 'strat_cx3_%s.json' % name), 'w'))
        if st != 'ADVERSARY':
            say('STOP: %s -- strategy saved to strat_cx3_%s.json' % (st, name)); return
        beta, v = b
        valid = [n for n in S.names if not E.is_void(n, v)]
        say('  adversary beta %.5f x=%s tau=%.4f roles %s' % (beta, [round(float(v[S.VI['x%d' % i]]), 4) for i in range(3)],
            v[S.VI['tau']], {n: [round(float(v[S.VI[S.c(n, j)]]), 4) for j in range(3)] for n in valid}))
        role, cost = escape_request(S, v, valid, 'X%d' % rd)
        if cost >= v[S.VI['tau']] - 1e-12:
            say('  NO escape box (tau*(roles) = %.4f >= tau)' % cost); return
        say('  ADD escape %s cost %.4f u=%s strict=%s' % (role['name'], cost, role['u'], role['strict']))
        spec = dict(spec); spec['roles'] = spec['roles'] + [role]


if __name__ == '__main__':
    main()
