"""Three-type two-part families near the pocket: s=(d,1-d), t=(c,1-c), u=(e,1-e) with d<e<c.
tau* = 1 - max(e-d, c-e) if the third type lies between; a survivor would beat the two-type pocket."""
import time
from multiprocessing import Pool
from p644_patterns import Pattern, venn_milp
def fam(d, c, e):
    return Pattern([1.0,1.0], 1.0, boxes=[((1,0),(1,0)), ((0,1),(0,1)), ((d,1-d),(d,1-d)), ((c,1-c),(c,1-c)), ((e,1-e),(e,1-e))])
def job(a):
    d, c, e = a; t0 = time.time(); st, _ = venn_milp(fam(d, c, e), m=None, time_limit=1200, intersecting=False)
    return (d, c, e, st, round(time.time() - t0))
if __name__ == '__main__':
    jobs = [(0.235, 0.715, e) for e in (0.26, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.69)] + [(0.29, 0.77, e) for e in (0.32, 0.4, 0.5, 0.6, 0.7, 0.75)]
    out = open('logs/nu2_pocket_3types.log', 'a')
    with Pool(2) as pool:
        for (d, c, e, st, secs) in pool.imap_unordered(job, jobs):
            tau = 1 - max(e - d, c - e)
            line = f"d={d} c={c} e={e} tau*={tau:.4f}: {st} [{secs}s]"
            print(line, flush=True); out.write(line + '\n'); out.flush()
