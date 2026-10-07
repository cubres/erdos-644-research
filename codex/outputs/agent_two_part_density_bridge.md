# Two-part density stability: completed continuous theorem [C]

Status: the explicit three-type construction and reduction below have hand
proofs. The final finite contradiction now has a standalone standard-library
rational checker, with eight positive capacity constructions and 2,744 rational
leaves. The theorem below is therefore computer-assisted [C]. It concerns the
continuous two-part model, not arbitrary families. A finite corollary is proved
below when a minimum cover has at least eleven vertices in each part; the
unrestricted finite pair-extendible case remains open here.

## Target and the first failed shortcut

For normalized rank one, write N=x+y. Suppose a closed trace set C has an
optimal free residual box using both parts, corresponding to a largest internal
gap g. Then

    t = tau* = N-1-g.

**Theorem [C].** Let C be a nonempty closed admissible trace set over two parts
of capacities x,y, with rank normalized to one. Let g be its largest internal
gap (zero if there are no gaps). Suppose its continuous transversal coefficient
satisfies t=N-1-g, so a mixed free residual box is optimal. If the family has
property (7,2) and t>2/3, then N+t<=5/2.

The exact relation to finite pair extendibility is proved below. Passing from
property (7,2) at one integer scale to the continuous property requires a
separate rounding argument; that passage is not silently assumed.

The complete two-type template menu does not suffice. A small exact linear
arithmetic search gives

    x=6747/20960, y=1957/1310,
    C={0,267/2096,271/1048},
    g=275/2096, t=14349/20960>2/3,
    N+t=6551/2620>5/2.

Every pair of these three traces passes all 42 two-type exclusions. This is not
a counterexample to the target: a tuple using all three types fails (7,2).
The following hand construction explains the failure directly.

## A three-type trimmed-Fano lemma, with explicit masses

Let a<=q<=c be three actual admissible traces. Assign the seven Fano row labels
the types a,q,q,q,q,c,c, putting the a row and the two c rows on a Fano line.
The seven complementary four-row cells form three symmetry classes:

* one cell consisting of the four q rows;
* two cells, each containing two q rows and both c rows;
* four cells, each containing the a row, two q rows, and one c row.

Put mass f in the first cell, mass b in each of the two cells, and mass d in
each of the four cells. The loads at the a,q,c rows are respectively

    4d, f+b+2d, 2b+2d,

and total mass is f+2b+4d.

In the first part choose

    d=a/4,
    b=c/2-a/4,
    f=max(0,q-c/2-a/4).

These are nonnegative, their row loads dominate a,q,c, and their total is

    A(a,q,c)=max(c+a/2, q+c/2+a/4).

In the second part choose

    d=(1-a)/4,
    b=max(0,(1+a-2c)/4),
    f=max(0,(1+a)/2-q-b).

These loads dominate 1-a,1-q,1-c. If b>0, the last displayed f is
(1+a+2c-4q)/4>=0 because q<=c<(1+a)/2. If b=0, its given maximum is used.
In the two cases the total is respectively 7/4-a/4-q-c/2 and
max(1-a,3/2-a/2-q). Thus in all cases it equals

    B(a,q,c)=max(1-a, 3/2-a/2-q, 7/4-a/4-q-c/2).

Consequently, if x>=A(a,q,c) and y>=B(a,q,c), there is a bad seven-tuple.
Indeed the masses fit in their respective parts; trim excess membership from
each individual row to obtain exactly its prescribed trace in each part.
Trimming replaces Fano-complement cells by subsets. Two such cells cannot cover
all seven row labels, so trimming preserves the obstruction. Unused capacity
lies outside every row. This construction is valid over reals, and over integer
scales after rational scaling.

For the displayed three-type candidate, take a=0, q=267/2096, c=271/1048.
Here A=c and B=31300/20960. The capacities are x=6747/20960>c and
y=31312/20960>B, so the failure is a hand-checked consequence of the formula.

## A precise interval-covering consequence

