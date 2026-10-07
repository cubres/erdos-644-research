#!/usr/bin/env python3
"""wref8 misc exact checks: (a) the free-residual characterisation (hence the tau* formula) against a direct
exact LP 'is there an admissible a <= u'; (b) note 7.78's C_theta; (c) the |I|=2 example x=(11/8,11/8),
theta=1 (template with C:=B must fail; any Fano assignment must fail); (d) hand-picked degenerate points."""
import itertools, random
from fractions import Fraction as F
from wref8_exactlp import feasible
from wref8_template import build, template_rows, tau_star, LINES

def has_type_below(u, x, th, I):
    p = len(u)
    for i in I:
        lb = [F(0)] * p; lb[i] = th[i]
        ubv = [min(u[j], x[j]) for j in range(p)]
        if any(lb[j] > ubv[j] for j in range(p)): continue
        if feasible(p, [], [({j: 1 for j in range(p)}, F(1))], lb, ubv)[0] == 'FEAS': return True
    return False

def part_a(N=300, seed=1):
    rng = random.Random(seed); bad = 0; n = 0
    while n < N:
        p = rng.randint(2, 5)
        x = [F(rng.randint(1, 40), 20) for _ in range(p)]
        I = sorted(rng.sample(range(p), rng.randint(1, p)))
        X = sum(x)
        th = [max(F(rng.randint(0, 20), 20) * min(x[i], F(1)), 1 - X + x[i]) if i in I else F(0) for i in range(p)]
        I = [i for i in I if th[i] <= min(x[i], F(1))]
        if not I: continue
        u = [F(rng.randint(0, 20), 20) * x[j] for j in range(p)]
        pred_free = sum(u) < 1 or all(u[i] < th[i] for i in I)
        if pred_free == has_type_below(u, x, th, I): bad += 1; print('  free predicate wrong', x, th, I, u)
        n += 1
    print(f'[a] free-residual characterisation: {N} random exact tests, disagreements {bad}')

def part_b():
    x = [F(4, 5)] * 3; th = [F(27, 50)] * 3; I = [0, 1, 2]
    print('[b] C_theta: tau* =', tau_star(x, th, I), ' template:', feasible(*build(x, th, template_rows(0, 1, 2)))[0])

def part_c():
    x = [F(11, 8)] * 2; th = [F(1)] * 2
    res = set()
    for assign in itertools.product([0, 1], repeat=7):
        res.add(feasible(*build(x, th, list(assign)))[0])
    print('[c] x=(11/8,11/8), theta=1, all 128 box assignments of the 7 Fano rows:', res,
          ' tau* =', tau_star(x, th, [0, 1]))
    # same with a third box part of tiny capacity -> |I|=3
    for eps in [F(1, 100), F(1, 1000)]:
        x3 = [F(11, 8), F(11, 8), eps]; th3 = [F(1), F(1), eps]  # third box: theta = x (tight in the small sense)
        # effective threshold of the third box: max(eps, 1 - X + eps) = eps
        ts = tau_star(x3, th3, [0, 1, 2])
        ok = [feasible(*build(x3, th3, template_rows(*t)))[0] for t in itertools.permutations(range(3), 3)]
        print(f'    add third box x=theta={eps}: tau*={ts}, templates over ordered triples: {ok}')

def part_d():
    pts = []
    # all three parts on theta=4x/7 edge with x_L at 7/4 - tiny, total exactly 3/4
    for xa in [F(1, 2), F(7, 8), F(3, 2), F(7, 4)]:
        for xl in [F(0), F(1, 2), F(7, 4) - F(1, 10**6)]:
            # choose xB = xC = s on theta=4x/7 so that 3/7 (xa + 2 s) + 3/7 xl = 3/4
            s = (F(7, 4) - xl - xa) / 2
            if s < 0 or s > F(7, 4): continue
            x = [xa, s, s, xl]; th = [F(4, 7) * xa, F(4, 7) * s, F(4, 7) * s, F(0)]
            pts.append((x, th))
    # mixtures tight/Fano near boundary
    pts.append(([F(1), F(1), F(7, 4) - F(1, 10**6), F(0)], [F(1), F(1), F(1), F(0)]))
    pts.append(([F(1) + F(1, 10**6), F(1), F(1), F(7, 4) - F(1, 10**6)], [F(1), F(1), F(1), F(0)]))
    pts.append(([F(1, 10**6), F(1, 10**6), F(1, 10**6), F(7, 4)], [F(1, 10**6)] * 3 + [F(0)]))
    for x, th in pts:
        g = sum(x[k] - th[k] for k in range(3)) + F(3, 7) * x[3]
        r = feasible(*build(x, th, template_rows(0, 1, 2)))[0]
        print('[d]', [str(v) for v in x], [str(v) for v in th], 'g=', g, r)

if __name__ == '__main__':
    part_a(); part_b(); part_c(); part_d()
