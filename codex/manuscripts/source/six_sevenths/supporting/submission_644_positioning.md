# Positioning the six-sevenths result for submission

26 September 2026. Internal editorial assessment; nothing has been submitted.

## The contribution to lead with

The central result is the general theorem

\[
 f(k,7)\le \lceil 6k/7\rceil+1\qquad(k\ge7),
\]

for the convention that every subfamily of at most seven edges has a
transversal of size at most two. It applies to arbitrary uniform families,
including families with two disjoint edges. Private padding gives the
corresponding statement for nonempty edges of rank at most k.

Fon-Der-Flaass, Kostochka and Woodall proved the upper bound
\(\lceil7k/8\rceil\) in *Discrete Mathematics* 207 (1999), 277–284.
The new leading coefficient is smaller by 1/56. Relative to the interval
between 3/4 and 7/8, this removes one seventh of the previous gap.
This is a quantitative advance on the unrestricted problem, even though
the conjectured coefficient 3/4 remains unproved.

The current proof is a hand proof. Its mathematical validity does not
depend on accepting a mixed-integer solver's infeasibility report or
replaying the search that discovered the constructions. A separate
computer certificate is useful research provenance, not a prerequisite
for reading the theorem.

The submission refinement also proves
\(f(42n,7),f(42n-1,7)\le36n\) for every n >= 1. Under the intersection
dichotomy `<= 3k/7` or `> k/2`, the sharper bound
\(\tau\le\lceil6k/7\rceil\) holds for all k >= 8. An exact four-form
integer budget replaces the earlier sufficient symmetric-allocation
criterion, and the local finishing proposition no longer needs a
balancing assumption. These are additional hand results with an
independent internal check; they are not merely changes to presentation.

Primary source: [the original FKW paper](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf),
[DOI](https://doi.org/10.1016/S0012-365X(99)00114-4).

## How strong a novelty claim is warranted

This is a plausible specialist combinatorics paper, subject to the normal
requirements that the complete proof withstand expert review and the
priority search find no equivalent earlier result. The numerical change
is modest, but it concerns the general parameter in an established open
problem. The additive constant is a secondary improvement.

Do not call the use of intersection gaps itself a new method: the 1999
proof already uses exclusions of intersection ranges. The defensible
methodological contribution is the stronger local avoidance constructions,
their three-stage combination, and the final argument using a largest
intersection of size at most half an edge. Integral allocation makes the
finite statement precise.

Do not claim a solution of Erdős Problem 644, a new universal three-quarter
bound, a proved reduction to symmetric/type-closed families, or guaranteed
journal acceptance. The literature-search report records the sources
checked and the limits of its negative findings. A search that finds no
later bound supports cautious novelty language; it cannot prove priority.

## Refined paper architecture

The focused manuscript is `work/submission_644/general_bound.tex`.

1. State the general theorem and explain its relation to the 1999 bound.
2. Define the avoidance principle and the two-point candidate pairs once.
3. Show the three explicit intersection exclusions in a short table and
   prove their scalar case divisions.
4. Prove the conditional finishing theorem using the largest small
   intersection.
5. Supply every local construction in an appendix, with ordinary lemma
   numbers, full proofs, and all integer rounding handled in the statement
   being used.

Keep discovery logs, certificate node counts, failed approaches, and
unrelated structured cases out of this article's main argument. Preserve
them in the research archive. The sharp structured three-quarter theorems
may support a companion paper after their own focused literature and proof
review; adding them here would obscure the central contribution.

## The claim an eventual submission can make

> We improve the upper bound of Fon-Der-Flaass, Kostochka and Woodall for
> uniform hypergraphs with property (7,2), replacing the leading coefficient
> 7/8 by 6/7. We give a self-contained proof based on explicit avoidance
> constructions and integral allocations.

Use this only with the complete manuscript, and qualify any claim that it
is the *first* improvement according to the evidence in the literature
report. Authors, affiliations, funding, contribution statements, and
declarations must be supplied truthfully by the submitting humans.

## Submission status

The research package contains a complete written argument and internal
checks by multiple AI agents. That is not an independent human referee
report. Before submission, the human authors need to read and take
responsibility for the proof and references, and use the target journal's
current disclosure requirements for the substantial AI assistance in
research and writing. No statement that this human review has already
occurred has been inserted into the manuscript.

Venue scope, current policies, and search provenance are recorded in
`outputs/submission_644_literature.md`.
