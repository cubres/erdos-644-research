"""multi-route value of the NC request at several box points. usage: probe_box.py t"""
import sys, time
from multiprocessing import Pool
from routes import solve_multi, fmt
from cells import triple_config
X, Y, Z = 3, 5, 6
t = float(sys.argv[1])
pts = []
for M in [4*t-3+0.0005, (4*t-3+t/2)/2, t/2-0.0005, t/2]:
    ycap = 1-(t+M)/2; zlo = 3*t-2-M
    for y in [t-0.5+0.0005, (t-0.5+ycap)/2, ycap]:
        for z in [zlo+0.0005, (zlo+1-t)/2, 1-t-0.0005]:
            pts.append((M, y, z))
def job(p):
    M, y, z = p
    cfg = triple_config(M, y, z)
    d = {Y: y, Z: z, X: t-y-z}
    t0 = time.time()
    r = solve_multi(cfg, d, t, M, iters=80)
    return (p, r['lb'], r['ub'], fmt(r['h']), {k: round(v, 4) for k, v in r['routes'].items()}, time.time()-t0)
if __name__ == '__main__':
    with Pool(10) as pool:
        for p, lb, ub, h, rt, dt in pool.imap(job, pts):
            print('M=%.4f y=%.4f z=%.4f  lb=%.5f ub=%.5f  %s  h=%s routes=%s (%.0fs)' % (p[0], p[1], p[2], lb, ub, 'CLOSES' if ub <= t+1e-6 else ('FAILS' if lb > t+1e-6 else 'open'), h, rt, dt), flush=True)
