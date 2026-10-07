"""boxrun with the excess bound in the base region.  args: lo hi maxfacet maxreq tlimit tag [engine=3|4] [-v]"""
import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search6 import *
lo = [F(v) for v in sys.argv[1].split(',')]; hi = [F(v) for v in sys.argv[2].split(',')]
mf = int(sys.argv[3]); mr = int(sys.argv[4]); tl = float(sys.argv[5]); tag = sys.argv[6]
eng = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] in ('3', '4') else '3'
Cls = Search
S = Cls(maxfacet=mf, maxreq=mr, tlimit=tl, log=('-v' in sys.argv))
REG = True
for a in sys.argv:
    if a.startswith('reg='): REG = a[4:]
S.userm = (REG is True)
C, E = bc.base_region(REG, True, (lo, hi), excess=True)
try:
    tree = S.solve(C, E, 0, 0, 0, '')
    nf = json.dumps(enc(tree)).count('"FAIL"')
    status = 'CLOSED' if nf == 0 else 'FAILS%d' % nf
    if nf == 0:
        json.dump({'box': [[str(v) for v in lo], [str(v) for v in hi]], 'balanced': REG, 'sorted': True, 'excess': True, 'core': 'b4',
                   'tree': enc(tree)}, open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/trees7/%s.json' % tag, 'w'))
except RuntimeError:
    status = 'TIMEOUT'
save_vcache()
print(tag, status, S.stats, round(time.time()-S.t0), flush=True)
