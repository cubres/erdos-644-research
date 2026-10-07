"""Split rank-40 unit boxes (lo triple) into the 8 rank-80 unit sub-boxes and run batch3.py at rank 80."""
import sys, subprocess, itertools
subs=[]
for s in sys.argv[1:]:
    lo=tuple(map(int,s.split(',')))
    for d in itertools.product((0,1),repeat=3):
        l=tuple(2*a+e for a,e in zip(lo,d)); subs.append(','.join(map(str,l+tuple(v+1 for v in l))))
subprocess.run(['python3','-u','batch3.py','80']+subs)
