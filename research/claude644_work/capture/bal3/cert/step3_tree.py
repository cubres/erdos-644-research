import sys; ARGS = list(sys.argv)
exec(open('mutual_tree2.py').read().split('X, Y = int(ARGS[1])')[0])
def total_fail(X, Y, Z, i):
    return row({'x' + P[i]: 4, tv(X, i): -4, tv(Y, i): -2, tv(Z, i): -1}, 0, True)
base = H + pat_ok(A, B) + pat_ok(A, C) + pat_ok(B, C)
NB2 = len(base)
which = ARGS[1]
if which == 'CC':
    rows = base + [total_fail(A, B, C, C)]
    c = exact_cert(rows)
    for k, l in c: print('  ', l, '*', fmt(rows[k]), '[BASE]' if k < len(BASE) else ('[H]' if k < NB else ('[PAT]' if k < NB2 else '[X]')))
else:
    i = {'A': A, 'B': B, 'C': C}[which]
    names = [s.strip() for s in ARGS[2].split(';')] if len(ARGS) > 2 and ARGS[2] else []
    tree(base + [total_fail(A, B, C, i)], names)