Let C be closed with largest internal gap g, and let delta=N-7/4>0. Suppose
g<2delta. Fix a,q,h in C such that

    a<=q<=h,
    h<=x-a/2,
    q>=3/2-y-a/2.

If

    7/2-2y-a/2-2q <= h,
    2x-a/2-2q >= q,

then the three-type construction gives a bad tuple, with some high trace c in
C intersected with [q,h]. To see this, consider the partner interval

    I=[7/2-2y-a/2-2q, 2x-a/2-2q].

It has length 2delta>g and meets [q,h]. If I contains either endpoint q or h,
it already contains an actual trace in [q,h]. Otherwise it lies inside (q,h)
and cannot avoid C, because its length exceeds the largest gap. Choose c in
the intersection. The endpoint conditions imply c+a/2<=x and
3/2-a/2-q<=y; membership in I gives both remaining total-mass inequalities.
The condition 1-a<=y follows from admissibility. The lemma applies.

Equivalently, whenever a,h in C satisfy a<=h<=x-a/2, the absence of a bad tuple
forces C to miss the middle-trace interval

    [max(a,3/2-y-a/2,(7/2-2y-a/2-h)/2),
     min(h,(2x-a/2)/3)].

This is a concrete interval propagation rule, not an informal assertion that
the type set behaves convexly.

## Reduction to four actual types

Suppose toward the density target that t>2/3 and N+t>5/2. Let l=min C and
c=max C. Mixed optimality gives

    y<=1-l+g if l>0,
    x<=c+g if c<1.

Also g<=c-l. Since N+t=2N-1-g>5/2, we have delta>g/2>=0.

The homogeneous Fano forbidden interval is

    H=[1-4y/7,4x/7].

There must be actual types on both sides. If all are above H, then l>0 and
x<7l/4. Consequently

    N+t=2(x+y)-1-g < 1+3l/2+g
        <=1+l/2+c <=5/2,

a contradiction. If all are below H, then c<1 and y<7(1-c)/4, giving

    N+t < 5/2-3c/2+g <=5/2-c/2-l <=5/2,

again a contradiction.

By compactness choose consecutive types a,b straddling H. They obey

    l<=a<b<=c,
    a<1-4y/7, b>4x/7,
    b-a<=g.

These four actual values l,a,b,c, the two endpoint cover conditions, the density
violation, and exclusion of a small number of two- and three-type constructions
already form an inconsistent QF_LRA system in discovery. No discretization of C
or assumption that it has only four elements was made.

## The completed compact finite argument [C]

`agent_kernel_gap_core.json` records the initial 23-assertion discovery core.
The completed certificate reconstructs these conditions independently, adding
only elementary valid bounds. The substantive conditions consist of:

* nine feasibility/order/central-gap conditions;
* the two endpoint cover bounds;
* t>2/3 and N+t>5/2;
* the existing two-type functions M0,M2,M5,M6,M7,M8,M9 at (a,b), and M1 at (l,b);
* the new triple (l,a,c), and the part-reflected new triple (l,b,c).

The stronger one-versus-six span inequality is unnecessary.

To express strict inequalities using closed rational polyhedra, introduce a
common gamma>0. Each strict positive quantity is required to be at least gamma.
This is valid because a hypothetical counterexample has only finitely many
strict conditions and construction exclusions under consideration: choose one
positive excess in each exclusion and then a sufficiently small common gamma.
We can assume gamma<=1. All eight variables (x,y,l,c,a,b,g,gamma) are treated as
free in the rational linear-combination checks; every sign or upper bound used
is an explicit row.

Each no-construction assertion is a disjunction of rational linear inequalities.
The two endpoint-cover assertions are also disjunctions, with an equality as one
alternative. A finite branching tree splits these disjunctions. Every split
contains every alternative exactly once; leaves may close before all remaining
disjunctions are split, since inconsistency then already follows. There are
3,258 nodes and 2,744 leaves.

At a leaf write the selected system as Av<=b. The certificate supplies sparse
rational multipliers z_i<0. Either

    z^T A=0 and z^T b>0,

contradicting feasibility, or

    z^T A=-e_gamma^T and z^T b>=0,

