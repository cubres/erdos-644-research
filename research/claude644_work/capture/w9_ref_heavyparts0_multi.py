"""RECONSTRUCTED 24 Sep by the heavyparts#0 BREAK-IT referee session: the original file of this name (written by
the LINE-BY-LINE referee session) was accidentally overwritten by a same-named file of the BRK session (now at
w9_ref_heavyparts0brk_multi.py).  This reconstruction re-verifies EXACTLY the counterexample recorded in
notes_referee_w9.md [heavyparts#0, LINE-BY-LINE] to the multi-type lift 'Fano-free iff EVERY representative
triple conflicts':  x=(46,45,48), A-types a1=(33,0,27), a2=(46,0,14), B=(16,38,6), C=(2,15,43) (all sum 60,
rank-normalised by 60).  Independent code (primal Fano form: rows on points, constraints on lines)."""
import itertools
from fractions import Fraction as Fr
from w9_ref_heavyparts0brk_arccsp import LINES, minimal_hitting
import w9_ref_heavyparts0brk_random as R
MH = [set(F) for F in minimal_hitting()]
S = 60
x = [Fr(v, S) for v in (46, 45, 48)]
a1, a2, b, c = ([Fr(v, S) for v in t] for t in ((33, 0, 27), (46, 0, 14), (16, 38, 6), (2, 15, 43)))
T = [a1, a2, b, c]
assert all(sum(t) == 1 and all(0 <= t[i] <= x[i] for i in range(3)) for t in T)
print('super-heavy at own part:', [3*t[i] > 2*x[i] for t, i in ((a1, 0), (a2, 0), (b, 1), (c, 2))])
for name, a in (('a1', a1), ('a2', a2)):
    Fb = R.forbidden(x, [a, b, c])
    print(name, 'rep triple forbidden', sorted(Fb), 'conflict:', any(F <= Fb for F in MH), ' Fano(one type/class):', R.feas(x, [a, b, c]))
def feas(x, T):
    for asg in itertools.product(range(len(T)), repeat=7):
        if all(max(T[j][i] for j in asg) <= x[i] and sum(T[j][i] for j in asg) <= 4*x[i] and
               all(sum(T[asg[q]][i] for q in L) <= 2*x[i] for L in LINES) for i in range(3)):
            return asg
    return None
asg = feas(x, T)
print('mixed Fano tuple (rows on points 0..6, 0=a1,1=a2,2=b,3=c):', asg)
if asg:
    print('  totals', [sum(T[j][i] for j in asg)*S for i in range(3)], 'vs 4x', [4*x[i]*S for i in range(3)])
print('tau* =', R.tau_star(x, T))
