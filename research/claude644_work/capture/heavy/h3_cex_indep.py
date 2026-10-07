"""Independent check of the H3 counterexamples: explicit class-mass Fano LP (mine/upbox_fano.fano, HiGHS) over
ALL 3^7 line->type maps (no symmetry reduction, no Lemma 7.63), and tau* by brute-force blocking maps."""
import sys, itertools
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/mine')
from upbox_fano import fano, tau_star
for name, x, T in [("H3-cex", [1.25, 1.25, 0.015], [[0.15, 0.85, 0], [0.85, 0.15, 0], [0.84, 0.15, 0.01]]),
                   ("H3*-cex", [1.2245, 1.2245, 0.015], [[0.15, 0.85, 0], [0.85, 0.15, 0], [0.84, 0.15, 0.01]])]:
    feas = [asg for asg in itertools.product(range(3), repeat=7) if fano(x, T, asg)]
    print(name, "tau* =", round(tau_star(x, T), 6), " feasible Fano maps:", len(feas), "of", 3**7)
