"""w9 referee [core#3]: independent exhaustive check of the type logic used by L+ / L++.
Rows 1..4 = G1..G4, rows 5,6,7 = G5,G6,G7. Constraints produced by the recipes:
  (a) row 4+j avoids I(mu_j) = union of Gi&Gj over the pairs of matching mu_j   (j=1,2,3, any bijection)
  (b) G7 avoids G5&G6   (so no point lies in all of G5,G6,G7)
Nothing else (T-sets only serve to guarantee (a),(b) and pairwise lightness; lightness itself is NOT used by the logic).
Claim: no two allowed types (equal allowed) have union {1..7}  => the 7 edges have no transversal of size <= 2.
Also: dropping any single constraint creates a covering pair (so every avoid-request is needed)."""
import itertools
PAIRS = [frozenset(p) for p in itertools.combinations(range(1,5),2)]
MATCHINGS = [(frozenset({1,2}),frozenset({3,4})),(frozenset({1,3}),frozenset({2,4})),(frozenset({1,4}),frozenset({2,3}))]
FULL = frozenset(range(1,8))
def allowed(assign, drop=None):
    # assign: dict matching index -> row in {5,6,7}
    row = {}
    for mi,r in assign.items():
        for p in MATCHINGS[mi]: row[p] = r
    out = []
    for s in range(0,8):
        for T in itertools.combinations(range(1,8), s):
            T = frozenset(T); ok = True
            for p in PAIRS:
                if p <= T and row[p] in T and drop != ('pair', p): ok = False
            if {5,6,7} <= T and drop != 'triple': ok = False
            if ok: out.append(T)
    return out
def covering(types):
    return [(A,B) for A in types for B in types if A|B == FULL]
nbad = 0
for perm in itertools.permutations([5,6,7]):
    assign = dict(enumerate(perm))
    al = allowed(assign)
    c = covering(al)
    assert not c, (perm, c[:3])
    # necessity of each constraint
    for d in [('pair',p) for p in PAIRS] + ['triple']:
        assert covering(allowed(assign, d)), (perm, d)
    nbad += 1
print(f"type logic PASS for all {nbad} bijections; every one of the 7 constraints is individually necessary")
