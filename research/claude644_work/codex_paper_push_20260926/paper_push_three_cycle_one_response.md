# A one-response theorem for three minima whose arrows lie in a directed cycle

26 September 2026. Full hand proof, developed jointly with the parent. The first cyclic Fano construction needs an extra pencil condition; the second construction below repairs every failure of that condition. No numerical coverage assertion is used.

## Theorem and notation

Let x_A,x_B,x_C>=3/4. Suppose three actual unit types a,b,c have their respective own-coordinate loads s_A=a_A, s_B=b_B, s_C=c_C strictly greater than 2x_i/3. Put

    e_i=x_i-s_i,     E=e_A+e_B+e_C,     N=x_A+x_B+x_C.

Assume E>3/4 and each pair of the e_i sums to less than 3/4. Draw an arrow i->j, for i!=j, when type i has j-th trace greater than e_j.

If this directed graph is contained in a directed three-cycle, then every (7,2) type-closed superfamily containing a,b,c has continuous transversal coefficient at most 3/4. More precisely, the anchors either already admit a bad V4 tuple, or a single request of cost strictly less than 3/4 has a residual box all of whose unit responses give a bad Fano tuple with six anchor rows.

There is no upper bound on the capacities in this theorem. It applies to a directed three-cycle, a directed path, one arrow, or the empty graph. The remaining functional graphs have a two-cycle or a vertex with two incoming arrows.

After relabeling, containment in the directed cycle A->B->C->A means exactly

    a_C<=e_C,       b_A<=e_A,       c_B<=e_B.             (L)

The designated other cross traces a_B,b_C,c_A are allowed to be either above or below their target slacks.

## Structural inequality: at most one outgoing arrow

Own loads satisfy s_i>1/2, all cross traces are below 1/2, and 0<=e_i<s_i/2<=1/2. Define

    h_i=E+x_i-2e_i-1.

Then

    h_i > E+x_i/3-1 >= E-3/4 >0,

and the off-coordinate sum in row i is exactly

    1-s_i=e_j+e_k-h_i<e_j+e_k.                         (R)

Consequently each type has at most one cross trace exceeding its target slack. Thus every arrow graph under the theorem's numerical assumptions has outdegree at most one. This observation does not itself eliminate two-cycles or two incoming arrows.

## Case 1: all three single-own pencils fit

Suppose

    s_A+2c_A<=2x_A,
    s_B+2a_B<=2x_B,
    s_C+2b_C<=2x_C.                                    (Q)

Use the Fano lines in order

    012, 034, 056, 135, 146, 236, 245

and assign their row types

    (b,b,c,a,c,a,u).

The four pencils not involving u are

    2b+c, a+b+c, 2a+b, a+2c.

Each satisfies the coordinatewise capacity bound 2x. At the coordinate of the doubled type, its other cross trace is one of (L), so 2s_i+cross<=2s_i+e_i<=2x_i. At the coordinate of the singleton type, the required inequality is one of (Q). At the third coordinate there are two light cross traces and one trace below 1/2, so the load is at most 2e_i+1/2<2x_i. Finally, each coordinate of a+b+c is at most s_i+e_i+1/2=x_i+1/2<2x_i.

For each coordinate let L_i be its designated incoming trace (c_A,a_B,b_C), let m_i be the other cross trace, and put

    d_i=(L_i-e_i)_+,      r_i=x_i-d_i.

These are valid residual capacities: 0<r_i<=x_i. Every pair of anchor loads in coordinate i sums to at most 2x_i-r_i. Indeed the largest pair includes its own load s_i>1/2, and its largest cross trace is at most e_i+d_i. Hence every response u<=r satisfies the three remaining pencils, whose anchor pairs are a+b,b+c,c+a.

The seven-row total also fits. If L_i>e_i, its excess over 4x_i at u_i=r_i is the negative of

    s_i-L_i+2(e_i-m_i)>0.

If L_i<=e_i, both cross traces are at most e_i and

    4x_i-[2(s_i+L_i+m_i)+r_i]>=s_i-e_i>0.

Thus every unit response in the box r yields a bad Fano tuple.

The request costs D=sum d_i. If all three arrows are present, (R) gives

    D<=E-sum h_i=3-N<3/4,

because E<N/3 and E>3/4 imply N>9/4. If exactly two arrows are present, they form a directed path. Each arrow i->j has excess at most e_k-h_i, where k is the third coordinate; the two third coordinates are distinct. Their two slacks sum to less than 3/4, so D<3/4. With one arrow D<e_k<1/2, and with no arrows D=0.

