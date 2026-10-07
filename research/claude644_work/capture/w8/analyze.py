import re, sys, itertools
from wtd_search import min_transversals
n = int(sys.argv[2])
fams = []
for line in open(sys.argv[1]):
    if line.startswith('#'):
        edges = re.findall(r"'([01]+)'", line)
        fams.append([sum(1<<i for i,c in enumerate(e) if c=='1') for e in edges])
def canon(edges):
    best = None
    for perm in itertools.permutations(range(n)):
        E = tuple(sorted(sum(1<<perm[i] for i in range(n) if e>>i&1) for e in edges))
        if best is None or E < best: best = E
    return best
seen = {}
for f in fams:
    c = canon(f)
    if c not in seen: seen[c] = f
print(len(fams), 'families,', len(seen), 'iso classes')
for c in seen:
    E = list(c)
    inter = lambda F: all(a & b for a in F for b in F)
    zs = [z for z in range(n) if inter([e for e in E if not e>>z&1])]
    tau = min(bin(J).count('1') for J in min_transversals(E, n))
    print([ ''.join(str(e>>i&1) for i in range(n)) for e in E], 'tau', tau, 'z with S-z intersecting:', zs)
