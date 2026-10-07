import sys
sys.path.insert(0, '.')
from plan_search import *
mode = sys.argv[1]; ms = int(sys.argv[2])
budgets = [1]*7 if mode == 'u' else [0]+[1]*6
for line in open('orders.txt'):
    lines = parse(line.strip())
    b = search(lines, budgets, ms)
    print(round(b[0], 6), '|', line.strip(), '|', {k: [''.join(map(str, sorted(p))) for p in s] for k, s in b[1].items() if s}, flush=True)
