"""Referee heavyparts#2: exact STRICT Fourier-Motzkin audit of the Pair Chain Lemma.
Variables xA,xB,aA,aB,bA,bB (alpha=a, beta=b; light-part coordinates enter only via aA+aB<=1, bA+bB<=1 because
light-part facets hold by the per-part argument -- checked separately in e2e).  Facets (exact covers from
w9_ref_heavyparts2_supports.py):  Q_a part i: 3a_i<=2x_i, 3a_i+4b_i<=4x_i;  Q_b mirror;
V(b,a) (5 b-rows): b_i+a_i<=x_i, 5b_i/4+a_i/2<=x_i.
Checks: (1) main claim: 64 facet-violation combos all infeasible; (2) 'Q_a fails only via 3aA>2xA';
(3) 'Q_b only via 3bB>2xB'; (4) variants: G non-strict, heavy non-strict, drop each hypothesis (necessity probes)."""
from fractions import Fraction as F
import itertools, sys
V = ['xA','xB','aA','aB','bA','bB']
def L(**kw):  # linear form dict
    return {k: F(v) for k, v in kw.items()}
def le(f, c=0, strict=False): return (dict(f), F(c), strict)            # f <= c
def ge(f, c=0, strict=False): return ({k: -v for k, v in f.items()}, -F(c), strict)  # f >= c
def sub(f, g): 
    h = dict(f)
    for k, v in g.items(): h[k] = h.get(k, 0) - v
    return h
def fm(rows):
    def norm(rs):
        best = {}
        for coef, rhs, st in rs:
            nz = {k: v for k, v in coef.items() if v != 0}
            if not nz:
                if rhs < 0 or (st and rhs == 0): return None
                continue
            m = max(abs(v) for v in nz.values())
            key = tuple(sorted((k, v/m) for k, v in nz.items())); r = rhs/m
            if key not in best or r < best[key][1] or (r == best[key][1] and st and not best[key][2]):
                best[key] = ({k: v/m for k, v in nz.items()}, r, st)
        return list(best.values())
    rows = norm(rows)
    if rows is None: return False
    for s in V:
        pos = [r for r in rows if r[0].get(s, 0) > 0]; neg = [r for r in rows if r[0].get(s, 0) < 0]
        new = [r for r in rows if r[0].get(s, 0) == 0]
        for cp, rp, sp in pos:
            for cn, rn, sn in neg:
                a, b = cp[s], -cn[s]
                coef = {k: cp.get(k, 0)*b + cn.get(k, 0)*a for k in set(cp) | set(cn)}; coef[s] = 0
                new.append((coef, rp*b + rn*a, sp or sn))
        rows = norm(new)
        if rows is None: return False
    return True

def hyps(Gstrict=True, Hstrict=True, drop=()):
    H = {}
    for v in V: H['nn_'+v] = ge(L(**{v: 1}), 0)
    H['boxA'] = le(sub(L(aA=1), L(xA=1))); H['boxB'] = le(sub(L(bB=1), L(xB=1)))  # rows <= capacity
    H['boxA2'] = le(sub(L(bA=1), L(xA=1))); H['boxB2'] = le(sub(L(aB=1), L(xB=1)))
    H['H2'] = ge(sub(L(aA=7), L(xA=4)), 0, Hstrict); H['H1'] = ge(sub(L(bB=7), L(xB=4)), 0, Hstrict)
    H['LtA'] = le(sub(L(bA=7), L(xA=4))); H['LtB'] = le(sub(L(aB=7), L(xB=4)))
    H['suma'] = le(L(aA=1, aB=1), 1); H['sumb'] = le(L(bA=1, bB=1), 1)
    H['G'] = ge(L(xA=1, aA=-1, xB=1, bB=-1), F(3, 4), Gstrict)
    return [v for k, v in H.items() if k not in drop]

def neg(f, c):  # violation of f <= c  : f > c
    return ge(f, c, True)
QA = {'A1': (L(aA=3, xA=-2), 0), 'A2': (L(aA=3, bA=4, xA=-4), 0), 'B1': (L(aB=3, xB=-2), 0), 'B2': (L(aB=3, bB=4, xB=-4), 0)}
QB = {'A1': (L(bA=3, xA=-2), 0), 'A2': (L(bA=3, aA=4, xA=-4), 0), 'B1': (L(bB=3, xB=-2), 0), 'B2': (L(bB=3, aB=4, xB=-4), 0)}
VB = {'A1': (L(aA=1, bA=1, xA=-1), 0), 'A2': (L(bA=F(5,4), aA=F(1,2), xA=-1), 0),
      'B1': (L(aB=1, bB=1, xB=-1), 0), 'B2': (L(bB=F(5,4), aB=F(1,2), xB=-1), 0)}

def main_claim(**kw):
    feas = []
    for qa, qb, vb in itertools.product(QA, QB, VB):
        rows = hyps(**kw) + [neg(*QA[qa]), neg(*QB[qb]), neg(*VB[vb])]
        if fm(rows): feas.append((qa, qb, vb))
    return feas
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
P('(1) main claim, G strict, heavy strict: feasible violation combos =', main_claim())
P('    G non-strict:', main_claim(Gstrict=False))
P('    G and heavy non-strict:', main_claim(Gstrict=False, Hstrict=False))
P('(2) Q_alpha facets that can fail under hypotheses:', [k for k in QA if fm(hyps() + [neg(*QA[k])])])
P('(3) Q_beta facets that can fail under hypotheses:', [k for k in QB if fm(hyps() + [neg(*QB[k])])])
P('    V(beta,alpha) facets that can fail under hypotheses alone:', [k for k in VB if fm(hyps() + [neg(*VB[k])])])
P('(3b) V facets failing when R1 and R2 both hold:', [k for k in VB if fm(hyps() + [neg(*QA['A1']), neg(*QB['B1']), neg(*VB[k])])])
P('(4) necessity probes (drop one hypothesis; nonempty list = claim fails without it):')
for d in ['H2', 'H1', 'LtA', 'LtB', 'suma', 'sumb', 'G', 'boxA', 'boxB', 'boxA2', 'boxB2']:
    P('   drop', d, '->', main_claim(drop=(d,))[:4])
# weaker Lt used in the proof: bA<=aA, aB<=2xB/3 (and mirror)
def weakLt():
    H = hyps(drop=('LtA', 'LtB'))
    return H + [le(sub(L(bA=1), L(aA=1))), le(sub(L(aB=3), L(xB=2))), le(sub(L(aB=1), L(bB=1))), le(sub(L(bA=3), L(xA=2)))]
feas = [c for c in itertools.product(QA, QB, VB) if fm(weakLt() + [neg(*QA[c[0]]), neg(*QB[c[1]]), neg(*VB[c[2]])])]
P('(5) weak Lt (bA<=aA, aB<=bB, aB<=2xB/3, bA<=2xA/3):', feas)
open(__file__.replace('.py', '.log'), 'w').write('\n'.join(out) + '\n')
