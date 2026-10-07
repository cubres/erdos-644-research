"""Search over first requests D1 using the multi-route position value.
usage: python3 search_multi.py x y z t forbidden_spec [nrand] [seed]
forbidden_spec: 'dich' -> [(x,1/2)]; 'none' -> []; or 'lo,hi;lo,hi'.
Screening: hill adversary with proxy position (exact cover3 for alpha, lemma minimum for beta).
Certification: solve_multi2 on the best few.
"""
import sys, random, itertools, time
sys.path.insert(0, '../explore')
from multiprocessing import Pool
from cells import triple_config, cover, cellname, H
from adversary import padded_respond
from routes import triple_cells_after, evalexpr, beta_available, X, Y, Z, PE, PF, PG, CELLS6, fmt
from routes2 import solve_multi2, trace_ok, verdict
from lemmas import split, asym1, asym2, four, sym, s0

x, y, z, t = map(float, sys.argv[1:5])
spec = sys.argv[5] if len(sys.argv) > 5 else 'dich'
NRAND = int(sys.argv[6]) if len(sys.argv) > 6 else 40
SEED = int(sys.argv[7]) if len(sys.argv) > 7 else 0
if spec == 'dich':
    FORB = [(x, 0.5)]
elif spec == 'none':
    FORB = []
else:
    FORB = [tuple(map(float, s.split(','))) for s in spec.split(';')]
cfg = triple_config(x, y, z)


def lemma_min(a, b, c):
    return min(f(a, b, c) for f in (split, asym1, asym2, four, sym, s0))


def proxy_position(d, h):
    vals = {'alpha': cover(padded_respond(cfg, d, h, H), 15, 3)}
    for w in 'EFG':
        if beta_available(d, cfg, w):
            ex = triple_cells_after(cfg, w)
            m = [max(evalexpr(e, h), 0.0) for e in ex]
            vals['beta' + w] = lemma_min(m[0], m[1], m[2])
    return min(vals.values()), vals


def hill_proxy(d, seed=0, nrand=20, climb=12):
    rng = random.Random(seed)
    cells = [c for c in CELLS6 if cfg[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: cfg[c] - d.get(c, 0.0) for c in cells}
    best = (-1.0, None)
    for _ in range(nrand):
        order = cells[:]; rng.shuffle(order)
        h = {c: 0.0 for c in cells}; rem = 1.0
        for c in order:
            a = min(avail[c], rem * (1.0 if rng.random() < 0.6 else rng.random()))
            h[c] = a; rem -= a
        if trace_ok(h, FORB):
            v = proxy_position(d, h)[0]
            if v > best[0]:
                best = (v, h)
    if best[1] is None:
        return best
    h = dict(best[1]); cur = best[0]; step = 0.05
    for _ in range(climb):
        improved = False
        for c1 in cells:
            for c2 in cells + [None]:
                if c1 == c2:
                    continue
                h2 = dict(h); a = min(step, h2[c1]); h2[c1] -= a
                if c2 is not None:
                    h2[c2] += min(a, avail[c2] - h2[c2])
                if trace_ok(h2, FORB):
                    v = proxy_position(d, h2)[0]
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
            h2 = dict(h); a = min(step, avail[c1] - h2[c1], 1 - sum(h2.values()))
            if a > 1e-9:
                h2[c1] += a
                if trace_ok(h2, FORB):
                    v = proxy_position(d, h2)[0]
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
        if not improved:
            step /= 2
            if step < 2e-3:
                break
    return (cur, h)


def vertex_requests():
    out = []
    for r in range(0, 7):
        for sub in itertools.combinations(CELLS6, r):
            s = sum(cfg[c] for c in sub)
            if s > t + 1e-12:
                continue
            rest = [c for c in CELLS6 if c not in sub]
            if not rest or s >= t - 1e-9:
                out.append({c: cfg[c] for c in sub}); continue
            for p in rest:
                d = {c: cfg[c] for c in sub}; d[p] = min(cfg[p], t - s); out.append(d)
    seen = set(); uniq = []
    for d in out:
        key = tuple(round(d.get(c, 0.0), 6) for c in CELLS6)
        if key not in seen:
            seen.add(key); uniq.append(d)
    return uniq


def rand_request(rng):
    w = {c: rng.random() ** 2 for c in CELLS6}
    for c in (X, Y, Z):
        if rng.random() < 0.5:
            w[c] = 5.0
    order = sorted(CELLS6, key=lambda c: -w[c] * rng.random())
    d = {}; rem = t
    for c in order:
        a = min(cfg[c], rem * (1.0 if rng.random() < 0.6 else rng.random())); d[c] = a; rem -= a
    for c in order:
        a = min(cfg[c] - d[c], rem); d[c] += a; rem -= a
    return d


def screen(args):
    d, seed = args
    v, h = hill_proxy(d, seed=seed)
    return (v, d, h)


if __name__ == '__main__':
    rng = random.Random(SEED)
    cands = vertex_requests() + [rand_request(rng) for _ in range(NRAND)]
    print('triple', (x, y, z), 't', t, 'forbidden', FORB, 'candidates', len(cands), flush=True)
    t0 = time.time()
    with Pool(10) as p:
        res = p.map(screen, [(d, i) for i, d in enumerate(cands)])
    res.sort(key=lambda r: r[0])
    print('screened in %.0fs' % (time.time() - t0), flush=True)
    for v, d, h in res[:10]:
        print('  %.5f  d=%s  h=%s' % (v, fmt(d), fmt(h)), flush=True)
    # local search on the best 3
    finals = []
    for v, d, h in res[:3]:
        cur_v, cur_d = v, dict(d); step = 0.03
        for it in range(5):
            trials = []
            for c1 in CELLS6:
                for c2 in CELLS6:
                    if c1 == c2:
                        continue
                    d2 = dict(cur_d); a = min(step, d2.get(c1, 0.0), cfg[c2] - d2.get(c2, 0.0))
                    if a <= 1e-9:
                        continue
                    d2[c1] -= a; d2[c2] = d2.get(c2, 0.0) + a; trials.append(d2)
            if not trials:
                break
            with Pool(10) as p:
                rr = p.map(screen, [(d2, 11 + i) for i, d2 in enumerate(trials)])
            rr.sort(key=lambda r: r[0])
            if rr[0][0] < cur_v - 1e-6:
                cur_v, cur_d = rr[0][0], rr[0][1]
                print('  local -> %.5f d=%s' % (cur_v, fmt(cur_d)), flush=True)
            else:
                step /= 2
        finals.append((cur_v, cur_d))
    finals.sort(key=lambda r: r[0])
    print('=== certification (exact routes, column generation) ===', flush=True)
    for v, d in finals[:2]:
        t0 = time.time()
        r = solve_multi2(cfg, d, t, FORB, iters=80)
        print('d=%s screen=%.5f  lb=%.5f ub=%.5f %s h=%s routes=%s (%.0fs)' % (
            fmt(d), v, r['lb'], r['ub'], verdict(r, t), fmt(r['h']),
            {k: round(a, 4) for k, a in r['routes'].items()}, time.time() - t0), flush=True)