forcing gamma<=0. All equalities and inequalities are checked with Python
`fractions.Fraction`. The 2,744 leaves use 18,442 nonzero multipliers in total.

The eight construction records are positive witnesses only. For each listed
capacity function M(s,t), its fixed bad parent support and coloring are checked.
At the coordinate rays and every corner ray of M, explicit nonnegative parent
masses meet all seven row demands and have total M(s,t). Between consecutive
rays the same linear form maximizes M at both endpoints; convex combination
therefore gives a realization of the asserted cost throughout that cone.
Trimming preserves the bad support. This verifies sufficiency of the eight
constructions without checking, assuming, or importing completeness of the
42-function catalogue. The three-type construction has the hand proof above.

The following fresh replay completed successfully using only the standard
library, without SciPy, Z3, or imports from the old catalogue checker:

    python3 -B -S p644_agent_audit_density_check.py

Output:

    PASS: 8 positive two-type constructions;
    {'nodes': 3258, 'leaves': 2744, 'multipliers': 18442};
    every Boolean branch closed by exact rational arithmetic.

The checker and producer are in the research directory:
`p644_agent_audit_density_check.py` and `p644_agent_audit_density_discover.py`.
The only data inputs to replay are
`logs/astra_agent_audit_density/positive_templates.json` and
`logs/astra_agent_audit_density/branch_certificate.json`.
Discovery uses SciPy to propose duals; replay verifies their exact identities
and does not trust the numerical solver. This completes the continuous theorem.

## The exact finite consequence of pair extendibility

Let an integer k-uniform two-part type-closed family have nonempty parts of
sizes n1,n2. Let its allowed integer first-part traces be C. Suppose a minimum
transversal meets both parts; pair extendibility implies this by taking one
vertex from each part.

Let u,v be the two residual sizes after deleting that minimum transversal.
Because at least one vertex was deleted from each part, increasing either u or
v by one is possible. Minimality of the cover implies that each such increase
creates an allowed edge. Increasing u forces c=u+1 to be an allowed trace;
increasing v forces d=k-v-1 to be allowed. They are distinct and consecutive:
the interval [d+1,c-1] contains no allowed trace, since the original residual box
was free. This includes the empty interval case c=d+1. Consequently

    u+v=k+(c-d)-2,
    tau=n1+n2-k-(c-d)+2.

Every other internal gap with endpoints d',c' gives a feasible free residual
box (c'-1,k-d'-1). Optimality therefore forces c-d to be the largest gap G, and

    tau=n1+n2-k-G+2.

In particular there must be at least two allowed types. This treats ties and
even minimum covers with only one selected vertex in one of the parts; no
positive proportional lower bound on both cover counts was used.

For the continuous model obtained from these same capacities and trace values,
the mixed value n1+n2-k-G is optimal. An active one-part cover costs one more
than its continuous coefficient in the finite model, whereas the mixed cover
costs two more; hence finite optimality of the mixed cover implies continuous
optimality as well. Nevertheless a continuous bad tuple can have nonintegral
cell sizes. The theorem above therefore does not by itself assert a uniform
finite density bound without addressing that rounding issue.

## A finite balanced-cover corollary, and the remaining boundary case

**Finite corollary [C].** Let H be a k-uniform two-part type-closed (7,2) family
on n vertices, with transversal number t. Suppose some minimum transversal has
at least eleven vertices in each part. If t>2k/3+22, then

    n+t <= 5k/2+42.

**Proof.** Delete ten points of that fixed minimum transversal from each part.
The residual family H' has transversal number exactly t-20: adjoining the
deleted points proves the lower bound, while the remainder of the same minimum
transversal proves the upper bound. This remainder still meets both parts.
The finite identity just proved therefore shows that the continuous coefficient
of H' is exactly t-22, with a mixed residual box optimal. Its remaining ground
size is n-20.

If n+t>5k/2+42, this continuous family violates the density theorem, since

    (n-20)+(t-22)>5k/2 and t-22>2k/3.

