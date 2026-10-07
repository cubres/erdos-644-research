"""mutual conflict {XXY,YYX} (balanced rigid representatives, 7 maps): for each failure-mode subcase find a single
V(S,T) all of whose 6 failure alternatives are LP-infeasible (then V(S,T) is forced)."""
exec(open('conflicts.py').read().split('A, B, C = 0, 1, 2')[0])
import itertools
A, B, C = 0, 1, 2
def V_fail_alts(S, T):
    out = []
    for i in range(3):
        s, t, xi = tv(S, i), tv(T, i), 'x' + P[i]
        out.append(row({xi: 1, s: -1, t: -1}, 0, True))
        out.append(row({xi: 1, s: F(-5, 4), t: F(-1, 2)}, 0, True))
    return out
for (X, Y) in [(A, B), (A, C), (B, C)]:
    for modes in itertools.product(range(2), repeat=2):
        pats = [(X, Y), (Y, X)]
        rows = H + [pat(a, b)[m] for (a, b), m in zip(pats, modes)]
        lab = ','.join(f"{P[a]}{P[a]}{P[b]}@{P[a] if m == 0 else P[b]}" for (a, b), m in zip(pats, modes))
        forced = []
        for S, T in itertools.permutations(range(3), 2):
            if all(lp(rows + [r])[0] <= 1e-9 for r in V_fail_alts(S, T)): forced.append(P[S] + P[T])
        print(lab, "forced V:", forced)
