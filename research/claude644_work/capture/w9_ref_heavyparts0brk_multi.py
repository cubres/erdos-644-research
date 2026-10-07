"""Referee w9, heavyparts#0, part D (exact).
(a) H3s counterexample: recompute the forbidden patterns / conflict type with independent code.
(b) The notes' extension 'Fano-free (pencil level) iff EVERY choice of representatives shows a conflict'
    for classes with SEVERAL types: search for families where every representative triple has a
    mutual/cyclic conflict but a MIXED-row assignment is pencil- (and fully) feasible.
usage: python3 w9_ref_heavyparts0brk_multi.py SEED N"""
import sys, random, itertools
from fractions import Fraction as Fr
from w9_ref_heavyparts0brk_arccsp import LINES, minimal_hitting
import w9_ref_heavyparts0brk_random as R
MH = [set(F) for F in minimal_hitting()]
def feas_multi(x, T, totals):
    p = len(x)
    for asg in itertools.product(range(len(T)), repeat=7):
        ok = True
        for i in range(p):
            z = [T[c][i] for c in asg]
            if max(z) > x[i] or (totals and sum(z) > 4*x[i]) or any(sum(z[q] for q in L) > 2*x[i] for L in LINES):
                ok = False; break
        if ok: return asg
    return None
if __name__ == '__main__':
    x = [Fr(861, 1000), Fr(1440, 1000), Fr(741, 1000)]
    T = [[Fr(664, 1000), Fr(0), Fr(336, 1000)], [Fr(19, 1000), Fr(981, 1000), Fr(0)], [Fr(424, 1000), Fr(0), Fr(576, 1000)]]
    Fb = R.forbidden(x, T)
    print('H3s-cex forbidden:', sorted(Fb), ' minimal conflicts contained:', [sorted(F) for F in MH if F <= Fb],
          ' super-heavy:', [3*T[c][c] > 2*x[c] for c in range(3)], ' tau*=', R.tau_star(x, T),
          ' Fano:', R.feas(x, T))
    seed, N = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
    found = 0
    for it in range(N):
        x, T3 = R.rand_family(rng, 3)
        # second A-type: resample
        x2, T3b = R.rand_family(rng, 3)
        a2 = T3b[0]
        if not (3*a2[0] > 2*x[0] and all(a2[i] <= x[i] for i in range(3))): continue
        T = [T3[0], a2, T3[1], T3[2]]    # classes A,A,B,C
        allconf = all(any(F <= R.forbidden(x, [a, T3[1], T3[2]]) for F in MH) for a in (T3[0], a2))
        if not allconf: continue
        pen = feas_multi(x, T, totals=False)
        if pen is not None:
            full = feas_multi(x, T, totals=True)
            found += 1
            if found <= 3:
                print('MIXED-FEASIBLE despite all representative conflicts: x', [str(v) for v in x],
                      'types(A1,A2,B,C)', [[str(v) for v in a] for a in T], 'pencil asg', pen, 'full asg', full,
                      'forb(A1)', sorted(R.forbidden(x, [T3[0], T3[1], T3[2]])), 'forb(A2)', sorted(R.forbidden(x, [a2, T3[1], T3[2]])),
                      'tau*', float(R.tau_star(x, T)), flush=True)
    print('found', found)
