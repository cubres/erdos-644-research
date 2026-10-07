# Arbitrary complementary cores: maximum imbalance and propagated overlap gaps

Status: hand proofs unless explicitly labelled numerical discovery. This report
concerns a special case of Erdős 644, not the unrestricted problem.

Let \(\mathcal H\subseteq\binom Uk\), where \(|U|=2k\), be closed under
complementation in \(U\), and have property \((7,2)\). The edges may be an
arbitrary subfamily; there is no type-closure assumption. Write \(\tau=\tau(\mathcal
H)\). We use normalized masses with \(k=1\) when proving asymptotic statements.

## 1. Cofinal containment and the balanced eight-cell form

If \(\tau>T\), every set of at most \(T\) points is contained in an actual
edge: take an actual edge disjoint from the set and complement it. This is a
containment oracle, not a simultaneous arbitrary containment/avoidance oracle.

For three actual cuts, label the four even cells
\(000,011,101,110\) by \(P_0,P_1,P_2,P_3\), and their respective opposite cells
by \(M_0,M_1,M_2,M_3\). The balance equations imply that the four differences
\(|P_i|-|M_i|\) are equal. To see this, put \(d_i=|P_i|-|M_i|\).
The three row-balance equations are
\(d_0+d_1-d_2-d_3=d_0-d_1+d_2-d_3=d_0-d_1-d_2+d_3=0\),
which force equality. Complementing one cut changes the sign. Thus we may write

\[
 |P_i|=v_i+s,\qquad |M_i|=v_i,\qquad
 v_i\ge0,\quad s\ge0,\quad \sum_i v_i+2s=k.
\]

Define \(M\) to be the largest such nonnegative imbalance over **all triples
of actual cuts**. Repeated cuts are permitted. This is one global extremum;
no minimum-pair-count assumption is used below.

The three pair overlaps, after suitable choices of sides, are
\(s+v_0+v_1,s+v_0+v_2,s+v_0+v_3\). If their deviations from \(k/2\) have
absolute values at most \(\eta k\), Hadamard inversion gives

\[
 \left|v_i-\frac{k-2s}{4}\right|\le\frac32\eta k.
 \tag{1}
\]

## 2. Two global consequences of bounded imbalance

**Residual intersection bound.**
\[
 \tau\le M+1+\left\lfloor\frac{k+1}{2}\right\rfloor.
 \tag{2}
\]
Indeed choose a set \(S\) of \(M+1\) points. Three actual edges avoiding
\(S\) cannot have empty common intersection: their all-zero cell has at
least \(M+1\) points, and their all-one cell is empty, contradicting maximality
of \(M\). Thus the residual family is three-wise intersecting. The standard
greedy intersection-chain bound for a rank-\(k\), three-wise intersecting
family is \(\lfloor(k+1)/2\rfloor\). Adding \(S\) proves (2). If
\(M+1>|U|\), the displayed estimate is already vacuous. In particular the
range \(M\le k/4\) gives the desired asymptotic \(3k/4\) bound.

**Global overlap gap.** If \(\tau>T\), every actual pair has overlap in

\[
 [0,M]\ \cup\ [T-M,k-T+M]\ \cup\ [k-M,k].
 \tag{3}
\]

Proof. Write \(x=\min(a,k-a)\), where \(a\) is the pair overlap, and let
\(W\) be the union of the two opposite quadrants each of size \(x\).
If \(2x\le T\), contain all of \(W\) in an actual edge. The resulting
triple has imbalance \(x\), so \(x\le M\). If \(2x>T\), contain a
\(T\)-set in \(W\); the new imbalance is at least \(T-x\), so
\(x\ge T-M\). Reflecting \(x\) about \(k/2\) proves (3). Integer
versions use an integer \(T<\tau\).

## 3. A whole interval is excluded: maximum imbalance below 7/24

**Theorem (hand, asymptotic).** For every fixed \(\delta>0\), arbitrary
complement-closed \((7,2)\)-families as above satisfying
\(M\le(7/24-\delta)k\) have
\[
 \tau\le(3/4+o(1))k.
 \tag{4}
\]
Equivalently, any sequence of counterexamples with a fixed positive excess
over \(3k/4\) must eventually have \(M/k\ge7/24-o(1)\).

We prove the normalized, divisible-mass inequalities; all requests have size
\(3/4\). The concluding paragraph explains rounding. By (2) only
\(M=1/4+\eta\), with \(0\le\eta<1/24\), needs consideration.
Assume \(\tau>3/4\), so the gap (3) has the form

\[
 [0,M]\ \cup\ [3/4-M,1/4+M]\ \cup\ [1-M,1].
 \tag{5}
\]

First we construct three actual cuts with controlled cells. Fix an actual cut
\(A\), prescribe \(3/8\) points' mass on each side of \(A\), and contain
the prescribed set in an actual cut \(B\). Its overlap with \(A\) lies in
\([3/8,5/8]\). Since \(M<3/8\), (5) forces that overlap into
\([1/2-\eta,1/2+\eta]\). The two equally sized opposite \(A,B\) quadrants
therefore each have size at least \(1/2-\eta>3/8\).

