import random, sys, itertools, numpy as np, b3lib as B, gen
TOL = 1e-12
def T_ok(x, a, b, c):
    for i in range(3):
        if 2*a[i]+b[i] > 2*x[i]+TOL or 2*a[i]+c[i] > 2*x[i]+TOL or 2*b[i]+c[i] > 2*x[i]+TOL or 4*a[i]+2*b[i]+c[i] > 4*x[i]+TOL: return False
    return True
def V_ok(x, s, t):
    return all(s[i]+t[i] <= x[i]+TOL and 1.25*s[i]+0.5*t[i] <= x[i]+TOL for i in range(3))
def canon(x, T):
    S, sig, e = B.regime(x, T)
    mins = [[j for j in S[i] if abs(T[j][i]-sig[i]) < 1e-12] for i in range(3)]
    return S, sig, e, mins
def stratA(x, T, S, sig, e, mins):
    for al in itertools.product(*mins):
        ok = False
        for X, Y, Z in itertools.permutations(range(3)):
            if T_ok(x, T[al[X]], T[al[Y]], T[al[Z]]): ok = True; break
        if not ok: return False
    return True
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); m = int(sys.argv[2]); n = int(sys.argv[3])
    cnt = [0, 0]; fails = []
    for k in range(n):
        r = gen.rand_inst(rng, m)
        if r is None: continue
        x, T = r; S, sig, e, mins = canon(x, T)
        a = stratA(x, T, S, sig, e, mins)
        cnt[a] += 1
        if not a and len(fails) < 3: fails.append((x, T))
    print("stratA fail/ok", cnt)
    for f in fails: print(f)
