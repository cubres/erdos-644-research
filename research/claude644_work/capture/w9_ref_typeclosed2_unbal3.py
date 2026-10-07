"""[typeclosed#2] broad random sampling (no repair) in the unbalanced 3-class regime; mechanism = REMARK corner
(u_i capped at sigma_i) and the UNCAPPED corner u=(x_i-a_i, x_j-a_j, sigma_k-eps) (cost 1-sigma_k+e_k < 3/4 always)
with ANY witness c (S_j or S_i) and V(a,c).  Records failures of each; failures of both are checked for bad tuples."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *

def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

def mech2(C, x, S, sig, e, j, k, T):
    i = 3 - j - k
    Ak = [a for a in S[k] if a[k] == sig[k]]
    rem = any(e[i] <= a[i] and 3 * a[i] <= 2 * x[i] for a in Ak)
    capped = uncapped = False
    for a in Ak:
        if max(a[i], e[i]) + a[j] + e[k] < T:
            cs = [c for c in C if c[i] <= x[i] - a[i] and c[i] < sig[i] and c[j] <= x[j] - a[j] and c[k] < sig[k]]
            assert cs and all(c in S[j] for c in cs)
            if any(V_ok(a, c, x) for c in cs): capped = True
        assert a[i] + a[j] + e[k] < F(3, 4) or a[k] != sig[k]
        cs = [c for c in C if c[i] <= x[i] - a[i] and c[j] <= x[j] - a[j] and c[k] < sig[k]]
        assert cs
        if any(V_ok(a, c, x) for c in cs): uncapped = True
    return rem, capped, uncapped

seed = int(sys.argv[1]); N = int(sys.argv[2])
rng = random.Random(seed)
st = dict(sampled=0, tau_gt=0, unbal=0, remark=0, capped=0, uncapped=0, none=0, fano=0, Vany=0, milp_bad=0, other=0)
for trial in range(N):
    den = rng.choice([10, 20, 40])
    x = [rnd(rng, F(1, 2), F(1), 40), rnd(rng, F(11, 10), F(3, 2), 40), rnd(rng, F(11, 10), F(3, 2), 40)]
    C = []
    for _ in range(rng.randint(3, 7)):
        for _t in range(100):
            h = rng.randrange(3); lo = 2 * x[h] / 3; top = min(x[h], F(1))
            if top <= lo: continue
            ch = lo + (top - lo) * F(rng.randint(1, den), den)
            o = [m for m in range(3) if m != h]; rng.shuffle(o)
            r = 1 - ch
            c = [F(0)] * 3; c[h] = ch
            v = r * F(rng.choice([0, 0, rng.randint(0, den)]), den); c[o[0]] = v; c[o[1]] = r - v
            if any(c[m] > x[m] for m in range(3)): continue
            C.append(tuple(c)); break
    st['sampled'] += 1
    S, sig, e = super_classes(C, x)
    if not all(S): continue
    orients = [(j, k) for j in range(3) for k in range(3) if j != k and e[j] + e[k] > F(3, 4)]
    if not orients: continue
    T, _ = tau_star(C, x)
    if T <= F(3, 4): continue
    st['tau_gt'] += 1; st['unbal'] += 1
    R = [mech2(C, x, S, sig, e, j, k, T) for (j, k) in orients]
    if any(r[0] for r in R): st['remark'] += 1
    if any(r[1] for r in R): st['capped'] += 1
    if any(r[2] for r in R): st['uncapped'] += 1
    if not any(r[1] or r[2] for r in R):
        st['none'] += 1
        print('MECH FAIL', [str(v) for v in x], [[str(v) for v in c] for c in C], T, flush=True)
        if fano_search(C, x) is not None: st['fano'] += 1
        elif any(V_ok(p, q, x) for p in C for q in C): st['Vany'] += 1
        else:
            from w4_typeclosed_lib import bad_tuple_milp
            s, _, _ = bad_tuple_milp(C, [float(v) for v in x], time_limit=120)
            if s == 'BAD': st['milp_bad'] += 1
            else: st['other'] += 1; print('NO BAD TUPLE FOUND', s, flush=True)
print('seed', seed, st)
