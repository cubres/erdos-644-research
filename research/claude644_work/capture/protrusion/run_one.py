import sys, time
sys.path.insert(0, '.')
from discrete_game import make_solver
tl = eval(sys.argv[1])
mode = sys.argv[2]
ms = [int(x) for x in sys.argv[3].split(',')]
budgets = [1] * 7 if mode == 'u' else [0] + [1] * 6
for m in ms:
    t0 = time.time()
    val = make_solver([frozenset(L) for L in tl], budgets, m)
    v = val(0, ())
    print(m, v, round(time.time() - t0, 1), val.cache_info().currsize, flush=True)
