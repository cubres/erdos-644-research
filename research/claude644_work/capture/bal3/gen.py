"""random balanced-regime instances (rigid finite type sets over 3 parts)"""
import random, b3lib as B
def rand_inst(rng, m, TGT=0.7505, xlo=0.5, xhi=1.5, tries=100000, spread=None):
    for _ in range(tries):
        x = [rng.uniform(xlo, xhi) for _ in range(3)]
        T = []
        for j in range(m):
            i = rng.randrange(3) if spread else j % 3
            a = [0, 0, 0]; lo = 2*x[i]/3; hi = min(1, x[i])
            if lo >= hi: break
            a[i] = rng.uniform(lo, hi)
            r = 1 - a[i]; o = [k for k in range(3) if k != i]; w = rng.random()**rng.choice([1, 1, 3])
            if rng.random() < 0.5: w = 1 - w
            a[o[0]] = r*w; a[o[1]] = r*(1-w)
            if a[o[0]] > x[o[0]] or a[o[1]] > x[o[1]]: break
            T.append(a)
        if len(T) < m: continue
        r = B.regime(x, T)
        if r is None: continue
        S, sig, e = r
        if any(e[i]+e[j] > 0.75 for i in range(3) for j in range(i+1, 3)): continue
        if sum(e) < TGT: continue
        if B.tau_star(x, T) < TGT: continue
        return x, T
    return None
