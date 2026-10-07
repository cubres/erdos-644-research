# Search over "source plans" for the adversary: at step j, reuse ALL non-avoided vertices whose pattern lies in Src_j
# (all these patterns contain a common earlier step i, so the reuse fits in the budget), fill with fresh.
# The prover's best response to a fixed plan is an LP (avoid amounts per source pattern). Value = LP optimum.
import sys, itertools
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import linprog

def parse(s):
    return [frozenset(int(c) for c in w) for w in s.split()]

class Plan:
    def __init__(self, lines, budgets):
        self.lines = lines; self.budgets = budgets
    def safe(self, S):
        return not any(L <= S for L in self.lines)

def threatening(lines, p, j):
    # reuse of pattern p at step j is 'threatening' if p|{j} safe and contains a pair {a,j} whose line's third point c>j
    S = p | {j}
    if any(L <= S for L in lines): return False
    for a in p:
        L = [L for L in lines if a in L and j in L][0]
        c = [x for x in L if x != a and x != j][0]
        if c > j and c not in p: return True
    return False

def evaluate(lines, budgets, plan):
    """plan: dict j -> list of source patterns. Returns LP value (prover's best max cost), m=1."""
    n = 7
    # symbolic masses: dict pattern -> vector of coefficients over variables (+ const in index 0)
    var = []  # (j, pattern)
    def newvar(j, p):
        var.append((j, p)); return len(var)
    mu = {}  # pattern -> {varidx or 0: coeff}
    costs = []
    constraints = []  # (expr >= 0)
    def add(e1, e2, s=1):
        r = dict(e1)
        for k, v in e2.items(): r[k] = r.get(k, 0) + s * v
        return r
    for j in range(n):
        b = budgets[j]
        forced = [p for p in mu if not all(True for _ in [0]) or any(L <= (p | {j}) for L in lines)]
        cost = {}
        for p in forced:
            cost = add(cost, mu[p])
        if b == 0:
            costs.append(cost); continue
        src = plan.get(j, [])
        reused = {}
        newmu = {p: dict(e) for p, e in mu.items()}
        for p in src:
            if p not in mu: continue
            v = newvar(j, p)
            a = {v: 1}
            # 0 <= a <= mu[p]
            constraints.append(a)
            constraints.append(add(mu[p], a, -1))
            cost = add(cost, a)
            moved = add(mu[p], a, -1)
            newmu[p] = a
            q = p | {j}
            newmu[q] = add(newmu.get(q, {}), moved)
            reused = add(reused, moved)
        fresh = add({0: 1}, reused, -1)
        q = frozenset({j})
        newmu[q] = add(newmu.get(q, {}), fresh)
        constraints.append(fresh)  # fresh >= 0 (budget)
        mu = {p: e for p, e in newmu.items() if any(abs(c) > 1e-12 for c in e.values())}
        costs.append(cost)
    nv = len(var) + 1
    # variables: x_1..x_V, t ; minimize t
    def row(e):
        r = np.zeros(nv + 1); c0 = 0
        for k, v in e.items():
            if k == 0: c0 += v
            else: r[k - 1] += v
        return r, c0
    A = []; bvec = []
    for e in constraints:  # e >= 0  ->  -e_lin <= c0
        r, c0 = row(e); A.append(-r[:nv]); bvec.append(c0)
    for e in costs:  # e <= t
        r, c0 = row(e); rr = r[:nv].copy(); rr[nv - 1] = -1; A.append(rr); bvec.append(-c0)
    cobj = np.zeros(nv); cobj[nv - 1] = 1
    res = linprog(cobj, A_ub=np.array(A), b_ub=np.array(bvec), bounds=[(None, None)] * nv, method='highs')
    return res.fun if res.status == 0 else None, var, res

def search(lines, budgets, maxsrc=3, verbose=False):
    n = 7
    best = [0, None]
    # DFS over steps; at each step choose a source set among threatening present patterns sharing a common step
    def present_patterns(plan, j):
        # simulate structurally which patterns can have positive mass at time j
        pats = set()
        for i in range(j):
            if budgets[i] == 0: continue
            src = plan.get(i, [])
            newp = set(pats)
            for p in src:
                if p in pats: newp.add(p | {i})
            newp.add(frozenset({i}))
            pats = newp
        return pats
    def dfs(j, plan):
        if j == n:
            v, var, res = evaluate(lines, budgets, plan)
            if v is not None and v > best[0] + 1e-9:
                best[0] = v; best[1] = dict(plan)
                if verbose: print(round(v, 6), {k: [tuple(sorted(p)) for p in s] for k, s in plan.items()}, flush=True)
            return
        if budgets[j] == 0:
            dfs(j + 1, plan); return
        pats = [p for p in present_patterns(plan, j) if threatening(lines, p, j)]
        options = [[]]
        for r in range(1, maxsrc + 1):
            for comb in itertools.combinations(pats, r):
                common = frozenset.intersection(*comb)
                if len(common) == 0: continue
                options.append(list(comb))
        for opt in options:
            plan[j] = opt
            dfs(j + 1, plan)
        del plan[j]
    dfs(0, {})
    return best

if __name__ == '__main__':
    lines = parse(sys.argv[1]); budgets = [int(c) for c in sys.argv[2]]
    ms = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    b = search(lines, budgets, ms, verbose=True)
    print('BEST', b[0], {k: [tuple(sorted(p)) for p in s] for k, s in b[1].items()})
