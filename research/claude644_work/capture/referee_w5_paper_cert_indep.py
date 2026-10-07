# referee_w5_paper_cert_indep.py -- referee (w5, "certificate" claim) independent checks.
# (1) Mutation sensitivity of w5_paper_prop10_vertices.py and w5_paper_constants.py (source-patched copies).
# (2) From-scratch random integer check of Prop 4.1 (paper_0865.tex) at LARGE r (1000..10^7) and at
#     random T in [ceil(beta r + 3), r] (not only the minimal T), following the paper's case chain on
#     exact normalised values and checking the INTEGER hypotheses of the lemma used, as stated in Sec. 3.
import random, subprocess, sys, os, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))

def run_patched(src, subs, args=()):
    code = open(os.path.join(HERE, src)).read()
    for a, bb in subs:
        assert a in code, (src, a)
        code = code.replace(a, bb, 1)
    p = subprocess.run([sys.executable, '-c', code, *args], capture_output=True, text=True, cwd=HERE)
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-300:]

print('--- (1) mutation sensitivity ---')
muts = [
  ('budget 0.8645', [('b = F(173, 200); e = 1 - b', 'b = F(17290, 20000); e = 1 - F(173,200)')]),
  ('budget 0.8645 incl e', [('b = F(173, 200); e = 1 - b', 'b = F(17290, 20000); e = 1 - b')]),
  ('h = 93/200', [('h = F(92, 200)', 'h = F(93, 200)')]),
  ('m+2y <= 228/200', [('le((1, 2, 0), 2 - b)', 'le((1, 2, 0), 2 - b + F(1,200))')]),
  ('case a up to 120/400', [("le((1, 0, 0), F(119, 400))]), lambda m, y, z: L18(m))",
                            "le((1, 0, 0), F(120, 400))]), lambda m, y, z: L18(m))")]),
  ('c4 splitB swapped', [('def splitB(m, y, z): return (e + y - z, e + m - z, z)',
                          'def splitB(m, y, z): return (e + m - z, e + y - z, z)')]),
]
for name, subs in muts:
    print(f'{name:24s} ->', run_patched('w5_paper_prop10_vertices.py', subs))
cmuts = [
  ('K = cb+9', [('K = cb + 10', 'K = cb + 9')]),
  ('K = cb+8', [('K = cb + 10', 'K = cb + 8')]),
  ('T = cb+3 (5.1/5.3)', [('T = cb + 4', 'T = cb + 3')]),
]
for name, subs in cmuts:
    print(f'{name:24s} ->', run_patched('w5_paper_constants.py', subs, ('1000', '20000')))

print('--- (2) random large-r integer check of Prop 4.1 ---')
b = Fr(173, 200); e = 1 - b
def cdiv(a, d): return -((-a) // d)
def hyp(r, T, lemma, x, y, z, splits=None):
    S = x + y + z
    if lemma == 'L18':   # budget ceil(max((3r+m)/4,(2r+2m)/3)) <= T, m <= r/2 (x = m)
        m = x
        return 2 * m <= r and max(cdiv(3 * r + m, 4), cdiv(2 * r + 2 * m, 3)) <= T
    if lemma == 'L26':
        return (T >= S and T >= r - x + z and T >= r - y + z and 2 * T >= 2 * r - 2 * x + y
                and 2 * T >= 2 * r - 2 * y + x and 3 * T >= r + 2 * x + 2 * y + z)
    if lemma == 'L32':
        return (T <= r and T >= S and 2 * T >= r + 2 * y and 2 * T >= r + 2 * x - y + z
                and 3 * T >= r + 2 * x + y + 3 * z)
    if lemma == 'L31':
        return (T <= r and T >= x + y and 2 * T >= r + 2 * x and 2 * T >= r + 2 * y and T >= r + x - y - z
                and T >= r - x + y - z and 3 * T >= 3 * r - S and 5 * T >= 3 * r + S
                and 3 * T >= r + x + y + 2 * z and 4 * T >= 2 * r + 3 * z)
    if lemma == 'S2':
        P = max(0, r + y - x - z - T); Q = max(0, r + x - y - z - T)
        return (x <= T and y <= T and T >= r - x + z + P + Q and T >= y + z + Q
                and 2 * T >= r + y + 2 * z + P + 2 * Q)
    if lemma == 'S1':
        x1, y1, z1 = splits
        return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1 + y1 + z1 <= T
                and y1 + z1 >= r + x - T and x1 + z1 >= r + y - T and x1 + y1 >= r + z - T)