If the superfamily had tau*>3/4, this request would have an admissible unit response, giving the bad tuple. This closes Case 1.

## Case 2: one of (Q) fails

Cyclically relabel so that

    2a_B+s_B>2x_B,  equivalently a_B>s_B/2+e_B.         (F)

This necessarily gives the arrow A->B. Since a_B<1/2 and s_B>1/2, we have e_B<1/4. Also the row sum of a and own heaviness give

    1>=s_A+a_B>2e_A+s_B/2+e_B>2e_A+2e_B.

Therefore

    e_A+e_B<1/2,     e_C>1/4,     e_A+e_C>1/2.          (S)

In particular,

    c_A<=1-s_C<1-2e_C<2e_A,
    b_C<1/2<s_C/2+e_C.                                (P)

### Case 2a: the return arrow C->A is present

Thus c_A>e_A. Assign the Fano rows

    (c,a,a,b,b,c,u)

to the same ordered seven lines. Its four anchor-only pencils are

    2a+c, 2b+c, a+b+c, a+b+c,

and its three response pencils have anchor pairs 2c,a+b,a+b.

The four anchor pencils fit. The two potentially new constraints are c_A<=2e_A and s_C+2b_C<=2x_C, supplied by (P). The other own/doubled-own constraints use (L). At any remaining coordinate, two cross loads below 1/2 plus a light cross load at most e_i are less than 1+e_i<2x_i, since s_i>1/2. The all-distinct pencil fits as in Case 1.

The exact maximal partner cap from these pencils and the total is

    r_i=min(x_i, 2x_i-2c_i, 2x_i-a_i-b_i,
            4x_i-2a_i-2b_i-2c_i).

Using (L), own loads greater than 1/2, and cross loads below 1/2, its request costs simplify to

    x_A-r_A=(2c_A-x_A)_+,
    x_B-r_B=a_B-e_B,
    x_C-r_C=s_C-e_C.                                  (D)

For completeness: at A, the a+b pair costs b_A-e_A<=0, and the total cost is at most 2c_A-x_A because b_A<=e_A. At B, the 2c constraint costs nothing and the total cost is below a_B-e_B because a_B<s_B and c_B<=e_B. At C, a_C+b_C<x_C because a_C<=e_C and b_C<s_C; the total cost is below s_C-e_C by the same inequality. All residual coordinates are positive: at A use c_A<1/2 and x_A>=3/4; at B use s_B>a_B; at C r_C=2e_C>1/2.

Let D be the sum in (D). If 2c_A<=x_A, substitute a_B=1-s_A-a_C and use c_A>e_A, which gives s_C<1-e_A-c_B. Then

    D=1-s_A-a_C+s_C-E+e_A
      <2-s_A-E-a_C-c_B<3/4.

If 2c_A>x_A, substitute also c_A=1-s_C-c_B. This gives

    D=3-2s_A-s_C-E-a_C-2c_B<3/4,

because 2s_A+s_C>3/2 and E>3/4. Thus the partner box again gives a single request of cost below 3/4 whose every response produces a bad Fano tuple.

### Case 2b: the return arrow C->A is absent

Now c_A<=e_A. We show a bad V4 tuple directly, with four a-rows, one b-row, and two c-rows. The V4 inequalities for this assignment are

    b+2c<=2x,       2a+2c<=2x,       4a+b+2c<=4x.      (V)

First a+c<=x: at A and C use c_A<=e_A and a_C<=e_C; at B use a_B<1/2<s_B and c_B<=e_B.

For b+2c, at A the load is at most 3e_A<2x_A; at B it is at most s_B+2e_B<2x_B; at C it is below 2s_C+1/2<2s_C+2e_C=2x_C by e_C>1/4.

For the total, the A-coordinate is at most 4s_A+3e_A<4x_A. At B,

    4a_B+s_B+2c_B<2+s_B+2e_B=2+x_B+e_B<4x_B,

because e_B<1/4 and x_B>=3/4. At C, the total is below

    4e_C+1/2+2s_C<4e_C+4s_C=4x_C.

Thus every inequality in (V) holds. The seven anchor rows are already bad; no extra request is needed.

All cases are exhausted. This proves the theorem.

## Scope of the new reduction

The inequality (R) proves that the only arrow graphs not handled by this theorem have a directed two-cycle or a vertex of indegree two. In particular a counterexample in the balanced three-minimum regime at capacities >=3/4 must have one of those patterns. The proof treats actual anchor types and a genuine request in their full superfamily; it does not assert that the three-anchor subfamily retains the transversal number of the original family.

