# A membership restriction on robust witnesses in intersecting families

Status: hand proof. This is a necessary condition for the witness branch of
`agent_critical_cover_witness_exchange.md`, not a selection theorem for a
single witness working for all prescribed vertices.

Let H be an intersecting family, let E be an actual edge, and fix distinct
points x in E and y outside E. Put Q=E\{x}, and assume Q is nonempty.
Suppose q actual edges F_1,...,F_q form a robust shortening witness:

    for every z in Q, the set {x,y,z} fails to meet some F_i.

For a point v, let t(v)={i:v belongs to F_i}, and put

    I_xy = [q] \ (t(x) union t(y)).

Then

    |I_xy| >= 2,
    |t(x) union t(y)| <= q-2.                         (1)

**Proof.** Robustness says precisely that

    Q intersect intersection_{i in I_xy} F_i = empty.

The index set cannot be empty, because then every triple {x,y,z} would
already meet all the rows using x,y. If I_xy={i}, then F_i avoids x, while
intersectingness gives F_i intersect E nonempty. Therefore F_i meets Q,
contradicting the displayed empty intersection. This proves (1). QED.

For q=6 and |t(x)|=4, equation (1) forces t(y) contained in t(x).
In the exact nineteen-type clean profile (four full K4 star types, three
cycle types and their twelve three-subtypes), a degree-four x belongs to
one cycle type. No other cycle or star is contained in this cycle.
Consequently y must belong to that same cycle class or one of its four
defect classes. This conclusion requires the full clean star types;
incidence-trimmed star classes may have additional contained subtypes.

For q=6 and |t(x)|=3, y can belong to at most one row outside t(x).
For q=5, the corresponding general restriction is
|t(x) union t(y)|<=3.

There is a trace-intersection refinement. If every subfamily of at most s
of the nonempty traces F_i intersect Q, i outside t(x), has nonempty common
intersection, then |I_xy|>=s+1. Indeed I_xy is a subfamily of those indices
whose traces have empty common intersection. Thus

    |t(x) union t(y)| <= q-s-1.                       (2)

Here one assumes s<=q-|t(x)|, or interprets the hypothesis literally; no
trace is asserted to be an actual edge of H.

Finally fix one degree-four, six-row robust witness in the critical-cover
normal form, with B=B_E meeting every F_i and avoiding E. This SAME witness
cannot be robust for every y in B. Choose a row F_j avoiding x and then
y in B intersect F_j. Such a y exists because F_j is an actual edge other
than E. Its type is not contained in t(x), so (1) fails. This does not
force the cover branch for that y: a different robust witness may certify
the failed augmentation. The freedom to change the witness is the precise
remaining obstruction to applying the fixed-witness restriction uniformly
over the critical cover B.
