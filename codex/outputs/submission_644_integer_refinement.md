# Exact integer refinements of the six-sevenths proof

26 September 2026. New hand results, separate from the existing general theorem. The bound valid in every rank remains `tau <= ceil(6k/7)+1` for k>=7; the extra point is removed on two residue classes below. This note also sharpens the conditional finishing theorem and gives an exact closed form for the symmetric static construction. None of these results resolves the conjectured coefficient 3/4.

## 1. An exact boxed-triangle allocation criterion

Let M_1,M_2,M_3 be nonnegative integers and L_1,L_2,L_3 arbitrary integers. Assume

    L_i <= M_j+M_l  whenever {i,j,l}={1,2,3}.

The minimum of a_1+a_2+a_3 over integer vectors satisfying

    0 <= a_i <= M_i,    a_j+a_l >= L_i

is exactly the ceiling of

    max(0, L_1,L_2,L_3,
        L_1+L_2-M_3, L_1+L_3-M_2, L_2+L_3-M_1,
        (L_1+L_2+L_3)/2).                              (1)

This sharpens the earlier existence-only triangle allocation lemma.

Proof. For a proposed integer total t, the pair inequalities are equivalent to

    0 <= a_i <= min(M_i,t-L_i),   sum_i a_i=t.

Such integer coordinates exist if and only if all three upper bounds are nonnegative and their sum is at least t. Expanding the sum of the three minima as the minimum of its eight linear expressions gives exactly:

    t >= 0, L_1,L_2,L_3;
    t >= L_i+L_j-M_l  for distinct i,j,l;
    2t >= L_1+L_2+L_3;
    t <= M_1+M_2+M_3;
    L_i <= M_j+M_l.

The last three host inequalities are assumed. Each lower bound in (1) is at most M_1+M_2+M_3, so the ceiling of their maximum also satisfies the upper bound on t. Integral coordinates of that total can be filled successively within their integral upper bounds. This proves (1). The same argument without ceilings gives the real optimum. QED.

## 2. Exact symmetric static closing lemma

Let E,F,G be k-edges with empty common intersection. Let their three pair-cell sizes be m>=y>=z>=0 and set S=m+y+z. The symmetric four-request construction S1 has an implementation with all request sizes at most the integer T if and only if

    T >= max(k+m-y-z,
             (k+m)/2,
             (2k+m+y-z)/3,
             (3k+S)/5).                               (2)

In particular the least integer budget of this construction is the ceiling of the displayed maximum. This is a sharp statement about S1 itself, not an assertion that no other closing construction can do better.

Proof. Split the pair cells M,Y,Z into parts of sizes a,b,c and their complements. Let P_E,P_F,P_G be the original private cells. Use the four requests

    R_0=M_1 union Y_1 union Z_1,
    R_M=M union P_G union Y_2 union Z_2,
    R_Y=Y union P_F union M_2 union Z_2,
    R_Z=Z union P_E union M_2 union Y_2.

Their sizes are a+b+c, k+m-b-c, k+y-a-c, k+z-a-b. Apply the exact triangle criterion with hosts (m,y,z) and pair requirements

    L_1=k+m-T,  L_2=k+y-T,  L_3=k+z-T.

Its host requirements reduce, using m>=y>=z, to T>=k+m-y-z. Its three individual L_i<=T requirements reduce to 2T>=k+m. Its three two-L requirements reduce to 3T>=2k+m+y-z. Its total requirement is 5T>=3k+S. These are exactly (2).

Every pair piercing E,F,G is either in two different pair cells or in a pair cell and its opposite private cell. The latter pair lies in its corresponding request. For the former pair, if both points lie in subscript-1 parts, they lie in R_0; otherwise one of the other three requests contains them. Thus responses avoiding these four requests yield at most seven edges with no two-point transversal. QED.

## 3. A conditional finishing theorem with no additive allowance

**Theorem.** Let k>=8. Suppose H is k-uniform, has property (7,2), and every pair of distinct edges has intersection of size at most 3k/7 or greater than k/2. Then

    tau(H) <= ceil(6k/7).                              (3)

Private padding extends the statement to nonempty families of rank at most k, since it preserves the original intersections, property (7,2), and transversal number.

Put T=ceil(6k/7)=k-floor(k/7), and suppose tau>T. Every set of at most T points has an avoiding edge. A request consisting of T points of one edge shows that some pair intersection is at most k-T<k/2. Let M be the largest intersection at most k/2. Then M<=3k/7, and every intersection is at most M or greater than k/2.

### Small maximum: M<=2k/7

