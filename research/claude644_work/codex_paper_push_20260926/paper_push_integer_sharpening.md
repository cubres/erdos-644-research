# Removing three points from the general hand bound

26 September 2026. Hand proof. Read with
`paper_push_six_sevenths_hand_proof.md` and its dependency appendix. This
addendum changes only the integer implementation of those constructions;
the three rational gap exclusions and their scalar case divisions stay
the same.

## The strengthened theorem

For every integer k>=7, every k-uniform family with property (7,2) satisfies

    tau(H)<=ceil(6k/7)+1.

In particular the same bound holds for f(k,7). The leading coefficient
remains 6/7, so the general 3/4 conjecture is not resolved.

## An integral triangle-allocation lemma

Let m,y,z and L1,L2,L3,T be integers, with m,y,z>=0. Suppose there are real
numbers a,b,c satisfying

    0<=a<=m, 0<=b<=y, 0<=c<=z,
    b+c>=L1, a+c>=L2, a+b>=L3,
    a+b+c<=T.

Then there are integer a,b,c satisfying the same inequalities.

Proof. Minimize a+b+c over the compact polytope given by the box bounds
and the three pair-sum lower bounds. Its minimum is at most T and is
attained at a vertex. A vertex with an active coordinate bound is integral:
after fixing that coordinate at its integer endpoint, every nonsingular
two-by-two system formed from the remaining bounds has determinant 1 or -1.
If no coordinate bound is active, all three pair constraints must be
equalities. Their solution is either integral or has all three coordinates
half-integral. In the latter case round any two coordinates up and the
third down. Every pair sum weakly increases; all coordinate bounds hold
because their endpoints are integers. The new sum is the ceiling of the
old sum, hence is at most the integer T. This proves the lemma.

Apply this to the S1a construction with

    L1=k+m-T, L2=k+y-T, L3=k+z-T.

Its four request sizes are a+b+c, k+m-b-c, k+y-a-c, and k+z-a-b.
The real S1a construction at budget beta*k is feasible for these relaxed
inequalities whenever T>=beta*k. The integral lemma therefore implements
S1a at budget T itself, without an extra rounding allowance.

## The other local rounding allowances

Put b=6k/7 and T=ceil(b)+1. Throughout the argument T<=k, since k>=7.
The cap request starting each gap stage has size strictly less than b+2.
Its size is an integer, so it is at most ceil(b)+1=T.

L29, L31, L32, L33, the S0 Hall allocation, and the near-core/fullcore
allocations are already integral whenever their real bounds fit T.
S1a is integral by the preceding lemma. Only L35, L37, L46 and the old
small-maximum finisher require a closer estimate.

**L35.** Each use of h0=floor(h*k) introduces an error strictly less than
one. Its initial request C0 is consequently strictly less than b+2, and
fits the integer T. The numerator k+3x+p+t in its two split-request bounds
is strictly less than 3b+2. Each split request has size at most

    (k+3x+p+t-T)/2+1/2 < (3b+2-T)/2+1/2 <= T,

where the last inequality follows from T>=b+1. Its third final request
has size below b, as in the original proof. All hosts and padding choices
are unchanged.

**L37.** Its first two final bases have sizes at most b+1/2<=T; its third
base has size below b. The total-load argument distributes integer points
among integer residual capacities and uses only T>=b. Thus it fits T.

**L46.** Its first request has size strictly less than b+2 and hence at
most T. The rest of its proof uses only the original homogeneous budget
inequalities and T>=b, and all subsequent allocations are integral.

## The small-maximum finisher with the smaller budget

In the old Lemma L50 proof, the hypothesis T=ceil(beta*k)+4 can be replaced,
for beta=6/7, by T=ceil(6k/7)+1. Here are all affected inequalities, so no
old additive allowance is being silently imported.

Suppose the largest pair intersection at most k/2 is m<=2k/7. The first
balanced request gives other intersections at most k-floor((T+m)/2).
If both are at most k/2, their sizes are at most m and L18 fits T exactly
as before.

Otherwise the relabeled large intersection x satisfies

    x<=k-(T+m)/2+1/2,  m<=k-T.

The latter inequality is exact: T+m>=k+1 would force the new trace to be
at most k/2. Since T>=5k/6+1, we get m<=k/6-1<k/4 and

    x+2m <= (5k-4T+1)/2 < T,

the last inequality following from 6T>5k+1. The next core-avoidance request
therefore fits. If its opposite trace is small, use L18 again. Otherwise
the three requirements of L41 follow from

    ceil(k/2)+2m <= ceil(k/2)+2k-2T <= T,
    x+m <= 3k/2-T+1/2 <= T,
    2x+b'+ceil(k/2)+2m <= (9k+m-5T+4)/2 <= 3T.

Here b' denotes that opposite trace. For the last inequality use m<=k-T
and 12T>=10k+4. The other two require only

    3T>=2k+ceil(k/2),  2T>=3k/2+1/2,

which follow from T>=5k/6+1. Thus L50's entire construction fits the new T.

## Completion of the general proof

All three gap stages in the main hand proof now use this same T, proving
that no pair intersection lies in [3k/7,k/2]. Obtain a largest small
intersection M as before. If M<=2k/7, apply the preceding finisher.

If M>2k/7, take its balanced response. Its new traces Y>=Z obey

    M+2Y<=2k-T+1<=8k/7.

Also

    Y<=k-floor((T+M)/2)<3k/7+1/2<=k/2,

because T>=6k/7+1, M>2k/7, and k>=7. Consequently maximality gives
Y,Z<=M. These are exactly the hypotheses of the main proof's final
four-case local proposition. The strengthened integer implementations
above make every branch fit T. The near-core/fullcore allocations already
fit the larger integer budget by monotonicity of their capacities.

Every case produces at most seven original edges with no two-point
transversal, contradicting (7,2). Hence tau(H)<=ceil(6k/7)+1. QED.

No new computer certificate is needed for this improvement. It is based
on an integral allocation lemma and explicit integer budget inequalities.

The general-bound agent independently checked the triangle-allocation
lemma, every changed L35/L37/L46/L50 budget, the final balanced response,
the k>=7 boundary, and the transcription of this addendum. No numerical
sample is used as a substitute for one of those arguments.
