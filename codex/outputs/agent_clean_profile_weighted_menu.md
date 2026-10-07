# Clean six-row profiles: weighted menu and a triangle lemma

Status: the request implications below are hand proofs. The finite type-table
checks also have a standard-library exact certificate. This report does not
prove the general clean-profile theorem, and no weighted profile below is
claimed to be a counterexample to the Erdős bound.

## 1. Setting and endpoint comparison

Let H be a rank-at-most-k family with property (7,2). For an actual subfamily
S, write P(S) for the points that occur in a two-point transversal of S. Suppose
every subfamily of at most six edges has at least p endpoints, equivalently
every indexed six-tuple with repetitions has at least p endpoints. It is enough to impose this
only on six-edge subfamilies with empty common intersection for the arguments
here. All selected old cores below have empty common intersection.

We use the following elementary request rule. Retain j actual old edges with
empty common intersection, and choose 6-j sets D_i of size at most T. If
tau(H)>T, there are actual response edges A_i avoiding D_i. Every transversal
pair of the resulting six rows must cover the old rows. Also its two points
cannot both belong to any D_i. Thus the endpoints of the resulting six rows
are contained in the endpoint support of the old pair graph after deleting
every pair wholly contained in at least one D_i. If that support has size less
than p, there is a contradiction. If some selected actual edges coincide,
the assumed endpoint lower bound still applies. When the family contains
six distinct edges, extension to six distinct rows is also legitimate and
can only shrink the endpoint set. We do not require distinctness of the
indexed witness rows at degenerate parameter values.

No restriction on new outside points is needed: a point outside the old core
union cannot participate in an old transversal pair, because its partner would
have to belong to every old row.

The clean six-row support consists of the four star triples

    235, 145, 136, 246

and the three four-types 1234, 1256, 3456 together with their twelve distinct
three-subtypes. The four star types are noneligible for the six-row graph;
with all nineteen masses positive, all other fifteen types are eligible.
In the symmetric specialization let each star mass be c, each four-type mass
be a, and each of the twelve other triples have mass b. Then each row has size

    k0 = 2c + 2a + 6b,

and the endpoint set has size p = 3a + 12b. When a or b is zero, eligibility
must be checked separately; the lemmas remain valid under the explicit global
endpoint lower bound p used in their statements.

## 2. An exact weighted criterion for the existing two-request table

Retain rows 2,4,5,6, in that order. Their four-bit cell masses are m_s. The clean
support projects into types 0,1,2,3,5,6,8,9,10,11,12,13,14. A request code q
specifies which request sets contain a point: bit 1 denotes D_1 and bit 2
denotes D_2. Use this table:

| Old type s | Request code q | Mass |
|---|---:|---:|
| 0,5,8 | 0 | their full masses |
| 1,2,3,10,14 | 1 | their full masses |
| 6,11 | 2 | their full masses |
| 13 | 3 | m_13 |
| 9 | 2 | m_9-e_9 |
| 9 | 3 | e_9 |
| 12 | 1 | m_12-e_12 |
| 12 | 3 | e_12 |

Here 0 <= e_9 <= m_9 and 0 <= e_12 <= m_12. Define

    d1 = m1+m2+m3+m10+m12+m13+m14,
    d2 = m6+m9+m11+m13,
    r0 = m5+m9+m10+m11+m12+m14.

The request costs are d1+e9 and d2+e12. A pair can survive the request
restrictions only when its old types have union 1111 and its request codes
are disjoint. Directly checking these conditions leaves endpoints only in
types 5, 9 with code 2, 10, 11, 12 with code 1, and 14. Their total mass is

    r0-e9-e12.

Consequently this table proves tau(H)<=T whenever

    d1<=T, d2<=T,
    min(m9,T-d1)+min(m12,T-d2) > r0-p.                 (2.1)

For integer masses and T the displayed minimum choices are integers, so the
strict criterion directly supplies actual subsets. There is no rounding
assertion hidden here. For real asymptotic masses, rational choices can be
scaled; an equality boundary alone requires an additional strictness or
integer argument.

Replacing the last strict inequality by a weak one is equivalent to four
linear inequalities:

    r0-p <= m9+m12,
    r0-p <= m9+T-d2,
    r0-p <= T-d1+m12,
    r0-p <= 2T-d1-d2.

Together with d1,d2<=T these give a finite piecewise-linear menu suitable for
future exact covering calculations. Permuting the four underlying K4 vertices
gives 24 versions of this table.

## 3. Exact hole in that fixed orbit

For the symmetric profile, straightforward projection gives

    d1 = 3a+9b,
    d2 = a+2c+3b,
    r0 = a+2c+6b,
    m9 = b,  m12 = 2b.

Put h=c-a-3b. Then

    k0 = 4a+12b+2h,
    T = 3k0/4 = 3a+9b+(3/2)h,
    d2 = 3a+9b+2h,
    r0 = p+2h.

