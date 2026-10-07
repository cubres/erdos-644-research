"""[typeclosed#2] referee's partial repair, LEMMA U (hand proof in notes_referee_w9.md): 3 parts i,j,k, every type
super-heavy (>2/3 fill) somewhere, e_j+e_k > 3/4 (sigma_m = inf_{S_m} c_m, e = x - sigma).  Let a be an S_k-minimiser,
b an S_j-minimiser.  If a_i + b_i <= x_i then V(s,t) is feasible with s = the one of a,b with the smaller i-coordinate.
(Parts j,k by the L+ identities, NO tau* hypothesis used beyond e_j+e_k>3/4.)  Exact random test, plus the frequency
of the residual subcase a_i+b_i > x_i and whether the corner mechanisms cover it there."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *

def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

seed = int(sys.argv[1]); N = int(sys.argv[2])
rng = random.Random(seed)
st = dict(unbal=0, U_applies=0, U_ok=0, resid=0, resid_tau=0, resid_V=0, resid_fano=0)
for trial in range(N):
    den = rng.choice([10, 20, 40])
    x = [rnd(rng, F(1, 10), F(1), 40), rnd(rng, F(1), F(3, 2), 40), rnd(rng, F(1), F(3, 2), 40)]
    C = []
    for _ in range(rng.randint(2, 6)):
        for _t in range(100):
            h = rng.randrange(3); lo = 2 * x[h] / 3; top = min(x[h], F(1))
            if top <= lo: continue
            ch = lo + (top - lo) * F(rng.randint(1, den), den)
            o = [m for m in range(3) if m != h]; rng.shuffle(o)
            r = 1 - ch; c = [F(0)] * 3; c[h] = ch
            v = r * F(rng.randint(0, den), den); c[o[0]] = v; c[o[1]] = r - v
            if any(c[m] > x[m] for m in range(3)): continue
            C.append(tuple(c)); break
    S, sig, e = super_classes(C, x)
    for (j, k) in [(1, 2), (2, 1), (0, 1), (1, 0), (0, 2), (2, 0)]:
        i = 3 - j - k
        if not (S[j] and S[k] and e[j] + e[k] > F(3, 4)): continue
        st['unbal'] += 1
        for a in [c for c in S[k] if c[k] == sig[k]]:
            for b in [c for c in S[j] if c[j] == sig[j]]:
                if a[i] + b[i] <= x[i]:
                    st['U_applies'] += 1
                    s, t = (a, b) if a[i] <= b[i] else (b, a)
                    assert V_ok(s, t, x), (x, C, j, k, a, b)
                    st['U_ok'] += 1
                else:
                    st['resid'] += 1
                    T, _ = tau_star(C, x)
                    if T > F(3, 4):
                        st['resid_tau'] += 1
                        if any(V_ok(p, q, x) for p in C for q in C): st['resid_V'] += 1
                        elif fano_search(C, x) is not None: st['resid_fano'] += 1
                        else: print('RESID no V/Fano', [str(v) for v in x], C, flush=True)
print('seed', seed, st)
