# w9_ref_tc2_example.py -- referee [typeclosed#2]: explicit UNBALANCED 3-class family satisfying Lemma E+ for all i
# (so Theorem L+ gives nothing) in which the notes' REMARK (partial 3-class extension) fails in every orientation.
# Shows that "what remains open for Th(3) is the balanced case" is NOT established by the stated arguments.
from fractions import Fraction as F
import random
from w9_ref_tc2_lib import *
x = (F(59, 40), F(13, 40), F(39, 40))
C = [(F(5,24),F(0),F(19,24)), (F(0),F(1,4),F(3,4)), (F(5,24),F(1,24),F(3,4)), (F(5,16),F(5,16),F(3,8)),
     (F(1),F(0),F(0)), (F(1,8),F(5,16),F(9,16)), (F(1,12),F(1,4),F(2,3))]
assert all(sum(c) == 1 and all(0 <= c[i] <= x[i] for i in range(3)) for c in C)
T23 = F(2, 3)
S = [[c for c in C if c[i] > T23 * x[i]] for i in range(3)]
print("every type super-heavy somewhere:", all(any(c[i] > T23 * x[i] for i in range(3)) for c in C))
ts = tau_star(C, x); print("tau* =", ts, ">3/4:", ts > F(3, 4))
# Monte-Carlo sanity of tau*: no random free u cheaper than tau*
rng = random.Random(0)
for _ in range(200000):
    u = tuple(F(rng.randint(0, 400), 400) * x[i] for i in range(3))
    if not any(all(c[i] <= u[i] for i in range(3)) for c in C):
        assert sum(x) - sum(u) >= ts
sig = [min(c[i] for c in S[i]) for i in range(3)]; e = [x[i] - sig[i] for i in range(3)]
print("sigma =", sig, " e =", e)
for i in range(3):
    print(f" tau*(C^({i})) =", tau_star([c for c in C if c[i] <= T23 * x[i]], x))
for j in range(3):
    for k in range(3):
        if j != k and e[j] + e[k] > F(3, 4):
            i = 3 - j - k
            mins = [c for c in S[k] if c[k] == sig[k]]
            print(f" unbalanced (j,k)=({j},{k}) e_j+e_k={e[j]+e[k]}; S_{k}-minimisers {mins}: need e_{i}={e[i]} <= a_{i} <= {T23*x[i]}:",
                  [e[i] <= a[i] <= T23 * x[i] for a in mins])
print(" V pairs (a on 5 rows, c on 2 rows) that work:", [(C.index(a), C.index(c)) for a in C for c in C if V_ok(a, c, x)])
print(" types in two super classes:", [c for c in C if sum(c[i] > T23 * x[i] for i in range(3)) > 1])
