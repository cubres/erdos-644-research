#!/usr/bin/env python3
"""Referee check 2: exact integer arithmetic of the labelings.

(A) Disjoint pairs: min over splits of F (4 classes b,b2,c,c2) and G (2 classes a,a2) of the
    largest m-request equals ceil(f/2)+ceil(g/2)  (brute force, f,g <= 40).
(B) Anchor with protrusion.  Labels: F cap U -> u_b,u_b2,u_c,u_c2 ; F \\ U -> o_* ; U \\ F -> p0 (w),
    a (al), a2 (al2).  Requests:
        l2 (host, size <= q-1):  w + u_b + u_b2        l3: w + u_c + u_c2
        M1 (global, <= t-1): al + x_b + x_c    M4: al + x_b2 + x_c2
        M2: al2 + x_b2 + x_c                   M3: al2 + x_b + x_c2          (x = u + o)
    If all fit, (7,2) fails.  Hence (7,2) => q <= Qstar(f,g,N,t) := min over labelings with the four
    m-requests <= t-1 of max(l2,l3)   (Qstar = inf if no labeling is feasible).
    (B1) explicit labeling achieving  Qf = ceil(f/2) + max(0, N-f-2(t-1-h)),  h = ceil((f+g)/2),
         whenever h <= t-1 (checked for f,g <= 30, N-f <= 30, t <= 40).
    (B2) brute-force optimality of Qf among ALL labelings for small parameters.
    (B3) exact additive constant C in  q <= max(ceil(f/2), N-2t+g+ceil(f/2)) + C  for the
         nondegenerate case, and for the degenerate case h >= t using q <= min(t, N-4 floor(N/7)).
"""
import itertools

