# A spanning good triple obstructs fixed-prefix seven-edge proofs

Status: the 9/5 lower bound below is proved by hand using a verified theorem of Füredi. The equality classification at 7/4 is also proved by hand. The numerical optimization suggests 11/6 is sharp, but that lower bound is NOT certified here. No claim about a new bound on f(k,7) is made.

## 1. The explicit barrier

**Proposition.** Let A_1,...,A_7 be k-element subsets of a finite set U of size N. Suppose A_1∩A_2∩A_3 is empty and A_1∪A_2∪A_3=U. If the seven sets cannot be pierced by two points, then N≥9k/5.

**Proof.** We can assume N<2k; otherwise the conclusion is immediate. For each point v let t(v)={i:v∉A_i} be its complementary incidence type. Non-two-pierceability says that all positive-mass types are nonempty and pairwise intersect. Normalize the mass of U to one, and put d=(N−k)/N<1/2. Each of the seven type coordinates has total mass d.

No positive type can have size one or two. Indeed, if t(v)⊆{i,j}, then every other positive type intersects {i,j}. Thus the union of coordinates i,j contains all mass, whereas its mass is at most 2d<1. A singleton is treated by repeating its coordinate or by the stronger bound d<1.

Let z be the total mass of types of size at least four. Summing the seven coordinate masses gives

    7d = Σ_t |t|w_t ≥ 3(1−z)+4z = 3+z,

so z≤7d−3.

The triple-type subfamily is an intersecting 3-uniform hypergraph on seven vertices. It contains no Fano plane. To see this, the spanning good-triple assumptions imply that every positive type t meets Q={1,2,3} in exactly one or two points. But for any Fano plane on these seven coordinates, either Q itself is a line, or a line is disjoint from Q. In the former case Q is a forbidden type with |t∩Q|=3, and in the latter case a forbidden type has |t∩Q|=0. Hence its seven lines cannot all occur among the triple types.

Füredi's fractional matching theorem says that a Fano-free 3-uniform hypergraph has fractional matching number at most twice its matching number. This statement is explicitly restated as Theorem 3.1 in the author-hosted paper of Chan and Lau linked below. Since our triple-type family is intersecting, its matching number is at most one. Assigning mass w_t/d to each triple gives a fractional matching, because every coordinate has triple mass at most d. Therefore

    1−z ≤ 2d.

Combining 1−2d≤z≤7d−3 yields d≥4/9. Hence k/N=1−d≤5/9, as required. ∎

The cited result is Z. Füredi, *Maximum degree and fractional matchings in uniform hypergraphs*, Combinatorica 1 (1981), 155–162, DOI 10.1007/BF02579271. Its required precise form was verified in Y. H. Chan and L. C. Lau, *On Linear and Semidefinite Programming Relaxations for Hypergraph Matching*, Theorem 3.1 (PDF page 11): https://cs.uwaterloo.ca/~lapchi/papers/hypergraph-old.pdf . The original DOI endpoint was inaccessible in this session; the hand argument above uses the theorem as a literature dependency, not as a newly reproved result.

The proposition applies to fewer than seven rows as well: repeat rows to obtain seven without changing two-pierceability or the distinguished first three rows.

## 2. Consequence for the current difficult seed

Consider a good triple of k-sets with pair-core sizes (.49,.49,.24)k and private parts (.27,.27,.02)k, with no other ground points. Its union U has size (3−1.22)k=1.78k. Assume k is divisible by 100 so all sizes are integral.

Take as an avoidance adversary the complete k-uniform family on U. Every deletion of at most .76k points leaves at least 1.02k available points, so an actual k-set avoiding the deletion always exists. Yet every seven-tuple containing the original three rows is two-pierceable, by the proposition, since 1.78<1.8.

Thus **no strategy whose final certificate contains this fixed spanning good triple can win against this adversary**, regardless of how it chooses its four additional rows, how it splits cells, or whether it uses an optimal three-bin cover. This is stronger than failure of a particular first request. Even arbitrarily many intermediate queries cannot help if the final bad tuple must retain all three original rows and every answer stays in U.

