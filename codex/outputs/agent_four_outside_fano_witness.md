# Four outside rows in a near-Fano missing-trace witness

Status: complete hand classification of the internal-intersection branches and exact outside endpoint support. One of the two cases improves the general outside-support bound by a factor of two. Both cases are locally realizable with sharp support counts, so neither is excluded by the witness geometry alone. No high-transversal counterexample or general upper-bound improvement is claimed.

## 1. Setup and the two possible internal branches

Let H have rank at most k and property (7,2). Fix U of size N and assume every actual U-trace has size at least L, where

    N < 9L/5.

Let F be actual, and X=F intersect U a nonempty missing trace. Consider a bad saturation tuple

    X, G_1,G_2,G_3,G_4,K_1,K_2,

where the G_i are actual edges not contained in U and the K_i are actual edges contained in U. The two internal rows are forced by the majority-six lemma, since all seven projected rows are larger than N/2. Put

    I = K_1 intersect K_2.

Every pair piercing the actual tuple obtained by replacing X with F avoids X. Its point meeting F therefore lies outside U, and its other point lies in I. Thus I is nonempty.

Apply the minimum-row-size Fano support lemma proved in `agent_three_outside_trace_witness.md`, Section 4, to the seven projected rows of this particular bad tuple. Every positive complementary type contains a line of a Fano plane on the seven row coordinates, and all seven lines occur as positive complementary types. This is a statement about the single projected witness; it is not a local-property claim about the full projected family.

Let Q be the pair of internal row coordinates. Its Fano line is Q union {e}. There are exactly two Fano lines avoiding Q. Label them

    {e,a,b} and {e,c,d}.

The five external row coordinates are therefore e,a,b,c,d. Any point of I has a complementary type contained in these five coordinates. Its type must contain one of the two displayed lines. Consequently its external membership is a subset of {a,b} or a subset of {c,d}. In particular:

1. no point of I lies in row e;
2. no point of I belongs to external rows from both pairs;
3. the two pure classes whose external memberships are exactly {a,b} and exactly {c,d} are both nonempty.

The last assertion follows because each of the two Fano lines itself occurs as a positive complementary type. For an allowed external subset R, write I_R for the class of I having exactly that subset as its external membership. Thus the only possible classes are

    I_empty, I_a, I_b, I_ab, I_c, I_d, I_cd,

with I_ab and I_cd nonempty. There are two cases depending on whether e is F or a witness row.

## 2. Case A: the distinguished coordinate e is F

Now the four outside witness rows are A,B,C,D, paired as {A,B} and {C,D}, while every point of I avoids X. Write O_A=A outside U, and similarly for the other rows, and set

    Z_1 = O_A intersect O_B,
    Z_2 = O_C intersect O_D.

**Exact actual piercing branches.** For every allowed subset R of {A,B} or {C,D}, the pairs having internal endpoint in I_R are exactly

    I_R x ((F outside U) intersect intersection of all witness G not in R).

Their union is the full piercing graph of the seven actual rows. In particular, the two maximal branches are

    I_AB x ((F outside U) intersect Z_2),
    I_CD x ((F outside U) intersect Z_1).

At least one maximal branch is nonempty. Indeed, any smaller-class branch has an outside endpoint that also works with the nonempty pure class for its containing pair. Equivalently, the actual outside endpoint set is exactly

    (F outside U) intersect (Z_1 union Z_2).

**Exact outside support of the six witness rows.** Let S={A,B,C,D,K_1,K_2}. Then

    P(S) outside U = Z_1 union Z_2.                     (A)

To prove this, an outside endpoint must pair with a point of I. That point belongs to at most one of the two external pairs, so the outside endpoint must meet all of the opposite pair. Conversely every point of Z_1 pairs with any point in nonempty I_CD, and every point of Z_2 pairs with any point in nonempty I_AB.

This gives the sharp support estimate

    |P(S) outside U|
      <= min(|O_A|,|O_B|)+min(|O_C|,|O_D|)
      <= 2(k-L).

The two pure classes also force the trace restrictions

    X intersect C intersect D = empty,
    X intersect A intersect B = empty.

These intersections involve X and are automatically inside U. No corresponding global three-fold intersection of witness rows is forced to be empty in this case.

## 3. Case B: e is an outside witness row

Call row e by the name E. Label the two external pairs as {F,A} and {B,C}. Thus the witness rows are A,B,C,E, the pure classes I_FA and I_BC are nonempty, and every point of I avoids E.

**A global empty triple is forced:**

    B intersect C intersect E = empty.                 (B1)

Indeed a point of the nonempty pure class I_FA belongs to X, A, and both internal rows. Any point common to B,C,E, including an outside point, would pair with it to pierce the bad tuple. Thus no such point exists.

Put

    Z = (A intersect E) outside U,
    J = (F outside U) intersect A intersect E.

The exact piercing graph of the seven actual rows is the union of

    I_BC x J,
    I_B x (J intersect C),
    I_C x (J intersect B).                             (B2)

All other I-classes are inactive. The classes containing F are excluded because an actual piercing pair cannot meet X. The class I_A would require an outside partner common to F,B,C,E, impossible by (B1). The empty class would require an outside partner common to all four witness rows, also impossible by (B1). The remaining three classes give precisely (B2).

Since some actual pair exists and I_BC is nonempty, J is nonempty and the maximal I_BC x J branch is active. The actual outside endpoint set is exactly J.

