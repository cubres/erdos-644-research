# Arbitrary overlapping private traces: global pruning and a private-count tail alternative

Status: hand corollaries of the EXISTING fractional bound in Section7.129
and the existing rounding argument in Section7.193. The cube-root
fractional theorem is not new. The useful new application covers the
ENTIRE actual private family, permits arbitrary E-trace overlaps, and
gives a quantitative alternative involving many large private families.

## 1. Polynomial total private count needs no overlap hypothesis

Let H be a finite rank-at-most-k (7,2) family, let E be an actual
nonempty edge, and let B be a disjoint (t-1)-cover of H minus {E},
where t=tau(H). Let P be the family of ALL actual private rows:

    P={F in H minus {E}: |F intersection B|=1}.

Suppose M=|P|>=1, and write W=(35k)^(1/3). Then there exist Q contained
in E and Z outside E such that

    1<=|Q|,
    |Q|+|Z|<=ceil(W log M)+2,                         (1)

Q union Z meets E and EVERY private row, and the ACTUAL residual

    K={F in H:F avoids Q union Z}

satisfies

    tau(K)>=t-ceil(W log M)-2.                        (2)

Every row of K has B_0-trace of size at least two, where B_0=B minus Z.
No assumption at all is made on intersections among the E-traces.
The argument also allows private rows whose E-traces are empty,
although that case is absent in an intersecting family.

Proof. P is an actual subfamily, so it has rank at most k and retains
(7,2). The old Section7.129 theorem gives tau_f(P)<=W. The old greedy
rounding bound from Section7.193 therefore gives a transversal S of
P with |S|<=ceil(W log M)+1. Put Z=S minus E and Q=S intersection E.
If Q is empty, add any one point of E to Q. This proves (1), and
Q union Z meets E and all private rows.

Every other original row has a nonempty B-trace. If it survives,
it avoids Z, so its B_0-trace equals its original B-trace. It cannot
have a singleton B-trace, since every original private row was met
by Q union Z. The surviving traces therefore have size at least two.
Adjoining Q union Z to any transversal of K covers H, proving (2).
Rank and (7,2) pass to this actual subfamily, as does intersectingness
when present. No projected trace is treated as an actual edge.

If M<=k^C for a fixed constant C, the loss in (1) is

    O(k^(1/3) log k)=o(k).

More generally log M=o(k^(2/3)) suffices. Thus allowing Q itself to
have o(k) points removes Section7.197's common disjoint-support
hypotheses in the stated small-M regime. Its stronger control |Q|<=2
does not follow from this proof, nor is it claimed.

For reference, the invoked old fractional theorem has this short
mechanism. Normalize any fractional matching of total weight w into
a row distribution and sample seven actual rows independently. By
(7,2), some point belongs to at least four indexed samples. With
p_v the one-row inclusion probabilities,

    1<=binom(7,4) sum_v p_v^4<=35k/w^3,

because p_v<=1/w and sum_v p_v<=k. LP duality gives the fractional
cover bound. This is a restatement of Section7.129, not a new proof
claim or an assumption on projected private traces.

## 2. Exponentially many rows at a few centers can also be absorbed

Let s=|B| and order the actual private-family sizes as

    q_1>=q_2>=...>=q_s>=1.

The positivity follows because B is a minimum cover of H minus {E}:
without a private row at a center, that center could be removed.
For 0<=r<s put

    M_r=sum_{i=r+1}^s q_i.

There are Q contained in E and Z outside E meeting E and ALL private
rows, with

    |Q|+|Z|<=r+ceil(W log M_r)+2.                     (3)

Proof. Put the first r center points into Z, covering every private
row at those centers. Apply Section1 to the actual remaining private
family of size M_r. This does not need that those rows form the full
private family of a new critical cover: they are an actual (7,2)
subfamily, which is all the fractional bound uses. Add the resulting
cover and, if necessary, one E-point. The same residual proof gives
minimum B_0-trace size two and loss at most (3).

Consequently, it suffices that all but o(k) centers have

    q_i<=exp(o(k^(2/3)))                              (4)

with a uniform little-o estimate. Since s<=2k-1, the number of
remaining private rows also has logarithm o(k^(2/3)). In particular,
o(k) exceptional centers may have arbitrarily large private families,
while every other center has polynomially many private rows. Arbitrary
overlap among their E-traces is still allowed.

This is useful because total M by itself can be enormous due to a
single center. Such concentration is harmless: that center point
costs only one outside-E point. The next conclusion quantifies the
only possible counting escape from (3).

## 3. Failure requires exponentially large private families at many centers

Let p=tau(P), where P is the entire private family. For every integer
0<=r<p-2,

    q_{r+1}>=exp((p-r-2)/W)/(s-r).                    (5)

Proof. Cover the first r private families by their center points and
round a fractional cover of the remaining actual family. This gives

    p<=r+ceil(W log M_r)+1<=r+W log M_r+2.

Thus M_r>=exp((p-r-2)/W). Since the sizes are ordered,
M_r<=(s-r)q_{r+1}, which proves (5). The condition r<p-2 ensures
r<s, because B itself is a p-cover upper bound p<=s; the logarithm
therefore concerns a nonempty family.

For example, if p>=delta*k for fixed delta>0, choose
r=floor(delta*k/2). For large k, there are at least r+1 centers
whose private families each have at least

    (1/(2k)) exp((delta*k/2-2)/(35k)^(1/3))           (6)

actual rows. Hence a linear private transversal number forces
exponentially many rows, on the scale exp(c k^(2/3)), at LINEARLY
MANY different critical-cover centers. A single complicated star,
or even o(k) complicated stars, cannot obstruct the small private
cover sought here.

Equivalently, the unrestricted-overlap route has the following actual
global alternative. Either the private rows have a sublinear common
transversal, yielding the desired excess-preserving pruning, or along
a subsequence there are linearly many centers each carrying at least
exp(c k^(2/3)) private rows for some positive c. This statement does
not bound the number of private rows of a general counterexample.

## 4. Remaining scope

Neither a polynomial M bound nor condition (4) has been deduced from
high tau and criticality. Equation (5) identifies the required
distributed complexity if these counting conditions fail; it does
not contradict it. The root's separate private-center encoding shows
why unrestricted removal of the counting condition requires additional
minimality or high-excess structure.

The resulting residual may retain all of the high transversal number
in its rows with larger B_0-traces. There is no proved rank decrease
and no claim that E remains critical after it is removed by Q.
Thus this is a global pruning reduction for arbitrary overlapping
private traces, not a proof of the three-quarter coefficient.
