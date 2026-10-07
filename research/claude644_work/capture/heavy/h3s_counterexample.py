"""EXACT: Conjecture H3s (every type heavy at EXACTLY one part, >=3 parts host heavy types, tau*>3/4 => Fano)
is FALSE.  W-like Fano-free core on parts A,C plus an independent near-pure type at B.  Also lists the pair
templates (42-function catalogue) that do kill it."""
from fractions import Fraction as F
import itertools, heavylib as h, pairlib as P
x = [F(861,1000), F(1440,1000), F(741,1000)]
T = [[F(664,1000), F(0), F(336,1000)],      # alpha: heavy only at A
     [F(19,1000), F(981,1000), F(0)],        # beta : heavy only at B
     [F(424,1000), F(0), F(576,1000)]]       # gamma: heavy only at C
for a in T: assert sum(a) == 1 and all(0 <= a[i] <= x[i] for i in range(3))
hs = [[i for i in range(3) if 7*a[i] > 4*x[i]] for a in T]
sup = [[i for i in range(3) if 3*a[i] > 2*x[i]] for a in T]
t = h.tau_star(x, T)
print("heavy sets", hs, "super-heavy sets", sup)
print("tau* =", t, "=", float(t))
print("Fano (exact Lemma 7.63 over orbit reps):", h.any_fano(x, T, tol=0))
import sys; sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/mine')
from upbox_fano import fano as lpfano
xf = [float(v) for v in x]; Tf = [[float(v) for v in a] for a in T]
print("Fano (class-mass LP, all 3^7 maps):", sum(1 for asg in itertools.product(range(3), repeat=7) if lpfano(xf, Tf, asg)))
# exact pair check over the 42 functions
from fractions import Fraction as Fr
import json
D = json.load(open('astra_support_capacity_minimal.json'))
FUN = [[(Fr(u), Fr(v)) for u, v in f['vertices']] for f in D['minimal_functions']]
names = ['alpha', 'beta', 'gamma']
for j, l in itertools.product(range(3), repeat=2):
    for k, V in enumerate(FUN):
        if all(max(u*T[j][i] + v*T[l][i] for u, v in V) <= x[i] for i in range(3)):
            print("pair template: fn%d (s=%s, t=%s) vertices %s" % (k, names[j], names[l], [(str(u), str(v)) for u, v in V]))
