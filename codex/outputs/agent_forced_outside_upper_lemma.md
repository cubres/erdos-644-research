# A forced outside-mass lemma for paired-Q minimization

This is a conditional **hand-proved upper-bound lemma**, not a resolution
of Erdős 644. All pairs mentioned below are actual disjoint pairs of
edges. The family is k-uniform and has property (7,2). We assume its
minimum piercing-pair count among triples of disjoint pairs is at least
`c k^2`. This assumption applies when the selected original paired
six-tuple globally minimizes that count and has count `c k^2`.

## 1. The four-quadrant lemma

Suppose two complementary edge pairs partition a set U of size 2k into
four quadrants U00,U01,U10,U11 of size k/2 each. Let D be a set of size
3k/4 whose deletion leaves capacities

\[
 (|U_{00}\setminus D|,|U_{01}\setminus D|,
   |U_{10}\setminus D|,|U_{11}\setminus D|)
 =(k/2,k/8,k/8,k/2).
\]

Take any actual edge R avoiding D and any actual edge S disjoint from R.
The latter exists under the separate hypothesis that every edge has a
disjoint partner. Write `h=|R\setminus U|/k`. If `0<=h<=1/8`, then the
six-row piercing-pair count satisfies

\[
 \boxed{Q(U_{0*},U_{1*},U_{*0},U_{*1},R,S)
          \le (7/32+3h/8)k^2.}
\]

The bound permits arbitrary points of S outside U.

**Proof.** Normalize k=1. Write the four R masses as a,b,e,d, so
`a,d<=1/2`, `b,e<=1/8`, and `a+b+e+d=1-h`. Write the four S masses as
`s_i<=1/2-r_i`; their sum is at most 1. Set the unused capacities to
`l_i=1/2-r_i-s_i`. They are nonnegative and have total at least h.
Every pair piercing the first four rows consists of points in opposite
quadrants. Therefore

\[
 Q=\tfrac12(1-h)-2(ad+be)-\sum_i r_{\bar i}l_i
 \le\tfrac12(1-h)-2(ad+be)-h\min(a,b,e,d).
\]

Because h<=1/8, both a,d are at least `1/4-h>=1/8`, so the minimum is
`min(b,e)`. Interchange the middle quadrants if necessary and take b<=e.
Since a+d=1-h-b-e and a,d<=1/2, we have

\[
 ad\ge\tfrac12(\tfrac12-h-b-e).
\]

It follows that

\[
 Q\le h/2+b+e-2be-hb.
\]

The right side is increasing in b,e throughout `0<=b<=e<=1/8` and
`0<=h<=1/8`: its partial derivatives are `1-2e-h>=5/8` and
`1-2b>=3/4`. Substituting b=e=1/8 gives `7/32+3h/8`, as required.

Equality in this four-quadrant optimization is possible. For example,
take R masses `(1/2,1/8,1/8,1/4-h)` and S masses
`(0,3/8-h,3/8,1/4+h)`. Thus the coefficient 3/8 cannot be improved
using only the four-quadrant capacities and the two rank constraints.

**Corollary.** If `7/32<c<=17/64`, global paired-Q minimality forces

\[
 |R\setminus U|\ge\tfrac83(c-7/32)k.
\]

Indeed, the displayed bound gives this when h<=1/8, and when h>1/8
the conclusion is automatic in the stated c interval. At c=6/25,

\[
 \boxed{|R\setminus U|\ge17k/300.}
\]

If one works with rank at most k instead of uniform rank, the same proof
controls `1-|R\cap U|/k`; interpreting this deficiency as actual outside
mass requires the stated uniformity assumption.

## 2. Application to the explicit low-c refinement state

In the six-pair construction in `agent_paired_refinement_survivors.md`,
let A=000, B=011, C=100, D0=101, E=110, F=111. The first two old cuts
have quadrants A, B, C union D0, E union F, all of size 1/2. For every
`1/8<=c<1/4`, delete

