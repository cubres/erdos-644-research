"""Enumerate arc colourings of the 7 Fano lines by h classes (each class an arc: no 3 concurrent lines),
all classes used; report, per colouring (up to Fano automorphism + class renaming), the multiset of point
patterns (sorted class letters of the three lines through each point) and the 'pair-point' conditions XXY."""
import itertools, sys
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as H
h = int(sys.argv[1]) if len(sys.argv) > 1 else 4
LINES = H.LINES; PENCIL = H.PENCIL
letters = 'ABCDEFG'[:h]
seen = set(); out = {}
for col in itertools.product(range(h), repeat=7):
    if len(set(col)) < h: continue
    # arc condition
    if any(len(set(col[l] for l in PENCIL[q])) < 3 and any(sum(1 for l in PENCIL[q] if col[l] == c) == 3 for c in range(h)) for q in range(7)): continue
    # canonical form under automorphisms x class renaming
    key = None
    for lp in LPERMS if False else H.LPERMS:
        nc = [None]*7
        for i in range(7): nc[lp[i]] = col[i]
        # rename classes by first appearance
        ren = {}; c2 = []
        for c in nc:
            if c not in ren: ren[c] = len(ren)
            c2.append(ren[c])
        t = tuple(c2)
        if key is None or t < key: key = t
    if key in seen: continue
    seen.add(key)
    sizes = tuple(sorted((key.count(c) for c in range(h)), reverse=True))
    pats = []
    for q in range(7):
        pats.append(''.join(sorted(letters[key[l]] for l in PENCIL[q])))
    pats = tuple(sorted(pats))
    out.setdefault(sizes, []).append((key, pats))
for sizes in sorted(out, reverse=True):
    print("class sizes", sizes, "colourings", len(out[sizes]))
    for key, pats in out[sizes]:
        pairpts = [p for p in pats if p[0] == p[1] or p[1] == p[2]]
        print("   ", ''.join(letters[c] for c in key), " patterns:", ' '.join(pats), " | pair-points:", ' '.join(pairpts))
