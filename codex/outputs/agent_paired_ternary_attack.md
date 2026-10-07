# Three disjoint pairs: targeted finite-state attack

Status: the requested necessary-constraint exploration is complete. It does
not prove the intermediate-endpoint-mass case. It identifies a small exact
state and a rigid paired exchange that any successful continuation must use.
No result here asserts that a finite response state extends to a family of
large transversal number.

## 1. The 26-type exploration

`work/p644_agent_alternative_paired_ternary.py` uses the nonempty types in
`{*,0,1}^3`, with each coordinate representing an actual disjoint pair.
It imposes the six rank bounds, the exact antipodal endpoint mass m, all
sixteen-mode subset-neighborhood profiles for every retained two pairs,
connected-seed bounds, the proved high-m bound

    tau <= 7/2 - 3m/2,

and the new necessary condition that each triple of actual rows has some
intersection strictly greater than 1/4. A floating-point MILP for the
matching disjointness graph has a feasible optimum tau=m=1.2, well above
3/4. This is discovery evidence that these inequalities do not close the
case, not a realizable hypergraph or an exact optimization certificate.

The following much cleaner exact state already suffices to explain the
failure of the same inequalities. Normalize k=1 and take cells

| Cell | Type | Mass |
|---|---|---:|
| A | 000 | 1/2 |
| B | 011 | 1/2 |
| C | 100 | 1/4 |
| D | 101 | 1/4 |
| E | 110 | 1/4 |
| F | 111 | 1/4 |

Every row has size 1 and each of the three disjoint pairs partitions the
ground set U of size 2. The six-row piercing graph has components A x F
and B x C, so its endpoint mass is m=3/2 and its pair count is q=1/4.
Every triple of the six rows has two rows intersecting in at least 1/2.
For retained coordinates 0,1 or 0,2, the four quadrant masses are all 1/2;
the smallest strict subset-neighborhood profile is 1. For retained
coordinates 1,2, the masses are (3/4,1/4,1/4,3/4), with smallest strict
profile 5/4. Thus neither the profiles nor the small-intersection-triangle
theorem excludes this state.

## 2. An exact one-pair response

Request an actual G avoiding A union F, of mass 3/4, and let H be an actual
disjoint partner. The following response stays entirely in U. For
0<e<1/8 put

    G = (0, 1/2-e, 1/4-e, 1/8+e, 1/8+e, 0),
    H = (1/2, e, e, 1/8-e, 1/8-e, 1/4),

where each entry specifies the mass in A,B,C,D,E,F respectively and the
two entries partition each cell. Both rows have size 1. At e=1/16 exact
enumeration of the eight rows gives:

| Three coordinate pairs | Endpoint mass | Pair count |
|---|---:|---:|
| 0,1,2 | 3/2 | 1/4 |
| 0,1,3 | 27/16 | 11/64 |
| 0,2,3 | 27/16 | 11/64 |
| 1,2,3 | 2 | 21/64 |

Every seven-row subfamily has a piercing pair, and every triple has a pair
intersection greater than 1/4. [C: exact rational arithmetic, routine
`inspect(state('inside'),4)` in
`work/p644_agent_alternative_paired_second.py`.]

Consequently the request survives minimum-endpoint-mass comparison. It
would fail comparison to a globally minimum pair count, since 11/64<1/4.
These are different global choices and cannot be assumed simultaneously.

An earlier proposed response G=B union C union half(D) union half(E),
H=its complement, is invalid for endpoint minimization: two new paired
triples have endpoint mass 5/4. The split response above fixes that defect.

## 3. A response with outside points, independently checked

In units of 1/32 one can also take

    G=(0,13,7,6,6,0), H=(16,3,1,2,2,5),

and add 3/32 fresh mass to H. Leave 3/32 of F in neither new row. Each
rank is 1. New paired masses are 27/16,27/16,61/32 and their pair counts
are 87/512,87/512,301/1024. Again all seven-row and triangle checks pass.
[C: `inspect(state('outside'),4)` in the same script.]

This state is useful for testing a second response that is allowed to
interact with the first response's outside points; it is not needed for
the simpler obstruction in Section 2.

