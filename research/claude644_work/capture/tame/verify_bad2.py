import itertools
from tc_lib import is72_code
from verify_bad import realize
for kp in (1,2):
    k=4*kp; n=[4*kp,3*kp+1]; c=[(1,),(0,)]; a=(1,)
    r=is72_code(n,c,a,k)
    ok,edges=realize(n, r[1][1], r[1][2], c, a, k)
    print(f"parity k={k} N={sum(n)}: ILP support orbit {r[1][0]}; explicit tuple verified bad (no 2-transversal): {ok}")
    for E in edges: print("   ",sorted(E),"|E cap P|=",sum(1 for x in E if x<n[0]))
