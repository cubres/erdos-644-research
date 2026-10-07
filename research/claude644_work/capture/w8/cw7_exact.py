"""Exact certificate that max{tau_w : w(E)<=1, 0<=w_v<=1/2} <= 1 for each family in a JSON list.
Dual: distribution lambda on minimal transversals J, alpha_E>=0, beta_v>=0 with
   sum_{E ni v} alpha_E + beta_v >= sum_{J ni v} lambda_J  (all v),   sum alpha + sum beta/2 <= 1.
Then for any feasible w: min_J w(J) <= sum_J lambda_J w(J) <= sum_v w_v (sum_E alpha + beta)
   = sum_E alpha_E w(E) + sum_v beta_v w_v <= sum alpha + sum beta/2 <= 1.
Discovery by HiGHS, then rationalised and checked exactly (beta recomputed exactly)."""
import json, sys
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
from wtd_search import min_transversals
def certify(E, n):
    T = min_transversals(E, n); m = len(E); t = len(T)
    # variables: lambda (t), alpha (m), beta (n); minimize sum alpha + sum beta/2
    c = np.concatenate([np.zeros(t), np.ones(m), 0.5*np.ones(n)])
    A_ub = []; b_ub = []
    for v in range(n):
        row = np.zeros(t+m+n)
        for k,J in enumerate(T):
            if J>>v&1: row[k] = 1
        for k,e in enumerate(E):
            if e>>v&1: row[t+k] = -1
        row[t+m+v] = -1
        A_ub.append(row); b_ub.append(0)
    A_eq = [np.concatenate([np.ones(t), np.zeros(m+n)])]
    r = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=[1], bounds=(0,None), method='highs')
    lam = [F(x).limit_denominator(60) for x in r.x[:t]]; s = sum(lam)
    lam = [x/s for x in lam]
    alpha = [F(x).limit_denominator(60) for x in r.x[t:t+m]]
    beta = [max(F(0), sum(lam[k] for k,J in enumerate(T) if J>>v&1) - sum(alpha[k] for k,e in enumerate(E) if e>>v&1)) for v in range(n)]
    obj = sum(alpha) + sum(beta)/2
    return obj, float(r.fun)
if __name__ == '__main__':
    data = json.load(open(sys.argv[1])); n = int(sys.argv[2]); worst = F(0); bad = 0
    for i, c in enumerate(data):
        obj, fl = certify(c['edges'], n)
        worst = max(worst, obj)
        if obj > 1: bad += 1; print('NOT CERTIFIED', i, obj, fl, c['edges'])
    print('families', len(data), 'max exact dual bound', worst, 'uncertified', bad)