The proof of L50 works at this T. Here are its integer requirements explicitly, replacing its earlier convenient sufficient assumption T>=5k/6+1:

    6T>5k+1,       3T>=2k+ceil(k/2),
    2T>=3k/2+1/2,  12T>=10k+4.                       (4)

For k>=14 they follow from T>=6k/7: the respective real margins are k/7-1, at least k/14-1/2, 3k/14-1/2, and 2k/7-4. For 8<=k<=13, T=k-1, and (4) reduces respectively to k>7, k-3>=ceil(k/2), k>=5, and k>=8. Thus all four hold throughout the stated range.

For completeness, select a pair attaining M and make the balanced request of size T, including its intersection. Each new trace is at most k-floor((T+M)/2). If both traces are at most k/2, maximality bounds them by M, and L18 applies: its budget expressions (2k+2M)/3 and (3k+M)/4 are at most 6k/7 and 23k/28, respectively.

Otherwise relabel the large trace x>k/2. The other two pair cells have sizes at most M. Then

    x <= k-(T+M)/2+1/2,    M<=k-T<=k/7<k/4.

The request omitting all three pair cells and then padding in the opposite edge to size T fits, since

    x+2M <= (5k-4T+1)/2 < T.

Its two traces against the large-pair edges are below k/2 and hence at most M. If the opposite trace b is at most k/2, apply L18 to the appropriate triple. Otherwise b>k/2 and b<=k-T+x. The hypotheses of L41 follow from

    ceil(k/2)+2M <= ceil(k/2)+2k-2T <=T,
    x+M <=3k/2-T+1/2 <=T,
    2x+b+ceil(k/2)+2M
        <=(9k+M-5T+4)/2
        <=(10k-6T+4)/2 <=3T.

These are exactly (4). L41 produces the forbidden seven-tuple.

### A stronger local proposition: the balanced inequality is unnecessary

Suppose the full maximum-small gap holds with parameter M, and a good triple has sorted pair sizes

    0<=Z<=Y<=M<=3k/7.

Then the triple closes at integer budget T=ceil(6k/7). No hypothesis on M+2Y is needed. This simplification was identified independently by the parent agent during the integer refinement.

**Case 1: Y<=5k/14.**

* If Y-Z>M-k/7, L32(M,Y,Z) has its four budget expressions bounded by 6k/7, 6k/7, 11k/14 and 5k/6.
* If Y-Z<=M-k/7 but S:=M+Y+Z<3k/7, L32(Z,Y,M) has the last two expressions below 5k/7 and 16k/21, and the first two fit directly.
* Otherwise use L31(Z,Y,M). The assumption Y-Z<=M-k/7 implies M>=k/7. Its expressions Y+Z, k/2+Y, k/2+Z, k+Z-Y-M, k-Z+Y-M, k-S/3, (3k+S)/5, (k+Y+Z+2M)/3, (2k+3M)/4 fit T. Specifically, S<=M+2Y<=8k/7 gives (3k+S)/5<=29k/35; the penultimate expression is at most6k/7 and the last at most23k/28. The two difference expressions use M+Y-Z>=M>=k/7 and M-Y+Z>=k/7. All other bounds follow directly from the case assumptions.

**Case 2: Y>5k/14 and k/7<Z<=5k/14.** Use the full-maximum-gap L46 construction in orientation (x,y,z)=(M,Z,Y), with h=1/2 and lower threshold M. Its domain conditions hold since M+Z>=Y+Z>k/2. As these sums are integers, they are at least ceil(k/2), so its g-point cuts fit their hosts even when k is odd.

The exact initial request size is

    Z+2(k-Z-floor(k/2))_+
       =max(Z,k-Z+(k mod2)).

Because Z>k/7 and Z is integral, Z>=floor(k/7)+1; therefore this request fits T=k-floor(k/7). Assigning Z=k/7 to Case4 is essential to this particular parity estimate.

All remaining L46 inequalities fit without rounding: 2M<=6k/7, M+Y<=2M, k/2+Z<=6k/7, 3k/4<T, and

    (3k+S)/5 <=(3k+2M+5k/14)/5<=59k/70<6k/7.

The actual new traces are at most floor(k/2), hence at most M under the full gap. The remaining request allocations are integral.

**Case 3: Y>5k/14 and Z>5k/14.** Apply the exact symmetric lemma (2). Its four expressions are respectively strictly below or at most

    5k/7, 5k/7, 5k/6, 6k/7.

Indeed Y+Z>5k/7, M<=3k/7, M+Y-Z<6k/7-5k/14=k/2, and S<=3M<=9k/7. There is no rounding loss.

