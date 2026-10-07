"""|H|=2 residual case generator: parts A,B heavy, one light part L. Minimisers alpha,beta with R1 (3th_A>2x_A),
R2 (3th_B>2x_B), alpha_L+beta_L > x_L.  Add random helper types (heavy at A or B, light elsewhere) until
tau*>3/4.  Report which bad tuples exist: pairs (which fn, which types), Fano."""
import random, sys, collections, heavylib as h, pairlib as P
seed, N = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
stats = collections.Counter(); shown = 0; tested = 0
def rand_type(x, j, thmin):
    # heavy at j (A=0 or B=1), trace in [thmin, min(1,x_j)], rest split between other heavy part and L (light)
    for _ in range(200):
        a = [0.0]*3; a[j] = rng.uniform(thmin, min(1.0, x[j])); rest = 1 - a[j]
        u = rng.random(); o = 1 - j
        a[o] = rest*u; a[2] = rest*(1-u)
        if a[o] <= 4*x[o]/7 and a[2] <= 4*x[2]/7: return a
    return None
while tested < N:
    xA, xB = rng.uniform(1.0, 1.5), rng.uniform(1.0, 1.5); xL = rng.uniform(0.05, 0.5)
    x = [xA, xB, xL]
    thA = rng.uniform(max(2*xA/3, 4*xA/7), min(1, xA)); thB = rng.uniform(max(2*xB/3, 4*xB/7), min(1, xB))
    if (xA - thA) + (xB - thB) <= 0.75: continue
    # alpha with big L trace
    aL = rng.uniform(0.5*xL, 4*xL/7); bL = rng.uniform(max(0, xL - aL) , 4*xL/7)
    if aL + bL <= xL or aL > 1 - thA or bL > 1 - thB: continue
    al = [thA, 1 - thA - aL, aL]; be = [1 - thB - bL, thB, bL]
    if al[1] > 4*xB/7 or be[0] > 4*xA/7 or al[1] < 0 or be[0] < 0: continue
    T = [al, be]
    for _ in range(rng.randint(1, 6)):
        j = rng.randrange(2); t = rand_type(x, j, [thA, thB][j])
        if t: T.append(t)
    t = h.tau_star_fast(x, T)
    if t <= 0.75: continue
    tested += 1
    pr = P.any_pair(x, T); fa = h.any_fano_np(x, T)
    key = ('pair' if pr else '') + ('fano' if fa else '')
    stats[key or 'NONE'] += 1
    if pr: stats['fn%d' % pr[2]] += 1; stats['uses_minpair' if set(pr[:2]) == {0, 1} else ('uses_one_min' if (0 in pr[:2] or 1 in pr[:2]) else 'no_min')] += 1
    if not pr and not fa: print("NONE", t, x, T, flush=True)
print(tested, dict(stats))
