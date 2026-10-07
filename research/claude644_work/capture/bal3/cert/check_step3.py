"""Independent checker (stdlib only) for the step-3 case trees of the human proof of Theorem 3T (balanced).
Reads step3/{TC,TB,TA}.txt (output of step3b.py), re-parses every named fact from its inequality TEXT with an
independent parser, rebuilds the disjunction alternatives from scratch, and verifies:
  (1) tree completeness: under every branching node the children are EXACTLY the alternatives of the named
      disjunction (pair map / ALL@X map / template failure list), and every path ends in a leaf;
  (2) every leaf Farkas combination: multipliers >= 0, only facts available on the path (base facts, case extras,
      path facts), variable coefficients cancel exactly, and the constant gives a contradiction
      (sum lam*expr == c with c > 0, or c == 0 with positive weight on a strict fact), all in exact rationals.
Conventions: every fact is 'expr <= 0' or 'expr < 0'; e_X abbreviates x_X - s_X.
usage: python3 check_step3.py   (from bal3/cert)"""
import re, sys
from fractions import Fraction as F
P = 'ABC'
VARS = ['xA', 'xB', 'xC', 'tau', 'sA', 'aB', 'aC', 'bA', 'sB', 'bC', 'cA', 'cB', 'sC']
def tv(r, i):  # trace of rep r (0=alpha,1=beta,2=gamma) at part i
    return 's' + P[i] if r == i else 'abc'[r] + P[i]

# ---------- independent parser of linear expressions ----------
TOK = re.compile(r'\s*([+-]|\d+/\d+|\d+|tau|[esxabc][ABC]|sum\([abc]\)|\(|\)|/)')
def parse_expr(s):
    """returns dict var->Fraction plus '1' for constant.  grammar: sum of terms; term = [coef] var [/den] | number"""
    s = s.replace(' ', '')
    out = {}
    sign = 1; i = 0
    while i < len(s):
        if s[i] == '+': sign = 1; i += 1; continue
        if s[i] == '-': sign = -1; i += 1; continue
        # term
        m = re.match(r'(\d+/\d+|\d+)?(tau|[esxabc][ABC]|sum\([abc]\))?(?:/(\d+))?', s[i:])
        if not m or m.end() == 0: raise ValueError('cannot parse ' + s + ' at ' + s[i:])
        coef = F(m.group(1)) if m.group(1) else F(1)
        if m.group(3): coef /= int(m.group(3))
        var = m.group(2)
        if var is None: out['1'] = out.get('1', 0) + sign * coef
        elif var.startswith('sum('):
            r = 'abc'.index(var[4])
            for j in range(3): v = tv(r, j); out[v] = out.get(v, 0) + sign * coef
        elif var == 'tau' or var[0] in 'xsabc': out[var] = out.get(var, 0) + sign * coef
        elif var[0] == 'e':   # e_X = x_X - s_X
            X = var[1]; out['x' + X] = out.get('x' + X, 0) + sign * coef; out['s' + X] = out.get('s' + X, 0) - sign * coef
        i += m.end(); sign = 1
    return {k: v for k, v in out.items() if v != 0}
def parse_fact(name):
    """name -> (expr dict meaning expr <= 0 (or < 0), strict)"""
    t = name
    if ': ' in t: t = t.split(': ', 1)[1]
    if t.startswith('bal '): t = t[4:]
    t = t.replace('(<=)', '').replace('(>=)', '').strip()
    if name.endswith('(>=)'): t = t.replace('=', '>=')      # sum(a)=1 (>=)  means sum >= 1
    elif name.endswith('(<=)'): t = t.replace('=', '<=')
    if name == '(TB) holds': t = '4aB+2sB+cB<=4xB'
    for op in ['<=', '>=', '<', '>', '=']:
        if op in t:
            L, R = t.split(op); break
    else: raise ValueError(name)
    l, r = parse_expr(L), parse_expr(R)
    diff = {}
    if op in ('<=', '<', '='):   # L - R <= 0
        for k, v in l.items(): diff[k] = diff.get(k, 0) + v
        for k, v in r.items(): diff[k] = diff.get(k, 0) - v
    else:                        # R - L <= 0
        for k, v in r.items(): diff[k] = diff.get(k, 0) + v
        for k, v in l.items(): diff[k] = diff.get(k, 0) - v
    return ({k: v for k, v in diff.items() if v != 0}, op in ('<', '>'))

# ---------- base facts (the hypotheses of step 3), rebuilt from scratch ----------
BASE = []
for X in P:
    BASE += [f'x{X}<=3/2', f's{X}>=2x{X}/3', f's{X}<=x{X}', f's{X}<=1', f'x{X}>=0']
for r in range(3):
    for i in range(3):
        if r != i: BASE += [f'{tv(r, i)}>=0', f'{tv(r, i)}<=2x{P[i]}/3']
    BASE += [f'sum({"abc"[r]})=1 (<=)', f'sum({"abc"[r]})=1 (>=)']
BASE += ['tau>3/4', 'bal eA+eB<=3/4', 'bal eA+eC<=3/4', 'bal eB+eC<=3/4', 'id: tau<=eA+eB+eC',
         'AAB@A: bA<=2eA', 'AAB@B: aB<=eB+sB/2', 'AAC@A: cA<=2eA', 'AAC@C: aC<=eC+sC/2', 'BBC@B: cB<=2eB', 'BBC@C: bC<=eC+sC/2']
EXTRA = {'TC': ['(TC) fails: 4aC+2bC+sC>4xC'], 'TB': ['(TB) fails: 4aB+2sB+cB>4xB'],
         'TA': ['(TA) fails: 4sA+2bA+cA>4xA', '(TB) holds']}
