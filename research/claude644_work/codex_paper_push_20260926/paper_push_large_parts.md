# A dimension-free three-quarter theorem when every part is large

26 September 2026. Status: hand proof. This extends the new three-class
selection theorem to an arbitrary number of parts. The first statement
is in the continuous type model. A finite theorem with a uniform
additive constant is proved at the end.

Update: `paper_push_three_theory.md` now proves the stronger continuous
theorem with every x_i>=6/7. The four-class obstruction at x_i>=1 remains
useful for the sharper finite constant 30. The final section below proves
a uniform finite version of the stronger 6/7-capacity theorem, with
constant 84.

Let x=(x_1,...,x_p), let every x_i>=1, and let C be a nonempty closed
subset of {a:0<=a<=x, sum a_i=1}. Define tau*(C) by the usual free-box
formula. A bad tuple is a realization of seven types of C, allowing
repetition, with no two-point transversal.

**Theorem. If C has no bad tuple, then tau*(C)<=3/4.**

Neither convexity nor a bound on the number of types or parts is needed.
In physical units the hypothesis says that every part has size at least
the edge size. The coefficient is sharp already for one part: take the
complete family and let its ambient size tend to 7/4 from below.

## A four-class obstruction

Call a type a super-heavy at coordinate i when a_i>2x_i/3. Every such
type has a_i>2/3, so it is super-heavy at only one coordinate and the sum
of all its other coordinates is less than 1/3.

Suppose four distinct coordinates support super-heavy types. Choose one
such type a^i for each of these coordinates, i=1,2,3,4. Write

    s_i=a^i_i,       e_i=x_i-s_i.

No minimizing property is needed. Choose an index D whose e_i is smallest,
and call the other three A,B,C. Label the seven *rows* by the points of
a Fano plane. Put type a^D at a central point; put two copies of a^A on
the two other points of one line through that point, two copies of a^B
on a second such pair, and two copies of a^C on the last pair.

We verify the Fano capacity criterion in every physical coordinate:
every row load is at most x_j, every Fano line's three-row load is at
most 2x_j, and the total seven-row load is at most 4x_j. This criterion
is precisely the Fano parent-capacity lemma already proved in the main
note (and is invariant under Fano point-line duality).

For a doubled coordinate i in {A,B,C}, the only line containing both
own-heavy rows contains the central D-row. Since x_D>=1,

    a^D_i <= 1-s_D = 1-x_D+e_D <= e_D <= e_i.

Its three-row load is therefore at most 2s_i+e_i<=2x_i. Every other line
contains at most one own-heavy row, giving load at most x_i+2/3<=2x_i;
a line with none has load less than 1<=2x_i. The seven-row total is
less than 2x_i+5/3<=4x_i.

At the singleton coordinate D, line loads are at most x_D+2/3<=2x_D
and the total is less than x_D+2<=4x_D. At any coordinate outside these
four, all selected row loads are less than 1/3. Line loads are less than
1<=2x_j and the total is less than 7/3<=4x_j. All individual row loads
are at most capacity by admissibility. Thus the criterion holds in
every coordinate and produces a bad tuple.

We have proved the stronger structural fact:

**If all x_i>=1 and C has no bad tuple, then at most three coordinates
ever support a super-heavy type.**

This fact does not require tau*(C)>3/4 or closedness.

## Completion using the three-class selection theorem

Suppose tau*(C)>3/4 and there is no bad tuple. The hand pencil lemma
implies that every type is super-heavy somewhere. If at most two
coordinates support such types, Claude's hand Theorem L+ gives a bad
tuple. The four-class obstruction reduces the remaining case to exactly
three super-heavy coordinates.

Apply the three-class hand theorem in `paper_push_three_theory.md`.
For completeness, its extension to extra coordinates is justified here.
Choose minimum-heavy types in the three nonempty super-heavy classes,
with diagonal entries s_i and slacks e_i=x_i-s_i. Such minima are attained:
a limiting type that lost its unique heavy coordinate would be light
everywhere and supply a pencil tuple. Blocking the three classes by
retaining just below s_i in their own coordinates and all points elsewhere
gives E=sum e_i>=tau*(C)>3/4.

The three-coordinate proof requires only x_i>=6/7 in these three
coordinates, diagonal super-heaviness, off-diagonal bounds <=3/7,
and the upper bound

    sum of the six cross entries <= 3-s_1-s_2-s_3.

All hold here. The former equality may become an inequality because
some mass is in extra coordinates; its direction strengthens the
quad-selection argument. The three-class proof therefore chooses either
V(a,b), with five a-rows and two b-rows, or T(a;b,b;c), with four a-rows,
two b-rows and one c-row, satisfying every capacity condition in the
three super-heavy coordinates.

In every extra coordinate all selected entries are at most 3/7.
For V the additional inequalities follow from

    a_j+b_j <= 6/7 <= x_j,
    5a_j/4+b_j/2 <= 3/4 <= x_j.