## 4. Full second-response model and its precise scope

`work/p644_agent_alternative_paired_second.py` splits every positive old
cell between a new disjoint pair, allowing each new row to use fresh
outside points. It imposes all seven-row subfamilies of the ten rows,
the endpoint lower bound 3/2 for every new triple of paired coordinates,
the rank bounds, and the small-intersection-triangle prohibition. It
restricts the new pair to intersect each old row, so a found response is
valid but infeasibility would only exclude that restriction.

Four tested requests against the inside-U response all survive:
A union F; A plus mass 1/4 of B_G; B union C; and D union E union F.
Three corresponding requests against the outside response also survive.
The surviving solutions were rationalized and directly checked by
enumerating actual nonzero cells. These are finite request tests, not a
claim that every second request survives. No further catalogue was run.

The last request has zero best endpoint margin and leads to the following
hand lemma, stronger than simply recording a feasible point.

## 5. Rigid exchange lemma for the clean state — hand proved

Assume the clean state in Section 1 attains the global minimum endpoint
mass 3/2 among triples of actual disjoint pairs. Choose an actual G
avoiding D union E union F, and an actual disjoint partner H. Retain the
two coordinate pairs 1 and 2. Their piercing graph is

    (A union C) x (B union F), together with D x E.

Because G misses D,E,F, the second component contributes no piercing pair
after G,H are added. Every endpoint of the resulting paired six-tuple
belongs to A union B union C union F, whose mass is 3/2. Hence global
minimality forces the new endpoint set to be exactly this union.

In particular every point of A union B union C belongs to exactly one of
G,H, while every point of F belongs to H. Set

    x=|G intersection (A union C)|,
    y=|G intersection B|, s=x+y.

The rank bounds on G,H give 1/2<=s<=1: G has at least s points, and H has
at least 3/2-s points. The new piercing graph therefore has pair count

    q_new=x(3/4-y)+y(3/4-x)
         =3s/4-2xy
         >=3s/4-s^2/2
         >=1/4.

The first inequality uses xy<=s^2/4. The last quadratic is concave on
[1/2,1] and equals 1/4 at both endpoints. Equality holds precisely when

    (s,x,y)=(1/2,1/4,1/4) or (1,1/2,1/2).

Thus this request forces an exact endpoint-set equality, but minimizing
pair count after minimizing endpoint size does not close it: pair count
can only increase. The two equality cases force one of the new rows to
use exactly 1/2 outside this endpoint set, and the other to use none
outside it. This is the useful structural conclusion for a subsequent
exchange that also controls those outside points.

## 6. Remaining global gap

The high-endpoint-mass argument closes m>=11k/6+O(1), whereas the clean
state has m=3k/2. The existing profile inequalities do not force m into
that high regime or produce a small transversal in the intermediate
regime. A next proof must exploit compatibility of many paired exchanges,
or select a different global extremum; it cannot just apply the currently
listed inequalities to one triple of disjoint pairs. The rigid equality
lemma narrows one exchange to two explicit outside-mass alternatives,
which is more specific than an unrestricted response search.

## 7. A successful Q-minimum exchange — hand proved

This changes the globally minimized quantity: let Q be the number of
unordered pairs piercing six rows, minimized over all triples of actual
disjoint pairs of a rank-at-most-k family in which every edge has a
disjoint partner. Repetitions of pairs are allowed. Suppose a minimizing
triple has exactly the six positive cells of Section 1, with masses
k/2,k/2,k/4,k/4,k/4,k/4. Then

    tau <= 3k/4 + 2.

The exact equal-size statement assumes the indicated cell sizes are
integers. There may be arbitrary vertices outside all six old rows.

Proof. Suppose tau>3k/4+2. Choose one point of B and one point of D, and
request an actual G avoiding these two points and all of A union F.
Choose an actual disjoint partner H. Normalize masses by k and write

    (G_A,G_B,G_C,G_D,G_E,G_F)=(0,b,c,d,e,0),
    (H_A,H_B,H_C,H_D,H_E,H_F)=(a',b',c',d',e',f').

