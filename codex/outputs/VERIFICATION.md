# Erdős 644: verified research checkpoint

The full `3/4` problem remains unresolved. The working note gives the complete computer-assisted argument

\[
f(k,7)\le\lceil6k/7\rceil+10\quad(k\ge1000),
\qquad c_7\le6/7=0.857142\ldots<7/8.
\]

It applies to general families, including those with disjoint edges. The proof has exact rational certificates, full hand lemmas, and explicit integer rounding. External mathematical review and a comprehensive priority check remain outstanding. Nothing has been published. The research goal remains active.

## Main argument

Assume the transversal number exceeds `ceil(6k/7)+10`. A 256-step chronological certificate excludes all pair-intersection proportions in `[0.143,0.5]`. The first 41 steps use unconditional constructions. Later steps use only previously established gaps. A new construction keeps two triple cells after the fourth response, and a further trace dichotomy closes the last middle interval. The conditional 5/6 theorem then gives a contradiction.

The certificate has **18,270 cover nodes**. It uses 75 static templates and adaptive hand lemmas, covering complete real parameter regions. The 215 later steps record their prior gaps, so dependencies can be checked without circular assumptions. The last step has four boxes with 112 nodes in total. Static budgets are independently reconstructed by rational hyperplane-arrangement enumeration and LP duality. Each static template has at most 15 labels across six parts, so restoring integer part totals adds at most nine points to any request. The new hand constructions include all domain conditions and integer rounding.

Full proof: Theorem 7.48 in `note_644.md`, Section 7.49, with preceding lemmas. The authoritative file under `/Users/cubres/Documents/Clauding/erdos-hunt/` is also updated. Earlier bounds `43/50`, `31/36`, `0.862`, `0.865`, `0.87`, and `3499/4000` remain valid but are weaker.

## Further completed results

- **Conditional 5/6 theorem:** if every pair intersection is at most `k/4` or greater than `k/2`, then `tau <= ceil(5k/6)+4`. Theorem 7.42 is a hand proof using a second adaptive response. This does **not** establish a general 5/6 bound.
- **Exact structured constant:** `sigma_2 = 11/20` for continuous two-part type-closed families containing both parts as edges. Explicit integral constructions attain `11k/20` for multiples of 20 with `k >= 1000`.
- **Intersecting non-convex theorems:** two fixed admissible vectors over any number of parts are covered. The new Theorem 7.54 also covers a union of two closed convex type intervals over two parts of arbitrary capacities: coefficient above `3/4` forces a continuous bad seven-tuple. Its interior-endpoint case has a hand proof; the complete boundary analysis has 188 independently checked rational duals. A rank-2440 example is verified explicitly. Rational witnesses scale to suitable multiples; no uniform all-scales rounding claim is made. The new Theorem 7.59 also covers two sliced-box components over three parts; its thirteen exact systems have independently reconstructed inputs and externally checked CPC proofs. Arbitrary convex components and the full problem remain open.
- **A further exact obstruction:** Proposition 7.55 gives a two-part family of coefficient `4/5` with a bad five-tuple but no tuple supported on the downward closure of the complements of one Fano plane. Thus those templates cannot simply drop the intersecting hypothesis.
- **Exact method limits:** four static requests need `7/8` at a specified good triple; a partial-core response also needs `7/8` for three fixed final requests; another complementary-pair configuration has fixed-request optimum `11/13`. The new later-adaptive lemma handles that last configuration below `11/13` using the global intersection gap.
- **Structural obstructions:** explicit counterexamples invalidate ordinary shifting, bounded-part exact type closure, a compulsory Fano conclusion, and extraction of two representative types from two convex components.
- **Verifier repair:** positive occupancy cutoffs can report false continuous wins. The replacement checks strict supports and rational LP certificates, with separate request-budget verification.

## Independent replay

Run these inside the adjacent `certificates_6_7_two_intervals` directory. All nineteen use only Python's standard library; `-S` disables site packages. Earlier certificate directories and the old ZIP are preserved checkpoints.

