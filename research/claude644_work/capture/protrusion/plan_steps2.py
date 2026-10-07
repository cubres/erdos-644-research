import sys, itertools
sys.path.insert(0, '.')
from plan_milp import parse, evaluate, present_patterns, threatening, is_forced, fmt

def search(lines, budgets, maxlen=2, target=None, verbose=False):
    best = [0, None]
    steps = [j for j in range(7) if budgets[j]]
    seen = set()
    def dfs(idx, plan):
        if target is not None and best[0] >= target - 1e-9: return
        if idx == len(steps):
            key = tuple((j, tuple(tuple(sorted(p)) for p in plan[j])) for j in sorted(plan))
            if key in seen: return
            seen.add(key)
            v = evaluate(lines, budgets, plan)
            if v is not None and v > best[0] + 1e-9:
                best[0] = v; best[1] = {k: list(s) for k, s in plan.items()}
                if verbose: print(round(v, 6), fmt(plan), flush=True)
            return
        j = steps[idx]
        pats = present_patterns(lines, budgets, plan, j)
        thr = sorted([p for p in pats if threatening(lines, p, j)], key=lambda p: (len(p), sorted(p)))
        earlier = sorted(set(a for p in thr for a in p))
        opts = [[]]
        for r in range(1, maxlen + 1):
            for comb in itertools.permutations(earlier, r):
                src = []
                for a in comb:
                    for p in thr:
                        if a in p and p not in src: src.append(p)
                opts.append(src)
        # dedupe
        uniq = []
        for o in opts:
            if o not in uniq: uniq.append(o)
        for o in uniq:
            if o: plan[j] = o
            dfs(idx + 1, plan)
            plan.pop(j, None)
    dfs(0, {})
    return best

if __name__ == '__main__':
    mode = sys.argv[1]; ml = int(sys.argv[2]); tg = float(sys.argv[3])
    only = sys.argv[4] if len(sys.argv) > 4 else None
    budgets = [1]*7 if mode == 'u' else [0]+[1]*6
    for line in open('orders.txt'):
        if only and line.strip() != only: continue
        lines = parse(line.strip())
        b = search(lines, budgets, ml, tg)
        print(round(b[0], 6), '|', line.strip(), '|', fmt(b[1]) if b[1] else None, flush=True)
