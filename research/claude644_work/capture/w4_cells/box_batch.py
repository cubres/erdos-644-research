"""Run cells_box.py on a list of capacity boxes with limited parallelism; verify UNSAT ones."""
import subprocess, sys, json, time, os
from concurrent.futures import ThreadPoolExecutor
boxes = [tuple(map(int, b.split(','))) for b in sys.argv[2:]]   # lo1,lo2,lo3,hi1,hi2,hi3
R = int(sys.argv[1])
def work(b):
    lo, hi = b[:3], b[3:]
    tag = f'box_{R}_{"_".join(map(str,hi))}_lo_{"_".join(map(str,lo))}_T{3*R//4}_fano_regions_parents'
    log = f'run_{tag}.log'
    subprocess.run(f'python3 -u cells_box.py {R} {hi[0]} {hi[1]} {hi[2]} --lo {lo[0]} {lo[1]} {lo[2]} --fano --regions --parents > {log} 2>&1', shell=True)
    last = open(log).read().strip().split('\n')[-1]
    with open('batch_summary.txt', 'a') as f: f.write(f'{lo} {hi} {last}\n')
    if 'UNSAT' in last:
        subprocess.run(f'./verify_box.sh logs/astra_continuous_type_cells/{tag}', shell=True)
    return last
with ThreadPoolExecutor(int(os.environ.get('NW', '4'))) as ex:
    for b, r in zip(boxes, ex.map(work, boxes)): pass
print('batch done')