```sh
python3 -S p644_astra_six_sevenths_check.py
python3 -S p644_astra_below_six_sevenths_check.py
python3 -S p644_astra_two_intervals_check.py
python3 -S p644_astra_two_triple_obstruction_check.py
python3 -S p644_astra_one_trace_check.py
python3 -S p644_astra_gap_response_obstruction_check.py
python3 -S p644_astra_31_36_check.py
python3 -S p644_astra_gap_matching_check.py
python3 -S p644_astra_interval_bound_check.py
python3 -S p644_astra_global_bound_check.py
python3 -S p644_astra_maxsmall_check.py
python3 -S p644_astra_partial_tree_obstruction.py
python3 -S p644_astra_frontier_check.py
python3 -S p644_astra_certificate_check.py
python3 -S p644_astra_pocket_check.py
python3 -S p644_astra_two_types_check.py
python3 -S p644_astra_obstruction_check.py
python3 -S p644_astra_static_check.py
python3 -S p644_astra_static_obstruction_check.py
```

The newest general-bound replay checks all chronological dependencies, rational leaves and subdivisions, domain conditions, maximum-small-intersection bounds, the final conditional theorem, and integer allowances. The two-triple obstruction checker covers all 6,194,025 label templates through 665,408 exact cases, then verifies a symbolic strict-gap perturbation. The other replays retain earlier proofs and method obstructions. `MANIFEST.json` contains SHA-256 hashes.

Discovery programs and representative strategy checks may require NumPy/SciPy or SymPy. In particular, `p644_gap_two_triples.py` checks cases with and without surviving triple cells; `p644_gap_trace_dichotomy.py` checks its three response branches. Earlier strategy checks are also retained. Universal validity is established by the accompanying hand proofs, not inferred from these representative cases.

## Current work below 6/7

At budget `107/125 = 0.856`, the refined 55-step certificate has 4,716 exact nodes and gives the partial gaps `[0.196,0.212]`, `[0.267,0.356]`, and `[0.432,0.474]`. The earlier 35-step certificate is retained and replayed too. They do not establish a general 0.856 bound. The new independent checker also evaluates 187 sufficient regions at the feasible triple `(0.4,0.086,0.372)`: the minimum listed budget is exactly `0.8572`, so this finite menu does not close that triple. Different cap choices and adaptive requests remain open. A subsequent search, including starting pairs above half the rank, completed three passes and found no additional exclusions on its last pass. It certified no exclusions above half the rank. This finite search result is not an impossibility claim.

Lemma 7.50 generalizes the conditional finishing theorem: for beta at least 5/6, a gap from `(3 beta - 2)k/2` to `k/2` suffices at budget `ceil(beta k)+4`. Lemma 7.51 records a bound on the minimum intersection sum of a good triple and the resulting constraints on later responses. Both have full hand proofs. Sections 7.51–7.57 contain these earlier results. The new results below are in Sections 7.58–7.73.

## Remaining work

The general `3/4` bound, its restriction to two disjoint edges, the two-convex-component extension over more than two parts, and the proposed `13/16` general coefficient remain open. T3's target of an improvement below `7/8` is achieved. The changed first request gets past Proposition 7.45's `0.891k` fixed-response obstruction. Proposition 7.49 shows a new precise limitation: even with strict intersection gaps, three fixed final requests can require budgets approaching `6k/7`. Another initial request, later adaptivity, or further consequences of a large transversal number remain credible routes. This is not a lower bound on the original problem. The goal remains active.

