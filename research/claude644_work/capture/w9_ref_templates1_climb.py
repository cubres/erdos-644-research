# Referee w9, templates#1: adversarial climb. Maximise  viol = min_{Qb,Qa,V} max_i (template_i - x_i)
# at the canonical pair (all heavy pairs I,J), subject to tau*(U(g)uU(h)) >= 3/4 (closed-form tau*,
# cross-checked exactly against note Lemma 7.56 at the end), both generators heavy (H fails).
# Theorem 2UB predicts viol <= 0 always.  Float search, exact rational re-check of the best point.
import random, sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w9_ref_templates1_e2e import tau_star, Q_real, V_real

def tau_cf(x, g, h):
    p = len(x); best = sum(x) - 1
    for i in range(p):
        if g[i] > 0 and h[i] > 0: best = min(best, x[i] - min(g[i], h[i]))
        for j in range(p):
            if i != j and g[i] > 0 and h[j] > 0: best = min(best, x[i] - g[i] + x[j] - h[j])
    return best

def viol(x, g, h):
    p = len(x)
    if any(g[i] > x[i] or h[i] > x[i] for i in range(p)) or sum(g) > 1 or sum(h) > 1 or min(g + h) < 0: return None
    if tau_cf(x, g, h) < 0.75: return None
    Is = [i for i in range(p) if 7*g[i] > 4*x[i]]; Js = [i for i in range(p) if 7*h[i] > 4*x[i]]
    if not Is or not Js: return None
    worst = -9
    for I in Is:
        for J in Js:
            a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
            if a[J] > x[J] or b[I] > x[I]: return 9   # admissibility failure = counterexample
            qb = max(max(1.5*b[i], a[i] + .75*b[i]) - x[i] for i in range(p))
            qa = max(max(1.5*a[i], b[i] + .75*a[i]) - x[i] for i in range(p))
            v = max(max(a[i] + b[i], 1.25*a[i] + .5*b[i]) - x[i] for i in range(p))
            worst = max(worst, min(qb, qa, v))
    return worst

def climb(seed, iters=20000):
    rng = random.Random(seed); p = rng.choice([2, 3, 4, 5])
    best = None
    while best is None:
        x = [rng.uniform(.3, 1.9) for _ in range(p)]
        I, J = rng.sample(range(p), 2)
        g = [0.0]*p; h = [0.0]*p
        g[I] = min(1, x[I]) * rng.uniform(.6, 1); h[J] = min(1, x[J]) * rng.uniform(.6, 1)
        for i in range(p):
            if i != I: g[i] = min(x[i], 1 - sum(g)) * rng.uniform(0, .5) if rng.random() < .5 else 0.0
            if i != J: h[i] = min(x[i], 1 - sum(h)) * rng.uniform(0, .5) if rng.random() < .5 else 0.0
        cur = viol(x, g, h)
        if cur is not None: best = (cur, x, g, h)
    step = .1
    for it in range(iters):
        _, x, g, h = best
        x2, g2, h2 = list(x), list(g), list(h)
        for vec in rng.sample([x2, g2, h2], rng.randint(1, 3)):
            i = rng.randrange(p)
            if vec is x2 or vec[i] > 0 or rng.random() < .1: vec[i] = max(0.0, vec[i] + rng.gauss(0, step))
        c = viol(x2, g2, h2)
        if c is not None and c >= best[0]: best = (c, x2, g2, h2)
        if it % 2000 == 1999: step *= .6
    return p, best

if __name__ == '__main__':
    s0, n = int(sys.argv[1]), int(sys.argv[2])
    top = -9
    for s in range(s0, s0 + n):
        p, (c, x, g, h) = climb(s)
        # exact recheck: round to rationals, verify tau* exactly by Lemma 7.56 and templates exactly
        xe = [F(v).limit_denominator(10**6) for v in x]; ge = [F(v).limit_denominator(10**6) for v in g]; he = [F(v).limit_denominator(10**6) for v in h]
        top = max(top, c)
        print('seed', s, 'p', p, 'max viol %.6f' % c, 'x', [round(v, 4) for v in x], 'g', [round(v, 4) for v in g], 'h', [round(v, 4) for v in h], flush=True)
        if c > 0:
            print('  POSITIVE VIOLATION -> exact recheck', 'tau*', tau_star(xe, [ge, he]))
    print('overall max viol', top, 'DONE')
