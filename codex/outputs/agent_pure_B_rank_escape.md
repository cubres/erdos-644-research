# Pure-B incidence losses: an exact triangle criterion and a sharp table barrier

Status: hand proofs with an exact finite type-table checker. The general
pure-B 3/4 statement remains unproved. This report gives a conditional
bound for the actual witness profile of Section7.157 and identifies precisely
why the standard three-request triangle table stops short of 3/4 there.
It is a barrier for the specified request table, not for arbitrary requests
or for the Erdős conjecture. No main-note edits were made.

## 1. The weighted triangle table, including singleton incidence losses

Retain three actual rows with empty common intersection. Suppose their
nonzero cells have only singleton and doubleton types. Write s_i for the
mass of singleton i and m_ij for the mass of doubleton ij, for i,j in
{1,2,3}. All masses are nonnegative integers. Points of type zero do not
participate in transversal pairs of these three rows.

Split doubleton ij into a heavy piece of size h_ij and a light piece
of size m_ij-h_ij. Put its heavy piece in requests D_i and D_j, and its
light piece in the remaining request D_l. Split singleton i arbitrarily
between requests D_j and D_l, with j,l distinct from i. Let u_ij be the
number of singleton-i points assigned to D_j. Thus

    u_ij >= 0,  u_ii=0,  sum_j u_ij=s_i.

Every heavy doubleton point is isolated in the residual pair graph: its
neighbors are points of the other two doubletons and its complementary
singleton, whose request codes all overlap its own two-bit request code.
Consequently, with H=sum h_ij and S=sum s_i, the residual endpoint count
is at most

    R = sum m_ij - H + S.                         (1)

If all three light pieces are nonempty, equality holds. Distinct light
doubleton classes remain mutually adjacent, and every singleton point
remains adjacent to its complementary light doubleton. This last fact is
why simply charging singleton losses to existing row ranks is insufficient.

The request associated with row i has size

    |D_i| = H + m_jl - 2h_jl + sum_{r != i} u_ri,  (2)

where {i,j,l}={1,2,3}. In particular,

    sum_i |D_i| = H + sum m_ij + S.               (3)

These formulas yield an exact small flow criterion for the table. Given
integer h_ij between zero and m_ij and an integer request budget T, put

    c_i = T - (H+m_jl-2h_jl).

The singleton assignment exists if and only if

    c_i >= 0 for every i,
    S <= c_1+c_2+c_3,
    s_i <= sum_{j != i} c_j for every i.           (4)

Proof: send the s_i singleton points to the two request bins other than
i, with capacities c_j. The displayed inequalities are exactly the
capacitated Hall conditions. A single source has the last capacity
condition; any two or three distinct sources have all three bins as
their joint neighborhood. Integral max flow gives an integer assignment.

If every actual subfamily of at most six rows has at least p endpoints,
conditions (4) together with R<p imply tau(H)<=T. Otherwise actual
responses avoiding the three requests exist; together with the retained
rows they have fewer than p endpoints. Arbitrary outside points in the
responses do not affect this conclusion, because the three retained
rows have empty common intersection. Coincident responses are harmless
under the at-most-six convention.

## 2. The concrete pure-B profile from Section7.157

For an integer b>=1, the six actual rows have these cells:

| Six-row type | Mass |
|---|---:|
|1234, 1256, 3456|37b each|
|135|30b+2|
|35, 15, 13|2b-1 each|
|146|32b|
|16, 14|2b each|
|236|34b|
|36|2b|
|245|36b|

All other points have zero membership in these six rows. Every row has
rank 144b. The four containing A stars are 135,146,236,245. Their host
sizes are 36b-1,36b,36b,36b, respectively, and every A point has degree
at least two. The six-row endpoint set consists exactly of the three
four-type B classes, of total size 111b.

Retain rows 2,3,5, in that order. Their singleton and doubleton masses are

    (s1,s2,s3) = (0,4b-1,2b-1),
    (m12,m13,m23) = (71b,73b,69b+1).

Choose

    (h12,h13,h23) = (35b,36b,37b),

and assign both singleton classes to request D1. The resulting requests
have exact sizes

    (|D1|,|D2|,|D3|) = (109b-1,109b,109b).

All light pieces are positive. Equation (1) gives the exact residual
endpoint count 111b-1. Therefore:

**Conditional theorem.** If a rank-at-most-k (7,2)-family contains these
six actual rows and its global endpoint minimum over at most six rows
is 111b, then

    tau(H) <= 109b.                               (5)

No criticality, saturated-family hypothesis, or assumption about the
response ranks beyond belonging to the actual family is needed. For the
Section7.157 ambient rank k=144b+1, (5) still exceeds the desired
ceil(3k/4)=108b+1 when b>=2.

## 3. Exact obstruction for all four triangles in this table family

The four K4 triangles avoiding common A-star points are 235,145,136,246.
Write D for their total A-doubleton mass and S for their A-singleton
mass, and M=D+S. Each of the first three triangles has

    M=108b-1,  sum m_ij=213b+1,
    min m_ij=69b+1.

The fourth has

    M=108b,  sum m_ij=213b,  min m_ij=69b.

These identities follow either by projection of the displayed type table
or because a triangle meets every degree-at-least-two point in its three
incident star hosts and misses the fourth host.

Consider ANY choice of heavy sizes and ANY singleton splitting allowed
by Section1. Suppose all three request sizes are less than 109b. No
light doubleton can be empty. Indeed, if h_ij=m_ij, then the two
requests containing that heavy piece have combined size at least

    sum m_rs + m_ij >= 282b.

This follows directly by adding their instances of (2); all singleton
contributions are nonnegative. But two budgets below 109b have sum
below 218b, a contradiction.

Thus all light pieces are positive, so the residual endpoint count in
(1) is exact. To make it strictly less than p=111b=3a, a=37b, one needs

    H > D+S = M.

Equation (3) now gives

    sum_i |D_i| > 3a+2M >= 327b-2.

For integer request sizes the sum is at least 327b-1, so some request
has size at least 109b. This contradicts the assumed smaller budget.
Section2 attains 109b, proving that the exact optimum over this table
family and all four triangles is

    T_table = 109b.                               (6)

In particular, simply using the actual ranks to optimize the singleton
allocation in this triangle table cannot prove the desired 3/4 bound
on the Section7.157 profile. The obstruction is a linear b-sized gap,
even though the six actual rows each have rank only 144b.

This result does not rule out other request codes, retaining four or
five old rows, adaptive requests using responses, exploiting an actual
critical edge, or the general pure-B theorem. The precise open step
remains to exploit the degree-two incidence losses by a method outside
the table whose optimum is computed here.

## 4. Verification

Run `python3 work/p644_pure_B_rank_escape_check.py`. The checker uses
integer coefficient pairs for affine functions of b. It verifies every
row rank, six-row endpoint support, all four triangle projections, the
explicit request sizes, and the exact residual support. No numerical
solver is required for the theorem or its barrier.

A single separate unrestricted numerical discovery run at b=10 also
returned 1089 2/3 for a residual target 1109. Its output is retained in
`outputs/agent_pure_B_triangle_discovery_10.0.json`. That numerical
optimality claim is not used as an exact certificate and is not promoted
to a lower bound for unrestricted request codes.
