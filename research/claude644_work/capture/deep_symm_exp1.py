"""Experiment 1: random saturated k-uniform (7,2) families on [n].
Record tau, exchangeability classes, and for every non-exchangeable pair (u,v):
  - swap closure H u (uv)H : (7,2)?  (must fail for saturated H: sanity check)
  - Zykov clone u<-v : tau change, (7,2)?
"""
import random, sys, collections
from deep_symm_lib import *

def analyse(H, n, k):
    t = tau(H, n)
    cls = exch_classes(H, n)
    stats = collections.Counter()
    for u in range(n):
        for v in range(n):
            if u == v: continue
            if all(swap(E,u,v) in set(H) for E in H):
                stats['aut'] += 1; continue
            Z = zykov(H, u, v)
            tz = tau(Z, n)
            ok = is72(Z, n)
            key = ('drop' if tz < t else ('same' if tz == t else 'up')) + ('/72' if ok else '/bad')
            stats[key] += 1
            # swap closure sanity: must fail for saturated families
            SC = list(set(H) | set(swapfam(H,u,v)))
            if is72(SC, n):
                stats['SWAPCLOSURE_OK(!)'] += 1
    return t, cls, stats

if __name__ == '__main__':
    n, k, trials, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    tally = collections.Counter()
    best = None
    for tr in range(trials):
        H = saturate_uniform(n, k, rng)
        t, cls, stats = analyse(H, n, k)
        sizes = tuple(len(c) for c in cls)
        tally[(t, sizes)] += 1
        if best is None or t > best[0]:
            best = (t, H, cls, stats)
        print(f"trial {tr}: |H|={len(H)} tau={t} classes={sizes} zykov-stats={dict(stats)}", flush=True)
    print("TALLY", dict(tally))