def ceilF(q): return -((-q.numerator) // q.denominator)

def prop(r, T, m, y, z):
    M, Yn, Zn = Fr(m, r), Fr(y, r), Fr(z, r)
    if M <= Fr(119, 400):
        return 'a', hyp(r, T, 'L18', m, y, z)
    Sn = M + Yn + Zn
    if Yn <= Fr(73, 200):
        if Yn - Zn > M - e: return 'b2', hyp(r, T, 'L32', m, y, z)
        if Sn < Fr(81, 200): return 'b3', hyp(r, T, 'L32', z, y, m)
        return 'b1', hyp(r, T, 'L31', z, y, m)
    u = M + Yn; d = M - Yn
    if Zn <= Fr(319, 200) - 2 * u: return 'c1', hyp(r, T, 'L26', m, y, z)
    if Zn < e - d: return 'c2', hyp(r, T, 'S2', y, m, z)
    if Zn <= (Fr(146, 200) - Yn) / 2: return 'c3', hyp(r, T, 'S2', m, y, z)
    if 3 * Zn >= e + u:
        sp = ((e + Yn + Zn - M) / 2, (e + M + Zn - Yn) / 2, (e + M + Yn - Zn) / 2); tag = 'c4A'
    else:
        sp = (e + Yn - Zn, e + M - Zn, Zn); tag = 'c4B'
    return tag, hyp(r, T, 'S1', m, y, z, tuple(ceilF(s * r) for s in sp))

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
cnt = {}; fails = []
for it in range(N):
    r = rng.choice([rng.randint(1000, 5000), rng.randint(1000, 10**7)])
    Tmin = cdiv(173 * r + 600, 200)
    T = Tmin if rng.random() < 0.6 else rng.randint(Tmin, r)
    hmax = (23 * r) // 50
    # bias toward the (c) region and boundaries
    if rng.random() < 0.5:
        y = rng.randint(cdiv(73 * r, 200), (227 * r) // 600)
        m = rng.randint(y, min(hmax, (227 * r - 400 * y) // 200))
    else:
        m = rng.randint(0, hmax)
        y = rng.randint(0, min(m, (227 * r - 200 * m) // 400))
    if y > m or 200 * (m + 2 * y) > 227 * r or m > hmax: continue
    z = rng.randint(0, y) if rng.random() < 0.7 else rng.choice([0, y, max(0, y - 1), rng.randint(0, y)])
    tag, ok = prop(r, T, m, y, z)
    cnt[tag] = cnt.get(tag, 0) + 1
    if not ok: fails.append((r, T, m, y, z, tag))
print('counts', dict(sorted(cnt.items())), 'failures', len(fails), fails[:5])
# mutation: T one below the allowed minimum must fail somewhere (only c4 rounding uses the +3)
mf = 0
for it in range(100000):
    r = rng.randint(1000, 10**6); T = cdiv(173 * r + 600, 200) - 3
    y = rng.randint(cdiv(73 * r, 200), (227 * r) // 600); m = rng.randint(y, min((23 * r) // 50, (227 * r - 400 * y) // 200))
    if y > m: continue
    z = rng.randint(0, y)
    tag, ok = prop(r, T, m, y, z)
    mf += (not ok)
print('mutation T = ceil(beta r) (no +3): failures', mf)