This is NOT a counterexample to Problem 644. The complete family on U does fail (7,2), and the missing bad tuple necessarily omits at least one original seed row. Indeed, for k divisible by 100 a standard Fano complement on 7k/4 points fits inside U.

The original triple also attains the minimum possible intersection sum among good triples inside U: for any good triple of k-sets on U, inclusion-exclusion gives S'=3k−|union|≥3k−N=1.22k. Thus adding all replacement-good-triple inequalities does not eliminate this particular fixed-prefix adversary.

This conclusion concerns the earlier globally minimum-S seed. It must not be silently transferred to the newer globally minimum-pair anchor: the complete family on U has minimum pair intersection 2k−N=.22k, whereas the displayed seed's smallest pair intersection is .24k. The new anchor normalization imposes additional information.

## 3. Hand uniqueness of equality in the seven-block bound

For completeness, suppose seven equal-sized complementary blocks cover all point pairs at N=7k/4. Then each complementary coordinate has normalized degree 3/7. The positive types are pairwise intersecting. As above no type has size at most two. The total incidence mass is exactly three, so every positive type is a triple.

Let w_e be the normalized mass of a positive triple e. Intersectingness gives

    9/7 = Σ_{i∈e} degree(i)
        = Σ_f w_f |e∩f|
        ≥ 1+2w_e,

and consequently w_e≤1/7.

Now preserve all seven coordinate degrees and choose an extreme feasible vector supported on the original triple family. It uses at most seven triples: more than seven incidence columns would have a nonzero linear dependence, and moving a sufficiently small distance in both directions along that dependence would preserve degrees and nonnegativity, contradicting extremality. Because all columns have size three, the degrees also preserve total mass one. The bound w_e≤1/7 applies to this new vector as well. It therefore has exactly seven positive triples, each of weight 1/7. Equality in the preceding displayed inequality implies that every two distinct triples meet in exactly one coordinate.

These seven triples form a Fano plane. Indeed, every coordinate has degree three; no pair of coordinates is repeated in two triples; the seven triples contain 7·3=21 pairs, exhausting all pairs of the seven coordinates.

Every original positive triple meets every line of this Fano plane. A nonline triple cannot do so: its three pairs lie on three distinct lines, accounting for six of its nine point-line incidences; its remaining three incidences account for at most three further lines. Thus at least one of the seven lines is disjoint from it. Therefore every original positive triple is itself a Fano line.

Finally the line weights are uniquely 1/7. If B is the 7×7 incidence matrix, then BB^T=2I+J, which is nonsingular; hence the prescribed degree vector determines the weights uniquely.

In particular, no three coordinates can meet all positive types in exactly one or two positions. A spanning good triple is therefore impossible at equality. Finitely many support families and compactness alone already give a positive gap above 7/4; the explicit 9/5 argument gives a usable gap.

## 4. Numerical 11/6 optimum and exact upper witness

A new 96-cell MILP minimized the total ground mass of seven rank-one rows, restricted to original incidence cells c with |c∩{1,2,3}|∈{1,2}. Binary support flags forbid positive c,d with c∪d=[7]. HiGHS reported an optimum 11/6 in 0.535 seconds. This is numerical optimization evidence, not an exact infeasibility certificate below 11/6.

Producer: `/Users/cubres/Documents/Clauding/erdos-hunt/p644_agent_audit_spanning_good_triple.py`.
Output: `/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_agent_audit_spanning_good_triple.json`.

There is, however, an exact rational realization at N/k=11/6. With bit 0 corresponding to row 1, use original incidence masks

    27, 38, 60, 77, 86, 106, 113

with respective masses

    2/6, 2/6, 1/6, 2/6, 1/6, 1/6, 2/6.

Their complementary types, now using 1-based coordinate notation, are

    {3,6,7}, {1,4,5,7}, {1,2,7}, {2,5,6},
    {1,4,6}, {1,3,5}, {2,3,4}.