\[
 \mathcal D=D_0\cup C_{H,K}\cup(B\setminus B_{G,J}).
\]

Its size is `(1/2-c)+(c-1/8)+3/8=3/4`. The residual quadrant capacities
are precisely those in the lemma. Hence in a hypothetical ambient
family with `tau>3k/4`, an actual avoiding response exists. Under the
no-isolated-disjointness and global paired-Q assumptions, this response
has the forced outside mass just proved.

This deletion was discovered after two further particular responses,
but its expression shows it is already available in the twelve-row
state. No claim is made that the preceding chosen responses are forced
in an arbitrary family.

## 3. Constraints available for an arbitrary next partner

For every old pair of complementary cuts i,j, the next actual disjoint
pair R,S must satisfy

\[
 Q_{ij}(R,S)=\sum_{x,y:\,x_i\ne y_i,\ x_j\ne y_j}r_xs_y\ge ck^2.
\]

Here x,y run over occupied old atom types; their masses obey
`r_x+s_x<=w_x`, `sum r_x<=k`, `sum s_x<=k`, and `r_x=0` on the deletion.
Points outside the old U do not contribute to these Q counts. One can
therefore optimize this system while permitting both rows arbitrary
outside mass; assuming S is the complement of R would be invalid.

Additional necessary conditions, not included in this displayed system,
are that every seven actual rows are two-pierceable and that the endpoint
set of every six actual rows has size at least the ambient transversal
number. Both apply to unpaired selections as well.

## 4. The exact finite state and the remaining link

At c=6/25, the particular sixteen-row state saved in
`agent_global_eight_pair_mixed_survivor.json` has minimum six-row endpoint
mass 7/8. Its minimizing six-tuple is rows 1,3,7,11,14,15. Deleting its
endpoint set except one B subcell of mass 1/8 gives the same request
above. The state and its exact row checks are computational facts [C],
separate from the universal conditional hand lemma.

A numerical nonconvex search found a local maximum minimum value about
0.23906471317, below 6/25. This was **not** an upper-bound certificate.
Its locally active comparisons are 12,24,26,34,36. The subsystem
containing only those comparisons admits a different, higher branch,
so they alone do not prove impossibility. Further comparisons are
necessary. The full relevant system now has the exact certificate below.

## 5. A forbidden five-pair pattern [C]

At c=6/25, suppose five actual complementary pairs on U have the
following ten occupied types and masses. A bit records membership in
the corresponding member of its pair. Column labels are arbitrary;
the historical labels were 1,2,3,4,6.

| Type | Mass |
|---|---:|
| 00001 | 1/4 |
| 00010 | 1/4 |
| 01100 | 1/4 |
| 01111 | 1/4 |
| 10011 | 6/25 |
| 11111 | 6/25 |
| 10100 | 1/4 |
| 10111 | 1/100 |
| 11000 | 1/4 |
| 11011 | 1/100 |

Assume every family edge has a disjoint partner and every triple of
actual disjoint pairs has at least `(6/25)k^2` piercing pairs. Then
`tau<=3k/4`, with the integer interpretation obtained by taking common
scales of the stated rational masses.

**Reduction to the certificate.** If tau>3k/4, choose R avoiding all
101 points, all 011 points except a chosen k/8-subset of type 01100,
and all 10011 points except a chosen k/8-subset. This deletes exactly
3k/4 points. In the table order, the only possible old R traces have
indices `0,1,2,4,5,8,9` and upper bounds

\[
 (1/4,1/4,1/8,1/8,6/25,1/4,1/100).
\]

Let S be any actual disjoint partner of R. Set r_i,s_j to the old atom
masses. They satisfy `sum r<=1`, `sum s<=1`, `r_i+s_i<=w_i`, and all
stated nonnegative capacity bounds. No assumption about their outside
points is made. For each of the ten pairs of old coordinates a,b,

