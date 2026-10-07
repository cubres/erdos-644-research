"""|H|=2 with light parts: parts 0=A,1=B heavy; parts 2.. light (every type <= 4x_j/7 there).  Types sum to 1.
For tau*>3/4: check minimiser-pair chain (Q_alpha, Q_beta, V(beta,alpha)), any pair (42 fns), any Fano."""
import random, sys, itertools, heavylib as h, pairlib as P
def QV(x, al, be):
    p = len(x)
    Qa = all(3*al[i] <= 2*x[i]+1e-12 and 4*be[i]+3*al[i] <= 4*x[i]+1e-12 for i in range(p))
    Qb = all(3*be[i] <= 2*x[i]+1e-12 and 4*al[i]+3*be[i] <= 4*x[i]+1e-12 for i in range(p))
    V = all(be[i]+al[i] <= x[i]+1e-12 and 1.25*be[i]+0.5*al[i] <= x[i]+1e-12 for i in range(p))
    return Qa, Qb, V
def gen(rng, nl, m):
    x = [rng.uniform(0.7, 1.5), rng.uniform(0.7, 1.5)] + [rng.uniform(0.05, 1.0) for _ in range(nl)]
    p = len(x); T = []
    for _ in range(m):
        for _ in range(200):
            j = rng.randrange(2)
            a = [0.0]*p
            a[j] = rng.uniform(4*x[j]/7, min(1, x[j]))
            rest = 1 - a[j]
            caps = [4*x[i]/7 if (i >= 2 or i != j) else 0 for i in range(p)]; caps[j] = 0
            if sum(caps) < rest: continue
            w = [rng.random()**rng.choice([1,2,4]) * (1 if caps[i] > 0 else 0) for i in range(p)]
            # fill greedily in random proportions respecting caps
            left = rest; order = list(range(p)); rng.shuffle(order)
            S = sum(w)
            for i in order:
                if caps[i] <= 0: continue
                v = min(caps[i], left, rest*w[i]/S*1.5 + 1e-9)
                a[i] += v; left -= v
            for i in order:
                if left <= 1e-12: break
                if caps[i] > 0:
                    v = min(caps[i]-a[i], left); a[i] += v; left -= v
            if left > 1e-9: continue
            if 7*a[1-j] > 4*x[1-j]: continue
            T.append(a); break
    return x, T
if __name__ == '__main__':
    nl, m, N, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
    tested = 0; stats = {'chain': 0, 'pair': 0, 'fano': 0, 'none': 0}
    while tested < N:
        x, T = gen(rng, nl, m)
        if len(T) < m: continue
        if any(h.is_homog(x, a) for a in T) or h.heavy_parts(x, T) != [0, 1]: continue
        t = h.tau_star_fast(x, T)
        if t <= 0.75: continue
        tested += 1
        al = min([a for a in T if 7*a[0] > 4*x[0]], key=lambda a: a[0]); be = min([a for a in T if 7*a[1] > 4*x[1]], key=lambda a: a[1])
        if any(QV(x, al, be)): stats['chain'] += 1; continue
        if P.any_pair(x, T): stats['pair'] += 1; continue
        if h.any_fano_np(x, T): stats['fano'] += 1; continue
        stats['none'] += 1
        print("NONE tau*=%.4f x=%s T=%s" % (t, [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
    print(nl, m, stats)
