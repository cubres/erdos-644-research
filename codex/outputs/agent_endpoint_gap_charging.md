# Endpoint-gap charging through actual private edges

Status: the cover-saving and actual-edge forcing statements below are hand
proved. They give a concrete conditional charging mechanism and a stronger
actual-edge oracle at the full size of a chosen cover. They do not prove
D<=2(|P|-t)+o(k). The missing control is identified as a system of actual
multi-point trace obstructions; no Hall or matroid exchange axiom is assumed.

## 1. Choose the transversal inside P more carefully

Fix the jointly minimizing six-tuple F_1,...,F_6, its endpoint transversal P,
and full repair supports W_i as in the main note. Write

    p=|P|,   d(v)=#{i:v in F_i},   q(v)=#{i:v in W_i},
    eta(v)=q(v)+2-d(v) for v in P.

Choose T among all transversals of H contained in P first to minimize its
cardinality, and then to minimize sum_{x in T} eta(x). Such a choice exists
because P itself is a transversal. Put

    ell=|T|>=t,   R=P\T,   sigma=ell-t>=0.

This is only a refinement in the choice of T. It makes no additional claim
about the six-tuple, and is compatible with either of the alternative
six-tuple normalizations discussed by the parent.

For x in T let

    E_x={E in H: E intersect T={x}}

be its full family of actual private edges. It is nonempty, by the
cardinality minimality of T. Every member E has

    E intersect P subset {x} union R.

One selected private witness for each x is insufficient for a collective
replacement test. The lemmas below use the entire actual family E_x.

## 2. A full-size weighted avoidance oracle

**Lemma 1.** Let S subset T and Y subset R. If either

    |Y|<|S|,

or

    |Y|=|S| and sum_{y in Y}eta(y)<sum_{x in S}eta(x),

then there is an actual edge E satisfying

    E intersect (T\S)=empty,   E intersect Y=empty,
    empty != E intersect T subset S.                         (1)

**Proof.** Otherwise (T\S) union Y would be a transversal contained in P.
It would have smaller cardinality than T in the first case, or equal
cardinality and smaller eta-weight in the second. Both contradict the
definition of T. Since T is a cover, the actual edge which it fails to meet
after the replacement has the asserted nonempty T-trace. QED.

The equal-cardinality case is useful: it authorizes an avoidance request
of size ell, whereas the ordinary transversal-number oracle only authorizes
arbitrary requests of size t-1. Its hypothesis is a strict improvement in
the actual cover potential, not an assumption that an arbitrary ell-set
can be avoided.

In particular, for x in T and y in R with eta(y)<eta(x), there is an actual
private edge in E_x which avoids y. This supplies a concrete exclusion
witness against every proposed lower-defect one-point replacement.

## 3. The exact residual obstruction after private edges have been covered

For Y subset R, define the set of unblocked retained points by

    S_Y={x in T: every E in E_x meets Y}.

Thus Y already covers every actual private edge of each x in S_Y. Define
a trace family on S_Y by

    M_Y={E intersect T:
          E in H, E intersect Y=empty,
          E intersect (T\S_Y)=empty}.

Every member of M_Y has size at least two: it is nonempty because T covers
H, and a singleton {x} would be a private edge of x missed by Y, contrary
to x in S_Y. These are traces of actual edges, used only to test whether
a proposed cover meets those edges. They are not declared to be actual
edges, and property (7,2) is not transferred to M_Y.

**Lemma 2 (collective cover-saving certificate).** If B subset S_Y meets
every member of M_Y, then

    (T\S_Y) union B union Y

is a transversal of H. Consequently

    |S_Y|-|B| <= |Y|.                                      (2)

If equality holds in (2), then also

    sum_{x in S_Y\B}eta(x) <= sum_{y in Y}eta(y).            (3)

**Proof.** An actual edge already meeting T\S_Y is covered. If it misses
that set but meets Y it is covered as well. Every remaining actual edge
has its T-trace in M_Y, which B meets. This proves the covering statement.
Inequality (2) follows from minimum cardinality of T among covers inside P.
In the equality case the new cover has the same cardinality, so its
eta-weight cannot be smaller; cancelling the unchanged vertices gives (3).
QED.

This is a usable finite certificate: it asks that Y cover all the relevant
actual private edges, and that B cover the remaining actual multi-point
traces. If |S_Y|-|B|>|Y|, it saves a cover point. If equality holds and the
eta-weight on the left of (3) is larger, it improves the secondary
potential. Either certificate contradicts the chosen T.

The missing condition cannot be reduced to covering the selected private
witnesses. Even after all private edges are met, actual edges whose T-trace
has two or more points can block a simultaneous replacement.

## 4. A precise Hall-type inequality and new actual pair-trace edges

The same statement has an exact independence form. Let alpha(M_Y) be the
largest size of a subset of S_Y containing no member of M_Y. Then

    alpha(M_Y)<=|Y|.                                     (4)

Indeed, if X subset S_Y is independent in M_Y, the set
(T\X) union Y is a cover: an edge missed by it would have a nonempty
T-trace contained in X and would give a member of M_Y there. A larger
independent X would save a point. Conversely any such replacement gives
an independent X. Thus (4) is the exact collective obstruction, not an
assumed ordinary bipartite matching condition.

Equivalently, every (|Y|+1)-subset X of S_Y contains the T-trace of an
actual edge avoiding Y. Such a trace has size between two and |Y|+1.

