"""Referee w9, heavyparts#0, part C: adversarial climb for TOTALS-KILLED families
(one type per class, super-heavy at own part, NO mutual/cyclic conflict, yet NO Fano tuple because every
conflict-free cap colouring violates a per-part total).  Maximise tau* (float), then exact re-check.
usage: python3 w9_ref_heavyparts0brk_climb.py SEED ITERS [extra_parts]"""
import sys, random, itertools, math
from fractions import Fraction as Fr
from w9_ref_heavyparts0brk_arccsp import PATSETS, minimal_hitting
import w9_ref_heavyparts0brk_random as R
MH = minimal_hitting()
PS = [(ps, n) for ps, cnts in PATSETS.items() for n in cnts]
CL = 'ABC'
def pslack(x, T, P):
    cs = [CL.index(ch) for ch in P]
    return min((2*x[i] - sum(T[c][i] for c in cs))/x[i] for i in range(len(x)))
def margins(x, T):
    sl = {P: pslack(x, T, P) for P in ['AAB','AAC','ABB','BBC','ACC','BCC','ABC']}
    g1 = min(max(sl[P] for P in F) for F in MH)              # >=0 : no conflict
    g2 = max(min(min(sl[P] for P in ps), min((4*x[i]-sum(n[c]*T[c][i] for c in range(3)))/x[i]
             for i in range(len(x)))) for ps, n in PS)       # <0 : Fano-free
    sh = min((T[c][c] - 2*x[c]/3)/x[c] for c in range(3))   # >0 : super-heavy
    return g1, g2, sh
def tau_f(x, T):
    p = len(x); best = 1e9
    for pi in itertools.product(*[[i for i in range(p) if a[i] > 0] for a in T]):   # FIX: positive traces only
        t = [0.0]*p
        for a, i in zip(T, pi): t[i] = max(t[i], x[i]-a[i])
        best = min(best, sum(t))
    return best
def decode(v, p):
    x = [0.05 + abs(v[i]) for i in range(p)]
    T = []
    for c in range(3):
        w = [abs(v[p + c*p + i]) + 1e-9 for i in range(p)]
        s = sum(w); a = [wi/s for wi in w]
        T.append(a)
    return x, T
def score(v, p):
    x, T = decode(v, p)
    pen = sum(max(0, T[c][i]-x[i]) for c in range(3) for i in range(p))
    g1, g2, sh = margins(x, T)
    pen += max(0, -g1) + max(0, g2 + 1e-4) + max(0, 1e-4 - sh)
    return tau_f(x, T) - 10*pen, (x, T, g1, g2, sh)
if __name__ == '__main__':
    seed, iters = int(sys.argv[1]), int(sys.argv[2]); extra = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = random.Random(seed); p = 3 + extra
    best_all = None
    for restart in range(8):
        v = [rng.uniform(0.3, 1.5) for _ in range(p)] + [rng.random() for _ in range(3*p)]
        for c in range(3): v[p + c*p + c] += 2
        s, info = score(v, p); step = 0.2
        for it in range(iters):
            w = [vi + rng.gauss(0, step) if rng.random() < 0.4 else vi for vi in v]
            s2, info2 = score(w, p)
            if s2 >= s: v, s, info = w, s2, info2
            if it % 2000 == 1999: step = max(step*0.7, 1e-4)
        x, T, g1, g2, sh = info
        print('restart', restart, 'score %.5f tau* %.5f g1 %.4f g2 %.4f sh %.4f' % (s, tau_f(x, T), g1, g2, sh),
              'x', [round(t, 4) for t in x], 'T', [[round(t, 4) for t in a] for a in T], flush=True)
        if best_all is None or s > best_all[0]: best_all = (s, x, T)
    s, x, T = best_all
    # exact re-check of best on a rational rounding
    xq = [Fr(round(t*2000), 2000) for t in x]
    Tq = []
    for a in T:
        aq = [Fr(round(t*2000), 2000) for t in a]; aq[max(range(p), key=lambda i: aq[i])] += 1 - sum(aq); Tq.append(aq)
    Fb = R.forbidden(xq, Tq)
    conf = any(set(F) <= Fb for F in MH)
    full = R.feas(xq, Tq) is not None
    sup = all(3*Tq[c][c] > 2*xq[c] for c in range(3)) and all(0 <= Tq[c][i] <= xq[i] for c in range(3) for i in range(p))
    print('EXACT best: tau*=%s (%.5f) conflict=%s fano=%s superheavy&admissible=%s' % (R.tau_star(xq, Tq),
          float(R.tau_star(xq, Tq)), conf, full, sup))
    print('  x', [str(t) for t in xq], 'T', [[str(t) for t in a] for a in Tq], 'forbidden', sorted(Fb))
