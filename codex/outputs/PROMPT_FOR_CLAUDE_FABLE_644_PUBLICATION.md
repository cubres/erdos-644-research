You are taking over the final mathematical and editorial development of a paper on Erdős Problem 644. Your job is to make its proof substantially simpler, conceptually clearer, and stronger if possible, then produce a serious submission draft. Work as a research mathematician: pursue new arguments, implement improvements, and deliver the revised paper rather than stopping at recommendations.

The priority is a correct, accessible mathematical contribution. A genuinely simpler proof of the present theorem is valuable even if the coefficient cannot be improved. Do not manufacture an improvement or conceal uncertainty to satisfy my ambitions.

1. Current result and status

For a finite k-uniform hypergraph H, property (7,2) means that every subfamily of AT MOST seven edges has a transversal of size at most two. Let f(k,7) be the maximum transversal number over these families.

The current manuscript claims the complete hand-proof theorem

    f(k,7) <= ceil(6k/7), for every integer k >= 8.

It also proves the corresponding rank-at-most-k statement for nonempty edges by private padding. The general 3/4 conjecture remains unresolved. The argument does not settle k=7.

The manuscript has undergone several internal AI-assisted mathematical checks. Those checks found no remaining gap in the current argument, but they are not external refereeing or formal verification. Treat the theorem as a working claim to understand and responsibly defend, not an axiom or an externally certified result. If you find a substantive defect, report it precisely and repair it before building on it.

The primary published comparison located is Fon-Der-Flaass–Kostochka–Woodall (1999), f(k,7) <= ceil(7k/8) for k >= 8. No competing improvement was located in the recorded search; priority has not been exhaustively established.

2. Files: start with the focused package

Task root:
/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd

Current manuscript directory, relative to that root:
output/source/six_sevenths_v2/

Read README.md and general_bound.tex, then the three included files as their lemmas are needed: allocations.tex, local_closures.tex, small_maximum.tex. The complete compiled paper is output/pdf/erdos_644_six_sevenths_v2.pdf. It is 20 pages. The directory's manifest.json identifies the frozen version.

Its supporting/ directory contains the exact-ceiling hand argument, independent internal review, final integration check, earlier full-manuscript review, literature assessment, and revision record. Start with submission_644_rounding_push.md and submission_644_v2_integration_check.md if you need a compact guide. Older reports sometimes describe superseded +1 bounds; the v2 theorem above is the current target.

Authoritative broader research directory:
/Users/cubres/Documents/Clauding/erdos-hunt

The current note_644.md records the latest theorem and qualifications in sections 7.221–7.222. A delivery copy is in claude644_work/codex_exact_ceiling_20260926/. Earlier experiments and failed approaches are available in the research directory, but do not begin by rereading the entire research history or rerunning old solver campaigns.

3. Understand the architecture, then simplify it

The engine is elementary: if tau(H)>T, every set of at most T points has an avoiding edge. A good triple has empty common intersection. Four additional avoidance requests complete it to a subfamily of at most seven edges that cannot be pierced by two points. Some constructions use a previously proved global gap in pair-intersection sizes.

The main proof takes T=ceil(6k/7) and uses integer endpoints

    A=floor(T/2), B=floor((4T-2k)/3), C=T-ceil(k/2),
    D=2k-T-2B, L=D-1.

It excludes [A+1,min(B,floor(k/2))]. If B>=floor(k/2), it immediately invokes the finisher. Otherwise it excludes [D,C], then [B+1,floor(k/2)]. Consequently every pair intersection is at most T/2 or greater than k/2. A largest small intersection supplies the final contradiction.

Look for the real common mechanism behind the local lemmas. Can a single request-cover or integral-allocation theorem replace several constructions? Can an invariant or structural dichotomy replace the three-stage bookkeeping? Can the local finisher be proved directly? Can selecting the initial pair or triple more intelligently eliminate entire branches?