\[
 Q_{ab}(R,S)=\sum_{i,j:\ T_i(a)\ne T_j(a),\ T_i(b)\ne T_j(b)}r_i s_j.
\]

Every one of these ten quantities must be at least 6/25. The rational
certificate proves that no such r,s exist. These five pairs are ten
actual rows; the earlier twelve-row construction contains an additional
pair which is not used anywhere in this theorem.

**Certificate details.** `work/p644_agent_global_outside_certificate.py`
produces `outputs/agent_global_outside_certificate.json`. There are
219 nodes: 109 binary splits and 110 closed leaf boxes. Every leaf
uses a linear relaxation with product variables p_ij for r_i s_j,
the four McCormick inequalities at that box's rational endpoints,
both product-rank inequalities, all ten Q inequalities, and the rank
and disjointness capacities above. There is no positive support cutoff.

The exact dual bound at a leaf is checked by the following elementary
inequality. For `Ax<=b`, rational nonnegative multipliers y, finite
variable bounds l,u, and `d=e_t-A^T y`,

\[
 t\le y\cdot b+\sum_j\max(d_jl_j,d_ju_j).
\]

Every exported leaf bound is strictly below 6/25. Their maximum is
approximately 0.23999815858783147, leaving a rational strict margin
greater than 0.00000184. Floating-point optimization selects a branch
and dual proposal only; Fraction arithmetic verifies the exported
inequalities. Independent standard-library reconstruction **passed**:
`work/p644_agent_audit_outside_certificate_check.py`, with output
`outputs/agent_audit_outside_certificate_check.json`. It independently
rebuilds all 316 inequalities, 88 finite variable bounds, the complete
closed-box cover, and every rational leaf inequality. Every leaf is
also strictly below the simpler rational number `239999/1000000`.

**Scope.** This excludes the displayed regular G/H refinement followed
by an exact A-flip pair. It does not prove that an arbitrary first or
second response must have this pattern. The next response probe has
explicit distant alternatives, recorded separately. Thus the new
certificate is a conditional upper-bound lemma, not an improved global
coefficient for Erdős 644.

The certificate also gives a small rigorous parameter neighborhood
without further optimization. It applies for
`|c-6/25|<=1/4000000`. To see this, reduce any old R,S traces at parameter
c to fit the atom capacities at 6/25. Only two atom capacities have
increased, so the total mass removed from R and S together is at most
`2|c-6/25|`. Every Q decreases by at most that amount, since both row
traces have size at most 1. Thus all Q values would remain at least
`c-2|c-6/25|>=6/25-3/4000000`, which is strictly larger than the
independently certified upper bound `239999/1000000`. This is a
stability statement for this particular five-pair pattern.

## 6. A distant response to the preceding request

Starting with only the original three pairs and the regular G/H pair,
the request `A_G union C union F union H(D0 union E)` has size 3/4.
The A-flip response is not forced. Another actual response state is

\[
 L=B\cup (D_0\cap G)\cup(E\cap G),\qquad M=U\setminus L.
\]

This changes k/2 points in symmetric difference from the A-flip edge.
The six new paired-Q counts, for old pairs 12,13,14,23,24,34, are

\[
 (1/4,1/4,1/4,3/8,3/8,3/8).
\]

They all exceed c=6/25. The ten rows share a piercing pair with one
point in B_G and the other in C, so every seven-row property holds.
The minimum unpaired six-row endpoint mass is 1 [C]; one minimizing
tuple has pair graph

\[
 \boxed{B\times(C\cup D_0),}
\]

whose sides each have size 1/2. Thus neither Q minimality nor all the
seven-row and endpoint-size constraints forces the A-flip pattern.
This is a local response obstruction; the finite displayed family has
transversal number 2, not a large transversal number.

`work/p644_agent_global_regular_response_alternatives.py` checks this
state and two further extreme alternatives exactly, saving their
profiles in `outputs/agent_global_regular_response_alternatives.json`.
The next globally required response can be directed at this new
biclique endpoint set. Its analysis is separate from the certified
forbidden A-flip pattern.

