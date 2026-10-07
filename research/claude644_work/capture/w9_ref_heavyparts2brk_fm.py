"""Referee w9 heavyparts#2 (BREAK-IT lens): independent exact strict Fourier-Motzkin for the Pair Chain Lemma.
Variables v = (xA, xB, aA, aB, bA, bB)  (alpha heavy at A, beta heavy at B).  Light parts decouple (checked by hand
and in section L below).  Constraint = (coef tuple, const, strict): coef.v + const > 0 (strict) or >= 0.
Every run prints the list of facet-failure combos that are FEASIBLE (a counterexample region) -- [] means proved.
"""
import itertools, sys
from fractions import Fraction as F

N = 6
XA, XB, AA, AB, BA, BB = range(6)
def lin(d, c=0, strict=False):
    v = [F(0)]*N
    for k, a in d.items(): v[k] = F(a)
    return (tuple(v), F(c), strict)

def fm_feasible(cons):
    cons = list(set(cons))
    for var in range(N):
        pos = [c for c in cons if c[0][var] > 0]; neg = [c for c in cons if c[0][var] < 0]
        rest = [c for c in cons if c[0][var] == 0]
        new = set(rest)
        for p in pos:
            for n in neg:
                lp, ln = -n[0][var], p[0][var]   # multiply p by -n_var, n by p_var
                co = tuple(lp*p[0][i] + ln*n[0][i] for i in range(N))
                cc = lp*p[1] + ln*n[1]
                st = p[2] or n[2]
                # normalise
                m = max([abs(a) for a in co] + [abs(cc)])
                if m == 0:
                    if st: return False
                    continue
                co = tuple(a/m for a in co); cc = cc/m
                if all(a == 0 for a in co):
                    if cc < 0 or (cc == 0 and st): return False
                    continue
                new.add((co, cc, st))
        cons = list(new)
        # prune: identical coef keep tightest
        best = {}
        for co, cc, st in cons:
            k = co
            if k not in best: best[k] = (cc, st)
            else:
                oc, os_ = best[k]
                if cc < oc or (cc == oc and st and not os_): best[k] = (cc, st)
        cons = [(k, v[0], v[1]) for k, v in best.items()]
    return all(not (cc < 0 or (cc == 0 and st)) for co, cc, st in cons)

def hyps(strictG=True, drop=(), light=F(4, 7)):
    H = {}
    for k in range(N): H['nn%d' % k] = lin({k: 1})
    H['H2'] = lin({AA: 7, XA: -4}, 0, True)          # 7 aA > 4 xA
    H['H1'] = lin({BB: 7, XB: -4}, 0, True)          # 7 bB > 4 xB
    H['LtA'] = lin({XA: light, BA: -1})              # bA <= light*xA
    H['LtB'] = lin({XB: light, AB: -1})              # aB <= light*xB
    H['suma'] = lin({AA: -1, AB: -1}, 1)
    H['sumb'] = lin({BA: -1, BB: -1}, 1)
    H['G'] = lin({XA: 1, AA: -1, XB: 1, BB: -1}, F(-3, 4), strictG)
    return [c for k, c in H.items() if k not in drop]

# failure facets (strict violations)
def fail(expr_d):  # expr > 0 strict
    return lin(expr_d, 0, True)
QA = {'QA:A 3a>2x': fail({AA: 3, XA: -2}), 'QA:A 3a+4b>4x': fail({AA: 3, BA: 4, XA: -4}),
      'QA:B 3a>2x': fail({AB: 3, XB: -2}), 'QA:B 3a+4b>4x': fail({AB: 3, BB: 4, XB: -4}),
      'QA:A a>x': fail({AA: 1, XA: -1}), 'QA:A b>x': fail({BA: 1, XA: -1}),
      'QA:B a>x': fail({AB: 1, XB: -1}), 'QA:B b>x': fail({BB: 1, XB: -1}),
      'QA:A a+2b>2x': fail({AA: 1, BA: 2, XA: -2}), 'QA:B a+2b>2x': fail({AB: 1, BB: 2, XB: -2})}
QB = {'QB:A 3b>2x': fail({BA: 3, XA: -2}), 'QB:A 3b+4a>4x': fail({BA: 3, AA: 4, XA: -4}),
      'QB:B 3b>2x': fail({BB: 3, XB: -2}), 'QB:B 3b+4a>4x': fail({BB: 3, AB: 4, XB: -4}),
      'QB:A a>x': fail({AA: 1, XA: -1}), 'QB:A b>x': fail({BA: 1, XA: -1}),
      'QB:B a>x': fail({AB: 1, XB: -1}), 'QB:B b>x': fail({BB: 1, XB: -1}),
      'QB:A b+2a>2x': fail({BA: 1, AA: 2, XA: -2}), 'QB:B b+2a>2x': fail({BB: 1, AB: 2, XB: -2})}
