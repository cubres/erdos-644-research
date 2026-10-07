# The remaining gap after two near-Fano requests

Status: the common-core exclusion and gap-adjusted repair-cover lemmas
below are hand proved. The two finite support calculations are exact
integer certificates [C], produced by the scripts listed below. No new
upper bound on the transversal number is obtained here. In particular,
the desired 108b+O(1) bound at a=33b remains unproved.

This report uses the new two-request construction and its actual responses;
it does not rerun the original five-row neighborhood optimization.

## 1. Setting and the rank deficit's first hiding place

Use the 35-type construction with a=33b. The old ground U has 259b
points: 33b in each Fano-line complementary type, and b in each
line-plus-one-point complementary type. The original six rows have
coordinates 1,...,6, and their endpoint set P has size p=111b. Assume
these six rows attain the global minimum endpoint count in the containing
actual (7,2) family. The available rank is k=144b+1.

On four old rows [2,4,5,6], put

    D1 = union of masks 0010,0110,1001,1011,1101.

The request has size 108b. An actual response G avoiding it has at most
k points, while the available old ground U\D1 has size 151b. Thus at
least 7b-1 old points are omitted by G, and more are omitted if G uses
points outside U.

For the fixed companion request consisting of masks

    0011,1010,1100,1101,1110,

the maximal remaining endpoint count is 114b. The available masks
0011,1000,0000 are endpoint-inert for that particular two-request
upper graph and together have mass 73b. Consequently the required
rank omission can be placed entirely in those classes. This explains
why rank alone cannot strengthen that fixed upper graph to 111b.

## 2. Exact aggregation of whole-cell second requests

Here is a precise upper-bound relaxation that can combine all whole-cell
second requests without pretending that partial traces are actual edges.

Fix four old rows with empty common intersection, and let K be their
piercing graph on U. Let A be the old point types allowed by D1. For a
second request D2, which is a union of complete four-row types, define

    B(D2) = {s : some type v in A is adjacent to s in K,
                    and s,v are not both in D2},

    Q(D2) = {s in A\B(D2) : some type v is adjacent to s in K,
                                  and s,v are not both in D2}.

Write g_s=|G intersect type s|. If H is an actual response avoiding D2,
then the endpoint set of the four old rows together with G,H has size
at most

    w(B(D2)) + sum_{s in Q(D2)} g_s.                    (1)

To prove this, first enlarge H to all of U\D2. For a point outside G
to be an endpoint, its partner must be a G-point, hence must belong to
an allowed type. This gives B(D2), where allowing a positive G-partner
in every allowed type only enlarges the bound. A G-point outside B(D2)
can still be an endpoint only through a pair counted in Q(D2). A point
outside U cannot help pierce the four old rows, since their common
intersection is empty. Thus outside masses do not invalidate (1).

If t>108b, every D2 of size at most 108b is avoided by an actual H.
Global endpoint minimality then makes

    sum_{s in Q(D2)}g_s >= 111b-w(B(D2))                (2)

a necessary condition on the first response G.

[C] Across all twelve four-old-row subsets with empty common
intersection, enumerate every union of their whole point types with
mass at most 108b. There are 51264 such choices, counted with their
four-row subset. After dropping nonpositive right sides and duplicate
inequalities, exactly two conditions remain. If g_L denotes G-mass
in the complementary type L, they are

    g_0346 + g_0456 + g_2346 + g_2456 >= b,
    g_0124 + g_0234 + g_1246 + g_2346 >= b.             (3)

Both have a second request of size 108b and constant term 110b in
(1). The common type 2346 has capacity b. Taking its mass equal to b
and all other g-masses zero satisfies every inequality (2). Conversely,
either displayed condition forces total g-mass at least b. Hence the
exact minimum rank demanded by this entire linear relaxation is only b.

This is a limitation of the stated relaxation, not an actual-family
counterexample: the mass vector does not claim all other global
six-row or seven-row obligations. In particular, the relaxation permits
partners from an allowed type even if its chosen G-mass is zero.
Whole-cell request averaging at this level therefore cannot provide
the missing rank contradiction. Partial-cell requests, actual support
correlations, and later configurations with multiple responses are
not covered by this obstruction.

The standard-library certificate is

    python3 -S work/p644_second_request_linear_obligations.py

It writes `outputs/agent_second_request_linear_obligations.json` and
completed with EXACT_PASS. The final certificate uses no optimization
solver or floating-point arithmetic.

## 3. How to exclude outside endpoints in a previously unsafe core

**Lemma 1 (common-core exclusion).** Let A_1,...,A_4 be four old rows
contained in U, with common intersection J. Let G,H be actual rows.
If

    J intersect (G union H)=empty,
    (G\U) intersect (H\U)=empty,

then every endpoint of a piercing pair for A_1,...,A_4,G,H lies in U.

**Proof.** If a piercing pair uses x outside U, its other point z must
belong to J in order to meet all four old rows. Since z belongs to
neither G nor H, the point x would have to belong to both G and H,
contrary to their disjoint outside traces. QED.

Both conditions matter. If J has a point in G and H misses J, then
every point of H is an endpoint, by pairing with that point of J.
Such a configuration cannot lower the global endpoint minimum merely
by bounding H from above by its rank when |H| can exceed p.

For the present first request, the three common four-old-row classes
are the base line classes 012,034,056. The first and third lie in G
for the dense response below. The middle class 034 is excluded by D1.
Therefore the useful previously unsafe core is [1,2,5,6], whose common
class is 034. An H avoiding all three base endpoint classes and avoiding
G's outside part makes Lemma 1 applicable.