They are pairwise intersecting, so the seven original rows are not two-pierceable. Direct summation gives mass one in every original row and total mass 11/6. Each original mask meets the first three bits in one or two positions. Thus this is a hand-checkable bad configuration with a spanning good triple whenever k is a multiple of six.

The rigorously established interval for the minimum possible ratio is therefore [9/5,11/6]. Proving that 11/6 is the exact minimum remains optional; the 9/5 theorem already excludes the stalled fixed-seed architecture.

## 5. Implication for the actual upper-bound attack

A proof at 3/4 must sometimes replace its seed. The minimum-pair anchored host oracle is a plausible mechanism: it gives actual rows with nearly full traces in prescribed hosts, and a new anchor can be selected after these rows are obtained. The barrier above shows why it is essential to allow the final seven rows to omit original anchors. It does not prove that the necessary replacement can be made with error tending to zero with the excess above 3/4; that is the remaining global step.

## 6. Stronger conclusion: even a small-intersection anchor pair cannot remain

**Proposition.** Suppose seven k-sets on an N-point ground set are not two-pierceable and N<9k/5. Then every pair of the seven rows has intersection at least 4k−2N.

**Proof.** Retain normalized complementary types and d=(N−k)/N from Section 1. If the positive triple-type subfamily contained no Fano plane, the identical Füredi argument would give N≥9k/5. Thus the triple types contain all seven lines of some Fano plane on the row coordinates.

Every positive complementary type meets every line of this Fano plane, because all positive types are pairwise intersecting. Such a blocking set contains a Fano line. For a set of at most three points, this follows from the nonline-triple counting argument in Section 3. A four-point set containing no line has a complementary line: its six point pairs lie on six distinct lines, each having a third point outside the set; each of the three outside points lies on at most two such lines, so each lies on exactly two. The remaining seventh line consequently contains all three outside points. Thus a four-point cap is not blocking. Finally, any set of at least five points contains a line: from one of its points, the other four occupy three lines, so two occupy the same line.

Choose a contained Fano line for each positive type and move that type's mass to the selected line. Write u_L for the resulting line masses and t_i for the resulting coordinate masses. Trimming only decreases coordinate masses, so t_i≤d. Also Σ_L u_L=1 and Σ_i t_i=3.

For any Fano line L,

    Σ_{i∈L} t_i = 1+2u_L,

because L meets every other line in exactly one point. Since the four coordinates outside L have total mass at most 4d,

    u_L = (Σ_{i∈L}t_i−1)/2 ≥ (3−4d−1)/2 = 1−2d.

Fix row coordinates i,j and let L be their unique Fano line. The original complementary types containing both i and j have mass at least u_L: all types assigned to L contained L before trimming. Therefore the normalized intersection mass of the two original rows is at least

    1−2d+u_L ≥ 2−4d.

Multiplying by N gives |A_i∩A_j|≥4k−2N. ∎

This proposition is a precise stability statement for the Fano configuration. In particular, if N<1.8k and a distinguished row pair has intersection at most .4k, that pair cannot occur in any bad seven-tuple on this ground set. At N=1.78k the required intersection is at least .44k.

Consequently the earlier complete-host adversary also defeats any strategy whose final seven-tuple retains the globally minimum pair (intersection .22k), even when the original third row is replaced. New residual good triples remain useful, but a final contradiction inside this host must omit at least one member of the anchor pair. This is a restriction on the proof architecture, not on the existence of unanchored bad tuples.

## 7. Every retained good triple must also be dense

Under the assumptions of Section 6, let A_i,A_j,A_h be any good triple among the seven rows, and write S for its pair-intersection sum. Then

    S ≥ 5k−2N,    |A_i∪A_j∪A_h| ≤ 2N−2k.