Prescribe mass \(3/8\) in each of those two quadrants and contain the
prescribed set in an actual cut \(C\). Its overlaps with both \(A\) and
\(B\) again lie in \([3/8,5/8]\), hence in the middle interval of (5).
Choose the labels so that the two prescribed cells are \(P_0,P_3\). They
each have size at least \(3/8\). If \(a\) is the common size of the two
chosen \(A,B\) quadrants, the new signed imbalance is
\[
 t=|P_0|+|P_3|-a
   \ge3/4-a\ge1/4-\eta.
\]
It is positive, and global maximality gives \(t\le M=1/4+\eta\).
All three pair overlaps are within \(\eta\) of \(1/2\), so (1) gives

\[
 |v_i-(1-2t)/4|\le3\eta/2,
 \qquad v_0+t\ge3/8,\quad v_3+t\ge3/8.
 \tag{6}
\]

We now obtain a contradiction by a second containment request. Cube
symmetries allow any chosen index \(j\) to be relabelled as \(3\).

**Case I: \(t\ge1/4\).** Put \(r=t-1/4\) and select an index \(j\)
with minimum \(v_j\). Contain all of \(P_j\), the three minority cells
\(M_i\) for \(i\ne j\), and a subset of \(M_j\) of mass \(r\), in an
actual cut \(G\). The total is exactly \(3/4\). We first verify that
this request is legitimate and that

\[
 v_i<3/4-M-t\quad(i\ne j),\qquad
 v_j<3/4+t-3M.                                  \tag{7}
\]

Write \(d=t-1/4\in[0,\eta]\). The mean minority mass is
\(1/8-d/2\). From (6), every minority mass is at least
\(1/8-d/2-3\eta/2\), which exceeds \(d\) since
\(1/8-3d/2-3\eta/2\ge1/8-3\eta>0\). Thus \(r\le v_j\).
Every \(v_i\) is at most \(1/8-d/2+3\eta/2\), whereas
\(3/4-M-t=1/4-\eta-d\). Their difference is at least
\(1/8-3\eta>0\). Finally the minimum \(v_j\) is at most
\(1/8-d/2\), less than \(3/4+t-3M=1/4+d-3\eta\), again because
\(1/8+3d/2-3\eta>0\). This proves (7).

Take \(j=3\). The first two overlaps of \(G\) with the old cuts are at
least \(1-t-v_2\) and \(1-t-v_1\). By (7) these exceed \(1/4+M\),
so (5) forces each to be at least \(1-M\). Consequently
\[
 |G\cap P_2|\ge t+v_2-M,\qquad
 |G\cap P_1|\ge t+v_1-M.
\]
The overlap with the third old cut is therefore at least
\[
 r+v_0+v_1+v_2+2t-2M=3/4+t-2M-v_3>M.
\]
On the other hand, the prescribed part of that overlap has mass \(v_0+r\),
and the unprescribed part of \(G\) has mass \(1/4\). Thus the overlap
is at most \(v_0+r+1/4=v_0+t<3/4-M\). It lies in a forbidden gap of
(5), a contradiction.

**Case II: \(t<1/4\).** Put \(h=1/4-t\in(0,\eta]\). By (6), two
minority cells each have mass at least \(1/8+h\). The other two therefore
have total mass at most \(1/4\). Choose \(j\) among those two with
\(v_j\le1/8\). The inequalities needed below are

\[
 v_i<1/2-M\quad(i\ne j),\qquad v_j<1-3M.
 \tag{8}
\]

Indeed (6) bounds every \(v_i\) by
\(1/8+h/2+3\eta/2\le1/8+2\eta<1/4-\eta=1/2-M\), and
\(v_j\le1/8<1/4-3\eta=1-3M\). Both strict inequalities use
\(\eta<1/24\).

Contain the three minority cells other than \(M_j\), and all but mass
\(h\) of \(P_j\), in an actual \(G\). This request has total mass
\(3/4\). It is possible because \(|P_j|\ge t>h\) in the present range.
Again set \(j=3\). Its first two old overlaps are at least
\(3/4-v_2\) and \(3/4-v_1\), hence exceed \(1/4+M\) by (8).
Each is at least \(1-M\). Using the full capacities of the other cells
in those overlaps gives
\(|G\cap P_2|\ge t+v_2-M\) and
\(|G\cap P_1|\ge t+v_1-M\).
The third overlap is consequently at least
\(1-2M-v_3>M\), while its prescribed mass is only \(v_0\), so it is
at most \(v_0+1/4<3/4-M\). This is the same forbidden-gap contradiction.

For integer families with \(M/k\le7/24-\delta\), use subsets within a
bounded number of points of the stated masses. Every decisive strict
comparison above has margin at least \(3\delta k\); the construction and
each derived overlap change by only a bounded number of points. A fixed
positive excess \(\tau/k-3/4\) makes all rounded requests legal for
sufficiently large \(k\). Equivalently one may take a convergent subsequence
of the normalized cell masses and pass to these strict inequalities. This
proves the stated asymptotic theorem. No claim at the exact boundary
\(M/k=7/24\) is made here.

## 4. Exact constraints retained for the next extension

The regularized triple above obeys stronger constraints than (6). For a
general global bound \(1/4\le M<3/8\), it satisfies

