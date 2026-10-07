#!/usr/bin/env python3
"""Referee w9 [templates#0]: COMPLETE exact certificate for the Gap-Pair Lemma (independent of the attacker's
identities): for every choice of a failing facet of Q_b, Q_a, V(a,b) (4*4*4 = 64 systems) the system
   x>0, y>0, 0<=a<=b<=1, 4y<7(1-a), 4x<7b, b-a <= x+y-7/4, + three strict failures
is infeasible (exact Fourier-Motzkin with strict inequalities).
Sensitivity: dropping each hypothesis in turn, report whether a counterexample system becomes feasible.
Also checks the variant with G non-strict vs strict, and without a<=b."""
import itertools, sys
from fractions import Fraction as F
from w9_ref_templates0_fm import fm_feasible, le, lt
V = ['x', 'y', 'a', 'b']
def L(**kw):
    return {k: F(v) for k, v in kw.items()}
# failure facets: expression e > cap  <=>  cap - e < 0 ; build as  (e - cap) > 0 <=> -(e-cap) < 0
def fail(expr_coef, const):
    # expr: sum coef*v + const > 0   <=>  -sum coef*v < const
    return lt({k: -v for k, v in expr_coef.items()}, F(const))
# Q_b(s,t)=max(3t/2, s+3t/4), s=a-load, t=b-load. part1 loads (a,b), part2 loads (1-a,1-b)
Qb = [fail(L(b=F(3, 2), x=-1), 0),                    # 3b/2 > x
      fail(L(a=1, b=F(3, 4), x=-1), 0),               # a+3b/4 > x
      fail(L(b=F(-3, 2), y=-1), F(3, 2)),             # 3(1-b)/2 > y
      fail(L(a=-1, b=F(-3, 4), y=-1), F(7, 4))]       # (1-a)+3(1-b)/4 > y
Qa = [fail(L(a=F(3, 2), x=-1), 0),
      fail(L(b=1, a=F(3, 4), x=-1), 0),
      fail(L(a=F(-3, 2), y=-1), F(3, 2)),
      fail(L(b=-1, a=F(-3, 4), y=-1), F(7, 4))]
Vt = [fail(L(a=1, b=1, x=-1), 0),
      fail(L(a=F(5, 4), b=F(1, 2), x=-1), 0),
      fail(L(a=-1, b=-1, y=-1), 2),
      fail(L(a=F(-5, 4), b=F(-1, 2), y=-1), F(7, 4))]
hyp = {
    'x>0': lt(L(x=-1), 0), 'y>0': lt(L(y=-1), 0),
    'a>=0': le(L(a=-1), 0), 'a<=b': le(L(a=1, b=-1), 0), 'b<=1': le(L(b=1), 1),
    'H1': lt(L(y=4, a=7), 7),            # 4y < 7 - 7a
    'H2': lt(L(x=4, b=-7), 0),           # 4x < 7b
    'G': le(L(b=1, a=-1, x=-1, y=-1), F(-7, 4)),   # b-a-x-y <= -7/4
}
def run(h):
    feas = []
    for f1, f2, f3 in itertools.product(Qb, Qa, Vt):
        if fm_feasible(list(h.values()) + [f1, f2, f3], V):
            feas.append((Qb.index(f1), Qa.index(f2), Vt.index(f3)))
    return feas
res = run(hyp)
print("Gap-Pair full hypotheses: feasible failure systems:", res)
assert res == []
print("GAP-PAIR: all 64 failure systems infeasible (exact).  CERTIFICATE")
for k in hyp:
    h2 = dict(hyp); del h2[k]
    r = run(h2)
    print(f"  drop {k:5s}: {len(r)} feasible failure systems", r[:3])
# G strict irrelevant (already non-strict). Check G with slack: b-a <= x+y-7/4 + eps fails?
h3 = dict(hyp); h3['G'] = le(L(b=1, a=-1, x=-1, y=-1), F(-7, 4) + F(1, 1000))
print("  G weakened by 1/1000:", len(run(h3)), "feasible systems")
