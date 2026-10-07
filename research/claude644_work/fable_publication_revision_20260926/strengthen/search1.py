"""Search over first requests D1 for the 1-adaptive + 3-static class at a triple (x,y,z),
budget t, dichotomy (<=M or >1/2) with M=x.  Screening adversary = hill (lower bound);
certification = column-generation adversary (lb certified, ub approximate).
usage: python3 search1.py x y z t [nrand] [seed]
"""
import sys, random, itertools, time
from multiprocessing import Pool
from cells import triple_config, cover, respond, cellname, H
from adversary import hill_adversary, solve_adversary

x, y, z, t = map(float, sys.argv[1:5])
NRAND = int(sys.argv[5]) if len(sys.argv) > 5 else 60
SEED = int(sys.argv[6]) if len(sys.argv) > 6 else 0
M = x
cfg = triple_config(x, y, z)
CELLS = [3, 5, 6, 1, 2, 4]


def fill(d):
    """scale/pad request to total exactly t if possible (never hurts)."""
    d = {c: min(cfg[c], max(0.0, d.get(c, 0.0))) for c in CELLS}
    s = sum(d.values())
    if s > t:
        # scale down proportionally
        f = t / s
        d = {c: v * f for c, v in d.items()}
    return d


def vertex_requests():
    """all subsets of cells fully requested (total<=t) plus one partial cell filling to t."""
    out = []
    for r in range(0, 7):
        for sub in itertools.combinations(CELLS, r):
            s = sum(cfg[c] for c in sub)
            if s > t + 1e-12:
                continue
            rest = [c for c in CELLS if c not in sub]
            if not rest or s >= t - 1e-9:
                out.append({c: cfg[c] for c in sub})
                continue
            for p in rest:
                d = {c: cfg[c] for c in sub}
                d[p] = min(cfg[p], t - s)
                out.append(d)
    # dedupe
    seen = set(); uniq = []
    for d in out:
        key = tuple(round(d.get(c, 0.0), 6) for c in CELLS)
        if key not in seen:
            seen.add(key); uniq.append(d)
    return uniq


def rand_request(rng):
    w = {c: rng.random() ** 2 for c in CELLS}
    for c in (3, 5, 6):
        if rng.random() < 0.5:
            w[c] = 5.0
    order = sorted(CELLS, key=lambda c: -w[c] * rng.random())
    d = {}; rem = t
    for c in order:
        a = min(cfg[c], rem * (1.0 if rng.random() < 0.6 else rng.random()))
        d[c] = a; rem -= a
    for c in order:
        a = min(cfg[c] - d[c], rem); d[c] += a; rem -= a
    return d


def screen(args):
    d, seed = args
    v, h = hill_adversary(cfg, d, t, M, 0.5, H, 15, 3, 4, seed=seed, nrand=25, climb=20)
    v2, h2 = hill_adversary(cfg, d, t, M, 0.5, H, 15, 3, 4, seed=seed + 1000, nrand=25, climb=20)
    if v2 > v:
        v, h = v2, h2
    return (v, d, h)


if __name__ == '__main__':
    rng = random.Random(SEED)
    cands = vertex_requests()
    print('vertex requests:', len(cands), flush=True)
    cands += [rand_request(rng) for _ in range(NRAND)]
    t0 = time.time()
    with Pool(10) as p:
        res = p.map(screen, [(d, i) for i, d in enumerate(cands)])
    res.sort(key=lambda r: r[0])
    print('screened %d requests in %.0fs' % (len(res), time.time() - t0), flush=True)
    for v, d, h in res[:12]:
        print('%.5f  d=%s  h=%s' % (v, {cellname(c): round(a, 4) for c, a in d.items() if a > 1e-9},
                                    {cellname(c): round(a, 4) for c, a in h.items() if a > 1e-9}), flush=True)
    # local search on the best few
    best = res[:4]
    improved = []
    for v, d, h in best:
        cur_v, cur_d = v, dict(d)
        step = 0.03
        for it in range(6):
            moved = False
            trials = []
            for c1 in CELLS:
                for c2 in CELLS:
                    if c1 == c2:
                        continue
                    d2 = dict(cur_d)
                    a = min(step, d2.get(c1, 0.0), cfg[c2] - d2.get(c2, 0.0))
                    if a <= 1e-9:
                        continue
                    d2[c1] -= a; d2[c2] = d2.get(c2, 0.0) + a
                    trials.append(d2)
            if not trials:
                break
            with Pool(10) as p:
                rr = p.map(screen, [(d2, 7 + i) for i, d2 in enumerate(trials)])
            rr.sort(key=lambda r: r[0])
            if rr[0][0] < cur_v - 1e-6:
                cur_v, cur_d = rr[0][0], rr[0][1]; moved = True
                print('  local improve -> %.5f d=%s' % (cur_v, {cellname(c): round(a, 4) for c, a in cur_d.items() if a > 1e-9}), flush=True)
            if not moved:
                step /= 2
        improved.append((cur_v, cur_d))
    improved.sort(key=lambda r: r[0])
    print('=== certification of best request(s) with column generation ===', flush=True)
    for v, d in improved[:2]:
        t0 = time.time()
        r = solve_adversary(cfg, d, t, M, 0.5, H, 15, 3, 4, iters=60)
        print('d=%s  screen=%.5f  certified lb=%.5f  ub=%.5f  h*=%s  (%.0fs)' % (
            {cellname(c): round(a, 4) for c, a in d.items() if a > 1e-9}, v, r['lb'], r['ub'],
            {cellname(c): round(a, 4) for c, a in r['h'].items() if a > 1e-9}, time.time() - t0), flush=True)
