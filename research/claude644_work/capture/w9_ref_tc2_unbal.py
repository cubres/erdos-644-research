# w9_ref_tc2_unbal.py -- referee [typeclosed#2]: does the UNBALANCED 3-class case (some e_j+e_k>3/4) really reduce to
# the notes' REMARK?  Search 3-part finite families with: every type super-heavy (fill>2/3) somewhere, tau*>3/4,
# tau*(C^(i))<=3/4 for all i (so Theorem L+ / Lemma E+ give nothing), some pair e_j+e_k>3/4, and the REMARK's side
# condition [exists S_k-minimiser a with e_i <= a_i <= 2x_i/3] FAILING for every unbalanced pair and both orientations.
import sys, random
from fractions import Fraction as F
from itertools import permutations
from w9_ref_tc2_lib import *
seed = int(sys.argv[1]); n = int(sys.argv[2])
rng = random.Random(seed)
TWO3 = F(2, 3); Q34 = F(3, 4)
stats = {}
def bump(k): stats[k] = stats.get(k, 0) + 1
found = []
for it in range(n):
    D = 40
    if len(sys.argv) > 3 and sys.argv[3] == 'target':
        xl = [F(rng.randint(4, 36), D), F(rng.randint(40, 60), D), F(rng.randint(40, 60), D)]
        rng.shuffle(xl); x = tuple(xl)
    else:
        x = tuple(F(rng.randint(int(0.2 * D), int(1.5 * D)), D) for _ in range(3))
    if sum(x) <= F(9, 4): continue
    C = []
    for _ in range(rng.randint(3, 8)):
        for _t in range(100):
            c = rand_type(rng, x, rng.choice([10, 12, 16, 20, 24]))
            if c is not None and any(c[i] > TWO3 * x[i] for i in range(3)):
                C.append(c); break
    C = list(set(C))
    S = [[c for c in C if c[i] > TWO3 * x[i]] for i in range(3)]
    if not all(S): continue
    ts = tau_star(C, x)
    if ts <= Q34: continue
    bump('tau>3/4, 3 classes')
    if any(tau_star([c for c in C if c[i] <= TWO3 * x[i]], x) > Q34 for i in range(3)): bump('L+ applies'); continue
    bump('E+ holds')
    sig = [min(c[i] for c in S[i]) for i in range(3)]
    e = [x[i] - sig[i] for i in range(3)]
    unbal = [(j, k) for j in range(3) for k in range(3) if j != k and e[j] + e[k] > Q34]
    if not unbal: bump('balanced'); continue
    bump('unbalanced')
    covered = False
    for (j, k) in unbal:
        i = 3 - j - k
        for a in [c for c in S[k] if c[k] == sig[k]]:
            if e[i] <= a[i] <= TWO3 * x[i]:
                covered = True
    if covered: bump('remark covers'); continue
    bump('REMARK FAILS')
    # what else works?  menu: V over all ordered pairs, Q over ordered pairs
    V_any = any(V_ok(a, c, x) for a in C for c in C)
    Q_any = any(Qb_ok(a, b, x) for a in C for b in C)
    if V_any: bump('  ...but some V pair works')
    if Q_any: bump('  ...but some Q pair works')
    if len(found) < 5: found.append((x, C, e, ts, V_any, Q_any))
print(stats)
for f in found:
    print("x=", f[0], "\n C=", f[1], "\n e=", f[2], " tau*=", f[3], " V_any", f[4], "Q_any", f[5])
