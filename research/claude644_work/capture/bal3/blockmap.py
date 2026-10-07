import itertools
def best_block(x, T):
    """return (tau*, blocking map, residual u) by brute force over blocking maps"""
    p = len(x); N = sum(x); best = None
    choices = [[i for i in range(p) if a[i] > 1e-5] for a in T]
    for pi in itertools.product(*choices):
        caps = list(x)
        for j, i in enumerate(pi): caps[i] = min(caps[i], T[j][i])
        s = sum(caps)
        if best is None or s > best[0]: best = (s, pi, caps)
    return N - best[0], best[1], best[2]