Aim for fewer independent ideas and fewer cases. Moving the same complexity into unexplained notation, hiding calculations, or omitting proofs is not a simplification. You may reorganize the paper completely. An illuminating asymptotic argument followed by a short exact-integer refinement is welcome if both are complete and the exact theorem is preserved.

4. Seek a stronger theorem through the actual bottlenecks

Identify every tight inequality that forces 6/7 and trace it to its underlying construction. Two useful starting points are the static allocation condition 3k+a<=4T with the estimate a<=T/2, and the finishing condition 3k+y<=4T with y<=T/2. Under those estimates, both demand T>=6k/7. Determine whether their worst cases are genuinely reachable under the preceding global exclusions, or whether additional structure gives slack.

Changing the endpoints alone may be insufficient. Try a different allocation, a sharper choice of response, a replacement local construction, or an additional useful global exclusion. Distinguish a limitation of one construction from a limitation of the full method or the theorem itself.

A complete unrestricted coefficient below 6/7 is especially valuable. Smaller finite improvements or new structural results can also matter, but keep the paper focused. Do not dilute the main result with a catalogue of unrelated computations. The 3/4 conjecture remains the long-term target; do not promise its resolution.

Use computation for discovery and counterexample finding when it helps. Turn successful ideas into hand proofs where possible. Any genuinely computer-assisted theorem needs an exact, independently checkable certificate and an explicit account of its computational dependencies. Floating-point infeasibility and finite grids do not prove an all-parameter statement.

5. Preserve the delicate points while changing the proof

All request budgets and subset sizes are integral. Preserve valid hosts, ceilings, parity cases, empty intervals, and all endpoint inclusions. The gap notation G(L,H) requires 0<=L<=H<k. In the main proof, L can be negative before the early-termination test; it is used as a gap threshold only in the valid later branch.

The maximum-small-intersection argument needs an attained pair size and the global dichotomy; an arbitrary upper bound is not an interchangeable hypothesis. The middle stage uses the FULL exact Hall criterion, including nonnegative capacities. A final obstruction must use at most seven distinct edges, even if more edges were collected during exploration. Preserve the explicit discarded-edge argument in the small-maximum case. Do not silently replace exact integer lemmas by normalized versions with an additive rounding loss.

Do one focused reconstruction to understand the proof. After that, prioritize simplification and new mathematics over repeatedly checking unchanged calculations. Validate new lemmas and every dependency affected by a rewrite; perform a final independent correctness pass on the resulting manuscript. If agents are available, separate conceptual simplification, strengthening, and skeptical checking, with disjoint editing responsibilities.

6. Publication standard and deliverables

Work in a fresh directory such as claude644_work/fable_publication_revision_YYYYMMDD/. Preserve the complete v2 package and all existing research. All notebooks and their identity artifacts must remain intact and in place. Do not interpret cleanup as permission for destructive filesystem changes.

Deliver a complete LaTeX manuscript and compiled PDF; a short change report distinguishing new theorems from exposition; a map from the old proof's lemmas to the new proof; and a portable source package with precise build instructions. Keep the proof self-contained and make its key new idea visible near the beginning. Compile and inspect the final PDF. Update the research note with fully proved new results while preserving concurrent work.

Check current primary literature before making novelty claims. Attribute the inherited avoidance and intersection-gap framework to FKW. Discrete Mathematics and Electronic Journal of Combinatorics were plausible venues in the recorded assessment; verify current instructions before adopting a submission format. Preserve an accurate account of substantial AI research and writing assistance. Leave unknown author details blank and identify the human review still required.

If a strengthening attempt fails, record the precise obstruction or missing lemma; do not write merely that it was difficult. If simplification succeeds without a stronger bound, deliver the simpler paper. If a gap remains, state exactly which theorem remains supported and which claim is conditional. Do not call the manuscript ready by concealing unfinished work.

Do not contact anyone, submit, post, or publish. I will make those decisions. Please work autonomously through useful iterations and return the strongest, clearest, honestly supported paper you can produce.
