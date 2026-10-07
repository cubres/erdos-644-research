"""REFEREE (w12) independent re-verification of bal3/cert/step3/{TC,TB,TA}.txt.
Independent of check_step3.py: no text parsing of inequalities.  Every fact/alternative name is REGENERATED
from the mathematical definitions by this script's own formatter and matched to the printed names; the rows are
built here from scratch; every leaf is checked by an LP (HiGHS): maximise the common slack t of all strict rows;
contradiction iff infeasible or t <= 0.  Tree completeness is re-checked with this script's own alternative sets.
Also: the Farkas lines are IGNORED (their exact check is check_step3.py; this is the second, independent method).
"""
import re, sys, itertools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
P = 'ABC'
V = ['xA', 'xB', 'xC', 'sA', 'sB', 'sC', 'aB', 'aC', 'bA', 'bC', 'cA', 'cB', 'tau']
IX = {v: i for i, v in enumerate(V)}
def tv(r, i): return 's' + P[i] if r == i else 'abc'[r] + P[i]
def e(X, k=1):  # k*e_X = k*(x_X - s_X)
    return {'x' + X: k, 's' + X: -k}
def add(*ds):
    out = {}
    for d in ds:
        for k, v in d.items(): out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}
def row(d, rhs, strict=False): return (dict(d), F(rhs), strict)   # d.z <= rhs (< if strict)

# ---- hypotheses of step 3 (theorem hypotheses + Lemma 0 + id map + T(A;B,B;C) pattern facts), own construction
FACTS = {}
def fact(name, d, rhs, strict=False): FACTS[name] = row(d, rhs, strict)
for X in P:
    fact(f'x{X}<=3/2', {'x' + X: 1}, F(3, 2))                     # derived: x = s+e <= 1 + x/3
    fact(f's{X}>=2x{X}/3', {'x' + X: F(2, 3), 's' + X: -1}, 0)
    fact(f's{X}<=x{X}', {'s' + X: 1, 'x' + X: -1}, 0)
    fact(f's{X}<=1', {'s' + X: 1}, 1)
    fact(f'x{X}>=0', {'x' + X: -1}, 0)
for r in range(3):
    s = {}
    for i in range(3):
        v = tv(r, i); s[v] = 1
        if r != i:
            fact(f'{v}>=0', {v: -1}, 0)
            fact(f'{v}<=2x{P[i]}/3', {v: 1, 'x' + P[i]: F(-2, 3)}, 0)   # Lemma 0
    fact(f'sum({"abc"[r]})=1 (<=)', s, 1)
    fact(f'sum({"abc"[r]})=1 (>=)', {k: -1 for k in s}, -1)
fact('tau>3/4', {'tau': -1}, F(-3, 4), True)
for i, j in itertools.combinations(P, 2): fact(f'bal e{i}+e{j}<=3/4', add(e(i), e(j)), F(3, 4))
fact('id: tau<=eA+eB+eC', add({'tau': 1}, e('A', -1), e('B', -1), e('C', -1)), 0)
# pattern facts of T(A;B,B;C): XXY at X: y_X <= 2e_X ; at Y: t^X_Y <= e_Y + s_Y/2
def pat_facts(X, Y):
    x, y = P[X], P[Y]
    return {f'{x}{x}{y}@{x}: {tv(Y, X)}<=2e{x}': row(add({tv(Y, X): 1}, e(x, -2)), 0),
            f'{x}{x}{y}@{y}: {tv(X, Y)}<=e{y}+s{y}/2': row(add({tv(X, Y): 1}, e(y, -1), {'s' + y: F(-1, 2)}), 0)}
for X, Y in [(0, 1), (0, 2), (1, 2)]: FACTS.update(pat_facts(X, Y))
EXTRA = {'TC': {'(TC) fails: 4aC+2bC+sC>4xC': row({'aC': -4, 'bC': -2, 'sC': -1, 'xC': 4}, 0, True)},
         'TB': {'(TB) fails: 4aB+2sB+cB>4xB': row({'aB': -4, 'sB': -2, 'cB': -1, 'xB': 4}, 0, True)},
         'TA': {'(TA) fails: 4sA+2bA+cA>4xA': row({'sA': -4, 'bA': -2, 'cA': -1, 'xA': 4}, 0, True),
                '(TB) holds': row({'aB': 4, 'sB': 2, 'cB': 1, 'xB': -4}, 0)}}