For T each three-row line load is at most 9/7<=2x_j and the total is
at most 3<=4x_j. Thus extra coordinates impose no obstruction. The
selected tuple is bad in the full p-part space, a contradiction. QED.

## Verification and scope

The root derived the four-class Fano coloring; the three-selection agent
independently checked its line and total bounds and the extension to
extra coordinates. The root independently checked every inequality of
the three-class selection proof. The complete argument is mathematical,
not based on an infeasibility solver.

The hypothesis that all parts have size at least the rank is essential
to this particular argument: it makes 1-s_D<=e_D, which controls the
three repeated-color Fano lines simultaneously. Removing that hypothesis
introduces 1-x_D into these three bounds. No claim that this loss can
always be absorbed is made here. The general hypergraph problem and the
arbitrary-small-part type theorem remain open.

## A finite theorem with a constant independent of the number of parts

**Finite theorem.** Let H be a k-uniform family invariant under arbitrary
permutations inside each of p vertex parts. Suppose every part has
integer size n_i>=k+6. If H has (7,2), then

    tau(H)<=floor(3(k-1)/4)+30.

No restriction on p, on N=sum n_i, or on the set of permitted integer
profiles is imposed. Empty H is trivial, so suppose H is nonempty.

Fix 0<epsilon<1, put r=k-1+epsilon and x_i=n_i-6>=k>r.
For every actual integer profile a of H put

    g_i(a)=max(0,a_i-1+epsilon).

Then 0<=g(a)<=x, sum g(a)<=r, and ceil(g_i(a))=a_i.
The sum bound holds because a has at least one positive coordinate:
if it has d positive coordinates, sum g=k-d+d epsilon<=k-1+epsilon.
Let C consist of all b with g(a)<=b<=x and sum b_i=r, for some permitted
profile a. Such extensions exist since sum x_i>=r. This is a nonempty
closed rank-r type family, being a finite union of closed polytopes.

First, C has no continuous bad tuple. Otherwise choose a witnessing
seven-row support in each part and an original a^j dominated by row b^j.
The sparse rounding lemma of Section 7.199 replaces each part's masses
by a feasible system with at most seven positive cells, total mass at
most x_i, and row loads dominating b^j_i. For integer x_i, rounding up
all cell masses has integer total less than x_i+7, hence at most
x_i+6=n_i. Every rounded row load is an integer at least g_i(a^j), so
at least a^j_i. Trim independently in each row and part to the prescribed
profile a^j. This gives seven actual edges of H, and trimming cannot
create a piercing pair. That contradicts (7,2).

Scale the continuous theorem by r. It gives tau*(C)<=3r/4. The four-class
obstruction also shows that at most three coordinates support a type
with b_i>2x_i/3. Call those coordinates heavy. Take a free box u for C
with deletion cost

    d=sum_i(x_i-u_i)<3r/4+eta<r,

where eta>0 is arbitrarily small. At a nonheavy coordinate every type
has b_i<=2x_i/3. Whenever u_i>=2x_i/3 there, raising u_i to x_i cannot
admit a new type; do so. Each remaining nonheavy coordinate with u_i<x_i
has deletion cost greater than x_i/3>=r/3. Since total cost is less than
r, at most two such coordinates remain. The free box now cuts at most
five coordinates in all.

For those cut coordinates J, define the integer retained counts

    v_i=floor(u_i+1-epsilon) (i in J),
    v_i=n_i                 (i not in J).

This is free for the actual integer profile family. Indeed, if some
actual a<=v, then g_i(a)<=u_i at every cut coordinate: this is immediate
when a_i=0 and follows from a_i<=floor(u_i+1-epsilon) otherwise. At an
uncut coordinate g_i(a)<=x_i=u_i. Hence g(a)<=u. The total size of u is
greater than sum x_i-r. If p>=2 this is at least r, since each x_i>=r;
therefore a rank-r extension of g(a) inside u would belong to C, a
contradiction. For p=1 a has exactly one positive coordinate, so g(a)
already has rank r and yields the same contradiction directly.

Finally v_i>u_i-epsilon on J. The complement of a retained set with
profile v is a transversal of H, of size

    sum_{i in J}(n_i-v_i)
      < d+6|J|+|J|epsilon
      < 3(k-1+epsilon)/4+eta+30+5epsilon.

Let epsilon and eta tend to zero. Since tau(H) is an integer, this proves
tau(H)<=floor(3(k-1)/4)+30. QED.

The bounded number of cut coordinates is the reason the rounding loss
does not grow with p. This improves the generic +6p transfer in this
large-part regime. The six extra vertices per part are used to fit the
seven-cell rounding; the assertion n_i>=k without an additive margin
is not proved by this finite argument.

## Uniform finite theorem down to parts of size six-sevenths of the rank

**Theorem.** Let H be a k-uniform family invariant under arbitrary
permutations within each vertex part, where every integer part size obeys

    n_i>=6k/7+6.

If H has property (7,2), then, independently of the number of parts,

    tau(H)<=floor(3(k-1)/4)+84.