## 7. A genuine outside continuation of the distant state [C]

For the distant state in Section 6, request an edge R avoiding
`(C union D0) union B_G`, of total size 3/4. This deletes a whole side
of its six-row biclique and a quarter of the other side. The following
exact response and disjoint partner S survive. Columns give masses
inside the indicated old class.

| Old class | R | S |
|---|---:|---:|
| A_G | 21/100 | 1/25 |
| A_H | 1/4 | 0 |
| B_G | 0 | 1/4 |
| B_H | 1/4 | 0 |
| C | 0 | 23/200 |
| F | 2/25 | 4/25 |
| D_G | 0 | 1/4 |
| D_H | 0 | 1/100 |
| E_G | 3/40 | 7/40 |
| E_H | 1/100 | 0 |
| Outside U | 1/8 | 0 |

The outside part is new and belongs only to R in this finite state.
Each row has rank 1, the two rows are disjoint, and R avoids the
request. Every new distinct paired Q is at least
`9913/40000=0.247825>6/25`. The only disjoint pairs in the resulting
twelve-row family are the six designated ones. All 792 seven-row
subfamilies are two-pierceable, and the minimum endpoint mass over
all six-row selections is `183/200=0.915`, attained by rows
`2,3,4,6,9,11` (two consecutive rows per designated pair).

The exact standard-library checker is
`work/p644_agent_global_distant_outside_survivor.py`; its output is
`outputs/agent_global_distant_outside_survivor.json`. It stores the
minimizing six-row pair graph and all rational masses. The finite
family has transversal number 3. Thus this particular next request
does not close the distant branch. A further argument must use a
new globally required response or another global family condition;
the existence of these twelve rows alone is compatible with every
finite constraint listed above.

## 8. One targeted step using the entire known outside part [C]

Let R0,S0 be the two rows from Section 7, and write
`O=R0\setminus U`, so |O|=1/8. The smallest six-row endpoint graph
there has B_H intersect R0 as a class X of mass 1/4, whose neighborhood
is exactly `Y=C union D0`, of mass 1/2. Make the single request

\[
 \mathcal D=O\cup Y\cup X',\qquad
 X'\subseteq X,\quad |X'|=1/8.
\]

The cost is `1/8+1/2+1/8=3/4`. Thus it uses the entire known outside
part, an entire endpoint neighborhood, and half its central class.

This request has an exact surviving transition. The new edge R1 has
the following masses on the fifteen old atoms listed in the Section 7
JSON, in that order:

\[
 (21/100,1/25,1/5,31/200,1/8,0,0,2/25,0,0,0,
   3/40,21/200,1/100,0).
\]

The named half X' can be chosen as the half avoided by R1; all points
of X have the same old row type. Set `S1=U\setminus R1`. Both new
edges have rank 1 and lie entirely in U, so they avoid the old outside
part. R1 avoids the whole request. Its partner is one allowed response
from the unrestricted class of disjoint partners; no complementary
restriction was imposed on the existence problem.

Every new distinct paired Q is at least `257/1000=0.257`, all 3,432
seven-row subfamilies are two-pierceable, and the minimum endpoint
mass over all six-row selections remains `183/200`. The minimizing
six rows remain `2,3,4,6,9,11`. The only disjoint pairs are the seven
designated ones, so the check of all their triples does cover every
actual disjoint-pair triple in this finite family. Its transversal
number is exactly 3.

The checker is `work/p644_agent_global_outside_control_survivor.py`,
using the general exact row-mask checker
`work/p644_agent_global_mask_check.py`. Data and the full minimizing
endpoint graph are saved in
`outputs/agent_global_outside_control_survivor.json`.

This is a precise obstruction to this particular outside-control
request: the response can return to U while retaining the old minimum
paired Q and the old minimum six-row endpoint mass. It is not a claim
of survival against every request. No broad deletion menu or further
response tree is inferred from this one transition.
