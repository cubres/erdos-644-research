"""crude DFS progress from a cegar5 checkpoint: fraction of the tree (uniform-subtree model) already finished."""
import sys, pickle, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_cert3 import Strategy3, Engine3
for name in sys.argv[1:]:
    st = pickle.load(open('certs/ck5_%s.pkl' % name, 'rb')); stack = st['stack']
    if not stack: print(name, 'empty stack'); continue
    S = Strategy3(st['spec'], F(0), fk=7, menu=('F', 'V', 'T3', 'R', 'W'), lazy=True); E = Engine3(S)
    deepest = max(stack, key=lambda e: len(e[0]))[0]
    # pending indices per level along the prefix of the deepest path
    frac_done = 0.0; weight = 1.0
    for L in range(len(deepest)):
        nm = deepest[L][0]
        n = len(E.disj(nm))
        prefix = deepest[:L]
        pend = sorted(p[L][1] for p, _ in stack if len(p) > L and p[:L] == prefix)
        cur = min(pend) if pend else 0     # DFS explores high indices first; indices below min(pend) untouched
        # alternatives with index > max pending were finished
        done = n - 1 - max(pend) if pend else n - 1
        frac_done += weight * done / n
        weight *= 1.0 / n
        if weight < 1e-12: break
    print('%s: nodes %d leaves %d stack %d, finished fraction (uniform model) ~ %.4f' % (name, st['nodes'], st['nleaves'], len(stack), frac_done))
