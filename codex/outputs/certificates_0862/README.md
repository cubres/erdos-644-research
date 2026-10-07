# Erdős 644: verified research checkpoint

The full `3/4` problem remains unresolved. The working note now gives the complete computer-assisted argument

\[
f(k,7)\le\lceil431k/500\rceil+10\quad(k\ge1000),
\qquad c_7\le0.862<7/8.
\]

It applies to general families, including those with disjoint edges. The proof has exact rational certificates, full hand lemmas, and an explicit integer rounding allowance. External mathematical review and a comprehensive priority check remain outstanding. Nothing has been published. The research goal remains active.

## Main argument

Assume the transversal number exceeds `ceil(0.862k)+10`. Every set within that budget has an avoiding edge. A certificate with 57 chronological steps excludes pair-intersection proportions in `[0.18,0.375]` and `[0.39,0.48]`. A conditional hand lemma and a 38-node cover extend the upper interval through `0.5`. A further 112-node cover closes the middle gap. The resulting gap `[0.18,0.5]` invokes the previously proved intersection-gap theorem and gives a contradiction.

The full certificate has 4,562 cover nodes and uses 75 static templates together with adaptive hand lemmas. It covers complete real parameter regions. Static template budgets are independently reconstructed by rational hyperplane-arrangement enumeration and LP duality. Every template has at most 15 labels across six parts; restoring integer part totals adds at most nine points to a request.

Full proof: `note_644.md`, Theorem 7.36 in Section 7.38, with the hand lemmas in preceding sections. The authoritative file under `/Users/cubres/Documents/Clauding/erdos-hunt/` is also updated. Earlier bounds `0.865`, `0.87`, and `3499/4000` remain valid but are weaker.

## Other completed results

- The structured constant is exactly `sigma_2 = 11/20` for continuous two-part type-closed families containing both parts as edges. An explicit integral construction attains `11k/20` for multiples of 20 with `k >= 1000`.
- For intersecting families specified by two fixed type vectors over any number of parts, continuous transversal coefficient above `3/4` forces a bad seven-tuple. Two arbitrary convex components remain open.
- Three new integral hand lemmas handle a surviving triple cell and choose allocations after seeing the fourth edge. All eight representative response branches pass strict-support and budget checks.
- Standard shifts, bounded-part exact type closure, a compulsory Fano conclusion, and extraction of two representative types have explicit obstructions.
- Four static requests at `(1/2,1/10,1/10)` require `7/8`; complete enumeration checks 151,341 templates. A new explicit four-edge response also requires exactly `7/8` for three fixed final requests; all 16,527 relevant tree templates are checked. Neither obstruction excludes later adaptivity.
- The inherited positive-cutoff verifier can report false continuous wins. The replacement checks strict supports and rational LP certificates, separately checking request budgets.

## Independent replay

Run these inside the adjacent `certificates_0862` directory. All eleven use only Python's standard library; `-S` disables site packages. The existing ZIP is an earlier 0.865 checkpoint and has been preserved unchanged.

```sh
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

The newest general-bound replay checks all 57 chronological steps, reconstructs prior exclusions before each use, checks both final gap covers, and checks the global and rounding constants. Other checks retain the structured upper/lower certificates, all 87 two-type cases, explicit counterexamples, earlier global bounds, and the precise limits of incomplete search menus. `MANIFEST.json` records SHA-256 hashes. Numerical discovery programs may require NumPy/SciPy or SymPy; the independent replays do not.

## Remaining gaps

The general `3/4` bound, its restriction to two disjoint edges, the two-convex-component extension, and the proposed `13/16` coefficient remain open. T3's target of any improvement below `7/8` is achieved. At target `31/36`, one certified menu covers maximum-small-intersection boxes through `0.48125` and has an exact rational hole beyond that. Chronological interval exclusion gets further but has not closed all gaps at that budget. These are limits of stated methods, not impossibility claims about the problem.

Inherited parity and small-universe computations unused by the new proofs have not all been independently rerun and remain labeled as inherited evidence. The baseline source is [Fon-Der-Flaass, Kostochka and Woodall (1999)](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdős Problem 644](https://www.erdosproblems.com/644).
