"""Referee w9 core#2: exact check of the combinatorial core of Theorem L.
Setting: G1..G7 arbitrary sets (repeats allowed).  Constraints used by the proof:
  (C5) G5 & I5 = 0, (C6) G6 & I6 = 0, (C7) G7 & I7 = 0, (C567) G5&G6&G7 = 0,
  where I(mu) = (Gi&Gj)|(Gk&Gl) for the 3 perfect matchings of [4] assigned to rows 5,6,7 (any bijection).
Claim: then {G1..G7} has no transversal of size <= 2.
Check 1 (universal model): a point is determined by its type T = {i : x in Gi}; the constraints are exactly
  'T is allowed'.  Taking one point of every allowed type gives the universal instance; any instance is a
  sub-instance (its type set is a subset of allowed types), and a 2-transversal of a sub-instance is a pair of
  allowed types with union [7] (or one type = [7]).  So: check no allowed type pair covers [7], for all 6
  bijections matchings->rows.
Check 2 (necessity): dropping any one constraint yields a covering pair (so all four are used).
Check 3 (arithmetic chain): for lam>=1, t>=3lam+1: 2lam<=t-1, 2lam+1<=t-1, 3lam<=t-1; and lam=0 fails 2lam+1<=3lam."""
import itertools
M = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
def allowed(T, rowof, drop=None):
    # T subset of range(7); rowof[m] = row index (4,5,6) of matching m
    for m, ((a,b),(c,d)) in enumerate(M):
        r = rowof[m]
        if drop == r: continue
        if r in T and ((a in T and b in T) or (c in T and d in T)): return False
    if drop != 'triple' and {4,5,6} <= T: return False
    return True
full = set(range(7))
types = [set(c) for s in range(8) for c in itertools.combinations(range(7), s)]
ok = True
for perm in itertools.permutations([4,5,6]):
    A = [T for T in types if allowed(T, perm)]
    cov = [(S,T) for S in A for T in A if S | T == full]
    if cov: ok = False; print("FAIL", perm, cov[:3])
    for drop in [4,5,6,'triple']:
        A2 = [T for T in types if allowed(T, perm, drop)]
        cov2 = [(S,T) for S in A2 for T in A2 if S | T == full]
        if not cov2: ok = False; print("constraint not necessary", perm, drop)
print("universal-model check:", "PASS" if ok else "FAIL", "(6 bijections; each of the 4 constraints necessary)")
# arithmetic chain
bad = [(lam,t) for lam in range(0,200) for t in range(3*lam+1, 3*lam+50)
       if not (2*lam <= t-1 and (2*lam+1 <= t-1) and 3*lam <= t-1 and (lam == 0 or 2*lam+1 <= 3*lam))]
print("arithmetic chain lam in [1,200):", "PASS" if all(l == 0 for l,_ in bad) else "FAIL",
      "| lam=0: 2lam+1<=3lam fails (as expected) -> lam>=1 needed only there")
# Check 4 (referee refinement, 'case A'): if no point lies in >=3 of G1..G4, constraint C567 is unnecessary:
# allowed types = C5,C6,C7 only and |T & [4]| <= 2.  Then no covering pair => request budget 2lam suffices (G6=G5 ok).
okA = True
for perm in itertools.permutations([4,5,6]):
    A = [T for T in types if allowed(T, perm, 'triple') and len(T & {0,1,2,3}) <= 2]
    if any(S | T == full for S in A for T in A): okA = False
print("case-A (no triple point among G1..G4, no C567) check:", "PASS" if okA else "FAIL")
# Check 5: dangerous set for C567 in general: a type S+{5,6,7} (S subset [4]) is in a covering pair iff |S|<=1 and
# the partner type [4]-S (or [4]) is allowed; list them.
for perm in [(4,5,6)]:
    A = [T for T in types if allowed(T, perm, 'triple')]
    dang = sorted(tuple(sorted(T)) for T in A if {4,5,6} <= T and any(T | U == full for U in A))
    print("dangerous {5,6,7}-types (0-based rows 4,5,6):", dang)