# ---------- disjunctions, rebuilt from scratch ----------
def alts_of(name):
    m = re.match(r'P\(([ABC])->([ABC])\)$', name)
    if m:
        Y, X = P.index(m.group(1)), P.index(m.group(2)); Z = 3 - X - Y; y = tv(Y, X)
        return {f'P({P[Y]}->{P[X]}): tau<=x{P[X]}-{y}+e{P[Z]}', f'{y}=0'}
    m = re.match(r'ALL@([ABC])$', name)
    if m:
        X = P.index(m.group(1)); Y, Z = [i for i in range(3) if i != X]; y, z = tv(Y, X), tv(Z, X)
        return {f'ALL@{P[X]}: {y}<=x{P[X]}-tau', f'ALL@{P[X]}: {z}<=x{P[X]}-tau', f'{y}=0', f'{z}=0'}
    m = re.match(r'T\(([ABC]);([ABC]),\2;([ABC])\)$', name)
    if m:
        X, Y, Z = [P.index(m.group(k)) for k in (1, 2, 3)]; out = set()
        for i in range(3):
            a, b, c, x = tv(X, i), tv(Y, i), tv(Z, i), 'x' + P[i]
            out |= {f'{name} fails: 2{a}+{b}>2{x}', f'{name} fails: 2{a}+{c}>2{x}', f'{name} fails: 2{b}+{c}>2{x}',
                    f'{name} fails: 4{a}+2{b}+{c}>4{x}'}
        return out
    m = re.match(r'V\(([ABC]),([ABC])\)$', name)
    if m:
        S, T_ = P.index(m.group(1)), P.index(m.group(2)); out = set()
        for i in range(3):
            s, t, x = tv(S, i), tv(T_, i), 'x' + P[i]
            out |= {f'{name} fails: {s}+{t}>{x}', f'{name} fails: 5{s}/4+{t}/2>{x}'}
        return out
    raise ValueError('unknown disjunction ' + name)

def check_farkas(terms, avail):
    """terms: list of (lam, factname).  returns None if OK else error string"""
    tot = {}; sw = 0
    for lam, nm in terms:
        if nm not in avail: return 'fact not available: ' + nm
        if lam < 0: return 'negative multiplier'
        e, strict = parse_fact(nm)
        for k, v in e.items(): tot[k] = tot.get(k, 0) + lam * v
        if strict and lam > 0: sw += lam
    for k, v in tot.items():
        if k != '1' and v != 0: return f'variable {k} does not cancel ({v})'
    c = tot.get('1', 0)
    # sum lam*expr <= 0 (strictly if sw>0); identity says sum == c  ->  contradiction iff c > 0 or (c == 0 and sw > 0)
    if c > 0 or (c == 0 and sw > 0): return None
    return f'no contradiction: constant {c}, strict weight {sw}'

def check_file(case, path):
    lines = open(path).read().split('\n')
    avail0 = set(BASE) | set(EXTRA[case])
    stack = []   # list of (indent, node_facts_set, disj_name or None, seen_children set)
    leaves = 0; errors = 0; nodes = 0
    def depth(l): return (len(l) - len(l.lstrip(' '))) // 4
    i = 0
    pending_leaf = None
    while i < len(lines):
        l = lines[i]; i += 1
        if not l.strip() or l.startswith('LEAVES'): continue
        if l.strip().startswith('Farkas:'):
            assert pending_leaf is not None, 'Farkas without leaf'
            terms = []
            for t in l.split('Farkas:')[1].split(' + '):
                t = t.strip(); lam, nm = t.split('*[', 1); nm = nm[:-1]
                terms.append((F(lam), nm))
            err = check_farkas(terms, pending_leaf)
            leaves += 1
            if err: errors += 1; print('  LEAF ERROR', case, err, '|', l.strip()[:120])
            pending_leaf = None; continue
        d = depth(l); s = l.strip()
        # pop the stack to the parent level
        while stack and stack[-1][0] >= d: stack.pop()
        # this line's label = facts added at this node (children of the parent's disjunction)
        if ' -> CONTRADICTION' in s: label = s.split(' -> CONTRADICTION')[0]; kind = 'leaf'
        elif ' ; use ' in s: label, rest = s.split(' ; use '); disj = rest.rstrip(':'); kind = 'branch'
        elif ' ; if ' in s: label, rest = s.split(' ; if '); disj = rest.split(' is feasible')[0]; kind = 'branch'
        elif ' OPEN' in s: print('  OPEN NODE', s); errors += 1; continue
        else: raise ValueError('unrecognised line: ' + s)
        facts = set() if label == 'root' else set(label.split(' & '))
        if stack:
            par = stack[-1]
            if not facts <= alts_of(par[2]): print('  ERROR child not an alternative of', par[2], ':', facts); errors += 1
            par[3].update(facts)
            avail = par[1] | facts
        else:
            assert label == 'root'; avail = set(avail0)
        if kind == 'leaf': pending_leaf = avail
        else:
            nodes += 1; stack.append((d, avail, disj, set()))
            # completeness check deferred: verify when popped; simpler: record and check at end of file
            stack[-1] = (d, avail, disj, set()); COMPLETE.append(stack[-1])
    return leaves, nodes, errors
COMPLETE = []
tot_err = 0
for case in ['TC', 'TB', 'TA']:
    COMPLETE.clear()
    leaves, nodes, errors = check_file(case, f'step3/{case}.txt')
    inc = 0
    for d, avail, disj, seen in COMPLETE:
        if seen != alts_of(disj): inc += 1; print('  INCOMPLETE branching on', disj, 'missing', alts_of(disj) - seen)
    print(f'case {case}: leaves {leaves} branch nodes {nodes} leaf errors {errors} incomplete branchings {inc}')
    tot_err += errors + inc
print('TOTAL ERRORS', tot_err)