## 4. An actual two-response survivor and its exact common defense

Let R be an 8b-subset of the base class 245, and let Y be b new outside
points. Use the dense first response

    G = ((U\D1)\R) union Y.

Let C consist of the four endpoint defect classes

    0125, 0126, 0156, 0256,

and set

    D2 = (P\C) union Y,
    H  = (U\(P\C))\R.

The two requests have size 108b. Both responses have rank 144b:

    |G|=(259-108-8+1)b=144b,
    |H|=(259-107-8)b=144b.

H has no outside points at all, so it excludes the shared outside
defense completely. The safe common core [1,2,5,6,G,H] nevertheless
has 151b endpoints.

The full actual-family verification is provided by the parallel
certificate `outputs/agent_near_fano_outside_control_certificate.json`:
the two responses survive all the required six-row minima and
seven-row piercing checks in that finite family. Its closest new
six-tuples have endpoint count 115b:

    [1,2,3,5,6,H],   [1,2,4,5,6,H].

That certificate is used here as an input; this report's new calculation
concerns their repair supports. The finite family has small transversal
number and is not a counterexample to the desired high-t theorem.

The common old defense has exact size

    |G intersect H|=71b.                               (4)

Thus, under t>108b, a third actual response can be forced to avoid the
entire intersection G intersect H and any additional 37b chosen points.
Equation (4) is a useful new request budget, not a proof that this
third request must succeed.

## 5. A valid repair-cover lemma for a nonminimal six-tuple

The new 115b tuples must not be assumed globally minimal. The following
version uses the true global endpoint minimum p and charges the gap.

**Lemma 2 (gap-adjusted full-repair cover).** Let Q be any six actual
rows with piercing graph Pi and endpoint set P_Q of size p+s, where p
is the global minimum endpoint count. Delete row i and let K_i be the
five-row piercing graph. Let W_i be the full set of endpoints of the
new pairs K_i\Pi. For any S subset P_Q with |S|>s, the set

    W_i union N_Pi[S]                                  (5)

is a global transversal. Here N_Pi[S] is the closed neighborhood.

**Proof.** Suppose an actual row F avoids (5). A pair in K_i\Pi has
both endpoints in W_i, so it cannot meet F. Therefore every pair
piercing the five retained rows and F belongs to Pi. Every Pi-pair
incident to S has both endpoints in N_Pi[S], so it also fails to meet
F. The new six-row endpoint set is consequently contained in P_Q\S,
of size p+s-|S|<p, contrary to the global definition of p. QED.

This authorizes a cover from a nonminimal tuple, with the exact cost
that more than s of its endpoints must be eliminated. It does not
authorize the old zero-gap repair inequality unchanged.

## 6. Why the closest tuples do not pay their 4b gap through full repairs

For both closest tuples, s=4b. [C] Their full repair supports have the
following sizes, in units of b:

| Six-tuple | Deleted row | Repair support size/b |
|---|---|---:|
| [1,2,3,5,6,H] | 1,2,5,6 | 114 |
| [1,2,3,5,6,H] | 3 | 113 |
| [1,2,3,5,6,H] | H | 115 |
| [1,2,4,5,6,H] | 1,2,5,6 | 114 |
| [1,2,4,5,6,H] | 4 | 113 |
| [1,2,4,5,6,H] | H | 107 |

Only the final 107b support could fit inside a 108b request. Its
intersection with P_Q consists of five point types. Their Pi-neighbor
mass outside W_H is respectively

    76b, 36b, 36b, 36b, 36b.                           (6)

The base type among them is 034; the other four complementary types
are 0134,0234,0345,0346. Equation (6) is an exact mass statement about
complete neighbor classes, so it also handles arbitrary partial point
selections.

Suppose a request D contains this W_H and has size at most 108b.
It adds at most b points. No old endpoint already in W_H can have
its entire Pi-neighborhood covered by D, by (6). Hence every old
endpoint whose closed neighborhood is contained in D must belong to
D\W_H. There are at most b such endpoints. Lemma 2 needs more than
4b, so it cannot apply. The same argument excludes 108b+O(1) for all
sufficiently large b.

The new standard-library certificate is

    python3 -S work/p644_two_request_gap_obstructions.py

It independently generates G,H and their finite point types, checks
that every five-row graph used here has empty common intersection,
and writes `outputs/agent_two_request_gap_obstructions.json`. It
completed with EXACT_PASS. This is a new repair-support calculation;
the full six/seven consistency certificate is not rerun.

This rules out the particular sufficient method which first includes
the **entire** W_i and then isolates more than the 4b gap in the old
six-row graph. More selective closed neighborhoods in the full
five-row graph can avoid that cost and are not ruled out here. Neither
are third requests using both new responses and three old rows.

## 7. Remaining forward condition

The presently valid two-request argument gives the parent's bound
3a+ceil((21b+1)/2), leaving 1.5b above the target 3a+9b+O(1).
The new results explain three distinct failures of an immediate
strengthening: rank omissions can hide in inert classes; whole-cell
second-request aggregation gives only the two weak obligations (3);
and the closest surviving tuples' full repair supports do not pay their
4b endpoint gap at the target budget.

The concrete unused obligation is a third response avoiding the 71b
common defense in (4), with 37b further avoidance capacity, or a
selective neighborhood using both G and H. No assertion is made that
these remaining possibilities fail or that the research is exhausted.
