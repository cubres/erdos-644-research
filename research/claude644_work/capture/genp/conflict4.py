"""Conflict digraphs for h classes with ONE rigid representative per class (arc-CSP as in heavyparts, generalised).
Edge X->Y ("X blocks Y"): the Y-representative's X-trace exceeds 2e_X, so the point pattern XXY is infeasible at X.
Ignoring mixed-point and total conditions, a Fano colouring (each class an arc, classes may be unused) is feasible iff
none of its pair points XXY has X->Y.  We list the MINIMAL digraphs that block every colouring (h = 3, 4, 5)."""
import itertools, sys
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as H
PENCIL = H.PENCIL
def colourings(h):
    out = []
    for col in itertools.product(range(h), repeat=7):
        ok = True
        for q in range(7):
            cs = [col[l] for l in PENCIL[q]]
            if len(set(cs)) == 1: ok = False; break
        if ok: out.append(col)
    return out
def pairpoints(col):
    pp = set()
    for q in range(7):
        cs = [col[l] for l in PENCIL[q]]
        for c in set(cs):
            if cs.count(c) == 2:
                y = [d for d in cs if d != c][0]; pp.add((c, y))
    return pp
for h in [3, 4, 5]:
    cols = colourings(h)
    PP = [pairpoints(c) for c in cols]
    arcs = [(x, y) for x in range(h) for y in range(h) if x != y]
    blocking = []
    for mask in range(1 << len(arcs)):
        D = {arcs[i] for i in range(len(arcs)) if mask >> i & 1}
        if all(pp & D for pp in PP): blocking.append(frozenset(D))
    minimal = [D for D in blocking if not any(E < D for E in blocking)]
    # classify up to class permutation
    reps = {}
    for D in minimal:
        key = min(tuple(sorted((pi[x], pi[y]) for x, y in D)) for pi in itertools.permutations(range(h)))
        reps.setdefault(key, 0); reps[key] += 1
    print("h =", h, "colourings", len(cols), "minimal blocking digraphs", len(minimal), "up to symmetry", len(reps))
    for key in sorted(reps, key=len):
        print("   ", ' '.join(f"{'ABCDE'[x]}>{'ABCDE'[y]}" for x, y in key), " (x%d)" % reps[key])
