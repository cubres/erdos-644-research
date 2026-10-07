"""Region CEGAR with full certification: each round runs the exact engine (gen_cert3, menu F,V,T3,R, streamed
certificate) to completion or to the first adversary; on an adversary it adds the escape-box request (cegar_exact)
and restarts.  usage: python3 cegar4.py <start.json> <name> [pi0=0] [rounds=40] [maxnodes=5000000] [fk=7] [rk=4]"""
import sys, json, time, os, gzip
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from gen_cert3 import Engine3, Strategy3
from cegar_exact import escape_request


def main():
    spec = json.load(open(sys.argv[1])); name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    pi0 = F(kw.get('pi0', '0')); maxn = int(kw.get('maxnodes', 5000000)); fk = int(kw.get('fk', 7)); rk = int(kw.get('rk', 4))
    log = open(os.path.join(HERE, 'cx4_%s.log' % name), 'a')
    def say(m):
        print(m, flush=True); log.write(time.strftime('%H:%M:%S ') + m + '\n'); log.flush()
    for rd in range(int(kw.get('rounds', 40))):
        S = Strategy3(spec, pi0, fk=fk, menu=tuple(kw.get('menu', 'F,V,T3,R,W').split(',')), lazy=True); E = Engine3(S); E.rk = rk; E.strong = int(kw.get('strong', 4))
        fn = os.path.join(HERE, 'certs', 'gcert4_%s_r%d.jsonl.gz' % (name, rd))
        E.stream = gzip.open(fn + '.part', 'wt')
        E.stream.write(json.dumps({'pi0': str(pi0), 'strategy': spec, 'fk': fk, 'rk': rk, 'menu': list(S.menu),
                                   'format': 'jsonl-v1'}) + '\n')
        json.dump(spec, open(os.path.join(HERE, 'strat_cx4_%s_r%d.json' % (name, rd)), 'w'))
        t0 = time.time()
        st, a, b = E.run(maxnodes=maxn, verbose=False)
        E.stream.close()
        say('round %d roles %d: %s (%.0fs, leaves %d)' % (rd, len(S.names), st, time.time() - t0, getattr(E, 'nleaves', 0)))
        if st == 'CERTIFIED':
            os.rename(fn + '.part', fn); say('CERTIFIED -> %s' % fn); return
        os.remove(fn + '.part')
        if st != 'ADVERSARY':
            say('STOP: %s' % st); return
        beta, v = b
        valid = [n for n in S.names if not E.is_void(n, v)]
        say('  adversary beta %.5f x=%s tau=%.4f roles %s' % (beta, [round(float(v[S.VI['x%d' % i]]), 4) for i in range(3)],
            v[S.VI['tau']], {n: [round(float(v[S.VI[S.c(n, j)]]), 4) for j in range(3)] for n in valid}))
        json.dump({'v': dict(zip(S.VARS, map(float, v))), 'beta': beta, 'valid': valid},
                  open(os.path.join(HERE, 'certs', 'gadv4_%s_r%d.json' % (name, rd)), 'w'))
        role, cost = escape_request(S, v, valid, 'X%d' % rd)
        if cost >= v[S.VI['tau']] - 1e-12:
            say('  NO escape box (tau*(roles) = %.4f >= tau): candidate genuine family!' % cost); return
        say('  ADD escape %s cost %.4f u=%s strict=%s' % (role['name'], cost, role['u'], role['strict']))
        spec = dict(spec); spec['roles'] = spec['roles'] + [role]


if __name__ == '__main__':
    main()
