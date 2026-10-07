"""Probe the second window M in (t/2, 3-3t] at t=0.855 with the multi-route oracle
(alpha: 3 static; beta: discard one edge + 4 static). First requests tried:
  NC   : Y, Z, and t-y-z points of X
  NCy  : X-part first then Y (avoid Z, all X if possible, rest of Y)
Discovery only (continuous model)."""
import sys, time
from multiprocessing import Pool
from routes import solve_multi, fmt
from cells import triple_config
X, Y, Z, PE, PF, PG = 3, 5, 6, 1, 2, 4
t = float(sys.argv[1]) if len(sys.argv) > 1 else 0.855
pts = []
for M in [t/2 + 0.002, (t/2 + 3 - 3*t)/2, 3 - 3*t - 0.001]:
    ycap = min(M, 1 - (t + M)/2); zlo = max(0.0, 3*t - 2 - M)
    for y in [t - 0.5 + 0.0005, ycap]:
        for z in [zlo + 0.0005, (zlo + 1 - t)/2, 1 - t - 0.0005]:
            if y <= ycap + 1e-12 and z <= y:
                for name in ['NC', 'NCzx']:
                    pts.append((M, y, z, name))
def request(name, M, y, z):
    if name == 'NC':
        return {Y: y, Z: z, X: t - y - z}
    if name == 'NCzx':   # avoid Z and X fully, rest from Y
        return {Z: z, X: min(M, t - z), Y: max(0.0, t - z - M)}
def job(p):
    M, y, z, name = p
    cfg = triple_config(M, y, z)
    d = request(name, M, y, z)
    t0 = time.time()
    try:
        r = solve_multi(cfg, d, t, M, iters=80)
        return (p, r['lb'], r['ub'], fmt(r['h']), {k: round(v, 4) for k, v in r['routes'].items()}, time.time() - t0)
    except Exception as e:
        return (p, None, None, str(e), {}, time.time() - t0)
if __name__ == '__main__':
    print('t', t, 'window2 (t/2, 3-3t] =', (t/2, 3 - 3*t), flush=True)
    with Pool(9) as pool:
        for p, lb, ub, h, rt, dt in pool.imap_unordered(job, pts):
            tag = 'ERR' if lb is None else ('CLOSES' if ub <= t + 1e-6 else ('FAILS' if lb > t + 1e-6 else 'open'))
            print('M=%.4f y=%.4f z=%.4f %-5s lb=%s ub=%s %s h=%s routes=%s (%.0fs)' % (p[0], p[1], p[2], p[3],
                  lb and round(lb, 5), ub and round(ub, 5), tag, h, rt, dt), flush=True)
