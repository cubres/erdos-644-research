# A hand proof of the general six-sevenths bound

26 September 2026. Consolidated proof by the general-bound and middle-gap agents. This removes all 718 nodes of the reduced certificate from the mathematical proof. The earlier exact certificate remains preserved as an independent discovery check. No claim of the conjectured 3/4 upper bound is made.

## Main theorem

Let k>=28 be an integer. Every k-uniform family H with property (7,2) has

    tau(H)<=ceil(6k/7)+4.

The same holds for families of nonempty sets of rank at most k, by private padding. In particular c_7<=6/7.

The proof uses the existing hand closing Lemmas 7.29, 7.31, 7.32, 7.33, 7.35, 7.37, 7.46, the hand static construction S1a, and the old conditional finishing Lemma 7.50. Its new ingredients are the near-core/fullcore lemma, the stronger conditional finishing theorem, the simple static allocation S0, and the following three hand gap extensions. Full proofs of all new ingredients are collected below; the earlier lemmas remain hand-proof dependencies, not computer assertions.

## Global proof and integer budgets

Put beta=6/7 and T=ceil(beta*k)+4. Since k>=28, T<=k. Suppose tau(H)>T. Every request containing at most T points then has an avoiding family edge.

Here is the cap construction used three times. Suppose E,F have intersection qk, where q lies in an interval [a,b]. Choose u and put v(q)=2-beta-q-u. When 0<=u,v(q)<=1-q, select subsets of the private parts of E,F of respective sizes floor(uk), floor(v(q)k). Request an edge avoiding E intersect F and the complements of those subsets inside the two private parts. This request has size

    2k-qk-floor(uk)-floor(v(q)k) < beta*k+2 <= T.

The response gives a good triple, whose other two pair proportions are at most u and v(q)<=v(a). Interchanging the two original edges allows these two proportions to be sorted.

Apply this construction in the following order:

| Stage | Hypothetical q | u | v(q) | Resulting response bounds |
|---|---|---|---|---|
| 1 | [3/7,10/21] | 5/14 | 11/14-q | y,z<=5/14 |
| 2 | [4/21,5/14] | 10/21 | 2/3-q | y,z<=3/7 by Stage 1 |
| 3 | [10/21,1/2] | 1/3 | 17/21-q | y,z<=4/21 by Stage 2 |

The cap-host inequalities are immediate in all three rows. Stage 1 is closed by its three hand cases below. In Stage 2, the raw caps are at most 10/21, so the gap [3/7,10/21] reduces both traces below 3/7; its two hand cases close. In Stage 3, the raw caps are at most 1/3<5/14, so the gap [4/21,5/14] reduces both traces below 4/21; its four hand cases close.

Thus there is no pair intersection in [3k/7,k/2]. The stronger conditional finishing theorem proved below gives tau(H)<=T, a contradiction.

All requests fit the SAME integer budget T. S0 is integral and has no rounding loss. L29, L31, L32 and L33 have integer constructions when their homogeneous real inequalities fit the integer budget. S1a costs fewer than three additional points. L35, L37 and L46 require at most four additional points, already included in T. The conditional finisher and the new near-core/fullcore lemma also fit T. The errors for the cap request and different subsequent requests are not added, since each is a separate avoidance request. No static LP rounding term is used anywhere in this proof. QED, using the local hand arguments below.

## First gap: three scalar cases

## Stage 1: the gap [3/7,10/21]

Suppose a good triple has pair sizes

    3/7<=x<=10/21,       0<=z<=y<=5/14.

Put s=y+z, d=y-z and S=x+s. We use the hand lemmas L31, L32 and S1a, whose complete proofs are included in the companion `paper_push_six_sevenths_hand_dependencies.md`.

**Case A: d>x-1/7.** Apply L32(x,y,z). Since s+d=2y<=5/7,

    S=x+s<=x+5/7-d<6/7,
    1/2+y<=6/7,
    (1+2x-d)/2 < (8/7+x)/2 <=17/21<6/7,
    (1+2x+2s-d)/3
       <=(1+2x+10/7-3d)/3
       <(20/7-x)/3<=17/21<6/7.

These are precisely its four budget inequalities.