Then b<1/2 and d<1/4. Disjointness gives, in particular,

    a'<=1/2, b'<=1/2-b, c'<=1/4-c,
    d'<=1/4-d, e'<=1/4-e, f'<=1/4.

All variables are nonnegative, c,e<=1/4, and the sum of the six primed
variables is at most 1, even if H also has outside points.

Retain old coordinate pairs 0,1, or 0,2, or 1,2, respectively, and append
G,H. Their normalized piercing-pair counts are exactly

    q01=a'e+b(c'+d')+b'(c+d),
    q02=a'd+b(c'+e')+b'(c+e),
    q12=b(a'+c')+c(b'+f')+d e'+e d'.

These formulas include every activation case, including empty cells.
Each piercing pair must use one point of G and one point of H, and their
old two-coordinate types must be opposite. A point outside all six old
rows cannot contribute: its partner would need to meet both members of
an old disjoint pair. Thus outside mass contributes neither an omitted
term nor an error term.

If b>=1/4, the capacity bounds imply

    q01 <= b/2+(d+e)/2+(1/2-2b)c-2bd,
    q02 <= b/2+(d+e)/2+(1/2-2b)c-2be.

Put u=min(d,e), v=max(d,e). Since 1/2-2b<=0,

    min(q01,q02)
      <= b/2+u/2+(1/2-2b)v
      <= b/2+(1-2b)u
      <= b/2+(1-2b)d
      < b/2+(1-2b)/4 = 1/4.

The strict inequality uses both b<1/2 and d<1/4.

If b<1/4, every coefficient in the displayed formula for q12 is at most
1/4, hence q12<=1/4. Suppose equality holds. The rank bound for H must
be tight, and the coefficients b,d that are strictly below 1/4 force
a'=c'=e'=0. The remaining capacities give

    1=b'+d'+f' <= (1/2-b)+(1/4-d)+1/4 =1-b-d.

Thus b=d=0 and b'=1/2,d'=f'=1/4. Equality in q12 also forces
c=e=1/4. Substituting gives q01=1/8<1/4. Therefore in every case at
least one replacement triple has fewer than k^2/4 piercing pairs,
contradicting the global minimum. QED.

The two additional deleted points are essential to this particular
strictness argument: at b=1/2 or d=1/4 boundary responses can tie the old
pair count. Their cost is O(1), which is harmless for the target
asymptotic bound. This is a successful bounded exchange, rather than a
computer-discovered obstruction.

## 8. Extension to a one-parameter family — hand proved

The preceding theorem extends to

    A=B=k/2, C=F=ck, D=E=(1/2-c)k,
    1/4 <= c <= 1/2.

For any globally Q-minimizing triple of this form,

    tau <= 3k/4+2.

The old normalized pair count is q_old=c. The endpoint mass, which is
not being minimized here, is 1+2c.

The case c=1/4 was proved above. Suppose c>1/4 and put s=1/2-c.
Request G avoiding A and a subset of F of size ceil(k/4). This costs
at most 3k/4+1. Normalize by k and put

    G=(0,b,z,d,e,f), H=(a',b',c',d',e',f'),

so f<=c-1/4. The three replacement counts are

    q01=(e+f)a'+b(c'+d')+b'(z+d),
    q02=(d+f)a'+b(c'+e')+b'(z+e),
    q12=(b+f)(a'+c')+z(b'+f')+d e'+e d'.

If b>=1/4, applying the capacities

    a'<=1/2, b'<=1/2-b, c'<=c-z,
    d'<=s-d, e'<=s-e

and using c+s=1/2 gives exactly the previous inequalities with an
additional term f/2. Hence

    min(q01,q02) <= b/2+(1-2b)min(d,e)+f/2
      <= b/2+(1-2b)s+(c-1/4)/2
      <= 1/4+(c-1/4)/2 < c.

For the penultimate inequality, b<=1/2 and s<1/4, so the displayed
affine expression is maximized at b=1/2.

