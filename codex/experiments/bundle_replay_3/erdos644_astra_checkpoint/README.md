# Erdos 644: verified research checkpoint

The full `3/4` problem remains unresolved. The current working note gives a complete computer-assisted argument for

\[
f(k,7)\le\lceil87k/100\rceil+10\quad(k\ge1000),
\qquad c_7\le0.87<7/8.
\]

The proof applies to general families, including families with two disjoint edges. It combines hand proofs with exact rational certificates and an explicit integer rounding allowance. It has not undergone external mathematical review, and novelty or priority has not been exhaustively checked. Nothing has been posted or published. The research goal remains active.

## Main new argument

Assume the transversal number exceeds `ceil(0.87k)+10`. Every set within that budget is avoided by a family edge. An exact case certificate first excludes pair-intersection proportions in `[0.27,0.475]`. Hand arguments extend the excluded interval to `[0.18,0.5]`. A separate intersection-gap theorem then gives a contradiction.

The local case certificate uses 51 static avoidance templates and two adaptive lemmas. The stronger adaptive lemma allows the first two cuts to have different sizes. Static template budgets are reconstructed by complete rational hyperplane-arrangement enumeration and LP duality. The proof covers the entire real parameter region, not a sampled grid. There are 44 slabs and 13904 tetrahedral proof nodes. Every static template has at most 15 labels across six parts, giving a uniform rounding allowance of at most nine points per request for all integer edge sizes.

Full proof: `note_644.md`, especially Sections 7.20-7.26. The authoritative working file at `/Users/cubres/Documents/Clauding/erdos-hunt/note_644.md` has also been updated.

## Other completed results

- **Exact structured constant:** `sigma_2 = 11/20` for continuous two-part type-closed families containing both parts as edges. For every multiple of 20 with `k >= 1000`, an explicit integral construction has `(7,2)` and transversal number exactly `11k/20`.
- **Intersecting two-type extension:** for arbitrarily many parts and two fixed admissible vectors, continuous transversal coefficient greater than `3/4` forces a bad seven-tuple. This does not yet cover two arbitrary convex components. Rational witnesses scale to suitable integral multiples.
- **Concrete method obstructions:** standard shifting can destroy `(7,2)` and decrease transversal number; bounded-part exact type-closed extraction can lose essentially all transversal number; approximate Fano structure does not imply non-pierceability; two fixed types cannot simply be extracted from two convex components.
- **Sharp static obstruction:** at good-triple proportions `(1/2,1/10,1/10)`, four static requests need budget at least `7/8`. Complete enumeration covers 151341 templates and 8312 symmetry orbits. Making only the last request adaptive does not improve this threshold. The general proof uses earlier adaptivity and global intersection restrictions.
- **Verifier repair:** fixed positive cell cutoffs can falsely certify continuous wins. The replacement uses strict supports and exact rational checks of LP discoveries, with a separate exact request-budget check. It reproduces all 21 FKW test cases.

## Independent certificate replay

Extract the ZIP and run the following inside `erdos644_astra_checkpoint`. All seven checkers use only Python's standard library; `-S` disables site packages.

```sh
python3 -S p644_astra_global_bound_check.py
python3 -S p644_astra_certificate_check.py
python3 -S p644_astra_pocket_check.py
python3 -S p644_astra_two_types_check.py
python3 -S p644_astra_obstruction_check.py
python3 -S p644_astra_static_check.py
python3 -S p644_astra_static_obstruction_check.py
```

| Check | Exact evidence |
|---|---|
| General upper bound | 51 independently reconstructed static regions; 44 slabs; 13904 nodes; global and integer rounding constants |
| Earlier general-bound checkpoint | 44 slabs; 6206 nodes; coefficient 3499/4000 |
| Structured upper bound | 20 polygons; 84 rational vertex witnesses; complete triangle coverage |
| Structured lower bound | 28 type multisets; 2036 nodes; 95 rational interval duals; all 6127 maximal triple families |
| Intersecting two-type theorem | All 87 cases; 25 margin duals and 62 infeasibility duals |
| Explicit obstructions | Nine-edge shift example and an integer non-Fano bad tuple |
| Static constructions | Six rational avoidance witnesses |
| Sharp static obstruction | 151341 templates; 8312 orbits; 77 exact duals |

The bundle includes discovery programs, which may require NumPy/SciPy or SymPy. Those dependencies are unnecessary for the seven independent replays. `MANIFEST.json` records SHA-256 hashes. Certificate replays check the finite computations; the accompanying hand proofs explain why those computations imply the stated theorems.

## Remaining work and limits

The general `3/4` upper bound, the `3/4` bound restricted to two disjoint edges, the two-convex-component extension, and the proposed `13/16` general coefficient remain open. T3's less ambitious target of any coefficient below `7/8` is achieved. Further work is testing staged exclusion of pair-intersection intervals: previously forbidden intervals may simplify later local cases. Failed finite-menu searches do not establish that a general approach is impossible.

Inherited parity and small-universe computations not used in these proofs have not all been independently rerun. They remain labeled as inherited evidence in the note. The primary baseline is [Fon-Der-Flaass, Kostochka and Woodall (1999)](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdos Problem 644](https://www.erdosproblems.com/644).
