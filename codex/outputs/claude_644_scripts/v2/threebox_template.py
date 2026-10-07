import random, sys, itertools
from threebox_fano import fano_lp
rng = random.Random(11)
# template: quadrilateral missing point 6 -> box A; pencil at 6: L2,L4 -> box B, L5 -> box C
# line order: L0 012, L1 034, L2 056, L3 135, L4 146, L5 236, L6 245
def template(A, B, C):
    return (A, A, B, A, B, C, A)
def sample(lo, hi):
    while True:
        x = [rng.uniform(0.2, 1.4) for _ in range(3)]
        th = [xi - rng.uniform(0, 3*xi/7) for xi in x]
        if sum(th) < 1 or any(t > 1 for t in th): continue
        d = sum(xi - ti for xi, ti in zip(x, th))
        if lo < d < hi: return x, th, d
perms = list(itertools.permutations(range(3)))
for lo, hi in [(0.75, 0.7505), (0.75, 0.9), (0.70, 0.75)]:
    allperm_ok = 0; some_ok = 0; none = 0; N = 300
    for _ in range(N):
        x, th, d = sample(lo, hi)
        oks = [fano_lp(x, th, template(*p)) for p in perms]
        if all(oks): allperm_ok += 1
        if any(oks): some_ok += 1
        else: none += 1
    print(f"tau* in ({lo},{hi}): all 6 labelings work {allperm_ok}/{N}; some labeling works {some_ok}/{N}; none {none}", flush=True)