def cdiv(a, b):
    return -(-a // b)

# ---------------- (A)
def comps(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for rest in comps(n - i, k - 1):
            yield (i,) + rest

best4 = {}
for f in range(0, 41):
    # min over 4-splits of (max(b+c, b2+c2), max(b2+c, b+c2))
    opts = set()
    for (b, b2, c, c2) in comps(f, 4):
        opts.add((max(b + c, b2 + c2), max(b2 + c, b + c2)))
    best4[f] = opts
for f in range(0, 41):
    for g in range(0, 41):
        best = min(max(ga + Pa, g - ga + Pa2) for (Pa, Pa2) in best4[f] for ga in range(g + 1))
        assert best == cdiv(f, 2) + cdiv(g, 2), (f, g, best)
print('(A) disjoint pairs: min max m-request = ceil(f/2)+ceil(g/2) for f,g<=40')

# ---------------- (B1) explicit labeling
def explicit(f, g, N, t):
    n = f + g
    q0, r = divmod(n, 4)
    x = {'b': q0, 'b2': q0, 'c': q0, 'c2': q0}
    for key in ['b', 'b2', 'c'][:r]:
        x[key] += 1
    Sb, Sc = f // 2, cdiv(f, 2)
    if x['c'] + x['c2'] < Sc:
        Sb, Sc = Sc, Sb
    assert x['b'] + x['b2'] >= Sb and x['c'] + x['c2'] >= Sc
    u = {}
    u['b'] = min(x['b'], Sb); u['b2'] = Sb - u['b']
    u['c'] = min(x['c'], Sc); u['c2'] = Sc - u['c']
    assert all(0 <= u[k] <= x[k] for k in x)
    o = {k: x[k] - u[k] for k in x}
    assert sum(o.values()) == g and sum(u.values()) == f and min(o.values()) >= 0
    Pa = max(x['b'] + x['c'], x['b2'] + x['c2'])
    Pa2 = max(x['b2'] + x['c'], x['b'] + x['c2'])
    h = cdiv(n, 2)
    assert Pa <= h and Pa2 <= h
    if h > t - 1:
        return None
    al = min(t - 1 - Pa, N - f)
    al2 = min(t - 1 - Pa2, N - f - al)
    w = N - f - al - al2
    assert al >= 0 and al2 >= 0 and w >= 0
    m = [al + x['b'] + x['c'], al + x['b2'] + x['c2'], al2 + x['b2'] + x['c'], al2 + x['b'] + x['c2']]
    assert max(m) <= t - 1
    return max(w + u['b'] + u['b2'], w + u['c'] + u['c2'])

cnt = 0
worstC = -10**9
for f in range(0, 31):
    for g in range(0, 31):
        for N in range(f, f + 31):
            for t in range(1, 41):
                Q = explicit(f, g, N, t)
                h = cdiv(f + g, 2)
                if Q is None:
                    continue
                Qf = cdiv(f, 2) + max(0, N - f - 2 * (t - 1 - h))
                assert Q <= Qf, (f, g, N, t, Q, Qf)
                claim = max(cdiv(f, 2), N - 2 * t + g + cdiv(f, 2))
                worstC = max(worstC, Q - claim)
                cnt += 1
print('(B1) explicit labeling OK on', cnt, 'parameter sets; worst excess over max(ceil(f/2), N-2t+g+ceil(f/2)) =', worstC)

# ---------------- (B2) brute-force optimum over all labelings (small)
def qstar(f, g, N, t):
    best = None
    for u in comps(f, 4):
        for o in comps(g, 4):
            x = [u[i] + o[i] for i in range(4)]  # b,b2,c,c2
            Pa = max(x[0] + x[2], x[1] + x[3])
            Pa2 = max(x[1] + x[2], x[0] + x[3])
            if Pa > t - 1 or Pa2 > t - 1:
                continue
            al = min(t - 1 - Pa, N - f)
            al2 = min(t - 1 - Pa2, N - f - al)
            w = N - f - al - al2
            val = w + max(u[0] + u[1], u[2] + u[3])
            if best is None or val < best:
                best = val
    return best

bad = 0
tot = 0
for f in range(0, 7):
    for g in range(0, 7):
        for N in range(f, f + 8):
            for t in range(1, 12):
                qs = qstar(f, g, N, t)
                h = cdiv(f + g, 2)
                if h > t - 1:
                    assert qs is None
                    continue
                Qf = cdiv(f, 2) + max(0, N - f - 2 * (t - 1 - h))
                tot += 1
                if qs != Qf:
                    bad += 1
                    if bad <= 10:
                        print('  Qstar < Qf at', (f, g, N, t), qs, Qf)
print('(B2) brute-force optimum equals Qf on', tot - bad, 'of', tot, 'small parameter sets')

# ---------------- (B3) constants
# nondegenerate: Qf - max(ceil(f/2), N-2t+g+ceil(f/2)) = ? (should be <= 2 + ((f+g) mod 2))
mx = -10**9
for f in range(0, 60):
    for g in range(0, 60):
        for N in range(f, f + 80):
            for t in range(cdiv(f + g, 2) + 1, cdiv(f + g, 2) + 60):
                h = cdiv(f + g, 2)
                Qf = cdiv(f, 2) + max(0, N - f - 2 * (t - 1 - h))
                ex = Qf - max(cdiv(f, 2), N - 2 * t + g + cdiv(f, 2))
                assert ex <= 2 + ((f + g) % 2)
                mx = max(mx, ex)
print('(B3) nondegenerate: max excess =', mx, '(= 2 + parity bound)')
# degenerate: h >= t.  Only q <= min(t, N - 4 floor(N/7)) is available.
mxd = -10**9
arg = None
for f in range(0, 120):
    for g in range(0, 120):
        h = cdiv(f + g, 2)
        for t in range(1, h + 1):
            for N in range(f, f + 150):
                qb = min(t, N - 4 * (N // 7))
                ex = qb - max(cdiv(f, 2), N - 2 * t + g + cdiv(f, 2))
                if ex > mxd:
                    mxd, arg = ex, (f, g, t, N)
print('(B3) degenerate: max excess using min(t, Fano) =', mxd, 'at (f,g,t,N)=', arg)
