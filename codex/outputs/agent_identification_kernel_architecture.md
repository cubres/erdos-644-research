# Identification kernels: a useful quantitative stress test

Status: no proof of the general kernel statement or Problem 644. The explicit
example below and endpoint implication use the previously certified capacity
catalogue (Theorem 7.69). Their arithmetic and deductions were independently
checked here; the catalogue was not replayed. New SMT UNSAT outputs are discovery
evidence only.

## What identification genuinely provides

Identifying two vertices preserves property (7,2), does not increase rank, and
reduces the transversal number by at most one. It reduces the transversal number
if and only if some minimum transversal contains both vertices. Consequently a
counterexample chosen first with the fewest vertices has the property that every
pair extends to a minimum transversal. This is a global constraint that local
avoidance games do not express.

The classical terminology is stronger vertex criticality: Remark 2 of Gyárfás,
Lehel and Tuza, *Upper Bound on the Order of tau-Critical Hypergraphs*, JCTB 33
(1982), 161–165, considers families for which every prescribed k-vertex set lies
in a transversal of size t+u. The present condition is their k=2,u=0. Their
available order estimates are far too large when both rank and transversal
number grow linearly. Primary paper:
https://users.renyi.hu/~gyarfas/Cikkek/15_GyarfasLehelTuza_UpperBoundOnTheOrderofTauCriticalHypergraphs.pdf

## A sharp dichotomy fails even above density 0.70

The tempting assertion "either tau <= 2k/3+o(k), or n-tau <= k+o(k)" is false
for pair-irreducible (7,2) families.

For any positive integer m, take disjoint parts A,B of sizes 11m and 215m.
Set k=128m. Include all k-subsets of B, and all k-sets with exactly 8m points in
A and 120m points in B. The continuous parameters are

    x=11/128, y=215/128, d=0, c=1/16.

For every one of the 42 complete capacity functions M, either M(d,c)>x or
M(1-d,1-c)>y; the smallest positive maximum of these two excesses is exactly
1/128. Thus the certified capacity criterion gives property (7,2), including at
each integer scale.

To hit all B-only edges requires at least 87m+1 points of B. After taking that
many, one must either take at least 3m+1 points of A to eliminate the mixed type,
or increase the B selection to 95m+1. Therefore

    tau = min((87m+1)+(3m+1), 95m+1) = 90m+2.

Every selection of exactly 3m+1 points of A and 87m+1 points of B is a minimum
transversal. Since both counts are at least two, every pair of vertices extends
to such a transversal. Hence the family is irreducible under any single vertex
identification preserving tau. Nevertheless

    tau/k -> 45/64 > 2/3,
    (n-tau)/k -> 17/16 > 1.

This is an obstruction to that particular structural dichotomy, not to the
original problem: its transversal density remains below 3/4.

## A quantitative endpoint theorem survives

Consider two types (0,1) and (c,1-c), where 0<c<1, in parts of capacities x,y.
Suppose the mixed blocking option is strictly optimal and uses both parts:

    x>c, y>1, x<2c,
    t = x+y-1-c.

The condition x<2c is exactly t<y-1+c; the A-only blocking option is unavailable
because the first type has zero A coordinates.

**Endpoint implication.** If this family has (7,2) and t>2/3, then

    c<1/4, and t+c/2<3/4.

This implication needs only four already-certified capacity functions, with
zero-based catalogue indices 1,9,20,28:

    M1(s,t)  = max(s, s/4+3t/2),
    M9(s,t)  = max(3s/2, 3s/4+t),
    M20(s,t) = max(s/2+4t/3, s+2t/3),
    M28(s,t) = max(4s/5+t, s+7t/8, 7s/6+2t/3, 4s/3+t/3).

For each listed M, property (7,2) requires M(0,c)>x or M(1,1-c)>y.

**Proof that c<1/4.** Suppose c>=1/4. Since x>c, M9 forces y<3/2.
For c>=1/4, M20(1,1-c)=5/3-2c/3. Thus either x<4c/3 or
y<5/3-2c/3.

First suppose x<4c/3. The hypothesis t>2/3 forces y>5/3-c/3. If c<=1/2,
this contradicts y<3/2. If c>=1/2, direct comparison of the four linear forms
gives M28(1,1-c)=5/3-c/3. Because M28(0,c)=c<x, this also contradicts the
necessary M28 exclusion.

In the other case y<5/3-2c/3. Together with t>2/3 this gives x>5c/3, so in
particular x>3c/2. M1 therefore forces y<max(1,7/4-3c/2). As y>1, we must
have c<1/2 and y<7/4-3c/2. Using x<2c then gives

    t = x+y-1-c < 3/4-c/2 <= 5/8 < 2/3,

a contradiction. Hence c<1/4.

**Proof of the tradeoff.** Now c<1/4. M9 and x>c give y<7/4-c. If x<3c/2,
this directly yields t<3/4-c/2. If x>=3c/2, M1 gives y<7/4-3c/2, and
x<2c again yields the same bound. This proves the implication. The mirror
endpoint c=1 follows by interchanging the parts and types.

Since alpha=n-t=1+c, the endpoint result is precisely

    alpha-1 < 2(3/4-t), when t>2/3.

Thus the excess ground-set size can persist strictly below the conjectured
extremum, but it is forced to vanish linearly as the extremum is approached.
Small exact optimization probes at c=1/100,1/20,1/10,1/5 return the supremum
t=3/4-c/2; these optimality outputs are not needed in the proof above.

## What remains genuinely global

The bounded exact SMT stress test also finds no interior two-type example with
0<d<c<1, a strictly minimal mixed blocking option, and t>2/3. No hand proof of
that interior assertion was extracted here. Equal minimum-cover options were
not included in this stress test.

For unrestricted families the coherent open bridge is the following:

**Quantitative critical stability target (unproved).** A rank-at-most-k family
with property (7,2), with every pair extendible to a minimum transversal, and
with tau>2k/3+o(k), satisfies

    n+tau <= 5k/2+o(k).

The endpoint theorem proves the corresponding normalized inequality in its
restricted model, since n+t=1+c+2t<5/2. For the complete family at the conjectured
extremum the proposed inequality is asymptotically an equality. It also permits
the irreducible counterexample above.

Combined with the Fano-partition bound tau<=3n/7+O(1), this bridge would imply

    7tau <= 3n+O(1) <= 15k/2-3tau+o(k),

and hence tau<=3k/4+o(k). This is a complete-proof architecture, not a completed
argument. No existing critical-order theorem establishing this linear bound
under local (7,2) was found in the bounded literature check. Pair extendibility
alone is insufficient, and the earlier sharp 2/3 dichotomy must not be used.

The substantive missing step is to turn pair extendibility plus local (7,2)
into either a large almost-complete residual core or an explicit small cover.
Incidence-critical witness systems could supply the additional local-to-global
constraint; no valid charging inequality doing this has been established.

Reproduction: `p644_agent_audit_kernel_two_type.py` checks the displayed example
with exact rational arithmetic and runs the bounded QF_LRA stress tests. Its
JSON output is saved beside this report as `agent_kernel_two_type_probe.json`.