**Case B: d<=x-1/7 and s<=11/7-2x.** Apply L31 in orientation (y,z,x). Its nine expressions are bounded as follows:

    s<=5/7,
    1/2+y, 1/2+z <=6/7,
    1+d-x<=6/7,
    1-d-x<=4/7,
    1-S/3<=6/7                 (because S>=x>=3/7),
    (3+S)/5<=88/105<6/7        (because S<=25/21),
    (1+s+2x)/3<=6/7,
    (2+3x)/4<=6/7              (because x<=10/21).

**Case C: s>11/7-2x.** This is the only remaining case. Since x<=10/21,

    s>11/7-2x>=x+1/7.

Also d<=5/7-s, and therefore

    x+y-z=x+d<3x-6/7<=4/7=3beta-2.

Finally S<=25/21<9/7=5beta-3. These are exactly the three S1a conditions. Its split construction has fewer than three points of integer rounding loss.

The three cases cover the entire box. Thus an initial pair intersection q in [3/7,10/21], with cap u=5/14 and v(q)=11/14-q, always closes. The cap at the left endpoint is v(3/7)=5/14; the cap-host conditions hold throughout the interval. The resulting initial request costs at most beta*k+2.


## Middle gap: an integer allocation and two scalar cases

## Elementary static lemma S0

Let A1,A2,A3 be a good triple of unit edges, so their common intersection
is empty. Let their pair cells X=A1 intersect A2, Y=A1 intersect A3,
Z=A2 intersect A3 have sizes a,b,c. Suppose

    a<=3/7, b,c<=5/14, b+c<=4/7.                       (S0)

Then the triple closes at budget 6/7. The corresponding integer lemma has
no rounding loss: if the homogeneous assumptions hold at rank k, budget
T=ceil(6k/7) suffices for all four further avoidance requests.

*Proof.* Give each point of X the request label {1,2,3}, each point of Y
the label {2,4}, and each point of Z the label {3,4}. A label lists the
new requests containing that point. Distribute the private cells U of A1,
V of A2, and W of A3 among the following singleton labels:

    U, of mass 1-a-b:  {3} or {4};
    V, of mass 1-a-c:  {2} or {4};
    W, of mass 1-b-c:  {1}, {2}, or {3}.

The four remaining request capacities are

    C=(T-a, T-a-b, T-a-c, T-b-c),

where for the normalized proof T=6/7. They are nonnegative by (S0).
A capacitated bipartite allocation exists if and only if the total mass
of each subcollection of U,V,W does not exceed the capacity of the union
of its available request indices. The seven resulting inequalities are

    1+2c<=2T,              1+2b<=2T,
    1+3a<=3T,              2+b+c<=3T,
    2+2a+c<=4T,            2+2a+b<=4T,
    3+a<=4T.                                           (H)

These are the elementary max-flow/Hall conditions for three source nodes
and four request nodes. They all follow from (S0): the first two use
b,c<=5/14; the third uses a<=3/7; the fourth uses b+c<=4/7; the fifth and
sixth are at most 2+6/7+5/14=45/14<24/7; and the last uses a<=3/7.
Thus all four requests have size at most 6/7. For integer cell sizes and
integer T, the same bipartite network has an integral flow, so the private
points can be allocated without any rounding.

Request four further edges avoiding those four sets. Any two points
covering the original good triple must either lie in two distinct pair
cells, or in a pair cell and its opposite private cell. The labels of
every such pair intersect: {1,2,3}, {2,4}, {3,4} are pairwise intersecting;
U labels meet {3,4}, V labels meet {2,4}, and W labels meet {1,2,3}.
The two points are therefore both absent from at least one of the four
new edges. Points outside the original triple cannot change this argument,
since their partner alone cannot cover all three original edges. Hence the
seven edges have no two-point transversal. QED.

## Middle-box coverage in two cases

Assume all pair intersections avoid the interval [3/7,10/21], and a good
triple has pair sizes

    4/21<=x<=5/14,     0<=y,z<=3/7.                    (D)

Every such triple closes at budget 6/7, with only the integer allowance
already present in L46. By symmetry arrange y>=z.

**Case 1: x+z<=11/21.** Since x>=4/21,

    z<=1/3<5/14.

Apply S0 with distinguished pair size a=y and remaining sizes b=x,c=z.
Indeed a<=3/7, b<=5/14, c<5/14, and

    b+c=x+z<=11/21<4/7.

This closes the triple without using the gap assumption.

