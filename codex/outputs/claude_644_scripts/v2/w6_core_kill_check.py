"""Given a relaxation-counterexample (grid types), find which genuine bad 7-tuple kills it (discovery MILP)."""
import sys, ast, time
from fractions import Fraction as F
from w4_typeclosed_lib import bad_tuple_milp, CELLS
def main(X, D, A):
    Tn=[tuple(F(v,D) for v in a) for a in A]; xn=[F(v,D) for v in X]
    t0=time.time()
    st, assign, cells = bad_tuple_milp(Tn, xn, time_limit=600)
    print(st, time.time()-t0)
    if st=='BAD':
        print('rows (types):', [A[j] for j in assign])
        for (i,S),m in sorted(cells.items()):
            print('  part',i,'cell',[r for r in range(7) if S>>r&1],'mass',round(m*D,3))
if __name__=='__main__':
    X=[int(v) for v in sys.argv[1].split(',')]; D=int(sys.argv[2]); A=ast.literal_eval(open(sys.argv[3]).read().split('TYPES')[1].strip())
    main(X,D,A)