The resulting bad tuple uses the homogeneous Fano support, one of the eight
positive supports in the certificate, or the new three-type Fano support. Each
has at most eleven parent cells in a part: the only non-Fano supports have
eleven, and all the Fano supports have seven. Round each nonzero parent mass up
to an integer. Since the original remaining capacity is integral, this uses
at most ten extra points per part and hence fits in the original parts. Every
row's two loads now dominate its prescribed integer trace. Trim each row's
membership until its two loads are exact. The cells remain subsets of the bad
parent cells, and each row now has an original allowed trace. This contradicts
the finite (7,2) property and proves the corollary.

Pair extendibility by itself does not supply the balanced minimum transversal
used in this corollary. Nor can mixed optimality after arbitrary deletion be
recovered with only a bounded additive error. The following exact family is
an obstruction to both shortcuts.

For m>=3, let k=100m, give the parts sizes 5m+2 and 169m, and allow only traces
0 and 5m. The total ground size is 174m+2<7k/4, so property (7,2) follows from
the elementary complete-family bound. Directly,

    t=min((3)+(69m+1),74m+1)=69m+4>2k/3.

Every minimum cover has exactly three points in the first part and 69m+1 in
the second. Any pair extends to such a cover, but no minimum cover has eleven
points in the first part.

Deleting thirteen vertices from each part removes the 5m trace altogether.
The remaining family is the complete k-uniform family on the second part,
with 5m-11 unused vertices left in the first part. Its true continuous
transversal coefficient is 69m-13. The mixed expression using its now-zero
internal gap is 74m-24. Their difference is

    5m-11,

which grows linearly. This example does not violate the desired finite density
bound; it pinpoints why the standard deletion proof does not establish it.
The remaining case is a family whose minimum mixed covers always use at most
ten vertices in one of the two parts. An additional boundary argument, or
rounding that handles a nearly saturated part, is needed. No finite theorem
for all pair-extendible families is asserted here.

### A small cover in one part does not force a small trace endpoint

A further proposed shortcut would infer that the lower endpoint of the optimal
gap is O(1), or that some actual extremal type is near 0 or k. This is false
even with property (7,2), pair extendibility, and transversal density strictly
above 2/3.

For m>=2 let k=100m, give the parts sizes 80m+1 and 94m, and allow every integer
trace from 6m through 76m, together with 80m. All these traces are feasible. The
ground size is 174m+1<7k/4, so the complete-family bound proves (7,2).
The unique largest gap is (76m,80m), of length 4m. The three possible optimal
cover costs are

    first part only:  (80m+1)-6m+1 = 74m+2,
    second part only: 94m-100m+80m+1 = 74m+1,
    largest gap:      174m+1-100m-4m+2 = 70m+3.

Thus t=70m+3. Every minimum cover selects exactly two points of the first part
and 70m+1 of the second, so every pair extends to a minimum cover. However, the
lower endpoint of the optimal gap is 76m, the smallest allowed trace is 6m,
and the largest is 80m. None tends to 0 or k in absolute distance as k grows.
The excess of t above 2k/3 is also linear.

This family has n+t=244m+4<5k/2; it is an obstruction to the shortcut, not to
the desired density inequality. Any boundary proof must use the alleged
density violation itself or preserve the full geometry of the trace set.

## The step that fails without type closure

The mass construction is the precise use of symmetry. From the existence of
three actual edge profiles a,q,c, type closure permits making seven new edges
with those profiles and with the specific Fano incidence masses above. It
allows arbitrary exchanges inside each part, independently for each row, and
permits trimming surplus membership while retaining the prescribed profile.
Neither property follows from the mere existence of three edges of those
sizes in an arbitrary family.

A partition-free substitute would therefore have to prove an exchange or
realizability statement: high transversal number plus the critical normal form
must produce seven actual edges whose local incidence pattern realizes the
three-profile construction, or else give a cover at the desired cost. Pair
extendibility alone supplies minimum covers, not this exchange freedom.
Incidence-critical witnesses may supply the missing exchanges, but no such
lemma has been proved here. Simply assigning two parts to arbitrary edges and
running the continuous mass construction would be invalid.