If h>0, the second baseline cost exceeds T by h/2. If h<0, the first
baseline cost exceeds T by -3h/2. Since the profile is invariant under all
24 K4 automorphisms, all table copies have the same two baseline costs, up
to request exchange. Therefore at the exact 3k0/4 budget the entire fixed
orbit is legal only at h=0.

The concrete positive-excess example c=a+4b, b>0, gives

    k0 = 4a+14b, p = 3a+12b, T = 3a+(21/2)b,
    d1 = 3a+9b, d2 = 3a+11b.

The second baseline exceeds the target by b/2, while p exceeds the target by
3b/2. Thus neither this table orbit nor the trivial cover by P removes this
profile. This is a rigorous obstruction to this particular menu only.
It does not rule out another allocation, an adaptive strategy, or the desired
3/4 theorem for the clean class.

For a=33,b=1,c=37, the fixed table has costs (108,110), residual 113, and
donor capacities (1,2). Even budget 110 leaves residual at least 112. At
budget 111 it can reach residual 111 but not a strict endpoint decrease.
Secondary minimization of the number of transversal pairs could potentially
use this equality case; the present endpoint argument does not do so.

## 4. A new three-request triangle lemma

**Lemma.** Suppose the symmetric clean profile occurs among six actual rows
and the global six-row endpoint minimum is at least p=3a+12b. For nonnegative
integer a,b,c with a+2b>=1,

    tau(H) <= 2c+a+4b+1.                              (4.1)

In particular, if c<=a+b, then

    tau(H) <= 3k0/4+1.

**Proof.** Retain rows 1,3,5. No supported type contains all three. Their
projection has type 000 of mass c; each singleton 001,010,100 has mass 2b;
and each doubleton 011,101,110 has mass c+a+2b. Its transversal graph consists
of the three edges from each singleton to its complementary doubleton,
together with all pairs of distinct doubleton classes.

Choose an integer e with 1<=e<=a+2b. Split each doubleton into a heavy piece
of size c+e and a light piece of size a+2b-e. Three request codes have bits
1,2,4 for D_1,D_2,D_3. Assign the following codes:

| Old type | Piece | Request code |
|---|---|---:|
| 000 | all | 0 |
| 001 | all | 4 |
| 010 | all | 2 |
| 100 | all | 1 |
| 011 | heavy / light | 3 / 4 |
| 101 | heavy / light | 6 / 1 |
| 110 | heavy / light | 5 / 2 |

Each request contains two heavy doubleton pieces, one light doubleton piece,
and one singleton class. Thus each has size

    2(c+e)+(a+2b-e)+2b = 2c+a+4b+e.

Every heavy doubleton point becomes isolated in the residual transversal
graph. Indeed, each of its possible old graph neighbors has a request code
overlapping its two-bit request code, as inspection of the table shows.
Therefore all residual endpoints lie in the three light doubleton pieces
and the three singleton classes. Their total size is at most

    3(a+2b-e)+6b = p-3e < p.

If tau(H) exceeded the request size, three actual response rows avoiding the
requests would contradict the global six-row endpoint lower bound by the
request rule in Section 1. Taking e=1 proves (4.1). Finally

    2c+a+4b <= (3/4)(2c+2a+6b)

is equivalent to c<=a+b. This proves the last assertion. QED.

The result is conditional on the actual witness having these row sizes;
to state it as a rank-k bound use k=k0 (or note that a larger ambient k only
weakens the target). The proof applies to actual rank-at-most-k families and
does not require equal ranks for the response edges.

## 5. What remains unresolved

The existing two-request balance theorem handles c=a+3b. The triangle lemma
adds the region c<=a+b. If p<=3k0/4, equivalently c>=a+5b, the global
transversal P itself gives the target. These facts leave, for this report's
methods, the intermediate symmetric range a+b<c<a+5b, except for the solved
balance c=a+3b. Most urgently, c=a+4b is still open here. Arbitrary unequal
masses in the full nineteen-type clean class are also open.

Two numerical unrestricted cell-splitting searches at a=33,b=1,c=37 found
two-request and triangle-three-request costs near 111, against the target
109.5. They are discovery evidence only. No exact dual or exhaustive
certificate establishing a universal lower barrier for those larger search
classes was obtained. The exact obstruction established above is only to
the fixed 24-table orbit.

## 6. Reproduction and scope

Run:

    python3 work/p644_clean_profile_allocation_check.py

The script checks exact coefficient projections, the surviving endpoint
support for the weighted two-request table, and all request and residual
coefficients in the triangle construction. It has no solver dependency and
uses no floating-point computation. The hand proofs do not depend on the
numerical exploratory optimizers.

Exploratory files, retained without promoting their output to theorem status:

* work/p644_clean_profile_menu_hole.py
* work/p644_clean_symmetric_two_request.py
* outputs/agent_clean_profile_menu_hole_discovery.json
* outputs/agent_clean_symmetric_request_33.0_1.0_37.0.json
* outputs/agent_clean_symmetric_request_3_33.0_1.0_37.0.json

No main-note changes were made by this agent.
