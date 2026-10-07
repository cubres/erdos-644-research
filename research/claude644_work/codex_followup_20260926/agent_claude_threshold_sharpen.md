# Sharpening Claude's threshold-family theorem

Status: new hand deductions from Claude's continuous threshold theorem and
his newly located hand proofs for two-part type sets and two threshold boxes.
No assertion about arbitrary hypergraphs or improvement of the general
coefficient is made. No computer certificate is needed for the results below.

I read Claude's `sec_threshold.tex` and `templates_handproofs.md` Sections
0, 2, and 3 in full, and checked their explicit V support, Gap-Pair
inequalities, closed two-part theorem, and direct two-threshold-box reduction.
These hand inputs supersede the older computer-assisted results originally
used while drafting this report. Sections 7.73--7.78 of the main note were
also inspected to avoid presenting their prior statements as new results.

## 1. Every continuous bad seven-tuple has a sparse realization

**Lemma.** Suppose seven prescribed nonnegative row profiles are continuously
realized on finitely many parts, using a support of membership cells with no
two cells whose union is all seven row labels. There is another continuous
realization which dominates every prescribed row load, fits the same part
capacities, uses only cells from the same bad support, and has at most seven
positive cells in each part.

**Proof.** Fix a part. Let its existing nonempty allowed cells be the columns
of a zero-one matrix A with seven rows. Let z be the prescribed seven row
loads in that part. Solve the covering linear program

    minimize 1^T c subject to A c >= z and c >= 0.

The given realization is feasible, so the optimum is at most the capacity of
the part. An optimum exists: intersect a feasible objective sublevel set with
the nonnegative orthant; that set is compact. Choose an optimum with the
fewest positive coordinates. If more than seven coordinates were positive,
their columns would be linearly dependent. There would be a nonzero vector d
supported on those coordinates with A d=0. For sufficiently small positive
and negative steps, c+epsilon d would remain nonnegative and feasible. At an
optimum, 1^T d must therefore be zero. Move in either direction until a
positive coordinate first becomes zero. This leaves the objective unchanged
and contradicts the chosen support minimality. Thus at most seven coordinates
are positive. Do this independently in every part. All resulting cells
belong to the original bad support, so no covering pair has been introduced.
This proves the lemma. QED.

**Integer rounding consequence.** If a part has integer capacity n after a
deletion, round its at most seven positive cell masses up. Their integer sum
is strictly less than n+7, hence at most n+6. A zero-capacity part stays empty.
After rounding, each row may independently be trimmed. Trimming only changes
an old membership cell to a subset, so it cannot create a covering pair.

This six-vertex allowance applies to every continuous bad seven-tuple, not
only to a Fano tuple and not only to a particular catalogue of supports.

## 2. Sharper uniform finite bound for arbitrary two-part type sets

The first argument below improves the prior additive 28 to 14. Section 7
gives root's subsequently found stronger bound
`floor(3(k-1)/4)+12`, using a lattice-generator perturbation.

**Corollary (hand proof).** Every k-uniform (7,2) family
invariant under permutations within two parts satisfies

    tau(H) <= floor(3k/4) + 14.

This improves the additive 28 in Corollary 7.76 of the existing note.

