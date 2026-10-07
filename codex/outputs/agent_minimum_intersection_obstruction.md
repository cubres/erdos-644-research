# A counterexample to the minimum-intersection dichotomy [C]

The proposed implication

    tau>2k/3+O(1)  ==>  minimum pair intersection >= tau/3-O(1)

is false, including for intersecting families in which every pair of vertices
extends to a minimum transversal.

For any integer m>=1, let k=200m, and take parts A,B of sizes 14m and 339m.
Include all k-subsets of B and all k-sets with exactly 10m points of A and
190m points of B.

## Property (7,2): elementary proof

Suppose seven edges form a bad tuple, repeating edges if the tuple has fewer
than seven members. Let j be the number of mixed edges. Their complements
inside B have sizes 149m, while the B-only edges have complements of size
139m. These seven complements must cover every pair of points of B.

Every point of B belongs to at least three of the seven complements. Indeed,
if it belonged to at most two, those at most two blocks would have to cover
all of B, but their total size is at most 298m<339m. Counting incidences gives

    (7-j)139m+j149m >= 3(339m),

so j>=5. The complements inside A of mixed edges have size 4m. Consequently,
if a point of B belongs to all B-only edges, the mixed-row complement blocks
containing it must cover A, requiring at least four such blocks.

For j=5, the two B-only edges have intersection of size at least 61m. Hence
the total complement incidence on B is at least 3(339m)+61m=1078m, whereas
the available total is 1023m. For j=6, the single B-only edge supplies 200m
such points, giving at least 1217m incidences against an available 1033m.
For j=7 every B-point requires at least four incidences, again impossible.
Thus no bad tuple exists. This proof removes the catalogue dependency below.

## Independent earlier computer check [C]

For the unscaled integer units (rank 200, parts 14 and 339, traces 0 and 10),
every one of the 42 certified two-type capacity functions M satisfies

    M(0,10)>14 or M(200,190)>339.

Exact rational arithmetic checks these 42 exclusions; the smallest value of
max(M(0,10)-14, M(200,190)-339) is 1. Thus the previously certified complete
capacity criterion (Theorem 7.69) excludes every continuous bad seven-tuple.
In particular, the family has (7,2) at every integer scale m. This conclusion
depends on that existing completeness theorem; no large catalogue replay was
performed for this bounded counterexample test.

The exact check is `p644_agent_audit_minintersection_counter.py`. Its output
lists all 42 rational capacity values and is saved as
`outputs/agent_minimum_intersection_counter.json`.

## Transversal number (hand calculation)

A cover must delete at least 139m+1 points from B to eliminate B-only edges.
It must additionally eliminate the mixed type, either by deleting at least
4m+1 points from A, or by raising the B deletion count to 149m+1. Therefore

    tau=min((139m+1)+(4m+1),149m+1)=143m+2.

Every choice of 4m+1 points of A and 139m+1 points of B is a minimum cover.
Both counts are at least two, so every pair of vertices extends to such a
cover. In particular, any vertex identification lowers tau by one.

## Minimum pair intersection (hand calculation)

For two row types a,b in a part of capacity x, their least possible
intersection is max(0,a+b-x). The choices in the two parts are independent.
Thus the three possible minima here are

    low-low:   2(200m)-339m = 61m,
    low-high:  (200m+190m)-339m = 51m,
    high-high: (20m-14m)+(380m-339m) = 47m.

All bounds are attained by choosing the two sets to cover each part whenever
their two sizes exceed its capacity. Hence mu=47m>0, so the whole family is
intersecting. But

    tau-3mu=2m+2,
    tau-2k/3=(29/3)m+2.

Both gaps grow linearly. No bounded additive term can repair the proposed
dichotomy.

This does not disprove a stronger statement restricted to the full
incidence-minimal and edge-critical normal form: thinning this family while
preserving tau may increase its minimum pair intersection. It does show that
local (7,2), high transversal number, and pair extendibility alone do not give
the required minimum-intersection lower bound.
