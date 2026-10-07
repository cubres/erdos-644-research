# Erdős 644: verified research checkpoint

The full `3/4` problem remains unresolved. The working note gives the complete computer-assisted argument

\[
f(k,7)\le\lceil43k/50\rceil+10\quad(k\ge1000),
\qquad c_7\le43/50=0.86<7/8.
\]

It applies to general families, including those with disjoint edges. The proof has exact rational certificates, full hand lemmas, and explicit integer rounding. External mathematical review and a comprehensive priority check remain outstanding. Nothing has been published. The research goal remains active.

## Main argument

Assume the transversal number exceeds `ceil(43k/50)+10`. A 204-step chronological certificate excludes all pair-intersection proportions in `[0.14,0.5]`. The first 67 steps use unconditional constructions. Later steps use only previously established gaps, including a new partial-core lemma that needs just one small new trace. The conditional 5/6 theorem then gives a contradiction.

The certificate has **22,290 cover nodes**, including 15,390 in the initial unconditional stage. It uses 75 static templates and adaptive hand lemmas, covering complete real parameter regions. The 137 later steps record their prior gaps, so dependencies can be checked without circular assumptions. Static budgets are independently reconstructed by rational hyperplane-arrangement enumeration and LP duality. Each static template has at most 15 labels across six parts, so restoring integer part totals adds at most nine points to any request. The partial-core proofs explicitly include their domain conditions and integer rounding.

Full proof: Theorem 7.44 in `note_644.md`, Section 7.45, with preceding lemmas. The authoritative file under `/Users/cubres/Documents/Clauding/erdos-hunt/` is also updated. Earlier bounds `31/36`, `0.862`, `0.865`, `0.87`, and `3499/4000` remain valid but are weaker.

## Further completed results

- **Conditional 5/6 theorem:** if every pair intersection is at most `k/4` or greater than `k/2`, then `tau <= ceil(5k/6)+4`. Theorem 7.42 is a hand proof using a second adaptive response. This does **not** establish a general 5/6 bound.
- **Exact structured constant:** `sigma_2 = 11/20` for continuous two-part type-closed families containing both parts as edges. Explicit integral constructions attain `11k/20` for multiples of 20 with `k >= 1000`.
- **Intersecting two-type theorem:** for two fixed admissible vectors over any number of parts, continuous transversal coefficient above `3/4` forces a bad seven-tuple. Two arbitrary convex components remain open.
- **Exact method limits:** four static requests need `7/8` at a specified good triple; a partial-core response also needs `7/8` for three fixed final requests; another complementary-pair configuration has fixed-request optimum `11/13`. The new later-adaptive lemma handles that last configuration below `11/13` using the global intersection gap.
- **Structural obstructions:** explicit counterexamples invalidate ordinary shifting, bounded-part exact type closure, a compulsory Fano conclusion, and extraction of two representative types from two convex components.
- **Verifier repair:** positive occupancy cutoffs can report false continuous wins. The replacement checks strict supports and rational LP certificates, with separate request-budget verification.

## Independent replay

Run these inside the adjacent `certificates_086` directory. All fifteen use only Python's standard library; `-S` disables site packages. Earlier certificate directories and the old ZIP are preserved checkpoints.

```sh
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

The newest general-bound replay checks all chronological dependencies, rational leaves and subdivisions, domain conditions, maximum-small-intersection bounds, the final conditional theorem, and integer allowances. The matching checker enumerates all 5,832 templates and ten rational price vertices, proving the stated fixed-allocation limit. The other replays retain earlier proofs and method obstructions. `MANIFEST.json` contains SHA-256 hashes.

Discovery programs and representative strategy checks may require NumPy/SciPy or SymPy. In particular, `p644_partial_gap.py` checks both sides of the rounding boundary; `p644_gap_second_adaptive.py` checks both branches of the later-adaptive construction; and `p644_gap_one_trace.py` checks both allocation cases of the new single-trace lemma. Universal validity is established by the accompanying hand proofs, not inferred from these representative cases.

## Remaining work

The general `3/4` bound, its restriction to two disjoint edges, the two-convex-component extension, and the proposed `13/16` general coefficient remain open. T3's target of an improvement below `7/8` is achieved. Research at `6/7` continues; no general bound at that coefficient is claimed. Proposition 7.45 gives a precise obstacle: a legal fourth response respects the current three excluded intervals, but its three final fixed requests need exactly `0.891k`. All 16,527 templates are checked. Another initial request or later adaptivity can still work; this is not an impossibility result for the general problem.

Inherited parity and small-universe computations unused by the new proofs have not all been independently rerun and remain labeled as inherited evidence. The baseline is [Fon-Der-Flaass, Kostochka and Woodall (1999)](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdős Problem 644](https://www.erdosproblems.com/644).
