# Remaining converging fork: exact exclusions and an exchange branch

Status: hand lemmas proved below. The full converging-fork case is still open. This report continues the graph reduction in `paper_push_three_cycle_one_response.md`; it does not change the general 6/7 bound.

Use unit types a,b,c, own loads s_A=a_A,s_B=b_B,s_C=c_C, capacities x_i>=3/4, slacks e_i=x_i-s_i, strict own heaviness s_i>2e_i, E=e_A+e_B+e_C>3/4. The arrow graph is A->C,B->C, with no outgoing arrow from C. In particular a_B<=e_B,b_A<=e_A,c_A<=e_A,c_B<=e_B; every off-coordinate trace is below 1/2, and each s_i>1/2.

## 1. There cannot be two failed incoming pencils

Suppose both s_C+2a_C>2x_C and s_C+2b_C>2x_C. Then

    a_C+b_C>s_C+2e_C,
    s_A+s_B<=2-a_C-b_C<2-s_C-2e_C.

But e_A+e_B<(s_A+s_B)/2, hence

    E<1-s_C/2<3/4,

contrary to the assumption. Thus, after the previously proved branch where both pencils fit, there is exactly one failed pencil. Label it

    a_C>s_C/2+e_C,       b_C<=s_C/2+e_C.              (1)

Also (1) forces e_C<1/4: otherwise its right side is above 1/2, impossible for a_C.

## 2. The ABC pencil always fits in the fork

At A and B this follows from the light incoming traces: s_i+2e_i<=2x_i. At C, the two other own-heaviness inequalities and E>3/4 give

    s_A+s_B>2(e_A+e_B)>3/2-2e_C,
    a_C+b_C<=2-s_A-s_B<1/2+2e_C<s_C+2e_C.

Therefore a+b+c<=2x in every part, strictly at C. Any construction failing only this mixed pencil can consequently discard that obstruction.

## 3. Additional strict consequences of the failed pencil

The row-sum bound gives s_A<1-s_C/2-e_C. Thus

    e_A+e_C<s_A/2+e_C
             <1/2-s_C/4+e_C/2<1/2,

using e_C<s_C/2. Consequently e_B>1/4.

More sharply a_B<e_B/2. Indeed x_C>=3/4 gives s_C>=3/4-e_C, so

    2a_B=2-2s_A-2a_C<5/4-2s_A-e_C.

On the other hand e_B>3/4-e_A-e_C. The difference of the preceding upper bound and this lower bound is

    1/2-2s_A+e_A<1/2-(3/2)s_A<0.

This proves the claim. Thus the remaining single-failed branch has an especially small reverse trace into B, and B has slack greater than 1/4.

## 4. A two-V5 exchange closes a subregion of the remaining branch

Assume, in addition to (1),

    b_A<=e_A/2,
    4(e_A+e_B)-s_A-s_B-a_B-b_A>=1.                  (2)

Then the full type-closed superfamily has tau*<3/4.

Recall the V5 support: five a-rows, one b-row, and one response u form a bad tuple whenever 2a+b+u<=2x and 5a+b+u<=4x. Define its partner box

    R=min(x,2x-2a-b,4x-5a-b),

and define S with a,b exchanged. All minima are coordinatewise.

The two reverse-trace bounds a_B<e_B/2 and b_A<=e_A/2 imply R_B=x_B and S_A=x_A. For example, at B the pair cap is s_B+2e_B-2a_B>=x_B and the total cap is 3s_B+4e_B-5a_B>x_B; the latter follows already from s_B>2e_B and a_B<=e_B/2. The other coordinate is symmetric.

At the own coordinates, strict heaviness makes the total facet the minimum:

    R_A=4e_A-s_A-b_A,
    S_B=4e_B-s_B-a_B.

Each is strictly below 2e_i<1, while (2) says R_A+S_B>=1. Hence both are positive.

Put lambda=x_C-3/4. Since a_C,b_C<1/2 and x_C>=3/4,

    2a_C+b_C<3/2<=x_C+3/4,
    5a_C+b_C<3<=3x_C+3/4,

and the exchanged inequalities hold too. Thus R_C,S_C>lambda.

Choose a sufficiently small delta>0 with lambda+delta<=min(R_C,S_C). A request retaining (x_A,x_B,lambda+delta) costs 3/4-delta. Any unit response u either has u_A<=R_A, hence u<=R, or has u_A>R_A, hence u_B<=1-u_A<1-R_A<=S_B and u<=S. In each case one of the two actual V5 tuples is bad. Therefore the retained box is free and tau*<=3/4-delta<3/4. This is a genuine full-superfamily request argument; it does not replace admissible types by their convex hull.

## 5. Exact control illustrating why a different support matters

The rational fork

    x=(754,781,751)/1000,
    a=(503,0,497)/1000,
    b=(0,521,479)/1000,
    c=(245,244,511)/1000