# ---- disjunctions (own construction) ----
def alts(name):
    """returns dict altname -> row"""
    m = re.fullmatch(r'P\(([ABC])->([ABC])\)', name)
    if m:
        Y, X = P.index(m.group(1)), P.index(m.group(2)); Z = 3 - X - Y; y = tv(Y, X)
        return {f'P({P[Y]}->{P[X]}): tau<=x{P[X]}-{y}+e{P[Z]}': row(add({'tau': 1, 'x' + P[X]: -1, y: 1}, e(P[Z], -1)), 0),
                f'{y}=0': row({y: 1}, 0)}
    m = re.fullmatch(r'ALL@([ABC])', name)
    if m:
        X = P.index(m.group(1)); Y, Z = [i for i in range(3) if i != X]; y, z = tv(Y, X), tv(Z, X)
        return {f'ALL@{P[X]}: {y}<=x{P[X]}-tau': row({y: 1, 'x' + P[X]: -1, 'tau': 1}, 0),
                f'ALL@{P[X]}: {z}<=x{P[X]}-tau': row({z: 1, 'x' + P[X]: -1, 'tau': 1}, 0),
                f'{y}=0': row({y: 1}, 0), f'{z}=0': row({z: 1}, 0)}
    m = re.fullmatch(r'T\(([ABC]);([ABC]),([ABC]);([ABC])\)', name)
    if m:
        assert m.group(2) == m.group(3)
        X, Y, Z = [P.index(m.group(k)) for k in (1, 2, 4)]; out = {}
        for i in range(3):
            a, b, c, x = tv(X, i), tv(Y, i), tv(Z, i), 'x' + P[i]
            # Lemma 7.63 for 4 X-lines, 2 Y-lines, 1 Z-line: point sums <= 2x (XXY, XXZ, YYZ), total <= 4x
            out[f'{name} fails: 2{a}+{b}>2{x}'] = row({a: -2, b: -1, x: 2}, 0, True)
            out[f'{name} fails: 2{a}+{c}>2{x}'] = row({a: -2, c: -1, x: 2}, 0, True)
            out[f'{name} fails: 2{b}+{c}>2{x}'] = row({b: -2, c: -1, x: 2}, 0, True)
            out[f'{name} fails: 4{a}+2{b}+{c}>4{x}'] = row({a: -4, b: -2, c: -1, x: 4}, 0, True)
        return out
    m = re.fullmatch(r'V\(([ABC]),([ABC])\)', name)
    if m:
        S, T_ = P.index(m.group(1)), P.index(m.group(2)); out = {}
        for i in range(3):
            s, t, x = tv(S, i), tv(T_, i), 'x' + P[i]
            out[f'{name} fails: {s}+{t}>{x}'] = row({s: -1, t: -1, x: 1}, 0, True)
            out[f'{name} fails: 5{s}/4+{t}/2>{x}'] = row({s: F(-5, 4), t: F(-1, 2), x: 1}, 0, True)
        return out
    raise ValueError(name)

def lp_slack(rows):
    """max t: strict rows a.z + t <= b, nonstrict a.z <= b, t <= 1.  returns t* (or -inf if infeasible)"""
    n = len(V); M = len(rows)
    A = np.zeros((M + 1, n + 1)); b = np.zeros(M + 1)
    for k, (coef, rhs, st) in enumerate(rows):
        for v, c in coef.items(): A[k, IX[v]] = float(c)
        if st: A[k, n] = 1.0
        b[k] = float(rhs)
    A[M, n] = 1.0; b[M] = 1.0
    c = np.zeros(n + 1); c[n] = -1.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * (n + 1), method='highs')
    if res.status == 2: return -np.inf
    assert res.status == 0, res.message
    return -res.fun

def check(case, path):
    lines = [l for l in open(path).read().split('\n') if l.strip() and not l.startswith('LEAVES') and 'Farkas:' not in l]
    base = dict(FACTS); base.update(EXTRA[case])
    stack = []  # (depth, facts dict, disj name, seen set)
    leaves = 0; errs = 0; branches = []
    for l in lines:
        d = (len(l) - len(l.lstrip(' '))) // 4; s = l.strip()
        while stack and stack[-1][0] >= d: stack.pop()
        if ' -> CONTRADICTION' in s: label = s.split(' -> CONTRADICTION')[0]; kind = 'leaf'; disj = None
        elif ' ; use ' in s: label, rest = s.split(' ; use '); disj = rest.rstrip(':'); kind = 'branch'
        elif ' ; if ' in s: label, rest = s.split(' ; if '); disj = rest.split(' is feasible')[0]; kind = 'branch'
        else: print('  UNRECOGNISED', s); errs += 1; continue
        if label == 'root':
            assert not stack; facts = dict(base)
        else:
            par = stack[-1]; al = alts(par[2])
            names = label.split(' & ')
            if any(nm not in al for nm in names): print('  BAD CHILD', names, 'of', par[2]); errs += 1; continue
            par[3].update(names)
            facts = dict(par[1]); facts.update({nm: al[nm] for nm in names})
        if kind == 'leaf':
            t = lp_slack(list(facts.values())); leaves += 1
            if not (t <= 1e-9): print('  LEAF NOT REFUTED', case, label, 'slack', t); errs += 1
        else:
            stack.append((d, facts, disj, set())); branches.append(stack[-1])
    for d, facts, disj, seen in branches:
        missing = set(alts(disj)) - seen
        if missing: print('  INCOMPLETE', disj, missing); errs += 1
    print(f'case {case}: leaves {leaves} branches {len(branches)} errors {errs}')
    return errs
tot = 0
for case in ['TC', 'TB', 'TA']:
    tot += check(case, f'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert/step3/{case}.txt')
print('TOTAL ERRORS', tot)
# sanity: the base system itself (without extras) must be FEASIBLE with positive slack, else the check is vacuous
print('sanity: base slack (should be > 0):', lp_slack(list(FACTS.values())))
for case in ['TC', 'TB', 'TA']:
    r = dict(FACTS); r.update(EXTRA[case]); print(f'sanity: base+{case} extras slack:', lp_slack(list(r.values())))
