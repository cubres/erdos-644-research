"""Run cells_box3.py on capacity boxes (rank R, unit boxes [lo, lo+w]) with NW workers; verify UNSAT ones with
verify3.sh (audit + DRAT + drat-trim + std-lib LRAT).  Summary lines appended to batch3_summary.txt."""
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
R=int(sys.argv[1]); spec=sys.argv[2:]
boxes=[tuple(map(int,s.split(','))) for s in spec]   # lo1,lo2,lo3,hi1,hi2,hi3
def work(b):
    lo,hi=b[:3],b[3:]
    key='b3_%d_%s_lo_%s'%(R,'_'.join(map(str,hi)),'_'.join(map(str,lo)))
    if os.path.exists('logs/astra_continuous_type_cells/'+key+'.json'):
        return key+' exists'
    log='runs/'+key+'.log'
    subprocess.run('python3 -u cells_box3.py %d %d %d %d --lo %d %d %d > %s 2>&1'%(R,*hi,*lo,log),shell=True)
    last=open(log).read().strip().split('\n')[-1]
    with open('batch3_summary.txt','a') as f: f.write('%s %s %s\n'%(lo,hi,last[:60]))
    if 'UNSAT' in last: subprocess.run('./verify3.sh '+key,shell=True)
    return last
with ThreadPoolExecutor(int(os.environ.get('NW','2'))) as ex:
    for b,r in zip(boxes,ex.map(work,boxes)): pass
print('batch done')