**Case 2: x+z>=11/21.** Use L46 in orientation

    (a,b,c)=(y,x,z),    h=10/21, ell=3/7.

For clarity, L46 requires

    a+b>=1-h, b+c>=1-h,
    max(2-2h-b, a+ell, c+ell, 1/2+b, 3/4,
        (3+a+b+c)/5)<=6/7.

The domain conditions follow from y>=z and x+z>=11/21=1-h.
Every budget term is automatic on (D):

    2-2h-b=22/21-x<=18/21=6/7,
    a+ell=y+3/7<=6/7,
    c+ell=z+3/7<=6/7,
    1/2+b=1/2+x<=6/7,
    3/4<6/7,
    (3+a+b+c)/5 <=(3+5/14+6/7)/5=59/70<6/7.

Thus L46 closes the triple. The equality x+z=11/21 is covered by both
cases. This proves the entire Stage 2 box by hand. QED.


## Final gap: four scalar cases

## Stage 3: extending the upper gap to 1/2

Assume the gap [4/21,5/14] is already established. Consider a good triple with

    10/21<=x<=1/2,       0<=z<=y<=4/21.

Put s=y+z, d=y-z and S=x+s. Set ell=4/21 and h=5/14.

**Case A: S<=5/7.** Lemma 7.29 applies with dominant pair x. Its bounds are

    (1+S)/2<=6/7,
    1-x+d<=1-10/21+4/21=5/7,
    1-x-d<=1-x+d<=5/7,
    1/3+x<=5/6<6/7.

**Case B: 5/7<=S<=6/7 and z<=1/14.** Apply Lemma 7.33 in orientation (x,z,y). Its first bound S<=beta is given; its remaining bounds satisfy

    1/3+x<=5/6,
    1-x+y<=5/7,
    2x+y+3z<=1+4/21+3/14=59/42<11/7.

The last inequality is equivalent to its final budget expression (1+2x+y+3z)/3<=beta.

**Case C: 5/7<=S<=6/7 and z>=1/14.** Apply Lemma 7.35 with dominant x and gap [ell,h]. Its nine inequalities follow from

    S<=6/7,
    1-h+y, 1-h+z <=9/14+4/21=5/6,
    2-2h-x<=9/7-10/21=17/21,
    1/3+x<=5/6,
    2x-y, 2x-z <=1-1/14=13/14,
    x-y-z=2x-S<=1-5/7=2/7,
    2ell+y+z<=16/21.

Indeed, the sixth and seventh displayed lemma forms are at most
(23/14+13/14)/3=6/7, and its eighth is at most
(16/7+2/7)/3=6/7. The integer rounding allowance of this lemma is at most four.

**Case D: S>=6/7.** Apply Lemma 7.37 with dominant x and gap [ell,h]. Its domain condition is precisely this case. Its remaining bounds are

    x+y<=1/2+4/21=29/42,
    1-h+y, 1-h+z<=5/6,
    1/4+x+(y+z)/4<=3/4+2/21=71/84<6/7,
    2ell+y+z<=16/21,
    1/2+x/2+(z+ell)/4<=3/4+2/21=71/84<6/7.

Its integer rounding allowance is again at most four. This exhausts Stage 3.

For an initial pair q in [10/21,1/2], use u=1/3 and v(q)=17/21-q. Both traces are at most 1/3. The previously established gap [4/21,5/14] forces both below 4/21, giving exactly the covered box. The initial request costs at most beta*k+2.


## Stronger conditional finishing theorem

## Theorem

Let k>=28 and let H be a k-uniform family with property (7,2). Suppose every pair intersection has size at most 3k/7 or greater than k/2. Then

    tau(H) <= ceil(6k/7)+4.

Private padding gives the corresponding rank-at-most-k statement, since it preserves intersections of distinct edges, transversal number, and (7,2).

We use the exact integer closing lemmas L31 and L32 recorded in the hand-bound section of the research note, the static closing lemma S1a, the two-triple-cell lemma 7.46 with the full maximum-small gap, and the new near-core/fullcore lemmas in `outputs/paper_push_general.md`. Their statements and the full local algebra are included below.

## Closing tools and normalization

Write a good triple E,F,G as one with empty common intersection. Its pair cells have sizes x,y,z. Normalize the rank to one; beta=6/7 and e=1/7. Every local displayed budget inequality is homogeneous. The tools needed are:

