"""Three-part two-type families near the pocket: s = (d, 1-d-x, x), t = (c, 1-c-y, y), X of size xi."""
import sys, time
from multiprocessing import Pool
from p644_patterns import Pattern, venn_milp
def fam3(d, c, x, y, xi=1.0):
    return Pattern([1.0, 1.0, xi], 1.0, boxes=[((1,0,0),(1,0,0)), ((0,1,0),(0,1,0)),
                                              ((d, 1-d-x, x),(d, 1-d-x, x)), ((c, 1-c-y, y),(c, 1-c-y, y))])
def job(a):
    d, c, x, y = a; t0 = time.time()
    st, _ = venn_milp(fam3(d, c, x, y), m=None, time_limit=900, intersecting=False)
    return (d, c, x, y, st, round(time.time() - t0))
if __name__ == '__main__':
    jobs = [(d, c, x, y) for d in (0.2, 0.225, 0.25) for c in (0.7, 0.72, 0.74) for x in (0.0, 0.02, 0.05) for y in (0.0, 0.02, 0.05) if not (x == 0 and y == 0)]
    out = open('logs/nu2_pocket3.log', 'a')
    with Pool(2) as pool:
        for (d, c, x, y, st, secs) in pool.imap_unordered(job, jobs):
            tau = min(1 + d - c + x, 1 - d, 1 - (1 - c - y))
            line = f"d={d} c={c} x={x} y={y} tau*={tau:.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
