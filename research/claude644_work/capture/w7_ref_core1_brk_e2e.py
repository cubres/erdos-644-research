# Referee w7 / core#1 BREAK-IT: end-to-end contrapositive test of the S-corollary on ARBITRARY families.
# For a random family H (n<=9), t=tau(H) exact, k=max edge size: if some multiset quadruple has
#   S < stated(t,k) = min(t, floor(3(2t-k-2)/2)+1)   [claim]      or
#   S < sharp(t,k)  = min(t, ceil(3(2t-k-1)/2))       [LINE-BY-LINE sharpening]
# then H must NOT be (7,2) (exact bad-subfamily DFS). Negative control: sharp+1 (expected to fail sometimes).
# Families: random, and 'near-(7,2)' ones = complete K_n^r with random edits (large tau).
import itertools, random, sys
sys.path.insert(0, '.')
from lib72 import find_bad_subfamily, tau, complete
def popc(x): return bin(x).count('1')
def S_of(G): return sum(popc(a & b) for a, b in itertools.combinations(G, 2))
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2])
cnt = {'fam': 0, 'st_hit': 0, 'sh_hit': 0, 'ctl_hit': 0, 'st_fail': 0, 'sh_fail': 0, 'ctl_fail': 0, 'is72': 0}
ctl_example = None
for it in range(N):
    n = rng.randint(5, 9)
    if rng.random() < 0.5:
        r = rng.randint(2, n - 2); E = complete(n, r)
        rng.shuffle(E); E = E[:rng.randint(4, len(E))] if len(E) > 4 else E
        for _ in range(rng.randint(0, 4)):
            E.append(sum(1 << v for v in rng.sample(range(n), rng.randint(max(1, r - 2), min(n - 1, r + 1)))))
    else:
        E = [sum(1 << v for v in rng.sample(range(n), rng.randint(1, n - 2))) for _ in range(rng.randint(4, 14))]
    E = list(set(E))
    if len(E) < 1: continue
    t = tau(E, n); k = max(popc(e) for e in E)
    if t < 2: continue
    cnt['fam'] += 1
    Smin = min(S_of(G) for G in itertools.combinations_with_replacement(E, 4))
    st = min(t, (3 * (2 * t - k - 2)) // 2 + 1); sh = min(t, -((-3 * (2 * t - k - 1)) // 2))
    is72 = find_bad_subfamily(E, n, 7) is None
    cnt['is72'] += is72
    for key, b in (('st', st), ('sh', sh), ('ctl', sh + 1)):
        if Smin < b:
            cnt[key + '_hit'] += 1
            if is72:
                cnt[key + '_fail'] += 1
                if key == 'ctl' and ctl_example is None:
                    ctl_example = (n, k, t, Smin, sh, [sorted(v for v in range(n) if e >> v & 1) for e in E])
                if key != 'ctl':
                    print('COUNTEREXAMPLE', key, n, k, t, Smin, b, E, flush=True)
print(cnt)
if ctl_example: print('negative-control (S = sharp) realised by a (7,2) family: n,k,t,Smin,sharp,edges =', ctl_example)