Indeed, the coordinate triple Q={i,j,h} meets every positive complementary type, since the three original rows have no common point. In particular Q meets every line of the positive Fano plane, so Q is itself a Fano line. The mass of complementary types containing Q is at least the trimmed line mass u_Q≥1−2d. This is the mass outside the union of the three original rows. Hence their union has size at most N−N(1−2d)=2N−2k, and inclusion-exclusion gives the assertion about S.

At N=1.78k, a good triple retained in a bad seven-tuple must satisfy S≥1.44k. A residual good triple with only the lower bounds |C_i∩C_j|≥.44k need not meet that threshold: the symmetric value S=1.32k still admits the same complete-host obstruction. Thus one must retain the full residual-origin constraints, or prove a stronger replacement property, rather than treating the three pair lower bounds as sufficient information.

## 8. Residual replacement: exact algebra and the missing invariant

For the minimum-pair anchored host oracle, use normalized rank one. Let m be the old anchor intersection, S the conditional minimum good-triple sum, and p=1−S+m the private mass of the selected third row. Every row avoiding the anchor intersection has at least 1−p points in the host V of size 2−2m. Consequently two residual rows intersect in at least

    2m−2p = 2S−2.

If the residual transversal number exceeds 1/2 (up to the integer constant), it contains a good triple C_1,C_2,C_3, whose sum obeys

    S_new ≥ 6S−6.

This is an increase whenever S>6/5. It is potentially useful for an iteration, but it does NOT itself iterate: the new triple need not minimize S among triples retaining any of its pairs, so the lower host-trace bound cannot be applied to it without a new argument.

An attempted shortcut also fails: from a pair of the new triple, select a third row minimizing its new sum, so that the conditional cover bound forces that sum back below 2−T. This is a legitimate actual-row choice under tau>T, but it can undo the density gained in the residual step. At a=(.44,.44,.44), an explicit admissible fourth-row profile

    x=(0,.30,.30), y=(.12,.10,.10)

has a replacement good-triple sum 1.24 and retains a numerical optimal three-bin budget .94. The row has .92 mass in the old triple union and .08 outside. This single numerical check is only diagnostic; the complete-host obstruction already explains why pair-density and the low replacement sum alone cannot force a winning fixed-prefix packing.

Thus the precise missing step is a global replacement invariant that preserves information about the original anchor residual while moving to a denser triple, and does not force the final bad tuple to retain either original anchor. No such invariant is proved in this report.

## 9. Sharper residual-union estimate (root improvement)

The residual good triple in Section 8 satisfies the stronger estimate

    |C_1∪C_2∪C_3| ≤ |V|+3p = 2k−2m+3p,
    S_new ≥ k+2m−3p = 2S_old−k−p.

This uses the common host V directly and is stronger than summing the three pairwise intersection lower bounds. At m=.24k and p=.02k it gives S_new≥1.42k. The necessary Fano threshold on the old union of size N=3k−S_old is 5k−2N=2S_old−k, so this replacement misses that threshold by at most exactly p. No argument removing or charging that remaining p is established here.

## 10. Quantitative Fano structure (root corollary)

The trimming in Section 6 proves a full structural statement. Partition the ground by the selected contained Fano line, writing P_L for each class. Define

    B_i = U \ (union of P_L over lines L containing i).

Then A_i⊆B_i: every point assigned to a line through i originally belonged to the complementary type at coordinate i. Each point lies in exactly four B_i, so

    Σ_i |B_i\A_i| = 4N−7k.

Moreover the line-mass identity gives both bounds

    2k−N ≤ |P_L| ≤ N−3k/2.

The lower bound was proved in Section 6. The upper bound follows from 1+2u_L=Σ_{i∈L}t_i≤3d, multiplied by N.

Thus a bad seven-tuple on N=(7/4+δ)k<9k/5 is obtained from a Fano-complement blow-up whose seven class sizes lie between (1/4−δ)k and (1/4+δ)k, by deleting a total of exactly 4δk incidences. This is an exact hand-proved structure theorem, with the same verified Füredi dependency as Section 6. It makes no assertion that an arbitrary high-transversal family contains a bad tuple or such a small union.
