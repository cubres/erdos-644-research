import sys,json,time
from pathlib import Path
sys.path.insert(0,"/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c")
import search6 as s
# Read original libraries and cache, never persist changes into Claude's files.
lo=[s.F(v) for v in sys.argv[1].split(',')]; hi=[s.F(v) for v in sys.argv[2].split(',')]
reg=True if sys.argv[3]=='balanced' else sys.argv[3]
out=Path(sys.argv[4]); tl=float(sys.argv[5]) if len(sys.argv)>5 else 120
S=s.Search(maxfacet=5,maxreq=2,tlimit=tl,log=True,usesupp=False)
S.userm=reg is True
C,E=s.bc.base_region(reg,True,(lo,hi),excess=True)
try:
 tree=S.solve(C,E,0,0,0,'')
 nf=s.count_fail(tree)
 D={'box':[[str(v) for v in lo],[str(v) for v in hi]],'balanced':reg,'sorted':True,'excess':True,'core':'b4','tree':s.enc(tree)}
 out.write_text(json.dumps(D))
 print('CLOSED' if nf==0 else 'FAIL',nf,S.stats,round(time.time()-S.t0),flush=True)
except RuntimeError:
 print('TIMEOUT',S.stats,round(time.time()-S.t0),flush=True)
