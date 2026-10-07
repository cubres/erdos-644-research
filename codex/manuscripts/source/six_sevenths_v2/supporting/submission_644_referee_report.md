# Internal skeptical reading of the four-file manuscript

26 September 2026. This report concerns the source snapshot identified below, before the separately planned v2 rewrite. It is an internal mathematical review, not an external referee report or an acceptance recommendation. I did not edit the manuscript, rerun research certificates, or repeat the literature search.

**Result:** I found no counterexample to the main six-sevenths argument in this snapshot. I found one genuine proof-domain issue in the generic gap constructions and one minor missing qualification in the allocation proof. Both admit local repairs and neither affects the displayed parameter choices in the main theorem. This is not a formal verification certificate.

## Findings

### P2 — The generic gap inference needs \(h<1\), or an explicit distinct-response argument

**Sources:** local_closures.tex:14, lem:gapempty at lines 235–269, especially line 259; the same inference appears in lem:gaptwo at line 374. The main applications use \(h=5/14,10/21,1/2\), so are unaffected.

The appendix permits \(0\le\ell\le h\le1\). Its proofs infer that an intersection with a response, bounded above by \(\lfloor hk\rfloor\), is smaller than \(\ell k\). Under the usual interpretation that a forbidden pair-intersection interval refers to distinct edges, this inference can fail at \(h=1\): a response may be the earlier edge itself. Repeated responses are explicitly allowed at lines 7–8.

Here are exact parameters demonstrating failure of the proof step. Let the family consist of eight pairwise disjoint 8-element edges, choose three as \(E,F,G\), and set
\[
k=8,\quad \beta=\tfrac34,\quad T=7,\quad
\ell=\tfrac14,\quad h=1,\quad x=y=z=0.
\]
The family has transversal number \(8>T\), and no two distinct edges have intersection in \([2,8]\). Every numerical hypothesis of lem:gapempty holds: its nonzero displayed forms are \(8/3\) and \(4\), all at most \(\beta k=6\). The construction has \(p=t=C_0=0\) and requests seven private points of \(G\). The allowed response \(H=E\) has \(|E\cap H|=8\), contradicting the asserted bound \(|E\cap H|<2\). The proposed third request would have eight points, exceeding the budget.

This is a counterexample to the inference and arbitrary-response implementation, not to the lemma's existential conclusion: the example already has a bad triple. It cannot invalidate the main theorem because its actual thresholds are strictly below \(k\). Nor is it a counterexample if “pair” is explicitly defined to include diagonal pairs, since the \(h=1\) premise would then be impossible for any nonempty family. That ambiguity should not be left to the reader.

**Repair obligation:** restrict the normalized gap parameter to \(h<1\), or state the integer version with upper threshold \(H<k\). A response whose trace is at most \(H<k\) is automatically distinct from the earlier edge, and the forbidden interval applies. The parent reports that the v2 rewrite is making this repair; its final source has not been reviewed here.

### P3 — Specify that the proposed total is nonnegative

**Source:** allocations.tex:28–33, proof of lem:triangle.

The equivalence “integral coordinates exist if and only if all three upper bounds are nonnegative and their sum is at least \(t\)” also needs \(t\ge0\). For example, with all \(M_i=1\), all \(L_i=-5\), and \(t=-1\), those two tests hold but no nonnegative coordinates sum to \(t\). The following display includes \(t\ge0\), and the theorem's maximum includes zero, so there is no defect in the allocation formula or any application.

**Repair obligation:** change “a proposed integer total” to “a proposed nonnegative integer total,” or append \(t\ge0\) to the equivalence. This is a local exposition correction.

## Main-proof and application checks

### Initial requests and interval boundaries

Checked general_bound.tex:149–164 and the three rows of Table 1. The host conditions \(0\le u,v(q)\le1-q\) hold on every complete interval, including endpoints. The request size is an integer strictly below \(\beta k+2\), which implies at most \(\lceil\beta k\rceil+1\). It would not generally imply at most \(\lceil\beta k\rceil\); the manuscript does not make that inference.

