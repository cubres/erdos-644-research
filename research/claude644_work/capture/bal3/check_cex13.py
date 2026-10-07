import json, sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '../heavy')
import heavylib as h, pairlib as P, numpy as np
L = [l for l in open('logs/cegar_min.log') if 'GENUINE' in l][0]
d = json.loads(L[L.index('{'):])
x = [F(round(v*13), 13) for v in d['x']]
T = sorted(set(tuple(F(round(v*13), 13) for v in t) for t in d['T']))
T = [list(t) for t in T if sum(t) == 1]
print("x", x); print("types", [[str(v) for v in t] for t in T])
print("tau* exact", h.tau_star_fast(x, T))
fa = h.all_fano(x, T, tol=0)
print("Fano assignments feasible:", len(fa), fa[:5])
xf = [float(v) for v in x]; Tf = [[float(v) for v in t] for t in T]
print("pair margin (42 fns):", P.pair_margin(xf, Tf), P.any_pair(xf, Tf))
print("fano margin:", h.fano_margin(xf, Tf))
R = h.reparr(len(Tf)); mg, k = h.fano_margin(xf, Tf)
asg = R[k]; print("best assignment", asg, "lines", h.LINES)
S = [[j for j in range(len(T)) if 3*T[j][i] > 2*x[i]] for i in range(3)]
print("classes", S)
cls = lambda j: ''.join('ABC'[i] for i in range(3) if j in S[i])
print("line colours", [cls(j) for j in asg])
# margins of T/V among all types (not just roles)
import b3lib as B
print("T margin", B.t_margin(xf, Tf), "V margin", B.v_margin(xf, Tf))
