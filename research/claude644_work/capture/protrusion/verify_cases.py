# Structural verification for the hand lower-bound proofs (all line orders, all anchor choices).
# Time labels: the dual Fano plane on points 0..6 (0..6 = processing times of the 7 Fano lines).
# UNANCHORED: every labelling falls in Case A ({4,5,6} is a line) or Case B (not).
# ANCHORED: time 0 = anchor (its lines are dead); cases A'1, A'2, B'0, B'x, B'y, B'w(alpha), B'w(beta).
import itertools, sys
from collections import Counter
BASE = [frozenset(((0+i)%7, (1+i)%7, (3+i)%7)) for i in range(7)]
def relabel(order):  # order[t] = base point processed at time t
    pos = {p: t for t, p in enumerate(order)}
    return [frozenset(pos[p] for p in L) for L in BASE]
def line_through(lines, a, b):
    return [L for L in lines if a in L and b in L][0]
def third(lines, a, b):
    return next(iter(line_through(lines, a, b) - {a, b}))
cnt_u = Counter(); cnt_a = Counter()
for order in itertools.permutations(range(7)):
    lines = relabel(order)
    Ls = set(lines)
    # ---- unanchored
    if frozenset({4,5,6}) in Ls:
        ks = sorted(third(lines, 3, i) for i in (0,1,2))
        assert ks == [4,5,6], ks                      # lines through 3 meet {4,5,6} in distinct points
        i5 = [i for i in (0,1,2) if third(lines,3,i) == 5][0]; i6 = [i for i in (0,1,2) if third(lines,3,i) == 6][0]
        assert i5 != i6
        cnt_u['A'] += 1
    else:
        x, y, w = third(lines,4,5), third(lines,4,6), third(lines,5,6)
        assert len({x,y,w}) == 3 and max(x,y,w) <= 3
        cnt_u['B'] += 1
    # ---- anchored: anchor = time 0
    dead = lambda L: 0 in L
    if frozenset({4,5,6}) in Ls:
        k0 = third(lines, 0, 3)
        if k0 == 4:
            # live lines through 3 go to 5 and 6 with partners in {1,2}
            for k in (5,6):
                i = [i for i in (1,2) if third(lines,3,i) == k]; assert len(i) == 1
            cnt_a["A'1 (value>=1)"] += 1
        else:
            a12 = third(lines,1,2); assert a12 == k0 and k0 in (5,6)
            a13, a23 = third(lines,1,3), third(lines,2,3)
            assert {a13,a23} == {4,5,6} - {k0} and 4 in (a13,a23)
            cnt_a["A'2 (three chains)"] += 1
    else:
        x, y, w = third(lines,4,5), third(lines,4,6), third(lines,5,6)
        if 0 not in (x,y,w):
            cnt_a["B'0 (value>=1)"] += 1
        elif x == 0:
            z = ({1,2,3} - {y,w}).pop()
            live = sorted(tuple(sorted(L)) for L in lines if not dead(L))
            assert live == sorted([tuple(sorted({4,6,y})), tuple(sorted({5,6,w})), tuple(sorted({z,4,w})), tuple(sorted({z,5,y}))]), (live, x,y,w,z)
            cnt_a["B'x (three chains)"] += 1
        elif y == 0:
            z = ({1,2,3} - {x,w}).pop()
            live = sorted(tuple(sorted(L)) for L in lines if not dead(L))
            assert live == sorted([tuple(sorted({4,5,x})), tuple(sorted({5,6,w})), tuple(sorted({z,4,w})), tuple(sorted({z,6,x}))])
            cnt_a["B'y (three chains)"] += 1
        else:
            assert w == 0
            z = ({1,2,3} - {x,y}).pop()
            live = sorted(tuple(sorted(L)) for L in lines if not dead(L))
            assert live == sorted([tuple(sorted({4,5,x})), tuple(sorted({4,6,y})), tuple(sorted({z,x,6})), tuple(sorted({z,y,5}))])
            cnt_a["B'w(alpha) z=3 (value>=1)" if z == 3 else "B'w(beta) (adaptive 3/4)"] += 1
print('unanchored cases over all 5040 labellings:', dict(cnt_u))
print('anchored cases over all 5040 labellings (anchor = time 0):', dict(cnt_a))
