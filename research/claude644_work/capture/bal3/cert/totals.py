"""T(A;B,B;C) pattern-feasible (AAB, AAC, BBC hold at all parts) but a total fails: which single template is forced
(each failure alternative LP-infeasible) using the 7 maps only?"""
exec(open('conflicts.py').read().split('A, B, C = 0, 1, 2')[0])
import itertools
A, B, C = 0, 1, 2
def pat_ok(X, Y):   # XXY holds at X and at Y (third part automatic)
    return [row({tv(Y, X): 1, 'x' + P[X]: -2, 's' + P[X]: 2}, 0), row({tv(X, Y): 1, 'x' + P[Y]: -1, 's' + P[Y]: F(1, 2)}, 0)]
def total_fail(X, Y, Z, i):   # 4X+2Y+Z > 4x at part i
    return row({'x' + P[i]: 4, tv(X, i): -4, tv(Y, i): -2, tv(Z, i): -1}, 0, True)
def T_fail_alts(X, Y, Z):
    out = []
    for i in range(3):
        a, b, c, xi = tv(X, i), tv(Y, i), tv(Z, i), 'x' + P[i]
        for d in [{a: 2, b: 1}, {a: 2, c: 1}, {b: 2, c: 1}]:
            dd = {k: -v for k, v in d.items()}; dd[xi] = 2; out.append(row(dd, 0, True))
        out.append(row({xi: 4, a: -4, b: -2, c: -1}, 0, True))
    return out
def V_fail_alts(S, T):
    out = []
    for i in range(3):
        s, t, xi = tv(S, i), tv(T, i), 'x' + P[i]
        out += [row({xi: 1, s: -1, t: -1}, 0, True), row({xi: 1, s: F(-5, 4), t: F(-1, 2)}, 0, True)]
    return out
base = H + pat_ok(A, B) + pat_ok(A, C) + pat_ok(B, C)
print("T(A;B,B;C) pattern-OK: its totals can fail?")
for i in range(3):
    rows = base + [total_fail(A, B, C, i)]
    t = lp(rows)[0]
    if t <= 1e-9: print(" total at", P[i], "cannot fail"); continue
    forced = []
    for X, Y, Z in itertools.permutations(range(3)):
        if all(lp(rows + [r])[0] <= 1e-9 for r in T_fail_alts(X, Y, Z)): forced.append('T' + P[X] + P[Y] + P[Z])
    for S, T in itertools.permutations(range(3), 2):
        if all(lp(rows + [r])[0] <= 1e-9 for r in V_fail_alts(S, T)): forced.append('V' + P[S] + P[T])
    print(" total at", P[i], "can fail (slack %.4f); forced templates:" % t, forced)
