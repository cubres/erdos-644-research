# Independent review of the all-rank exact-ceiling proof

26 September 2026. This is a fresh review of outputs/submission_644_rounding_push.md, separate from the earlier four-file referee report. I checked its integer endpoints, all three gap stages, the actual G0/G1/G2 requests, and the generalized finishing argument. I did not edit the proof or manuscript, rerun the old certificates, or use a numerical rank sweep as evidence.

**Conclusion:** the proposed hand argument establishes
\[
f(k,7)\le\left\lceil\frac{6k}{7}\right\rceil\qquad(k\ge8),
\]
subject to carrying the explicit domain and allocation statements below into the final manuscript. I found no missing rounding point, uncovered interval, host failure, or invalid seven-edge count. This is an internal independent mathematical check, not formal proof-assistant verification or external refereeing. It does not establish the \(3/4\) conjecture or settle \(k=7\).

## Two integration obligations, neither a missing mathematical construction

1. **State the exact gap domains.** Section 1 of the short report says only that \(L,H\) are integers. The standalone lemmas must specify \(0\le L\le H<k\). The actual applications satisfy this, and the v2 TeX already states it. The strict upper bound prevents the repeated-response issue in the previous referee report; nonnegativity ensures that the private cuts fit their hosts.
2. **Use the exact Hall criterion in Stage 2.** The old S0 lemma had narrower normalized hypotheses, including a distinguished pair of size at most \(3k/7\). The new proof allows that size to reach \(A=\lfloor T/2\rfloor\), which can be larger. This is valid because Section 4 checks all seven exact Hall inequalities and all nonnegative residual capacities. The manuscript should state that exact criterion, or explicitly apply the Hall allocation proof, rather than cite the old restricted lemma without explaining the extension.

Neither point changes any calculation or requires an additional edge. The authoring agent was notified.

## 1. Exact gap constructions

I read both the report's descriptions and the complete request proofs in work/submission_644_v2/local_closures.tex.

For G0, \(p=(k-x-y-H)_+\) and \(t=(k-x-z-H)_+\) fit their private cells because \(H\ge0\). The padding in the third edge fits since the initial request contains all pair cells and \(T\le k\). The response's two actual traces are at most \(H<k\), hence it is distinct from those earlier edges and the global implication makes them at most \(L\). If its remaining trace has size \(b\le k-T+x+p+t\), then
\[
x+\left\lceil\frac b2\right\rceil\le T
\]
follows exactly from \(k+3x+p+t\le3T\), with no extra parity point. All four triple cells vanish; the three requests cover the three complementary pair products.

For G1, \(x+y\le T\) makes the initial subset size valid. The only possible triple cell has size at most \(Q=(S-T)_+\). The two displayed trace conditions apply to actual intersections. Its split condition is exact because \(x,Q,T\) are integers:
\[
2x+2Q+k-y-z\le2T
\ \Longrightarrow\
x+Q+\left\lceil\frac{k-y-z}{2}\right\rceil\le T.
\]
The third base fits, and the displayed total-load inequality supplies the remaining private points of the opposite edge. All bases contain the triple cell and their union contains the opposite edge. This covers the additional triple-cell product as well as the three complementary products. No separate condition \(S\ge\beta k\) is needed.

For G2, \(g\le\min(x,z)\) and \(y+2g\le T\) are precisely the cut-host and initial-budget conditions. Completion inside the middle edge fits because \(T-y\le k\). The priority of pair-cell points gives \(p+q\le(S-T)_+\). Its final bases contain both triple cells, and the residual integral allocation fills the union of the two opposite edges. The total-load bound is \(3k-T+(S-T)_+\), controlled by the two final hypotheses. The candidate-pair list is exhaustive. The new statements therefore permit direct applications at the smaller exact budget.

## 2. Integer identities and validity of the intervals

Put \(k=7h+s\), \(0\le s\le6\), \(h\ge1\), and \(T=6h+s\). With \(r=\lfloor(h+2s)/3\rfloor\), I independently obtained
\[
A=3h+\lfloor s/2\rfloor,\quad B=3h+r,\quad
C=\left\lfloor\frac{5h+s}{2}\right\rfloor,\quad
D=2h+s-2r.
\]
In particular \(B\ge A\), since \(r\ge\lfloor s/2\rfloor\), and \(B\ge3h\).

