# Adversary "priority plans" with budget capping, evaluated by MILP (prover's exact best response).
# At step j the adversary reuses non-avoided vertices from source patterns in the given priority order,
# up to the budget 1 (continuous masses, m=1), and fills the rest with fresh vertices.
import sys, itertools
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def parse(s):
    return [frozenset(int(c) for c in w) for w in s.split()]

def is_forced(lines, p, j):
    return any(L <= (p | {j}) for L in lines)

def threatening(lines, p, j):
    S = p | {j}
    if any(L <= S for L in lines): return False
    for a in p:
        L = [L for L in lines if a in L and j in L][0]
        c = [x for x in L if x != a and x != j][0]
        if c > j and c not in p: return True
    return False

class LE:  # linear expression over variables, index 0 = constant
    def __init__(self, d=None): self.d = dict(d or {})
    def __add__(self, o):
        r = dict(self.d)
        for k, v in o.d.items(): r[k] = r.get(k, 0) + v
        return LE(r)
    def __sub__(self, o):
        r = dict(self.d)
        for k, v in o.d.items(): r[k] = r.get(k, 0) - v
        return LE(r)
    def scale(self, s): return LE({k: v * s for k, v in self.d.items()})
    def iszero(self): return all(abs(v) < 1e-12 for v in self.d.values())

def evaluate(lines, budgets, plan, return_sol=False):
    n = 7
    nvar = [0]; integ = []
    def newvar(is_int=False):
        nvar[0] += 1; integ.append(is_int); return nvar[0]
    cons = []  # (LE, lo, hi) meaning lo <= LE <= hi  (LE includes constant)
    M = 20.0
    mu = {}
    costs = []
    one = LE({0: 1})
    for j in range(n):
        cost = LE()
        for p in list(mu):
            if is_forced(lines, p, j): cost = cost + mu[p]
        if budgets[j] == 0:
            costs.append(cost); continue
        src = [p for p in plan.get(j, []) if p in mu and not is_forced(lines, p, j)]
        newmu = dict(mu)
        remaining = one
        for p in src:
            a = LE({newvar(): 1})
            cons.append((a, 0, None)); cons.append((mu[p] - a, 0, None))
            cost = cost + a
            A = mu[p] - a
            # rho = min(A, remaining)
            rho = LE({newvar(): 1}); d = newvar(True)
            cons.append((A - rho, 0, None)); cons.append((remaining - rho, 0, None))
            cons.append((rho - A + LE({d: M}), 0, None)); cons.append((rho - remaining + LE({d: -M}) + LE({0: M}), 0, None))
            newmu[p] = mu[p] - rho
            q = p | {j}
            newmu[q] = (newmu.get(q, LE()) + rho)
            remaining = remaining - rho
        q = frozenset({j})
        newmu[q] = newmu.get(q, LE()) + remaining
        mu = {p: e for p, e in newmu.items() if not e.iszero()}
        costs.append(cost)
    t = newvar()
    for c in costs:
        cons.append((LE({t: 1}) - c, 0, None))
    nv = nvar[0]
    A = []; lo = []; hi = []
    for e, l, h in cons:
        row = np.zeros(nv); c0 = 0
        for k, v in e.d.items():
            if k == 0: c0 += v
            else: row[k - 1] += v
        A.append(row); lo.append((l - c0) if l is not None else -np.inf); hi.append((h - c0) if h is not None else np.inf)
    c = np.zeros(nv); c[t - 1] = 1
    lb = np.zeros(nv); ub = np.full(nv, np.inf)
    for i in range(nv):
        if integ[i]: ub[i] = 1
    res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.array([1 if x else 0 for x in integ]), bounds=Bounds(lb, ub))
    if res.status != 0: return None
    return (res.fun, res) if return_sol else res.fun

def present_patterns(lines, budgets, plan, j):
    pats = set()
    for i in range(j):
        if budgets[i] == 0: continue
        src = plan.get(i, [])
        newp = set(pats)
        for p in src:
            if p in pats and not is_forced(lines, p, i): newp.add(p | {i})
        newp.add(frozenset({i}))
        pats = newp
    return pats

def search(lines, budgets, maxsrc=2, target=None, verbose=False):
    n = 7; best = [0, None]
    def dfs(j, plan):
        if target is not None and best[0] >= target - 1e-9: return
        if j == n:
            v = evaluate(lines, budgets, plan)
            if v is not None and v > best[0] + 1e-9:
                best[0] = v; best[1] = dict(plan)
                if verbose: print(round(v, 6), fmt(plan), flush=True)
            return
        if budgets[j] == 0:
            dfs(j + 1, plan); return
        pats = sorted([p for p in present_patterns(lines, budgets, plan, j) if threatening(lines, p, j)], key=lambda p: (len(p), sorted(p)))
        options = [[]]
        for r in range(1, maxsrc + 1):
            for comb in itertools.permutations(pats, r):
                options.append(list(comb))
        for opt in options:
            plan[j] = opt
            dfs(j + 1, plan)
        del plan[j]
    dfs(0, {})
    return best

def fmt(plan):
    return {k: [''.join(map(str, sorted(p))) for p in s] for k, s in plan.items() if s}

if __name__ == '__main__':
    lines = parse(sys.argv[1]); budgets = [int(c) for c in sys.argv[2]]
    ms = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    tg = float(sys.argv[4]) if len(sys.argv) > 4 else None
    b = search(lines, budgets, ms, tg, verbose=True)
    print('BEST', b[0], fmt(b[1]))
