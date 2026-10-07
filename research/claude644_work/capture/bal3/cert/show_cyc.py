exec(open('conflicts.py').read().split('A, B, C = 0, 1, 2')[0])
import itertools
A, B, C = 0, 1, 2
def fmt(r):
    c, rhs, st = r
    return ' + '.join(f'{v}*{n}' for n, v in c.items()) + (' < ' if st else ' <= ') + str(rhs)
for cyc in [[(A, B), (B, C), (C, A)]]:
    for modes in itertools.product(range(2), repeat=3):
        rows = H + [pat(X, Y)[m] for (X, Y), m in zip(cyc, modes)]
        cert = exact_cert(rows)
        print("==", [f"{P[X]}{P[X]}{P[Y]}@{P[X] if m == 0 else P[Y]}" for (X, Y), m in zip(cyc, modes)])
        for k, l in cert: print("   ", l, ' * ', fmt(rows[k]))
