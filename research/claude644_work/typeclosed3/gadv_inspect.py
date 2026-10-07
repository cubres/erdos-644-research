"""inspect a gen_cert adversary: roles, tau*(named roles) and cheapest blocking thresholds (escape box)"""
import sys, json
from fractions import Fraction as F
from tc3lib import tau_star
d = json.load(open(sys.argv[1])); v = d['v']
x = [F(v['x%d' % i]).limit_denominator(10**6) for i in range(3)]
names = sorted(set(k[1:].rsplit('_', 1)[0] for k in v if k.startswith('c')))
roles = {n: [F(v['c%s_%d' % (n, j)]).limit_denominator(10**6) for j in range(3)] for n in names}
print('x', [float(a) for a in x], 'sigma', [round(v['s%d' % i], 4) for i in range(3)], 'tau %.4f' % v['tau'], 'beta %.5f' % d['beta'])
for n in names: print(' ', n, [round(float(a), 4) for a in roles[n]])
K = list(set(tuple(r) for r in roles.values()))
ts, thr = tau_star(K, x, want=True)
print('tau*(roles) = %.4f  thresholds' % float(ts), [None if t is None else round(float(t), 4) for t in thr])
