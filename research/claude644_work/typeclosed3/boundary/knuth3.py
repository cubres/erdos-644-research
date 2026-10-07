"""Knuth's random-probe estimate of the size of the certificate tree of gen_cert2 (same branching rule, strong=0):
from the root, repeatedly branch, solve the LP of every child, move to a uniformly random LP-feasible child;
estimate = product of the numbers of children (all children, feasible or not, become nodes).
usage: python3 knuth_est.py strat.json pi0 [probes=50] [fk=7] [seed=0]"""
import sys, json, random
from fractions import Fraction as F
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); import gen_cert as G, gen_cert2 as G2; from gen_cert3 import Engine3

spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2]); kw = dict(a.split('=') for a in sys.argv[3:])
S = G.Strategy(spec, pi0, fk=int(kw.get('fk', 7)), menu=('F','V','T3','R'), lazy=True); E = Engine3(S); E.rk = int(kw.get('rk', 4))
rnd = random.Random(int(kw.get('seed', 0)))
ests = []
for pr in range(int(kw.get('probes', 50))):
    extra = []; est = 1.0; nodes_est = 1.0; depth = 0
    while True:
        beta, v = E.lp(S.BASE + extra)
        if beta is None or beta <= 1e-9: break
        d_ok, d_sc = E.disj_status(v); bad = np.nonzero(~d_ok)[0]
        pick = E.names[bad[0]] if len(bad) else None
        if pick is None:
            K = int(kw.get('strong', 0))
            if K:
                best = None
                for nm in E.top_templates(v, k=K):
                    nf = 0
                    for alt in E.disj(nm):
                        b2, v2 = E.lp(S.BASE + extra + list(alt))
                        if b2 is not None and b2 > 1e-9: nf += 1
                        if best is not None and nf >= best[0]: break
                    if best is None or nf < best[0]: best = (nf, nm)
                pick = best[1] if best else None
            else:
                bt = E.best_template(v); pick = bt[1] if bt else None
        if pick is None: print('ADVERSARY hit in probe', pr); break
        alts = E.disj(pick)
        feas = []
        for alt in alts:
            b2, v2 = E.lp(S.BASE + extra + list(alt))
            if b2 is not None and b2 > 1e-9: feas.append(alt)
        est *= len(alts); depth += 1
        if not feas: break
        # each infeasible child is a leaf; continue into a random feasible child, weight = #feasible
        est = est / len(alts) * len(feas)
        nodes_est += est
        extra = extra + list(rnd.choice(feas))
    ests.append(nodes_est)
    if (pr + 1) % 10 == 0:
        print('probes %d: mean feasible-node estimate %.3g (median %.3g, max %.3g)' % (pr + 1, np.mean(ests), np.median(ests), np.max(ests)), flush=True)