If b<1/4, the coefficients of all primed variables in q12 are at most
c: b+f<c, z<=c, and d,e<=s<c. Therefore q12<=c. Equality would force
a'=c'=d'=e'=0 and b'+f'=1. But

    b'+f' <= (1/2-b)+(c-f) <= 1/2+c < 1

when c<1/2, a contradiction. At c=1/2 equality instead forces b=f=0,
b'=f'=1/2,z=1/2, and then q01=1/4<c. Thus some replacement has strictly
smaller Q in every case, again contradicting the global minimum. QED.

The uncovered part of this same family is 0<c<1/4. A floating-point
deletion minimax on the vertices of the deletion polytope suggests that
the three-replacement Q maximum remains at least 1/4 there, above the old
q=c. That observation is a guide for changing the argument; it is not an
impossibility theorem about all deletions or about further responses.

## 9. Open-neighborhood consequence — hand proved

For every fixed template in Section 8 and every epsilon>0, there is an
eta>0 such that a globally Q-minimizing paired triple within eta of that
template in normalized ternary-cell masses forces

    tau <= (3/4+epsilon)k+O(1).

This allows small positive masses on any of the other 26 nonempty
ternary types, not just perturbations of the six displayed positive
cells. Here distance can be the sum of absolute mass differences.

Proof. First make the deletion have a fixed strict normalized margin.
At c>1/4 the deletion in Section 8 already does this. At c=1/4 use the
deletion A union F plus positive mass rho from each of B,D, with
2rho<epsilon/2. Section 7 proves a strict Q drop for every response with
b<=1/2-rho and d<=1/4-rho.

The possible normalized traces of G,H on the fixed finite set of ternary
types form a compact polytope: their masses are nonnegative, their sum
on each cell is bounded by the cell mass, and each new row has total
trace at most 1. Each replacement count is a quadratic polynomial in
these traces. In particular no positivity-indicator or endpoint-support
variable occurs. The minimum of the three replacement counts is
continuous, so the strict inequality throughout the compact response
polytope has a positive uniform margin.

For completeness, the margin persists under perturbation by the usual
subsequence argument. If it did not, there would be old cell masses
converging to the template and feasible responses with no strict Q
improvement. Choose the deletion amounts continuously near the fixed
ones (delete an entire designated cell when specified, and truncate any
fixed partial amount at that cell's available mass). A subsequence of
the response traces converges. The limit satisfies every capacity,
deletion, and rank constraint of the original response polytope, while
continuity of all pair counts contradicts its strict margin. Cells with
zero limiting mass cause no exception: both new traces there tend to
zero. Vertices outside all six rows never participate in a piercing
pair for a paired replacement, as explained in Section 7.

Finally, for sufficiently small eta the deletion cost is at most
3/4+epsilon, with only bounded integer rounding overhead. A transversal
number above this cost supplies an actual avoiding G, and its actual
disjoint partner supplies the forbidden response. QED.

This stability is a concrete advantage of Q minimization over endpoint
minimization: tiny cells can abruptly activate large endpoint sets,
whereas their contribution to a pair count tends continuously to zero.

## 10. General Q-minimum degree profile — hand proved

Let Q be the global minimum piercing-pair count over triples of actual
disjoint pairs, and suppose every actual edge has a disjoint partner.
Take any two actual disjoint pairs, and let K be their four-row piercing
graph. For v in its vertex set write deg_K(v) for the number of possible
partners of v. Extend the degree by zero outside the endpoint set.

Then

    {v : deg_K(v) >= Q/k}

is a global transversal. Indeed, if an actual G avoided this set, choose
an actual disjoint partner H. Every piercing pair of the four old rows
plus G,H uses exactly one point of G and one point of H. Hence its count
is at most

    sum_{v in G} deg_K(v) < |G| Q/k <= Q,

contradicting minimality. The first strict inequality is valid since
G is nonempty and Q>0 under property (6,2).

More generally, if a deletion D has the property that the sum of the k
largest remaining K-degrees is less than Q (pad by zeros when necessary),
then D is a global transversal, by the same argument. This is an
inexpensive necessary profile for future Q-first finite-state models.
It does not require the chosen four old rows to come from a minimizing
six-tuple and does not assume minimum endpoint mass.
