"""REFEREE (w12): LP checks of every HAND chain in bal3/THEOREM_3T_balanced_proof.md, each with ONLY the facts
the text names (plus the always-available structural facts: ranges, row sums, Lemma 0, tau>3/4, balance).
A chain is confirmed iff the named system is infeasible (max strict slack <= 0)."""
import sys, itertools
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/referee_w12')
from ref_step3_lp import FACTS, row, add, e, tv, lp_slack, P, F
STRUCT = {k: v for k, v in FACTS.items() if not (k.startswith('id') or '@' in k)}   # no id map, no pattern facts
ID = FACTS['id: tau<=eA+eB+eC']
def pm(Y, X):   # pair map P(Y->X): tau <= x_X - y_X + e_Z  (valid iff y_X > 0; caller adds y_X > 0)
    Z = 3 - X - Y; y = tv(Y, X)
    return row(add({'tau': 1, 'x' + P[X]: -1, y: 1}, e(P[Z], -1)), 0)
def allat(X, which):  # ALL@X alternative: trace 'which' <= x_X - tau
    return row({which: 1, 'x' + P[X]: -1, 'tau': 1}, 0)
def gt(d, rhs): return row({k: -v for k, v in d.items()}, -F(rhs), True)   # d.z > rhs
def dfail(X, Y): return gt(add({tv(Y, X): 1}, e(P[X], -2)), 0)             # XXY fails at X: y_X > 2e_X
def sfail(X, Y): return gt(add({tv(X, Y): 1}, e(P[Y], -1), {'s' + P[Y]: F(-1, 2)}), 0)  # at Y: t^X_Y > e_Y+s_Y/2
def run(name, rows, expect_infeasible=True):
    t = lp_slack(list(STRUCT.values()) + rows)
    ok = (t <= 1e-9) == expect_infeasible
    print(('OK   ' if ok else 'FAIL ') + name + f'   [max strict slack {t:.4g}]')
    return ok
A, B, C = 0, 1, 2
print('--- step (a) cyclic conflict {AAB,BBC,CCA}: hand needs only id map + cross-mass (i.e. id) ---')
for modes in itertools.product([0, 1], repeat=3):
    rows = [ID] + [dfail(X, Y) if m == 0 else sfail(X, Y) for (X, Y), m in zip([(A, B), (B, C), (C, A)], modes)]
    # ddd (0,0,0) additionally needs the three pair maps P(B->A), P(C->B), P(A->C); (validity: b_A>2e_A>=0 etc.)
    if modes == (0, 0, 0): rows += [pm(B, A), pm(C, B), pm(A, C)]
    run(f'(a) modes {modes}', rows)
print('--- step (b): M1/M2 => V(gamma,alpha) ---')
M1 = [dfail(A, B), dfail(B, A)]          # b_A > 2e_A, a_B > 2e_B
M2 = [sfail(A, B)]                       # a_B > e_B + s_B/2
cA_gt_eA = gt(add({'cA': 1}, e('A', -1)), 0)
# part C conclusion: a_C <= 2e_C - s_C/2 from id only
negC = gt(add({'aC': 1}, e('C', -2), {'sC': F(1, 2)}), 0)
run('(b)(C) M1: id => aC<=2eC-sC/2', [ID] + M1 + [negC])
run('(b)(C) M2: id => aC<=2eC-sC/2', [ID] + M2 + [negC])
negB = gt({'aB': 1, 'cB': 1, 'xB': -1}, 0)
run('(b)(B) M1: id + P(A->B) => aB+cB<=xB', [ID, pm(A, B)] + M1 + [negB])
run('(b)(B) M2: id + P(A->B) => aB+cB<=xB', [ID, pm(A, B)] + M2 + [negB])
run('(b)(A) M2: id + P(C->A) + P(A->B) => cA<=eA', [ID, pm(C, A), pm(A, B)] + M2 + [cA_gt_eA])
run('(b)(A) M1, branch bA<=xA-tau: id + ALL@A(bA) => cA<=eA', [ID, allat(A, 'bA')] + M1 + [cA_gt_eA])
run('(b)(A) M1, branch cA<=xA-tau: id + ALL@A(cA) + P(A->B)  [AS WRITTEN]', [ID, allat(A, 'cA'), pm(A, B)] + M1 + [cA_gt_eA])
print('   ... same branch with more maps available:')
run('(b)(A) M1, cA<=xA-tau: + P(B->A)', [ID, allat(A, 'cA'), pm(A, B), pm(B, A)] + M1 + [cA_gt_eA])
run('(b)(A) M1, cA<=xA-tau: + P(C->A)', [ID, allat(A, 'cA'), pm(A, B), pm(C, A)] + M1 + [cA_gt_eA])
run('(b)(A) M1, cA<=xA-tau: + P(C->B)', [ID, allat(A, 'cA'), pm(A, B), pm(C, B)] + M1 + [cA_gt_eA])
run('(b)(A) M1, cA<=xA-tau: + all six pair maps', [ID, allat(A, 'cA')] + [pm(Y, X) for Y in range(3) for X in range(3) if X != Y] + M1 + [cA_gt_eA])
run('(b)(A) M1, cA<=xA-tau: + P(A->C) only', [ID, allat(A, 'cA'), pm(A, B), pm(A, C)] + M1 + [cA_gt_eA])
run('(b)(A) M1, cA<=xA-tau: + P(B->C) only', [ID, allat(A, 'cA'), pm(A, B), pm(B, C)] + M1 + [cA_gt_eA])
print('--- step 3 (TC) ---')
TCf = gt({'aC': 4, 'bC': 2, 'sC': 1, 'xC': -4}, 0)
run('(TC) aC=0', [ID, TCf, row({'aC': 1}, 0)])
run('(TC) aC>0: P(A->C)', [TCf, pm(A, C)])
print('--- Lemma 0 / cross-mass sanity ---')
run('cross-mass alpha from id', [ID, gt(add({'aB': 1, 'aC': 1}, e('B', -2), e('C', -2)), F(-1, 2))])
