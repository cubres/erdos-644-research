"""Referee w9 typeclosed#0: literal e2e of THEOREM L (4/7-light version) incl. the Q_b / Q_a branch.
Families: parts j=0,k=1; light parts 4/7-light; heavy types with heavy coordinate spread over (4x/7, 4x/7+0.25]
so that theta can land below or above 2x/3.  Hom Fano: 7 rows e, mass e/4 on each Fano point cell.
Q_b = pencil template with e:=b (3 lines through p0) and f:=a (4 m-lines); Q_a mirror."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed0brk_lib import *
from w9_ref_typeclosed0brk_e2e import split_mass, rnd

def hom_masses(e):
    return {FANO_CELLS[q]: e / 4 for q in range(7)}

def gen(den):
    p = random.randint(2, 4)
    x = [F(random.randint(int(0.6 * den), int(1.6 * den)), den) for _ in range(2)] + \
        [F(random.randint(0, 3 * den // 2), den) for _ in range(p - 2)]
    cl = [4 * x[i] / 7 for i in range(p)]
    C = []
    for _ in range(random.randint(2, 7)):
        kind = random.random()
        if kind < 0.08:
            v = split_mass(F(1), cl, den)
        else:
            h = 1 if kind < 0.54 else 0
            lo = 4 * x[h] / 7
            ch = rnd(lo, min(F(1), x[h], lo + F(random.choice([2, 5, 10, 15]), 60)), den)
            if ch is None: continue
            caps = [x[i] if i == 1 - h else cl[i] for i in range(p)]; caps[h] = F(0)
            v = split_mass(1 - ch, caps, den)
            if v is None: continue
            v[h] = ch
        if v and all(F(0) <= v[i] <= x[i] for i in range(p)): C.append(v)
    Cs = []
    for c in C:
        if c not in Cs: Cs.append(c)
    return x, Cs

def proofL(x, C, tau):
    p = len(x); j, k = 0, 1; T = F(3, 4)
    for e in C:
        if all(7 * e[i] <= 4 * x[i] for i in range(p)):
            ok, msg = realise_and_check([e] * 7, x, [hom_masses(e[i]) for i in range(p)]); assert ok, msg
            return 'hom'
    A = [c for c in C if 7 * c[k] > 4 * x[k]]; B = [c for c in C if 7 * c[j] > 4 * x[j]]
    assert all(c in A or c in B for c in C) and A and B
    tk = min(c[k] for c in A); tj = min(c[j] for c in B)
    assert (x[j] - tj) + (x[k] - tk) >= tau > T
    a = min(A, key=lambda c: c[k]); b = min(B, key=lambda c: c[j])
    if 3 * tj <= 2 * x[j]:
        # GGP facets
        assert b[j] + a[k] > 1
        for i in range(p):
            assert 3 * b[i] / 2 <= x[i] and a[i] + 3 * b[i] / 4 <= x[i], ('Q_b fails part', i)
        ok, msg = realise_and_check([b, b, b, a, a, a, a], x, [pencil_masses(b[i], a[i]) for i in range(p)])
        assert ok, msg
        return 'Q_b'
    if 3 * tk <= 2 * x[k]:
        for i in range(p):
            assert 3 * a[i] / 2 <= x[i] and b[i] + 3 * a[i] / 4 <= x[i], ('Q_a fails part', i)
        ok, msg = realise_and_check([a, a, a, b, b, b, b], x, [pencil_masses(a[i], b[i]) for i in range(p)])
        assert ok, msg
        return 'Q_a'
    assert x[j] + x[k] > F(9, 4)
    wit = [c for c in C if all(c[i] <= x[i] - a[i] for i in range(p) if i != k) and c[k] < tk]
    assert wit
    c = wit[0]; assert c in B
    ok, msg = realise_and_check([c, c, a, a, a, a, a], x, [V_masses(a[i], c[i]) for i in range(p)])
    assert ok, msg
    return 'V'

if __name__ == '__main__':
    seed = int(sys.argv[1]); target = int(sys.argv[2]); random.seed(seed)
    st = {}; tried = 0
    while sum(st.values()) < target:
        tried += 1
        x, C = gen(random.choice([24, 30, 36, 60, 120]))
        if not C: continue
        tau = tau_star(C, x)
        if tau <= F(3, 4): continue
        try:
            br = proofL(x, C, tau)
        except AssertionError as ex:
            br = 'FAIL'; print('FAIL', ex, x, C, tau, flush=True)
        st[br] = st.get(br, 0) + 1
    print('thmL seed', seed, 'tried', tried, st, flush=True)
