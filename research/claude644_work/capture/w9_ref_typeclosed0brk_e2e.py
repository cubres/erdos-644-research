"""Referee w9 typeclosed#0 (BREAK-IT lens; prefix typeclosed0brk to avoid clobbering the other typeclosed#0 referee's
w9_ref_typeclosed0_*.py): literal end-to-end run of the Theorem L+ proof on finite (hence closed) rational type
sets, exact arithmetic, with my own tau* and my own explicit template masses + literal integer realisation.
Generators (mode):
  super     : parts j=0,k=1 heavy (x in (1.05,1.5)), light parts random; A-types just above 2x_1/3 at part 1,
              B-types just above 2x_0/3 at part 0; light coords <= 2x_i/3 (boundary 2x_i/3 hit often); some
              light-everywhere types (pencil branch).
  superonly : as super, no light-everywhere types (V branch only).
  p2        : two parts, arbitrary random types (hypothesis vacuous) -> instances of note Thm 7.75.
  gen       : random p in 2..4 with hypothesis enforced but no targeting.
  mass      : like super but types of mass <= 1 (stress: mass 1 is used only through upper bounds).
Every intermediate assertion of the proof is checked; any failure is printed with the family.
usage: python3 w9_ref_typeclosed0brk_e2e.py MODE SEED NFAMILIES"""
import random, sys, json
from fractions import Fraction as F
from w9_ref_typeclosed0brk_lib import *

def rnd(lo, hi, den):
    a = int(lo * den) + 1; b = int(hi * den)
    if a > b: return None
    return F(random.randint(a, b), den)

def split_mass(r, caps, den):
    """random split of mass r into len(caps) coords with coord i <= caps[i] (None if not found)."""
    for _ in range(50):
        v = [F(0)] * len(caps)
        rem = r
        order = list(range(len(caps))); random.shuffle(order)
        for idx, i in enumerate(order):
            if idx == len(order) - 1:
                v[i] = rem
            else:
                hi = min(caps[i], rem)
                v[i] = F(random.randint(0, int(hi * den)), den) if random.random() > 0.15 else min(caps[i], rem)
            rem -= v[i]
        if all(F(0) <= v[i] <= caps[i] for i in range(len(caps))):
            return v
    return None

