"""heavyparts#2 end-to-end exact test of PCL on random rational multi-part instances.
Templates evaluated by EXACT cover functions (dual vertices from w9_ref_heavyparts2_supports.pkl), NOT by the
claimed formulas: Q_alpha = alpha on the 3 rows of a line (dual of a pencil), beta on the other 4;
V(beta,alpha) = beta on rows 2..6, alpha on rows 0,1 of the fn38 support.
Modes: 'gen' (hypotheses only), 'rr' (force R1 & R2: the V branch), 'lightfree' (drop a_j+b_j<=x_j at light parts,
to test 'only V facet failing at a light part is a+b<=x').  Usage: python3 ... mode seed N"""
import pickle, random, sys
from fractions import Fraction as F
D = pickle.load(open('w9_ref_heavyparts2_supports.pkl', 'rb'))
FV, VV = D['FV'], D['VV']
LINE0 = (0, 1, 2)
def cover(Vs, z): return max(sum(a*b for a, b in zip(v, z)) for v in Vs)
def Q_ok(x, a, b):  # a on a line, b elsewhere
    return all(cover(FV, [a[i] if r in LINE0 else b[i] for r in range(7)]) <= x[i] for i in range(len(x)))
def V_ok(x, b5, a2, parts=None):
    parts = range(len(x)) if parts is None else parts
    return all(cover(VV, [a2[i] if r < 2 else b5[i] for r in range(7)]) <= x[i] for i in parts)
mode, seed, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed); D_ = 240
def rq(lo, hi):  # random rational in [lo,hi]
    if hi < lo: return None
    k = rng.randint(0, D_); return lo + (hi - lo)*F(k, D_)
stats = dict(tried=0, inst=0, QA=0, QB=0, V=0, none=0, qa_fail_notR1=0, qb_fail_notR2=0, light_bad=0, light_Vfail=0)
while stats['inst'] < N:
    stats['tried'] += 1
    p = rng.randint(2, 5)
    x = [rq(F(1, 10), F(3, 2)) for _ in range(p)]
    if mode == 'rr':
        x[0] = rq(F(3, 4), F(3, 2)); x[1] = rq(F(3, 4), F(3, 2))
    a = [F(0)]*p; b = [F(0)]*p
    lo = 4*x[0]/7 if mode != 'rr' else 2*x[0]/3
    a[0] = rq(lo, min(x[0], F(1)))
    if a[0] is None or a[0] <= 4*x[0]/7: continue
    lo = 4*x[1]/7 if mode != 'rr' else 2*x[1]/3
    b[1] = rq(lo, min(x[1], F(1)))
    if b[1] is None or b[1] <= 4*x[1]/7: continue
    ra, rb = 1 - a[0], 1 - b[1]
    b[0] = rq(F(0), min(4*x[0]/7, rb)); a[1] = rq(F(0), min(4*x[1]/7, ra))
    if b[0] is None or a[1] is None: continue
    ra -= a[1]; rb -= b[0]
    ok = True
    for j in range(2, p):
        a[j] = rq(F(0), min(4*x[j]/7, ra)); ra -= a[j]
        cap = min(4*x[j]/7, rb) if mode == 'lightfree' else min(4*x[j]/7, rb, x[j] - a[j])
        b[j] = rq(F(0), cap); rb -= b[j]
        if rng.random() < 0.3 and mode != 'lightfree':  # push to the a+b=x boundary when allowed
            t = min(4*x[j]/7, rb + b[j], x[j] - a[j]); rb += b[j] - t; b[j] = t
    if rng.random() < 0.5 and p > 2:  # optionally fill sums up to exactly 1 in a light part if room
        pass
    if (x[0] - a[0]) + (x[1] - b[1]) <= F(3, 4): continue
    stats['inst'] += 1
    qa, qb = Q_ok(x, a, b), Q_ok(x, b, a)
    R1, R2 = 3*a[0] > 2*x[0], 3*b[1] > 2*x[1]
    if not qa and not R1: stats['qa_fail_notR1'] += 1; print('QA fails without R1', x, a, b)
    if not qb and not R2: stats['qb_fail_notR2'] += 1; print('QB fails without R2', x, a, b)
    v = V_ok(x, b, a)
    for j in range(2, p):
        if not V_ok(x, b, a, [j]):
            stats['light_Vfail'] += 1
            if a[j] + b[j] <= x[j]: stats['light_bad'] += 1; print('light V facet other than a+b', x, a, b, j)
    if mode == 'lightfree':
        v = V_ok(x, b, a, [0, 1])   # the lemma's two-part conclusion
    if qa: stats['QA'] += 1
    elif qb: stats['QB'] += 1
    elif v: stats['V'] += 1
    else: stats['none'] += 1; print('NO TEMPLATE', x, a, b)
print(mode, seed, stats)
