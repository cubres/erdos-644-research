"""Referee w9, heavyparts#0 BRK, part E: from a float start (x, three types), maximise the minimum of the
strict margins  g1 (no conflict, >=0), -g2 (Fano-free, >0), sh (super-heavy, >0), tau*-3/4 (>0), admissibility,
then round to rationals and certify EXACTLY (brute force of all 3^7 maps, exact tau*).
usage: python3 w9_ref_heavyparts0brk_refine.py SEED ITERS 'x0,x1,x2' 'a0,a1,a2' 'b0,b1,b2' 'c0,c1,c2'"""
import sys, random
from fractions import Fraction as Fr
import w9_ref_heavyparts0brk_climb as C
import w9_ref_heavyparts0brk_random as R
from w9_ref_heavyparts0brk_arccsp import minimal_hitting
MH = [set(F) for F in minimal_hitting()]
def m(x, T):
    p = len(x)
    if min(x) <= 0 or any(t < 0 for a in T for t in a): return -9
    adm = min(x[i]-a[i] for a in T for i in range(p))
    g1, g2, sh = C.margins(x, T)
    return min(g1, -g2, sh, C.tau_f(x, T) - 0.75, adm)
def norm(T): return [[t/sum(a) for t in a] for a in T]
if __name__ == '__main__':
    seed, iters = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
    x = [float(t) for t in sys.argv[3].split(',')]
    T = [[float(t) for t in s.split(',')] for s in sys.argv[4:7]]
    T = norm(T); p = len(x); cur = m(x, T); step = 0.01
    for it in range(iters):
        x2 = [v + rng.gauss(0, step) if rng.random() < .5 else v for v in x]
        T2 = norm([[max(0.0, t + rng.gauss(0, step)) if rng.random() < .5 else t for t in a] for a in T])
        v = m(x2, T2)
        if v >= cur: x, T, cur = x2, T2, v
        if it % 3000 == 2999: step = max(step*.7, 1e-6)
    print('float margin %.6f' % cur, 'tau* %.5f' % C.tau_f(x, T), 'x', [round(t, 5) for t in x], 'T', [[round(t, 5) for t in a] for a in T])
    for D in (1000, 10000, 100000):
        xq = [Fr(round(t*D), D) for t in x]; Tq = []
        for a in T:
            aq = [Fr(round(t*D), D) for t in a]; k = max(range(p), key=lambda i: aq[i]); aq[k] += 1 - sum(aq); Tq.append(aq)
        adm = all(0 <= Tq[c][i] <= xq[i] for c in range(3) for i in range(p)) and all(sum(a) == 1 for a in Tq)
        sup = all(3*Tq[c][c] > 2*xq[c] for c in range(3))
        Fb = R.forbidden(xq, Tq); conf = any(F <= Fb for F in MH)
        fano = R.feas(xq, Tq); pen = R.feas(xq, Tq, totals=False); ts = R.tau_star(xq, Tq)
        print('D=%d EXACT: admissible=%s superheavy=%s conflict=%s pencil_feasible_map=%s FANO=%s tau*=%s (%.5f)' %
              (D, adm, sup, conf, pen, fano, ts, float(ts)))
        if adm and sup and not conf and fano is None and ts > Fr(3, 4):
            print('  CERTIFIED totals-killed family: x', [str(t) for t in xq], 'T', [[str(t) for t in a] for a in Tq],
                  'forbidden', sorted(Fb)); break