\[
 1/2-M\le t\le M,\quad \sum_i v_i=1-2t,\quad v_i\ge0,
\]
\[
 3/4-M-t\le v_i+v_j\le1/4+M-t\quad(i\ne j),
\]
\[
 v_0+t\ge3/8,\qquad v_3+t\ge3/8.
 \tag{9}
\]

These are global consequences of cofinal containment and maximal imbalance,
not restrictions to a type-closed model. A new containment response must
preserve both the global imbalance bound and the global pair-overlap gap.
The current proof uses the simpler bounds (6); extending it should retain
the full polytope (9).

## 5. Precise limit of a one-response maximum-imbalance relaxation

When \(M\ge T/2\), the three overlap bands in (3) cover the entire
interval \([0,k]\). Furthermore maximum imbalance alone admits every
single containment request. Normalize \(k=1\), let \(w\) be any balanced
eight-cell vector, and prescribe \(0\le u\le w\) with \(\sum u=T\).
The fractional response
\[
 g=\frac{u+(1-T)w}{2-T}
\]
has \(u\le g\le w\) and total mass one. For any retained pair of old
cuts whose equally sized opposite quadrants have total mass \(2a\), its
new signed imbalance is
\((u(W)-Ta)/(2-T)\). The constraints
\(0\le u(W)\le\min(T,2a)\) and
\(u(W)\ge\max(0,T-2+2a)\) bound its absolute value by \(T/2\).
Thus all three replacement imbalances are at most \(M\).

This is a barrier to this **one-response relaxation**, not a construction of
a high-transversal \((7,2)\)-family and not an obstruction to using several
actual responses or their seven-row consistency.

## 6. Bounded numerical screen already completed

`work/p644_agent_alternative_core_lyapunov.py` tested the full-cell-plus-one-
partial-cell request menu for four states and the three potentials
\(Q+\lambda s^2\), \(\lambda\in\{0,1/2,9/10\}\), at containment
budget \(0.7501\). All twelve screens had surviving numerical responses;
the least reported best-response margin was about \(0.0234\).
Output: `outputs/agent_core_lyapunov_discovery.jsonl`.

This is **numerical discovery only**: local SLSQP does not certify its
maxima, and a vertex request menu does not exhaust nonlinear request
optimization. It has not been used as a theorem or as a general barrier.
The next work follows the global gap (9), rather than extending that broad
scalar-potential screen.

## 7. Recursive pair-gap amplification: the entire range M < 5/16

The preceding whole-range theorem can be strengthened without selecting a
regularized triple. The new argument uses **interior containment requests**;
testing only the vertices of the request polytope misses the mechanism.

**Gap-amplification lemma (hand).** Normalize \(k=1\), and suppose every
set of mass \(3/4\) is contained in an actual half-cut. Suppose all actual
pair overlaps belong to
\[
 [0,b]\cup[a,1-a]\cup[1-b,1],
 \qquad 0\le b<3/8,\quad 1/4<a\le1/2.
 \tag{10}
\]
If \(g=a-b>1/8\), they in fact belong to the same three intervals with
\[
 b\quad\hbox{replaced by}\quad b'=\max(0,b+1/4-a).
 \tag{11}
\]

Proof. Put \(\ell=1/4-g\). Suppose an actual pair has overlap
\(r\in(\max(0,\ell),b]\). Its four quadrants have sizes
\((r,1-r,1-r,r)\), in the order \(00,01,10,11\). We prescribe a
\(3/4\)-set with quadrant masses
\[
 u=(r,\ 3/4-r-p,\ p-e,\ e).
 \tag{12}
\]
Choose
\[
 \max(0,r-g)<e<\min(r,r-\ell).
 \tag{13}
\]
This open interval is nonempty: \(r>\max(0,\ell)\), and
\(g>1/8\) implies \(g>\ell\). Next choose
\[
 b-r+e<p<\min(a-1/4,\ 3/4-r+e-b).
 \tag{14}
\]
This interval is nonempty because \(e<r-\ell=r+a-b-1/4\), and
\(3/4-2b>0\).

The request (12) fits the four quadrants. Its first and fourth coordinates
are \(r\) and \(e\in(0,r)\). The third is positive, because
\(p-e>b-r\ge0\), and is less than \(a-1/4\le1/4<1-r\).
The second is nonnegative, since the second upper bound in (14) is at most
\(3/4-r\) (as \(e\le r\le b\)), and is at most \(3/4-r<1-r\).
The four coordinates sum to \(3/4\).

Let an actual \(G\) contain this request, and let \(x,y\) be its two
overlaps with the old cuts. The prescribed part of \(x\) is \(p\), so
\(x\le p+1/4<a\). Hence (10) forces \(x\le b\). The prescribed part
of \(y\) is \(q=3/4-r+e-p\). By (14),
\(b<q<3/4-b\). Thus \(y>b\) and \(y\le q+1/4<1-b\), so (10)
forces \(y\le1-a\). Consequently
\[
 x+y\le1-a+b=1-g.
\]
But \(G\) contains the entire \(00\) quadrant and at least mass \(e\)
in \(11\). Therefore
\[
 x+y=1-|G\cap00|+|G\cap11|\ge1-r+e>1-g,
\]
by (13). This is a contradiction. Complement closure reflects the exclusion
near overlap zero to the corresponding exclusion near overlap one, proving
(11). The proof uses one globally valid overlap set throughout.

