# A hand finisher for the general six-sevenths proof

26 September 2026. New hand proof. This does not lower the general coefficient below 6/7. It replaces the earlier global finishing hypothesis 'all small intersections <=2k/7' by the substantially weaker 'all small intersections <=3k/7'.

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

## Consequence for the existing general certificate

The general 6/7 proof no longer needs to establish exclusions down to 143k/1000 or bridge the final middle interval. It suffices to certify the upper exclusion

    (3k/7,k/2].

The compression is now complete and independently replayed. The old 256 steps / 18,270 nodes are replaced by **three rational stages / 718 nodes**, using only seven static label templates. No numerical solver is needed to check the new artifact.

## General theorem with three gap extensions [C]

For every integer k>=1000,

    f(k,7) <= ceil(6k/7)+10.

This preserves the coefficient and additive constant of the existing Theorem 7.48. The new result is a substantially shorter proof. The conditional hand theorem above has the separate, smaller additive constant +4.

*Proof.* Put beta=6/7 and K=ceil(beta*k)+10. Suppose tau(H)>K. For a pair with intersection proportion q in [a,b], request an edge avoiding the intersection and enough private points to leave caps floor(u*k), floor(v(q)*k), where

    v(q)=2-beta-q-u.

The cap-host inequalities hold in the table below. The initial request costs at most beta*k+2 and gives a good triple. Its other two intersection proportions lie below u and v(a); previously excluded intervals remove the corresponding response ranges. All endpoints in the retained boxes may safely be included.

| Stage | New excluded interval for q | u=v(a) | Remaining response box | Exact nodes |
|---|---|---|---|---|
| 1 | [3/7,10/21] | 5/14 | [0,5/14]^2 | 378 |
| 2 | [4/21,5/14] | 10/21 | [0,3/7]^2 | 146 |
| 3 | [10/21,1/2] | 1/3 | [0,4/21]^2 | 194 |

Stage 1 is unconditional. Stage 2 uses only the gap from Stage 1. Stage 3 uses the gap from Stage 2; the full chronological record also retains the Stage 1 gap. The exact certificate covers each product of the displayed q interval and response box by tetrahedra, each wholly contained in a proved closing region. Every subdivision and region inequality is checked over rational numbers, including boundary points.

The local tools actually used are:

* Stage 1: one static label template, Lemma 7.31 and Lemma 7.32.
* Stage 2: six static label templates, Lemma 7.31 and Lemma 7.46 with gap [3/7,10/21].
* Stage 3: Lemmas 7.29 and 7.33, and the gap Lemmas 7.35 and 7.37 with gap [4/21,5/14].

The seven static templates are original indices 0,2,3,6,8,9,27; the stored artifact includes only these seven. The independent checker reconstructs their budgets from their label antichains, rather than trusting stored facets. No leaf uses the other adaptive region families, the single-trace lemma, the maximum-small-region lemma, or the trace-dichotomy lemma. In particular, the former final trace-dichotomy stage is unnecessary.

The finite rounding allowance is unchanged from Theorem 7.48: the initial cap request costs at most beta*k+2, static allocations cost at most ceil(beta*k)+9, and the hand closing lemmas cost at most ceil(beta*k)+4. These are separate requests, so these allowances are compared with K rather than added to one another. For k>=1000 all auxiliary budgets are at most k.

The three stages exclude [3k/7,k/2]. The conditional hand theorem above then gives tau(H)<=ceil(6k/7)+4<K, a contradiction. QED.

## Frozen certificate and replay

The final artifact is

    work/paper_push/general/six_sevenths_three_gaps_minimal.json

It has 21,173 bytes and SHA256

    bad247bf7bfd3661dcb412854567b3fef4ae80110d765577fdd6dbb17b5d077a

From this task's root directory, run

    python3 -S work/paper_push/general/check_three_gap_six_sevenths.py

The replay passes: three stages, 718 nodes, exclusions [4/21,5/14] and [3/7,1/2]. The wrapper checks the artifact hash and the exact final record, then states the implication using the new hand theorem. The older checker's line `PARTIAL EXCLUSIONS ONLY` concerns its superseded quarter-gap finishing criterion, and does not test the new hand finisher. Its counter `conditional_steps=3` counts the presence of a `prior_gaps` field, including the empty field at Stage 1; there are only two mathematically gap-dependent stages.

The replay imports only these standard-library checker files from `~/Documents/Clauding/erdos-hunt/`:

    p644_astra_one_trace_check.py
    p644_astra_global_bound_check.py
    p644_astra_frontier_check.py
    p644_astra_maxsmall_check.py
    p644_astra_interval_bound_check.py
    p644_astra_31_36_check.py

The mathematical dependencies also include the hand proofs cited above, the conditional finishing Lemma 7.50 for its m<=2k/7 branch, and the near-core/fullcore proofs in `outputs/paper_push_general.md`. The wrapper does not claim to formalize those hand proofs. The parent independently checked the new local lemmas and all four cases of the new finisher before this certificate was assembled.

Earlier compressed artifacts (138,115,7,5,3 stages, including the earlier 930-node three-stage version) remain preserved as discovery history. The frozen 718-node artifact is the one to cite. This compression does not improve the general coefficient below 6/7 and does not resolve the 3/4 conjecture.
