"""best-first strict-adversary search for a strategy (no certificate).  usage: python3 adv_search.py strat.json pi0 [fk=7] [budget=..]"""
import sys, json, time
from fractions import Fraction as F
import gen_cert as G, gen_cert2 as G2
spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2]); kw = dict(a.split('=') for a in sys.argv[3:])
S = G.Strategy(spec, pi0, fk=int(kw.get('fk', 7)), lazy=True); E = G2.Engine2(S)
base = sys.argv[1].split('/')[-1].replace('.json', '')
t0 = time.time()
st, a, b = G2.adversary_search(E, budget=int(kw.get('budget', 200000)))
print(st, '(%.0fs)' % (time.time() - t0), a if st != 'ADVERSARY' else '')
if st == 'ADVERSARY':
    beta, v = b
    print('beta %.6g' % beta, {k: round(float(x), 5) for k, x in zip(S.VARS, v)})
    json.dump({'path': a, 'v': dict(zip(S.VARS, map(float, v))), 'beta': beta}, open('certs/gadv_%s_%s.json' % (base, str(pi0).replace('/', '_')), 'w'))