For \(L=D-1\) and \(U=C-h\), the inequality \(L\le U\) is equivalent to
\[
2r+1\ge\left\lceil\frac{h+s}{2}\right\rceil.
\]
The report's bound \(r\ge\lfloor(h+s)/3\rfloor\) and its six-residue proof establish this for every \(h,s\). This is a finite algebraic verification of one floor identity, not an inference from tested ranks.

Writing \(h+2s=3r+t\), \(0\le t\le2\), gives
\[
4L-T=2t-2r-s-4\le0.
\]
Likewise
\[
(k-B-1+L)-T=s-3r-2\le-h-s\le0.
\]
Thus all three inequalities \(L\le U\), \(4L\le T\), and (III) hold universally.

An important scope point is that \(L\) need not be nonnegative before the early-termination test. For example \(k=13\) gives \(D=0\). This causes no problem: that rank terminates after Stage 1, and neither \(L\) nor the later gap lemmas is used. In the non-early branch \(B<\lfloor k/2\rfloor\),
\[
D=k+h-2B>h\ge1,\qquad
D=L+1\le C-h+1\le C.
\]
Consequently Stage 2 is a nonempty positive interval, and the later implication has \(0\le L<C<k\). The earlier implication uses \(0\le A\le B<k\).

## 3. First gap, including empty intervals and early termination

The first interval is exactly
\[
[A+1,\min(B,\lfloor k/2\rfloor)]
\]
among integer intersection sizes. Starting at \(A+1\), rather than \(A\), is essential.

For its cap request,
\[
2k-T-2C=3h+(k\bmod2)\le A+1.
\]
Thus the required nonnegative retained total \(2k-T-q\) can be split into two integer caps at most \(C\). Both caps fit because \(C\le\lfloor k/2\rfloor\le k-q\). Also \(C\le A\), so the distinguished pair \(x=q>A\) really is the largest pair in the symmetric case.

I checked the three local cases directly against L32, L31 and the exact S1 criterion. Their useful endpoint comparisons are
\[
B\le3T-2k,\qquad B\le2T-k,\qquad x\ge3h+1>2h.
\]
The first follows from \(T\ge4k/5\); the second needs only \(2T\ge k\). These control every term cited in the report. The case split is exhaustive, including equality in the second-case threshold.

If \(B\ge\lfloor k/2\rfloor\), the entire interval \((A,k/2]\) has been excluded, even when it was empty to begin with, and the finisher applies. If \(B<\lfloor k/2\rfloor\) but \(A=B\), Stage 1 is empty and the implication “trace at most \(B\) implies trace at most \(A\)” is tautological. Subsequent stages remain valid. For example, \(k=14\) has \(A=B=6\), \(C=5\), \(D=4\); the proof does not incorrectly require a nonempty first gap.

## 4. Second gap and the exact Hall allocation

The interval is \([D,C]\). Both retained caps can be at most \(B\), because \(q\ge D=2k-T-2B\); they fit their private hosts because \(q\le C\le\lfloor k/2\rfloor\) and \(B<\lfloor k/2\rfloor\). Stage 1 then bounds both actual response traces by \(A\).

If \(x+z\ge k-B\), G2 with orientation \((y,x,z)\), threshold \(H=B\), and trace bound \(A\) has valid hosts and request size
\[
\max(x,2k-x-2B)\le T.
\]
The other inequalities follow from \(2A\le T\), \(k+2C\le2T\), and
\[
3k+C+2A\le\frac{5k}{2}+2T\le5T.
\]

If \(x+z<k-B\), the proposed static allocation has \(a=y\le A\), \(b=x\le C\), and
\[
c=z\le T+B-k-1\le C,\qquad b+c\le k-B-1\le3T-2k.
\]
The seven Hall conditions were checked individually. In particular the potentially tight total condition is
\[
3k+a\le3k+T/2\le4T,
\]
which uses precisely \(T\ge6k/7\). Its residual capacities are nonnegative because \(A+C\le T\) and \(k-B-1\le T\). Thus the exact allocation applies despite the wider parameter domain than the old normalized S0 statement.

## 5. Third gap and parity cancellation

Now \(q\in[B+1,\lfloor k/2\rfloor]\). The same \(C\)-cap request fits because \(B\ge A\), and Stage 2 forces both response traces below \(D\), hence at most \(L\). The implication needed by G0/G1 is exactly “trace at most \(C\) implies trace at most \(L\).”

