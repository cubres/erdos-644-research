"""Where do the stages fail at budget t with formula lemmas (fast) and exact static4 (MILP)?"""
import sys, numpy as np
sys.path.insert(0, '../explore')
from lemmas import split, asym1, asym2, four, sym, s0, g0, g1, g2, nc
from cells import triple_config, cover
t = float(sys.argv[1]) if len(sys.argv) > 1 else 0.855
A = 3 - 3*t; B = (4*t-2)/3; C = t - 0.5; D = 2 - t - 2*B; L = D - 1e-6
print('t=%.4f  A=3-3t=%.4f  B=%.4f  C=t-1/2=%.4f  D=%.4f  t/2=%.4f  4t-3=%.4f  1-t=%.4f' % (t, A, B, C, D, t/2, 4*t-3, 1-t))
def closes_formula(x, y, z, gaps=(), dich=None):
    if min(f(x, y, z) for f in (split, asym1, asym2, four, sym, s0)) <= t + 1e-9: return True
    for lo, hi in gaps:
        if g0(x, y, z, lo, hi) <= t + 1e-9 or g1(x, y, z, lo, hi, t) or g2(x, y, z, lo, hi, t): return True
    if dich is not None:
        if nc(x, y, z, dich, t) or g0(x, y, z, dich, 0.5) <= t+1e-9 or g1(x, y, z, dich, 0.5, t) or g2(x, y, z, dich, 0.5, t): return True
    return False
def scan(name, xs, capf, N=9, gaps=(), dichf=None, static=False):
    bad = []; worst_static = (0, None)
    for x in xs:
        cap = capf(x)
        for y in np.linspace(0, cap, N):
            for zz in np.linspace(0, y, N):
                ok = closes_formula(x, y, zz, gaps, dichf(x) if dichf else None)
                if not ok:
                    bad.append((round(x,4), round(y,4), round(zz,4)))
                    if static:
                        v = cover(triple_config(x, y, zz), 7, 4)
                        if v > worst_static[0]: worst_static = (v, (round(x,4), round(y,4), round(zz,4)))
    print('%-45s formula-uncovered %4d/%d  %s' % (name, len(bad), len(xs)*N*(N+1)//2, ('worst static4 among them %.4f at %s' % worst_static) if static else ''), flush=True)
    if bad: print('     examples:', bad[:4], '...', bad[-2:])
# Stage 1 as designed: q in (A,B], caps C
scan('Stage1 q in (A,B], caps C (no gap)', np.linspace(A+1e-4, B, 8), lambda q: C, static=True)
# Stage 1 extended down to t/2: caps (2-t-q)/2
scan('Stage1 ext q in (t/2,A], caps (2-t-q)/2', np.linspace(t/2+1e-4, A, 6), lambda q: (2-t-q)/2, static=True)
# Stage 2: x in [D,C], y,z <= A, gap (A,B]
scan('Stage2 x in [D,C], y,z<=A, gap(A,B]', np.linspace(D, C, 8), lambda q: A, gaps=((A, B),), static=True)
scan('Stage2 restricted y,z<=4t-3', np.linspace(D, C, 8), lambda q: 4*t-3, gaps=((A, B),))
# Stage 3: x in (B,1/2], y,z <= L, gaps (A,B],(L,C]
scan('Stage3 x in (B,1/2], y,z<=L, gaps', np.linspace(B+1e-4, 0.5, 8), lambda q: L, gaps=((A, B), (L, C)), static=True)
# Finisher: M in (1-t.., t/2], y,z <= min(M, 1-(t+M)/2), dichotomy (M,1/2]
scan('Finisher M in (2/7,t/2], caps min(M,1-(t+M)/2)', np.linspace(2/7+1e-4, t/2, 8), lambda M: min(M, 1-(t+M)/2), dichf=lambda M: M, static=True)
scan('Finisher ext M in (t/2,A], caps min(M,1-(t+M)/2)', np.linspace(t/2+1e-4, A, 6), lambda M: min(M, 1-(t+M)/2), dichf=lambda M: M, static=True)
