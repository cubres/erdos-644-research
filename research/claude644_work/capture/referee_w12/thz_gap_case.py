"""Referee w12, claim generalp#0 (Theorem M, Th_Z version).
Exhibits the boundary case missing from the written proof of the 'sup-distance 1' claim and checks the fix.
Setting (notes_generalp.md item (8), Th_Z version): row (v,z) of G'_{Mr} dominates (Mg - e_i, 1), z = 1,
|v| = Mr - 1, part i has NO room (v_i > M n_i - 1).  The text says 'v_i = M n_i >= M g_i so v >= Mg'.
Rows are REAL, so v_i can lie strictly between M n_i - 1 and M n_i; if g_i = n_i then v_i < M g_i and
v + e_m is NOT >= Mg for any m.  Fix: u' = v + a e_i + (1-a) e_m with a = M n_i - v_i in (0,1), m a part with
room >= 1 (exists by the counting argument, and m != i).  Exact rational check.
"""
from fractions import Fraction as F
import itertools, random

def in_G(u, gens, n, R):
    # u in G_R := { u : |u| = R, g <= u <= n for some g }
    if sum(u) != R: return False
    if any(ui > ni for ui, ni in zip(u, n)): return False
    return any(all(ui >= gi for ui, gi in zip(u, g)) for g in gens)

def gap_case():
    p = 3; n = (2, 3, 4); r = 5
    g = (2, 1, 1)                  # g_1 = n_1: generator at capacity in part 1 ; |g| = 4 <= r
    gens = [g]
    N = sum(n); M = 4              # M > p/(N-r) = 3/4 ; (delta irrelevant here)
    Mg = tuple(M*gi for gi in g); Mn = tuple(M*ni for ni in n); R = M*r
    i = 0                          # i(g): g_0 = 2 >= 1
    gen2 = (Mg[0]-1, Mg[1], Mg[2]) # (Mg - e_i)
    # a row (v,1) of G'_{Mr}: v >= Mg - e_i, v <= Mn, |v| = Mr - 1, with v_i = Mn_i - 1/2 (no room, non-integer)
    v = [F(Mn[0]) - F(1,2), F(gen2[1]), F(0)]
    v[2] = F(R - 1) - v[0] - v[1]
    v = tuple(v)
    assert all(vi >= gi for vi, gi in zip(v, gen2)) and all(vi <= ni for vi, ni in zip(v, Mn)) and sum(v) == R-1
    print("row v =", v, " Mg =", Mg, " Mn =", Mn, " |v| = Mr-1 =", sum(v))
    print("part i has no room (v_i > Mn_i - 1):", v[i] > Mn[i]-1, "; v_i = Mn_i ?", v[i] == Mn[i], "; v >= Mg ?", all(vi >= gi for vi, gi in zip(v, Mg)))
    for m in range(p):
        u = list(v); u[m] += 1
        print(f"  v + e_{m} in G_Mr ?", in_G(tuple(u), [Mg], Mn, R))
    # the fix
    a = F(Mn[i]) - v[i]
    rooms = [m for m in range(p) if m != i and v[m] <= Mn[m] - 1]
    assert rooms, "counting argument guarantees a part with room >= 1"
    m = rooms[0]
    u = list(v); u[i] += a; u[m] += 1 - a; u = tuple(u)
    print("  fix: u' = v + a e_i + (1-a) e_m, a =", a, " m =", m, " u' =", u, " in G_Mr ?", in_G(u, [Mg], Mn, R),
          " sup|u'-v| <= 1 ?", max(abs(ui-vi) for ui, vi in zip(u, v)) <= 1)

def random_fix_check(trials=3000, seed=1):
    """For random (n, r, Gen) and random REAL rows (v,z) of G'_{Mr}: the two-case recipe (with the fix) always
    produces u' in G_{Mr} with 0 <= u' - v <= 1 coordinatewise."""
    rnd = random.Random(seed); bad = 0
    for t in range(trials):
        p = rnd.randint(2, 4)
        n = tuple(rnd.randint(1, 5) for _ in range(p)); N = sum(n)
        r = rnd.randint(1, max(1, N - 1))
        gens = []
        for _ in range(rnd.randint(1, 3)):
            g = [rnd.randint(0, ni) for ni in n]
            while sum(g) > r:
                k = rnd.randrange(p); g[k] = max(0, g[k]-1)
            if sum(g) == 0: g[rnd.randrange(p)] = 1 if r >= 1 and n[rnd.randrange(p)] >= 1 else 0
            if sum(g) >= 1 and sum(g) <= r and all(gi <= ni for gi, ni in zip(g, n)): gens.append(tuple(g))
        if not gens: continue
        M = p // (N - r) + 1 + rnd.randint(0, 3)          # M > p/(N-r)
        Mn = tuple(M*ni for ni in n); R = M*r
        # pick a random real row of G'_{Mr}
        g = rnd.choice(gens); Mg = tuple(M*gi for gi in g)
        kind = rnd.randint(0, 1)
        if kind == 0:
            z = F(rnd.randint(0, 8), 8); base = Mg
        else:
            z = F(1); i = rnd.choice([k for k in range(p) if g[k] >= 1]); base = list(Mg); base[i] -= 1; base = tuple(base)
        # raise base to mass R - z within Mn, random real increments
        v = [F(b) for b in base]; need = F(R) - z - sum(v)
        if need < 0: continue
        order = list(range(p)); rnd.shuffle(order)
        for k in order:
            add = min(need, F(Mn[k]) - v[k]) * F(rnd.randint(0, 4), 4) if k != order[-1] else min(need, F(Mn[k]) - v[k])
            v[k] += add; need -= add
        if need != 0: continue
        v = tuple(v)
        # recipe
        rooms = [m for m in range(p) if v[m] <= Mn[m] - z]
        assert rooms, "counting argument failed?!"
        if kind == 0:
            m = rooms[0]; u = list(v); u[m] += z
        else:
            if v[i] <= Mn[i] - 1:
                u = list(v); u[i] += 1
            else:
                a = F(Mn[i]) - v[i]; ms = [m for m in rooms if m != i]; assert ms
                u = list(v); u[i] += a; u[ms[0]] += 1 - a
        u = tuple(u)
        ok = in_G(u, [tuple(M*gi for gi in gg) for gg in gens], Mn, R) and all(0 <= ui - vi <= 1 for ui, vi in zip(u, v))
        if not ok: bad += 1; print("FAIL", n, r, gens, M, v, u)
    print("random fix check: trials", trials, "failures", bad)

if __name__ == "__main__":
    gap_case(); random_fix_check()