**Case 4: Y>5k/14 and Z<=k/7.** Apply the near-core or fully omitted-core construction in orientation (x,y,z)=(M,Z,Y), with global maximum-small parameter M. Its common inequalities follow from

    Y+Z<=4k/7<T,
    M+Y<=2M<=6k/7<=T,
    k+Z-Y<11k/14<T,
    2k+M-2Y<2k+3k/7-5k/7=12k/7<=2T,
    2k+2M-Y<5k/2<=3T,
    2M<=T.

If S<=T, the omitted-core inequalities additionally follow from

    k-M+Z<=k-Y+Z<11k/14<T,
    2k-2M+Y<=2k-M<23k/14<2T.

If S>T, put Delta=S-T. Its four remaining inequalities reduce exactly to

    k+Y+2Z<=2T,
    2k-M+2Y+Z<=3T,
    2k+M+Z<=3T,
    3k+Y<=4T.

Their left sides are at most12k/7, 18k/7, 18k/7 and24k/7, respectively, since Y<=M<=3k/7 and Z<=k/7. All allocations are integral at budget T.

This proves the local proposition.

### Completion when M>2k/7

Select a pair attaining M and make the balanced avoidance request of size T. The other two traces satisfy

    Y,Z <= k-floor((T+M)/2) <3k/7+1/2<=k/2,

where the last inequality holds for k>=7. Maximality of M therefore gives Y,Z<=M. The new local proposition closes the triple. Together with the small-maximum argument this contradicts (7,2), proving (3). QED.

## 4. An unconditional arithmetic improvement

For every integer n>=1,

    f(42n,7)<=36n,    f(42n-1,7)<=36n.                (5)

Both statements also hold for nonempty families of rank at most the indicated rank. Thus the existing unrestricted upper bound improves by one point on the residue classes0 and41 modulo42.

Proof. Set k=42n and T=6k/7=36n. Use the same three gap stages as the established hand theorem. All the fixed fractions used in cap requests and gap thresholds are integral at this rank:

    5k/14=15n, 10k/21=20n, k/3=14n,
    4k/21=8n, 3k/7=18n, k/2=21n.

The other cap in each stage is an integer because it is2k-T-q minus the first cap, with q the integer original pair intersection. Thus every initial cap request has size exactly T, with no floor loss. The scalar case divisions and their homogeneous estimates are unchanged.

L29,L31,L32,L33 and S0 are already integral whenever their homogeneous bounds fit T. Section2 makes S1 integral. In L35, h*k is an integer, so both its initial request and the bound on its split numerator have no threshold rounding error. That numerator is at most3T, and hence each split request has size at most

    ceil((3T-T)/2)=T.

Its third request is strictly smaller than T. In L37, each of the first two base sizes is an integer at most T+1/2, hence at most T; its remaining allocation uses only integral residual capacities and the homogeneous total bound. In L46, h*k is an integer, so the initial request fits T without any error, and the remaining allocations are integral. Therefore all three stages exclude the gap[3k/7,k/2] at budget T itself. The conditional theorem of Section3 completes the argument.

For k=42n-1, private-pad each edge to rank42n, preserving its transversal number and property(7,2), and apply the first assertion. Its bound36n equals ceil(6(42n-1)/7). QED.

## 5. Status of the unrestricted extra point

The earlier gap-exclusion proof does not immediately fit T=ceil(6k/7). For example, let k=7n with n odd and start Stage 1 from a pair intersection 3n. Its prescribed two trace caps are both 5n/2. Keeping both integer traces at most floor(5n/2) requires an avoidance request of size

    2k-3n-2floor(5n/2)=6n+1=T+1.

Thus merely replacing the budget in the existing proof is invalid for infinitely many k. This is an obstruction to that prescribed cap implementation, not to the desired stronger theorem: rounding one cap up yields a nearby response which may still close by another construction. The exact conditional result above isolates the remaining work entirely in the three gap-exclusion stages.

## 6. A single all-rank corollary

Combining the preceding arithmetic improvement, the established general hand bound, and the classical f(k,6)=k gives, for every k>=2,

    f(k,7) <= min(k, ceil(6k/7)+1, 36ceil(k/42)).

For k<7 the first term supplies the bound; for k>=7 the second term is the established theorem; the third follows by private padding to rank42ceil(k/42). The same inequality holds for nonempty families of rank at most k. This is a convenient presentation of the finite consequences, not a further leading-coefficient improvement.

Verification record: the parent independently checked the exact triangle criterion, the simplified local four-case argument, and the new integer finisher inequalities. All statements in this note have hand proofs; no sampled computation or exhaustive grid is used.
