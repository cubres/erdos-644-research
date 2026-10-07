# Erdős 644 — Astra research checkpoint

The full Erdős problem remains unresolved. No improved general bound on `c_7` is claimed. The research goal remains active; this bundle records completed work so it can be reviewed independently while the general cases continue.

## Completed results

- **Exact structured constant:** `sigma_2 = 11/20` in the continuous two-part type-closed model. The lower construction is fully integral: for every multiple of 20 with `k >= 1000`, include the two disjoint parts as edges and all `k`-sets with first-part trace `k/4 - 1` or `7k/10 + 1`. This family has `(7,2)` and transversal number exactly `11k/20`.
- **Intersecting two-type extension:** for any number of parts and two fixed admissible vectors, continuous transversal coefficient greater than `3/4` forces a bad seven-tuple. This covers two points, not two arbitrary convex components. Rational witnesses scale to suitable integral multiples.
- **Two good-triple lemmas:** a seven-edge hand proof replaces the inherited eight-edge example; a separate static construction gives budget `6r/7` at intersection proportions `(1/2,1/4,1/4)` and covers an explicit neighbourhood at budget `0.87r`.
- **Concrete obstructions:** standard shifts can destroy `(7,2)` and can decrease transversal number; bounded-part exact type-closed extraction can lose essentially all transversal number; approximate Fano structure does not imply non-pierceability; the exact Fano conclusion fails for non-convex intersecting two-type families. Selecting two types also fails as a reduction for two convex components.
- **Verifier correction:** a fixed positive cell cutoff can produce false continuous “wins.” The new verifier uses convexity of feasible mass vectors and exact rational checks of LP discoveries, with no occupancy cutoff.

Full statements, proofs, qualifications, and remaining gaps are in `note_644.md`, particularly §§7.1–7.13. The working copy at `/Users/cubres/Documents/Clauding/erdos-hunt/note_644.md` has been updated too.

## Independent certificate replay

Extract the ZIP and run these commands inside its `erdos644_astra_checkpoint` directory. They use only Python's standard library; `-S` disables site-package loading.

```sh
python3 -S p644_astra_certificate_check.py
python3 -S p644_astra_pocket_check.py
python3 -S p644_astra_two_types_check.py
python3 -S p644_astra_obstruction_check.py
python3 -S p644_astra_static_check.py
```

Expected results:

| Check | Exact certificate |
|---|---|
| Structured upper bound | 20 polygons, 84 rational vertex witnesses, complete triangle coverage |
| Pocket interval lower bound | 28 type multisets, 2036 proof nodes, 95 rational interval duals, all 6127 maximal triple families covered |
| Intersecting two-type theorem | All 87 coordinate/support/order cases; 25 margin duals and 62 infeasibility duals |
| Explicit obstructions | Nine-edge shift example and an integer non-Fano bad tuple |
| Static requests | Six rational avoidance witnesses, including the `6/7` lemma |

The discovery programs are included. They use NumPy/SciPy, and some geometric reconstruction uses SymPy; none is needed for these five certificate replays. `MANIFEST.json` records SHA-256 hashes of bundle contents.

## What remains

T1 still needs a method that reaches general families: the two-convex-component extension and control of outside intersections remain open. T2 has no general `3/4` bound yet. T3 needs a complete, legally budgeted case cover and a justified passage to the intended integer/asymptotic setting. The new local lemmas do not supply that cover.

The new strict-support verifier reproduces all 21 FKW test triples even without assuming intersectingness. It also gives rational survivors for the tested clustered scripts and the first-seven-edge truncation of the inherited example. These are obstructions to specific scripts, not universal impossibility theorems. The old fixed-cutoff results cannot be accepted without re-verification.

The inherited parity and small-universe computations not used in the new proofs have not all been independently rerun. Novelty and priority have not been exhaustively checked. The primary 1999 reference is [Fon-Der-Flaass–Kostochka–Woodall](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf); the original question is [Erdős Problem 644](https://www.erdosproblems.com/644).

No material has been posted or published.
