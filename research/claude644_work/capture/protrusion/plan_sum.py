# Search adversary plans (step-class sources, adaptive priority among classes) that force SUM_j c_j >= target
# for every prover response (MILP: prover minimises total). Used for the profile-sum lower bound sigma >= 3.
import sys, itertools
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from plan_milp import parse, is_forced, threatening, LE

def evaluate(lines, budgets, splan):
    n = 7; nvar = [0]; integ = []
    def newvar(is_int=False):
        nvar[0] += 1; integ.append(is_int); return nvar[0]
    cons = []; M = 20.0
    t = newvar()
    def node(j, mu, acc):
        if j == n:
            cons.append((LE({t: 1}) - acc, 0, None)); return
        cost = LE()
        for p in list(mu):
            if is_forced(lines, p, j): cost = cost + mu[p]
        if budgets[j] == 0:
            node(j + 1, mu, acc + cost); return
        classes = splan.get(j, [])
        srcs = {}; allsrc = []
        for a in classes:
            lst = [p for p in sorted(mu, key=lambda p: (len(p), sorted(p))) if a in p and not is_forced(lines, p, j) and threatening(lines, p, j)]
            srcs[a] = lst
            for p in lst:
                if p not in allsrc: allsrc.append(p)
        avoid = {}
        for p in allsrc:
            a = LE({newvar(): 1}); cons.append((a, 0, None)); cons.append((mu[p] - a, 0, None))
            cost = cost + a; avoid[p] = a
        orders = list(itertools.permutations(classes)) if classes else [()]
        for order in orders:
            seq = []
            for a in order:
                for p in srcs[a]:
                    if p not in seq: seq.append(p)
            newmu = dict(mu); remaining = LE({0: 1})
            for p in seq:
                A = mu[p] - avoid[p]
                rho = LE({newvar(): 1}); d = newvar(True)
                cons.append((A - rho, 0, None)); cons.append((remaining - rho, 0, None))
                cons.append((rho - A + LE({d: M}), 0, None)); cons.append((rho - remaining + LE({d: -M}) + LE({0: M}), 0, None))
                newmu[p] = newmu[p] - rho
                q = p | {j}; newmu[q] = newmu.get(q, LE()) + rho
                remaining = remaining - rho
            q = frozenset({j}); newmu[q] = newmu.get(q, LE()) + remaining
            newmu = {p: e for p, e in newmu.items() if not e.iszero()}
            node(j + 1, newmu, acc + cost)
    node(0, {}, LE())
    nv = nvar[0]; A = []; lo = []; hi = []
    for e, l, h in cons:
        row = np.zeros(nv); c0 = 0
        for k, v in e.d.items():
            if k == 0: c0 += v
            else: row[k - 1] += v
        A.append(row); lo.append((l - c0) if l is not None else -np.inf); hi.append((h - c0) if h is not None else np.inf)
    c = np.zeros(nv); c[t - 1] = 1
    ub = np.array([1 if x else np.inf for x in integ])
    res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.array([1 if x else 0 for x in integ]), bounds=Bounds(np.zeros(nv), ub))
    return res.fun if res.status == 0 else None

def search(lines, budgets, maxlen=2, target=None):
    best = [0, None]; steps = [j for j in range(7) if budgets[j]]
    def dfs(idx, splan):
        if target is not None and best[0] >= target - 1e-9: return
        if idx == len(steps):
            v = evaluate(lines, budgets, splan)
            if v is not None and v > best[0] + 1e-9: best[0] = v; best[1] = dict(splan)
            return
        j = steps[idx]; earlier = [a for a in steps if a < j]
        opts = [[]]
        for r in range(1, maxlen + 1):
            for comb in itertools.combinations(earlier, r): opts.append(list(comb))
        for o in opts:
            if o: splan[j] = o
            dfs(idx + 1, splan); splan.pop(j, None)
    dfs(0, {}); return best

if __name__ == '__main__':
    mode = sys.argv[1]; ml = int(sys.argv[2]); tg = float(sys.argv[3])
    budgets = [1]*7 if mode == 'u' else [0]+[1]*6
    for line in open('orders.txt'):
        lines = parse(line.strip())
        b = search(lines, budgets, ml, tg)
        print(round(b[0], 6), '|', line.strip(), '|', b[1], flush=True)
