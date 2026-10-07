import time
from multiprocessing import Pool
from p644_patterns import venn_milp
from p644_nu2_pattern_thm import fam2
def job(a):
    d, c = a; t0 = time.time(); st, _ = venn_milp(fam2(d, c), m=None, time_limit=1500, intersecting=False)
    return (d, c, st, round(time.time() - t0))
if __name__ == '__main__':
    jobs = [(round(0.240 + 0.001 * i, 4), round(0.694 + 0.001 * j, 4)) for i in range(16) for j in range(12)]
    jobs = [(d, c) for (d, c) in jobs if 1 + d - c >= 0.54]
    out = open('logs/nu2_pocket_ultra.log', 'a')
    with Pool(3) as pool:
        for (d, c, st, secs) in pool.imap_unordered(job, jobs):
            line = f"d={d} c={c} tau*={1+d-c:.4f} gap={d+0.5-c:+.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
