"""Two adaptive requests followed by two static requests (discovery oracle).

State after D1 and response H: config over masks on edges E,F,G,H (bit 8 = H), including
the H-private cell (mask 8) whose mass only matters for the dichotomy on |H ∩ I|.
D2: request over these cells (sum<=t). I: response (bit 16), dichotomy on traces on E,F,G,H.
Final: exact 2-request cover on the 5-edge configuration (cells irrelevant unless they have a
candidate partner; H-private / I-private / H∩I-only cells never have partners).

value_after_H(config4, t, M) = min over D2 (heuristic search) of max over I (adversary) of cover2.
"""
import itertools, random, time, math
from cells import cover, respond, cellname, relevant, H, I
from adversary import hill_adversary, solve_adversary, padded_respond

FULL5 = 31


def cheap_adversary(config, d, t, M, nrand=40, seed=0):
    """random maximal responses only (fast lower bound)."""
    rng = random.Random(seed)
    cells = [c for c in config if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    def ok(h):
        if sum(h.values()) > 1 + 1e-9:
            return False
        for e in range(4):
            tr = sum(h[c] for c in cells if c & (1 << e))
            if M + 1e-9 < tr < 0.5 + 1e-5:
                return False
        return True
    best = (-1.0, None)
    tries = 0
    while tries < nrand * 3 and (best[1] is None or tries < nrand):
        tries += 1
        order = cells[:]; rng.shuffle(order)
        h = {c: 0.0 for c in cells}; rem = 1.0
        for c in order:
            a = min(avail[c], rem * (1.0 if rng.random() < 0.6 else rng.random()))
            h[c] = a; rem -= a
        if not ok(h):
            # try to repair traces by trimming to M
            for e in range(4):
                tr = sum(h[c] for c in cells if c & (1 << e))
                if M < tr < 0.5:
                    f = M / tr
                    for c in cells:
                        if c & (1 << e):
                            h[c] *= f
            if not ok(h):
                continue
        v = cover(padded_respond(config, d, h, I), FULL5, 2)
        if v > best[0]:
            best = (v, h)
    return best


def d2_candidates(config, t, max_full=6, partial=True):
    cells = sorted(config, key=lambda c: -config[c])
    # only cells that matter: relevant ones for the 4-edge graph plus H-private (dichotomy)
    rel, nb = relevant(config, 15)
    use = [c for c in cells if c in rel or c == 8]
    out = []
    for r in range(0, min(max_full, len(use)) + 1):
        for sub in itertools.combinations(use, r):
            s = sum(config[c] for c in sub)
            if s > t + 1e-12:
                continue
            base = {c: config[c] for c in sub}
            rest = [c for c in use if c not in sub]
            if not partial or not rest or s >= t - 1e-9:
                out.append(base); continue
            for p in rest:
                d = dict(base); d[p] = min(config[p], t - s)
                out.append(d)
    seen = set(); uniq = []
    for d in out:
        key = tuple(sorted((c, round(v, 6)) for c, v in d.items() if v > 1e-9))
        if key not in seen:
            seen.add(key); uniq.append(d)
    return uniq


def value_after_H(config, t, M, verbose=False, top=15, exact=True, max_full=6, pool=None):
    """min over D2 of adversary value. returns (value, D2, I, certified_lb_flag)."""
    cands = d2_candidates(config, t, max_full=max_full)
    if verbose:
        print('    D2 candidates:', len(cands), flush=True)
    def cheap(d):
        return cheap_adversary(config, d, t, M, nrand=30)[0]
    if pool is not None:
        scores = pool.map(_cheap_job, [(config, d, t, M) for d in cands])
    else:
        scores = [cheap(d) for d in cands]
    order = sorted(range(len(cands)), key=lambda i: scores[i])
    best = (9.0, None, None)
    for i in order[:top]:
        d = cands[i]
        v, h = hill_adversary(config, d, t, M, 0.5, I, FULL5, 2, 5, seed=i, nrand=30, climb=20)
        if v < best[0]:
            best = (v, d, h)
    if verbose:
        print('    best D2 after hill: %.5f d=%s' % (best[0], fmt(best[1])), flush=True)
    # local search on D2
    d = dict(best[1]); cur = best[0]; step = 0.03
    cells = [c for c in config]
    for it in range(8):
        moved = False
        for c1 in cells:
            for c2 in cells:
                if c1 == c2:
                    continue
                d2 = dict(d)
                a = min(step, d2.get(c1, 0.0), config[c2] - d2.get(c2, 0.0))
                if a <= 1e-9:
                    continue
                d2[c1] -= a; d2[c2] = d2.get(c2, 0.0) + a
                v, h = hill_adversary(config, d2, t, M, 0.5, I, FULL5, 2, 5, seed=it, nrand=25, climb=15)
                if v < cur - 1e-6:
                    cur, d = v, d2; moved = True
                    best = (v, d2, h)
        if not moved:
            step /= 2
            if step < 2e-3:
                break
    if exact:
        r = solve_adversary(config, best[1], t, M, 0.5, I, FULL5, 2, 5, iters=60)
        if verbose:
            print('    exact adversary on best D2: lb=%.5f ub=%.5f' % (r['lb'], r['ub']), flush=True)
        return (max(best[0], r['lb']), best[1], r['h'], r['ub'])
    return (best[0], best[1], best[2], None)


def _cheap_job(args):
    config, d, t, M = args
    return cheap_adversary(config, d, t, M, nrand=30)[0]


def fmt(d):
    return {cellname(c): round(v, 4) for c, v in d.items() if v > 1e-9}


if __name__ == '__main__':
    import sys
    from cells import triple_config
    from multiprocessing import Pool
    x, y, z, t = 0.425, 0.36, 0.144, 0.855
    cfg = triple_config(x, y, z)
    # NC request and the certified worst H from adversary.py
    d1 = {5: y, 6: z, 3: t - y - z}
    hstar = {3: 0.074, 1: 0.215, 2: 0.4296, 4: 0.2295}
    c4 = respond(cfg, H, hstar)
    c4[8] = 1 - sum(hstar.values())
    print('4-edge config:', fmt(c4))
    print('3-cover:', cover(c4, 15, 3), ' 2-cover:', cover(c4, 15, 2))
    t0 = time.time()
    with Pool(10) as p:
        v, d2, i_, ub = value_after_H(c4, t, x, verbose=True, pool=p)
    print('value after this H with 2 adaptive: %.5f (ub %.5f) D2=%s I=%s (%.0fs)' % (v, ub, fmt(d2), fmt(i_), time.time() - t0))