The identity
\[
J=2k-C+2\lfloor k/2\rfloor-3T
 =\left\lfloor\frac{h-s}{2}\right\rfloor
\]
is correct. When \(J\le0\), the branch \(z<J\) is empty; all nonnegative \(z\) enter the complementary branch.

For the first two local cases, (III) controls the asymmetric trace difference, and the rough bound
\[
k+2x+3z+y\le 2k+\frac{3h}{2}+2h+s
 =\frac{35h}{2}+3s\le3T
\]
is valid in the \(z<J\) branch.

For G0, I expanded both positive-part expressions independently. The first request is controlled by \(L\le C-h\) and \(x\ge B+1\ge3h+1\). In the split numerator the two middle terms fit by \(z\ge J\). The final term is bounded by
\[
4k-2C+2\lfloor k/2\rfloor-2T=6k-4T\le3T.
\]
The equality really cancels both parity contributions because \(C=T-\lceil k/2\rceil\). The third request has size at most \(4L\le T\).

For G1, \(Q=S-T\) in its branch. Its split and total-load expressions are bounded respectively by
\[
2T-3(k\bmod2),\qquad 3T-2(k\bmod2),
\]
as claimed. The remaining conditions follow from \(L\le C-h\), \(4L\le T\), and \(S\ge T\). No floor or ceiling error has been dropped.

The three stages therefore exclude every integer intersection in \((A,k/2]\). No ordering or uncovered-region assumption beyond the displayed early-termination branch is used.

## 6. Generalized finisher

The small-maximum argument is unchanged and its four exact arithmetic requirements hold for every \(k\ge8\). For the large-maximum branch, \(M\le T/2\) suffices to make the balanced request legal. Its other two traces are below \(3k/7+1/2\le k/2\), hence at most \(M\) by maximality.

For the local closing proposition, set \(c=T-k/2\) and \(h=k-T\). Since \(h\le c\), the four cases partition the sorted domain \(M\ge y\ge z\).

In case (i), the last L32 form after using \(y-z>M-h\) is below
\[
\frac{k-M+4y+3h}{3}
 \le\frac{k+3c+3h}{3}=\frac{5k}{6}\le T.
\]
The other L32 branch and all nine L31 forms fit. In particular the final L31 form requires only \(T\ge4k/5\), and the total term requires only \(T\ge4k/5\); both follow from \(T\ge6k/7\).

In case (ii), G2 uses \(H=\lfloor k/2\rfloor<k\), \(L=M\le H\). Its host sums exceed \(c+h=k/2\), and integrality supplies the odd-rank host size. Since the integer \(z>h\), its first request costs at most \(k-z+(k\bmod2)\le T\). All remaining conditions fit without rounding.

In case (iii), the four exact S1 forms are bounded by the four expressions in the report. The last, \((3k+3T/2)/5\le T\), uses exactly \(T\ge6k/7\).

In case (iv), substituting \((x,y,z)=(M,z,y)\) into the near-core lemma gives the listed common inequalities. For \(S\le T\), the omitted-core conditions suffice. For \(S>T\), the four residual conditions reduce to bounds by \(3k-3T/2\), \(3k-T/2\), \(3k-T/2\), and \(3k+T/2\), respectively. Each is controlled by \(T\ge6k/7\). The global maximum-small parameter remains \(M\), so the dichotomy in the actual near-core response proof is available.

Finally, the exclusion of \((A,k/2]\), with \(A=\lfloor T/2\rfloor\), is exactly the finishing hypothesis for integer intersection sizes. This completes the argument.

## Review boundary and provenance

Reviewed source:

- outputs/submission_644_rounding_push.md, 307 lines, SHA-256 8ed3dc17f89b6748ed1ce9ab795692b1701078769e015500765eacce13a192bf.
- Exact G0/G1/G2 proofs in work/submission_644_v2/local_closures.tex, 500-line snapshot, SHA-256 2f0c72c99da38b8de8e52ff27a2571857b25f5cc689769c11a345f5c7ea0ce41.

The earlier unchanged constructions were checked in the separate four-file referee review. I did not rerun the author's new rank sweep: its output is supplementary transcription evidence and is not needed for this review's universal conclusion. The aside about \(2\le k\le6\) and its classical reference was not independently rechecked here. The final integrated TeX must still be checked for transcription differences; this report reviews the proposed mathematical argument, not later edits.

