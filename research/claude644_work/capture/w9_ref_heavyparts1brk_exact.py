"""Referee w9, claim heavyparts#1 (BREAK-IT lens). Exact (Fraction) tests of
  (A) at a 4/7-light part every Lemma 7.63 inequality holds, so for EVERY row assignment
      feasible(all parts) == feasible(heavy parts only)   [assignment level, stronger than existence]
  (B) tau*(reduced model: light parts deleted, types restricted to H) >= tau*(original),
      computed by two independent exact methods:
        M1: blocking maps  sup = max_pi sum_i min(x_i, min_{pi(a)=i} a_i), pi(a) in supp(a)
        M2: grid enumeration of candidate u (coordinates in {a_i} u {x_i}) with the limit-free test
            'for every a there is i with a_i>0 and u_i <= a_i'.
  (C) mutation: replace the light threshold 4/7 by 4/7+1/50, 3/5, 2/3 -> (A) must FAIL somewhere (power check).
Independent of heavylib: rows are indexed by Fano POINTS (note Lemma 7.63 orientation), constraints on LINES.
Usage: python3 w9_ref_heavyparts1brk_exact.py SEED N [thr_num thr_den]
"""
import sys, random, itertools
from fractions import Fraction as F

LINES = [(0,1,3),(1,2,4),(2,3,5),(3,4,6),(4,5,0),(5,6,1),(6,0,2)]  # cyclic difference set {0,1,3} mod 7
assert all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2))

def part_ok(z, x):
    """Lemma 7.63 in one part: max z <= x, line sums <= 2x, total <= 4x."""
    if max(z) > x: return False
    if sum(z) > 4*x: return False
    for L in LINES:
        if z[L[0]] + z[L[1]] + z[L[2]] > 2*x: return False
    return True

def asg_ok(x, T, asg, parts):
    return all(part_ok([T[j][i] for j in asg], x[i]) for i in parts)

def tau_M1(x, T, parts):
    X = sum(x[i] for i in parts); best = None
    ch = [[i for i in parts if a[i] > 0] for a in T]
    if any(len(c) == 0 for c in ch): return None   # a type with zero trace on 'parts': nothing free -> +inf
    for pi in itertools.product(*ch):
        caps = {i: x[i] for i in parts}
        for j, i in enumerate(pi): caps[i] = min(caps[i], T[j][i])
        s = sum(caps.values())
        if best is None or s > best: best = s
    return X - best

def tau_M2(x, T, parts):
    X = sum(x[i] for i in parts)
    if any(all(a[i] == 0 for i in parts) for a in T): return None
    cand = [sorted(set([x[i]] + [a[i] for a in T if 0 < a[i] <= x[i]])) for i in parts]
    best = None
    for u in itertools.product(*cand):
        ud = dict(zip(parts, u))
        if all(any(a[i] > 0 and ud[i] <= a[i] for i in parts) for a in T):
            s = sum(u)
            if best is None or s > best: best = s
    return X - best

def rnd_frac(rng, lo, hi, den=None):
    den = den or rng.choice([7, 20, 28, 60, 100, 140, 1000])
    a = int(lo*den) ; b = int(hi*den)
    if b < a: b = a
    return F(rng.randint(a, b), den)

