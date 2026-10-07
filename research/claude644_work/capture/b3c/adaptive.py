"""Adaptive x-box splitting driver.  Queue file: lines 'lo hi depth'.  A box that fails/times out is split in two
along its widest coordinate (respecting sortedness is automatic: sub-boxes violating x0<=x1<=x2 become empty regions).
Results appended to adapt_<name>.txt: 'tag status stats secs lo hi depth'.  Usage: adaptive.py name NP TL MINW"""
import sys, subprocess, time, os
from fractions import Fraction as F
D = '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c'
name, NP, TL, MINW = sys.argv[1], int(sys.argv[2]), sys.argv[3], F(sys.argv[4])
REG = sys.argv[5] if len(sys.argv) > 5 else 'bal'
ENG = sys.argv[6] if len(sys.argv) > 6 else '3'
qf = os.path.join(D, 'adaptq_%s.txt' % name); rf = os.path.join(D, 'adapt_%s.txt' % name)
queue = [l.split() for l in open(qf) if l.strip()]
done = set()
if os.path.exists(rf):
    for l in open(rf):
        p = l.split(); done.add((p[-3], p[-2]))
def tagof(lo, hi): return REG + '_' + lo.replace('/', 'd').replace(',', '_') + '__' + hi.replace('/', 'd').replace(',', '_')
running = []
def feasible_sorted(lo, hi):
    l = [F(v) for v in lo.split(',')]; h = [F(v) for v in hi.split(',')]
    return l[0] <= h[1] and l[1] <= h[2] and l[0] <= h[2] and sum(h) > F(9, 4)
while queue or running:
    for pr in running[:]:
        p, lo, hi, dep, fn = pr
        if p.poll() is not None:
            running.remove(pr)
            out = open(fn).read().strip().splitlines()
            line = out[-1] if out else 'X CRASH {}'
            st = line.split()[1] if len(line.split()) > 1 else 'CRASH'
            with open(rf, 'a') as f: f.write('%s %s %s %s\n' % (line, lo, hi, dep))
            if st != 'CLOSED':
                l = [F(v) for v in lo.split(',')]; h = [F(v) for v in hi.split(',')]
                k = max(range(3), key=lambda i: h[i] - l[i])
                if h[k] - l[k] > MINW:
                    m = (l[k] + h[k]) / 2
                    h1 = list(h); h1[k] = m; l2 = list(l); l2[k] = m
                    for a, b in ((l, h1), (l2, h)):
                        queue.append([','.join(map(str, a)), ','.join(map(str, b)), str(int(dep) + 1)])
                else:
                    with open(rf, 'a') as f: f.write('OPEN %s %s %s\n' % (lo, hi, dep))
    while queue and len(running) < NP:
        lo, hi, dep = queue.pop(0)
        if (lo, hi) in done: continue
        tag = tagof(lo, hi); fn = os.path.join(D, 's2logs', tag + '.out')
        p = subprocess.Popen(['python3', '-u', os.path.join(D, 'boxrun5.py'), lo, hi, '6', '3', TL, tag, ENG] + ([] if REG == 'bal' else ['reg=' + REG]),
                             stdout=open(fn, 'w'), stderr=subprocess.STDOUT)
        running.append((p, lo, hi, dep, fn))
    time.sleep(3)
print('ADAPTIVE DONE', name)