**Corollary 3 (actual pair completion).** For a single discarded endpoint
y in R, put S_y=S_{ {y} }. For every two distinct x,x' in S_y there is an
actual edge E_{x,x';y} with

    E_{x,x';y} intersect T={x,x'},   y not in E_{x,x';y}.    (5)

**Proof.** Otherwise {x,x'} would be independent in M_{ {y} }. Replacing
x,x' by y would give a smaller cover inside P. The actual obstruction trace
must have size two because singleton traces have already been excluded by
the definition of S_y. QED.

Thus a discarded point which individually replaces many retained points
forces an entire collection of actual pair-trace edges. This is a concrete
global constraint available for subsequent seven-edge arguments. Their
points outside T remain uncontrolled; the traces in (5) are not themselves
the actual edges.

There is also a weight restriction on the individual replacements:

    x in S_y  implies  eta(x)<=eta(y).                    (6)

Indeed (T\{x}) union {y} is then a cover of the same size. In particular,
a discarded endpoint of nonpositive eta-weight cannot individually replace
a retained endpoint of positive eta-weight in the chosen weighted minimum.
For every such unequal pair, Lemma 1 supplies an actual private edge
excluding the discarded point instead.

## 5. Where this could pay for the endpoint gap

The precise pointwise account is

    D-2(p-t)
      = sum_{x in T} eta(x)
        + sum_{y in R}(eta(y)-2)
        + sum_{v outside P}(q(v)-d(v))
        - 2 sigma.                                      (7)

This separates retained endpoint defects, the two units of capacity
available at each discarded endpoint, contributions outside P, and the
slack if the minimum cover inside P is larger than a global minimum cover.

Lemma 2 gives an actual mechanism for moving a retained defect contribution
to discarded endpoints: when its residual multi-point obstruction is met
by B and the exchange preserves cardinality, the eta-weight of the removed
retained points is at most the eta-weight of Y. If eta(y)<=2 on those
discarded recipients, this is a two-unit-per-recipient bound. Disjoint valid
exchanges could be summed without double counting their recipients.

No argument currently supplies enough such valid exchanges to pay for all
positive terms in (7). Three separate issues must not be omitted:

* a discarded set Y must meet all private edges of the proposed retained
  points, not merely one chosen witness per point;
* the actual higher-order obstruction family M_Y must admit the needed
  small hitting set B; by Corollary 3 it can contain all pair traces on S_y;
* positive contributions at vertices outside P, and any eta(y)>2 on R,
  need their own charge or cancellation against negative contributions.

These are concrete remaining conditions. The original two-point incidence
and repair counts do not establish them by themselves.

## 6. Relation to the alternate global minimum-cover choice

One can instead choose a global minimum cover T0 of size t maximizing its
intersection with P. Then, for y in P\T0 and z in T0\P, some actual edge
has T0-trace {z} and avoids y. Otherwise replacing z by y would preserve
cardinality and increase the intersection with P.

More generally, whenever S subset T0 and Y subset P\T0 have equal size
and S contains a point outside P, an actual edge avoids (T0\S) union Y.
This follows from the same maximum-intersection argument. The actual
edge's T0-trace is a nonempty subset of S.

This alternate choice supplies a useful full-size exchange oracle, but it
changes the accounting: if O=T0\P and R0=P\T0, then p-t=|R0|-|O|. The
outside selected points cannot be silently ignored when charging into R0.
The report therefore uses the cover contained in P for the direct defect
calculation (7).

## 7. Legitimate outside replacements in the zero-gap case

The restriction Y subset P\T in Sections 1-5 is substantive: T was chosen
to minimize cardinality only among covers contained in P. Such a minimum
does not justify arbitrary replacements by outside points.

If |T|=t, however, T is a global minimum cover. The cardinality statements
in Lemmas 1-2 and Corollary 3 then apply to any Y subset V\T. Define S_Y
using the same entire actual private-edge families, and define M_Y from
actual edges avoiding Y exactly as before. A replacement saving a point is
now impossible regardless of whether its new points lie in P.

**Corollary 4 (zero-gap outside charging).** If p=t, then T=P is a global
minimum cover. For every Y subset V\P, define S_Y from the full actual
private families relative to P. The cardinality-only conclusion of Lemma 2
and alpha(M_Y)<=|Y| remain valid; for singleton Y, actual pair completion
(5) remains valid as well. The eta-weight equality conclusion is not
asserted for these outside replacements.

In particular, when p=t one has T=P, and for any outside point y in V\P,

    S_y={x in P: every actual E with E intersect P={x} contains y}

has the following consequence: every two distinct x,x' in S_y force an
actual edge E with E intersect P={x,x'} and y not in E. This is a
nonvacuous row-generation rule even though P\T is empty. It directly
opposes a defense in which y is used in all the actual singleton-trace
responses of many retained endpoints.

The equal-cardinality eta-weight comparisons do not automatically extend
to these outside replacements. They would require a weight defined on the
whole ground set and a global minimum cover optimized for that weight.
Only the cardinality and actual-row forcing conclusions are asserted here.
Likewise, knowing that y belongs to one selected private witness for each
x does not put x in S_y; membership requires all actual private edges.

At positive endpoint gap, outside replacements can instead be based on a
true global minimum cover such as T0 in Section 6, with its changed
accounting, or on an explicit proof that the chosen cover inside P has
size t. Neither identification is made silently.

## 8. Current endpoint

The proved progress is a weighted, full-size avoidance oracle and a
collective cover-saving criterion, together with actual pair-trace edges
which must exist whenever private-edge replacements would otherwise save
a point. These add global constraints to a potential charging argument.

A complete proof still needs a defect-specific reason that enough of the
families M_Y have small hitting sets, or a seven-edge contradiction from
their forced actual multi-point trace edges. Neither has been derived here.
No bound on D-2(p-t) beyond the stated conditional mechanism is claimed.
