import sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-cubres-Documents-Clauding/3451ffda-5ca8-4fb7-94da-7d7eeb432722/scratchpad/capture')
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp
D=20; X=[22,22,6]; x=[F(v,D) for v in X]
for a in [(14,5,1),(16,3,1),(17,3,0),(12,6,2)]:
    types=[(20,0,0),(0,20,0),a]
    tf=[tuple(F(v,D) for v in t) for t in types]
    st,asg,cells=bad_tuple_milp(tf,x,time_limit=60)
    print(a, st, asg)
    if cells:
        for (i,S),v in sorted(cells.items()):
            print('   part',i,'cell',format(S,'07b')[::-1],round(v*D,3))
