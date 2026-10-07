import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search3 import *
lo = [F(v) for v in sys.argv[1].split(',')]; hi = [F(v) for v in sys.argv[2].split(',')]
mf = int(sys.argv[3]); mr = int(sys.argv[4]); tl = float(sys.argv[5]); tag = sys.argv[6]
S = Search(maxfacet=mf, maxreq=mr, tlimit=tl, log=('-v' in sys.argv))
C, E = bc.base_region(True, True, (lo, hi))
try:
    tree = S.solve(C, E, 0, 0, 0, '')
    nf = json.dumps(enc(tree)).count('"FAIL"')
    status = 'CLOSED' if nf == 0 else 'FAILS%d' % nf
    json.dump({'box': [[str(v) for v in lo], [str(v) for v in hi]], 'balanced': True, 'sorted': True, 'tree': enc(tree)},
              open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/trees/%s.json' % tag, 'w'))
except RuntimeError:
    status = 'TIMEOUT'
save_vcache()
print(tag, status, S.stats, round(time.time()-S.t0), flush=True)