The established gaps reduce the Stage 2 traces from at most \(10/21\) to strictly below \(3/7\), and Stage 3 traces from at most \(1/3\) to strictly below \(4/21\). I checked every scalar form used in prop:gapone, prop:gaptwo and prop:gapthree against its cited lemma and orientation. The initial pair need not be largest except in the symmetric-lemma application, where it is: \(x\ge3/7>5/14\ge y,z\). Case boundaries are covered; the first and third excluded intervals join to give \([3/7,1/2]\).

### Conditional finishing proposition

Checked prop:localfinish, general_bound.tex:310–408, including the integer budget \(T_0=\lceil6k/7\rceil\).

- In Case 1, the last asymmetric bound is at most \(5/6\): \(4y-m\le3y\le15/14\), giving \((10/7+15/14)/3=5/6\) at line 329. No lower bound on \(m\) is missing.
- The surviving-triple-cell branch has \(m\ge1/7\), from \(y-z\le m-1/7\). Its two difference inequalities follow as written.
- In Case 2, the cited lemma is stated with a larger budget and a closed forbidden gap. The manuscript explicitly reconstructs the initial request, replaces strict trace bounds by weak bounds, and checks the downstream capacities. This is sufficient. Integrality gives \(Z\ge\lfloor k/7\rfloor+1\); the host sums \(mk+Z\ge yk+Z>k/2\) are at least \(\lceil k/2\rceil\), as needed for odd \(k\).
- In Case 3, the symmetric allocation's sorting and its three convenient conditions hold. Its exact integer criterion removes the rounding loss.
- In Case 4, the orientation is \((x,y,z)=(m,z,y)\), with gap parameter still \(m\). I substituted this into all nine near-core inequalities. The omitted-core domain holds for \(S\le6/7\); increasing the budget to \(T_0\) reduces the actual surviving-core bound. For \(S\ge6/7\), the four displayed inequalities are precisely the remaining near-core conditions.

### Conditional theorem, small ranks, and the main result

Checked thm:finish, general_bound.tex:410–443, against small_maximum.tex.

A small pair is obtained before taking its maximum, so that maximum is not over an empty set. The balanced request fits because \(M\le3k/7\le T\le k\). For \(M>2k/7\), the other traces are at most \(k/2\), and maximality bounds them by \(M\). At \(k=7\) the theorem uses budget 7; the local closure at budget 6 remains available under \(\tau>7\).

For the small-maximum branch I checked all four arithmetic requirements, including \(8\le k\le13\), \(k=14\), and \(k=T=7\). The large new trace forces \(m\le k-T\), rather than merely \(m\le2k/7\). The next request fits its private host, the four resulting edges have no triple cell, and the opposite-large-cell lemma's three hypotheses follow from the four arithmetic requirements.

If the fourth-edge trace is small, the proof applies the small-triple construction to \(E,G,H\), dropping \(F\). Thus it uses a forbidden subfamily of seven edges, although eight edges may have been collected over the search. This is valid under the at-most-seven convention.

The main theorem follows with \(T=\lceil6k/7\rceil+1\le k\) for all \(k\ge7\). I found no application relying on an unproved reduction to intersecting families.

### Smaller budget in the arithmetic corollary

Checked cor:arithmetic, general_bound.tex:465–502, directly against the request proofs. The generic gap lemmas are stated at \(\lceil\beta k\rceil+1\), but the corollary explains why their implementations fit \(T=\beta k\) for \(k=42n\):

- every fixed cap and threshold is integral;
- the empty-triple gap lemma has no threshold floor error, and its actual split is at most \(\lceil(3T-T)/2\rceil=T\);
- the surviving-triple lemma has integer base sizes bounded by \(T+1/2\), hence by \(T\);
- the two-triple lemma has an integral threshold and all remaining capacities are integral.

