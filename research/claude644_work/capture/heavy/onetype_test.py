"""Reduced model, ONE type per heavy part: c^j heavy at j (c^j_j > 4x_j/7), other coords arbitrary in [0,x],
sum <= 1.  If tau*_H > 3/4: is T(A,B,C) (rows c^A x4 quad, c^B x2 pencil, c^C x1 pencil) feasible for some
ordered triple?  Also: any Fano at all?"""
import random, sys, itertools, heavylib as h
hh, N, seed, mode = map(int, sys.argv[1:5]); rng = random.Random(seed)
TPL = (0,0,1,0,1,2,0)   # lines 0,1,2 through point 0 get pattern (0,0,1)?? check below
# In LINES, lines through point 0 are 0,1,2.  TPL assigns: line0->A? we want quad lines (3,4,5,6)->A, pencil lines 0,1->B, 2->C
TPL = (1,1,2,0,0,0,0)
tested = tf = ff = 0
while tested < N:
    x = [rng.uniform(0.3, 1.5) for _ in range(hh)]
    T = []
    ok = True
    for j in range(hh):
        c = [0.0]*hh
        c[j] = rng.uniform(4*x[j]/7, min(x[j], 1.0))
        if c[j] <= 4*x[j]/7: ok = False; break
        rest = 1.0 - c[j] if mode == 1 else rng.uniform(0, 1.0 - c[j])
        w = [rng.random()**rng.choice([1,2,4]) if i != j else 0 for i in range(hh)]; S = sum(w)
        for i in range(hh):
            if i != j: c[i] = min(x[i], rest*w[i]/S)
        T.append(c)
    if not ok: continue
    t = h.tau_star_fast(x, T)
    if t <= 0.75: continue
    tested += 1
    good = any(h.fano_rows_ok(x, [T[(A,B,C)[k]] for k in TPL]) for A, B, C in itertools.permutations(range(hh), 3))
    if not good:
        tf += 1
        anyf = h.any_fano_np(x, T)
        if not anyf: ff += 1
        print("TFAIL tau*=%.4f anyFano=%s x=%s T=%s" % (t, anyf, [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
print(f"h={hh} mode={mode}: tested {tested}; template fails {tf}; Fano-free {ff}")