**Corollary (hand, asymptotic).** For every fixed \(\delta>0\), arbitrary
complement-closed families on \(2k\) points with
\(M\le(5/16-\delta)k\) have
\[
 \tau\le(3/4+o(1))k.                           \tag{15}
\]
Property \((7,2)\) is not needed for this corollary.

**Nearness-cluster lemma (hand, finite).** Suppose a rank-exactly-\(k\)
family on \(2k\) points has all overlaps in
\([0,b]\cup[a,k-a]\cup[k-b,k]\), where \(2b<a\). Define two actual
edges to be near when their overlap is at least \(k-b\). This is an
equivalence relation: if \(A,B\) and \(B,C\) are near, then
\(|A\cap C|\ge k-2b>k-a\), so the allowed intervals force \(A,C\)
to be near. Suppose every \(q\)-set is contained in an actual edge and
\(q-1>k-a\). Choose containing edges for all \(q\)-sets. Adjacent
\(q\)-sets differ in one point, so their containing edges have overlap at
least \(q-1\) and lie in the same nearness class. Connectivity of the
Johnson graph forces all those edges into one class. Every actual edge
contains a \(q\)-set and is near that set's chosen edge, so the entire
family is one class. Fix \(E\) in the class. Any \(b+1\) points of
\(E\) hit every edge, because each other edge omits at most \(b\) points
of \(E\). Hence \(\tau\le b+1\).

To prove (15), use normalized masses first. The range \(M\le1/4\)
follows from (2). For \(1/4<M<5/16\), the initial global gap (5) has
\(a=3/4-M\), \(b=M\), and \(a-b=3/4-2M>1/8\).
The amplification lemma replaces \(b\) by \(b_1=2M-1/2\). Now
\[
 a-2b_1=7/4-5M>3/16,
 \qquad 3/4-(1-a)=1/2-M>3/16.
\]
Thus the nearness-cluster lemma applies with strict linear margins and
\(q\) close to \(3k/4\). It gives \(\tau\le b_1k+o(k)\), which is
inconsistent with \(\tau>(3/4+\varepsilon)k\). Only the first contraction
is needed.

Here is a precise way to absorb integer rounding. Fix
\(M/k\le5/16-\delta\) and a proposed excess \(\tau/k\ge3/4+\varepsilon\).
Choose any sufficiently small fixed \(\rho>0\), for example
\(\rho<\min(\delta,1/100)\). Apply the amplification request only to
normalized overlaps \(r\ge b_1+\rho\). Over this compact range, (13)
and (14) have uniformly positive slack, since
\(g-1/8\ge2\delta\). Round the four requested cell sizes and their
sum within a bounded number of points. The strict comparisons and the
containment budget remain valid for sufficiently large \(k\), excluding
all those overlaps. Therefore the finite family has allowed intervals with
near-width \((b_1+\rho)k+O(1)\). The two displayed margins still imply
\(2b<a\) and \(q-1>k-a\). The finite nearness-cluster lemma now gives
\(\tau\le(b_1+\rho)k+O(1)\), a contradiction. This completes the
asymptotic hand proof, without an assumption that a tiny cell can be split.

**Discovery provenance.** `work/p644_agent_alternative_pair_gap_closure.py`
found interior requests which the vertex menu misses. The proof above is
independent of numerical feasibility and is the certificate for (15).
The program's request samples are not a proof of full projection coverage.
At \(M=.32\), fourteen initial allowed overlaps, each tested against up to
1,000 interior requests plus the vertex menu, all survived. This is only a
bounded numerical observation and does not establish a global barrier.

## 8. General containment budget

The amplification proof works for a normalized containment budget \(T\),
with \(\beta=1-T\), by replacing \(1/4\) everywhere by \(\beta\).
Assume \(0\le b<T/2\), \(\beta<a\le1/2\), and \(g=a-b>\beta/2\).
The allowed set \([0,b]\cup[a,1-a]\cup[1-b,1]\) contracts to the same
set with
\[
 b'=\max(0,b+\beta-a).
\]
For an old overlap \(r>\max(0,\beta-g)\), choose
\[
 \max(0,r-g)<e<\min(r,r-\beta+g),
\]
\[
 b-r+e<p<\min(a-\beta,T-r+e-b),
\]
and prescribe \((r,T-r-p,p-e,e)\). The new two overlaps are respectively
at most \(b\) and \(1-a\), whereas their sum exceeds \(1-a+b\), exactly
as in Section 7. The request fits provided \(a-\beta\le1-r\); this is
automatic in the applications here, where \(a\le1/2\) and \(r\le b<T/2\).

