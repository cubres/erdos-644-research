"""Referee heavyparts#2 (LINE-BY-LINE lens), follow-up logic checks.  Exact strict FM (reused from
w9_ref_heavyparts2_fm.py, whose FM routine was re-read line by line) + an independent HiGHS max-slack LP
cross-check of every FM verdict, + exact rational witnesses.
 (i)   Lt (b_A<=4x_A/7, a_B<=4x_B/7) is DERIVABLE from H1,H2,G,sums (no boxes needed).
 (ii)  main claim with Lt AND all box constraints dropped.
 (iii) the CLAIM-text proof of the V facet 5b_B/4+a_B/2<=x_B from 'the symmetric bound' x_B>1/2+b_B/2+a_B alone
       is insufficient (explicit witness), while x_B>1/4+b_B+a_B/2 (G+R1+sum) suffices.
 (iv)  light part: with a,b<=4x/7 only the facet a+b<=x of V can fail (witness), all Q facets and 5b/4+a/2 hold.
"""
import itertools, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'w9_ref_heavyparts2_fm.py')).read().split("out = []")[0])
from scipy.optimize import linprog

def lp_slack(rows):
    """max eps s.t. coef.v + eps*[strict] <= rhs, vars >= 0 (bounded).  >0 => strict system feasible."""
    A = [[float(c.get(v, 0)) for v in V] + [1.0 if st else 0.0] for c, r, st in rows]
    b = [float(r) for c, r, st in rows]
    res = linprog([0]*len(V) + [-1], A_ub=A, b_ub=b, bounds=[(0, 10)]*len(V) + [(0, 1)], method='highs')
    return None if res.status != 0 else res.x[-1]

def both(rows):
    f = fm(rows); s = lp_slack(rows)
    lpf = s is not None and s > 1e-9
    return f, lpf

def check_exact(pt, rows):
    val = lambda c: sum(c.get(v, 0)*pt[v] for v in V)
    return all(val(c) < r if st else val(c) <= r for c, r, st in rows)

out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

NOBOX = ('boxA', 'boxB', 'boxA2', 'boxB2')
base = hyps(drop=('LtA', 'LtB') + NOBOX)
# (i)
for name, f in [('LtA', sub(L(bA=7), L(xA=4))), ('LtB', sub(L(aB=7), L(xB=4)))]:
    P('(i) negation of', name, 'with H1,H2,G,sums, no Lt, no boxes: (FM feasible, LP feasible) =', both(base + [ge(f, 0, True)]))
# (ii)
mism = 0; feas = []
for qa, qb, vb in itertools.product(QA, QB, VB):
    rows = base + [neg(*QA[qa]), neg(*QB[qb]), neg(*VB[vb])]
    f, l = both(rows)
    if f != l: mism += 1
    if f or l: feas.append((qa, qb, vb))
P('(ii) main claim without Lt and without boxes: feasible combos', feas, ' FM/LP mismatches', mism)
# also sub-claims without Lt/boxes
P('     Q_alpha facets that can fail:', [k for k in QA if fm(base + [neg(*QA[k])])],
  ' Q_beta:', [k for k in QB if fm(base + [neg(*QB[k])])])
# (iii) condensed-proof gap: R1, R2, heavy, sums, 'symmetric bound' x_B > 1/2 + b_B/2 + a_B, violate V facet B2; no G
R1 = neg(*QA['A1']); R2 = neg(*QB['B1'])
symB = ge(L(xB=1, bB=F(-1, 2), aB=-1), F(1, 2), True)
rows = hyps(drop=('G',)) + [R1, R2, symB, neg(*VB['B2'])]
P('(iii) R1,R2,H,Lt,sums + x_B>1/2+b_B/2+a_B + NOT(5b_B/4+a_B/2<=x_B), G dropped: (FM, LP) =', both(rows))
pt = {'xA': F(1), 'aA': F(1), 'bA': F(0), 'aB': F(0), 'bB': F(1), 'xB': F(9, 8)}
P('      witness', {k: str(v) for k, v in pt.items()}, 'exact check:', check_exact(pt, rows),
  ' (5b_B/4+a_B/2 =', F(5, 4), '> x_B =', pt['xB'], ')')
P('      same witness satisfies G?', check_exact(pt, [hyps()[-1]]), '(G: (xA-aA)+(xB-bB) =', pt['xA']-pt['aA']+pt['xB']-pt['bB'], ')')
bndB = ge(L(xB=1, bB=-1, aB=F(-1, 2)), F(1, 4), True)   # x_B > 1/4 + b_B + a_B/2
notbnd = le(L(xB=1, bB=-1, aB=F(-1, 2)), F(1, 4))          # x_B <= 1/4 + b_B + a_B/2
P('     bound x_B>1/4+b_B+a_B/2 implied by G+R1+sums (no Lt, no boxes)?', not fm(base + [R1, notbnd]))
P('     that bound + b_B<=1 kills the B2 violation?', not fm([bndB, le(L(bB=1), 1), neg(*VB['B2'])] + [ge(L(**{v: 1}), 0) for v in V]))
# (iv) light part, one variable set (x,a,b) reused through (xA,aA,bA)
lt = [ge(L(xA=1), 0), ge(L(aA=1), 0), ge(L(bA=1), 0), le(sub(L(aA=7), L(xA=4))), le(sub(L(bA=7), L(xA=4)))]
facets = {'Q_a 3a<=2x': QA['A1'], 'Q_a 3a+4b<=4x': QA['A2'], 'Q_b 3b<=2x': QB['A1'], 'Q_b 3b+4a<=4x': QB['A2'],
          'V a+b<=x': VB['A1'], 'V 5b/4+a/2<=x': VB['A2']}
P('(iv) light-part facets that can fail (a,b<=4x/7):', [k for k, f in facets.items() if fm(lt + [neg(*f)])])
P('     witness x=1,a=b=4/7 violates a+b<=x:', F(8, 7) > 1)
open(os.path.join(HERE, 'w9_ref_heavyparts2_logic.log'), 'w').write('\n'.join(out) + '\n')
