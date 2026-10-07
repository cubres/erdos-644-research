"""EXACT check: Conjecture H3 ('|H|>=3 and tau*>3/4 => Fano tuple') is FALSE, and so is the refined
H3* ('every 2-heavy-part subfamily C|S has tau*<=3/4').  Construction: W(x,s) two-part Fano-free family plus a
tiny third part C carrying a slightly shifted copy gamma of the A-heavy type."""
from fractions import Fraction as F
import heavylib as h
def report(name, x, T):
    t = h.tau_star(x, T)
    fano = h.any_fano(x, T, tol=0)
    heavy = [[i for i in range(len(x)) if 7*a[i] > 4*x[i]] for a in T]
    print(name, "x=", [str(v) for v in x], "tau*=", t, float(t), "heavy sets", heavy, "Fano:", fano)
    return t, fano
# (1) H3 counterexample: W(5/4, 3/20) + tiny part
eps = F(1,100); c = F(3,2)*eps
x = [F(5,4), F(5,4), c]
T = [[F(3,20), F(17,20), 0], [F(17,20), F(3,20), 0], [F(17,20)-eps, F(3,20), eps]]
for a in T: assert sum(a) == 1 and all(0 <= a[i] <= x[i] for i in range(3))
report("H3-cex", x, T)
# (2) H3* counterexample: x_A=x_B chosen so tau*(W)<3/4, tiny part pushes tau* over 3/4
xa = F(12245,10000)
x2 = [xa, xa, c]
report("W alone (2 parts)", [xa, xa], [[F(3,20), F(17,20)], [F(17,20), F(3,20)]])
report("W|{A,C}", x2, [T[1], T[2]]); report("W|{B,C}", x2, [T[0]])
report("H3*-cex", x2, T)
