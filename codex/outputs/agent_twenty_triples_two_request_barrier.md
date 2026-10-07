# Symmetric twenty-triple witness: the 7.5 allocation target fails

Status: the target obstruction below is a hand proof. A separate rational
upper allocation is checked exactly. The numerical solver's optimality
status is not used as a lower-bound certificate.

Start with six rows on twenty cells of mass one, one for each triple of
[6]. Every row has rank 10. Every choice of four retained rows is equivalent
under permutation of the six labels. Its fourteen projected cells are:

    T_i = triple missing i: mass 1,       i in [4];
    C_i = singleton i:      mass 1;
    B_ij = doubleton ij:    mass 2,       ij in binom([4],2).

The total mass is 20. The pair graph consists of the complete graph between
the four T cells, edges T_i--C_i, edges T_i--B_ij, and the three complementary
B-cell pairs. All fourteen cells are nonisolated.

Give every point an arbitrary request code in {0,1,2,12}, allowing real
splits within cells. Write b1,b2 for request costs, r for the endpoint mass
of the relaxed residual graph, q for total code12 mass, and u for total
code0 mass. A pair remains in this relaxed graph exactly when its old cell
types cover the four rows and its request codes are disjoint.

## Hand theorem

If b1<8 and b2<8, then

    r >= 16 - (b1+b2)/2.                       (1)

In particular, b1,b2<=15/2 force r>=17/2. There is NO allocation having
max(b1,b2,r)<=15/2. Moreover the minimum possible value of that maximum is
at least 8.

Proof. A code0 point is always a residual endpoint, since its old cell has
a neighbor and code0 is disjoint from every partner code. Counting request
incidences gives

    b1+b2 = 20-u+q,
    r >= u = 20-b1-b2+q.                      (2)

Call a point noneligible when it is not an endpoint of the relaxed graph.
A code-j point, for j equal to the singleton code 1 or 2, is noneligible
only if EVERY point in its neighboring cells belongs to request j.
This uses actual positive support and has no minimum positive mass.

Each triple cell T_i has neighbor mass 3+1+6=10. Since b_j<8, no singleton-
coded point of a T cell can be noneligible. The four C cells contribute
at most four to the noneligible mass of singleton-coded points.

Fix one request j and consider double cells containing positive mass of
noneligible code-j points. We claim their total such mass is at most two.

* If there is only one such cell, its whole mass is two.
* Two complementary such cells require both B cells (mass four) and all
  four T cells (mass four) inside request j, contradicting b_j<8.
* Two distinct noncomplementary such cells correspond to two incident
  edges of K4. Their neighbor cells require their two complementary B
  cells (mass four) and the three corresponding T cells (mass three),
  a disjoint baseline mass seven in request j. The noneligible code-j
  points of the two chosen B cells are disjoint from this baseline and
  also belong to request j. Their total is therefore at most b_j-7<1.
* Three or more such cells require at least three distinct complementary
  B cells (mass six) and at least three distinct T cells (mass three),
  already exceeding the budget. Thus this case is impossible.

This proves the claim. Summing over the two requests, at most four units
of double-cell mass can be noneligible with singleton codes. Together
with the four C cells, at most eight units of singleton-coded mass are
noneligible. Code12 contributes at most q further units; code0 contributes
none. Therefore

    r >= 20-(8+q) = 12-q.                     (3)

The average of the right sides of (2) and (3) is exactly the right side
of (1). This proves (1) and its stated consequences. No integrality,
symmetry assumption on the allocation, or finite cell-size threshold
was used.

The bound is for the relaxed endpoint-count certificate. Actual responses
may destroy further pairs; their ranks or other global family constraints
could force that extra destruction. Consequently this obstruction does
not rule out adaptive or rank-sensitive arguments, and it does not
construct a high-transversal (7,2) family. The original six displayed
rows alone have transversal number two.

## Bounded discovery and exact upper check

`work/p644_twenty_triples_two_request.py` uses 56 mass variables, 56 support
binaries, 56 endpoint-mass variables and a maximum-cost variable. It
imposes x_(M,C)<=w_M z_(M,C) and, for every compatible partner (N,D),

    r_(M,C) >= x_(M,C)-w_M(1-z_(N,D)).

The only support link is the upper implication x>0 implies z=1; no positive
lower cutoff is imposed. The single bounded run reported objective 28/3
and a matching numerical dual bound. This numerical optimality claim is
NOT promoted to a theorem.

The discovered allocation was recovered with exact thirds and independently
checked by the standard-library script

    python3 work/p644_twenty_triples_two_request_check.py

The upper allocation at 28/3 is marked [C], with this script as its exact
certificate checker. It verifies every cell total, enumerates compatible positive-support pairs
exactly, and obtains b1=b2=r=28/3. Its certificate is saved as
`outputs/agent_twenty_triples_two_request_exact.json`; the discovery output
is `outputs/agent_twenty_triples_two_request_discovery.json`.

Thus the exact proven interval for the optimum of this particular scheme
is [8,28/3]. Equality with the numerically suggested 28/3 is unproved and
is not needed to exclude the requested 15/2 target.

The earlier report's reference to Section 7.97 has also been corrected:
5/7 there is a LOWER construction in the disjoint-edge case. The general
three-quarter upper bound for that case remains unproved.

## Separate complete-bipartite obstruction

For the indexed witness A,A,A,B,B,B with disjoint k-sets A,B, any four
retained occurrences include both sets and have pair graph K_(k,k).
If b1,b2<k, a noneligible singleton-code-j point would require the entire
opposite side inside request j, costing at least k. Code0 is always
eligible. Hence only code12 points can be noneligible, and their total
mass is at most min(b1,b2). Therefore

    r >= 2k-min(b1,b2) > k.

Thus this particular relaxed two-request endpoint scheme cannot certify
ANY coefficient below one from that witness. This is a limitation of the
rank-only allocation scheme, not an upper or lower conclusion about tau
of an ambient (7,2) family.