# V(beta,alpha): five beta rows, two alpha rows: max(b+a, 5b/4+a/2) <= x
VV = {'V:A a+b>x': fail({AA: 1, BA: 1, XA: -1}), 'V:A 5b/4+a/2>x': fail({BA: F(5, 4), AA: F(1, 2), XA: -1}),
      'V:B a+b>x': fail({AB: 1, BB: 1, XB: -1}), 'V:B 5b/4+a/2>x': fail({BB: F(5, 4), AB: F(1, 2), XB: -1})}
# V(alpha,beta) (five alpha rows) for the orientation question
VW = {'W:A a+b>x': fail({AA: 1, BA: 1, XA: -1}), 'W:A 5a/4+b/2>x': fail({AA: F(5, 4), BA: F(1, 2), XA: -1}),
      'W:B a+b>x': fail({AB: 1, BB: 1, XB: -1}), 'W:B 5a/4+b/2>x': fail({AB: F(5, 4), BB: F(1, 2), XB: -1})}

def combos(H, menus):
    out = []
    for choice in itertools.product(*[list(m.items()) for m in menus]):
        if fm_feasible(H + [c for _, c in choice]): out.append(tuple(k for k, _ in choice))
    return out

def single(H, menu):
    return [k for k, c in menu.items() if fm_feasible(H + [c])]

if __name__ == '__main__':
    # sanity: hypotheses alone feasible
    print('hyps feasible:', fm_feasible(hyps()))
    # positive control: FM detects an obviously feasible failure (drop G)
    print('control (drop G, QA/QB/V all fail somewhere):', len(combos(hyps(drop=('G',)), [QA, QB, VV])) > 0)
    print('(1) MAIN, G strict: feasible failure combos =', combos(hyps(), [QA, QB, VV]))
    print('    G non-strict:', combos(hyps(strictG=False), [QA, QB, VV]))
    print('(2) Q_alpha facets failable:', single(hyps(), QA))
    print('    Q_beta facets failable:', single(hyps(), QB))
    print('    V facets failable (no R assumption):', single(hyps(), VV))
    R1 = QA['QA:A 3a>2x']; R2 = QB['QB:B 3b>2x']
    print('(3) V facets failable under R1&R2:', single(hyps() + [R1, R2], VV))
    print('(4) drop Lt at A and B:', combos(hyps(drop=('LtA', 'LtB')), [QA, QB, VV]))
    # Lt redundancy directly: hyps without Lt + violation of Lt
    print('    LtA derivable? (hyps-Lt + bA>4xA/7 feasible):',
          fm_feasible(hyps(drop=('LtA', 'LtB')) + [fail({BA: 7, XA: -4})]))
    print('    LtB derivable? :', fm_feasible(hyps(drop=('LtA', 'LtB')) + [fail({AB: 7, XB: -4})]))
    print('    bA<=aA derivable w/o Lt? :', fm_feasible(hyps(drop=('LtA', 'LtB')) + [fail({BA: 1, AA: -1})]))
    for d in ['H1', 'H2', 'suma', 'sumb', 'G']:
        r = combos(hyps(drop=(d,)), [QA, QB, VV])
        print('    drop', d, '-> #feasible combos', len(r), r[:2])
    print('(5) orientation: menu QA,QB,V(alpha,beta):', combos(hyps(), [QA, QB, VW]))
    print('(6) sharpness of 3/4: G with 3/4 -> 3/4 - 1/1000:')
    H = hyps(); H = [c for c in H if not (c[1] == F(-3, 4))] + [lin({XA: 1, AA: -1, XB: 1, BB: -1}, F(-749, 1000), True)]
    print('    feasible failure combos:', combos(H, [QA, QB, VV])[:3])
    # L: light part j with 2/3-light + a+b<=x (weaker than claim's 4/7): all 3 templates fit at j
    xj, aj, bj = 0, 1, 2
    def L(d, c=0, s=False):
        v = [F(0)]*N
        for k, a in d.items(): v[k] = F(a)
        return (tuple(v), F(c), s)
    for thr, nm in [(F(4, 7), '4/7'), (F(2, 3), '2/3')]:
        Hj = [L({xj: 1}), L({aj: 1}), L({bj: 1}), L({xj: thr, aj: -1}), L({xj: thr, bj: -1}), L({xj: 1, aj: -1, bj: -1})]
        fac = {'3a>2x': L({aj: 3, xj: -2}, 0, True), '3a+4b>4x': L({aj: 3, bj: 4, xj: -4}, 0, True),
               '3b>2x': L({bj: 3, xj: -2}, 0, True), '3b+4a>4x': L({bj: 3, aj: 4, xj: -4}, 0, True),
               'a+b>x': L({aj: 1, bj: 1, xj: -1}, 0, True), '5b/4+a/2>x': L({bj: F(5, 4), aj: F(1, 2), xj: -1}, 0, True),
               '5a/4+b/2>x': L({aj: F(5, 4), bj: F(1, 2), xj: -1}, 0, True)}
        print('(L) light', nm, '+ a+b<=x: failable facets at j:', [k for k, c in fac.items() if fm_feasible(Hj + [c])])
        Hj2 = Hj[:5]
        print('(L) light', nm, 'WITHOUT a+b<=x: failable facets at j:', [k for k, c in fac.items() if fm_feasible(Hj2 + [c])])
