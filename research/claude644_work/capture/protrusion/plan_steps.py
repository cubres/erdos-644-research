# Adversary plans whose sources are step-classes: at step j reuse (non-avoided, non-forced, threatening) vertices
# containing step a1, then those containing a2, ... (priority), capped by the budget. MILP evaluation.
import sys, itertools
sys.path.insert(0, '.')
from plan_milp import parse, evaluate, present_patterns, threatening, is_forced, fmt

def expand(lines, budgets, splan):
    """splan: dict j -> list of earlier steps. Build pattern plan incrementally."""
    plan = {}
    for j in range(7):
        if budgets[j] == 0 or j not in splan: continue
        pats = present_patterns(lines, budgets, plan, j)
        src = []
        for a in splan[j]:
            for p in sorted(pats, key=lambda p: (len(p), sorted(p))):
                if a in p and p not in src and threatening(lines, p, j):
                    src.append(p)
        plan[j] = src
    return plan

def search(lines, budgets, maxlen=2, target=None, verbose=False):
    best = [0, None, None]
    steps = [j for j in range(7) if budgets[j]]
    def dfs(idx, splan):
        if target is not None and best[0] >= target - 1e-9: return
        if idx == len(steps):
            plan = expand(lines, budgets, splan)
            v = evaluate(lines, budgets, plan)
            if v is not None and v > best[0] + 1e-9:
                best[0] = v; best[1] = dict(splan); best[2] = plan
                if verbose: print(round(v, 6), splan, flush=True)
            return
        j = steps[idx]
        earlier = [a for a in steps if a < j]
        opts = [[]]
        for r in range(1, maxlen + 1):
            for comb in itertools.permutations(earlier, r):
                opts.append(list(comb))
        for o in opts:
            if o: splan[j] = o
            dfs(idx + 1, splan)
            splan.pop(j, None)
    dfs(0, {})
    return best

if __name__ == '__main__':
    mode = sys.argv[1]; ml = int(sys.argv[2]); tg = float(sys.argv[3])
    budgets = [1]*7 if mode == 'u' else [0]+[1]*6
    for line in open('orders.txt'):
        lines = parse(line.strip())
        b = search(lines, budgets, ml, tg)
        print(round(b[0], 6), '|', line.strip(), '|', b[1], '|', fmt(b[2]) if b[2] else None, flush=True)