This is a finite counterpart of the dimension-free continuous theorem
at x_i>=6/7, proved in `paper_push_three_theory.md`. The constant 84 is
not claimed optimal. All steps below are hand arguments.

### At most six coordinates need preliminary deletion

Call coordinate i pre-heavy if some actual permitted integer profile a
has a_i>2(n_i-6)/3. Every such profile has a_i>4k/7, so all other entries
of that profile are less than 3k/7, and it cannot be pre-heavy in another
coordinate.

Suppose seven distinct coordinates are pre-heavy. Choose one such actual
profile for each and place these seven profiles on the seven Fano row
labels, once each. We construct integer Fano parent masses part by part.

At a chosen coordinate i, consider the four Fano line-complement cells
containing its own row. Partition the n_i available vertices into these
four cells as equally as possible, with each cell of size floor(n_i/4)
or ceil(n_i/4). Its own row receives all n_i vertices, at least its
required entry. Every other row belongs to exactly two of these four
cells and therefore receives at least

    2floor(n_i/4)>=n_i/2-3/2>=3k/7+3/2>3k/7.

This dominates all its required cross entries. At a coordinate not among
the chosen seven, let q be the maximum of the seven required entries,
an integer less than 3k/7. Give each of the seven Fano parents exactly
ceil(q/4) vertices. Every row then receives at least q. The total is

    7ceil(q/4)<=7q/4+21/4<3k/4+21/4<n_i.

The last comparison follows from n_i>=6k/7+6. Trim each row in each part
to its original integer profile. Every resulting row is an actual edge
of H. No pair of Fano parent cells covers the seven rows, and trimming
cannot create a piercing pair. This contradicts (7,2). Hence there are
at most six pre-heavy coordinates.

Delete six fixed vertices from each pre-heavy part. This costs at most
36 vertices. Let H' be the actual family of edges avoiding this deleted
set, on the remaining parts. If it is empty, the theorem is immediate.
Otherwise every permitted profile a of H' satisfies

    a_i<=x_i:=n_i-6

in every coordinate: in pre-heavy parts this follows from the deletion;
in the others it follows from the defining non-pre-heavy inequality
a_i<=2(n_i-6)/3. The actual remaining part sizes m_i equal x_i in the
pre-heavy parts and x_i+6 in the others.

### Continuous reduction and a bounded number of cut coordinates

Fix 0<epsilon<1 and let r=k-1+epsilon. Form

    g_i(a)=max(0,a_i-1+epsilon)

from the profiles of H', and let C be their closed rank-r up-closure in
the capacity box x. As before g<=x, sum g<=r, and ceil(g_i)=a_i.
Since x_i>=6k/7>6r/7, there is enough total capacity for extensions
when p>=2; the case p=1 is covered separately below.

C has no continuous bad tuple. Indeed, the seven-cell sparse rounding
argument lifts any such tuple into part sizes x_i+6=n_i, with row loads
dominating actual profiles of H'. These are permitted profiles of the
original H, so invariance supplies actual edges of H after trimming.
The lift need not avoid the preliminary deleted vertices; it contradicts
the (7,2) property of the original family directly.

The continuous six-sevenths-capacity theorem gives tau*(C)<=3r/4.
Its seven-distinct-class obstruction, which does not assume a large
transversal coefficient, shows that at most six coordinates support a
type of C with b_i>2x_i/3. Choose a free box u with deletion cost

    d=sum(x_i-u_i)<3r/4+eta<6r/7.

At every nonheavy coordinate with u_i>=2x_i/3 raise u_i to x_i, preserving
freeness. Each remaining cut nonheavy coordinate has cost greater than
x_i/3>=2r/7. Thus there are at most two of them, and at most eight cut
coordinates in all.

For p>=3, sum x_i>=18k/7>18r/7, so |u|=sum x_i-d>r.
Retain floor(u_i+1-epsilon) vertices in each cut coordinate and all m_i
remaining vertices in every uncut coordinate. If these integer retained
counts contained a profile a of H', then g(a)<=u; since |u|>=r, it would
extend inside u to a member of C. This contradicts freeness. The
complement of the retained set therefore hits H'. Its size is less than

    d+6(8)+8epsilon<3r/4+eta+48+8epsilon.

Adding the preliminary at-most-36 vertices gives a transversal of H of
size less than 3r/4+eta+84+8epsilon. Let epsilon,eta decrease to zero
and use integrality to obtain the stated bound.

If p<=2, the already proved all-two-part finite theorem gives the stronger
bound floor(3(k-1)/4)+12, with no part-size hypothesis. This handles the
only cases where the rank-extension estimate above was not invoked and
completes the proof. QED.

The finite theorem applies uniformly to sequences with arbitrarily many
parts, each at least (6/7+delta)k for any fixed positive delta and large
enough k. It also covers the explicit additive boundary n_i>=6k/7+6.
It does not cover arbitrarily small parts or arbitrary non-invariant
hypergraphs.