For the original six-row witness S={A,B,C,E,K_1,K_2}, the exact outside support is

    P(S) outside U = Z = (A intersect E) outside U.     (B3)

The pure class I_BC pairs with every point of Z, giving one inclusion. Conversely, points of I_FA, I_F, I_A, or I_empty could be paired with an outside point only if that point belonged to B intersect C intersect E, which is empty. The remaining classes I_BC,I_B,I_C require an outside endpoint in A intersect E. This proves (B3).

Consequently

    |P(S) outside U| <= min(|A outside U|,|E outside U|)
                     <= k-L.

This is a factor-two improvement over the general four-outside-row bound, with a precise support identity rather than only a numerical estimate. It comes from the positive pure I_FA class, which supplies the global prohibition (B1).

## 4. Consequences and limits of the endpoint counts

In both cases S has six actual rows, so P(S) is a global transversal and P(S) intersect U is disjoint from X. Therefore Case A gives

    t <= N-|X|+|Z_1 union Z_2| <= N+2k-3L,

while Case B gives

    t <= N-|X|+|Z| <= N+k-2L.

The second bound is strictly better as an outside-support statement. Substitution of N=k+t-1 and L=6(t-d)-2N-8 nevertheless gives, respectively,

    12t <= 9k+18d+17,
     8t <= 6k+12d+11.

Both retain the leading coefficient 3/2 on d in the resulting bound for t. The new information is the dichotomy between two outside pair intersections and one outside pair intersection together with a globally empty witness triple. The numerical substitution itself does not improve the established asymptotic coefficient.

## 5. Sharp local realizations of both cases

These examples satisfy the strict near-Fano hypothesis at equality N/L=7/4, realize the asserted full-width missing-trace obstruction, and attain the outside-support bounds relative to k-L. They do not have a large induced transversal number.

Take the Fano lines

    123,145,167,246,257,347,356.

For each line L_0 introduce a disjoint class C_{L_0} of m points, where m>=1. Let U be their union, so N=7m. Define the seven projected rows

    B_i = union of C_{L_0} over lines L_0 not containing i.

Each B_i has size L=4m. The seven rows are not two-pierceable: two points' line labels intersect in a row missed by both. Every proper subfamily is two-pierceable: if row i is omitted, points from two line classes whose lines meet exactly at i cover every other row. Every old point belongs to exactly four rows.

Use B_6,B_7 as the two internal rows. Their distinguished Fano coordinate is e=1, and the two avoiding lines are 123 and 145. The two pure I-classes are C_145, with external membership {2,3}, and C_123, with external membership {4,5}.

Fix b>=1 and let k=4m+b.

### Case A realization

Take disjoint outside clouds Z_23 and Z_45 of b points each. The actual outside witness rows are

    G_2=B_2 union Z_23,    G_3=B_3 union Z_23,
    G_4=B_4 union Z_45,    G_5=B_5 union Z_45.

Choose z in Z_23 and take F=B_1 union {z}. All rows have rank at most k. A point of C_123 together with z pierces all seven actual rows, so the actual family has (7,2).

Replacing F by X=B_1 makes the seven rows non-two-pierceable. Two old points fail by the Fano argument. An outside point belongs to only two witness rows, so its partner would have to cover five projected rows, impossible because every old point has only four memberships. Two outside points miss both internal rows. Every proper subfamily is two-pierceable by the old Fano pairs, so the witness has minimum width six.

Here

    P(S) outside U = Z_23 union Z_45,
    |P(S) outside U| = 2b = 2(k-L).

Thus the two-intersection bound in Case A cannot be lowered from this local support information.

### Case B realization

Let the missing-trace coordinate F be 2. The special outside row E is 1, its paired row A is 3, and the other pair is B=4,C=5. Take three disjoint outside clouds Z_13,Y_4,Y_5, each of size b, and set

    G_1=B_1 union Z_13,    G_3=B_3 union Z_13,
    G_4=B_4 union Y_4,     G_5=B_5 union Y_5.

Choose z in Z_13 and put F=B_2 union {z}. A point in C_123, whose original external membership is {4,5}, together with z pierces all actual rows. Again every row has size at most k and the family has (7,2).

Replacing F by X=B_2 produces a minimum-width-six bad tuple by the same argument: outside points meet at most two witness rows, while old points meet at most four original rows. Also G_1 intersect G_4 intersect G_5 is globally empty: it is empty in U because {1,4,5} is a Fano line, and the three outside clouds are disjoint.

In this case

    P(S) outside U = Z_13,
    |P(S) outside U| = b = k-L.

The improved single-intersection bound is therefore also sharp locally.

## 6. Precise remaining obstruction

Both cases have actual piercing pairs, positive pure-line classes, and valid full-width missing-trace witnesses. Neither positive pure-line class creates an impossibility; in Case B it creates exactly the global empty triple and single outside intersection described above. Any saturated extension retaining the witness rows still excludes the missing trace, since the bad seven-tuple persists.

These examples do not establish minimum vertex count, a high-q optimal host, or minimality of the number of outside rows among all possible witnesses. Their induced internal family has small transversal number. Thus they identify the limit of the local support argument without contradicting the desired global theorem. Further progress must use compatibility of the forced empty triples or the outside intersection covers with the rest of the high-transversal induced core. The local four-outside classification and its support bounds are complete.
