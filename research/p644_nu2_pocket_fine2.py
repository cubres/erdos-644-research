import time
from multiprocessing import Pool
from p644_patterns import venn_milp
from p644_nu2_pattern_thm import fam2
def job(a):
    d, c = a; t0 = time.time(); st, _ = venn_milp(fam2(d, c), m=None, time_limit=1500, intersecting=False)
    return (d, c, st, round(time.time() - t0))
if __name__ == '__main__':
    jobs = [(round(0.2325 + 0.0025 * i, 4), round(0.6925 + 0.0025 * j, 4)) for i in range(8) for j in range(12)]
    jobs += [(round(0.28 + 0.0025 * i, 4), round(0.75 + 0.0025 * j, 4)) for i in range(7) for j in range(9)]
    out = open('logs/nu2_pocket_fine2.log', 'a')
    with Pool(5) as pool:
        for (d, c, st, secs) in pool.imap_unordered(job, jobs):
            line = f"d={d} c={c} tau*={1+d-c:.4f} gap={d+0.5-c:+.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
