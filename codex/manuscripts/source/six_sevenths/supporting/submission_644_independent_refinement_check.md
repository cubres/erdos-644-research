# Independent check of the new integer refinements

26 September 2026. Checked by the literature/certificate agent at the parent's request. This is a bounded hand check of the new claims in `outputs/submission_644_integer_refinement.md`, against the actual request constructions in the two six-sevenths hand-proof files. It does not claim another independent audit of every older lemma. No computational test is used as a proof here.

**Conclusion:** no flaw found in the exact S1 budget, the removal of the balanced-response hypothesis from the all-small triple proposition, the conditional bound for every \(k\ge8\), or the unconditional refinements at ranks \(42n\) and \(42n-1\).

## 1. Exact S1 criterion

For fixed integer total \(t=a_1+a_2+a_3\), the constraints are exactly

\[
0\le a_i\le\min(M_i,t-L_i),\qquad\sum_i a_i=t.
\]

The eight expansions of the sum of these upper bounds give the stated individual, pair, total and host inequalities. Their lower bounds on \(t\) are bounded above by the integer \(\sum M_i\), using the assumed host conditions. Thus taking the ceiling of their maximum is legitimate; integer coordinates can fill any integer total up to the sum of the three integer upper bounds.

Substituting \(L_i=k+M_i-T\) and \((M_1,M_2,M_3)=(m,y,z)\), the largest individual, pair, and host conditions occur respectively at \(m\), \(m+y-z\), and \(m-y-z\). This gives exactly the four forms in (2). This proves necessity and sufficiency for the specified S1 requests. Their coverage of the two candidate-pair classes also checks directly.

## 2. All-small triples need no balanced-response condition

I checked the four cases against the exact inequalities of L31, L32, L46 and the near-core/omitted-core construction. All four cover their boundaries correctly. Three potentially compressed steps are worth making explicit in a paper.

In Case 1's first branch, write \(d=Y-Z>M-k/7\). The last L32 expression is

\[
\frac{k+2M+4Y-3d}{3}.
\]

If \(M\le k/7\), use \(Y\le M,d\ge0\); if \(k/7\le M\le5k/14\), use \(Y\le M,d>M-k/7\); if \(M\ge5k/14\), use \(Y\le5k/14,d>M-k/7\). The respective bounds are at most \(13k/21\), \(5k/6\), and \(5k/6\). Thus the stated \(5k/6\) bound holds without a missing lower bound on \(M\).

In Case 2, L46 is used with the full dichotomy “at most \(M\) or greater than \(k/2\),” so its new traces are bounded by \(M\), rather than strictly below \(M\). Its later base-load bounds only need the weak inequality. The initial cut size is exactly

\[
k-Z+(k\bmod2)\le k-\lfloor k/7\rfloor=T,
\]

because \(Z\) is an integer greater than \(k/7\). The host inequalities hold integrally because \(M+Z\ge Y+Z>k/2\). The remaining L46 allocation conditions are homogeneous inequalities in \(T\) and integer residual capacities. No hidden extra rounding point remains.

In Case 4, substitute \(x=M,y=Z,z=Y\) into the near-core hypotheses. For \(S>T\), moving the \(\Delta=S-T\) term to the right gives exactly the four displayed inequalities in the refinement note. Their bounds use only \(Y\le M\le3k/7\) and \(Z\le k/7\). For \(S\le T\), the omitted-core variant really omits the two conditions arising solely from the now-isolated private cell. Thus the asserted case split is valid at integer budget \(T\).

## 3. Conditional theorem, including \(8\le k\le13\)

The four small-maximum integer requirements hold directly for \(T=k-1\) in this range. In the large-trace alternative of that argument, the balanced-response inequality forces \(M\le k-T\): otherwise \(T+M\ge k+1\) would bound the trace by \(\lfloor k/2\rfloor\), a contradiction. This supplies the stronger bound on \(M\) used in the later requests; it is not being assumed from \(M\le2k/7\).

The subsequent four-edge configuration has empty triple cells, its two cross traces are below \(k/2\), and its remaining large trace obeys \(b\le k-T+x\). Substitution into L41 gives precisely the four integer requirements recorded in the note. The padding request fits its private host because \(T\le k\).

For \(M>2k/7\), the balanced response has both other traces strictly below \(3k/7+1/2\le k/2\) for \(k\ge7\). Their actual sizes are therefore at most \(M\), and the stronger local proposition applies. No balanced-response inequality beyond this reduction is needed.

## 4. The two unconditional residue classes

At \(k=42n\), every fixed cap and gap threshold used by the three stages is integral. The response-dependent second cap is integral as well. Reading the underlying constructions rather than their earlier rounded statements gives:

- L35: its threshold has no floor error. Its split numerator is at most \(3T\), so the actual integer split requests have size at most \(\lceil(3T-T)/2\rceil=T\).
- L37: each of the first two request sizes is an integer bounded above by \(T+1/2\), hence is at most \(T\). The combined residual allocation remains bounded by \(3T\).
- L46: the cut threshold is integral, so its initial request has no rounding loss, and the later allocations use integer capacities.
- The exact S1 criterion removes the earlier upward-rounding allowance in that construction. L29, L31, L32, L33 and S0 were already integral.

The unchanged homogeneous stage inequalities therefore give the full forbidden intersection interval at \(T=36n\). The newly checked conditional theorem closes the proof.

For rank \(42n-1\), private padding to \(42n\) preserves the transversal number: an original transversal still works; conversely, each selected new private point can be replaced by any original point of its own edge, without increasing the size or losing any previously covered original edge. It also preserves property (7,2). The resulting bound is \(36n=\lceil6(42n-1)/7\rceil\).

The final parity obstruction in the refinement note is also correct: at \(k=7n\) with odd \(n\), its specified Stage 1 cap pair costs \(6n+1\), so the unconditional exact-ceiling statement cannot be obtained by simply dropping the old extra point. This limits that prescribed cap construction, not the truth of a stronger theorem.

## Files read

- `outputs/submission_644_integer_refinement.md`
- `outputs/paper_push_six_sevenths_hand_proof.md`
- `outputs/paper_push_six_sevenths_hand_dependencies.md`

The files above were not edited by this check. The literature/venue report is separately finalized in `outputs/submission_644_literature.md`.
