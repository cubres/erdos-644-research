"""Exhaustive logic check of the TETRAHEDRAL dual-pencil lemma (note Lemma 7.70 support, lazy form).
Rows 0..3 = G1..G4 (A), rows 4,5,6 = B-rows for the three matchings (in a given order).
Allowed types: T with |T & A| <= 3 (no point in all four A-rows); if pair {i,j} subset T&A then the B-row of
matching(ij) not in T; if |T&A| >= 1 then T does not contain all three B-rows.  (|T&A|=3 => no B at all follows.)
Claim: no two allowed types cover [7].  Lazy consequence: G1..G4 with empty common intersection, G5 avoids I5,
G6 avoids I6, G7 avoids I7 u (G5 & G6 & (G1u..uG4))  =>  no 2-transversal."""
import itertools
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
for order in itertools.permutations(range(3)):
    rowof={}
    for j,mi in enumerate(order):
        for pr in MATCH[mi]: rowof[frozenset(pr)]=4+j
    allowed=[]
    for T in range(128):
        S=[i for i in range(4) if T>>i&1]
        if len(S)==4: continue
        if any(T>>rowof[frozenset(p)]&1 for p in itertools.combinations(S,2)): continue
        if S and (T>>4&1) and (T>>5&1) and (T>>6&1): continue
        allowed.append(T)
    assert not any(a|b==127 for a in allowed for b in allowed)
    assert 0b1110000 in allowed      # B-core cell allowed (difference from Lemma Q)
print("Lemma T logic PASS (all 6 orders): tetrahedral allowed types pairwise non-covering; B-core {5,6,7} allowed")
