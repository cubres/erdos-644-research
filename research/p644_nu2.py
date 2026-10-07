"""Erdős #644 — matching-number-2 pattern families: how large can tau/r be?

Parts A1, A2 (size 1 each, they ARE edges) and an outside part X of size xi.  Mixed edges are
admitted by a union of boxes on (c1, c2) = (|C∩A1|, |C∩A2|) (c3 free, sizes sum to 1).
For each pattern with tau*/r (computed at scale m=48, so O(1/48) accurate) above a threshold we
run the Venn-cell MILP (continuous => asymptotic certificate).
NOTE (18 Sep): an earlier version computed tau at m = 2D = 8, whose O(1/m) error made one-sided
families {A1, A2, (3/4,1/4)} (true tau = r/4 + 2) look like tau/r = 1/2.  Fixed by M_TAU = 48.
"""
import sys, time, itertools
from p644_patterns import Pattern, tau_pattern, check_72

M_TAU = 48

def nu2_pattern(xi, boxes_c12):
    """boxes_c12: list of ((a1,a2),(b1,b2)) on (c1,c2); c3 unconstrained."""
    boxes = [((1.0, 0.0, 0.0), (1.0, 0.0, 0.0)), ((0.0, 1.0, 0.0), (0.0, 1.0, 0.0))]
    for (a1, a2), (b1, b2) in boxes_c12:
        boxes.append(((a1, a2, 0.0), (b1, b2, None)))
    x = [1.0, 1.0, xi] if xi > 0 else [1.0, 1.0]
    if xi == 0: boxes = [(lo[:2], hi[:2]) for lo, hi in boxes]
    return Pattern(x, 1.0, boxes=boxes, name=f'nu2 xi={xi} {boxes_c12}')

def tau_ratio(P): return tau_pattern(P.scaled(M_TAU)) / M_TAU

def enum_sym(D, xis=(0.0, 0.5, 1.0), min_ratio=0.3, tl=60, log=None):
    ivals = [(a / D, b / D) for a in range(1, D + 1) for b in range(a, D + 1)]
    tested = 0; survivors = []; t0 = time.time(); best = 0.0; best_surv = 0.0
    for xi in xis:
        for (a1, b1) in ivals:
            for (a2, b2) in ivals:
                if a1 + a2 > 1: continue
                if (a2, b2) < (a1, b1): continue      # mirror box added anyway
                bx = [((a1, a2), (b1, b2)), ((a2, a1), (b2, b1))]
                P = nu2_pattern(xi, bx); tau = tau_ratio(P)
                if tau > best: best = tau
                if tau < min_ratio - 1e-9: continue
                tested += 1
                st, info = check_72(P, m=None, time_limit=tl, intersecting=False)
                line = f"xi={xi} c1∈[{a1},{b1}] c2∈[{a2},{b2}] (+mirror) tau/r={tau:.4f}: {st} via {info.get('via')}"
                if log: log.write(line + '\n'); log.flush()
                if st != 'FAILS':
                    survivors.append(line); best_surv = max(best_surv, tau); print('  SURVIVOR', line, flush=True)
        print(f"  xi={xi} done: tested {tested}, survivors {len(survivors)}, best tau/r seen {best:.4f}, best surviving {best_surv:.4f} [{time.time()-t0:.0f}s]", flush=True)
    print(f"enum_sym D={D}: tested {tested}; survivors {len(survivors)}; best tau/r {best:.4f}; best surviving {best_surv:.4f}", flush=True)
    return survivors

def enum_two_boxes(D, xis=(0.0, 0.5), min_ratio=0.3, tl=60, log=None):
    """Two independent boxes (not necessarily mirror images)."""
    ivals = [(a / D, b / D) for a in range(1, D + 1) for b in range(a, D + 1)]
    boxes = [((a1, a2), (b1, b2)) for (a1, b1) in ivals for (a2, b2) in ivals if a1 + a2 <= 1]
    tested = 0; survivors = []; t0 = time.time(); best = 0.0; best_surv = 0.0
    for xi in xis:
        for i, B1 in enumerate(boxes):
            for B2 in boxes[i:]:
                P = nu2_pattern(xi, [B1, B2]); tau = tau_ratio(P)
                if tau > best: best = tau
                if tau < min_ratio - 1e-9: continue
                tested += 1
                st, info = check_72(P, m=None, time_limit=tl, intersecting=False)
                line = f"xi={xi} boxes {B1} {B2} tau/r={tau:.4f}: {st} via {info.get('via')}"
                if log: log.write(line + '\n'); log.flush()
                if st != 'FAILS':
                    survivors.append(line); best_surv = max(best_surv, tau); print('  SURVIVOR', line, flush=True)
        print(f"  xi={xi} done: tested {tested}, survivors {len(survivors)}, best {best:.4f}, best surviving {best_surv:.4f} [{time.time()-t0:.0f}s]", flush=True)
    print(f"enum_two_boxes D={D}: tested {tested}; survivors {len(survivors)}; best tau/r {best:.4f}; best surviving {best_surv:.4f}", flush=True)
    return survivors

if __name__ == '__main__':
    mode = sys.argv[1]; D = int(sys.argv[2]); mr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
    tl = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    with open(f'logs/nu2v2_{mode}_D{D}.log', 'a') as lg:
        if mode == 'sym': enum_sym(D, min_ratio=mr, tl=tl, log=lg)
        else: enum_two_boxes(D, min_ratio=mr, tl=tl, log=lg)