Starting from the maximum-imbalance gap \(a=T-M,b=M\), amplification
applies when
\[
 M<(3T-1)/4,
\]
and yields \(b'=\max(0,2M+1-2T)\). If \(T>3/5\), this threshold
also ensures \(2b'<a\) and \(T>1-a\), so the finite nearness-cluster
argument applies with fixed margins. If \(a>1/2\), the residual bound (2)
already handles the corresponding range. This states a robust asymptotic
criterion for any fixed \(T>3/5\), rather than relying on a formal split
of a one-point cell.

## 9. Sharp one-pair response barrier at a balanced pair

This section is an **exact hand obstruction to a particular local
relaxation**, not a construction of a global hypergraph.

Let two old cuts have four quadrants of mass \(1/2\) each. Put
\[
 S_M=[0,M]\cup[3/4-M,1/4+M]\cup[1-M,1].
\]
For every \(M\ge5/16\), every request
\(u\in[0,1/2]^4\) of total mass at most \(3/4\) has an extension
\(g\in[0,1/2]^4\) of total mass one such that both new overlaps belong
to \(S_M\), and the new triple imbalance is at most \(M\).
Thus a balanced old pair cannot be eliminated by one request against the
**initial** global overlap restriction once \(M\ge5/16\).

It suffices to prove this for \(5/16\le M\le1/3\), since both \(S_M\)
and the permitted imbalance range increase with \(M\). Write
\(a=3/4-M\), \(U=1/4+M\), and \(c=2M-1/2\). The four request
coordinates are ordered \(00,01,10,11\). A side sum means a sum on one
side of either old cut; there are four such adjacent-pair sums.

We first give three sufficient response constructions.

**Corner response.** If
\[
 u_{01}+u_{11}\le M,\quad u_{10}+u_{11}\le M,\quad u_{11}\le c,
\]
then choose \(g_{11}=u_{11}=z\). Choose \(g_{01}\ge u_{01}\) and
\(g_{10}\ge u_{10}\), each at most \(M-z\), with their sum in
\([1/2-z,1-z-u_{00}]\). These intervals are compatible: the upper
sum capacity is \(2M-2z\ge1/2-z\); the lower requested sum is at most
\(1-z-u_{00}\); and \(u_{00}\le1/2\). Set
\(g_{00}=1-z-g_{01}-g_{10}\). The two overlaps are at most \(M\),
and all four cells stay between their prescribed lower bounds and \(1/2\).
The imbalance has absolute value at most either low overlap: for example
\(g_{00}+g_{11}-1/2\le g_{11}\le g_{10}+g_{11}\), and
\(g_{00}+g_{11}-1/2=1/2-g_{01}-g_{10}\ge-g_{10}\).

**Side response.** If
\[
 u_{10}+u_{11}\le M,\quad
 u_{01}+u_{11}\le U,\quad u_{00}+u_{10}\le U,
\]
there is a response whose first overlap is at most \(M\) and whose second
lies in \([a,U]\). Put
\(x=\min(M,1-u_{00}-u_{01})\). Then
\(u_{10}+u_{11}\le x\). Choose
\[
 g_{01}\in[\max(u_{01},1/2-x),\min(1/2,1-x-u_{00})],
\]
\[
 g_{11}\in[u_{11},x-u_{10}].
\]
Both intervals are nonempty. Their sum interval meets \([a,U]\): its
lower endpoint is at most \(U\), using \(u_{01}+u_{11}\le U\) and
\(1/2-x+u_{11}\le1/2\); its upper endpoint is at least \(a\), using
\(1-u_{00}-u_{10}\ge a\). Choose their sum in that interval, and set
\(g_{10}=x-g_{11}\), \(g_{00}=1-x-g_{01}\). This gives the claimed
response. The imbalance is again at most the low overlap \(x\).

**Central response.** A response with both overlaps in \([a,U]\) and
imbalance at most \(M\) exists whenever
\[
 \max_i u_i\le3M/2,\quad
 \text{every side sum}\le U,\quad
 u_{00}+u_{11},u_{01}+u_{10}\le1/2+M,\quad \sum u_i\le1.
 \tag{16}
\]
Here is a full elimination proof. Put \(h=M-1/4\). Such a response has
coordinates
\[
 \tfrac14+\tfrac12(s-X-Y),\quad
 \tfrac14+\tfrac12(-s-X+Y),\quad
 \tfrac14+\tfrac12(-s+X-Y),\quad
 \tfrac14+\tfrac12(s+X+Y),
\]
with \(|X|,|Y|\le h\) and \(|s|\le M\). These coordinates automatically
lie in \([0,1/2]\), because \(M+2h=3M-1/2\le1/2\).
Write \(A_i=2u_i-1/2\), \(L=\max(A_{00},A_{11})\), and
\(K=\max(A_{01},A_{10})\). For fixed \(s\), the four lower bounds
ask that \(X+Y\) lie in \([A_{11}-s,s-A_{00}]\) and \(X-Y\) lie in
\([A_{10}+s,-A_{01}-s]\). The square \(|X|,|Y|\le h\) becomes
\(|X+Y|+|X-Y|\le2h\). Hence the two intervals meet that diamond exactly
when they are nonempty and
\((L-s)_++(K+s)_+\le2h\). The latter condition is equivalent to
\(L+K\le2h\) and \(L-2h\le s\le2h-K\).
Thus it suffices that
\[
 [-M,M]\cap[u_{00}+u_{11}-1/2,1/2-u_{01}-u_{10}]
 \cap[L-2h,2h-K]
\]
be nonempty, and \(L+K\le2h\). Every comparison of a lower endpoint with
an upper endpoint follows from (16). The cross comparisons not literally
listed in (16), such as
\(u_{00}+u_{11}+2\max(u_{01},u_{10})\le2U\), follow by adding the two
relevant side-sum bounds. This proves the central construction.

We now classify an arbitrary request of total at most \(3/4\).
If every side sum is at most \(U\), and some side sum is at most \(M\),
a side response applies. If all side sums exceed \(M\), the three cells
other than any chosen cell have total greater than \(M\). Thus each cell
is less than \(3/4-M\le3M/2\), since \(M\ge5/16>3/10\).
The opposite-pair sums are at most \(3/4<1/2+M\), so (16) applies.

Otherwise some side sum exceeds \(U\). Its opposite side has sum less
than \(3/4-U=1/2-M\le M\). If the two transverse side sums are both at
most \(U\), a side response applies. If one transverse side sum also
exceeds \(U\), orient the square so that the two large sides meet at
\(00\). Their two opposite sides have sums at most \(M\). If
\(u_{11}>c\), adding the two large-side inequalities gives
\[
 \sum u_i>2U-u_{00}+u_{11}\ge2U-1/2+c=4M-1/2\ge3/4,
\]
a contradiction. Therefore \(u_{11}\le c\), and a corner response
applies. This exhausts the possibilities and proves the barrier.

The threshold is sharp for this balanced-pair relaxation. For
\(M<5/16\) sufficiently close to \(5/16\), prescribe a full \(00\)
quadrant, just over \(M-1/4\) in each of \(01,10\), and just over
\(2M-1/2\) in \(11\). Its total can be less than \(3/4\).
A response's two overlaps are each less than \(3/4-M\), because
\(g_{00}=1/2\), so the global gap forces both at most \(M\).
Then \(g_{01},g_{10}\ge1/2-M\), leaving
\(g_{11}\le2M-1/2\), a contradiction.

This does not prove that the *whole* one-dimensional closure operator
stabilizes: removing other overlaps could strengthen the initial set
\(S_M\), after which this response construction need not respect that
stronger set. It also does not couple responses chosen for two different
old pairs. Those are the next global consistency questions.

## 10. Shared-cut consistency adds a strict restriction

The one-pair barrier does not extend automatically to several actual pairs.
For \(5/16\le M<1/3\), any three actual **pairwise balanced** cuts must
have imbalance
\[
 t\le2M-1/3.                                  \tag{17}
\]
Indeed their minority masses all equal \(v=1/4-t/2\). Suppose
\(t>2M-1/3\). Then \(1/4<t\le M<1/3\), so a request consisting of
one whole \(P_j\), the other three minority cells, and mass \(t-1/4\)
of \(M_j\), is legal and has size \(3/4\). Its first two old overlaps
are at least \(1-t-v=3/4-t/2>1/4+M\), because
\(t\le M<1/3\). The global gap forces them to be at least \(1-M\).
As in Section 3, the third overlap is then at least
\(3/4+t-2M-v>M\), using \(t>2M-1/3\), and is at most
\(v+t=1/4+t/2<3/4-M\). This is impossible.

More generally, if the three pair correlations have absolute values at most
\(e\), the interval
\[
 2M-1/3<t<\min(1/3-e,\ 1-2M-3e)
 \tag{18}
\]
is excluded. The deviation bound (1) guarantees every minority cell is
large enough for the same partial request and ensures the first two
high-overlap conclusions. Select a minimum minority cell for \(j\);
its mass is at most the mean, which gives the same last lower bound as in
(17). Thus (18) is a global restriction on actual triples, using only the
same global maximum \(M\).

In particular a pairwise-balanced triple attaining \(M\) is impossible
for \(M<1/3\), even though each of its old balanced pairs separately admits
**every** request against the initial gap by Section 9. This is the first
explicit compatibility obstruction beyond the sharp one-pair relaxation.

## 11. Lexicographic replacement at a middle-band boundary pair

Among the triples attaining the global maximum \(M\), choose one minimizing
\[
 E=\sum_{i=0}^3\left(v_i-\frac{1-2M}{4}\right)^2.
\]
Hadamard orthogonality gives the exact identity
\[
 E=\sum_{\{i,j\}\subseteq\{1,2,3\}}
       (|A_i\cap A_j|-1/2)^2.                 \tag{19}
\]
This is a genuine lexicographic extremum; it is not simultaneous minimum
pair count and maximum imbalance.

Put \(h=M-1/4\), and suppose \(1/4<M<1/3\). If the selected triple has
an old pair whose overlap, after complementation if necessary, is
\(a=3/4-M\), then
\[
 E\le2h^2.                                   \tag{20}
\]
To prove this, let \(W\) be that pair's two opposite quadrants, each of
size \(a\). Prescribe a \(3/4\)-set entirely inside \(W\), with totals
\((3/4+h)/2\) and \((3/4-h)/2\) in its two quadrants. Both totals lie
strictly between \(M\) and \(a\), because \(M<1/3\), so this is a
legal request. A containing actual edge \(G\) has
\(|G\cap W|-a\ge3/4-a=M\). Maximality forces equality: its new triple
has imbalance exactly \(M\), and its trace on \(W\) is exactly the
prescribed set. All remaining mass \(1/4\) lies outside \(W\).

The two overlaps \(x,y\) of \(G\) with that old pair must both be in
the middle band \([1/2-h,1/2+h]\): their prescribed lower bounds exceed
\(M\), and their upper bounds obtained by adding \(1/4\) are less than
\(1-M\). Moreover \(|x-y|=h\), determined by the unequal prescribed
quadrant totals. Therefore
\[
 (x-1/2)^2+(y-1/2)^2\le h^2.
\]
The retained old pair contributes \(h^2\), so the replacement triple has
imbalance \(M\) and variance at most \(2h^2\). Minimality proves (20).

This removes the exposed state
\(v=(.195,.055,.055,.055),\ M=.32\): its three squared pair correlations
sum to \(3(.07)^2\), whereas the forced replacement has variance at most
\(2(.07)^2\). The request's two quadrant totals can be \(.41,.34\).
An equal \(.375,.375\) request would leave two endpoint responses with
unchanged variance; the unequal request removes both endpoints at once.
The strict improvement has quadratic scale, so bounded integer rounding is
harmless when the old pair is at the exact corresponding boundary.

If an old overlap is only near \(3/4-M\), this request only forces a
near-maximizing triple. It does not automatically qualify for the exact
lexicographic comparison. That distinction remains a substantive gap.

## 12. A smaller-variance state survives the bounded lexicographic probe

A natural next state is
\[
 t=M,\qquad v=(1/8,1/8,3/8-M,3/8-M).
\]
Exactly one old pair has boundary correlation \(h=M-1/4\), while the
other two pairs are balanced. Its variance is \(h^2\). A replacement
retaining the boundary pair already contributes that entire amount, so it
cannot improve the variance. To defeat this lexicographic test it suffices
to keep the replacements retaining balanced pairs strictly below \(M\).

**Numerical discovery, bounded scope.**
`work/p644_agent_alternative_core_lex.py` tested this state at \(M=.32\)
against all 183 box-simplex request vertices and 200 interior requests.
Every tested request admitted both balanced-pair replacements with
imbalance at most \(.25\), while preserving all three old/new pair gaps
and the bound \(M\) on the remaining replacement. This is not an
all-request certificate.

Here is an exact response to the request with the smallest reported slack.
In binary cell order \(000,001,010,011,100,101,110,111\), divide all the
following integer vectors by 200:
\[
 w=(89,11,11,89,25,75,75,25),
\]
\[
 u=(0,0,0,75,0,75,0,0),\qquad
 g=(11,0,0,75,0,75,39,0).
\]
Then \(u\le g\le w\), \(\sum u=3/4\), and \(\sum g=1\).
The three new overlaps are \(.57,.57,.75\), all allowed. The three
replacement imbalances are \(.25,.07,.14\), all strictly below \(.32\).
Thus exact maximum-imbalance lexicography makes no comparison with any of
these replacements. The eight actual rows formed by the three old
complementary pairs and \(G,G^c\) are even two-pierceable together: a point
in old cell \(000\) lying in \(G\), and a point in old cell \(111\)
lying in \(G^c\), have opposite four-coordinate patterns. Both have
positive mass in the displayed response.

This explicit response is a local state transition, not a high-transversal
family. Further progress must couple another actual response or use global
information not captured by this exact lexicographic one-step comparison.

**Exact floor of the boundary-equality variance method.** Every maximal
replacement forced by prescribing \(T\) points inside the opposite
quadrants of a boundary pair retains that pair. By (19), that pair alone
contributes \(h^2\) to the new variance. The two-two state above already
has variance exactly \(h^2\). Therefore even an iterated pipeline using
only these boundary-retaining equality replacements cannot force a value
below this state. This is an obstruction to that particular potential
argument, not to using the seven-row condition or another global quantity.
A maximal replacement retaining an interior pair would evade this floor,
but a single containment request does not in general force such a
replacement to attain \(M\).

## 13. One further actual cut: exact bounded certificates

The exact eight-row survivor of Section 12 was extended by a fifth actual
cut and its complement. The test retained all ten triples' imbalance bounds,
all ten actual-pair overlap gaps, the variance lower bound on every triple
attaining the maximum, and every seven-row subfamily of the resulting ten
literal rows.

**[C] Bounded result.** All 24 selected whole-cell/one-partial requests had
exact rational responses. Five additional targeted requests, completed
before the menu was closed, contained both endpoints of two of the old
four-coordinate antipodal components. These also had exact responses. The
29 requests are distinct. Every resulting ten-row family has a common
piercing pair, so this bounded test forced no new seven-row obstruction.
It does not cover all legal requests.

Reproduce the two menus with:

```
python3 work/p644_agent_alternative_core_second.py
python3 work/p644_agent_alternative_core_second.py --components
```

Certificates are in `outputs/agent_core_second_discovery.jsonl` and
`outputs/agent_core_second_components.jsonl`. The script's `inspect()` uses
`Fraction` throughout to check all row sizes and inclusions, all pair gaps,
all ten triple inequalities and conditional variance inequalities, and all
120 seven-row subfamilies. Numerical LP is used only to discover the
rational responses. No infeasibility claim is made from this menu.

## 14. A surviving ten-row state now admits a small endpoint deletion

Use targeted component request 3. In the four-coordinate atom order
\[
 0000,0001,0010,0100,0110,0111,1000,1011,1100,1101,1110,
\]
the old masses, request, and fifth actual cut are respectively the following
vectors, divided by 200:
\[
 w=(78,11,11,11,14,75,25,75,36,39,25),
\]
\[
 u=(0,11,0,0,14,75,25,0,0,0,25),
\]
\[
 g=(27,11,10,0,14,75,25,13,0,0,25).
\]
Their totals are \(2,3/4,1\), and \(u\le g\le w\).
The new overlaps with the old four cuts are \((63,114,137,99)/200\),
which lie in the allowed bands. The six newly created triple imbalances,
in retained-pair order \(01,02,03,12,13,23\), are
\((27,24,50,63,23,10)/200\), all strictly less than \(M=64/200\).
The only maximal triple remains the original one, with variance
\(196/200^2\). All these assertions are checked exactly in the cited
certificate.

A pair pierces all ten literal rows exactly when its five-coordinate
patterns are opposite. Directly listing the positive atoms shows exactly
two complete bipartite components in this piercing graph:

| First atom | Mass in units 1/200 | Opposite atom | Mass in units 1/200 |
|---|---:|---|---:|
| 00101 | 10 | 11010 | 39 |
| 01000 | 11 | 10111 | 13 |

Consequently the union \(D\) of these four atoms has mass
\[
 |D|=(10+39+11+13)/200=73/200.
\]
An actual edge avoiding \(D\), available under \(\tau>3k/4\), destroys
**every common piercing pair of the ten old rows**. This is a further
five-cut request; it was not tested in either preceding menu, whose
requests created the fifth cut. Removing the common pairs of ten rows
alone does not yet violate the seven-row hypothesis.

**Minimality of this pure avoidance request (hand).** For a guarantee
based only on the request, every endpoint of every common pair must be
included. If a smaller deletion set omits an endpoint \(x\), let \(y\)
be any partner of \(x\). There is a \(k\)-set avoiding the deletion,
containing \(x\), and excluding \(y\): the available ground set has at
least \(k\) points because the deletion has size below \(3k/4\).
Then \(x,y\) still pierce both that new cut and its complement, as well
as the ten old rows. Thus \(D\), of size \(73k/200\), is the smallest
whole-current-cell deletion forcing the disappearance of all old common
pairs independently of further global constraints. The same conclusion
holds even if arbitrary subsets of cells are allowed.

For comparison, a minimum vertex cover of the old piercing graph has size
\((10+11)k/200=21k/200\), but deleting one side of each component leaves
pairs crossing the new cut and its complement available. It is not a
substitute for the endpoint-union request. A next test can spend the
remaining \(77k/200\) of the \(3k/4\) budget on additional current cells,
while retaining the forced deletion of \(D\).

## 15. The focused endpoint deletion survives all seven-row checks

Before extending the ten-row sample, all \(\binom{10}{6}=210\) six-row
endpoint unions were checked exactly. Their minimum is
\(248/200=1.24\), attained twice. Thus the sample is not already excluded
by a six-row endpoint transversal of size at most \(3k/4\). One minimum
occurs at literal row indices \((1,2,3,4,5,8)\), where rows \(2j,2j+1\)
are the two sides of cut \(j\).

Only the single request from Section 14 was then tested: contain the full
endpoint union \(D\) of size \(73/200\), equivalently take an actual
complementary cut avoiding \(D\). No further menu was searched.

**[C] Exact response.** In current five-coordinate atom order
\[
 00000,00001,00011,00100,00101,01000,01101,
 01111,10001,10110,10111,11000,11010,11101,
\]
the masses, request, and sixth actual cut are the following vectors,
divided by 200:
\[
 w=(51,27,11,1,10,11,14,75,25,62,13,36,39,25),
\]
\[
 u=(0,0,0,0,10,11,0,0,0,0,13,0,39,0),
\]
\[
 g=(101/2,53/2,1/2,1/2,10,11,4,67/2,10,1/2,13,1/2,39,1/2).
\]
The exact checker verifies all 792 seven-row subfamilies, all fifteen
pair-overlap gaps, all twenty triple imbalance inequalities, and the
conditional variance inequality on every triple attaining \(M\).
Every newly created triple has imbalance strictly below \(64/200\);
the largest new imbalance is \(56/200\). The original maximal triple
still has variance \(196/200^2\).

The smallest six-row endpoint union in this twelve-row extension is
\((469/2)/200=469/400\), again greater than \(3/4\). Thus this next
state also passes that necessary global-transversal test.

Reproduction and exact certificate:

```
python3 work/p644_agent_alternative_core_third.py
```

Output is saved in `outputs/agent_core_third_endpoint_request.json`.
The script first recomputes the old six-row minimum, tests the one focused
request, and then verifies the displayed rational response with `Fraction`.

**Hand consequence:** the resulting twelve-row sample has transversal
exactly three. It has no common piercing pair: every pair piercing the ten
old rows has both endpoints in \(D\), hence both lie in the sixth cut
and miss its complement. Conversely choose any old piercing pair and add
one point in the sixth cut's complement; these three points meet all twelve
rows. The failure of two-pierceability therefore occurs only across more
than seven rows, fully consistently with all the local checks.

This is a precise limitation of the selected next-response attempt. It is
not a high-transversal construction, does not certify every possible next
request, and does not settle the complementary-core upper bound. The local
request expansion has stopped at this concrete verified transition.
