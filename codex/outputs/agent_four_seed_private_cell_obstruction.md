# Private cells obstruct the three-bin completion even below sum 5/4

Status: **hand proved**, following a numerical discovery. This is a barrier
for a fixed four-row completion, not a counterexample to property (7,2) at
large transversal number.

Normalize rank to one. Start with a good triple, and index its disjoint pair
cores by Xi=Aj intersection Ak. Take their sizes to be
\[
 (a_0,a_1,a_2)=(49/100,49/100,24/100).
\]
The three private parts then have sizes (27/100,27/100,2/100).
Take a fourth actual row D with
\[
 x_i=|D\cap X_i|=(1/4,1/4,0),\qquad
 y_i=|D\cap\text{private}(A_i)|=(1/4,1/4,0).
\]
These numbers specify four rank-one rows. The initial good-triple sum is
61/50=1.22. The only other good triple among the four has sum 31/25=1.24,
so all minimum-sum inequalities visible on these four rows hold.

The active Venn cells of their two-transversal graph have weights
\[
 T_0=T_1=Y_0=Y_1=1/4,\quad Z_0=Z_1=Z_2=6/25,\quad
 S_0=S_1=1/50.
\]
The remaining private cell S2 is isolated in this graph and is irrelevant.
There is an edge between T0 and T1, a common neighbor Z2, the two paths
\[
 T_0-Y_0-Z_0-T_1,\qquad T_0-Z_1-Y_1-T_1,
\]
and the leaves S0 adjacent to T0 and S1 adjacent to T1.
Adjacency means that **every** pair of points from the two indicated cells
is a two-transversal of the four rows.

Let q be the smallest possible maximum size of three point sets whose
induced complete graphs cover every such pair. Arbitrary splitting of every
cell between bin-membership patterns is allowed. Then exactly
\[
 q=137/150>3/4.
\]

## Lower bound, including arbitrary splitting

If q is at least 49/50, the desired lower bound already holds. Suppose q is
smaller than 49/50. A point of T0 that belongs to only one bin would force
that bin to contain **all** its neighboring cells T1,Z1,Z2,Y0,S0. Their
total weight is one, already larger than q. The same holds for T1.
Consequently every point in T0 and T1 belongs to at least two bins.
(Even omitting the private leaf gives neighboring weight 49/50.)

If both Y0 and Z0 have points belonging to just one bin, their singleton
bins must be the same, since the two cells are adjacent. That bin must then
contain all four cells T0,T1,Y0,Z0, of total weight 99/100, again larger
than q. Thus at least one of Y0,Z0 has every point in at least two bins.
The same argument applies to Y1,Z1. Each of these two compulsory duplicated
cells has weight at least 6/25.

All active points have total weight 44/25. Counting their bin memberships
therefore gives
\[
 3q\ge 44/25+1/2+2(6/25)=137/50,
\]
which proves q at least 137/150.

## Matching upper bound

Split each Zi for i=0,1 into a part Zi' of size 13/75 and a part Zi'' of
size 1/15. The following three bins cover all graph edges:
\[
 \begin{aligned}
 B_1&=T_1\cup Y_1\cup Z_0'\cup Z_1,\\
 B_2&=T_0\cup Y_0\cup Z_0\cup Z_1',\\
 B_3&=T_0\cup T_1\cup Z_2\cup S_0\cup S_1
       \cup Z_0''\cup Z_1''.
 \end{aligned}
\]
Each has size 137/150. All quantities scale to ordinary finite sets, for
example at rank 300m.

At the boundary a=(1/2,1/2,1/4), with the same x,y, the private leaves
vanish and every active cell has size 1/4. The same argument gives the exact
value q=11/12. For the matching upper bound use the same bins, splitting
Z0,Z1 into parts 1/6 and 1/12.

## What must change in a successful argument

Merely assuming S<5/4 and imposing every minimum-good-triple inequality
among the four rows does not force a three-bin completion at budget 3/4.
The fourth row in this example is compatible with those conditions but has
a substantial completion obstruction. A global argument must choose a
different fourth row using further information, or obtain additional rows
and examine other seven-subfamilies. It cannot silently replace the actual
four-row graph by the three-sun graph obtained by dropping the private-trace
cells Yi.

Discovery scripts and logs are preserved in the research directory:
`p644_agent_audit_four_seed_bins.py`,
`logs/astra_agent_audit_four_seed_intermediate.json`, and
`logs/astra_agent_audit_four_seed_boundary.json`.
The script uses all seven nonempty memberships in three bins, has no
positive-mass cutoff, and records all four-row minimum-sum checks. Its
numerical conclusions have been replaced by the hand argument above.
