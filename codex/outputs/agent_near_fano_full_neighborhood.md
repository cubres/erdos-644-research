# Full five-row neighborhood profile of the symmetric near-Fano defect state

Status: exact computer-assisted finite support calculation [C], with an
analytic reduction that includes all continuous partial type masses.
The result is a method obstruction at the fixed ratio a=33b, not a
high-transversal counterexample and not a general upper bound.

## 1. Result and scope

Use the 35 complementary types from
`agent_quantitative_width_six_excess.md`: a copies of each Fano line
type and b copies of each line-plus-one-point type, with a=33b. The
six fixed actual rows omit coordinate 0. Their endpoint count and pair
count are

    p=111b, Q=3669b^2.

Retain any five of these six rows and let K be their piercing graph.
Then |P5|=185b, so the strict neighborhood criterion of Section 7.93
requires a set S with mass greater than 74b.

[C] The complete neighborhood optimization has the following exact values:

- Among all continuous partial subsets S of mass at least 74b, the
  minimum closed-neighborhood mass is 111b.
- With the strict continuous requirement mass(S)>74b, every closed
  neighborhood has mass greater than 111b; the infimum is 111b.
- For integer b>=1 and actual point subsets, the strict requirement is
  |S|>=74b+1. The exact minimum is 111b+1.

Thus the full neighborhood profile does not improve on the existing
endpoint cover of size p. In the seven-row example the rank is
k=144b+1, and 3k/4=108b+3/4. The profile misses that target by a
positive linear amount.

All six choices of the omitted witness row are isomorphic: the Fano
automorphisms fixing coordinate 0 act transitively on the other six
coordinates, and the assigned type weights are invariant under these
automorphisms. No claim is made for ratios a/b other than 33.

## 2. The exact graph and the reduction for partial masses

Omit coordinate 1 as well as coordinate 0, leaving row coordinates
2,...,6. Merge point classes having the same five-row membership mask.
There are 17 positive endpoint types. Their weights, divided by b, are:

| Mask | Weight/b |
|---|---:|
|00011|2|
|00101|2|
|00110|1|
|00111|34|
|01001|2|
|01010|1|
|01011|34|
|01110|1|
|10001|2|
|10100|1|
|10101|34|
|10110|1|
|11000|1|
|11001|34|
|11010|1|
|11100|1|
|11110|33|

Two types are adjacent precisely when their bitwise union is 11111.
There are no loops or edges inside a type, since no type has mask 11111.
Points outside P5 can be excluded from S: they are not in the domain of
the neighborhood criterion and cannot improve its objective.

For a selected subset S, let Z be the set of types where its selected
mass is positive, and let N(Z) be the open type neighborhood. Every
point of every type in N(Z) belongs to the closed neighborhood of S.
The only further cost is the mass selected from Z outside N(Z).
Writing w for type mass, selection of at least h points therefore costs
at least

    w(N(Z)) + max(0, h-w(Z intersect N(Z))).             (1)

It is infeasible if w(Z)<h. This reduction does not require selecting
whole types: the free selected mass inside N(Z) and the paid mass
outside it are continuous variables. Filling the free mass first and
then the paid mass attains the expression if zero selections in an
activated type are allowed; such zero selections can only overcount
the declared neighborhood. More directly, enumerating all true supports
proves the lower bound, and the actual partial witnesses below prove
attainment. No minimum positive occupancy is imposed.

## 3. The exhaustive exact certificate

The script

    python3 -S work/p644_near_fano_neighborhood_exact.py

generates the 35 original types, merges them into the 17 graph types,
and checks all 2^17=131072 supports using integer arithmetic. It uses
no optimizer and no floating-point comparisons.

For the weak requirement h=74b, it checks (1) on all 98126 supports
of capacity at least 74b and proves the lower bound 111b.

For h=74b+1, a support has sufficient integer capacity precisely when
its capacity coefficient is at least 75. There are 92846 such supports.
Write n=w(N(Z))/b and i=w(Z intersect N(Z))/b. The script checks:

    if i<=74, then n+74-i>=111;
    if i>=75, then n>=112.

The first case makes (1) at least 111b+1. The second makes it at
least 112b, which is at least 111b+1 for every integer b>=1.
These inequalities also show that a strict continuous selection has
closed-neighborhood mass strictly greater than 111b: in the first
case the positive threshold margin is retained, while the second
has an entire b unit of extra cost.

The exact result and the witness vector are saved in
`outputs/agent_near_fano_neighborhood_exact.json`. The script completed
with EXACT_PASS. The earlier MILP was only a discovery tool; its
reported optimality is not used in this certificate.

## 4. Actual partial witnesses

Select the following numbers of points; leave all other types unselected:

| Mask | Strict integer selection |
|---|---:|
|00011|b+1|
|00101|b|
|00110|b|
|00111|34b|
|01001|b|
|10001|b|
|11000|b|
|11001|34b|

All capacities are respected for every b>=1, including b+1<=2b.
The selected set has size 74b+1. Its open neighborhood has mass
107b. The selected points outside that open neighborhood occupy
00011,00101,01001,10001, with total mass 4b+1. Hence its closed
neighborhood has size 111b+1 exactly. By Section 7.93, this is an
actual global transversal whenever the six original rows attain the
global endpoint minimum p.

Replacing b+1 by b in type 00011 gives an actual weak-threshold
selection of size 74b and a closed neighborhood of size 111b. In
the continuous formulation replacing b+1 by b+epsilon, with
0<epsilon<=b, gives size 74b+epsilon and closed-neighborhood size
111b+epsilon, proving the asserted strict infimum.

## 5. The stronger pair-count tie criterion cannot give a cheaper cover either

For an arbitrary candidate point set D, let K_D consist of the edges
of K having at least one endpoint outside D. If an actual replacement
row G avoids D, its piercing graph with the five retained rows is
a subgraph of K_D. Consequently, if the endpoint/pair-count pair
of K_D is lexicographically below (p,Q), then D is a global
transversal under the joint minimum hypothesis.

The weak-threshold lower bound above applies to this stronger test,
including candidate sets D which were not constructed as closed
neighborhoods. Let S be the vertices of P5 isolated in K_D. Each
such vertex belongs to D, and every one of its original neighbors
belongs to D. Therefore

    N_K[S] subset D.

If K_D has at most p endpoints, then |S|>=|P5|-p=74b. The exact
weak lower bound gives |D|>=|N_K[S]|>=111b=p. Thus no candidate
set D of size less than p can pass this stronger criterion, whether
it relies on strict endpoint loss or on a pair-count decrease at
equal endpoint count. This includes arbitrary partial type masses.

For completeness, the displayed weak optimal witness has exactly
111b endpoints remaining in K_D but 3740b^2 remaining pairs, which
exceeds Q=3669b^2. That particular equality witness therefore does
not pass the pair tie test. The lower-bound conclusion does not
require classifying which other sets of size exactly p might pass.

## 6. What this rules out and what it leaves open

At this fixed near-Fano support, the full five-row closed-neighborhood
profile and the stronger pair-count tie criterion cannot by themselves
produce a transversal below p=111b. This is an exact finite method
barrier with continuous partial masses included.

The concrete seven-row family still has transversal number two. The
calculation does not assert the existence of any high-transversal
extension, and does not obstruct later tuples containing newly
obtained actual rows. A successful global argument must use such
additional consistency or a different cover certificate; optimizing
the present five-row graphs more finely cannot close the gap.