* L32 closes if the budget is at least

      max(S, 1/2+y, (1+2x-y+z)/2, (1+2x+y+3z)/3),

  where S=x+y+z.

* L31 closes if the budget is at least

      max(x+y, 1/2+x, 1/2+y,
          1+x-y-z, 1-x+y-z, 1-S/3,
          (3+S)/5, (1+x+y+2z)/3, (2+3z)/4).

* S1a closes, with fewer than three points of integer rounding loss, if the sorted pair sizes m>=y>=z satisfy

      y+z>=m+e,       m+y-z<=3beta-2,       S<=5beta-3.

* Under the full gap 'every intersection <=m or >1/2', Lemma 7.46 can be used with h=1/2 and ell=m. Its proof only needs a response trace <=1/2 to be <=m, so the open lower endpoint is harmless. It closes a triple with oriented pair sizes x,y,z if

      x+y>=1/2, y+z>=1/2,
      max(1-y,x+m,z+m,1/2+y,3/4,(3+S)/5)<=beta.

  The original integer allowance is at most four points.

* The near-core lemma, with the same full gap, closes oriented sizes x,y,z if Delta=max(0,S-beta), y+z<=beta, and

      m+z<=beta,       1+y-z<=beta,
      2+x-2z<=2beta,   2+x+m-z<=3beta,   x+m<=beta,
      1-x+y+Delta<=beta,
      2-2x+z+Delta<=2beta,
      2-z+Delta<=2beta,
      3-x-y+Delta<=3beta.

  If S<=beta, the fully omitted-core variant drops the final two inequalities. These two new tools use exact integer-capacity allocations and have no rounding loss once the chosen budget is an integer.

All permutations of the three pair sizes are available in every tool.

## Local proposition

Suppose the full maximum-small gap holds with parameter m, and a good triple has sorted pair sizes

    2/7 < m <= 3/7,      m>=y>=z>=0,      m+2y<=8/7.       (D)

Then the triple closes at normalized budget 6/7, with at most four points of integer allowance.

### Case 1: y<=5/14

If y-z>m-1/7, use L32 in orientation (m,y,z). Its four terms satisfy

    S<2y+1/7<=6/7,
    1/2+y<=6/7,
    (1+2m-y+z)/2 < (1+m+1/7)/2 <=11/14,
    (1+2m+y+3z)/3 < (10/7+4y-m)/3
                            <=(10/7+3y)/3<=5/6.

If y-z<=m-1/7 but S<3/7, use L32 in orientation (z,y,m). Its first two terms fit directly. Its other two terms are bounded by (1+S)/2<5/7 and (1+3S)/3<16/21.

It remains that y-z<=m-1/7 and S>=3/7. Use L31 in orientation (z,y,m). The nine inequalities follow from

    y+z<=5/7,
    1/2+y<=6/7,
    m+y-z>=m>2/7>1/7,
    m-y+z>=1/7,
    S>=3/7,
    (3+S)/5 <= (3+8/7)/5=29/35,
    (1+y+z+2m)/3 <= (1+5/7+6/7)/3=6/7,
    (2+3m)/4<=23/28.

The bound for 1/2+z follows from z<=y. Thus all nine L31 terms are at most 6/7.

### Case 2: y>5/14 and 1/7<=z<=5/14

Use the full-gap version of Lemma 7.46, oriented as (x,y,z)=(m,z,y). Its two domain conditions follow because

    m+z >= y+z >5/14+1/7=1/2.

Its six budget terms satisfy

    1-z<=6/7,       2m<=6/7,       y+m<=2m<=6/7,
    1/2+z<=6/7,     3/4<6/7,       (3+S)/5<=29/35<6/7.

### Case 3: y>5/14 and z>=5/14

Use S1a. Indeed

    y+z>5/7>m+1/7,
    S<=8/7<9/7=5beta-3.

For the remaining S1a inequality, use the balanced constraint:

    m+y<=8/7-y<11/14,
    m+y-z<11/14-5/14=3/7.

Thus all S1a inequalities hold.

### Case 4: y>5/14 and z<1/7

Apply the new near-core or fully omitted-core lemma in orientation

    (x,y,z)_new=(m,z,y).

From (D),

    5/14<m<=3/7,       y<=8/21,       m<=8/7-2y.

