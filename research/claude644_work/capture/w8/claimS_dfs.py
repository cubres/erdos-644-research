"""Independent (no SAT) exhaustive DFS over antichains on [n] with property (7,2) (hereditary), listing
iso classes of those with tau>=3 and no edge meeting all edges.  Standard library only."""
import sys, itertools, time
n = int(sys.argv[1]); P = 7
sets = sorted(range(1, 1<<n), key=lambda s: (bin(s).count('1'), s))
pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
perms = list(itertools.permutations(range(n)))
def relabel(e, pm): return sum(1<<pm[i] for i in range(n) if e>>i&1)
def canon(E): return min(tuple(sorted(relabel(e, pm) for e in E)) for pm in perms)
# cover mask: for each set, bitmask over pairs index of pairs hitting it
hit = {s: sum(1<<k for k,q in enumerate(pairs) if s & q) for s in sets}
FULL = (1<<len(pairs)) - 1
def ok_add(E, s):
    # (7,2) hereditary: check all subfamilies of size <= 6 of E together with s
    for r in range(0, min(P-1, len(E))+1):
        for sub in itertools.combinations(E, r):
            m = hit[s]
            for e in sub: m &= hit[e]
            if m == 0: return False
    return True
found = {}; count = 0; t0 = time.time()
def dfs(E, start):
    global count
    count += 1
    if len(E) >= 2:
        tau3 = all(any(not (e & q) for e in E) for q in pairs)
        if tau3 and all(any(not (e & f) for f in E) for e in E):
            c = canon(E)
            if c not in found: found[c] = list(E)
    for k in range(start, len(sets)):
        s = sets[k]
        if any((e & s) == e or (e & s) == s for e in E): continue
        if ok_add(E, s):
            E.append(s); dfs(E, k+1); E.pop()
dfs([], 0)
print('n', n, 'antichains with (7,2) visited', count, 'classes', len(found), round(time.time()-t0,1))
for c in found: print([''.join(str(e>>i&1) for i in range(n)) for e in c])