**Proof.** Delete min(6,n_i) vertices from each of the two parts and retain
the actual original edges avoiding them. Call the resulting type-closed
family H'. If tau(H)>3k/4+14, then tau(H')>3k/4+2. Its continuous coefficient,
using exactly its admissible integer type vectors, is at least tau(H')-2:
rounding down both coordinates of a continuous free vector proves this
standard bound. Consequently Claude's hand Theorem 7.75'
(`templates_handproofs.md`, Section 2) gives a
continuous bad seven-tuple with actual permitted row types of H'. Apply the
sparse-realization lemma, and round each cell mass up. The deleted six
vertices in each nonempty surviving part provide all the required room. A
part reduced to zero needs no room. Each row dominates its prescribed integer
profile and can be trimmed separately to precisely that profile. Thus all
seven resulting integer edges belong to H and have no two-point transversal,
a contradiction. A one-part surviving family uses the homogeneous Fano
construction; an empty H' contradicts the assumed positive transversal
number. Integrality gives the stated floor. QED.

## 3. Exact transversal formula for threshold unions

Let the ground set be partitioned into parts of integer sizes n_i, and let
some parts be boxes with integer thresholds 1<=t_i<=k. The family consists
of all k-sets whose trace in at least one box i has size at least t_i. Ignore
boxes with n_i<t_i. Assume the family is nonempty, and write N=sum n_i.
Then

    tau = min(N-k+1, sum_boxes (n_i-t_i+1)).                 (1)

Indeed, a residual set contains an edge if and only if it has at least k
points and meets some effective box in at least its threshold. Therefore its
maximum independent size is the greater of k-1 and the sum obtained by
retaining t_i-1 points in every box and every point of each nonbox. Taking
the complement proves (1).

For real rank r, capacities n_i, and real effective thresholds 0<theta_i<=r,
the identical argument, with suprema at strict boundaries, gives

    tau_cont = min(N-r, sum_boxes (n_i-theta_i)).           (2)

There is no need to replace theta_i by an effective lower bound arising from
the other capacities in order to obtain this exact formula.

## 4. The continuous threshold theorem covers every number of boxes

**Corollary (hand proof).** For a continuous threshold union of
rank r with any finite number of parts and any number of effective boxes,

    tau_cont > 3r/4

implies a bad seven-tuple.

For at least three effective boxes this is Claude's continuous threshold
theorem (which actually permits equality). For one effective box, (2) implies
N>7r/4 and n_i-theta_i>3r/4. Since theta_i<=r, the latter gives
n_i>7theta_i/4. Hence an admissible row fits coordinatewise below 4n/7, giving
the homogeneous Fano tuple. With zero boxes the family is empty.

For exactly two effective boxes, the following is Claude's hand argument
(`templates_handproofs.md`, Section 3), included to make clear why no
three-part computer certificate is needed. Normalize r=1. If the homogeneous
Fano construction is unavailable, both thresholds satisfy theta_i>4n_i/7;
otherwise N>7/4 lets us fill that low-threshold coordinate to a row below
4n/7. Put d_i=n_i-theta_i. Formula (2) gives d_A+d_B>3/4. It follows that
n_A+n_B>7/4 and theta_A+theta_B>1. Also 1-theta_B<=n_A: if the reverse held,
then n_B<7theta_B/4<7(1-n_A)/4, which together with
d_i<3n_i/7 would give d_A+d_B<3/4-9n_A/28, a contradiction. The mirrored
inequality holds too.

Thus the actual types (theta_A,1-theta_A) and (1-theta_B,theta_B), with zero
load outside A and B, are admissible. Their first coordinates are ordered as
a=1-theta_B<b=theta_A and satisfy

    4n_B < 7(1-a),  4n_A < 7b,
    b-a <= n_A+n_B-7/4.

Claude's hand Gap-Pair Lemma supplies a bad seven-tuple from Q_a, Q_b, or V.
For completeness, its proof is only scalar inequalities: the three
displayed assumptions give x>b+3a/4 and y>7/4-a-3b/4. These ensure all Q_b
facets except possibly 3b/2<=x, and all Q_a facets except possibly
3(1-a)/2<=y. If both fail, combining x<3b/2 and y<3(1-a)/2 with the gap
condition gives

    x>a+b,       x>5a/4+b/2,
    y>2-a-b,     y>5(1-a)/4+(1-b)/2,

so V is feasible in both parts. Its explicit bad support and realizing
allocations are in Section 0 of that same hand-proof file and were checked
here. This establishes the two-box case entirely by hand. No intersectingness
is assumed.

## 5. Uniform finite theorem with no padding or box-count hypotheses

**Theorem (hand proof).** Let T be any
k-uniform threshold union. Combine all nonbox parts into a single part and
discard empty parts and initially ineffective boxes (whose parts join the
nonbox part). Let s be the number of remaining parts. If T has property
(7,2), then

    tau(T) <= floor(3(k-1)/4) + 6s.                        (3)

In particular, if q is the number of effective boxes then s<=q+1. When every
part is an effective box, s=q. There is no assumption that n_i>=t_i+7, no
assumption that three boxes exist, and q may vary with k.

**Proof.** Suppose the asserted inequality fails. Delete min(6,n_i) vertices
from each of the s parts, and let T' consist of the original edges avoiding
these vertices. Its rank is still k, its surviving thresholds are still the
integers t_i, and

    tau(T') >= tau(T)-6s > 3(k-1)/4.                      (4)

In particular T' is nonempty. Denote its integer capacities by n'_i and its
number of effective boxes by q'>=1. For a positive epsilon<1 define a new
continuous threshold family on these same capacities with

    r = k-1+epsilon,
    theta_i = t_i-1+epsilon.

Its effective boxes are exactly the effective boxes of T', since the
capacities and original thresholds are integers. Also 0<theta_i<=r. By (1)
and (2), its continuous transversal coefficient is

    min(N'-k+1-epsilon,
        sum_effective (n'_i-t_i+1) - q' epsilon),

which is at least tau(T')-q' epsilon. By (4), epsilon can be chosen so small
that this is greater than 3(k-1+epsilon)/4. The continuous corollary therefore
provides seven bad rows, each of total mass r and meeting at least one
assigned box i in mass at least theta_i.

Compress its support separately in every surviving part by the lemma in
Section 1 and round its positive masses up. This fits in the original parts
because at most six vertices of padding per part are required; parts of zero
remaining capacity need none. Every row now has integer size at least
ceil(r)=k and has at least ceil(theta_i)=t_i points in its assigned box.
Choose exactly k of its points while retaining at least t_i points there.
The resulting row is an actual edge of T. All seven rows remain in the
downward closure of the original bad support, so no pair meets them all.
This contradicts property (7,2), proving (3). QED.

Distinctness of the seven constructed rows is unnecessary: if repeated rows
occur, discard repetitions. The resulting subfamily still has no two-point
transversal and has at most seven members, exactly the required convention.

### Comparisons and scope

* In Claude's original hypotheses with p parts and at least three padded
  boxes, (3) gives floor(3(k-1)/4)+6p instead of 3k/4+8p, and needs only his
  hand continuous theorem: after deleting six points, all three padded
  boxes remain effective.
* In arbitrary threshold unions, (3) removes both of his additional
  hypotheses. The two-box branch uses Claude's already established hand
  Gap-Pair proof; the finite rounding consequence is the new deduction.
* With at most two effective boxes and any number of nonbox parts, s<=3, so
  tau<=floor(3(k-1)/4)+18. With exactly two parts, s<=2 gives additive 12.
* For q=o(k), (3) proves the asymptotic coefficient 3/4 uniformly over these
  threshold unions, even when their number of parts is not fixed. If q is
  comparable to k, the additive term does not vanish. No result for general
  nonsymmetric families follows.

The rank perturbation k-1+epsilon is essential for the stronger constant in
(3): rounding an integer row back to k points requires only a continuous
row size strictly greater than k-1. Perturbing the threshold simultaneously
preserves its required ceiling t_i and removes the usual per-part loss in
comparing the finite and continuous transversal numbers.

## 6. Universal robust-profile transfer shift six

This further consequence was identified by root and checked here against
Claude's `capture/PROOF_ARCHITECTURE.md`, Section 2. It improves that file's
universal shift 14 (using Milner's theorem), or 31 (its elementary argument),
to **six, by an elementary proof independent of any support catalogue**.

Let H be any finite family on parts P_1,...,P_p of sizes n_i. For an integer
profile w let f(w) be the probability that independently chosen uniform
w_i-subsets of P_i together contain an actual edge of H. Fix eta<1/7 and
an integer s>=6, and define the robust integer profile set

    A = {u: 0<=u<=n integer, f((u-s*1)^+) >= 1-eta}.

**Transfer statement.** If there is a continuous bad seven-tuple whose rows
dominate seven integer profiles u^1,...,u^7 in A, then H fails (7,2).

**Proof.** Compress each part's cell allocation by the lemma in Section 1,
prescribing the seven integer loads u_i^j. The new continuous windows
dominate these integer loads, use at most seven positive cells per part, and
fit its original capacity. Round all cell masses down. In each part a given
row loses strictly less than seven mass, so its new integer window size is
strictly greater than u_i^j-7 and is therefore at least u_i^j-6. It is also
nonnegative. Put the unassigned vertices into the empty cell. All resulting
cells belong to the downward closure of the original bad support.

Independently for each part, uniformly distribute its actual vertices among
these fixed-size cells. Every individual row window is a uniform subset of
each part of its prescribed integer size, independently between parts. Its
profile dominates (u^j-s*1)^+, so monotonicity gives probability at least
1-eta that it contains an actual edge. A union bound over seven rows gives
positive probability that every window contains an edge. Choose such an
outcome and one actual edge in each window. Since no pair of cells covers
all seven rows, these at most seven edges are not two-pierceable. QED.

For clarity, when the prescribed load is a noninteger v, floor-rounding is
not guaranteed to leave ceil(v)-6 points. The argument uses the INTEGER
lower target u directly: an integer strictly greater than u-7 is at least
u-6. This is exactly what the robust-profile transfer requires.

Claude's completeness argument is unchanged and gives

    tau_int(A) >= tau(H)-sp,
    tau_cont(A) >= tau(H)-(s+1)p.

Consequently all conditional transfer statements in that architecture may
take s=6 with an additive **7p** instead of 15p (or 32p). In particular, with
RL and EL defined for this new shift-six robust profile family, the same
continuous type theorem as in the architecture implies

    tau(H) <= 3r/4 + RL(r) + 7p,
    tau(H) <= 3k/4 + EL + 7p.

Changing the shift changes A and hence RL and EL; these are not asserted to
be the old shift-14 values. The open continuous type theorem and tameness
conditions remain necessary. This is an improvement of a proved transfer
lemma, not a proof of those missing conditions or of Erdős 644.

## 7. Root's stronger lattice transfer: two-part constant twelve

This strengthening was supplied by root and independently checked here.
It combines the sparse-realization lemma with a coordinatewise perturbation
of the original integer generators, and supersedes the bound in Section 2.

Write Th(p) for the following continuous assertion: every closed nonempty
rank-r type set over p parts whose coefficient exceeds 3r/4 admits a
continuous bad seven-tuple. Claude's hand two-part theorem establishes Th(2).
Th(p) is not proved here in general.

**Conditional finite-transfer theorem.** Suppose Th(p) holds. Then every
k-uniform (7,2) family H invariant under permutations
within p parts satisfies

    tau(H) <= floor(3(k-1)/4)+6p.                          (5)

In particular, the UNCONDITIONAL HAND two-part consequence is

    tau(H) <= floor(3(k-1)/4)+12.                          (6)

Th(p) also implies Th(j) for j<p: append positive-capacity dummy parts in
which every allowed type has coordinate zero. This leaves the coefficient
unchanged; a resulting bad tuple can be trimmed to zero in those parts.
Thus empty parts arising after deletion cause no additional hypothesis.

**Proof.** Suppose tau(H)>3(k-1)/4+6p. Delete min(6,n_i) vertices from every
part, retaining actual original edges avoiding these vertices. Call the
result H', its integer capacities n_i, its total capacity N, its set of
admissible integer profiles A, and its transversal number t'. Then

    t' >= tau(H)-6p > 3(k-1)/4.

Consequently H' and A are nonempty. Every a in A has integer coordinates
and total k. For 0<epsilon<1 define

    g_i(a)=max(0,a_i-1+epsilon),
    G={g(a):a in A},
    r=k-1+epsilon.

If a has d>=1 positive coordinates, then

    |g(a)|=k-d(1-epsilon)<=k-1+epsilon=r.

Also 0<=g(a)<=n. We claim

    tau_cont(G)>=t'-p epsilon.                            (7)

Let u be any continuous free box for G. Put

    v_i=min(n_i,floor(u_i+1-epsilon)).

These coordinates are nonnegative integers. If some a in A satisfied
a<=v, then for every positive coordinate a_i we would have
a_i-1+epsilon<=u_i; a zero coordinate of g(a) is automatically at most u_i.
Thus g(a)<=u, contradicting freeness. Therefore v is an integer free box
for A. Moreover v_i>u_i-epsilon: this is the elementary floor inequality
unless the capacity cap is active, and in that case n_i>=u_i also gives
the strict inequality. Hence

    |u|<|v|+p epsilon<=N-t'+p epsilon.

Taking a supremum over free u proves (7).

Now take the rank-r upclosure

    C={c: |c|=r, 0<=c<=n, and g<=c for some g in G}.

C is a nonempty finite union of compact sliced boxes. A residual box u
contains a member of C exactly when |u|>=r and it contains a member of G:
if it contains g and has sufficient total capacity, increase coordinates
from g to attain total r. Therefore

    tau_cont(C)=min(tau_cont(G),N-r).

The elementary finite bound t'<=N-k+1 gives
N-r=N-k+1-epsilon>=t'-epsilon. Combining this with (7) yields

    tau_cont(C)>=t'-p epsilon.

Choose epsilon sufficiently small that

    t'-p epsilon>3(k-1+epsilon)/4=3r/4.

After omitting zero-capacity parts, Th(j) gives a continuous bad seven-tuple
with row types c^1,...,c^7 in C. For each row choose an original profile a^j
with g(a^j)<=c^j. Apply the sparse-realization lemma in each part and round
all its at most seven positive cell masses up. At most six vertices of
padding per nonempty part are needed, so the construction fits the original
parts before deletion. Parts reduced to zero have zero mass throughout and
need no padding.

Every rounded row has integer trace at least g_i(a^j). Crucially,

    ceil(max(0,a_i^j-1+epsilon))=a_i^j

for every nonnegative INTEGER a_i^j, including zero. Thus that row
coordinatewise dominates the ORIGINAL allowed integer profile a^j, not
merely its perturbed version. In every part trim the row to exactly a_i^j
points. It is now an actual edge of H, since H is invariant within parts.
Trimming preserves the absence of a covering pair. We have obtained a bad
subfamily of at most seven actual edges of H, a contradiction. This proves
(5). Claude's hand Th(2), together with the homogeneous one-part argument,
gives (6). QED.

The conditioning in (5) is essential. This improves the finite passage
whenever a continuous type theorem is available; it does not establish the
missing continuous theorem for three or more arbitrary parts. The threshold
theorem in Section 5 remains unconditional because its perturbed threshold
family stays inside the class Claude proved.
