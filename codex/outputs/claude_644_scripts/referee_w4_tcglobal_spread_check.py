# Referee check (w4, tcglobal spread lemma). Exact arithmetic.
# (1) For e = 2 mod 4 and s = 0 (t-1 = e/2), no quartering with E1uE3=P, E2uE4=P' (|P|=|P'|=e/2)
#     satisfies |E1uE4|,|E2uE3|<=t-1 AND |E1uE2|,|E3uE4|<=t-1 (oracle existence of b1,b2).
# (2) Double star counterexample to the Corollary as stated (rank <= k, e=2, t=2).
from itertools import combinations
from fractions import Fraction as Fr

def quarter_ok(a, b, t):
    sols = []
    for E1 in range(a+1):
        E3 = a-E1
        for E2 in range(b+1):
            E4 = b-E2
            if max(E1+E4, E2+E3) <= t-1 and max(E1+E2, E3+E4) <= t-1:
                sols.append((E1,E2,E3,E4))
    return sols

print("(1) quartering feasibility with oracle b1,b2, s=0:")
for e in range(2, 31):
    a = e//2; b = e-a; t = -(-e//2) + 1
    print(f"  e={e:2d} (e mod 4={e%4}) t={t}: feasible={bool(quarter_ok(a,b,t))}")
    if e % 4 == 2: assert not quarter_ok(a,b,t)
    else: assert quarter_ok(a,b,t)
# with s>=1 always feasible
for e in range(1, 60):
    a=e//2; b=e-a; t=-(-e//2)+2
    assert quarter_ok(a,b,t)
print("  s>=1: always feasible (e<60)")

print("(2) double star")
k = 2; L = 4*k+1
x, y = 'x', 'y'
H = [frozenset({x,y})] + [frozenset({x,f'a{i}'}) for i in range(L)] + [frozenset({y,f'b{i}'}) for i in range(L)]
V = sorted(set().union(*H))
def tau(F):
    for r in range(len(V)+1):
        for T in combinations(V, r):
            Ts=set(T)
            if all(Ts & G for G in F): return r
t = tau(H); print("  tau =", t)
bad = 0
for S in combinations(H, 7):
    if not any(all((u in G) or (w in G) for G in S) for u in V for w in V):
        bad += 1
print("  bad 7-subsets:", bad, "(0 => (7,2))")
E0 = H[0]; e = len(E0); P = {x}; Pp = {y}
OP = [G - E0 for G in H if (G & E0) <= P]
OPp = [G - E0 for G in H if (G & E0) <= Pp]
# outside parts are pairwise disjoint nonempty singletons -> nu* = count (exact: weight 1 each is feasible; cover by all points = count)
assert all(len(o)==1 for o in OP+OPp) and len(set().union(*OP))==len(OP)
nuP, nuPp = len(OP), len(OPp)
lhs = Fr(1,nuP)+Fr(1,nuPp); rhs = Fr(t - (-(-e//2)), 2*k)
print(f"  nu*(O_P)={nuP}, nu*(O_P')={nuPp}, LHS={lhs}, RHS={rhs}, corollary holds? {lhs>=rhs}")
print(f"  'in particular' bound ceil(e/2)+k/4 = {Fr(-(-e//2))+Fr(k,4)} vs t={t}")
