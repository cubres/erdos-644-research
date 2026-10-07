"""Extended pocket map: two-type families F(d,c) with larger gaps (tau* = 1 + d - c = 1/2 + gap)."""
import sys, time
from multiprocessing import Pool
from p644_patterns import venn_milp
from p644_nu2_pattern_thm import fam2
def job(a):
    d, c = a; t0 = time.time(); st, _ = venn_milp(fam2(d, c), m=None, time_limit=1200, intersecting=False)
    return (d, c, st, round(time.time() - t0))
if __name__ == '__main__':
    jobs = []
    for i in range(0, 17):
        d = round(0.18 + 0.01 * i, 4)
        for gap in (0.025, 0.03, 0.035, 0.04, 0.05, 0.06, 0.08):
            c = round(d + 0.5 - gap, 4)
            if c > 0.5: jobs.append((d, c))
    out = open('logs/nu2_pocket_ext.log', 'a')
    with Pool(6) as pool:
        for (d, c, st, secs) in pool.imap_unordered(job, jobs):
            line = f"d={d} c={c} tau*={1+d-c:.4f} gap={d+0.5-c:+.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
