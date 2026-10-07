"""DFS strict-adversary search with a node budget (no certificate kept); on ADVERSARY the point is saved and exactly
re-checked by gadv_verify.py.  usage: python3 adv_dfs.py strat.json pi0 tag [fk=7] [budget=..] [strong=0]"""
import sys, json, time, subprocess
from fractions import Fraction as F
import gen_cert as G, gen_cert2 as G2
spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2]); tag = sys.argv[3]
kw = dict(a.split('=') for a in sys.argv[4:])
S = G.Strategy(spec, pi0, fk=int(kw.get('fk', 7)), lazy=True); E = G2.Engine2(S); E.strong = int(kw.get('strong', 0))
t0 = time.time()
st, a, b = E.run(maxnodes=int(kw.get('budget', 50000)), verbose=False)
print(tag, st, '(%.0fs)' % (time.time() - t0), flush=True)
if st == 'ADVERSARY':
    beta, v = b
    fn = 'certs/gadv_%s.json' % tag
    json.dump({'path': a, 'v': dict(zip(S.VARS, map(float, v))), 'beta': beta}, open(fn, 'w'))
    print('beta %.6g' % beta, {k: round(float(x), 5) for k, x in zip(S.VARS, v) if not k.startswith('c')}, flush=True)
    out = subprocess.run(['python3', 'gadv_verify.py', sys.argv[1], fn, sys.argv[2]], capture_output=True, text=True).stdout
    print(out.strip().splitlines()[-1] if out.strip() else 'verify: no output', flush=True)
