import itertools, sys
from fractions import Fraction as F
from w4_typeclosed_lib import bad_tuple_milp, tau_star
d = F(1,100); x = [F(3,4)]*3
base = [(F(1,2)+d, F(1,2)-d, 0), (F(1,2)+d, F(1,4), F(1,4)-d), (F(1,2)+d, F(3,10), F(1,5)-d), (F(3,4), F(1,4), 0),
        (F(3,4), F(1,8), F(1,8)), (F(6,10), F(4,10), 0), (F(6,10), F(2,10), F(2,10)), (F(1,2)+d, F(3,8), F(1,8)-d)]
types = sorted(set(p for b in base for p in itertools.permutations(b)))
print(len(types), 'types; tau* =', tau_star(types, x))
for sub in [types]:
    st, assign, cells = bad_tuple_milp(sub, x, time_limit=300)
    print(st, assign and [sub[a] for a in assign])
