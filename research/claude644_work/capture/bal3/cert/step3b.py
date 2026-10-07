"""Step 3 of the structured human proof of 3T (balanced): no conflict, T(A;B,B;C) pattern-feasible.
Named facts; DFS over named disjunctions; leaves printed as Farkas combinations of named facts (exact)."""
import sys; ARGS = list(sys.argv)
exec(open('three_type_cert.py').read().split('STATS = ')[0].replace("XMIN = F(sys.argv[1]) if len(sys.argv) > 1 else F(0)", "XMIN = F(0)").replace("BAL = int(sys.argv[2]) if len(sys.argv) > 2 else 0", "BAL = 1"))
P = 'ABC'; A, B, C = 0, 1, 2
NAMED = []   # (name, row)
def fact(name, d, rhs, strict=False): NAMED.append((name, row(d, rhs, strict)))
for i in range(3):
    X = P[i]
    fact(f'x{X}<=3/2', {'x'+X: 1}, F(3, 2)); fact(f's{X}>=2x{X}/3', {'x'+X: F(2, 3), 's'+X: -1}, 0)
    fact(f's{X}<=x{X}', {'s'+X: 1, 'x'+X: -1}, 0); fact(f's{X}<=1', {'s'+X: 1}, 1); fact(f'x{X}>=0', {'x'+X: -1}, 0)
for r in range(3):
    s = {}
    for i in range(3):
        v = tv(r, i); s[v] = 1
        if r != i:
            fact(f'{v}>=0', {v: -1}, 0)
            fact(f'{v}<=2x{P[i]}/3', {v: 1, 'x'+P[i]: F(-2, 3)}, 0)     # simple types (Lemma 0)
    fact(f'sum({"abc"[r]})=1 (<=)', s, 1); fact(f'sum({"abc"[r]})=1 (>=)', {k: -1 for k in s}, -1)
fact('tau>3/4', {'tau': -1}, F(-3, 4), True)
for i, j in itertools.combinations(range(3), 2):
    fact(f'bal e{P[i]}+e{P[j]}<=3/4', {'x'+P[i]: 1, 's'+P[i]: -1, 'x'+P[j]: 1, 's'+P[j]: -1}, F(3, 4))
fact('id: tau<=eA+eB+eC', {'tau': 1, 'xA': -1, 'sA': 1, 'xB': -1, 'sB': 1, 'xC': -1, 'sC': 1}, 0)
# pattern OK (no conflict, T(A;B,B;C) pattern-feasible)
fact('AAB@A: bA<=2eA', {'bA': 1, 'xA': -2, 'sA': 2}, 0); fact('AAB@B: aB<=eB+sB/2', {'aB': 1, 'xB': -1, 'sB': F(1, 2)}, 0)
fact('AAC@A: cA<=2eA', {'cA': 1, 'xA': -2, 'sA': 2}, 0); fact('AAC@C: aC<=eC+sC/2', {'aC': 1, 'xC': -1, 'sC': F(1, 2)}, 0)
fact('BBC@B: cB<=2eB', {'cB': 1, 'xB': -2, 'sB': 2}, 0); fact('BBC@C: bC<=eC+sC/2', {'bC': 1, 'xC': -1, 'sC': F(1, 2)}, 0)
def pm(Y, X):   # pair map P(Y->X): tau <= x_X - y_X + e_Z
    Z = 3 - X - Y; y = tv(Y, X)
    return (f'P({P[Y]}->{P[X]})', [[(f'P({P[Y]}->{P[X]}): tau<=x{P[X]}-{y}+e{P[Z]}', row({'tau': 1, 'x'+P[X]: -1, y: 1, 'x'+P[Z]: -1, 's'+P[Z]: 1}, 0))],
                                    [(f'{y}=0', row({y: 1}, 0))]])
def allat(X):
    Y, Z = [i for i in range(3) if i != X]; y, z = tv(Y, X), tv(Z, X)
    return (f'ALL@{P[X]}', [[(f'ALL@{P[X]}: {y}<=x{P[X]}-tau', row({y: 1, 'x'+P[X]: -1, 'tau': 1}, 0))],
                           [(f'ALL@{P[X]}: {z}<=x{P[X]}-tau', row({z: 1, 'x'+P[X]: -1, 'tau': 1}, 0))],
                           [(f'{y}=0', row({y: 1}, 0))], [(f'{z}=0', row({z: 1}, 0))]])
