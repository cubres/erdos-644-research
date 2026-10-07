# Referee w9, templates#2: directed test of the SURVIVOR step of Theorem H2 Case C (b* != b0).
# Seed example (hand-built by the referee): x=(32/25,32/25,9/100),
#   a0=(9/10,1/20,1/20), a1=(91/100,9/100,0), b0=(1/20,9/10,1/20), b1=(2/25,23/25,0):
#   tau*=19/25 >= 3/4, Case C, b0 incompatible with a0 at the light part (1/20+1/20 > 9/100), b*=b1.
# Then random perturbations of this pattern (random capacities/thresholds/extra types), exact checks via
# w9_ref_templates2_e2e.check (independent kill-map tau*, support-derived template functions).
import sys, random
from fractions import Fraction as F
seed = int(sys.argv[1]); NT = int(sys.argv[2])
sys.argv = [sys.argv[0], '0', '0', '0', 'V']
import w9_ref_templates2_e2e as E
stats = {'H': 0, 'Qb': 0, 'Qa': 0, 'V': 0}
x = [F(32, 25), F(32, 25), F(9, 100)]
T = [[F(9, 10), F(1, 20), F(1, 20)], [F(91, 100), F(9, 100), F(0)], [F(1, 20), F(9, 10), F(1, 20)], [F(2, 25), F(23, 25), F(0)]]
print('seed example tau* =', E.tau_star(x, T), 'result', E.check(x, T, stats), stats)
assert stats.get('V_bstar_ne_b0', 0) >= 1
rng = random.Random(seed)
def r(lo, hi, d=240): return lo + (hi - lo) * F(rng.randint(0, d), d)
n = hit = tries = 0; worst = None
while hit < NT and tries < 200000:
    tries += 1
    p = rng.choice([3, 3, 4])
    x = [r(F(11, 10), F(3, 2)), r(F(11, 10), F(3, 2))] + [r(F(1, 50), F(1, 4)) for _ in range(p - 2)]
    def mk(h, lo, lightfrac):
        t = [F(0)] * p
        t[h] = r(lo, min(x[h], F(1)))
        rest = 1 - t[h]
        for l in range(2, p):
            v = min(rest, 4 * x[l] / 7 * lightfrac); t[l] = v; rest -= v
        o = 1 - h
        if rest < 0 or 7 * rest > 4 * x[o]: return None
        t[o] = rest; return t
    th = [r(2 * x[0] / 3, min(x[0], F(1))), r(2 * x[1] / 3, min(x[1], F(1)))]
    T = []
    for h in (0, 1):
        t0 = mk(h, th[h], r(F(3, 5), F(1)))           # light-mass-rich argmin candidates
        t1 = mk(h, th[h], F(0))                        # light-free partners
        t2 = mk(h, th[h], r(F(0), F(1)))
        for t in (t0, t1, t2):
            if t is not None: T.append(t)
    T = [list(t) for t in dict.fromkeys(tuple(t) for t in T)]
    if len(T) < 3 or any(E.heavy(t, x, l) for t in T for l in range(2, p)): continue
    before = stats.get('V_bstar_ne_b0', 0)
    res = E.check(x, T, stats)
    if res is None: continue
    n += 1
    if stats.get('V_bstar_ne_b0', 0) > before:
        hit += 1
        if worst is None or res[1] < worst[0]: worst = (res[1], x, T)
print('tries', tries, 'tau*>=3/4 instances', n, 'V-case instances with b* != b0:', hit, stats)
if worst: print('min V slack among b*!=b0:', worst[0], float(worst[0]), worst[1], worst[2])
print('ALL CHECKS PASSED')
