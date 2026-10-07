"""Referee w9 typeclosed#0: exact checks of the two templates used by Theorem L+ (no LP, hand masses).
(1) V support: no covering pair; explicit masses give loads >= (t,t,s^5) with total EXACTLY max(s+t,5s/4+t/2)
    on the rational grid s,t in {0,1/40,..,1}.
(2) Pencil: Fano cells, loads (e,e,e,f,f,f,f), total max(3e/2, f+3e/4); with e<=2x/3, f<=x-3e/4 total <= x.
(3) Literal realisation at integer scale for random rational instances (points, trimmed rows, all pattern pairs)."""
import random
from fractions import Fraction as F
from w9_ref_typeclosed0brk_lib import *

assert check_cells_noncovering(V_CELLS), 'V support covers'
assert check_cells_noncovering(FANO_CELLS)
# sanity: pencil rows 0..2 are the lines through point 0
assert all(0 in LINES[l] for l in range(3)) and all(0 not in LINES[l] for l in range(3, 7))

n = 0
for a in range(41):
    for b in range(41):
        s, t = F(a, 40), F(b, 40)
        m = V_masses(s, t)
        assert all(v >= 0 for v in m.values())
        loads = [sum(v for C, v in m.items() if r in C) for r in range(7)]
        assert all(loads[r] >= t for r in (0, 1)) and all(loads[r] >= s for r in range(2, 7)), (s, t, loads)
        assert sum(m.values()) == max(s + t, 5 * s / 4 + t / 2), (s, t)
        e, f = s, t
        pm = pencil_masses(e, f)
        loads = [sum(v for C, v in pm.items() if r in C) for r in range(7)]
        assert all(loads[r] >= e for r in range(3)) and all(loads[r] >= f for r in range(3, 7))
        assert sum(pm.values()) == max(3 * e / 2, f + 3 * e / 4)
        n += 1
print('grid checks', n, 'OK (V total = max(s+t,5s/4+t/2) exactly; pencil total = max(3e/2,f+3e/4))')

# Lower bound for V (not needed by the proof, only sufficiency is): dual check via two valid dual vectors
# w = e_0/2+e_1/2+e_z ... skipped: sufficiency is all Theorem L+ uses.

random.seed(7)
ok = 0
for it in range(300):
    p = random.randint(1, 3)
    den = random.choice([12, 20, 24, 30])
    s = [F(random.randint(0, den), den) for _ in range(p)]
    t = [F(random.randint(0, den), den) for _ in range(p)]
    x = [max(si + ti, 5 * si / 4 + ti / 2) for si, ti in zip(s, t)]
    rows = [t, t, s, s, s, s, s]
    good, msg = realise_and_check(rows, x, [V_masses(s[i], t[i]) for i in range(p)])
    assert good, msg
    e = s; f = [min(ti, xi - 3 * ei / 4) for ti, xi, ei in zip(t, x, e)]
    x2 = [max(3 * ei / 2, fi + 3 * ei / 4, ei, fi) for ei, fi in zip(e, f)]
    rows = [e, e, e, f, f, f, f]
    good, msg = realise_and_check(rows, x2, [pencil_masses(e[i], f[i]) for i in range(p)])
    assert good, msg
    ok += 1
print('literal integer realisations (V and pencil) at the exact capacity boundary:', ok, 'OK')