More explicitly, the seven possible loopless arrow graphs up to relabeling, with outdegree at most one, are: empty, one arrow, a directed path of length two, a converging fork, an isolated directed two-cycle, a directed three-cycle, and a directed two-cycle with the third vertex pointing into it. This theorem covers the first, second, third, and sixth possibilities. The remaining graphs are exactly the fork, two-cycle, and two-cycle with a feeder.

The double-incoming condition (Q) cannot simply be omitted. For example, in units of 1/1000,

    x=(754,751,784),
    a=(503,497,0), b=(0,511,489), c=(477,0,523),

all own heaviness and slack assumptions hold, with E=752/1000, but (2a+b)_B=1505/1000 exceeds 2x_B=1502/1000. Case 2 is essential. This is a failure of that particular fixed Fano construction, not a counterexample to the theorem.

## Exact diagnostic

Run `python3 -B -S work/paper_push/general/check_three_cycle_one_response.py`.
This standard-library script reconstructs all seven Fano pencils from the displayed lines, checks both explicit row assignments, checks every V4 inequality in its branch, and checks the exact residual caps and request costs. The run passed 3,000 rational generated states and four targeted controls, including both failed-(Q) branches. Its branch counts were 3,002 for Case 1, one targeted Case 2a, and one targeted Case 2b. This is a finite diagnostic accompanying the hand proof, not an exhaustive parameter certificate.

## A converging-fork theorem

The following additional lemma was derived by the parent and independently checked here. Suppose the arrow graph is the converging fork A->C,B->C, with C having no outgoing arrow. In addition to the numerical hypotheses above, assume

    s_C+2a_C<=2x_C,       s_C+2b_C<=2x_C.              (FQ)

Then one Fano partner request of cost below 3/4 closes the full superfamily. In particular (FQ) is automatic when e_C>=1/4, since s_C>1/2 and a_C,b_C<1/2. No upper bound on any part capacity is needed.

*Proof.* Relabel A,B so that s_A>=s_B. All four off-coordinate traces a_B,b_A,c_A,c_B are light at their target coordinates. Use Fano rows

    (a,a,b,a,b,c,u).

The four anchor pencils are 2a+b twice, 2a+c, and 2b+c. At A and B the needed bounds follow from the light traces. At C the pencils 2a+b have load below 3/2<=2x_C, and the other two bounds are (FQ).

The response pairs are a+c,a+b,a+b. All fit with full residual capacities x_A,x_B: the pairs containing an own type use a light cross trace, and at B the a+c pair is at most 2e_B<x_B. The six-anchor totals at A and B satisfy

    3s_A+2b_A+c_A<=3x_A,
    3a_B+2s_B+c_B<=4e_B+2s_B<3x_B.

At C retain

    r_C=min(x_C,2x_C-a_C-s_C,2x_C-a_C-b_C,
            4x_C-3a_C-2b_C-s_C).

The request cost is

    D=max(0,a_C-e_C,a_C+b_C-x_C,
          3a_C+2b_C+s_C-3x_C).                        (FD)

The first two nonzero candidates are below 1/2 and 1/4 respectively. For the last, write a_C=1-s_A-a_B and b_C=1-s_B-b_A to obtain

    5-3s_A-2s_B-2s_C-3e_C-3a_B-2b_A.                 (FT)

If e_C>=1/4, then 3s_A+2s_B+2s_C>7/2, so (FT)<3/2-3e_C<=3/4.

If e_C<=1/4, use s_A>=s_B, own heaviness, and E>3/4:

    3s_A+2s_B >=(5/2)(s_A+s_B)
               >5(e_A+e_B)>15/4-5e_C.

Also s_C=x_C-e_C>=3/4-e_C, hence

    2s_C+3e_C>=3/2+e_C.

Their sum is strictly greater than 21/4-4e_C>=17/4. Thus (FT)<3/4 in this case as well. Consequently every candidate in (FD) is below 3/4, so D<3/4 and r_C=x_C-D>0. All partner-pencil and total inequalities hold by its definition. The corresponding request retaining (x_A,x_B,r_C) therefore forces a bad Fano tuple. QED.

This reduces the remaining fork regime further: its target slack must satisfy e_C<1/4, and at least one of the two inequalities (FQ) must fail. The total capacity bound in the displayed construction is already sufficient throughout the fork regime; the unresolved issue is the anchor pencil with one own C load and two large incoming loads.