The shared domain and first five bounds are

    z+y<1/7+8/21=11/21<6/7,
    m+y<=2m<=6/7,
    1+z-y<11/14<6/7,
    2+m-2y <=22/7-4y<12/7,
    2+2m-y<5/2<18/7,
    2m<=6/7.

If S<=6/7, the fully omitted-core variant needs only two more inequalities:

    1-m+z<11/14<6/7,
    2-2m+y<=2-m<23/14<12/7.

If S>=6/7, put Delta=S-6/7. The four remaining near-core inequalities, after moving the budget term from Delta, become

    1+2z+y<=12/7,
    2-m+z+2y<=18/7,
    2+m+z<=18/7,
    3+y<=24/7.

They follow respectively from

    1+2z+y<1+2/7+8/21=5/3<12/7,
    2-m+z+2y<=2+y+z<53/21<18/7,
    m+z<4/7,
    3+y<=71/21<24/7.

This exhausts the local domain and proves the proposition.

## Passage to the global conditional theorem

Set T=ceil(6k/7)+4<=k and suppose tau(H)>T. Request an edge avoiding any T points of another edge. This provides an intersection of size at most k-T<k/2, so a largest pair intersection M<=k/2 exists. By the assumed gap, M<=3k/7.

If M<=2k/7, the existing variable-threshold finishing lemma 7.50, with beta=6/7, already gives tau(H)<=T. Suppose M>2k/7.

Choose a pair attaining M and make the standard balanced avoidance request of size T: avoid their intersection, and split the remaining T-M requested points as evenly as possible between their private parts. The avoiding response forms a good triple. Its other two intersections, Y>=Z, satisfy

    Y,Z<=k-floor((T+M)/2),
    M+2Y<=2k-T+1<=8k/7-3.

Since M>2k/7, both new traces are smaller than 3k/7 and hence below k/2; maximality of M gives Y,Z<=M. Normalizing by k yields precisely (D).

Apply the local proposition. L31 and L32 have integer request constructions whenever their inequalities fit the integer budget. S1a costs less than three extra points, and Lemma 7.46 costs at most four; both fit T. For the near-core lemma, increasing its budget from the real value 6k/7 to the integer T decreases Delta and increases every available capacity, so its exact integer allocation also fits T. The fully omitted-core variant is likewise integral. Every branch therefore gives a bad subfamily of at most seven original edges, a contradiction. QED.


## Full proof of the new near-core tool

## New local closing lemma

Let H be k-uniform with property (7,2), and assume every pair intersection is either at most m or greater than k/2, where m<=k/2. Suppose T is an integer and tau(H)>T. Let E,F,G have empty common intersection, with x=|E intersect F|, y=|E intersect G|, z=|F intersect G|. Write

    Delta=max(0,x+y+z-T).

Assume y+z<=T and all the following inequalities:

    m+z<=T,                 k+y-z<=T,
    2k+x-2z<=2T,            2k+x+m-z<=3T,
    x+m<=T,
    k-x+y+Delta<=T,
    2k-2x+z+Delta<=2T,
    2k-z+Delta<=2T,
    3k-x-y+Delta<=3T.                       (NC)

Then four further legal responses produce a subfamily of at most seven edges which has no two-point transversal, a contradiction.

### Proof

Put X=E intersect F, Y=E intersect G, Z=F intersect G; these cells are disjoint. Request H4 avoiding Y union Z and a subset of X of size min(x,T-y-z). This is legal. The only potentially nonempty triple cell among E,F,G,H4 is

    P=E intersect F intersect H4,       p=|P|<=Delta.

Use the disjoint cells

    X'=X minus P,
    A=H4 intersect (E minus (F union G)),        a=|A|,
    B=H4 intersect (F minus (E union G)),        b=|B|,
    C=H4 intersect G,                           c=|C|,
    W=G minus (E union F union H4),              w=|W|.

Their elementary bounds are

    a<=k-x-y, b<=k-x-z, c<=k-y-z,
    p+a+b+c<=k,               c+w=k-y-z.

The complete products of candidate piercing pairs are

    P times (Y union Z union C union W),
    X' times C, Y times B, Z times A.

This is exhaustive: any point belonging to at least three of the first four edges lies in P; otherwise two covering points must lie in complementary pair cells.