def tmplT(X, Y, Z):
    alts = []
    for i in range(3):
        a, b, c, x = tv(X, i), tv(Y, i), tv(Z, i), 'x' + P[i]
        for nm, d in [(f'2{a}+{b}>2{x}', {a: 2, b: 1, x: -2}), (f'2{a}+{c}>2{x}', {a: 2, c: 1, x: -2}), (f'2{b}+{c}>2{x}', {b: 2, c: 1, x: -2}),
                      (f'4{a}+2{b}+{c}>4{x}', {a: 4, b: 2, c: 1, x: -4})]:
            alts.append([(f'T({P[X]};{P[Y]},{P[Y]};{P[Z]}) fails: ' + nm, row({k: -w for k, w in d.items()}, 0, True))])
    return (f'T({P[X]};{P[Y]},{P[Y]};{P[Z]})', alts)
def tmplV(S, T_):
    alts = []
    for i in range(3):
        s, t, x = tv(S, i), tv(T_, i), 'x' + P[i]
        alts.append([(f'V({P[S]},{P[T_]}) fails: {s}+{t}>{x}', row({s: -1, t: -1, x: 1}, 0, True))])
        alts.append([(f'V({P[S]},{P[T_]}) fails: 5{s}/4+{t}/2>{x}', row({s: F(-5, 4), t: F(-1, 2), x: 1}, 0, True))])
    return (f'V({P[S]},{P[T_]})', alts)
DISJS = {}
for Y in range(3):
    for X in range(3):
        if X != Y: n, a = pm(Y, X); DISJS[n] = a
for X in range(3): n, a = allat(X); DISJS[n] = a
for X, Y, Z in itertools.permutations(range(3)): n, a = tmplT(X, Y, Z); DISJS[n] = a
for S, T_ in itertools.permutations(range(3), 2): n, a = tmplV(S, T_); DISJS[n] = a
LEAVES = [0]
def leaf(named, ind):
    rows = [r for _, r in named]
    c = exact_cert(rows)
    if c is None: print(ind + '   CERT FAIL'); return False
    LEAVES[0] += 1
    print(ind + '   Farkas: ' + ' + '.join(f'{l}*[{named[k][0]}]' for k, l in c))
    return True
def tree(named, menu, ind='', label='root'):
    rows = [r for _, r in named]
    t, z, du = lp(rows)
    if t <= 1e-9:
        print(ind + label + ' -> CONTRADICTION'); leaf(named, ind); return
    best = None
    for nm in menu:
        alts = DISJS[nm]
        if any(all(eval_row(r, z) for _, r in al) for al in alts): continue
        feas = [ai for ai, al in enumerate(alts) if lp(rows + [r for _, r in al])[0] > 1e-9]
        if best is None or len(feas) < len(best[2]): best = (nm, alts, feas)
    if best is None: print(ind + label + ' OPEN  point:', dict(zip(V, [round(v, 4) for v in z]))); return
    nm, alts, feas = best
    if nm.startswith('T(') or nm.startswith('V('):
        print(ind + label + f' ; if {nm} is feasible we are done; else one of its inequalities fails:')
    else:
        print(ind + label + f' ; use {nm}:')
    for ai, al in enumerate(alts):
        tree(named + al, menu, ind + '    ', ' & '.join(n for n, _ in al))
case = ARGS[1]; menu = ARGS[2].split('|')
extra = []
if case == 'TB':
    extra = [('(TB) fails: 4aB+2sB+cB>4xB', row({'xB': 4, 'aB': -4, 'sB': -2, 'cB': -1}, 0, True))]
elif case == 'TA':
    extra = [('(TA) fails: 4sA+2bA+cA>4xA', row({'xA': 4, 'sA': -4, 'bA': -2, 'cA': -1}, 0, True)),
             ('(TB) holds', row({'xB': -4, 'aB': 4, 'sB': 2, 'cB': 1}, 0))]
elif case == 'TC':
    extra = [('(TC) fails: 4aC+2bC+sC>4xC', row({'xC': 4, 'aC': -4, 'bC': -2, 'sC': -1}, 0, True))]
tree(NAMED + extra, menu)
print('LEAVES', LEAVES[0])
