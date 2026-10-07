"""Fano-with-requests (FR) evaluator.  Lines of PG(2,2) as in heavylib.  An assignment maps each line to a type index
or None (light: any type; needs total avoided mass < tau*).  LP over point masses m[p][i] >= 0, sum_p m[p][i] = x_i;
actual line l with type t: sum_{p in l} m[p][i] <= x_i - t_i;  minimise the max light mass."""
import itertools, numpy as np, sys
from scipy.optimize import linprog
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as h
LINES = h.LINES
def fr_lp(x, T, asg, ret_m=False):
    p = len(x); nv = 7*p + 1
    A = []; b = []; Aeq = []; beq = []
    for i in range(p):
        r = np.zeros(nv); r[[q*p+i for q in range(7)]] = 1; Aeq.append(r); beq.append(x[i])
    light = False
    for li, l in enumerate(LINES):
        t = asg[li]
        if t is not None:
            for i in range(p):
                r = np.zeros(nv); r[[q*p+i for q in l]] = 1; A.append(r); b.append(x[i]-T[t][i])
        else:
            light = True
            r = np.zeros(nv); r[[q*p+i for q in l for i in range(p)]] = 1; r[-1] = -1; A.append(r); b.append(0)
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=np.array(Aeq), b_eq=beq,
                  bounds=[(0, None)]*(7*p) + [(0 if light else 0, None)], method='highs')
    if res.status != 0: return None if not ret_m else (None, None)
    return res.fun if not ret_m else (res.fun, res.x[:-1].reshape(7, p))
# P1: pencil at point 0 = lines 0,1,2 (0,1,2),(0,3,4),(0,5,6); quad lines 3..6; actual quad line = 3 (1,3,5)
def p1_best(x, T, taus, want_all=False):
    n = len(T); best = (-1e9, None); allok = []
    for pen in itertools.combinations_with_replacement(range(n), 3):
        for q in range(n):
            asg = [pen[0], pen[1], pen[2], q, None, None, None]
            v = fr_lp(x, T, asg)
            if v is None: continue
            mg = taus - v
            if mg > best[0]: best = (mg, asg)
            if want_all and mg > 0: allok.append((mg, asg))
    return (best, allok) if want_all else best