def gen_family(mode, den):
    if mode == 'p2':
        p = 2
        x = [F(random.randint(den // 4, 7 * den // 4), den) for _ in range(p)]
        C = []
        for _ in range(random.randint(2, 7)):
            lo = max(F(0), 1 - x[1]); hi = min(F(1), x[0])
            if lo > hi: return None
            a = F(random.randint(int(lo * den) + (0 if (lo * den).denominator == 1 else 1), int(hi * den)), den)
            if not (lo <= a <= hi): continue
            C.append([a, 1 - a])
        return (x, C, 0, 1) if C else None
    p = random.randint(2, 5) if mode != 'gen' else random.randint(2, 4)
    if mode == 'gen':
        x = [F(random.randint(den // 5, 3 * den // 2), den) for _ in range(p)]
    else:
        x = [F(random.randint(int(1.05 * den), int(1.5 * den)), den) for _ in range(2)] + \
            [F(random.randint(0, 3 * den // 2), den) for _ in range(p - 2)]
    j, k = 0, 1
    caps_light = [2 * x[i] / 3 for i in range(p)]
    C = []
    for _ in range(random.randint(2, 7)):
        kind = random.random()
        massr = F(1) if mode != 'mass' else F(random.randint(den * 3 // 4, den), den)
        if mode == 'gen':
            caps = [x[i] if i in (j, k) else caps_light[i] for i in range(p)]
            v = split_mass(massr, caps, den)
            if v: C.append(v)
            continue
        if kind < (0.1 if mode != 'superonly' else -1):   # light everywhere (pencil branch)
            v = split_mass(massr, caps_light, den)
        else:
            h = k if kind < 0.55 else j
            lo = 2 * x[h] / 3
            hi = min(massr, x[h], lo + F(random.choice([1, 2, 5, 10]), 60))
            ch = rnd(lo, hi, den)
            if ch is None: continue
            caps = [x[i] if i == (j if h == k else k) else caps_light[i] for i in range(p)]
            caps[h] = F(0)
            rest = split_mass(massr - ch, caps, den)
            if rest is None: continue
            v = rest; v[h] = ch
        if v and all(F(0) <= v[i] <= x[i] for i in range(p)):
            C.append(v)
    return (x, C, j, k) if C else None

def check_hyp(x, C, j, k):
    return all(c[i] <= 2 * x[i] / 3 for c in C for i in range(len(x)) if i not in (j, k))

def run_proof(x, C, j, k, tau):
    """returns branch name; raises AssertionError on any failed step."""
    p = len(x)
    third = F(3, 4)
    assert tau > third
    # (0) pencil
    for e in C:
        if all(e[i] <= 2 * x[i] / 3 for i in range(p)):
            u = [x[i] - 3 * e[i] / 4 for i in range(p)]
            assert sum(x[i] - u[i] for i in range(p)) <= third * sum(e) <= third
            assert not is_free(C, u), 'pencil request u is free although cost<=3/4<tau*'
            f = next(c for c in C if all(c[i] <= u[i] for i in range(p)))
            rows = [e, e, e, f, f, f, f]
            good, msg = realise_and_check(rows, x, [pencil_masses(e[i], f[i]) for i in range(p)])
            assert good, 'pencil realisation failed: ' + msg
            return 'pencil'
    A = [c for c in C if c[k] > 2 * x[k] / 3]
    B = [c for c in C if c[j] > 2 * x[j] / 3]
    assert all(c in A or c in B for c in C), 'a type is super-heavy nowhere in {j,k}'
    assert A and B, 'class empty but tau*>3/4'
    sk = min(c[k] for c in A); sj = min(c[j] for c in B)
    ej, ek = x[j] - sj, x[k] - sk
    assert not any(c[j] < sj and c[k] < sk for c in C)       # (sj-eps, sk-eps, x elsewhere) is free
    assert ej + ek >= tau > third, 'e_j+e_k >= tau* failed'
    assert x[j] + x[k] > F(9, 4) and x[j] <= F(3, 2) and x[k] <= F(3, 2) and x[j] > third and x[k] > third
    assert not any(c in A and c in B for c in C)
    a = min(A, key=lambda c: c[k])                            # finite: minimiser attained (eta = 0)
    cost = (sum(a) - a[k]) + ek                               # + eps
    assert cost <= 1 + x[k] - 2 * sk and 1 + x[k] - 2 * sk <= 1 - x[k] / 3 and 1 - x[k] / 3 < third
    wit = [c for c in C if all(c[i] <= x[i] - a[i] for i in range(p) if i != k) and c[k] < sk]
    assert wit, 'no witness c <= u although cost(u) < 3/4 < tau*'
    for c in wit:   # EVERY witness must work (the proof takes an arbitrary one)
        assert c in B and c[j] >= sj and c[k] <= 1 - sj
        for i in range(p):
            if i == k: continue
            assert a[i] + c[i] <= x[i]
            assert 5 * a[i] / 4 + c[i] / 2 <= x[i], ('V facet part', i)
        assert a[j] <= 1 - sk <= 1 - 2 * x[k] / 3 < 2 * x[j] / 3
        I1 = (ej + ek - third) + 2 * (sj - 2 * x[j] / 3) + (x[j] - third) / 3
        I2 = (ej + ek - third) + (1 - sk) / 4 + F(3, 2) * (sj - 2 * x[j] / 3)
        assert I1 == x[k] - sk - (1 - sj) and I2 == x[k] - 5 * sk / 4 - (1 - sj) / 2
        assert I1 > 0 and I2 > 0
        assert a[k] + c[k] <= x[k] and 5 * a[k] / 4 + c[k] / 2 <= x[k]
        rows = [c, c, a, a, a, a, a]
        good, msg = realise_and_check(rows, x, [V_masses(a[i], c[i]) for i in range(p)])
        assert good, 'V realisation failed: ' + msg
    return 'V'

def main():
    mode = sys.argv[1]; seed = int(sys.argv[2]); target = int(sys.argv[3])
    random.seed(seed)
    stats = {}
    tried = 0
    while sum(stats.values()) < target:
        tried += 1
        den = random.choice([12, 24, 30, 36, 60, 120])
        g = gen_family(mode, den)
        if g is None: continue
        x, C, j, k = g
        Cs = []
        for c in C:
            if c not in Cs: Cs.append(c)
        C = Cs
        if not check_hyp(x, C, j, k): continue
        tau = tau_star(C, x)
        if tau is None or tau <= F(3, 4): continue
        try:
            br = run_proof(x, C, j, k, tau)
        except AssertionError as ex:
            print('FAIL', ex, json.dumps({'x': [str(v) for v in x], 'C': [[str(v) for v in c] for c in C],
                                          'tau': str(tau)}), flush=True)
            br = 'FAIL'
        stats[br] = stats.get(br, 0) + 1
    print('mode', mode, 'seed', seed, 'families tried', tried, 'tau*>3/4 families:', stats, flush=True)

if __name__ == '__main__':
    main()
