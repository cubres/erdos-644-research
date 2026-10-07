"""run the engine on one capacity box (sorted x0<=x1<=x2 imposed), save tree"""
import sys, os; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search2 import *
lo=[F(s) for s in sys.argv[1].split(',')]; hi=[F(s) for s in sys.argv[2].split(',')]
mf=int(sys.argv[3]); mr=int(sys.argv[4]); tl=float(sys.argv[5]); tag=sys.argv[6]
S = Search(balanced=True, maxfacet=mf, maxreq=mr, nsamp=12, log=False)
S.tlimit = tl
C, E = base_constraints(True)
for i in range(3):
    C.append(({X(i): F(-1)}, -lo[i])); C.append(({X(i): F(1)}, hi[i]))
C.append(({X(0): 1, X(1): -1}, F(0))); C.append(({X(1): 1, X(2): -1}, F(0)))
try:
    tree = S.solve(C, E, 0, 0, 0, '')
    nf = json.dumps(tree).count('"FAIL"')
    status = 'CLOSED' if nf == 0 else 'FAILS%d' % nf
    json.dump({'lo': [str(v) for v in lo], 'hi': [str(v) for v in hi], 'tree': tree}, open('trees/%s.json' % tag, 'w'))
except RuntimeError:
    status = 'TIMEOUT'
print(tag, status, S.stats, round(time.time()-S.t0), flush=True)
