import sys; ARGS = list(sys.argv)
exec(open('three_type_structured.py').read().split('tot = {')[0])
def fmt(r):
    c, rhs, st = r
    return ' + '.join(f'{v}*{n}' for n, v in c.items()) + (' < ' if st else ' <= ') + str(rhs)
def tree(rows, names, depth=0, label='root'):
    D = [(nm, DD[nm]) for nm in names + PAIRMAPS]
    t, z, du = lp(rows)
    ind = '  ' * depth
    if t <= 1e-9:
        c = exact_cert(rows)
        print(ind + label + ' -> LEAF', 'cert-ok' if c else 'CERT FAIL')
        return
    best = None
    for nm, alts in D:
        if any(all(eval_row(r, z) for r in al) for al in alts): continue
        feas = [ai for ai, al in enumerate(alts) if lp(rows + al)[0] > 1e-9]
        if best is None or len(feas) < len(best[2]): best = (nm, alts, feas)
    if best is None: print(ind + label + ' OPEN'); return
    print(ind + label + ' split on ' + best[0])
    for ai, al in enumerate(best[1]):
        tree(rows + al, names, depth + 1, f'{best[0]}[{ai}]: ' + ' & '.join(fmt(r) for r in al))
X, Y = int(ARGS[1]), int(ARGS[2]); m1, m2 = int(ARGS[3]), int(ARGS[4]); vs = ARGS[5]
Z = 3 - X - Y
rows = H + [pat_fail(X, Y, m1), pat_fail(Y, X, m2)]
tree(rows, [vs] + [f'map {(v, v, v)}' for v in range(3)])
