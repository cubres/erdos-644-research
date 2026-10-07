import random, itertools, collections, b3lib as B, gen
from test_canon import T_ok, V_ok
rng = random.Random(5); cnt = collections.Counter(); n = 0; only = collections.Counter()
for it in range(20000):
    r = gen.rand_inst(rng, 3, TGT=0.7505, tries=200)
    if r is None: continue
    x, T = r; S, sig, e = B.regime(x, T)
    if sorted(len(s) for s in S) != [1, 1, 1]: continue
    rep = [S[i][0] for i in range(3)]; t = [T[j] for j in rep]; n += 1
    ok = []
    for X, Y, Z in itertools.permutations(range(3)):
        if T_ok(x, t[X], t[Y], t[Z]): ok.append('T' + 'ABC'[X] + 'ABC'[Y] + 'ABC'[Z])
    for s_, u_ in itertools.permutations(range(3), 2):
        if V_ok(x, t[s_], t[u_]): ok.append('V' + 'ABC'[s_] + 'ABC'[u_])
    cnt[len(ok) > 0] += 1
    if len(ok) <= 2: only[tuple(ok)] += 1
print(n, cnt, only.most_common(20))