def gen0(rng, thr):
    """random instance: p parts, some designated light (all traces <= thr*x_j, often ON the boundary),
    types with sum exactly 1 (rank 1) or <= 1; tiny parts, zero traces, zero capacities included."""
    p = rng.randint(2, 5); m = rng.randint(1, 4)
    nlight = rng.randint(1, p-1) if rng.random() < 0.9 else p
    light = set(rng.sample(range(p), nlight))
    x = []
    for i in range(p):
        r = rng.random() if i in light else 0.3 + 0.7*rng.random()
        if r < 0.1: x.append(F(0))
        elif r < 0.25: x.append(rnd_frac(rng, 0.001, 0.05))
        else: x.append(rnd_frac(rng, 0.2, 1.6))
    T = []
    for _ in range(m):
        a = [F(0)]*p
        for j in light:
            r = rng.random(); cap = thr*x[j]
            if r < 0.35: a[j] = cap                      # boundary: exactly thr*x
            elif r < 0.5: a[j] = F(0)
            else: a[j] = cap * rnd_frac(rng, 0, 1)
        heavy = [i for i in range(p) if i not in light]
        # fill heavy parts with the rest of the unit mass (clip at capacity), sometimes leave sub-stochastic
        rest = 1 - sum(a)
        if rest < 0:   # scale light traces down
            sc = F(1) / sum(a); a = [v*sc for v in a]; rest = F(0)
        rng.shuffle(heavy)
        for idx, i in enumerate(heavy):
            if idx == len(heavy)-1: v = min(rest, x[i])
            else: v = min(rest, x[i]) * rnd_frac(rng, 0.3, 1)
            a[i] = v; rest -= v
        if rest > 0 and rng.random() < 0.5:     # make it stochastic again by topping up light parts to <= thr*x
            for j in light:
                add = min(rest, thr*x[j] - a[j]); a[j] += add; rest -= add
        T.append(a)
    return x, T

def gen(rng, thr):
    while True:
        x, T = gen0(rng, thr)
        H = [i for i in range(len(x)) if any(a[i] > thr*x[i] for a in T)]
        if H or rng.random() < 0.05: return x, T

def light_parts(x, T, thr):
    return [j for j in range(len(x)) if all(a[j] <= thr*x[j] for a in T)]

def main():
    seed = int(sys.argv[1]); N = int(sys.argv[2])
    thr = F(int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else F(4, 7)
    rng = random.Random(seed)
    stats = dict(inst=0, asg=0, asg_feas=0, inst_fano=0, A_fail=0, B_fail=0, M_disagree=0,
                 strict_gain=0, zeroH=0, allLight=0, gain_over_34=0)
    maxgain = F(0); first_fail = None
    for _ in range(N):
        x, T = gen(rng, thr)
        p = len(x); m = len(T)
        Lt = light_parts(x, T, thr); Hp = [i for i in range(p) if i not in Lt]
        stats['inst'] += 1
        if not Hp: stats['allLight'] += 1
        anyf = False
        for asg in itertools.product(range(m), repeat=7):
            stats['asg'] += 1
            full = asg_ok(x, T, asg, range(p)); red = asg_ok(x, T, asg, Hp)
            if full: stats['asg_feas'] += 1; anyf = True
            if full != red:
                stats['A_fail'] += 1
                if first_fail is None: first_fail = (x, T, asg, Lt)
        stats['inst_fano'] += anyf
        # tau* checks (only if the original has no zero-support type, i.e. well-defined)
        t1 = tau_M1(x, T, list(range(p))); t2 = tau_M2(x, T, list(range(p)))
        if t1 != t2: stats['M_disagree'] += 1
        if t1 is None: continue
        r1 = tau_M1(x, T, Hp); r2 = tau_M2(x, T, Hp)
        if r1 != r2: stats['M_disagree'] += 1
        if r1 is None:
            stats['zeroH'] += 1
            # a type with zero H-trace is 4/7-light everywhere -> homogeneous Fano must exist
            if thr <= F(4, 7) and not anyf: stats['A_fail'] += 1
            continue
        if r1 < t1:
            stats['B_fail'] += 1
            if first_fail is None: first_fail = ('B', x, T, Lt, t1, r1)
        if r1 > t1:
            stats['strict_gain'] += 1; maxgain = max(maxgain, r1 - t1)
            if t1 <= F(3, 4) < r1: stats['gain_over_34'] += 1
    print('thr', thr, stats, 'max tau* gain', maxgain, float(maxgain))
    if first_fail: print('FIRST FAIL', first_fail)

if __name__ == '__main__':
    main()
