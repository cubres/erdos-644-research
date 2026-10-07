# One-response closure by a union of exact forbidden boxes

26 September 2026. Hand reduction and exact discovery routine. This does not
resolve all three-part families or the general three-quarter conjecture.

Let C be a closed set of admissible unit profiles on parts of capacities x.
For actual anchors d,a,b in C, the V4 construction (four d-rows, one a-row,
one b-row, and one proposed u-row) is feasible precisely when u is admissible
and is bounded coordinatewise by

    L_i(d,a,b) = min(x_i, 2x_i-a_i-b_i,
                    2x_i-2d_i-b_i, 4x_i-4d_i-a_i-b_i).

Indeed these are exactly the three nontrivial V4 capacity inequalities,
together with the individual row bound. The resulting seven-edge support
has no covering pair. Thus a (7,2) family containing the anchors contains no
unit profile in any of these closed boxes. A box with a negative coordinate
or total capacity below one can be discarded.

**One-request lemma.** Let B be any finite collection of these forbidden
boxes, constructed from actual anchors. If a residual box [0,u] has its
entire rank-one slice contained in their union, then

    tau*(C) <= sum_i(x_i-u_i).

Proof. Every admissible profile has total mass one. Containment says that
any profile of C below u would complete a bad seven-tuple with some six
anchor rows, contradicting (7,2). Thus u is free. This is the defining
upper bound for tau*. The hypothesis only involves actual anchors; it
does not assert that the convex hull of C is admissible. QED.

## Exact complement calculation

The complement of a union of downward boxes is an upward-closed set. Start
with the orthant of all nonnegative vectors. To remove a box with top L,
split each still-intersecting orthant according to the alternatives

    u_i > L_i.

Keep the resulting lower endpoints and their strictness flags. Drop any
orthant outside the capacity box, or whose lower coordinates sum to at
least one and include a strict inequality. Remove contained orthants.
Every operation preserves the exact remaining rank-one slice. In
particular positive lower endpoints retain strict flags even on equality
boundaries; an arbitrary small numerical tolerance is not used.

If a retained box has total capacity at least one, it intersects an
escaped orthant exactly when its top satisfies every lower constraint of
that orthant. To see this, interpolate between a point arbitrarily close
to the lower endpoint (whose total is below one) and the retained top.
All strict lower inequalities can be preserved, and the sum reaches one.
Hence the endpoint arrangement is sufficient to optimize a request.
For an infimum that cuts at a non-strict positive lower endpoint, reduce
that retained coordinate by an arbitrarily small amount. A non-strict zero
endpoint cannot be excluded in that way and must be treated separately.

The standard-library script

    work/paper_push/three_cert/v4_escape_boxes.py

implements this reduction with Fraction arithmetic. In three parts it
enumerates retained levels in two coordinates and determines the largest
valid third level directly. It is a terminal-rule generator; the V4 hand
lemma and the box-containment proof above supply its mathematical meaning.

## Exact diagnostics and their limits

For x=(106,106,112)/140 and anchors (71,69,0)/140,(65,0,75)/140, the routine
returns retained box (4,106,112)/140 and request cost 51/70. This matches
the two-anchor hand theorem exactly. Its closed box is free, so this
application needs no limiting epsilon.

The focused search's nine-profile parent-region witness at
x=(3/4,3/4,4/5) generates 23 maximal forbidden boxes and five escaped
orthants. The resulting single-coordinate request costs approximately
0.55619732424. But that witness is already inconsistent with (7,2): using
zero-based row indices from `balanced_point_optimal20.diagnostic.json`,
the V4 tuple (d,a,b,c)=(1,0,7,2) satisfies all capacity inequalities.
Thus this is an example of a branch point that can be closed by the
existing support menu, not a new obstruction or a counterexample. The
original search stopped on a time limit and had not established this
witness as surviving every template. No full point or neighborhood
theorem follows merely from closing this one witness.

The methodological gain is a direct way to design a request around all
its possible answers. Maximizing the separation from already revealed
profiles is useful for obtaining a new profile, but does not by itself
choose a request that forces a contradiction soon.