has e=(251,260,240)/1000 and E=751/1000. All heaviness and fork hypotheses hold. Its a-pencil fails because s_C+2a_C=1505/1000>1502/1000=2x_C, while its b-pencil fits.

The tempting alternate Fano assignment (a,a,b,b,b,c,u), on the usual line order 012,034,056,135,146,236,245, avoids the failed anchor pencil. Its anchor pencils are 2a+b,a+2b,a+b+c,2b+c and all fit. However its partner box is (754,520,62)/1000, costing 950/1000. Thus that single replacement is insufficient.

The exchange lemma above closes this state: R=(501,781,29)/1000, S=(754,519,47)/1000. Since 501/1000+519/1000>1, retaining (754,781,29)/1000 is a free box, costing only 722/1000=361/500. The exact existing Fano/V4 oracle independently reports the same optimum for its one-occurrence Fano/V4 menu in `work/paper_push/general/fork_single_failed_alternative.json`. This numerical configuration is an obstruction only to the specified fixed Fano assignment; it is not an obstruction to one-request closure.

## Precise remaining branch and next step

The fork cases not closed by the current hand arguments must satisfy (1), e_C<1/4, e_B>1/4, a_B<e_B/2, and at least one of

    b_A>e_A/2,
    4(e_A+e_B)-s_A-s_B-a_B-b_A<1.

The ABC pencil is already valid. A concrete next line is to combine a V5 box with an asymmetric Fano box or the new 223 support in this residual branch: if the reverse trace b_A is large then b_C is correspondingly smaller, so the lost exchange-box capacity is accompanied by extra capacity in the problematic common part. No complete inequality covering this branch is claimed here.


## 6. Two repeated-response Fanos and the bounded eight-branch probe

The parent proposed Fano assignments (a,b,b,b,u,c,u) and (a,a,b,b,u,u,c). Under the one-failed-fork hypotheses their exact request costs simplify to

    D1=b_A/2+s_B-e_B+a_C-e_C
         +max(0,(3b_C-a_C-s_C)/2),
    D2=b_A/2+s_B/2+a_C-e_C+max(0,b_C-s_C/2).

For the second assignment the fixed pencils are 2a+b and 2b+c; response inequalities give the box

    min(x-b/2,2x-a-b,2x-a-c,(4x-2a-2b-c)/2).

At A its deficit is b_A/2, at B it is s_B/2, and at C it is max(a_C-e_C,a_C+b_C-s_C/2-e_C), giving D2. The first formula was independently derived by the parent.

These two assignments alone do not suffice. For

    x=(85,140,76)/100,
    a=(57,0,43)/100,
    b=(0,94,6)/100,
    c=(28,1,71)/100,

all hypotheses hold with e=(28,46,5)/100, and D1=86/100,D2=85/100. The exchange lemma of Section 4 does close that state.

A bounded LP probe enumerated the eight ways that D1>=3/4, D2>=3/4, and at least one of (2) fails: two affine choices for each Fano maximum, and two exchange-failure choices. The exploratory program is `work/paper_push/general/fork_combined_lp.py`. It found the following exact witness with positive margins in the required strict inequalities; its properties and costs can be checked directly without trusting floating-point infeasibility:

    x=(121,157,108)/144,
    a=(81,0,63)/144,
    b=(21,105,18)/144,
    c=(1,52,91)/144.

Here e=(40,52,17)/144 and E=109/144>3/4; all strict own and fork conditions hold. The a-pencil exceeds capacity by 1/144. We have

    D1=73/96>3/4,       D2=109/144>3/4,
    b_A=21/144>20/144=e_A/2.

Thus the union of these three simplified sufficient criteria is not a theorem for all forks. This is a precise obstruction to that finite proposed case split.

Crucially, the actual V5 boxes still repair this state immediately:

    R=(58,157,72)/144,
    S=(119,103,108)/144.

The retained box (119,157,72)/144 is free: either u_A<=58/144 and u belongs to R, or u_B<86/144<103/144 and u belongs to S. Its cost is only 38/144=19/72. The obstruction therefore identifies the missing freedom in the simplified exchange criterion: a small cut in A can be paid for by retaining much more in C.

The exact witness is saved in `work/paper_push/general/fork_combined_failure_exact.json`. Run `python3 -B -S work/paper_push/general/check_fork_combined_failure.py`. This independent standard-library check reconstructs the Fano pencils for both repeated-response assignments, verifies all strict fork hypotheses and both request costs, and verifies the two V5 boxes and their cheaper free-box repair. No LP solver is used by the checker.

The remaining inequalities in Section 5 describe the scope of the proved sufficient hand criteria, not a failure of the full V5 partner oracle. Likewise the eight-branch witness rules out only the stated simplified three-criterion case split; it does not establish a counterexample to full one-request closure.