Use three further requests, indexed 1,2,3. The following notation assigns each cell a set of permissible membership labels. For example {1,3} as a single label means the entire cell belongs to requests 1 and 3, while alternatives {1} or {3} mean the cell may be partitioned between them. Every splitting described below uses integer flows with integer capacities, so has no rounding loss.

**Case I: p+a<=m.** Put P in all three requests, X' in requests 1 and 3, Y and B in request 1, and Z and A in request 2. Partition C between requests 1 and 3, then W among all three. Before the last two partitions, the three loads are

    L1=x+y+b,              L2=p+z+a,              L3=x.

All are at most T: bound L1 by k+y-z, L2 by m+z, and L3 by x+m. The first partition fits since

    L1+L3+c = 2x+y+b+c <= 2k+x-2z <= 2T.

After partitioning C, W fits because the combined total load is

    L1+L2+L3+c+w = 2x+k+p+a+b
                         <=2k+x+m-z <=3T.

Every candidate pair is contained in one request: P lies in all of them; X' meets both possible C labels; Y and B share request 1; Z and A share request 2.

**Case II: p+a>m.** The global dichotomy gives p+a>k/2. Since (E intersect H4) and (G intersect H4) are disjoint, c<k/2, and consequently c<=m.

Put P in requests 1 and 2, X' and C in request 2, Y and B in request 1, and Z in requests 1 and 3. Partition A between requests 1 and 3, and W between requests 1 and 2. The base loads are

    L1=p+y+z+b,             L2=x+c,               L3=z.

All fit: L1<=Delta+k-x+y, L2<=x+m, and L3<=m+z. The two flexible cells can be assigned if and only if

    a<=2T-L1-L3,
    w<=2T-L1-L2,
    a+w<=3T-L1-L2-L3.

These are the elementary capacity conditions for two items whose allowed request pairs are {1,3} and {1,2}; they also follow directly from the integral max-flow theorem. Here they hold because

    L1+L3+a <= Delta+2k-2x+z <=2T,
    L1+L2+w =p+x+k+b <=Delta+2k-z <=2T,
    L1+L2+L3+a+w =p+x+k+z+a+b
                                 <=Delta+3k-x-y <=3T.

Every candidate pair is covered: P's labels {1,2} meet the labels of Y,Z,C,W; X' and C share request 2; Y and B share request 1; both possible A labels meet Z's {1,3}. Thus the three avoiding responses eliminate every possible two-point transversal of the first four rows. This proves the lemma. QED.

## Fully omitted core: no budget should be spent on an isolated cell

If x+y+z<=T, the first request avoids the entire pair-cell union, so P is empty. The cell W then has no candidate-pair neighbor and may be omitted from every final request.

Consequently, in the near-core lemma above, replace the four Delta-dependent inequalities by just

    k-x+y<=T,                 2k-2x+z<=2T,

and add the domain condition x+y+z<=T. The Case I conditions stay as stated above.

Proof. In Case II, use the same base loads with p=0 and partition A between requests 1 and 3; W is not assigned. It suffices that all base loads fit and a<=2T-L1-L3. These are precisely x+m<=T, k-x+y<=T, z<=T, and 2k-2x+z<=2T. The other two Hall conditions from the earlier proof arose only from W and are no longer needed. All candidate products that survive when P is empty remain covered. The Case I proof already succeeds even if W is unnecessarily assigned, so needs no change.

This variant is used only on its explicit x+y+z<=T domain.


## Scope and verification record

The final theorem above is a hand theorem. Its proof is independent of the reduced three-stage certificate and imports no assertion of numerical infeasibility. The certificate is retained separately at `work/paper_push/general/six_sevenths_three_gaps_minimal.json`; its independent rational replay verifies the same three boxes with 718 nodes but is unnecessary after the hand replacements. The previous certificate-based global theorem had additive constant +10 for k>=1000; the all-hand proof above improves the finite allowance to +4 for k>=28. The conditional finishing theorem has the same +4 allowance, not an additional +4.

The main asymptotic coefficient remains 6/7. This does not resolve Erdős Problem 644's target 3/4. The parent independently checked Stages 1 and 3, the S0 Hall conditions and Stage 2, the exact cap formulas, the integer +4 allowances in L35/L37/L46, and the k=28 boundary. It previously checked the near-core/fullcore lemmas and the new conditional finisher. The extracted old hand dependencies, excluding search chronology, are in `outputs/paper_push_six_sevenths_hand_dependencies.md`.
