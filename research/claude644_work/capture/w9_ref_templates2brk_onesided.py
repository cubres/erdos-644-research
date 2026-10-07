# Referee w9 (BREAK-IT), templates#2: SCOPE of the significance claim "one-sided |I|<=2 are special cases of H2".
# A one-sided box family with boxes A={a_1>=thA}, B={a_2>=thB} over parts {1,2} u L contains types heavy at L
# (e.g. (thA,0,1-thA) when 1-thA > 4x_L/7), so |H(C)| can be 3 and H2 does not apply verbatim.  Repair: restrict to
# C' = C cap {a_l <= 4x_l/7 for l in L} (closed, heavy only in {1,2}); hand argument: tau*(C') >= min(dA+dB, xA+xB-1)
# >= 3/4.  Here: exact grid check of the example and of random one-sided grid families (tau*(C)>=3/4 => tau*(C')>=3/4,
# and the H2 recipe on C' succeeds, verified at Venn level).
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w9_ref_templates2brk_lib import tau_star, heavy, recipe
def comps(D, p):
    if p == 1: yield (D,); return
    for k in range(D + 1):
        for r in comps(D - k, p - 1): yield (k,) + r
def family(x, thA, thB, D):
    p = len(x); C = []
    for c in comps(D, p):
        a = [F(v, D) for v in c]
        if any(a[i] > x[i] for i in range(p)): continue
        if a[0] >= thA or a[1] >= thB: C.append(a)
    return C
x = [F(1), F(1), F(1, 2)]; C = family(x, F(3, 5), F(3, 5), 20)
Hs = sorted({i for t in C for i in range(3) if heavy(t, x, i)})
Cp = [t for t in C if not any(heavy(t, x, l) for l in range(2, 3))]
print('example x=(1,1,1/2), thA=thB=3/5, grid 1/20: heavy parts', Hs, ' tau*(C)=', tau_star(x, C), ' tau*(C\')=', tau_star(x, Cp))
assert Hs == [0, 1, 2] and [F(3, 5), F(0), F(2, 5)] in C
res = recipe(x, Cp); print('  recipe on C\':', res[0], 'slack', res[1])
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
n = nh3 = 0
for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 300):
    p = rng.choice([3, 3, 4]); D = {3: 20, 4: 10}[p]
    x = [F(rng.randint(20, 32), 20), F(rng.randint(20, 32), 20)] + [F(rng.randint(1, 30), 20) for _ in range(p - 2)]
    thA = F(rng.randint(0, D), D); thB = F(rng.randint(0, D), D)
    if not (7 * thA > 4 * x[0] and 7 * thB > 4 * x[1] and thA <= x[0] and thB <= x[1]): continue
    C = family(x, thA, thB, D)
    ts = tau_star(x, C)
    if ts < F(3, 4): continue
    n += 1
    Cp = [t for t in C if not any(heavy(t, x, l) for l in range(2, p))]
    if len(Cp) < len(C): nh3 += 1
    tp = tau_star(x, Cp)
    assert tp >= F(3, 4), ('restriction drops tau*', x, thA, thB, ts, tp)
    r = recipe(x, Cp); assert r[1] >= 0
print('random one-sided grid families with tau*>=3/4:', n, ' of which with types heavy outside {1,2}:', nh3,
      ' restriction kept tau*>=3/4 and recipe succeeded in all. PASS')
