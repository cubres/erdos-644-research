"""Map the region near c = d + 1/2 where two-type families F(d,c) HAVE property (7,2) despite tau* > 1/2."""
import sys, time, json
from multiprocessing import Pool
from p644_patterns import venn_milp
from p644_nu2_pattern_thm import fam2
def job(args):
    d, c, tl = args
    t0 = time.time(); st, _ = venn_milp(fam2(d, c), m=None, time_limit=tl, intersecting=False)
    return (d, c, st, round(time.time() - t0))
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'fine'
    jobs = []
    if mode == 'fine':
        for i in range(0, 13):
            d = round(0.20 + 0.005 * i, 4)
            for j in range(0, 9):
                c = round(d + 0.48 + 0.0025 * j, 4)
                jobs.append((d, c, 900))
    else:   # coarse sweep along the boundary for all d
        for i in range(1, 50):
            d = round(0.01 * i, 4)
            for gap in (0.0, 0.005, 0.01, 0.02):
                c = round(d + 0.5 - gap, 4)
                if c > 0.5: jobs.append((d, c, 900))
    out = open(f'logs/nu2_pocket_{mode}.log', 'a')
    with Pool(6) as pool:
        for (d, c, st, secs) in pool.imap_unordered(job, jobs):
            line = f"d={d} c={c} tau*={1+d-c:.4f} gap={d+0.5-c:+.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
