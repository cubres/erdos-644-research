"""[typeclosed#2] significance test: is the UNBALANCED 3-class case (some e_j+e_k > 3/4) really closed?
Only mechanism on record: REMARK (notes_typeclosed ~10:25): a = S_k minimiser, corner
u = (min(x_i-a_i, sigma_i-eps), x_j-a_j, sigma_k-eps) -> witness c in S_j -> V(a,c); proved only under the extra
hypothesis e_i <= a_i <= 2x_i/3.  We search (repair adversary, exact) for 3-part families with
  every type super-heavy somewhere, all S_i nonempty, tau* > 3/4, max_{j<k} e_j+e_k > 3/4,
and record (A) whether the REMARK hypothesis holds for some unbalanced orientation, (B) whether the mechanism
itself (corner cost < tau*, some witness c with V(a,c)) succeeds for some orientation and some minimiser a.
If neither, we look for a bad tuple: exhaustive Fano search (exact), all ordered V pairs (exact), else the attacker's
all-support MILP (discovery only)."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *

def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

def mech(C, x, S, sig, e, j, k, T):
    i = 3 - j - k
    Ak = [a for a in S[k] if a[k] == sig[k]]
    remark = any(e[i] <= a[i] and 3 * a[i] <= 2 * x[i] for a in Ak)
    ok = False
    for a in Ak:
        # u_i = min(x_i - a_i, sigma_i - eps): c_i <= x_i - a_i and c_i < sigma_i
        cost = max(a[i], e[i]) + a[j] + e[k]      # + eps (strict inequality below handles it)
        if not cost < T: continue
        cs = [c for c in C if c[i] <= x[i] - a[i] and c[i] < sig[i] and c[j] <= x[j] - a[j] and c[k] < sig[k]]
        assert cs and all(c in S[j] for c in cs)
        if any(V_ok(a, c, x) for c in cs):
            ok = True; break
    return remark, ok

def gen(rng):
    den = rng.choice([10, 20, 40])
    sm = rng.randrange(3)
    x = [None] * 3
    for m in range(3):
        x[m] = rnd(rng, F(1, 5), F(1), 40) if m == sm else rnd(rng, F(1), F(3, 2), 40)
    C = []
    for it in range(40):
        if C:
            T, t = tau_star(C, x)
            if T > F(3, 4): return x, C, T
            u = [t[m] if t[m] is not None else x[m] for m in range(3)]   # need c_m < t_m (finite) / <= x_m
        else:
            u = list(x)
        # random non-pencil type below the current optimal corner
        for _ in range(300):
            h = rng.randrange(3)
            lo = 2 * x[h] / 3
            top = min(u[h], x[h], F(1))
            if top <= lo: continue
            ch = lo + (top - lo) * F(rng.randint(1, den), den)
            if ch >= u[h] and u[h] < x[h] or ch == lo: continue
            o = [m for m in range(3) if m != h]; rng.shuffle(o)
            rem = 1 - ch
            c = [F(0)] * 3; c[h] = ch
            v = min(rem, rnd(rng, 0, min(u[o[0]], x[o[0]]), den))
            c[o[0]] = v; c[o[1]] = rem - v
            if any(c[m] < 0 or c[m] > x[m] for m in range(3)): continue
            if any(C and c[m] >= u[m] and u[m] < x[m] for m in range(3)): continue
            if pencil_type(c, x): continue
            C.append(tuple(c)); break
        else:
            return None
    return None

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
    if len(ex) < 5: ex.append((x, C, T, e))
    if fano_search(C, x) is not None: st['fano'] += 1; continue
    if any(V_ok(a, b, x) for a in C for b in C): st['V'] += 1; continue
    from w4_typeclosed_lib import bad_tuple_milp
    s, _, _ = bad_tuple_milp(C, [float(v) for v in x], time_limit=120)
    st['milp_' + {'BAD': 'bad', 'NONE': 'none', 'UNKNOWN': 'unk'}[s]] += 1
    if s != 'BAD':
        print('NO BAD TUPLE FOUND', s, x, C, T, flush=True)
print('seed', seed, st)
for x, C, T, e in ex[:3]:
    print('mechanism-fail example: x', [str(v) for v in x], 'tau*', T, 'e', [str(v) for v in e])
    for c in C: print('   ', [str(v) for v in c])
