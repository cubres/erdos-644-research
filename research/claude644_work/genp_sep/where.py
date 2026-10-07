"""LP points of the deepest pending stack entries of a gen_certp checkpoint: python3 where.py <ck.pkl> <strategy.json> <pi0> [k]"""
import sys, pickle, json
from fractions import Fraction as F
import numpy as np
import gen_certp as GP
st = pickle.load(open(sys.argv[1], 'rb')); spec = json.load(open(sys.argv[2])); pi0 = F(sys.argv[3])
k = int(sys.argv[4]) if len(sys.argv) > 4 else 5
S = GP.StratP(spec, pi0); E = GP.EngineP(S)
for path, extra in st['stack'][-k:]:
    beta, v = E.lp(S.BASE + extra)
    if v is None: print(len(path), 'infeasible'); continue
    d, roles = GP.describe(S, v)
    print(len(path), 'beta %.4f' % beta, d, {n: r for n, r in roles.items()})
