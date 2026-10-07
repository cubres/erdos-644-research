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
- **Intersecting non-convex theorems:** two fixed admissible vectors over any number of parts are covered. The new Theorem 7.54 also covers a union of two closed convex type intervals over two parts of arbitrary capacities: coefficient above `3/4` forces a continuous bad seven-tuple. Its interior-endpoint case has a hand proof; the complete boundary analysis has 188 independently checked rational duals. A rank-2440 example is verified explicitly. Rational witnesses scale to suitable multiples; no uniform all-scales rounding claim is made. More than two parts remains open.
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

Lemma 7.50 generalizes the conditional finishing theorem: for beta at least 5/6, a gap from `(3 beta - 2)k/2` to `k/2` suffices at budget `ceil(beta k)+4`. Lemma 7.51 records a bound on the minimum intersection sum of a good triple and the resulting constraints on later responses. Both have full hand proofs. Sections 7.51–7.57 contain these results, the new two-interval theorem, and the precise current limitations.

## Remaining work

The general `3/4` bound, its restriction to two disjoint edges, the two-convex-component extension over more than two parts, and the proposed `13/16` general coefficient remain open. T3's target of an improvement below `7/8` is achieved. The changed first request gets past Proposition 7.45's `0.891k` fixed-response obstruction. Proposition 7.49 shows a new precise limitation: even with strict intersection gaps, three fixed final requests can require budgets approaching `6k/7`. Another initial request, later adaptivity, or further consequences of a large transversal number remain credible routes. This is not a lower bound on the original problem. The goal remains active.

Inherited parity and small-universe computations unused by the new proofs have not all been independently rerun and remain labeled as inherited evidence. The baseline is [Fon-Der-Flaass, Kostochka and Woodall (1999)](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdős Problem 644](https://www.erdosproblems.com/644).
