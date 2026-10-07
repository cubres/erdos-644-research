"""[typeclosed#2] TARGETED version of w9_ref_typeclosed2_unbal.py: seed the S_2 and S_1 minimisers with ZERO part-0
coordinate (so the REMARK hypothesis e_0 <= a_0 fails) and keep them minimisers during the repair; then test the
corner/V mechanism in every unbalanced orientation, and look for bad tuples (exact Fano search, exact V pairs,
attacker MILP as discovery fallback)."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *
from w9_ref_typeclosed2_unbal import mech, rnd

def gen(rng):
    den = rng.choice([20, 40])
    x = [rnd(rng, F(2, 5), F(9, 10), 40), rnd(rng, F(21, 20), F(27, 20), 40), rnd(rng, F(21, 20), F(27, 20), 40)]
    s1 = 2 * x[1] / 3 + rnd(rng, F(1, 200), F(1, 20), 10); s2 = 2 * x[2] / 3 + rnd(rng, F(1, 200), F(1, 20), 10)
    s0 = 2 * x[0] / 3 + rnd(rng, F(1, 200), F(1, 20), 10)
    if max(s1, s2) >= 1: return None
    a = (F(0), 1 - s2, s2); b = (F(0), s1, 1 - s1)
    if a[1] > x[1] or b[2] > x[2]: return None
    C = [a, b]
    floors = [s0, s1, s2]
    for it in range(40):
        T, t = tau_star(C, x)
        if T > F(3, 4): return x, C, T
        u = [t[m] if t[m] is not None else x[m] for m in range(3)]
        for _ in range(400):
            h = rng.randrange(3)
            lo = floors[h]; top = min(x[h], F(1))
            if top < lo: continue
            ch = lo + (top - lo) * F(rng.randint(0, den), den)
            o = [m for m in range(3) if m != h]; rng.shuffle(o)
            rem = 1 - ch
            if rem < 0: continue
            c = [F(0)] * 3; c[h] = ch
            v = min(rem, rnd(rng, 0, x[o[0]], den)); c[o[0]] = v; c[o[1]] = rem - v
            if any(c[m] < 0 or c[m] > x[m] for m in range(3)): continue
            if not all(c[m] < u[m] or (u[m] == x[m] and c[m] <= x[m]) for m in range(3)): continue
            if pencil_type(c, x): continue
            # keep a, b as minimisers: S_m types must have c_m >= floors[m]
            if any(3 * c[m] > 2 * x[m] and c[m] < floors[m] for m in range(3)): continue
            C.append(tuple(c)); break
        else:
            return None
    return None

if __name__ == '__main__':
    seed = int(sys.argv[1]); N = int(sys.argv[2])
    rng = random.Random(seed)
    st = dict(fam=0, unbal=0, remark=0, mech=0, neither=0, fano=0, V=0, milp_bad=0, milp_none=0, milp_unk=0)
    ex = []
    for trial in range(N):
        g = gen(rng)
        if g is None: continue
        x, C, T = g
        S, sig, e = super_classes(C, x)
        if not all(S): continue
        st['fam'] += 1
        orients = [(j, k) for j in range(3) for k in range(3) if j != k and e[j] + e[k] > F(3, 4)]
        if not orients: continue
        st['unbal'] += 1
        R = [mech(C, x, S, sig, e, j, k, T) for (j, k) in orients]
        if any(r[0] for r in R): st['remark'] += 1
        if any(r[1] for r in R): st['mech'] += 1; continue
        st['neither'] += 1
        if len(ex) < 3: ex.append((x, C, T, e, orients))
        if fano_search(C, x) is not None: st['fano'] += 1; continue
        if any(V_ok(p, q, x) for p in C for q in C): st['V'] += 1; continue
        from w4_typeclosed_lib import bad_tuple_milp
        s, _, _ = bad_tuple_milp(C, [float(v) for v in x], time_limit=120)
        st['milp_' + {'BAD': 'bad', 'NONE': 'none', 'UNKNOWN': 'unk'}[s]] += 1
        if s != 'BAD': print('NO BAD TUPLE FOUND', s, x, C, T, flush=True)
    print('seed', seed, st)
    for x, C, T, e, orients in ex:
        print('mechanism-fail example: x', [str(v) for v in x], 'tau*', T, 'e', [str(v) for v in e], 'orients', orients)
        for c in C: print('   ', [str(v) for v in c])