These are sufficient modifications, not invalid direct invocations of larger-budget statements. The second residue class follows by private padding; its ceiling calculation is correct.

## Local constructions checked

The checks below address the complete appendix dependency list, not only the new refinements.

| Label and source | Proof obligations checked |
|---|---|
| lem:balanced, general_bound.tex:116–130 | Equal splitting fits both private hosts; the trace floor identity is exact. |
| lem:triangle, allocations.tex:13–47 | Eight affine expansions, feasibility of the minimum, and integral filling. P3 is the only qualification needed. |
| lem:symmetric, allocations.tex:49–99 | Exact four-form criterion; the convenient conditions control the second form; pair-cell/private-cell and pair-cell/pair-cell coverage. |
| lem:hallstatic, allocations.tex:101–141 | Nonnegative residual capacities, all seven Hall inequalities for the three private source cells, and label coverage. |
| lem:nearcore, allocations.tex:143–239 | Exhaustive candidate list; both response cases; base loads; two-source Hall conditions; omitted-core variant. The global dichotomy is used on an actual trace, disjoint from the other relevant trace. |
| lem:smalltriple, local_closures.tex:17–40 | Nonnegative host selections, \(B\le k\), exact maximum formula for the fourth request, and all candidate-pair cases. Its different cell naming is local and consistent. |
| lem:split, local_closures.tex:42–70 | Initial private cut fits, \(S\le T\), both response branches, and all three complementary products. |
| lem:fourcase, local_closures.tex:72–169 | One surviving triple cell; all four cases; nonemptiness of the integer interval in Case 3; residual capacity; \(Q\times E\) and the three complementary products. |
| lem:asymone, local_closures.tex:171–202 | Private padding, nonnegative split capacities, both branches, complementary-product coverage. |
| lem:asymtwo, local_closures.tex:204–233 | Host feasibility, response cap, both split branches, residual allocation. |
| lem:gapempty, local_closures.tex:235–270 | Floor errors below two; the \(+1\) budget absorbs the split error; padding; three-product coverage. Subject to P2. |
| lem:gapsurvive, local_closures.tex:272–310 | Both \(S\le T\) and \(S>T\), including the rounding strip; trace bounds, base sizes, total capacity and exhaustive candidates. |
| lem:twolarge, local_closures.tex:312–342 | Nonnegative \(p,q\) fit their hosts; exact budget \(T\); existence of \(B_1\); last request even when \(B_1=B\); all complementary products. |
| lem:gaptwo, local_closures.tex:344–389 | Integer hosts after flooring, priority filling, two surviving triple cells, total capacity, exhaustive candidates. Subject to P2. |
| lem:smallmax, small_maximum.tex:2–65 | Maximum selection, large-trace parity implication, private padding, hypotheses of both possible closing lemmas. |

No probabilistic assumption, numerical feasibility result, or limit argument was needed. The proposed exact integer-gap rewrite should make the smaller-budget applications easier to assess; that rewrite is outside this snapshot.

## Snapshot and limits

All four files are under work/submission_644/. Line references and SHA-256 hashes:

    general_bound.tex  541 lines  2d5430573f437be59f6f5cb2f49dc81aee217e1a97616b538e9cfd748cc16142
    allocations.tex    239 lines  19a125c39cb5b8b79ad7a6bcd1b5c12b420213c4b736872ea60a3a31d3e561ba
    local_closures.tex 389 lines  a317f91f933137cb2265819a2aa54373c6c75403f297836add05f17467a7cc18
    small_maximum.tex   65 lines  94a457c069bd8cb9064954ebd3aba7af30255223ab9b3796b14ded3f48435418

I read the complete mathematical source, recomputed the local inequalities and checked the candidate-pair support arguments. I did not perform proof-assistant verification, establish novelty, or audit a later all-rank exact-ceiling theorem. Future modifications, including the proposed v2 integer-gap lemmas, need their own bounded change review.

