# EXACT verification (symbolic identities, no LP solver) of the three-chain adversary plans used in the hand proof
# of the anchored lower bound.  Continuous game, m=1.
# plan: dict step j -> earlier step a: at step j the adversary reuses ALL non-avoided, non-forced vertices containing a
# (they all lie in G_a, so the budget 1 is never exceeded) and fills G_j with fresh vertices.
# The prover's free variables are the avoided masses a_k of each source pattern (0 <= a_k <= its mass).
# We check symbolically that sum_{j in J} c_j == 3 identically (hence max_j c_j >= 3/4 for EVERY prover response),
# where c_j = forced mass at step j + avoided mass at step j (other avoidances only increase c_j).
# NOTE: sympy.solvers.simplex.lpmin (sympy 1.14) was found to be nondeterministic/wrong on these LPs; it is NOT used.
import itertools, sys
from sympy import Symbol, expand, Integer
BASE = [frozenset(((0+i)%7, (1+i)%7, (3+i)%7)) for i in range(7)]
def relabel(order):
    pos = {p: t for t, p in enumerate(order)}
    return [frozenset(pos[p] for p in L) for L in BASE]
def forced(lines, p, j): return any(L <= (p | {j}) for L in lines)
def simulate(lines, budgets, plan):
    mu = {}; costs = {}; k = [0]; box = []
    for j in range(7):
        cost = Integer(0)
        for p in list(mu):
            if forced(lines, p, j): cost += mu[p]
        if budgets[j] == 0:
            costs[j] = cost; continue
        newmu = dict(mu); reused = Integer(0)
        if j in plan:
            a = plan[j]
            for p in list(mu):
                if a in p and not forced(lines, p, j):
                    k[0] += 1; v = Symbol('a%d' % k[0])
                    box.append((v, mu[p]))          # 0 <= v <= mu[p]
                    cost += v
                    newmu[p] = v
                    q = p | {j}; newmu[q] = newmu.get(q, Integer(0)) + (mu[p] - v)
                    reused += mu[p] - v
        q = frozenset({j}); newmu[q] = newmu.get(q, Integer(0)) + (1 - reused)
        mu = newmu; costs[j] = expand(cost)
    return costs, box, mu
def third(lines, a, b): return next(iter([L for L in lines if a in L and b in L][0] - {a, b}))
if __name__ == '__main__':
    seen = {}
    for order in itertools.permutations(range(7)):
        lines = relabel(order); key = tuple(sorted(tuple(sorted(L)) for L in lines))
        seen.setdefault(key, lines)
    budgets = [0] + [1] * 6
    n = 0
    for key, lines in seen.items():
        Ls = set(lines)
        if frozenset({4,5,6}) in Ls:
            k0 = third(lines, 0, 3)
            if k0 == 4: continue
            kp = ({5,6} - {k0}).pop(); i = 1 if third(lines,1,3) == kp else 2
            plan = {2: 1, 3: i, 5: 4}; J = [2,3,5,6]; case = "A'2"
        else:
            x, y, w = third(lines,4,5), third(lines,4,6), third(lines,5,6)
            if x == 0:
                z = ({1,2,3} - {y,w}).pop(); s = max(z,y); plan = {s: min(z,y), 4: y, 5: w}; J = [s,4,5,6]; case = "B'x"
            elif y == 0:
                z = ({1,2,3} - {x,w}).pop(); s = max(z,x); plan = {s: min(z,x), 4: x, 5: w}; J = [s,4,5,6]; case = "B'y"
            else: continue
        costs, box, mu = simulate(lines, budgets, plan)
        total = expand(sum(costs[j] for j in J))
        # every final pattern must be safe (no live line contained) -- the adversary only reuses non-forced vertices
        assert all(not any(L <= p for L in lines) for p in mu), 'unsafe pattern'
        assert len(set(J)) == 4 and total == 3, (case, key, plan, total)
        n += 1
        print(case, key, 'plan', plan, 'J', J, ' sum_J c_j =', total)
    print('verified', n, 'three-chain classes: sum_{j in J} c_j == 3 identically, |J| = 4  =>  max_j c_j >= 3/4')