Inherited parity and small-universe computations unused by the new proofs have not all been independently rerun and remain labeled as inherited evidence. The baseline is [Fon-Der-Flaass, Kostochka and Woodall (1999)](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdős Problem 644](https://www.erdosproblems.com/644).

## Three-part theorem and new exact tools (21 September)

Theorem 7.59 proves the continuous 3/4 threshold for intersecting families defined by two convex boxes sliced by the rank-one plane over three parts. This is a structured theorem, not a full resolution. Rational witnesses scale to suitable multiples only.

The new three-versus-four Fano construction was necessary: Proposition 7.58 gives an explicit intersecting family with coefficient 19/25 for which all four orientations of the older templates fail. Its new integral bad tuple has rank 100 and was independently checked.

The portable `three_part_box_certificate` bundle contains thirteen complete proof inputs, cvc5 CPC contradiction proofs, an independent mathematical-input auditor, the standalone Ethos checker with matching signatures, licenses, provenance, and 124 SHA-256 hashes. All thirteen cases passed the portable replay. Run:

```sh
python3 -S three_part_box_certificate/p644_box_certificate_check.py
```

No SMT solver is needed for replay. The bundled executable is for macOS arm64; `--ethos` selects another compatible Ethos 0.2.4 executable. This checks a finite exact reduction; it is not a claim that the entire mathematical note has been formalized.

Further additions in `research_extensions`:

- Lemma 7.63 now has a full hand proof of the Fano capacity formula. The independent enumeration of all 3432 rational bases confirms its sixteen dual vertices. This reduces arbitrary seven-type Fano realizability to fifteen nontrivial linear inequalities per part. Run `python3 -S p644_fano_capacity_check.py` there.
- Proposition 7.64 gives exact response obstructions for all three ways to omit one unit from one pair cell in the current 0.856 hole, even retaining the available minimum-sum constraints. Run `python3 -S p644_minimum_response_obstruction_check.py` there; each of the three examples checks all 16527 label assignments.
- Full hand proofs give the usual fractional-cover bound and an intersecting pocket-family obstruction to reducing the fractional covering number to 7/4 by deleting o(k) vertices. A new local minimum-sum lemma closes an exactly balanced triple at budget 3k/4, but its domain is not forced for general families.
- Four-part numerical discovery found Fano witnesses in all 3510 qualifying visits among 10000 local mutations. The first exact four-part batch had one UNSAT and 21 UNKNOWN outcomes at 60 seconds per case; no four-part theorem is asserted. A refined batch excluding homogeneous witnesses is ongoing.

The unrestricted bound remains 6/7. Further work is still needed to obtain the full 3/4 coefficient. Nothing has been published.


## Complete-support and adaptive tools (21 September, later checkpoint)

Sections 7.67–7.70 add the following, without changing the general 6/7 bound:

- A complete catalogue of 715 relevant bad-seven supports, verified by an independent count and permutation-orbit check against the primary authors' truth tables. The intersecting subcatalogue has 604 classes.
- A complete decision procedure for two rational sliced boxes over any number of parts, using 54,214 support/component assignments. Every accepted result has exact primal or Farkas certificates. The narrow pocket example passes all 54,214 negative checks; three known failing examples have explicit, independently checked bad tuples.
- A hand formula for the exact cost of two final pair-cover requests. Its implementation passes 1,024 small graph/mass checks. A zero-neighbor error found in its first discovery version is explicitly corrected; those original adaptive outputs are not certificates.
- Stronger local method obstructions compatible with the current intersection gaps: all 326, 328 and 325 whole-cell first requests in three specific states have independently verified adversarial responses defeating two simultaneous final requests. These do not rule out partial-cell requests or further adaptivity.

The files and replay instructions are in `research_extensions`. Four-part SMT and partial-cell strategy searches remain discovery work; timeouts and unfinished synthesis are not infeasibility proofs. The research goal remains active.


## Complete two-type results (21 September, newest checkpoint)

Theorem 7.69 gives a complete 42-function criterion for bad seven-tuples in families with two fixed types over arbitrary parts and capacities. All 54,214 support/colour assignments, 375,446 rational LP certificates and the exact dominance reduction to 42 functions passed independent replay. The portable `two_type_capacity_certificate` bundle stores the full data in a 10.84 MB lossless archive; its nine file hashes pass.

Theorem 7.71 removes the intersecting hypothesis from the earlier two-fixed-type 3/4 theorem. Its nonintersecting branch reduces to 125 root cases and a complete 107-node refinement. Independent standard-library verification checks 120 root duals, 101 leaf duals, all six case splits and three additional construction templates. The earlier 87-case intersecting proof also passed again. The small `two_fixed_types_certificate` bundle replays the theorem without the large capacity catalogue.

Lemma 7.70 is a new hand construction from the three perfect matchings of K4, with exact capacity max(2s/3+t,4s/3+t/2). Adding it did not close the four selected four-part cases within 180 seconds; those are UNKNOWN, not impossibility results. The three-part two-box extension below has since completed.

The unrestricted general coefficient remains 6/7. Neither the two-fixed-type theorem nor the capacity classification supplies the missing reduction for arbitrary families. The research goal remains active; nothing has been published.

## Arbitrary two-part type sets and general three-part boxes

Theorem 7.73 removes intersectingness from the three-part two-box theorem. All thirteen mixed-disjoint systems passed independent mathematical-input audits and cvc5/Ethos checks. The full portable replay also passed: all 174 manifest hashes, both thirteen-case branches, and the additional capacity constructions in `three_part_general_box_certificate`.

Theorem 7.75 proves the 3/4 threshold for every closed admissible type set over two parts, without convexity or intersectingness. Its independent standard-library replay passed all 640 rational dual leaves and the explicit support/capacity constructions, again from `all_two_part_types_certificate`. Run `python3 -B -S all_two_part_types_certificate/p644_two_part_gap_check.py`.

Corollary 7.76 gives the uniform finite bound `tau <= floor(3k/4)+28` for every k-uniform (7,2)-family invariant under permutations within two parts. The full hand proof is in section 7.77. It permits arbitrary allowed integer types that vary with k.

The 1,190-point capacity scan guided discovery but is not proof evidence. The rational pruning experiment checked 4,940 branch eliminations; its reduced SMT timeouts are not used by the theorem. Lemma 7.72 gives the separate hand obstruction to adapting only the final avoidance request in the unrestricted response model.

The general problem remains open in this work, with proved general coefficient 6/7. Nothing has been published. The research goal remains active.

## Higher-dimensional method obstruction

Lemma 7.77 gives a sufficient test using the deletion cost of a box of partner types. Proposition 7.78 proves that one round of all 42 such tests is insufficient: a three-part family of coefficient 39/50 survives every test at budget 3/4, although an explicit pair of its types has a bad seven-tuple. All 31 infeasibility duals, 11 coordinate upper bounds, capacity certificates and bad-pair evaluations passed independent replay, including the portable `partner_budget_barrier_certificate` copy. The full hand transversal calculation and the exact scope of the obstruction are in section 7.78.

Proposition 7.79 is a stronger obstruction to using only pairs of actual types: nine rational three-part types have coefficient 483/640, while every two-type subfamily has (7,2). The whole family has independently checked bad tuples. The portable `three_part_two_type_barrier_certificate` replay passed all 3,402 exact pair exclusions, both exhaustive transversal calculations and both positive witnesses. Its completeness dependency was also replayed again: all 54,214 support-colour capacities, 375,446 rational LP certificates and 11,865 dominance checks passed in `two_type_capacity_certificate`.

The continuous type-cell pipeline treats entire triangles and therefore avoids interpreting a sampled grid as a continuous theorem. It now adds verified exclusions involving several actual types, using the Fano capacity formula and fifteen explicit bad parent supports. Current SAT relaxations and timeouts are discovery results; no new universal three-part theorem is asserted. The three continuous response searches using only pairs ended UNKNOWN, and Proposition 7.79 now explains the broader limitation of that information restriction.

## Arbitrary types at three equal capacities

Theorem 7.80 now proves the continuous 3/4 bound at capacities (4r/5,4r/5,4r/5), for an arbitrary admissible type set. The whole-cell certificate covers 1212 triangles and uses 496 residual queries and 556 multi-type region exclusions, of which five use a parent support beyond the Fano construction. The independently reconstructed formula has 538035 clauses.

The mathematical input audit passed. DRAT-trim and its LRAT checker passed, and the separate standard-library RUP-only checker independently verified 74164 derived clauses and 11471059 unit-propagation steps. The portable `three_equal_parts_certificate` bundle includes a losslessly compressed proof and its two standalone replay commands. The stronger threshold 29r/40 remains only a SAT relaxation of the present discretization. The theorem is continuous and at the stated capacities; no general integer-rounding extension or arbitrary-capacity theorem is claimed.

The general coefficient remains 6/7. A global structural reduction for arbitrary families is still missing; computational progress alone does not establish a timetable for a full proof. Research remains active, external review is outstanding, and nothing has been published.
